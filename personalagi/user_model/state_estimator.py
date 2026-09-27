from __future__ import annotations
import re
from personalagi.schemas import InteractionEvent, MemoryRecord, SourceType, UserState, UserBelief


class TemporalStateEstimator:
    """Transparent local estimator supporting conditional preferences and preference reversal."""

    def infer(self, event: InteractionEvent, state: UserState) -> tuple[list[MemoryRecord], list[str]]:
        text = event.user_message.strip()
        lower = text.lower()
        memories: list[MemoryRecord] = []
        goals: list[str] = []

        gm = re.search(r"\b(?:my goal is|i want to|i need to)\s+(.+?)(?:[.!]|$)", text, re.I)
        if gm:
            goals.append(gm.group(1).strip())

        pref = self._extract_preference(text)
        if pref:
            key, value, stability, confidence, context = pref
            # Carry conversational domain forward for elliptical updates such as
            # "That changed; I prefer mornings now" after a work-time preference.
            if key == "preference.time_of_day" and "preference.work_time" in state.beliefs:
                key = "preference.work_time"
                context = {"domain": "work_schedule", "inherited_context": True}
            record = MemoryRecord(
                key=key, value=value, content=text, memory_type="preference",
                source=SourceType.EXPLICIT, confidence=confidence, user_id=event.user_id,
                stability=stability, context=context, valid_from=event.timestamp,
            )
            memories.append(record)
            state.beliefs[key] = UserBelief(key=key, value=value, confidence=confidence,
                                            source=SourceType.EXPLICIT, last_updated=event.timestamp,
                                            context=context)

        # Autonomy preference is itself personalized.
        if "don't nag" in lower or "do not nag" in lower or "ask me first" in lower:
            state.autonomy_preference = max(0.0, state.autonomy_preference - 0.2)
        if "be proactive" in lower or "keep me on track" in lower or "remind me" in lower:
            state.autonomy_preference = min(1.0, state.autonomy_preference + 0.15)
        if "concise" in lower or "short answers" in lower:
            state.interaction_style["verbosity"] = 0.2
        if "detailed" in lower or "more detail" in lower:
            state.interaction_style["verbosity"] = 0.8
        return memories, goals

    def _extract_preference(self, text: str):
        lower = text.lower().strip()

        # Resolve explicit within-utterance temporal reversals by privileging the
        # clause marked as current ("now", "actually", "changed").
        current = lower
        if " but now " in lower:
            current = lower.split(" but now ", 1)[1]
        elif ";" in lower and " now" in lower:
            current = lower.split(";", 1)[1]
        elif "that changed" in lower:
            current = lower.split("that changed", 1)[1]

        def time_value(segment: str):
            if "morning" in segment:
                return "morning"
            if "evening" in segment:
                return "evening"
            if "night" in segment:
                return "night"
            return None

        tv = time_value(current)
        time_signal = re.search(r"\b(?:prefer(?:red)?|works? (?:better|best)|work(?:ing)? .* (?:in|at)|usually .*work|maybe .*prefer|better now)\b", current)
        if tv and time_signal:
            context = {'domain': 'work_schedule'} if any(x in lower for x in ['work', 'talk', 'focus']) else {}
            key = 'preference.work_time' if context else 'preference.time_of_day'
            confidence = .60 if 'maybe' in lower else (.78 if 'usually' in lower else .97)
            stability = 'low' if confidence < .7 else 'medium'
            return key, tv, stability, confidence, context

        # Conditional detail takes precedence over the general communication slot.
        if "technical" in lower and ("detailed" in lower or "more detail" in lower):
            return "preference.response_detail.technical", "detailed", "medium", .97, {"domain": "technical"}
        if "concise" in lower or "short answers" in lower or "keep answers short" in lower:
            return "preference.response_detail", "concise", "high", .99, {"domain": "communication"}
        if "detailed" in lower or "more detail" in lower:
            return "preference.response_detail", "detailed", "medium", .97, {"domain": "communication"}

        m = re.search(r"\bi (?:really )?(?:prefer|like)\s+(.+?)(?:[.!]|$)", text, re.I)
        if m:
            raw = m.group(1).strip()
            key = "preference.general." + re.sub(r"[^a-z0-9]+", "_", raw.lower()).strip("_")[:32]
            return key, raw, "medium", .92, {}
        m = re.search(r"\bi (?:don't|do not) like\s+(.+?)(?:[.!]|$)", text, re.I)
        if m:
            raw = m.group(1).strip()
            key = "preference.dislike." + re.sub(r"[^a-z0-9]+", "_", raw.lower()).strip("_")[:32]
            return key, raw, "medium", .96, {}
        return None



# Backward compatible name.
RuleBasedStateEstimator = TemporalStateEstimator
