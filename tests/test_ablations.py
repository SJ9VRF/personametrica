from personalagi.agent.core import PersonalAGIAgent
from personalagi.config import AgentConfig
from personalbench.runner import run_detailed_comparison


def test_temporal_update_ablation_has_stale_memory():
    r=run_detailed_comparison(20,45,seed=2)['systems']
    assert r['full_temporal_os']['metrics']['stale_memory_rate'] == 0
    assert r['no_temporal_update']['metrics']['stale_memory_rate'] > .3


def test_contradiction_ablation_creates_conflicts():
    r=run_detailed_comparison(20,45,seed=2)['systems']
    assert r['full_temporal_os']['metrics']['contradiction_rate'] == 0
    assert r['no_contradiction_resolution']['metrics']['contradiction_rate'] > 0


def test_goal_model_ablation_is_real():
    a=PersonalAGIAgent('u',AgentConfig(goal_model=False)); a.observe('My goal is finish the report by Friday.')
    assert not a.goals.active(a.state)


def test_outcome_verification_ablation_is_real():
    a=PersonalAGIAgent('u',AgentConfig(outcome_verification=False))
    _,verification=a.execute_and_verify('notes','add',{'text':'x'},{'text':'wrong'})
    assert verification is None


def test_confidence_tracking_ablation_changes_memory_confidence():
    a=PersonalAGIAgent('u',AgentConfig(confidence_tracking=False)); a.observe('Maybe I prefer working in the morning.')
    assert a.memory.get_by_key('u','preference.work_time').confidence == 1.0


def test_benchmark_reproducible():
    a=run_detailed_comparison(12,30,seed=99)
    b=run_detailed_comparison(12,30,seed=99)
    assert a == b
