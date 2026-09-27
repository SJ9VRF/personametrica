from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from personalbench.belief_benchmark import BenchmarkConfig, TimeAwareLatestTracker, BeliefStateTracker, generate_user_stream
from scripts.calibrated_baseline_eval import collect_raw, fit_bucket_calibrator, eval_rows

DEV_SEEDS = (1, 2, 3)
TEST_SEEDS = tuple(range(30, 40))
THRESHOLDS = (0.55, 0.65, 0.70, 0.75, 0.85)
DEFER_COSTS = (0.00, 0.05, 0.10, 0.20, 0.35)
METHODS = {
    'time-aware-latest': TimeAwareLatestTracker,
    'personal-belief-state': BeliefStateTracker,
}


def streams(seed: int, *, users: int = 40, turns: int = 800, query_every: int = 50):
    cfg = BenchmarkConfig(users=users, turns=turns, seed=seed, query_every=query_every)
    return [generate_user_stream(i, cfg) for i in range(users)]


def fit_isotonic_calibrator(rows):
    # Pool-adjacent-violators over confidence buckets. Fit on development labels only.
    grouped = defaultdict(lambda: [0, 0])
    for _, _, conf, ok in rows:
        k = round(float(conf), 2)
        grouped[k][0] += int(ok)
        grouped[k][1] += 1
    blocks = []
    for k in sorted(grouped):
        correct, n = grouped[k]
        # Laplace smoothing avoids degenerate 0/1 estimates for tiny bins.
        blocks.append({'xs': [k], 'sum': correct + 1.0, 'n': n + 2.0})
    i = 0
    while i < len(blocks) - 1:
        a = blocks[i]['sum'] / blocks[i]['n']
        b = blocks[i+1]['sum'] / blocks[i+1]['n']
        if a <= b + 1e-12:
            i += 1
            continue
        merged = {
            'xs': blocks[i]['xs'] + blocks[i+1]['xs'],
            'sum': blocks[i]['sum'] + blocks[i+1]['sum'],
            'n': blocks[i]['n'] + blocks[i+1]['n'],
        }
        blocks[i:i+2] = [merged]
        i = max(0, i-1)
    mapping = {}
    for block in blocks:
        value = block['sum'] / block['n']
        for x in block['xs']:
            mapping[x] = value
    keys = sorted(mapping)
    def cal(c):
        if not keys:
            return float(c)
        k = min(keys, key=lambda x: abs(x - round(float(c), 2)))
        return mapping[k]
    return mapping, cal


def identity(c):
    return float(c)


def mean(xs):
    return sum(xs) / max(1, len(xs))


def entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)


