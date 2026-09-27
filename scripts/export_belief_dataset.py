from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig, generate_user_stream, DOMAINS
cfg=BenchmarkConfig(users=500,turns=240,seed=31)
out=ROOT/'data'/'personalbench_x.jsonl'
with out.open('w',encoding='utf-8') as f:
    for i in range(cfg.users):
        obs,qs=generate_user_stream(i,cfg)
        row={
          'user_id':(obs[0].user_id if obs else qs[0].user_id), 'turns':cfg.turns,
          'observations':[o.__dict__ if hasattr(o,'__dict__') else {k:getattr(o,k) for k in o.__slots__} for o in obs],
          'queries':[q.__dict__ if hasattr(q,'__dict__') else {k:getattr(q,k) for k in q.__slots__} for q in qs],
        }
        f.write(json.dumps(row,ensure_ascii=False)+'\n')
print(out)
