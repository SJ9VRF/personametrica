from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.agent_evals import run_agent_eval_suite

out=run_agent_eval_suite()
(ROOT/'data'/'agent_trajectory_eval.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
m=out['grader_metrics']
lines=['# Agent trajectory evaluation','',
'PersonaMetrica-Bench trajectory extension separates task success from the path used to obtain it. It is a synthetic grader benchmark, not a frontier-model performance result.','',
'## Setup','',f"- Tasks: {out['benchmark']['tasks']}",f"- Trials: {out['benchmark']['trials']}",'- Tool domains: reminders, notes, tasks',f"- Perturbations: {', '.join(out['benchmark']['perturbations'])}",'',
'## Grader reliability against scenario gold labels','',
'| Grader | Accuracy | False accept | False reject |','|---|---:|---:|---:|']
for name in ('end_state_only','trajectory_policy','composite_agent','robust_trajectory','causal_trajectory'):
    x=m[name]; lines.append(f"| {name} | {x['accuracy']:.3f} | {x['false_accept_rate']:.3f} | {x['false_reject_rate']:.3f} |")
lines += ['', '## Adversarial false-accept rate', '', '| Grader | FAR on all gold-failing perturbations, including permission, tool/action, verification, partial-state, loop, false-claim, and forged-verification failures |','|---|---:|']
for name,val in m['adversarial_false_accept'].items(): lines.append(f'| {name} | {val:.3f} |')
lines += ['', '## Interpretation','',
'An end-state-only grader can accept trajectories that reach the requested state by violating permission, skipping required verification, or using an excessively long loop. The trajectory-aware grader makes those intermediate constraints explicit. This result validates the evaluation harness, not the behavior of a frontier model.', '',
'## Boundary','',
'- Gold labels are scenario-authored and deterministic.','- No LLM-as-judge claim is made.','- The suite is designed to calibrate future trace graders against explicit assertions and, later, independent human labels.']
(ROOT/'reports'/'AGENT_TRAJECTORY_EVAL.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'report':'reports/AGENT_TRAJECTORY_EVAL.md','metrics':m},indent=2))
