from personalbench.agent_evals.heldout_attacks import run_heldout_attack_suite
from personalbench.agent_evals.suite import build_agent_eval_suite
from personalbench.agent_evals.graders import CausalTrajectoryGrader


def test_causal_grader_preserves_original_gold_suite():
    tasks,trials=build_agent_eval_suite(n_tasks=30,trials_per_task=10,seed=17)
    tm={t.task_id:t for t in tasks}; g=CausalTrajectoryGrader()
    assert all(g.grade(tm[tr.task_id],tr).passed == tr.gold_pass for tr in trials)


def test_causal_grader_rejects_heldout_attack_families():
    out=run_heldout_attack_suite(n_tasks=50)
    assert out['metrics']['causal_trajectory']['false_accept_rate'] == 0.0
    assert out['metrics']['robust_trajectory']['false_accept_rate'] > 0.5


def test_heldout_attack_families_are_separate_from_authored_suite():
    out=run_heldout_attack_suite(n_tasks=25)
    assert len(out['benchmark']['attacks']) == 5
    assert 'verification_subset' in out['benchmark']['attacks']
