from __future__ import annotations
import json,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig,generate_user_stream,_evaluate_tracker
from personalagi.user_model.probabilistic_belief import PersonalBeliefState

halves=[60,90,120,180,260]
temps=[.20,.30,.42,.55]
rows=[]
for h in halves:
  for temp in temps:
    metrics=[]
    for seed in [1,2,3]:
      cfg=BenchmarkConfig(users=120,turns=240,seed=seed)
      streams=[generate_user_stream(i,cfg) for i in range(cfg.users)]
      class Tracker:
        def __init__(self): self.pbs=PersonalBeliefState(half_life_turns=h,temperature=temp)
        def observe(self,o): self.pbs.update(o.evidence())
        def read(self,q):
          r=self.pbs.read(q.slot,turn=q.turn,context=q.context);return r.value,r.confidence
      metrics.append(_evaluate_tracker(Tracker,streams))
    rows.append({'half_life_turns':h,'temperature':temp,'mean_brier':statistics.fmean(m['brier'] for m in metrics),'mean_accuracy':statistics.fmean(m['accuracy'] for m in metrics),'mean_utility':statistics.fmean(m['decision_utility'] for m in metrics)})
rows.sort(key=lambda x:(x['mean_brier'],-x['mean_accuracy']))
best=rows[0]
out={'selection_rule':'minimum mean Brier on development seeds 1,2,3','development_users_per_seed':120,'grid':rows,'selected':best,'held_out_test_seeds':'10-19'}
(ROOT/'data'/'belief_tuning.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
lines=['# PBS Hyperparameter Selection','', 'Hyperparameters are selected on development seeds **1-3 only** by minimum mean Brier score; test seeds 10-19 are held out from selection.','',f"Selected: half-life **{best['half_life_turns']} turns**, temperature **{best['temperature']:.2f}**.",'','| Half-life | Temperature | Dev Brier ↓ | Dev accuracy | Dev utility |','|---:|---:|---:|---:|---:|']
for x in rows: lines.append(f"| {x['half_life_turns']} | {x['temperature']:.2f} | {x['mean_brier']:.3f} | {x['mean_accuracy']:.3f} | {x['mean_utility']:.3f} |")
(ROOT/'reports'/'BELIEF_TUNING.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(best,indent=2))
