from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig,run_benchmark
cfg=BenchmarkConfig(users=180,turns=240,seed=47)
rows=[]
for threshold in [.50,.60,.70,.80,.90]:
  for cost in [0.0,.05,.10,.20,.40,.60]:
    r=run_benchmark(cfg,action_threshold=threshold,defer_cost=cost)['results']
    p,t,ta=r['personal-belief-state'],r['trusted-latest'],r['time-aware-latest']
    rows.append({
      'threshold':threshold,'defer_cost':cost,'pbs_utility':p['decision_utility'],
      'trusted_utility':t['decision_utility'],'time_aware_utility':ta['decision_utility'],
      'gain_vs_trusted':p['decision_utility']-t['decision_utility'],
      'gain_vs_time_aware':p['decision_utility']-ta['decision_utility'],
      'pbs_coverage':p['coverage'],'trusted_coverage':t['coverage'],'time_aware_coverage':ta['coverage']})
out={'config':{'users':cfg.users,'turns':cfg.turns,'seed':cfg.seed},'rows':rows,
     'wins_vs_trusted':sum(x['gain_vs_trusted']>0 for x in rows),
     'wins_vs_time_aware':sum(x['gain_vs_time_aware']>0 for x in rows),'cells':len(rows)}
(ROOT/'data'/'belief_sensitivity.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
lines=['# Decision-Utility Sensitivity','',
 f"PBS has higher utility than trusted-latest in **{out['wins_vs_trusted']}/{out['cells']}** settings and higher utility than the stronger time-aware-latest baseline in **{out['wins_vs_time_aware']}/{out['cells']}** settings.",'',
 '| Threshold | Defer cost | PBS | Time-aware | Trusted | Gain vs time-aware |','|---:|---:|---:|---:|---:|---:|']
for x in rows: lines.append(f"| {x['threshold']:.2f} | {x['defer_cost']:.2f} | {x['pbs_utility']:.3f} | {x['time_aware_utility']:.3f} | {x['trusted_utility']:.3f} | {x['gain_vs_time_aware']:+.3f} |")
(ROOT/'reports'/'BELIEF_SENSITIVITY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'wins_vs_trusted':out['wins_vs_trusted'],'wins_vs_time_aware':out['wins_vs_time_aware'],'cells':out['cells'],'min_gain_vs_time_aware':min(x['gain_vs_time_aware'] for x in rows),'max_gain_vs_time_aware':max(x['gain_vs_time_aware'] for x in rows)},indent=2))
