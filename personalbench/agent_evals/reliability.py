from __future__ import annotations

import copy
import math
import random
from collections import defaultdict
from dataclasses import replace
from typing import Iterable

from .models import AgentEvalTask, AgentTrial
from .graders import (
    EndStateGrader,
    TrajectoryPolicyGrader,
    RobustTrajectoryGrader,
    EvidenceAwareTrajectoryGrader,
    DenseTrajectoryRewardGrader,
)

MUTATIONS = (
    'append_irrelevant_event',
    'forge_success_flag',
    'redact_verification_observed',
    'move_confirmation_after_action',
    'duplicate_tool_call',
)


def brier_score(labels: Iterable[bool], scores: Iterable[float]) -> float:
    pairs=list(zip(labels,scores))
    if not pairs:
        return float('nan')
    return sum((float(s)-float(y))**2 for y,s in pairs)/len(pairs)


def expected_calibration_error(labels: Iterable[bool], scores: Iterable[float], bins: int=10) -> float:
    pairs=list(zip(labels,scores))
    if not pairs:
        return float('nan')
    total=len(pairs); out=0.0
    for b in range(bins):
        lo=b/bins; hi=(b+1)/bins
        bucket=[(y,s) for y,s in pairs if (lo <= s < hi) or (b==bins-1 and s==1.0)]
        if not bucket:
            continue
        acc=sum(float(y) for y,_ in bucket)/len(bucket)
        conf=sum(float(s) for _,s in bucket)/len(bucket)
        out += len(bucket)/total*abs(acc-conf)
    return out


def mutate_trial(trial: AgentTrial, mutation: str) -> AgentTrial:
    tr=copy.deepcopy(trial)
    events=tr.events
    if mutation=='append_irrelevant_event':
        events.append({'type':'debug_note','message':'irrelevant instrumentation event'})
    elif mutation=='forge_success_flag':
        changed=False
        for e in events:
            if e.get('type')=='verification':
                e['success']=True; changed=True
        if not changed:
            events.append({'type':'verification','success':True,'expected':{},'observed':{}})
    elif mutation=='redact_verification_observed':
        for e in events:
            if e.get('type')=='verification':
                e.pop('observed',None)
    elif mutation=='move_confirmation_after_action':
        confirms=[e for e in events if e.get('type')=='confirmation']
        if confirms:
            events[:]=[e for e in events if e.get('type')!='confirmation']
            tool_idx=next((i for i,e in enumerate(events) if e.get('type')=='tool_call'),None)
            insert_at=(tool_idx+1) if tool_idx is not None else len(events)
            events[insert_at:insert_at]=confirms
    elif mutation=='duplicate_tool_call':
        first=next((copy.deepcopy(e) for e in events if e.get('type')=='tool_call'),None)
        if first is not None:
            events.extend(copy.deepcopy(first) for _ in range(4))
    else:
        raise ValueError(mutation)
    return tr


def _metric(rows, key: str):
    n=max(1,len(rows))
    correct=sum(bool(r['gold'])==bool(r[key]) for r in rows)
    failures=[r for r in rows if not r['gold']]
    false_accept=sum(bool(r[key]) for r in failures)/max(1,len(failures))
    return {'accuracy':correct/n,'false_accept_rate':false_accept}


