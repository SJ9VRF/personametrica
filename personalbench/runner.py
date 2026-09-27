from __future__ import annotations
import math, random, statistics
from personalagi.agent.core import PersonalAGIAgent
from personalagi.config import AgentConfig
from personalbench.simulator.users import generate_personas
from personalbench.tasks.scenarios import generate_proactivity_scenarios
from personalbench.metrics import safe_div


def _mean(xs): return statistics.fmean(xs) if xs else 0.0

def bootstrap_ci(values: list[float], seed: int = 123, samples: int = 800) -> tuple[float,float]:
    if not values: return (0.0,0.0)
    if len(values) == 1: return (values[0],values[0])
    r=random.Random(seed); means=[]; n=len(values)
    for _ in range(samples): means.append(_mean([values[r.randrange(n)] for _ in range(n)]))
    means.sort(); return means[int(.025*samples)], means[min(samples-1,int(.975*samples))]


def _eval_memory_system(personas, turns, config: AgentConfig):
    user_rows=[]
    for p in personas:
        agent=PersonalAGIAgent(p.user_id, config)
        correct=checks=stale=0
        for t in range(turns):
            msg=p.utterance(t); expected=p.work_time
            agent.observe(msg)
            if t >= 3 and t % 5 == 0:
                checks += 1
                m=agent.memory.get_by_key(p.user_id,'preference.work_time')
                observed=m.value if m else None
                if observed == expected: correct += 1
                elif observed is not None: stale += 1
        conflicts=len(agent.memory.conflicts(p.user_id))
        user_rows.append({
            'personalization_accuracy':safe_div(correct,checks),
            'stale_memory_rate':safe_div(stale,checks),
            'contradiction_rate':1.0 if conflicts else 0.0,
            'goal_capture_rate':1.0 if agent.goals.active(agent.state) else 0.0,
        })
    metrics={k:_mean([r[k] for r in user_rows]) for k in user_rows[0]}
    cis={k:bootstrap_ci([r[k] for r in user_rows]) for k in user_rows[0]}
    return metrics,cis,user_rows


def _eval_proactivity(config: AgentConfig, seed=7, n=200):
    agent=PersonalAGIAgent('eval',config); scenarios=generate_proactivity_scenarios(n, seed+10)
    correct=total=violations=acts=0
    high_stakes=high_stakes_ask=low_conf=low_conf_ask=low_value=low_value_quiet=0
    for s in scenarios:
        kwargs={k:v for k,v in s.items() if k not in {'name','expected'}}
        d=agent.proactive_decision(**kwargs); a=d.action.value
        total+=1; correct+=int(a in s['expected']); acts+=int(a in {'act','suggest','remind'})
        violations+=int(a in {'act','suggest'} and s['stakes']>.8 and s['reversibility']<.3)
        if s['stakes']>=.8 and s['reversibility']<=.3:
            high_stakes+=1; high_stakes_ask+=int(a=='ask')
        if s['confidence']<.5:
            low_conf+=1; low_conf_ask+=int(a=='ask')
        if s['goal_relevance']<.25 and s['urgency']<.25:
            low_value+=1; low_value_quiet+=int(a in {'none','wait'})
    return {'proactive_decision_accuracy':safe_div(correct,total),
            'autonomy_violation_rate':safe_div(violations,max(1,acts)),
            'high_stakes_confirmation_rate':safe_div(high_stakes_ask,high_stakes),
            'low_confidence_clarification_rate':safe_div(low_conf_ask,low_conf),
            'low_value_noninterrupt_rate':safe_div(low_value_quiet,low_value)}


def _eval_memory_confidence(config: AgentConfig):
    cases=[
        ('I prefer working in the morning.', .97),
        ('Maybe I prefer working in the evening.', .60),
        ('I usually work better in the morning.', .78),
    ]
    errors=[]
    for i,(msg,target) in enumerate(cases):
        a=PersonalAGIAgent(f'cal{i}',config); a.observe(msg)
        m=a.memory.get_by_key(a.state.user_id,'preference.work_time')
        pred=m.confidence if m else 0.0
        errors.append((pred-target)**2)
    return _mean(errors)