def main():
    # Generate each synthetic history exactly once per seed, then replay every tracker on the same histories.
    dev_streams = {seed: streams(seed, users=60, turns=240, query_every=24) for seed in DEV_SEEDS}
    long_streams = {seed: streams(seed) for seed in TEST_SEEDS}
    dev_rows = {}
    test_rows = {}
    for name, cls in METHODS.items():
        rows = []
        for seed in DEV_SEEDS:
            rows.extend(collect_raw(cls, dev_streams[seed]))
        dev_rows[name] = rows
        test_rows[name] = {seed: collect_raw(cls, long_streams[seed]) for seed in TEST_SEEDS}

    calibrators = {'native': {name: ({}, identity) for name in METHODS}}
    bucket = {}
    isotonic = {}
    for name in METHODS:
        bucket[name] = fit_bucket_calibrator(dev_rows[name])
        isotonic[name] = fit_isotonic_calibrator(dev_rows[name])
    calibrators['bucket-laplace'] = bucket
    calibrators['isotonic-laplace'] = isotonic

    cells = []
    wins = defaultdict(int)
    ties = 0
    signs = []
    for cal_name, per_method in calibrators.items():
        for threshold in THRESHOLDS:
            for defer_cost in DEFER_COSTS:
                per_seed = {}
                for method in METHODS:
                    cal = per_method[method][1]
                    vals = [eval_rows(test_rows[method][seed], cal, threshold=threshold, defer_cost=defer_cost)['decision_utility'] for seed in TEST_SEEDS]
                    per_seed[method] = vals
                a = mean(per_seed['time-aware-latest'])
                b = mean(per_seed['personal-belief-state'])
                delta = b - a
                if delta > 1e-12:
                    winner = 'personal-belief-state'; wins[winner] += 1; signs.append(1)
                elif delta < -1e-12:
                    winner = 'time-aware-latest'; wins[winner] += 1; signs.append(-1)
                else:
                    winner = 'tie'; ties += 1; signs.append(0)
                cells.append({
                    'calibration': cal_name,
                    'threshold': threshold,
                    'defer_cost': defer_cost,
                    'time_aware_utility': a,
                    'pbs_utility': b,
                    'pbs_minus_time_aware': delta,
                    'winner': winner,
                    'per_seed_delta': [p-t for p,t in zip(per_seed['personal-belief-state'], per_seed['time-aware-latest'])],
                })

    total = len(cells)
    p_pbs = wins['personal-belief-state'] / total
    p_time = wins['time-aware-latest'] / total
    p_tie = ties / total
    # Pairwise rank-reversal rate: probability two randomly selected protocol cells select opposite winners.
    n_pos = wins['personal-belief-state']; n_neg = wins['time-aware-latest']
    pair_denom = total * (total - 1) / 2
    reversal_pairs = n_pos * n_neg
    reversal_rate = reversal_pairs / pair_denom if pair_denom else 0.0
    winner_entropy = entropy([p_pbs, p_time, p_tie])

    by_cal = {}
    for cal_name in calibrators:
        subset = [c for c in cells if c['calibration'] == cal_name]
        by_cal[cal_name] = {
            'cells': len(subset),
            'pbs_wins': sum(c['winner']=='personal-belief-state' for c in subset),
            'time_aware_wins': sum(c['winner']=='time-aware-latest' for c in subset),
            'ties': sum(c['winner']=='tie' for c in subset),
            'mean_delta': mean([c['pbs_minus_time_aware'] for c in subset]),
        }

    result = {
        'version': '4.2.0',
        'development_seeds': DEV_SEEDS,
        'long_horizon_test_seeds': TEST_SEEDS,
        'protocol_grid': {
            'calibration': list(calibrators),
            'thresholds': THRESHOLDS,
            'defer_costs': DEFER_COSTS,
            'cells': total,
        },
        'summary': {
            'pbs_wins': wins['personal-belief-state'],
            'time_aware_wins': wins['time-aware-latest'],
            'ties': ties,
            'pbs_win_rate': p_pbs,
            'time_aware_win_rate': p_time,
            'pairwise_protocol_rank_reversal_rate': reversal_rate,
            'winner_entropy_bits': winner_entropy,
        },
        'by_calibration': by_cal,
        'cells': cells,
        'interpretation': (
            'The identity of the higher-utility system is not invariant to plausible calibration, '
            'action-threshold, and deferral-cost choices. These statistics characterize protocol fragility; '
            'they do not identify a universally superior memory system.'
        ),
    }
    (ROOT/'data'/'protocol_stability_matrix.json').write_text(json.dumps(result, indent=2) + '\n')

    s = result['summary']
    lines = [
        '# Protocol Stability Matrix', '',
        '## Question', '',
        'Does the long-horizon utility ranking between the two strongest controlled systems remain stable across plausible evaluation protocols?', '',
        'The protocol grid is fixed **without using long-horizon diagnostic labels for protocol selection**. We cross three confidence treatments (native, development-only bucket calibration, development-only isotonic calibration) with five action thresholds and five deferral costs, for **75 protocol cells**. Calibrators are fit on a development cohort (60 users per seed, seeds 1–3) and frozen before an independent long-horizon diagnostic cohort (40 users per seed, seeds 30–39). The larger primary benchmark remains unchanged; this smaller cohort exists to make the protocol sweep reproducible within the release budget.', '',
        '## Result', '',
        '| Quantity | Value |', '|---|---:|',
        f"| PBS wins | {s['pbs_wins']} / 75 |",
        f"| Time-aware-latest wins | {s['time_aware_wins']} / 75 |",
        f"| Ties | {s['ties']} / 75 |",
        f"| Pairwise protocol rank-reversal rate | {s['pairwise_protocol_rank_reversal_rate']:.3f} |",
        f"| Winner entropy | {s['winner_entropy_bits']:.3f} bits |", '',
        'A high reversal rate means that two defensible protocol choices frequently induce opposite pairwise selections. This is a property of the **evaluation protocol**, not evidence that either system is intrinsically best.', '',
        '## By calibration family', '',
        '| Calibration | PBS wins | Time-aware wins | Ties | Mean PBS - baseline utility |', '|---|---:|---:|---:|---:|',
    ]
    for k,v in by_cal.items():
        lines.append(f"| {k} | {v['pbs_wins']} | {v['time_aware_wins']} | {v['ties']} | {v['mean_delta']:+.3f} |")
    lines += ['', '## Why this is stronger than a single rank flip', '',
              'The earlier result showed one native-vs-calibrated reversal at a fixed threshold/cost. This matrix asks whether that observation survives a broader set of reasonable protocol choices. It also makes a cherry-picking failure mode visible: selecting a threshold or confidence treatment after inspecting test outcomes can select the preferred system.', '',
              '## Boundary', '',
              'The grid is still a controlled synthetic study. Its purpose is measurement diagnosis. It does not establish that the same reversal frequency holds for frontier models or human preference distributions. External model-backed validation is required before making a population or leaderboard claim.']
    (ROOT/'reports'/'PROTOCOL_STABILITY_MATRIX.md').write_text('\n'.join(lines) + '\n')

    # Small SVG heatmap with no third-party dependency.
    cell_w, cell_h = 72, 36
    margin_l, margin_t = 120, 60
    groups = list(calibrators)
    width = margin_l + cell_w*len(THRESHOLDS) + 40
    height = margin_t + cell_h*(len(DEFER_COSTS)*len(groups)) + 80
    def color(delta):
        # neutral grayscale-like palette avoids implying moral preference; encoded by lightness.
        if delta > 0: return '#d9e8f5'
        if delta < 0: return '#f1dfd2'
        return '#eeeeee'
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
         '<rect width="100%" height="100%" fill="white"/>',
         '<style>text{font-family:Arial,sans-serif;fill:#111}.small{font-size:11px}.label{font-size:12px;font-weight:600}.title{font-size:16px;font-weight:700}</style>',
         '<text x="20" y="26" class="title">Protocol stability: PBS minus time-aware utility</text>']
    for j,t in enumerate(THRESHOLDS):
        x=margin_l+j*cell_w+cell_w/2
        svg.append(f'<text x="{x}" y="48" text-anchor="middle" class="small">thr {t:.2f}</text>')
    row=0
    for cal in groups:
        for dc in DEFER_COSTS:
            y=margin_t+row*cell_h
            if dc == DEFER_COSTS[0]:
                svg.append(f'<text x="8" y="{y+15}" class="label">{cal}</text>')
            svg.append(f'<text x="{margin_l-8}" y="{y+23}" text-anchor="end" class="small">cost {dc:.2f}</text>')
            for j,t in enumerate(THRESHOLDS):
                c=next(c for c in cells if c['calibration']==cal and c['threshold']==t and c['defer_cost']==dc)
                x=margin_l+j*cell_w
                d=c['pbs_minus_time_aware']
                svg.append(f'<rect x="{x}" y="{y}" width="{cell_w-2}" height="{cell_h-2}" rx="3" fill="{color(d)}" stroke="#ccc"/>')
                svg.append(f'<text x="{x+(cell_w-2)/2}" y="{y+22}" text-anchor="middle" class="small">{d:+.3f}</text>')
            row+=1
    svg += [f'<text x="20" y="{height-30}" class="small">Blue: PBS higher utility. Tan: time-aware-latest higher. Values are mean delta across seeds 30-39.</text>', '</svg>']
    (ROOT/'paper'/'figures'/'protocol_stability_matrix.svg').write_text('\n'.join(svg)+'\n')
    print(json.dumps(result['summary'], indent=2))

if __name__ == '__main__':
    main()
