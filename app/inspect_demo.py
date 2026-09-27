import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from personalagi.agent.core import PersonalAGIAgent
import json

agent=PersonalAGIAgent("demo")
for m in ["I prefer working in the evening.","I prefer concise answers.","My goal is prepare my conference talk by Friday.","Actually, mornings work better for me now."]:
    agent.observe(m)
print(json.dumps(agent.explain_state(),indent=2,default=str))
