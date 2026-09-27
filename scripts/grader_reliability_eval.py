from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.agent_evals import build_agent_eval_suite
from personalbench.agent_evals.reliability import run_grader_reliability_suite, multi_trial_task_summary

tasks,trials=build_agent_eval_suite(n_tasks=100,trials_per_task=8,seed=23)
out=run_grader_reliability_suite(tasks,trials)
out['multi_trial']=multi_trial_task_summary(tasks,trials,seed=23)
(ROOT/'data'/'grader_reliability.json').write_text(json.dumps(out,indent=2),encoding='utf-8')

m=out['mutation_metrics']; mt=out['multi_trial']
lines=['# Grader reliability and drift audit','',
'This audit treats the evaluator as a system that can itself fail. It stress-tests invariance, missing evidence, threshold drift, score calibration, and the stability of estimates under repeated stochastic trials.','',
'## Metamorphic / evidence tests','',
'| Check | Result |','|---|---:|',
f"| Benign-event invariance | {100*m['benign_invariance_rate']:.1f}% |",
f"| Forged success-flag invariance | {100*m['forged_flag_invariance_rate']:.1f}% |",
f"| Missing-observation abstention | {100*m['redacted_evidence_abstention_rate']:.1f}% |",
f"| Late-confirmation detection | {100*m['late_confirmation_detection_rate']:.1f}% |",
f"| Excess tool-loop detection | {100*m['tool_loop_detection_rate']:.1f}% |",'',
'## Score calibration','',
'| Grader | Brier ↓ | ECE ↓ |','|---|---:|---:|']
for name,row in out['score_calibration'].items():
    lines.append(f"| {name} | {row['brier']:.3f} | {row['ece']:.3f} |")
lines += ['','## Composite-threshold drift','',
'Changing a weighted grader threshold can materially change false accepts; the release therefore reports threshold sensitivity rather than treating one threshold as ground truth.','',
'| Threshold | Accuracy | False accept |','|---:|---:|---:|']
for r in out['threshold_drift']:
    lines.append(f"| {r['threshold']:.2f} | {100*r['accuracy']:.1f}% | {100*r['false_accept_rate']:.1f}% |")
lines += ['','## Multi-trial stability','',
f"Task-level robust-grader pass rate: **{100*mt['task_success_rate']['mean']:.1f}%** (bootstrap 95% CI {100*mt['task_success_rate']['low']:.1f}–{100*mt['task_success_rate']['high']:.1f}%).",'',
'| Trials/task | Mean estimate | Sampling SD |','|---:|---:|---:|']
for r in mt['trial_count_sensitivity']:
    lines.append(f"| {r['trials_per_task']} | {100*r['mean_estimate']:.1f}% | {100*r['sampling_sd']:.2f} pp |")
lines += ['','## Interpretation','',
'- A benign logging event should not change a verdict.','- A forged success flag should not override state evidence.','- If critical observation evidence is missing, the evidence-aware grader abstains rather than inventing certainty.','- One stochastic trial per task yields a noisier estimate than repeated trials; trial count is therefore part of the eval protocol, not a cosmetic choice.','',
'These are controlled synthetic tests of grader behavior, not human-grader calibration results. Independent human calibration remains an external-evidence requirement.']
(ROOT/'reports'/'GRADER_RELIABILITY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'mutation_metrics':m,'multi_trial':mt,'threshold_drift':out['threshold_drift']},indent=2))
