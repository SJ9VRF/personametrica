from __future__ import annotations
import json, random, statistics, sys
from pathlib import Path
from collections import defaultdict, Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig, TRACKERS, generate_user_stream
from scripts.calibrated_baseline_eval import fit_bucket_calibrator, eval_rows
from scripts.protocol_stability_matrix import fit_isotonic_calibrator

DEV_SEEDS=(1,2,3)
TEST_SEEDS=tuple(range(30,40))
THRESHOLDS=(0.55,0.65,0.70,0.75,0.85)
DEFER_COSTS=(0.00,0.05,0.10,0.20,0.35)
BOOTSTRAPS=2000
BOOTSTRAP_SEED=39017

def streams(seed:int, users:int, turns:int, query_every:int):
    cfg=BenchmarkConfig(users=users,turns=turns,seed=seed,query_every=query_every)
    return [generate_user_stream(i,cfg) for i in range(users)]

def collect_all_raw(streams):
    out={c.name:[] for c in TRACKERS}
    for obs,qs in streams:
        trackers={c.name:c() for c in TRACKERS}
        events=sorted([(o.turn,0,o) for o in obs]+[(q.turn,1,q) for q in qs],key=lambda x:(x[0],x[1]))
        for _,kind,obj in events:
            if kind==0:
                for t in trackers.values(): t.observe(obj)
            else:
                for name,t in trackers.items():
                    pred,conf=t.read(obj); ok=pred==obj.expected
                    out[name].append((pred,obj.expected,float(conf),ok))
    return out
def ident(x): return float(x)
def rank(vals): return [k for k,_ in sorted(vals.items(),key=lambda kv:(-kv[1],kv[0]))]
def tau(a,b):
    pos={x:i for i,x in enumerate(b)}; c=d=0
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            if pos[a[i]]<pos[a[j]]: c+=1
            else: d+=1
    return (c-d)/max(1,c+d)
def summarize_cells(cells):
    n=len(cells); pairs=n*(n-1)//2; wc=0; ts=[]
    for i in range(n):
        for j in range(i+1,n):
            wc += cells[i]['winner'] != cells[j]['winner']
            ts.append(tau(cells[i]['ranking'],cells[j]['ranking']))
    return {'winner_change_probability':wc/max(1,pairs),'mean_pairwise_kendall_tau':statistics.mean(ts),'minimum_pairwise_kendall_tau':min(ts)}
def quantile(xs,q):
    ys=sorted(xs); idx=(len(ys)-1)*q; lo=int(idx); hi=min(len(ys)-1,lo+1); f=idx-lo
    return ys[lo]*(1-f)+ys[hi]*f


