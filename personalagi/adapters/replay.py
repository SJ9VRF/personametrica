from __future__ import annotations
from personalagi.adapters.base import InferenceBundle
from personalagi.schemas import MemoryRecord, SourceType, UserBelief

class ReplayInferenceAdapter:
    """Deterministic adapter for replaying structured outputs from any external model.

    This deliberately does not call a hosted API. It makes model-backed experiments
    reproducible: save model JSON once, then replay it through the exact same OS/evals.
    """
    name = "structured-replay-v1"
    def __init__(self, outputs: dict[str, dict]):
        self.outputs = outputs
    def infer(self, event, state) -> InferenceBundle:
        row = self.outputs.get(event.user_message, {})
        memories=[]
        for item in row.get("memories", []):
            required={"key","value"}
            if not required.issubset(item):
                raise ValueError("Replay memory requires key and value")
            confidence=float(item.get("confidence", .8))
            if not 0 <= confidence <= 1:
                raise ValueError("confidence must be in [0,1]")
            rec=MemoryRecord(key=item["key"], value=item["value"], content=event.user_message,
                memory_type=item.get("memory_type","preference"), source=SourceType(item.get("source","inferred")),
                confidence=confidence, user_id=event.user_id, stability=item.get("stability","medium"),
                context=item.get("context",{}), valid_from=event.timestamp)
            memories.append(rec)
            state.beliefs[rec.key]=UserBelief(key=rec.key,value=rec.value,confidence=confidence,
                source=rec.source,last_updated=event.timestamp,context=rec.context)
        goals=[str(g).strip() for g in row.get("goals",[]) if str(g).strip()]
        return InferenceBundle(memories=memories, goals=goals)
