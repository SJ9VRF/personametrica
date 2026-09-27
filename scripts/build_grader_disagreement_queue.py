from __future__ import annotations
import json, sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.agent_evals import build_agent_eval_suite
from personalbench.agent_evals.graders import EndStateGrader, TrajectoryPolicyGrader, RobustTrajectoryGrader, EvidenceAwareTrajectoryGrader

tasks,trials=build_agent_eval_suite(n_tasks=100,trials_per_task=8,seed=23); tm={t.task_id:t for t in tasks}
priority={'forged_verification':5,'unsafe_shortcut':5,'false_claim':5,'missing_verification':4,'wrong_tool':4,'redundant_loop':3,'recoverable_mismatch':2,'clean':1}
rows=[]
for tr in trials:
    task=tm[tr.task_id]
    results={g.name:g.grade(task,tr) for g in [EndStateGrader(),TrajectoryPolicyGrader(),RobustTrajectoryGrader(),EvidenceAwareTrajectoryGrader()]}
    verdicts={k:('unknown' if v.abstained else ('pass' if v.passed else 'fail')) for k,v in results.items()}
    if len(set(verdicts.values())) <= 1:
        continue
    rows.append({
        'review_id':f'review-{len(rows):04d}','priority':priority.get(tr.perturbation,1),'task_id':tr.task_id,'trial_id':tr.trial_id,
        'perturbation':tr.perturbation,'gold_pass':tr.gold_pass,'gold_failure_reason':tr.gold_failure_reason,
        'grader_verdicts':verdicts,'grader_scores':{k:v.score for k,v in results.items()},'task':task.to_dict(),'trajectory':tr.to_dict(),
    })
rows.sort(key=lambda x:(-x['priority'],x['task_id'],x['trial_id']))
path=ROOT/'data'/'grader_disagreement_queue.jsonl'
with path.open('w',encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r,sort_keys=True)+'\n')
counts=Counter(r['perturbation'] for r in rows)
report=['# Grader disagreement review queue','',
'Cases where graders disagree are promoted to an explicit review queue rather than silently averaged away. This is the handoff point for independent human calibration or a separately validated judge model.','',
f'- Disagreement cases: {len(rows)}',f'- High-priority (priority ≥4): {sum(r["priority"]>=4 for r in rows)}','',
'## By failure type','']
for k,v in sorted(counts.items(),key=lambda kv:(-kv[1],kv[0])): report.append(f'- `{k}`: {v}')
report += ['','The queue intentionally contains gold labels for offline research auditing. A blinded annotation export should remove `gold_*` fields before human evaluation.']
(ROOT/'reports'/'GRADER_DISAGREEMENT_QUEUE.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(json.dumps({'disagreements':len(rows),'high_priority':sum(r['priority']>=4 for r in rows),'by_type':dict(counts)},indent=2))
