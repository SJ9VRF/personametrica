from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

MemoryUpdatePolicy = Literal['latest', 'first', 'all']

@dataclass(slots=True)
class AgentConfig:
    memory_enabled: bool = True
    memory_update_policy: MemoryUpdatePolicy = 'latest'
    contradiction_resolution: bool = True
    confidence_tracking: bool = True
    goal_model: bool = True
    calibrated_proactivity: bool = True
    outcome_verification: bool = True
    privacy_guard: bool = True

    @classmethod
    def full(cls) -> 'AgentConfig':
        return cls()