def main():
    registry=json.loads((ROOT/'configs'/'protocol_registry.json').read_text())
    assert tuple(registry['development_seeds'])==DEV_SEEDS
    assert tuple(registry['long_horizon_test_seeds'])==TEST_SEEDS
    dev_streams={s:streams(s,60,240,24) for s in DEV_SEEDS}
    test_streams={s:streams(s,10,800,50) for s in TEST_SEEDS}
    methods=[c.name for c in TRACKERS]
    raw_dev={m:[] for m in methods}; raw_test={m:{} for m in methods}
    for s in DEV_SEEDS:
        all_rows=collect_all_raw(dev_streams[s])
        for m in methods: raw_dev[m].extend(all_rows[m])
    for s in TEST_SEEDS:
        all_rows=collect_all_raw(test_streams[s])
        for m in methods: raw_test[m][s]=all_rows[m]
    calibrators={}
    for cls in TRACKERS:
        n=cls.name
        calibrators[n]={'native':ident,'bucket-laplace':fit_bucket_calibrator(raw_dev[n])[1],'isotonic-laplace':fit_isotonic_calibrator(raw_dev[n])[1]}

    # Seed-level utilities for every frozen protocol cell.
    cells=[]
    for cal in registry['calibration_families']:
        for th in THRESHOLDS:
            for cost in DEFER_COSTS:
                per_seed={}
                means={}
                for m in methods:
                    vals=[eval_rows(raw_test[m][s],calibrators[m][cal],threshold=th,defer_cost=cost)['decision_utility'] for s in TEST_SEEDS]
                    per_seed[m]=vals; means[m]=statistics.mean(vals)
                order=rank(means)
                cells.append({'calibration':cal,'threshold':th,'defer_cost':cost,'mean_utilities':means,'per_seed_utilities':per_seed,'ranking':order,'winner':order[0]})
    point=summarize_cells(cells)

    # Bootstrap test seeds as the sampling unit. Same resampled seed indices are used for every
    # method and every protocol cell to preserve paired structure.
    rng=random.Random(BOOTSTRAP_SEED)
    wcp=[]; mtau=[]; mintau=[]; same_winner_support=[0]*len(cells)
    original_winners=[c['winner'] for c in cells]
    winner_counts=Counter()
    for _ in range(BOOTSTRAPS):
        idxs=[rng.randrange(len(TEST_SEEDS)) for _ in TEST_SEEDS]
        bcells=[]
        for ci,c in enumerate(cells):
            vals={m:statistics.mean(c['per_seed_utilities'][m][i] for i in idxs) for m in methods}
            order=rank(vals); winner=order[0]
            same_winner_support[ci]+=winner==original_winners[ci]
            winner_counts[winner]+=1
            bcells.append({'ranking':order,'winner':winner})
        sm=summarize_cells(bcells); wcp.append(sm['winner_change_probability']); mtau.append(sm['mean_pairwise_kendall_tau']); mintau.append(sm['minimum_pairwise_kendall_tau'])
    ci=lambda xs:[quantile(xs,.025),quantile(xs,.975)]
    cell_support=[x/BOOTSTRAPS for x in same_winner_support]
    out={
      'version':'4.2.0','bootstrap_unit':'long-horizon test seed','bootstrap_replicates':BOOTSTRAPS,'bootstrap_rng_seed':BOOTSTRAP_SEED,
      'development_seeds':list(DEV_SEEDS),'test_seeds':list(TEST_SEEDS),'diagnostic_users_per_seed':10,'protocol_cells':len(cells),
      'point_estimate':point,
      'bootstrap_95_ci':{'winner_change_probability':ci(wcp),'mean_pairwise_kendall_tau':ci(mtau),'minimum_pairwise_kendall_tau':ci(mintau)},
      'bootstrap_claim_support':{
        'p_winner_change_gt_0_40':sum(x>.40 for x in wcp)/BOOTSTRAPS,
        'p_mean_tau_lt_0_90':sum(x<.90 for x in mtau)/BOOTSTRAPS,
      },
      'cell_winner_stability':{
        'mean_original_winner_support':statistics.mean(cell_support),
        'minimum_original_winner_support':min(cell_support),
        'cells_support_ge_0_95':sum(x>=.95 for x in cell_support),
        'cells_support_ge_0_80':sum(x>=.80 for x in cell_support),
      },
      'cells':[{'calibration':c['calibration'],'threshold':c['threshold'],'defer_cost':c['defer_cost'],'winner':c['winner'],'original_winner_bootstrap_support':cell_support[i]} for i,c in enumerate(cells)],
      'interpretation':'Seed bootstrap quantifies sampling uncertainty for the fixed synthetic generator and frozen protocol grid. It does not establish population-level human or frontier-model uncertainty.'
    }
    (ROOT/'data'/'leaderboard_seed_uncertainty.json').write_text(json.dumps(out,indent=2)+'\n')
    lines=['# Leaderboard Seed-Uncertainty Audit','',
      '## Question','',
      'On a lower-cost 10-user-per-seed diagnostic cohort, does protocol-sensitive ranking survive paired resampling of the same ten long-horizon seeds?','',
      'The sampling unit is a complete long-horizon seed. Each bootstrap replicate resamples the same seed indices jointly for every method and every protocol cell, preserving paired comparisons. Calibration remains fit only on development seeds 1–3.','',
      '## Result','', '| Quantity | Point estimate | 95% seed-bootstrap CI |','|---|---:|---:|',
      f"| Winner-change probability | {point['winner_change_probability']:.3f} | [{out['bootstrap_95_ci']['winner_change_probability'][0]:.3f}, {out['bootstrap_95_ci']['winner_change_probability'][1]:.3f}] |",
      f"| Mean Kendall tau | {point['mean_pairwise_kendall_tau']:.3f} | [{out['bootstrap_95_ci']['mean_pairwise_kendall_tau'][0]:.3f}, {out['bootstrap_95_ci']['mean_pairwise_kendall_tau'][1]:.3f}] |",
      f"| Minimum Kendall tau | {point['minimum_pairwise_kendall_tau']:.3f} | [{out['bootstrap_95_ci']['minimum_pairwise_kendall_tau'][0]:.3f}, {out['bootstrap_95_ci']['minimum_pairwise_kendall_tau'][1]:.3f}] |",'',
      f"Across {BOOTSTRAPS:,} paired seed bootstraps, P(winner-change probability > 0.40) = **{out['bootstrap_claim_support']['p_winner_change_gt_0_40']:.3f}** and P(mean Kendall tau < 0.90) = **{out['bootstrap_claim_support']['p_mean_tau_lt_0_90']:.3f}**.",'',
      f"The original per-cell winner is not equally certain: mean bootstrap support is {out['cell_winner_stability']['mean_original_winner_support']:.3f}, while the least stable cell has support {out['cell_winner_stability']['minimum_original_winner_support']:.3f}. This is expected and is precisely why PersonaMetrica reports ranking stability rather than presenting every cell winner as ground truth.",'',
      '## Boundary','',
      'This is a lower-cost diagnostic cohort, separate from the 40-user-per-seed primary leaderboard audit. It measures uncertainty under the synthetic generator seeds used by PersonaMetrica. It is **not** a confidence interval over real users, model families, or deployment environments. External model and human validation remain separate evidence requirements.'
    ]
    (ROOT/'reports'/'LEADERBOARD_SEED_UNCERTAINTY.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({**point,**out['bootstrap_95_ci'],**out['bootstrap_claim_support'],**out['cell_winner_stability']},indent=2))
if __name__=='__main__': main()
