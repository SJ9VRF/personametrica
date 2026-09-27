from personalagi.agent.core import PersonalAGIAgent
from personalbench.tasks.adversarial import PREFERENCE_STRESS_CASES, REVERSAL_SEQUENCES


def test_preference_stress_suite_has_reasonable_coverage():
    correct=0
    for i,(msg,key,expected) in enumerate(PREFERENCE_STRESS_CASES):
        a=PersonalAGIAgent(f"s{i}"); a.observe(msg)
        m=a.memory.get_by_key(a.state.user_id,key)
        correct += int(m is not None and m.value==expected)
    assert correct / len(PREFERENCE_STRESS_CASES) >= 0.8


def test_temporal_reversal_sequences():
    for i,(msgs,key,expected) in enumerate(REVERSAL_SEQUENCES):
        a=PersonalAGIAgent(f"r{i}")
        for msg in msgs: a.observe(msg)
        m=a.memory.get_by_key(a.state.user_id,key)
        assert m is not None and m.value==expected
