from personalagi.proactivity.policy import CalibratedProactivityPolicy
from personalagi.schemas import ActionType


def test_high_stakes_irreversible_action_asks_first():
    policy = CalibratedProactivityPolicy()
    d = policy.decide(
        goal_relevance=0.9,
        urgency=0.9,
        confidence=0.95,
        stakes=0.95,
        reversibility=0.1,
        autonomy_preference=0.2,
        historical_acceptance=0.8,
        interruptibility=0.9,
    )
    assert d.action == ActionType.ASK


def test_low_risk_high_value_intervention_suggests():
    policy = CalibratedProactivityPolicy()
    d = policy.decide(
        goal_relevance=1.0,
        urgency=1.0,
        confidence=0.95,
        stakes=0.1,
        reversibility=1.0,
        autonomy_preference=0.5,
        historical_acceptance=1.0,
        interruptibility=1.0,
    )
    assert d.action == ActionType.SUGGEST
