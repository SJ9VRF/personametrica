from personalagi.agent.core import PersonalAGIAgent


def test_agent_extracts_goal_and_preference():
    agent = PersonalAGIAgent("u")
    agent.observe("I prefer concise answers.")
    result = agent.observe("My goal is finish my talk.")
    assert len(agent.memory.active("u")) == 1
    assert len(result["active_goals"]) == 1
    assert result["active_goals"][0].description == "finish my talk"
