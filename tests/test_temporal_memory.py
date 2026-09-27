from personalagi.agent.core import PersonalAGIAgent
from personalagi.schemas import MemoryStatus

def test_preference_reversal_supersedes_old_value():
    a=PersonalAGIAgent("u")
    a.observe("I prefer working in the evening.")
    a.observe("Actually, mornings work better for me now.")
    active=a.memory.get_by_key("u","preference.work_time")
    assert active.value=="morning"
    hist=[m for m in a.memory.history("u") if m.key=="preference.work_time"]
    assert len(hist)==2
    assert hist[0].status==MemoryStatus.SUPERSEDED
    assert hist[1].supersedes==hist[0].memory_id

def test_conditional_detail_does_not_overwrite_general():
    a=PersonalAGIAgent("u")
    a.observe("I prefer concise answers.")
    a.observe("For technical topics, give me more detail.")
    assert a.memory.get_by_key("u","preference.response_detail").value=="concise"
    assert a.memory.get_by_key("u","preference.response_detail.technical").value=="detailed"
