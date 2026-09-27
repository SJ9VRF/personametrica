from __future__ import annotations
from collections import defaultdict
from personalagi.schemas import FeedbackSignal, SourceType


class FeedbackEngine:
    VALID = {"useful", "wrong_fact", "wrong_memory", "wrong_assumption", "too_proactive", "not_proactive_enough", "wrong_tone", "outdated_preference"}
    def __init__(self):
        self.signals: list[FeedbackSignal] = []
        self.by_category = defaultdict(list)

    def add(self, category: str, value: float, *, source: SourceType = SourceType.EXPLICIT, comment: str = "", event_id: str | None = None):
        if category not in self.VALID:
            raise ValueError(f"unknown feedback category: {category}")
        s = FeedbackSignal(category, max(-1.0, min(1.0, value)), source, comment, event_id)
        self.signals.append(s); self.by_category[category].append(s)
        return s

    def acceptance_rate(self) -> float:
        useful = self.by_category.get("useful", [])
        return .5 if not useful else sum(1 for s in useful if s.value > 0) / len(useful)
