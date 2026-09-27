from personalagi.agent.core import PersonalAGIAgent
import json

agent=PersonalAGIAgent("demo-user")
sequence=[
    "I prefer concise answers.",
    "My goal is prepare my conference talk by Friday.",
    "I prefer working in the evening.",
    "Keep me on track, but don't nag me.",
    "Actually, mornings work better for me now.",
]
for msg in sequence:
    result=agent.observe(msg)
    print(f"USER: {msg}")
    if result["new_memories"]:
        print("  memory:",[(m.key,m.value) for m in result["new_memories"]])
    if result["event"].detected_goals:
        print("  goal captured")

d=agent.proactive_decision(goal_relevance=.95,urgency=.9,confidence=.91,stakes=.2,reversibility=.95,interruptibility=.8)
print("\nPROACTIVITY:",d.action.value,"score=",round(d.score,3))
print("WHY:","; ".join(d.rationale))
print("\nCURRENT STATE")
print(json.dumps(agent.explain_state(),indent=2,default=str))
