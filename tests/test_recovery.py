from personalagi.agent.core import PersonalAGIAgent

def test_verified_retry_recovers_payload_mismatch():
    a=PersonalAGIAgent('recover')
    out=a.execute_verify_recover(
        'reminders','create',
        {'text':'Work on deck','when':'evening'},
        {'text':'Work on deck','when':'morning'},
    )
    assert out['recovered'] is True
    assert out['success'] is True
    assert len(out['trace']) == 2
    assert out['trace'][0]['verification'].success is False
    assert out['trace'][1]['verification'].success is True

def test_verified_retry_does_not_retry_success():
    a=PersonalAGIAgent('recover-ok')
    out=a.execute_verify_recover('notes','add',{'text':'hello'},{'text':'hello'})
    assert out['success'] is True
    assert out['recovered'] is False
    assert len(out['trace']) == 1