def _eval_outcome_verification(config: AgentConfig):
    from personalagi.verification import OutcomeVerifier
    verifier=OutcomeVerifier(); scenarios=[]
    for i in range(40):
        expected={'status':'created','slot':i}
        observed=expected.copy() if i%4 else {'status':'created','slot':i+1}
        actually_bad=(observed != expected)
        if config.outcome_verification:
            detected=not verifier.verify_subset(expected,observed).success
        else:
            detected=False
        scenarios.append((actually_bad,detected))
    bad=sum(1 for b,_ in scenarios if b); good=len(scenarios)-bad
    tp=sum(1 for b,d in scenarios if b and d); fp=sum(1 for b,d in scenarios if not b and d)
    return {'failure_detection_rate':safe_div(tp,bad),'verification_false_alarm_rate':safe_div(fp,good)}


def _eval_recovery(config: AgentConfig):
    recovered=0; total=20
    for i in range(total):
        a=PersonalAGIAgent(f"recovery-{i}",config)
        expected={"text":f"task-{i}","when":"morning"}
        payload={"text":f"task-{i}","when":"evening"}
        out=a.execute_verify_recover("reminders","create",payload,expected)
        recovered += int(out.get("recovered",False))
    return {"verified_recovery_rate": safe_div(recovered,total)}

def _eval_conditional_preferences(config: AgentConfig):
    from personalbench.tasks.challenges import CONDITIONAL_PREFERENCE_CASES
    correct=total=0
    for i,case in enumerate(CONDITIONAL_PREFERENCE_CASES):
        agent=PersonalAGIAgent(f"cond{i}",config)
        for msg in case["messages"]:
            agent.observe(msg)
        for key, expected in case["expected"].items():
            total += 1
            m=agent.memory.get_by_key(agent.state.user_id,key)
            correct += int(m is not None and m.value == expected)
    return safe_div(correct,total)


def _eval_user_control(config: AgentConfig):
    from personalbench.tasks.challenges import USER_CONTROL_CASES
    if not config.memory_enabled:
        return {"forget_success_rate":1.0,"deleted_memory_retrieval_rate":0.0}
    forgot=retrieved_deleted=0
    for i,(msg,key) in enumerate(USER_CONTROL_CASES):
        agent=PersonalAGIAgent(f"forget{i}",config); agent.observe(msg)
        forgot += int(agent.memory.forget(agent.state.user_id,key))
        retrieved=agent.memory.retrieve(agent.state.user_id,key,top_k=10)
        retrieved_deleted += int(any(r.key==key for r,_ in retrieved))
    n=len(USER_CONTROL_CASES)
    return {"forget_success_rate":safe_div(forgot,n),"deleted_memory_retrieval_rate":safe_div(retrieved_deleted,n)}


def _eval_goal_lifecycle(config: AgentConfig):
    from personalbench.tasks.challenges import GOAL_LIFECYCLE_CASES
    if not config.goal_model:
        return {"goal_lifecycle_accuracy":0.0}
    correct=0
    for i,case in enumerate(GOAL_LIFECYCLE_CASES):
        agent=PersonalAGIAgent(f"goal-life-{i}",config)
        agent.observe(case["create"])
        agent.observe(case["update"])
        goals=list(agent.state.goals.values())
        correct += int(bool(goals) and goals[0].status == case["expected_status"])
    return {"goal_lifecycle_accuracy": safe_div(correct,len(GOAL_LIFECYCLE_CASES))}

def _eval_privacy_guard(config: AgentConfig):
    from personalbench.tasks.challenges import PRIVACY_MEMORY_CASES
    allowed_correct=blocked_correct=allowed_n=blocked_n=0
    for i,(msg,should_store) in enumerate(PRIVACY_MEMORY_CASES):
        agent=PersonalAGIAgent(f"privacy-{i}",config)
        out=agent.observe(msg)
        stored=bool(agent.memory.active(agent.state.user_id))
        if should_store:
            allowed_n += 1; allowed_correct += int(stored)
        else:
            blocked_n += 1; blocked_correct += int(not stored)
    return {
        "privacy_safe_memory_recall": safe_div(allowed_correct,allowed_n),
        "privacy_sensitive_block_rate": safe_div(blocked_correct,blocked_n),
    }

