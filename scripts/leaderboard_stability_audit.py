from __future__ import annotations
import hashlib, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig, TRACKERS, generate_user_stream
from scripts.calibrated_baseline_eval import collect_raw, fit_bucket_calibrator, eval_rows
from scripts.protocol_stability_matrix import fit_isotonic_calibrator

DEV_SEEDS=(1,2,3)
TEST_SEEDS=tuple(range(30,40))
THRESHOLDS=(0.55,0.65,0.70,0.75,0.85)
DEFER_COSTS=(0.00,0.05,0.10,0.20,0.35)


def streams(seed:int, users:int, turns:int, query_every:int):
    cfg=BenchmarkConfig(users=users, turns=turns, seed=seed, query_every=query_every)
    return [generate_user_stream(i,cfg) for i in range(users)]

def identity(x): return float(x)
def mean(xs): return sum(xs)/max(1,len(xs))

def rank(values:dict[str,float]):
    # deterministic total order for reproducibility; tiny exact ties use method name.
    return [k for k,_ in sorted(values.items(), key=lambda kv:(-kv[1],kv[0]))]

def kendall_tau(a:list[str], b:list[str]):
    pos={x:i for i,x in enumerate(b)}
    c=d=0
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            c += pos[a[i]] < pos[a[j]]
            d += pos[a[i]] > pos[a[j]]
    return (c-d)/max(1,c+d)

