from personalbench.agent_evals import build_agent_eval_suite, run_agent_eval_suite
from personalbench.agent_evals.graders import EndStateGrader, TrajectoryPolicyGrader, RobustTrajectoryGrader

def test_suite_is_deterministic():
    a=run_agent_eval_suite(n_tasks=12,trials_per_task=8,seed=4)
    b=run_agent_eval_suite(n_tasks=12,trials_per_task=8,seed=4)
    assert a['grader_metrics']==b['grader_metrics']

def test_end_state_grader_accepts_some_unsafe_shortcuts():
    tasks,trials=build_agent_eval_suite(n_tasks=10,trials_per_task=8,seed=3)
    tm={t.task_id:t for t in tasks}
    unsafe=[tr for tr in trials if tr.perturbation=='unsafe_shortcut' and not tr.gold_pass]
    assert unsafe
    assert any(EndStateGrader().grade(tm[tr.task_id],tr).passed for tr in unsafe)

def test_robust_grader_rejects_forged_verification():
    tasks,trials=build_agent_eval_suite(n_tasks=10,trials_per_task=8,seed=3)
    tm={t.task_id:t for t in tasks}
    forged=[tr for tr in trials if tr.perturbation=='forged_verification']
    assert forged
    assert any(TrajectoryPolicyGrader().grade(tm[tr.task_id],tr).passed for tr in forged)
    assert all(not RobustTrajectoryGrader().grade(tm[tr.task_id],tr).passed for tr in forged)

def test_robust_grader_matches_gold_in_authored_suite():
    out=run_agent_eval_suite(n_tasks=20,trials_per_task=8,seed=8)
    assert out['grader_metrics']['robust_trajectory']['accuracy']==1.0
