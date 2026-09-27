from personalagi.memory.store import InMemoryMemoryStore
from personalagi.schemas import MemoryRecord, SourceType, MemoryStatus


def record(value: str):
    return MemoryRecord(
        key="preference.work_time",
        value=value,
        content=value,
        memory_type="preference",
        source=SourceType.EXPLICIT,
        confidence=0.99,
        user_id="u1",
    )


def test_new_memory_supersedes_old_same_key():
    store = InMemoryMemoryStore()
    first = store.add(record("evening"))
    second = store.add(record("morning"))
    assert first.status == MemoryStatus.SUPERSEDED
    assert second.status == MemoryStatus.ACTIVE
    assert second.supersedes == first.memory_id
    assert store.get_by_key("u1", "preference.work_time").value == "morning"
