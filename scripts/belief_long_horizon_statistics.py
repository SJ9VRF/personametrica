from __future__ import annotations
import json,random,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig,run_benchmark

def ci(xs,seed=881,n=4000):
 r=random.Random(seed);ys=[]
 for _ in range(n):ys.append(statistics.fmean(xs[r.randrange(len(xs))] for _ in xs))
 ys.sort();return [ys[int(.025*n)],ys[min(n-1,int(.975*n))]]
rows=[]
for seed in range(30,40):
 r=run_benchmark(BenchmarkConfig(users=90,turns=800,seed=seed,query_every=50))['results']
 p,t=r['personal-belief-state'],r['time-aware-latest']
 rows.append({'seed':seed,'accuracy_delta':p['accuracy']-t['accuracy'],'utility_gain':p['decision_utility']-t['decision_utility'],'coverage_gain':p['coverage']-t['coverage'],'brier_reduction':t['brier']-p['brier']})
summary={k:{'mean':statistics.fmean(x[k] for x in rows),'bootstrap_95_ci':ci([x[k] for x in rows])} for k in ['accuracy_delta','utility_gain','coverage_gain','brier_reduction']}
out={'runs':rows,'summary':summary,'setting':'90 users x 800 turns; test seeds 30-39'}
(ROOT/'data'/'belief_long_horizon_statistics.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
lines=['# Long-Horizon Ranking Analysis','', 'Ten held-out seeds, each 90 users × 800 turns. PBS hyperparameters remain fixed from development seeds 1-3.','', '| PBS - time-aware-latest | Mean | 95% bootstrap CI |','|---|---:|---:|']
for k,v in summary.items():
 lo,hi=v['bootstrap_95_ci'];lines.append(f"| {k.replace('_',' ')} | {v['mean']:+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
(ROOT/'reports'/'BELIEF_LONG_HORIZON.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))
