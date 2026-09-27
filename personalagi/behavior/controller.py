from __future__ import annotations
from dataclasses import dataclass
from personalagi.schemas import UserState


@dataclass(slots=True)
class BehaviorProfile:
    verbosity: float
    directness: float
    warmth: float
    initiative: float


class BehaviorController:
    def profile(self, state: UserState) -> BehaviorProfile:
        s = state.interaction_style
        return BehaviorProfile(s["verbosity"], s["directness"], s["warmth"], s["initiative"])

    def constraints(self) -> list[str]:
        return [
            "Personalization must not override factuality.",
            "Agreement is not a personalization objective.",
            "Consequential irreversible actions require confirmation.",
        ]
