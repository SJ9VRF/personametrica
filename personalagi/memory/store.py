from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone
from math import exp
import re
from personalagi.schemas import MemoryRecord, MemoryStatus, AuditEvent


def _parse(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace('Z', '+00:00'))


class InMemoryMemoryStore:
    """Temporal/confidence-aware memory store with configurable update semantics."""

    def __init__(self, *, update_policy: str = 'latest', contradiction_resolution: bool = True) -> None:
        if update_policy not in {'latest', 'first', 'all'}:
            raise ValueError('update_policy must be latest, first, or all')
        self.update_policy = update_policy
        self.contradiction_resolution = contradiction_resolution
        self._records: dict[str, MemoryRecord] = {}
        self._by_user: dict[str, list[str]] = defaultdict(list)
        self.audit_log: list[AuditEvent] = []

    def add(self, record: MemoryRecord) -> MemoryRecord:
        existing = [r for r in self.active(record.user_id) if r.key == record.key]
        if existing and self.update_policy == 'first':
            # Preserve provenance of the ignored update without making it active.
            record.status = MemoryStatus.SUPERSEDED
            record.supersedes = existing[-1].memory_id
        elif existing and self.update_policy == 'latest' and self.contradiction_resolution:
            for old in existing:
                old.status = MemoryStatus.SUPERSEDED
                old.contradicted_by.append(record.memory_id)
                old.updated_at = record.created_at
                record.supersedes = old.memory_id
        # 'all' or contradiction_resolution=False intentionally leaves conflicts active.
        self._records[record.memory_id] = record
        self._by_user[record.user_id].append(record.memory_id)
        self.audit_log.append(AuditEvent('memory_write', record.user_id, record.memory_id, record.key, metadata={'status': record.status.value, 'source': record.source.value}))
        if record.supersedes:
            self.audit_log.append(AuditEvent('memory_supersede', record.user_id, record.memory_id, record.key, metadata={'supersedes': record.supersedes}))
        return record

    def active(self, user_id: str, now: str | None = None) -> list[MemoryRecord]:
        now_dt = _parse(now) or datetime.now(timezone.utc)
        out = []
        for mid in self._by_user.get(user_id, []):
            r = self._records[mid]
            if r.status != MemoryStatus.ACTIVE:
                continue
            until = _parse(r.valid_until)
            if until and until <= now_dt:
                r.status = MemoryStatus.EXPIRED
                self.audit_log.append(AuditEvent('memory_expire', r.user_id, r.memory_id, r.key))
                continue
            out.append(r)
        return out

    def history(self, user_id: str) -> list[MemoryRecord]:
        return [self._records[mid] for mid in self._by_user.get(user_id, [])]

    def get_by_key(self, user_id: str, key: str) -> MemoryRecord | None:
        matches = [m for m in self.active(user_id) if m.key == key]
        return matches[-1] if matches else None

    def conflicts(self, user_id: str) -> dict[str, list[MemoryRecord]]:
        by_key: dict[str, list[MemoryRecord]] = defaultdict(list)
        for r in self.active(user_id):
            by_key[r.key].append(r)
        return {k: rs for k, rs in by_key.items() if len({str(r.value) for r in rs}) > 1}

    def forget(self, user_id: str, key: str) -> bool:
        record = self.get_by_key(user_id, key)
        if not record:
            return False
        record.status = MemoryStatus.DELETED
        self.audit_log.append(AuditEvent('memory_forget', user_id, record.memory_id, key, reason='explicit user control'))
        return True

    def retrieve(self, user_id: str, query: str, *, top_k: int = 5, now: str | None = None) -> list[tuple[MemoryRecord, float]]:
        q = set(re.findall(r'[a-z0-9]+', query.lower()))
        now_dt = _parse(now) or datetime.now(timezone.utc)
        ranked: list[tuple[MemoryRecord, float]] = []
        for r in self.active(user_id, now=now_dt.isoformat()):
            toks = set(re.findall(r'[a-z0-9]+', f'{r.key} {r.value} {r.content}'.lower()))
            relevance = len(q & toks) / max(1, len(q))
            created = _parse(r.updated_at) or now_dt
            days = max(0.0, (now_dt - created).total_seconds() / 86400)
            half_life = {'low': 7, 'medium': 30, 'high': 180}[r.stability]
            recency = exp(-0.693 * days / half_life)
            contradiction_risk = 0.25 if r.contradicted_by else 0.0
            score = .45 * relevance + .25 * recency + .30 * r.confidence - contradiction_risk
            ranked.append((r, max(0.0, min(1.0, score))))
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def decay_confidence(self, user_id: str, *, now: str | None = None, floor: float = 0.2) -> None:
        now_dt = _parse(now) or datetime.now(timezone.utc)
        for r in self.active(user_id, now=now_dt.isoformat()):
            created = _parse(r.updated_at) or now_dt
            days = max(0.0, (now_dt - created).total_seconds() / 86400)
            rate = {'low': 0.025, 'medium': 0.008, 'high': 0.001}[r.stability]
            r.confidence = max(floor, r.confidence * exp(-rate * days))
