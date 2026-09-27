from __future__ import annotations
from personalagi.schemas import ActionType, ProactivityDecision


class CalibratedProactivityPolicy:
    """Risk-aware policy exposing decision factors for eval/debugging."""
    def __init__(self, calibrated: bool = True):
        self.calibrated = calibrated

    def decide(self, *, goal_relevance: float, urgency: float, confidence: float,
               stakes: float, reversibility: float, autonomy_preference: float,
               historical_acceptance: float = 0.5, interruptibility: float = 0.5) -> ProactivityDecision:
        inputs = {
            "goal_relevance": goal_relevance, "urgency": urgency, "confidence": confidence,
            "stakes": stakes, "reversibility": reversibility, "autonomy_preference": autonomy_preference,
            "historical_acceptance": historical_acceptance, "interruptibility": interruptibility,
        }
        invalid = {k: v for k, v in inputs.items() if not 0.0 <= v <= 1.0}
        if invalid:
            raise ValueError(f"proactivity features must be in [0, 1]: {invalid}")
        if not self.calibrated:
            # Useful but deliberately naive: intervene whenever expected benefit appears high,
            # without special treatment of uncertainty, stakes, or reversibility.
            score = .45 * goal_relevance + .35 * urgency + .20 * historical_acceptance
            action = ActionType.SUGGEST if score >= .55 else (ActionType.REMIND if score >= .38 else ActionType.NONE)
        else:
            benefit = 0.30 * goal_relevance + 0.25 * urgency + 0.20 * historical_acceptance + 0.15 * confidence
            friction = 0.15 * (1 - interruptibility)
            autonomy_risk = 0.25 * stakes * (1 - reversibility) * (1 - autonomy_preference)
            score = max(-1.0, min(1.0, benefit - friction - autonomy_risk))
            if goal_relevance < 0.25 and urgency < 0.25:
                action = ActionType.NONE if interruptibility < 0.6 else ActionType.WAIT
            elif confidence < 0.55:
                action = ActionType.ASK
            elif stakes > 0.75 and reversibility < 0.35:
                action = ActionType.ASK
            elif score >= 0.62:
                action = ActionType.SUGGEST
            elif score >= 0.42 and urgency >= 0.65:
                action = ActionType.REMIND
            elif score >= 0.25:
                action = ActionType.WAIT
            else:
                action = ActionType.NONE
        factors = dict(goal_relevance=goal_relevance, urgency=urgency, confidence=confidence,
                       stakes=stakes, reversibility=reversibility, autonomy_preference=autonomy_preference,
                       historical_acceptance=historical_acceptance, interruptibility=interruptibility)
        rationale = [f'{k.replace("_"," ")}={v:.2f}' for k, v in factors.items()]
        return ProactivityDecision(action=action, score=score, confidence=confidence, factors=factors, rationale=rationale)
