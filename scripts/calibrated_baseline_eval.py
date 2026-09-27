from __future__ import annotations
import json, math, sys
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import (
    BenchmarkConfig, TRACKERS, generate_user_stream,
)

DEV_SEEDS=(1,2,3)
TEST_SEEDS=tuple(range(10,20))
LONG_SEEDS=tuple(range(30,40))


def collect_raw(tracker_cls, streams):
    rows=[]
    for obs,qs in streams:
        tracker=tracker_cls()
        events=sorted([(o.turn,0,o) for o in obs]+[(q.turn,1,q) for q in qs], key=lambda x:(x[0],x[1]))
        for _,kind,obj in events:
            if kind==0: tracker.observe(obj)
            else:
                pred,conf=tracker.read(obj)
                rows.append((pred,obj.expected,float(conf), pred==obj.expected))
    return rows


def fit_bucket_calibrator(rows):
    # Deliberately simple post-hoc calibration: empirical correctness per raw-confidence bucket,
    # Laplace-smoothed so baselines with confidence=1.0 cannot remain spuriously certain.
    buckets=defaultdict(lambda:[0,0])
    for _,_,c,ok in rows:
        k=round(c,2); buckets[k][0]+=int(ok); buckets[k][1]+=1
    mapping={k:(v[0]+1)/(v[1]+2) for k,v in buckets.items()}
    keys=sorted(mapping)
    def cal(c):
        if not keys: return c
        k=min(keys,key=lambda x:abs(x-round(c,2)))
        return mapping[k]
    return mapping,cal


def eval_rows(rows,cal,threshold=.70,defer_cost=.10):
    total=len(rows); acted=correct=acted_correct=0; brier=0.0; pairs=[]
    for pred,expected,raw,ok in rows:
        conf=float(cal(raw)); correct+=int(ok); brier+=(conf-int(ok))**2; pairs.append((conf,int(ok)))
        if pred is not None and conf>=threshold:
            acted+=1; acted_correct+=int(ok)
    asks=total-acted
    coverage=acted/max(1,total); selective=acted_correct/max(1,acted)
    utility=(acted_correct-(acted-acted_correct)-defer_cost*asks)/max(1,total)
    return dict(accuracy=correct/max(1,total),coverage=coverage,selective_accuracy=selective,
                decision_utility=utility,brier=brier/max(1,total),queries=total)


def streams_for(seed,users,turns,query_every=24):
    cfg=BenchmarkConfig(users=users,turns=turns,seed=seed,query_every=query_every)
    return [generate_user_stream(i,cfg) for i in range(users)]


def mean_dict(rows):
    keys=rows[0].keys(); return {k:sum(r[k] for r in rows)/len(rows) for k in keys if isinstance(rows[0][k],(int,float))}


def main():
    out={'development_seeds':DEV_SEEDS,'standard_test_seeds':TEST_SEEDS,'long_horizon_test_seeds':LONG_SEEDS,'methods':{}}
    for cls in TRACKERS:
        dev=[]
        for seed in DEV_SEEDS:
            dev.extend(collect_raw(cls,streams_for(seed,120,240)))
        mapping,cal=fit_bucket_calibrator(dev)
        standard=[]
        for seed in TEST_SEEDS:
            standard.append(eval_rows(collect_raw(cls,streams_for(seed,160,240)),cal))
        long=[]
        for seed in LONG_SEEDS:
            long.append(eval_rows(collect_raw(cls,streams_for(seed,120,800,50)),cal))
        out['methods'][cls.name]={
            'calibration_map':{str(k):v for k,v in sorted(mapping.items())},
            'standard':mean_dict(standard), 'long_horizon':mean_dict(long),
            'standard_per_seed':standard,'long_horizon_per_seed':long,
        }
    p=ROOT/'data'/'calibrated_baseline_results.json'; p.write_text(json.dumps(out,indent=2))
    lines=['# Development-Calibrated Baseline Evaluation','',
           'All trackers receive the same post-hoc opportunity: raw confidence is mapped to Laplace-smoothed empirical correctness on development seeds 1–3 only. The mapping is frozen before held-out seeds 10–19 and long-horizon seeds 30–39. This test asks whether the paper\'s decision-quality findings survive simple baseline calibration.','',
           '## Standard held-out means','',
           '| Method | Accuracy | Coverage | Selective acc. | Utility | Brier ↓ |','|---|---:|---:|---:|---:|---:|']
    for name,d in out['methods'].items():
        m=d['standard']; lines.append(f"| {name} | {m['accuracy']:.3f} | {m['coverage']:.3f} | {m['selective_accuracy']:.3f} | {m['decision_utility']:.3f} | {m['brier']:.3f} |")
    lines += ['', '## 800-turn held-out means','', '| Method | Accuracy | Coverage | Selective acc. | Utility | Brier ↓ |','|---|---:|---:|---:|---:|---:|']
    for name,d in out['methods'].items():
        m=d['long_horizon']; lines.append(f"| {name} | {m['accuracy']:.3f} | {m['coverage']:.3f} | {m['selective_accuracy']:.3f} | {m['decision_utility']:.3f} | {m['brier']:.3f} |")
    lines += ['', '## Interpretation','', 'This calibration is intentionally low-capacity and uses no test labels. It is not a substitute for learned confidence models, but it removes the easiest objection that structured baselines were forced to act with their raw generator confidence.']
    (ROOT/'reports'/'CALIBRATED_BASELINES.md').write_text('\n'.join(lines)+'\n')
    print(p)

if __name__=='__main__': main()
