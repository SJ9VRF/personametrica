from __future__ import annotations
from dataclasses import dataclass, field, asdict
from math import exp, log
from typing import Any

SOURCE_RELIABILITY = {
    "explicit": 1.0,
    "implicit_choice": 0.72,
    "implicit_behavior": 0.58,
    "inferred": 0.45,
    "hypothetical": 0.05,
    "other_person": 0.02,
}

@dataclass(slots=True)
class PreferenceEvidence:
    slot: str
    value: str
    turn: int
    source: str = "explicit"
    confidence: float = 1.0
    context: str | None = None
    temporary_until: int | None = None
    negated: bool = False
    provenance: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(slots=True)
class BeliefCandidate:
    value: str
    probability: float
    score: float

@dataclass(slots=True)
class BeliefReadout:
    slot: str
    value: str | None
    confidence: float
    entropy: float
    evidence_count: int
    contradictory_values: int
    candidates: list[BeliefCandidate] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot": self.slot,
            "value": self.value,
            "confidence": self.confidence,
            "entropy": self.entropy,
            "evidence_count": self.evidence_count,
            "contradictory_values": self.contradictory_values,
            "candidates": [asdict(c) for c in self.candidates],
        }

class PersonalBeliefState:
    """Evidence-weighted temporal belief state for evolving preferences.

    This module deliberately separates *observations* from *beliefs*. Evidence can be
    explicit, implicit, hypothetical, about another person, or temporarily scoped. The
    state readout marginalizes evidence with source reliability, confidence, recency,
    and context compatibility instead of treating every utterance as an equally valid
    memory write.
    """

    def __init__(self, *, half_life_turns: float = 120.0, temperature: float = 0.55) -> None:
        if half_life_turns <= 0:
            raise ValueError("half_life_turns must be positive")
        if temperature <= 0:
            raise ValueError("temperature must be positive")
        self.half_life_turns = half_life_turns
        self.temperature = temperature
        self._evidence: dict[str, list[PreferenceEvidence]] = {}

    def update(self, evidence: PreferenceEvidence) -> None:
        if evidence.source not in SOURCE_RELIABILITY:
            raise ValueError(f"unknown evidence source: {evidence.source}")
        if not 0.0 <= evidence.confidence <= 1.0:
            raise ValueError("evidence confidence must be in [0,1]")
        self._evidence.setdefault(evidence.slot, []).append(evidence)

    def evidence(self, slot: str) -> list[PreferenceEvidence]:
        return list(self._evidence.get(slot, []))

    def _weight(self, ev: PreferenceEvidence, *, turn: int, context: str | None) -> float:
        # Evidence about another person or a hypothetical should almost never become a
        # persistent belief, but is kept in provenance for auditability.
        rel = SOURCE_RELIABILITY[ev.source]
        age = max(0, turn - ev.turn)
        recency = exp(-0.69314718056 * age / self.half_life_turns)
        context_factor = 1.0
        if ev.context is not None:
            context_factor = 1.0 if ev.context == context else 0.18
        # Temporary evidence is strong inside its validity window and sharply discounted
        # after expiry rather than deleting provenance.
        validity = 1.0
        if ev.temporary_until is not None and turn > ev.temporary_until:
            validity = 0.08
        sign = -1.0 if ev.negated else 1.0
        return sign * rel * ev.confidence * recency * context_factor * validity

    def read(self, slot: str, *, turn: int, context: str | None = None) -> BeliefReadout:
        rows = self._evidence.get(slot, [])
        if not rows:
            return BeliefReadout(slot, None, 0.0, 0.0, 0, 0, [])
        scores: dict[str, float] = {}
        for ev in rows:
            scores[ev.value] = scores.get(ev.value, 0.0) + self._weight(ev, turn=turn, context=context)
        if not scores:
            return BeliefReadout(slot, None, 0.0, 0.0, len(rows), 0, [])
        mx = max(scores.values())
        exps = {k: exp((v - mx) / self.temperature) for k, v in scores.items()}
        z = sum(exps.values()) or 1.0
        probs = {k: v / z for k, v in exps.items()}
        ranked = sorted(probs, key=probs.get, reverse=True)
        best = ranked[0]
        entropy = -sum(p * log(max(p, 1e-12)) for p in probs.values())
        candidates = [BeliefCandidate(v, probs[v], scores[v]) for v in ranked]
        return BeliefReadout(
            slot=slot,
            value=best,
            confidence=probs[best],
            entropy=entropy,
            evidence_count=len(rows),
            contradictory_values=max(0, len(scores)-1),
            candidates=candidates,
        )

    def snapshot(self, *, turn: int, context_by_slot: dict[str, str] | None = None) -> dict[str, dict[str, Any]]:
        context_by_slot = context_by_slot or {}
        return {slot: self.read(slot, turn=turn, context=context_by_slot.get(slot)).to_dict()
                for slot in sorted(self._evidence)}
