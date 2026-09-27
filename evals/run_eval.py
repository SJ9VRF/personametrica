from __future__ import annotations
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
import json, argparse
from pathlib import Path
from personalbench import run_detailed_comparison

def main():
    p=argparse.ArgumentParser(); p.add_argument('--users',type=int,default=100); p.add_argument('--turns',type=int,default=60); p.add_argument('--seed',type=int,default=7); p.add_argument('--out',default='data/eval_results.json')
    a=p.parse_args(); m=run_detailed_comparison(a.users,a.turns,a.seed)
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(m,indent=2)); print(json.dumps(m,indent=2))
if __name__=='__main__': main()
