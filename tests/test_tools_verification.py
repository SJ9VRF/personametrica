from personalagi.tools import SandboxTools
from personalagi.verification import OutcomeVerifier

def test_tool_result_can_be_verified():
    tools=SandboxTools(); v=OutcomeVerifier()
    r=tools.call("task_store","create",{"title":"finish deck"})
    assert r.success
    vr=v.verify_subset({"title":"finish deck"},r.payload)
    assert vr.success