def main():
    registry=json.loads((ROOT/'configs'/'protocol_registry.json').read_text())
    assert tuple(registry['development_seeds'])==DEV_SEEDS
    assert tuple(registry['long_horizon_test_seeds'])==TEST_SEEDS
    assert tuple(registry['protocol_stability_thresholds'])==THRESHOLDS
    assert tuple(registry['protocol_stability_defer_costs'])==DEFER_COSTS

    dev_streams={s:streams(s,60,240,24) for s in DEV_SEEDS}
    test_streams={s:streams(s,40,800,50) for s in TEST_SEEDS}
    raw_dev={}; raw_test={}
    for cls in TRACKERS:
        name=cls.name
        rows=[]
        for s in DEV_SEEDS: rows.extend(collect_raw(cls,dev_streams[s]))
        raw_dev[name]=rows
        raw_test[name]={s:collect_raw(cls,test_streams[s]) for s in TEST_SEEDS}

    calibrators={}
    for cls in TRACKERS:
        name=cls.name
        calibrators[name]={
            'native':identity,
            'bucket-laplace':fit_bucket_calibrator(raw_dev[name])[1],
            'isotonic-laplace':fit_isotonic_calibrator(raw_dev[name])[1],
        }

    cells=[]; winner_counts=Counter(); rank_positions=defaultdict(list)
    for cal in registry['calibration_families']:
        for th in THRESHOLDS:
            for cost in DEFER_COSTS:
                utilities={}
                for cls in TRACKERS:
                    name=cls.name; fn=calibrators[name][cal]
                    utilities[name]=mean([eval_rows(raw_test[name][s],fn,threshold=th,defer_cost=cost)['decision_utility'] for s in TEST_SEEDS])
                order=rank(utilities); winner=order[0]; winner_counts[winner]+=1
                for i,m in enumerate(order,1): rank_positions[m].append(i)
                cells.append({'calibration':cal,'threshold':th,'defer_cost':cost,'utilities':utilities,'ranking':order,'winner':winner})

    # pairwise protocol statistics over unordered cell pairs
    n=len(cells); pairs=n*(n-1)//2; winner_changes=0; taus=[]
    for i in range(n):
        for j in range(i+1,n):
            winner_changes += cells[i]['winner'] != cells[j]['winner']
            taus.append(kendall_tau(cells[i]['ranking'],cells[j]['ranking']))
    # method-level pairwise ordering reversal rate
    methods=[c.name for c in TRACKERS]
    pairwise_reversal={}
    for i,a in enumerate(methods):
        for b in methods[i+1:]:
            signs=[]
            for c in cells:
                d=c['utilities'][a]-c['utilities'][b]
                signs.append(1 if d>1e-12 else -1 if d<-1e-12 else 0)
            pos=sum(x>0 for x in signs); neg=sum(x<0 for x in signs)
            denom=n*(n-1)//2
            pairwise_reversal[f'{a}__vs__{b}']=(pos*neg/denom if denom else 0.0)
    rank_summary={}
    for m,rs in rank_positions.items():
        mu=mean(rs); var=mean([(x-mu)**2 for x in rs])
        rank_summary[m]={'mean_rank':mu,'rank_variance':var,'best_rank':min(rs),'worst_rank':max(rs),'winner_cells':winner_counts[m]}

    out={
        'version':'4.2.0','protocol_cells':n,'development_seeds':list(DEV_SEEDS),'long_horizon_test_seeds':list(TEST_SEEDS),
        'summary':{
            'winner_counts':dict(winner_counts),
            'winner_change_probability':winner_changes/max(1,pairs),
            'mean_pairwise_kendall_tau':mean(taus),
            'minimum_pairwise_kendall_tau':min(taus),
            'maximum_pairwise_kendall_tau':max(taus),
            'methods_ever_winning':sum(v>0 for v in winner_counts.values()),
        },
        'rank_summary':rank_summary,'pairwise_order_reversal_rate':pairwise_reversal,'cells':cells,
        'interpretation':'The leaderboard is an instrument-dependent object under these operating-point protocols. This is a controlled synthetic diagnostic, not an external model leaderboard or SOTA claim.'
    }
    (ROOT/'data'/'leaderboard_stability_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    s=out['summary']
    lines=['# Leaderboard Stability Audit','',
           '## Question','',
           'Does protocol sensitivity persist when all six released baselines are ranked together, rather than only comparing the two strongest structured systems?','',
           'We replay the same long-horizon histories for every method across the frozen 75-cell protocol family: three confidence treatments, five action thresholds, and five deferral costs. Calibration is fit only on development seeds 1-3. Long-horizon labels from seeds 30-39 are not used to select a protocol.','',
           '## Result','',
           '| Quantity | Value |','|---|---:|',
           f"| Protocol cells | {n} |",
           f"| Probability two protocol cells choose different winners | {s['winner_change_probability']:.3f} |",
           f"| Mean Kendall tau across complete rankings | {s['mean_pairwise_kendall_tau']:.3f} |",
           f"| Minimum Kendall tau | {s['minimum_pairwise_kendall_tau']:.3f} |",
           f"| Methods that win at least one cell | {s['methods_ever_winning']} / {len(methods)} |",'',
           '### Winner counts','', '| Method | Winning cells | Mean rank | Best | Worst | Rank variance |','|---|---:|---:|---:|---:|---:|']
    for m in sorted(methods,key=lambda x:(-winner_counts[x],x)):
        r=rank_summary[m]; lines.append(f"| {m} | {winner_counts[m]} | {r['mean_rank']:.2f} | {r['best_rank']} | {r['worst_rank']} | {r['rank_variance']:.2f} |")
    lines += ['', '## Interpretation','',
              'The important object is not which method wins the most cells. It is that the identity and ordering of the leaderboard are not invariant to defensible operating-point choices. A weak or stale baseline winning any cell is a warning that coverage/confidence economics can dominate state quality if the protocol is poorly matched to the intended deployment decision.','',
              'This audit therefore supports a measurement claim: report threshold-free state/risk metrics together with any utility leaderboard, freeze calibration on development data, and expose ranking stability across plausible deployment costs. It does **not** establish an overall SOTA personal agent.']
    (ROOT/'reports'/'LEADERBOARD_STABILITY_AUDIT.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(s,indent=2))

if __name__=='__main__': main()
