from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass(slots=True)
class AgentEvalTask:
    task_id: str
    category: str
    expected_state: dict[str, Any]
    confirmation_required: bool = False
    verification_required: bool = True
    allowed_tools: tuple[str, ...] = ('reminders',)
    allowed_actions: tuple[str, ...] = ('create',)
    max_tool_calls: int = 2
    description: str = ''

    def to_dict(self): return asdict(self)

@dataclass(slots=True)
class AgentTrial:
    task_id: str
    trial_id: str
    perturbation: str
    events: list[dict[str, Any]]
    final_state: dict[str, Any]
    claimed_success: bool
    gold_pass: bool
    gold_failure_reason: str | None = None

    def to_dict(self): return asdict(self)

@dataclass(slots=True)
class GraderResult:
    grader: str
    passed: bool
    score: float
    assertions: dict[str, bool] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    verdict: str | None = None
    abstained: bool = False
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self): return asdict(self)
