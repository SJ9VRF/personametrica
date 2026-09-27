from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol
from personalagi.schemas import InteractionEvent, MemoryRecord, UserState

@dataclass
class InferenceBundle:
    memories: list[MemoryRecord] = field(default_factory=list)
    goals: list[str] = field(default_factory=list)

class InferenceAdapter(Protocol):
    """Boundary between the agent runtime and a learned/heuristic inference component.

    A production model adapter only needs to implement this contract. The rest of the
    OS (privacy, memory reconciliation, goals, evals, persistence) remains unchanged.
    """
    name: str
    def infer(self, event: InteractionEvent, state: UserState) -> InferenceBundle: ...
