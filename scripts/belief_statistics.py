from __future__ import annotations
import json, random, statistics, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig, run_benchmark

def bootstrap_ci(xs, seed=99, n=5000):
    r=random.Random(seed); m=[]
    for _ in range(n): m.append(statistics.fmean(xs[r.randrange(len(xs))] for _ in xs))
    m.sort(); return [m[int(.025*n)],m[min(n-1,int(.975*n))]]

rows=[]
for seed in range(10,20):
    out=run_benchmark(BenchmarkConfig(users=220,turns=240,seed=seed))['results']
    p=out['personal-belief-state']; t=out['trusted-latest']; ta=out['time-aware-latest']
    row={'seed':seed}
    for label,b in [('trusted',t),('time_aware',ta)]:
      row.update({
        f'utility_gain_vs_{label}':p['decision_utility']-b['decision_utility'],
        f'accuracy_delta_vs_{label}':p['accuracy']-b['accuracy'],
        f'selective_gain_vs_{label}':p['selective_accuracy']-b['selective_accuracy'],
        f'brier_reduction_vs_{label}':b['brier']-p['brier'],
      })
    rows.append(row)
summary={}
for label in ['trusted','time_aware']:
  for metric in ['utility_gain','accuracy_delta','selective_gain','brier_reduction']:
    k=f'{metric}_vs_{label}';xs=[r[k] for r in rows];summary[k]={'mean':statistics.fmean(xs),'stdev':statistics.stdev(xs),'bootstrap_95_ci':bootstrap_ci(xs)}
out={'runs':rows,'summary':summary,'test_seeds':'10-19','selection':'PBS hyperparameters fixed from development seeds 1-3'}
(ROOT/'data'/'belief_statistics.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
lines=['# Personal Belief State — Held-out Multi-seed Statistics','', 'Ten paired **held-out** synthetic seeds (10-19); 220 users × 240 turns per seed. PBS hyperparameters were selected on development seeds 1-3. Intervals characterize simulator variability, not a human population.','', '| Effect | Mean | 95% bootstrap CI |','|---|---:|---:|']
for k,s in summary.items():
  lo,hi=s['bootstrap_95_ci'];lines.append(f"| {k.replace('_',' ')} | {s['mean']:+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
(ROOT/'reports'/'BELIEF_STATE_STATISTICS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))
