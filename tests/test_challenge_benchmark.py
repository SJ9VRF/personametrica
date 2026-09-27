from personalagi.agent.core import PersonalAGIAgent
from personalbench.runner import evaluate_config
from personalagi.config import AgentConfig


def test_conditional_preferences_coexist():
    a=PersonalAGIAgent('u')
    a.observe('I prefer concise answers.')
    a.observe('For technical topics, I prefer detailed answers.')
    assert a.memory.get_by_key('u','preference.response_detail').value == 'concise'
    assert a.memory.get_by_key('u','preference.response_detail.technical').value == 'detailed'


def test_forgetting_removes_from_active_retrieval():
    a=PersonalAGIAgent('u'); a.observe('I prefer concise answers.')
    assert a.memory.forget('u','preference.response_detail')
    assert a.memory.get_by_key('u','preference.response_detail') is None
    assert all(r.key != 'preference.response_detail' for r,_ in a.memory.retrieve('u','concise answers'))


def test_challenge_metrics_are_reported():
    r=evaluate_config('full',AgentConfig.full(),n_users=10,turns=20,seed=3)['metrics']
    assert r['conditional_preference_accuracy'] == 1.0
    assert r['forget_success_rate'] == 1.0
    assert r['deleted_memory_retrieval_rate'] == 0.0
