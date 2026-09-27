from personalagi.agent.core import PersonalAGIAgent


def test_snapshot_roundtrip_preserves_current_and_history(tmp_path):
    a=PersonalAGIAgent('u')
    a.observe('I prefer working in the evening.')
    a.observe('Actually mornings work better for me now.')
    a.observe('My goal is finish the paper.')
    path=tmp_path/'snapshot.json'
    a.save_snapshot(str(path))

    b=PersonalAGIAgent('u')
    b.load_snapshot(str(path))
    assert b.memory.get_by_key('u','preference.work_time').value == 'morning'
    assert len(b.memory.history('u')) == 2
    assert len(b.goals.active(b.state)) == 1


def test_snapshot_rejects_wrong_user(tmp_path):
    a=PersonalAGIAgent('u1'); a.observe('I prefer concise answers.')
    path=tmp_path/'snapshot.json'; a.save_snapshot(str(path))
    b=PersonalAGIAgent('u2')
    try:
        b.load_snapshot(str(path))
    except ValueError as e:
        assert 'user_id' in str(e)
    else:
        raise AssertionError('expected user mismatch failure')


def test_snapshot_restores_events_feedback_tools_and_audit(tmp_path):
    from personalagi.agent.core import PersonalAGIAgent
    from personalagi.schemas import SourceType
    a=PersonalAGIAgent("full-state")
    a.observe("I prefer short answers.")
    a.feedback.add("useful", 1.0, source=SourceType.EXPLICIT, comment="good")
    a.tools.call("notes","add",{"text":"remember demo"})
    a.memory.forget("full-state","preference.response_detail")
    path=tmp_path/"state-v2.json"
    a.save_snapshot(path)

    b=PersonalAGIAgent("full-state")
    b.load_snapshot(path)
    assert len(b.events)==1
    assert b.feedback.acceptance_rate()==1.0
    assert b.tools.notes==["remember demo"]
    assert any(x.event_type=="memory_forget" for x in b.memory.audit_log)
