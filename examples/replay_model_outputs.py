"""Replay structured outputs from an external learned model without a live API."""
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from personalagi.agent.core import PersonalAGIAgent
from personalagi.adapters import ReplayInferenceAdapter

outputs=json.loads(Path(__file__).with_name('model_outputs.json').read_text())
agent=PersonalAGIAgent('demo-user', inference_adapter=ReplayInferenceAdapter(outputs))
for message in outputs:
    agent.observe(message)
print(agent.explain_state())
