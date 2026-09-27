from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.agent_evals import build_agent_eval_suite
from personalbench.agent_evals.graders import EndStateGrader, TrajectoryPolicyGrader, RobustTrajectoryGrader

tasks,trials=build_agent_eval_suite(n_tasks=80,trials_per_task=10,seed=17); tm={t.task_id:t for t in tasks}
traj_path=ROOT/'data'/'agent_trajectories.jsonl'; pair_path=ROOT/'data'/'trajectory_failure_pairs.jsonl'; structured_path=ROOT/'data'/'trajectory_corrections.jsonl'
with traj_path.open('w',encoding='utf-8') as f:
    for tr in trials: f.write(json.dumps(tr.to_dict(),sort_keys=True)+'\n')

pairs=[]
for tr in trials:
    task=tm[tr.task_id]
    end=EndStateGrader().grade(task,tr); naive=TrajectoryPolicyGrader().grade(task,tr); robust=RobustTrajectoryGrader().grade(task,tr)
    if tr.gold_pass or not (end.passed or naive.passed) or robust.passed:
        continue
    rejected=f"Accept trajectory {tr.trial_id}: final result appears successful."
    reason=tr.gold_failure_reason or ', '.join(robust.reasons)
    chosen=f"Reject trajectory {tr.trial_id}: {reason}. Require policy-compliant evidence and recomputed verification before success."
    pairs.append({'id':f'trace-pair-{len(pairs):04d}','task_id':tr.task_id,'perturbation':tr.perturbation,'chosen':chosen,'rejected':rejected,'reason':reason,'source':'trajectory_grader_false_accept'})
with pair_path.open('w',encoding='utf-8') as f:
    for row in pairs: f.write(json.dumps(row,sort_keys=True)+'\n')
structured=[]
for row in pairs:
    tr=next(t for t in trials if t.trial_id==row['id'].replace('trace-pair-','') ) if False else None
# Build auditable structured corrections from the same false-accept cases.
for tr in trials:
    task=tm[tr.task_id]
    end=EndStateGrader().grade(task,tr); naive=TrajectoryPolicyGrader().grade(task,tr); robust=RobustTrajectoryGrader().grade(task,tr)
    if tr.gold_pass or not (end.passed or naive.passed) or robust.passed:
        continue
    structured.append({
        'correction_id':f'trace-correction-{len(structured):04d}',
        'task_id':tr.task_id,'trial_id':tr.trial_id,'failure_type':tr.perturbation,
        'failed_assertions':robust.reasons,
        'evidence':{'final_state':tr.final_state,'events':tr.events},
        'target':{'verdict':'fail','required_repair':'policy-compliant action plus independently recomputed verification'},
        'source':'robust_trajectory_grader_false_accept_mining'
    })
with structured_path.open('w',encoding='utf-8') as f:
    for row in structured: f.write(json.dumps(row,sort_keys=True)+'\n')
report=['# Failure-driven trajectory training data','',
'This artifact turns evaluation failures into explicit correction pairs. It demonstrates the data-flywheel plumbing; it is not evidence that a frontier model has been post-trained on these pairs.','',
f'- Trajectories: {len(trials)}',f'- False-accept correction pairs: {len(pairs)}','',
'Each pair is generated only when a weaker grader accepts a gold-failing trajectory and the robust evidence-recomputing grader rejects it.','',
'## Files','', '- `data/agent_trajectories.jsonl`', '- `data/trajectory_failure_pairs.jsonl`', '- `data/trajectory_corrections.jsonl`']
(ROOT/'reports'/'TRACE_FAILURE_DATA.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(json.dumps({'trajectories':len(trials),'pairs':len(pairs)},indent=2))
