from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
import uuid


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class SourceType(str, Enum):
    EXPLICIT = "explicit"
    IMPLICIT = "implicit"
    INFERRED = "inferred"
    SYNTHETIC = "synthetic"


class MemoryStatus(str, Enum):
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    EXPIRED = "expired"
    DELETED = "deleted"


class ActionType(str, Enum):
    ACT = "act"
    ASK = "ask"
    SUGGEST = "suggest"
    REMIND = "remind"
    WAIT = "wait"
    NONE = "none"


@dataclass(slots=True)
class InteractionEvent:
    user_id: str
    user_message: str
    assistant_response: str = ""
    session_id: str = "default"
    timestamp: str = field(default_factory=utcnow)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    context: dict[str, Any] = field(default_factory=dict)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    outcomes: list[dict[str, Any]] = field(default_factory=list)
    explicit_feedback: list[dict[str, Any]] = field(default_factory=list)
    implicit_feedback: list[dict[str, Any]] = field(default_factory=list)
    detected_goals: list[str] = field(default_factory=list)
    detected_preferences: list[str] = field(default_factory=list)
    uncertainty: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class MemoryRecord:
    key: str
    value: Any
    content: str
    memory_type: str
    source: SourceType
    confidence: float
    user_id: str
    created_at: str = field(default_factory=utcnow)
    updated_at: str = field(default_factory=utcnow)
    valid_from: str | None = None
    valid_until: str | None = None
    stability: Literal["low", "medium", "high"] = "medium"
    context: dict[str, Any] = field(default_factory=dict)
    supersedes: str | None = None
    contradicted_by: list[str] = field(default_factory=list)
    status: MemoryStatus = MemoryStatus.ACTIVE
    memory_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["source"] = self.source.value
        d["status"] = self.status.value
        return d


@dataclass(slots=True)
class Goal:
    description: str
    user_id: str
    priority: float = 0.5
    deadline: str | None = None
    status: str = "active"
    confidence: float = 1.0
    parent_goal_id: str | None = None
    subtasks: list[str] = field(default_factory=list)
    progress: float = 0.0
    blockers: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    goal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class UserBelief:
    key: str
    value: Any
    confidence: float
    source: SourceType
    last_updated: str = field(default_factory=utcnow)
    context: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class UserState:
    user_id: str
    beliefs: dict[str, UserBelief] = field(default_factory=dict)
    goals: dict[str, Goal] = field(default_factory=dict)
    autonomy_preference: float = 0.5
    interaction_style: dict[str, float] = field(default_factory=lambda: {
        "verbosity": 0.5,
        "directness": 0.5,
        "warmth": 0.5,
        "initiative": 0.5,
    })


@dataclass(slots=True)
class ProactivityDecision:
    action: ActionType
    score: float
    confidence: float
    factors: dict[str, float]
    rationale: list[str]


@dataclass(slots=True)
class PlanStep:
    objective: str
    action: str
    tool: str | None = None
    required_context: dict[str, Any] = field(default_factory=dict)
    success_condition: str = ""
    failure_condition: str = ""
    fallback: str | None = None
    step_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass(slots=True)
class ToolResult:
    tool: str
    action: str
    success: bool
    payload: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass(slots=True)
class VerificationResult:
    success: bool
    expected: dict[str, Any]
    observed: dict[str, Any]
    discrepancies: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FeedbackSignal:
    category: str
    value: float
    source: SourceType
    comment: str = ""
    event_id: str | None = None


@dataclass(slots=True)
class RewardVector:
    helpfulness: float
    personalization: float
    truthfulness: float
    proactivity: float
    autonomy: float
    memory_use: float
    sycophancy_penalty: float = 0.0

    def weighted(self, weights: dict[str, float] | None = None) -> float:
        w = weights or {
            "helpfulness": .2, "personalization": .2, "truthfulness": .2,
            "proactivity": .12, "autonomy": .12, "memory_use": .1,
            "sycophancy_penalty": .06,
        }
        d = asdict(self)
        return sum(w.get(k, 0.0) * (-v if k == "sycophancy_penalty" else v) for k, v in d.items())


@dataclass(slots=True)
class AuditEvent:
    event_type: str
    user_id: str
    subject_id: str | None = None
    key: str | None = None
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utcnow)
    audit_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
