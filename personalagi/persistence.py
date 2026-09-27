from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from personalagi.schemas import MemoryRecord, MemoryStatus, SourceType, Goal, UserBelief, AuditEvent, InteractionEvent, FeedbackSignal

SCHEMA_VERSION = 2


def dump_agent(agent, path: str | Path) -> Path:
    p = Path(path)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "user_state": {
            "user_id": agent.state.user_id,
            "autonomy_preference": agent.state.autonomy_preference,
            "interaction_style": agent.state.interaction_style,
            "beliefs": {
                k: {
                    "key": b.key,
                    "value": b.value,
                    "confidence": b.confidence,
                    "source": b.source.value,
                    "last_updated": b.last_updated,
                    "context": b.context,
                }
                for k, b in agent.state.beliefs.items()
            },
            "goals": {k: g.to_dict() for k, g in agent.state.goals.items()},
        },
        "memory_history": [m.to_dict() for m in agent.memory.history(agent.state.user_id)],
        "events": [e.to_dict() for e in agent.events],
        "memory_audit": [a.to_dict() for a in agent.memory.audit_log],
        "feedback": [
            {"category": f.category, "value": f.value, "source": f.source.value, "comment": f.comment, "event_id": f.event_id}
            for f in agent.feedback.signals
        ],
        "tool_state": agent.tools.snapshot(),
    }
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return p


def load_agent(agent, path: str | Path):
    p = Path(path)
    payload = json.loads(p.read_text(encoding="utf-8"))
    version = payload.get("schema_version")
    if version not in {1, SCHEMA_VERSION}:
        raise ValueError(f"unsupported snapshot schema: {version}")
    us = payload["user_state"]
    if us["user_id"] != agent.state.user_id:
        raise ValueError("snapshot user_id does not match agent user_id")

    agent.state.autonomy_preference = float(us.get("autonomy_preference", 0.5))
    agent.state.interaction_style = dict(us.get("interaction_style", {}))
    agent.state.beliefs.clear()
    for k, row in us.get("beliefs", {}).items():
        agent.state.beliefs[k] = UserBelief(
            key=row["key"], value=row.get("value"), confidence=float(row["confidence"]),
            source=SourceType(row["source"]), last_updated=row["last_updated"],
            context=dict(row.get("context", {})),
        )
    agent.state.goals.clear()
    for gid, row in us.get("goals", {}).items():
        agent.state.goals[gid] = Goal(**row)

    # Rebuild the store preserving full temporal history/status exactly.
    agent.memory._records.clear()
    agent.memory._by_user.clear()
    agent.memory.audit_log.clear()
    for row in payload.get("memory_history", []):
        row = dict(row)
        row["source"] = SourceType(row["source"])
        row["status"] = MemoryStatus(row["status"])
        rec = MemoryRecord(**row)
        agent.memory._records[rec.memory_id] = rec
        agent.memory._by_user[rec.user_id].append(rec.memory_id)
    for row in payload.get("memory_audit", []):
        agent.memory.audit_log.append(AuditEvent(**row))

    agent.events.clear()
    for row in payload.get("events", []):
        agent.events.append(InteractionEvent(**row))

    agent.feedback.signals.clear(); agent.feedback.by_category.clear()
    for row in payload.get("feedback", []):
        agent.feedback.add(
            row["category"], float(row["value"]), source=SourceType(row["source"]),
            comment=row.get("comment", ""), event_id=row.get("event_id")
        )
    if "tool_state" in payload:
        agent.tools.restore(payload["tool_state"])
    return agent
