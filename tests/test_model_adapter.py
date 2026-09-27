import pytest
from personalagi.agent.core import PersonalAGIAgent
from personalagi.adapters import ReplayInferenceAdapter

def test_replay_adapter_plugs_into_agent_runtime():
    msg='I have a model-produced preference.'
    adapter=ReplayInferenceAdapter({msg:{'memories':[{'key':'preference.work_time','value':'morning','confidence':.88}]}})
    a=PersonalAGIAgent('u', inference_adapter=adapter)
    a.observe(msg)
    m=a.memory.get_by_key('u','preference.work_time')
    assert m and m.value=='morning' and abs(m.confidence-.88)<1e-9

def test_replay_adapter_validates_confidence():
    msg='bad'
    adapter=ReplayInferenceAdapter({msg:{'memories':[{'key':'x','value':'y','confidence':2.0}]}})
    with pytest.raises(ValueError):
        PersonalAGIAgent('u', inference_adapter=adapter).observe(msg)
