from __future__ import annotations
from personalagi.schemas import RewardVector


class MultiObjectiveRewardModel:
    """Auditable local reward model used as a reproducible substitute for a learned RM."""
    def score(self, *, correct: bool, memory_relevant: bool, personalized: bool,
              proactive_accepted: bool | None, autonomy_violation: bool, sycophantic: bool = False) -> RewardVector:
        return RewardVector(
            helpfulness=1.0 if correct else 0.0,
            personalization=.95 if personalized else .5,
            truthfulness=1.0 if correct else .15,
            proactivity=.5 if proactive_accepted is None else (1.0 if proactive_accepted else 0.0),
            autonomy=0.0 if autonomy_violation else 1.0,
            memory_use=.95 if memory_relevant else .5,
            sycophancy_penalty=1.0 if sycophantic else 0.0,
        )