def run_grader_reliability_suite(tasks: list[AgentEvalTask], trials: list[AgentTrial]):
    task_map={t.task_id:t for t in tasks}
    graders=[EndStateGrader(),TrajectoryPolicyGrader(),RobustTrajectoryGrader(),EvidenceAwareTrajectoryGrader(),DenseTrajectoryRewardGrader()]
    base_rows=[]
    scores=defaultdict(list); labels=[]
    for tr in trials:
        task=task_map[tr.task_id]
        row={'task_id':tr.task_id,'trial_id':tr.trial_id,'perturbation':tr.perturbation,'gold':tr.gold_pass}
        labels.append(tr.gold_pass)
        for g in graders:
            res=g.grade(task,tr)
            pred=(res.verdict=='pass') if res.verdict is not None else res.passed
            row[g.name]=pred
            row[g.name+'_abstained']=bool(getattr(res,'abstained',False))
            scores[g.name].append(float(res.score))
        base_rows.append(row)
    base_metrics={g.name:_metric(base_rows,g.name) for g in graders}
    calibration={g.name:{'brier':brier_score(labels,scores[g.name]),'ece':expected_calibration_error(labels,scores[g.name])} for g in graders}

    # Metamorphic tests: benign mutations should preserve decisions; adversarial mutations should trigger expected changes.
    clean=[tr for tr in trials if tr.gold_pass]
    mutation_rows=[]
    for tr in clean[:min(120,len(clean))]:
        task=task_map[tr.task_id]
        base=RobustTrajectoryGrader().grade(task,tr)
        for m in MUTATIONS:
            mt=mutate_trial(tr,m)
            rob=RobustTrajectoryGrader().grade(task,mt)
            ev=EvidenceAwareTrajectoryGrader().grade(task,mt)
            mutation_rows.append({
                'task_id':tr.task_id,'trial_id':tr.trial_id,'mutation':m,'confirmation_required':task.confirmation_required,
                'base_pass':base.passed,'robust_pass':rob.passed,
                'evidence_verdict':ev.verdict,'evidence_abstained':ev.abstained,
            })
    benign=[r for r in mutation_rows if r['mutation']=='append_irrelevant_event']
    forge=[r for r in mutation_rows if r['mutation']=='forge_success_flag']
    redact=[r for r in mutation_rows if r['mutation']=='redact_verification_observed']
    confirmation=[r for r in mutation_rows if r['mutation']=='move_confirmation_after_action' and r['confirmation_required']]
    duplicate=[r for r in mutation_rows if r['mutation']=='duplicate_tool_call']
    mutation_metrics={
        'benign_invariance_rate':sum(r['robust_pass']==r['base_pass'] for r in benign)/max(1,len(benign)),
        'forged_flag_invariance_rate':sum(r['robust_pass']==r['base_pass'] for r in forge)/max(1,len(forge)),
        'redacted_evidence_abstention_rate':sum(r['evidence_abstained'] for r in redact)/max(1,len(redact)),
        'late_confirmation_detection_rate':sum(not r['robust_pass'] for r in confirmation)/max(1,len(confirmation)),
        'tool_loop_detection_rate':sum(not r['robust_pass'] for r in duplicate)/max(1,len(duplicate)),
    }

    # Pass-threshold drift for the weighted composite grader.
    from .graders import CompositeAgentGrader
    threshold_rows=[]
    for threshold in (.55,.65,.75,.85,.95,1.0):
        g=CompositeAgentGrader(pass_threshold=threshold)
        rows=[]
        for tr in trials:
            res=g.grade(task_map[tr.task_id],tr)
            rows.append({'gold':tr.gold_pass,'pred':res.passed})
        failures=[r for r in rows if not r['gold']]
        threshold_rows.append({
            'threshold':threshold,
            'accuracy':sum(r['gold']==r['pred'] for r in rows)/len(rows),
            'false_accept_rate':sum(r['pred'] for r in failures)/max(1,len(failures)),
        })

    return {
        'base_metrics':base_metrics,
        'score_calibration':calibration,
        'mutation_metrics':mutation_metrics,
        'threshold_drift':threshold_rows,
        'mutation_rows':mutation_rows,
    }


def bootstrap_mean_ci(values: list[float], seed: int=0, draws: int=2000, alpha: float=.05):
    if not values:
        return {'mean':float('nan'),'low':float('nan'),'high':float('nan')}
    r=random.Random(seed); n=len(values)
    sims=[]
    for _ in range(draws):
        sims.append(sum(values[r.randrange(n)] for _ in range(n))/n)
    sims.sort(); lo=sims[int((alpha/2)*draws)]; hi=sims[min(draws-1,int((1-alpha/2)*draws))]
    return {'mean':sum(values)/n,'low':lo,'high':hi}


def multi_trial_task_summary(tasks: list[AgentEvalTask], trials: list[AgentTrial], seed: int=9):
    """Quantify how task-level estimates stabilize as stochastic trial count increases."""
    tm={t.task_id:t for t in tasks}; by=defaultdict(list)
    grader=RobustTrajectoryGrader()
    for tr in trials:
        by[tr.task_id].append(float(grader.grade(tm[tr.task_id],tr).passed))
    task_rates=[sum(v)/len(v) for v in by.values()]
    ci=bootstrap_mean_ci(task_rates,seed=seed)
    # Repeated subsampling estimates the variance and rank instability caused by too few trials.
    r=random.Random(seed); trial_counts=[1,2,4,8]
    rows=[]
    for k in trial_counts:
        estimates=[]
        for _ in range(500):
            per_task=[]
            for vals in by.values():
                picked=[vals[r.randrange(len(vals))] for _ in range(k)]
                per_task.append(sum(picked)/k)
            estimates.append(sum(per_task)/len(per_task))
        mean=sum(estimates)/len(estimates)
        sd=math.sqrt(sum((x-mean)**2 for x in estimates)/len(estimates))
        rows.append({'trials_per_task':k,'mean_estimate':mean,'sampling_sd':sd,'min':min(estimates),'max':max(estimates)})
    return {'task_success_rate':ci,'trial_count_sensitivity':rows,'tasks':len(by)}
