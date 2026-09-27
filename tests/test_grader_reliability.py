from personalbench.agent_evals import build_agent_eval_suite
from personalbench.agent_evals.reliability import run_grader_reliability_suite, multi_trial_task_summary, mutate_trial
from personalbench.agent_evals.graders import EvidenceAwareTrajectoryGrader, RobustTrajectoryGrader

def test_missing_observation_causes_abstention():
    tasks,trials=build_agent_eval_suite(n_tasks=8,trials_per_task=8,seed=2); tm={t.task_id:t for t in tasks}
    clean=next(t for t in trials if t.gold_pass and any(e.get('type')=='verification' for e in t.events))
    tr=mutate_trial(clean,'redact_verification_observed')
    res=EvidenceAwareTrajectoryGrader().grade(tm[tr.task_id],tr)
    assert res.abstained and res.verdict=='unknown'

def test_benign_mutation_is_invariant():
    tasks,trials=build_agent_eval_suite(n_tasks=8,trials_per_task=8,seed=2); tm={t.task_id:t for t in tasks}
    clean=next(t for t in trials if t.gold_pass)
    base=RobustTrajectoryGrader().grade(tm[clean.task_id],clean).passed
    changed=RobustTrajectoryGrader().grade(tm[clean.task_id],mutate_trial(clean,'append_irrelevant_event')).passed
    assert base==changed

def test_reliability_suite_catches_policy_mutations():
    tasks,trials=build_agent_eval_suite(n_tasks=20,trials_per_task=8,seed=4)
    out=run_grader_reliability_suite(tasks,trials)
    m=out['mutation_metrics']
    assert m['benign_invariance_rate']==1.0
    assert m['forged_flag_invariance_rate']==1.0
    assert m['redacted_evidence_abstention_rate']==1.0
    assert m['tool_loop_detection_rate']==1.0

def test_more_trials_reduce_sampling_variance():
    tasks,trials=build_agent_eval_suite(n_tasks=30,trials_per_task=8,seed=5)
    rows=multi_trial_task_summary(tasks,trials,seed=5)['trial_count_sensitivity']
    assert rows[-1]['sampling_sd'] < rows[0]['sampling_sd']