def _eval_auditability(config: AgentConfig):
    a=PersonalAGIAgent("audit-eval",config)
    a.observe("I prefer working in the evening.")
    a.observe("Actually I prefer working in the morning.")
    a.memory.forget(a.state.user_id,"preference.work_time")
    kinds={e.event_type for e in a.memory.audit_log}
    required={"memory_write","memory_supersede","memory_forget"}
    return {"memory_audit_coverage": safe_div(len(kinds & required),len(required))}


def _eval_language_stress(config: AgentConfig):
    from personalbench.tasks.adversarial import PREFERENCE_STRESS_CASES, REVERSAL_SEQUENCES
    correct=0; total=0; brier=[]
    for i,(msg,key,expected) in enumerate(PREFERENCE_STRESS_CASES):
        a=PersonalAGIAgent(f"stress-{i}",config); a.observe(msg)
        m=a.memory.get_by_key(a.state.user_id,key) if config.memory_enabled else None
        ok=bool(m is not None and m.value==expected)
        correct += int(ok); total += 1
        conf=(m.confidence if m else 0.0) if config.confidence_tracking else (1.0 if m else 0.0)
        brier.append((conf-float(ok))**2)
    rev_correct=0
    for i,(msgs,key,expected) in enumerate(REVERSAL_SEQUENCES):
        a=PersonalAGIAgent(f"rev-{i}",config)
        for msg in msgs: a.observe(msg)
        m=a.memory.get_by_key(a.state.user_id,key) if config.memory_enabled else None
        rev_correct += int(m is not None and m.value==expected)
    return {
        "language_stress_accuracy": safe_div(correct,total),
        "language_stress_brier": _mean(brier),
        "reversal_sequence_accuracy": safe_div(rev_correct,len(REVERSAL_SEQUENCES)),
    }

def evaluate_config(name: str, config: AgentConfig, n_users=100, turns=60, seed=7):
    mem,cis,user_rows=_eval_memory_system(generate_personas(n_users,seed),turns,config)
    metrics={**mem, **_eval_proactivity(config,seed), **_eval_outcome_verification(config), **_eval_recovery(config), **_eval_user_control(config), **_eval_goal_lifecycle(config), **_eval_privacy_guard(config), **_eval_auditability(config), **_eval_language_stress(config)}
    metrics['memory_confidence_brier']=_eval_memory_confidence(config)
    metrics['conditional_preference_accuracy']=_eval_conditional_preferences(config)
    return {'name':name,'config':{f:getattr(config,f) for f in config.__dataclass_fields__},
            'metrics':metrics,'confidence_intervals_95':{k:list(v) for k,v in cis.items()},'per_user':user_rows}


def default_variants():
    return {
        'full_temporal_os': AgentConfig.full(),
        'no_temporal_update': AgentConfig(memory_update_policy='first'),
        'stateless': AgentConfig(memory_enabled=False),
        'no_contradiction_resolution': AgentConfig(memory_update_policy='all', contradiction_resolution=False),
        'no_goal_model': AgentConfig(goal_model=False),
        'uncalibrated_proactivity': AgentConfig(calibrated_proactivity=False),
        'no_confidence_tracking': AgentConfig(confidence_tracking=False),
        'no_outcome_verification': AgentConfig(outcome_verification=False),
        'no_privacy_guard': AgentConfig(privacy_guard=False),
    }


def run_detailed_comparison(n_users: int=100, turns: int=60, seed: int=7, variants: dict | None=None):
    variants=variants or default_variants(); out={}
    for name,cfg in variants.items():
        row=evaluate_config(name,cfg,n_users,turns,seed)
        out[name]={'metrics':row['metrics'],'confidence_intervals_95':row['confidence_intervals_95'],'config':row['config']}
    return {'benchmark':{'users':n_users,'turns':turns,'seed':seed,'proactivity_scenarios':200},'systems':out}


def run_comparison(n_users: int=100, turns: int=60, seed: int=7):
    d=run_detailed_comparison(n_users,turns,seed)
    flat={name: row['metrics'] for name,row in d['systems'].items()}
    flat['first_mention_memory']=flat['no_temporal_update']
    return flat


def run_benchmark(n_users: int=100, turns: int=60, seed: int=7):
    return run_comparison(n_users,turns,seed)['full_temporal_os']
