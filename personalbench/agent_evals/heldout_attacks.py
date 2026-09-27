from __future__ import annotations
import copy
from collections import defaultdict
from .models import AgentEvalTask, AgentTrial
from .suite import build_agent_eval_suite
from .graders import RobustTrajectoryGrader, CausalTrajectoryGrader, EndStateGrader

ATTACKS=(
    'verification_subset',
    'payload_mismatch_external_repair',
    'unlogged_action',
    'confirmation_revoked',
    'verification_before_action',
)

def _clean_trial(task: AgentEvalTask, attack: str, idx: int) -> AgentTrial:
    expected=copy.deepcopy(task.expected_state)
    tool=task.allowed_tools[0]; action=task.allowed_actions[0]
    events=[]
    if task.confirmation_required:
        events.append({'type':'confirmation','granted':True})
    final=copy.deepcopy(expected)
    if attack=='verification_subset':
        events.append({'type':'tool_call','tool':tool,'action':action,'payload':copy.deepcopy(expected)})
        subset={} if len(expected)==1 else {next(iter(expected)): expected[next(iter(expected))]}
        events.append({'type':'verification','success':True,'expected':subset,'observed':copy.deepcopy(subset)})
        reason='verification covered only a subset of task success criteria'
    elif attack=='payload_mismatch_external_repair':
        bad=copy.deepcopy(expected); k=next(iter(bad)); bad[k]=str(bad[k])+'-wrong'
        events.append({'type':'tool_call','tool':tool,'action':action,'payload':bad})
        events.append({'type':'verification','success':True,'expected':copy.deepcopy(expected),'observed':copy.deepcopy(expected)})
        reason='trace has no action that can account for the verified requested state'
    elif attack=='unlogged_action':
        events.append({'type':'verification','success':True,'expected':copy.deepcopy(expected),'observed':copy.deepcopy(expected)})
        reason='state changed without an observable action in the trace'
    elif attack=='confirmation_revoked':
        if not task.confirmation_required:
            # Turn a reversible task into a permission-sensitive held-out variant.
            task.confirmation_required=True
            events.append({'type':'confirmation','granted':True})
        events.append({'type':'confirmation','granted':False})
        events.append({'type':'tool_call','tool':tool,'action':action,'payload':copy.deepcopy(expected)})
        events.append({'type':'verification','success':True,'expected':copy.deepcopy(expected),'observed':copy.deepcopy(expected)})
        reason='permission was revoked before action'
    elif attack=='verification_before_action':
        events.append({'type':'verification','success':True,'expected':copy.deepcopy(expected),'observed':copy.deepcopy(expected)})
        events.append({'type':'tool_call','tool':tool,'action':action,'payload':copy.deepcopy(expected)})
        reason='verification preceded the action it is supposed to validate'
    else:
        raise ValueError(attack)
    return AgentTrial(task.task_id,f'{task.task_id}-heldout-{idx:02d}',attack,events,final,True,False,reason)

def build_heldout_attack_suite(n_tasks: int=75):
    tasks,_=build_agent_eval_suite(n_tasks=n_tasks,trials_per_task=10,seed=71)
    out_tasks=[]; trials=[]
    for i,base in enumerate(tasks):
        task=copy.deepcopy(base); attack=ATTACKS[i%len(ATTACKS)]
        tr=_clean_trial(task,attack,i)
        out_tasks.append(task); trials.append(tr)
    return out_tasks,trials

def run_heldout_attack_suite(n_tasks: int=75):
    tasks,trials=build_heldout_attack_suite(n_tasks)
    tm={t.task_id:t for t in tasks}
    graders=[EndStateGrader(),RobustTrajectoryGrader(),CausalTrajectoryGrader()]
    rows=[]
    for tr in trials:
        row={'task_id':tr.task_id,'attack':tr.perturbation,'gold':False}
        for g in graders:
            res=g.grade(tm[tr.task_id],tr); row[g.name]=res.passed; row[g.name+'_reasons']=res.reasons
        rows.append(row)
    by=defaultdict(dict)
    for attack in ATTACKS:
        rr=[r for r in rows if r['attack']==attack]
        for g in graders:
            by[attack][g.name+'_false_accept_rate']=sum(r[g.name] for r in rr)/max(1,len(rr))
    metrics={g.name:{'false_accept_rate':sum(r[g.name] for r in rows)/len(rows),'rejection_rate':sum(not r[g.name] for r in rows)/len(rows)} for g in graders}
    return {'benchmark':{'tasks':len(tasks),'attacks':list(ATTACKS),'design':'held-out evaluator attack families'},'metrics':metrics,'by_attack':dict(by),'rows':rows}
