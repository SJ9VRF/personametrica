from datetime import datetime, timedelta, timezone
import pytest
from personalagi.memory import InMemoryMemoryStore
from personalagi.proactivity import CalibratedProactivityPolicy
from personalagi.schemas import MemoryRecord, SourceType


def test_expired_memory_is_not_active():
    store=InMemoryMemoryStore()
    now=datetime.now(timezone.utc)
    rec=MemoryRecord(key='preference.temp',value='quiet',content='quiet today',memory_type='preference',source=SourceType.EXPLICIT,confidence=.9,user_id='u',valid_until=(now-timedelta(seconds=1)).isoformat())
    store.add(rec)
    assert store.active('u', now=now.isoformat()) == []


def test_retrieval_prefers_relevant_memory():
    store=InMemoryMemoryStore()
    store.add(MemoryRecord(key='preference.food',value='sushi',content='I like sushi',memory_type='preference',source=SourceType.EXPLICIT,confidence=.9,user_id='u'))
    store.add(MemoryRecord(key='preference.work_time',value='morning',content='I work best in the morning',memory_type='preference',source=SourceType.EXPLICIT,confidence=.9,user_id='u'))
    ranked=store.retrieve('u','When should I work in the morning?',top_k=2)
    assert ranked[0][0].key == 'preference.work_time'


def test_proactivity_rejects_out_of_range_features():
    policy=CalibratedProactivityPolicy()
    with pytest.raises(ValueError):
        policy.decide(goal_relevance=1.2,urgency=.5,confidence=.5,stakes=.5,reversibility=.5,autonomy_preference=.5)
