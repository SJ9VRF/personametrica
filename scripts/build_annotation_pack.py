from __future__ import annotations
import json, random, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from personalbench.tasks.scenarios import generate_proactivity_scenarios
from personalbench.belief_benchmark import BenchmarkConfig, generate_user_stream
r=random.Random(17)
tasks=[]
for i,s in enumerate(generate_proactivity_scenarios(300,17)):
    tasks.append({
      'id':f'pro-{i:04d}','task_type':'proactivity',
      'scenario':{k:v for k,v in s.items() if k!='expected'},
      'label_space':['act','ask','suggest','remind','wait','none'],
      'reference_label':sorted(s['expected']),
      'annotation_prompt':'Choose the least intrusive action that still appropriately advances the user goal. Judge uncertainty, stakes, reversibility, urgency, and interruption cost.'
    })
for u in range(80):
    obs,qs=generate_user_stream(u,BenchmarkConfig(users=80,turns=160,seed=93,query_every=32))
    for j,q in enumerate(qs[:4]):
        relevant=[o for o in obs if o.slot==q.slot and o.turn<=q.turn]
        tasks.append({
          'id':f'belief-{u:03d}-{j}','task_type':'belief_update','slot':q.slot,'turn':q.turn,'context':q.context,
          'evidence':[{k:getattr(o,k) for k in o.__slots__} for o in relevant],
          'label_space':list(sorted({o.value for o in relevant})),
          'reference_label':q.expected,
          'annotation_prompt':'Given the evidence available up to this turn, choose the user preference that should be treated as current. Ignore hypothetical or other-person evidence and respect temporary scope.'
        })
r.shuffle(tasks)
path=ROOT/'annotation'/'tasks.json'
path.write_text(json.dumps({'version':'1.0','tasks':tasks},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(tasks)} tasks -> {path}')
