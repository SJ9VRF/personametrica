from personalagi.feedback import FeedbackEngine
from personalagi.reward import MultiObjectiveRewardModel

def test_feedback_acceptance_rate():
    f=FeedbackEngine(); f.add("useful",1); f.add("useful",-1)
    assert f.acceptance_rate()==.5

def test_reward_penalizes_autonomy_violation():
    rm=MultiObjectiveRewardModel()
    good=rm.score(correct=True,memory_relevant=True,personalized=True,proactive_accepted=True,autonomy_violation=False)
    bad=rm.score(correct=True,memory_relevant=True,personalized=True,proactive_accepted=True,autonomy_violation=True)
    assert good.weighted()>bad.weighted()
