from personalagi.agent.core import PersonalAGIAgent


def test_sensitive_memory_is_blocked_but_ordinary_preference_is_stored():
    a=PersonalAGIAgent("u")
    out=a.observe("I prefer keeping my password secret.")
    assert out["blocked_memories"]
    assert a.memory.active("u") == []
    a.observe("I prefer short answers.")
    assert a.memory.get_by_key("u","preference.response_detail") is not None


def test_goal_lifecycle_completion_and_abandonment():
    a=PersonalAGIAgent("u")
    a.observe("My goal is finish the conference deck by Friday.")
    a.observe("I finished the conference deck.")
    assert list(a.state.goals.values())[0].status == "completed"
    b=PersonalAGIAgent("v")
    b.observe("I want to prepare the workshop demo.")
    b.observe("I canceled the workshop demo.")
    assert list(b.state.goals.values())[0].status == "abandoned"


def test_memory_audit_has_write_supersede_forget():
    a=PersonalAGIAgent("u")
    a.observe("I prefer working in the evening.")
    a.observe("Actually I prefer working in the morning.")
    assert a.memory.forget("u","preference.work_time")
    kinds=[e.event_type for e in a.memory.audit_log]
    assert "memory_write" in kinds
    assert "memory_supersede" in kinds
    assert "memory_forget" in kinds


def test_explicit_forget_command_wins():
    a=PersonalAGIAgent("u")
    a.observe("I prefer short answers.")
    out=a.observe("Forget that I prefer short answers.")
    assert "preference.response_detail" in out["forgotten_keys"]
    # Command itself must not silently recreate the deleted preference.
    assert a.memory.get_by_key("u","preference.response_detail") is None
