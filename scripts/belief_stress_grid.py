from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig, run_benchmark

def main():
    noise=[.05,.15,.30,.45]; beh=[.10,.25,.40,.55]; temps=[.10,.35,.60]
    rows=[]
    for i,n in enumerate(noise):
      for j,b in enumerate(beh):
       for k,t in enumerate(temps):
        cfg=BenchmarkConfig(users=90,turns=240,seed=400+i*100+j*10+k,noise_rate=n,behavior_noise_rate=b,temporary_rate=t)
        res=run_benchmark(cfg)['results']; p=res['personal-belief-state']; a=res['time-aware-latest']
        rows.append({'noise_rate':n,'behavior_noise_rate':b,'temporary_rate':t,
                     'pbs_accuracy':p['accuracy'],'baseline_accuracy':a['accuracy'],'accuracy_delta':p['accuracy']-a['accuracy'],
                     'pbs_utility':p['decision_utility'],'baseline_utility':a['decision_utility'],'utility_delta':p['decision_utility']-a['decision_utility'],
                     'pbs_brier':p['brier'],'baseline_brier':a['brier'],'brier_improvement':a['brier']-p['brier']})
    summary={'cells':len(rows),'pbs_utility_wins':sum(r['utility_delta']>0 for r in rows),'pbs_accuracy_wins':sum(r['accuracy_delta']>0 for r in rows),
             'mean_utility_delta':sum(r['utility_delta'] for r in rows)/len(rows),'mean_accuracy_delta':sum(r['accuracy_delta'] for r in rows)/len(rows),
             'worst_utility_delta':min(r['utility_delta'] for r in rows),'best_utility_delta':max(r['utility_delta'] for r in rows)}
    obj={'summary':summary,'rows':rows}; (ROOT/'data/belief_stress_grid.json').write_text(json.dumps(obj,indent=2))
    worst=sorted(rows,key=lambda r:r['utility_delta'])[:5]
    lines=['# Belief stress grid','',f"48 cells = 4 distractor-noise rates × 4 behavioral-noise rates × 3 temporary-preference rates. Each cell evaluates 90 users × 240 turns.",'',f"PBS wins on decision utility in **{summary['pbs_utility_wins']}/{summary['cells']}** cells and on raw state accuracy in **{summary['pbs_accuracy_wins']}/{summary['cells']}** cells.",f"Mean utility delta vs time-aware-latest: **{summary['mean_utility_delta']:+.3f}**. Worst cell: **{summary['worst_utility_delta']:+.3f}**.",'','## Hardest cells','', '| distractor noise | behavior noise | temporary rate | Δ accuracy | Δ utility |','|---:|---:|---:|---:|---:|']
    for r in worst: lines.append(f"| {r['noise_rate']:.2f} | {r['behavior_noise_rate']:.2f} | {r['temporary_rate']:.2f} | {r['accuracy_delta']:+.3f} | {r['utility_delta']:+.3f} |")
    lines += ['', 'This grid is a simulator stress test, not evidence of performance on human interaction distributions.']
    (ROOT/'reports/BELIEF_STRESS_GRID.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
