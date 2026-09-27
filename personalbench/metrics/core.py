from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass
class BenchmarkMetrics:
    personalization_accuracy: float
    stale_memory_rate: float
    contradiction_rate: float
    proactive_precision: float
    autonomy_violation_rate: float
    goal_capture_rate: float

    def to_dict(self): return asdict(self)


def safe_div(a: float, b: float) -> float:
    return a / b if b else 0.0
