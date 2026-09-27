from personalagi.agent.core import PersonalAGIAgent
from personalbench.agent_evals.models import AgentEvalTask, AgentTrial
from personalbench.agent_evals.graders import RobustTrajectoryGrader

def test_runtime_emits_grader_ready_recovery_trace():
    a=PersonalAGIAgent('trace-user')
    expected={'text':'submit paper','when':'morning'}
    out=a.execute_verify_recover_trace('reminders','create',{'text':'submit paper','when':'evening'},expected,confirmation_granted=True)
    assert out['success'] and out['recovered']
    assert [e['type'] for e in out['events']].count('tool_call')==2
    task=AgentEvalTask('runtime-task','consequential_reminder',expected,confirmation_required=True)
    trial=AgentTrial('runtime-task','trial-1','runtime_recovery',out['events'],out['final_state'],True,True)
    assert RobustTrajectoryGrader().grade(task,trial).passed
