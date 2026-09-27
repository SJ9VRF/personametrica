from __future__ import annotations
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
import json, argparse
from pathlib import Path
from personalbench.simulator.users import generate_personas


def main():
    p=argparse.ArgumentParser(); p.add_argument('--users',type=int,default=100); p.add_argument('--turns',type=int,default=50); p.add_argument('--out',default='data/personalbench.jsonl'); a=p.parse_args()
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',encoding='utf-8') as f:
        for persona in generate_personas(a.users):
            for t in range(a.turns):
                msg=persona.utterance(t)
                f.write(json.dumps({'user_id':persona.user_id,'turn':t,'message':msg,'ground_truth':{'work_time':persona.work_time,'response_detail':persona.response_detail,'autonomy':persona.autonomy}},ensure_ascii=False)+'\n')
    print(out)
if __name__=='__main__': main()
