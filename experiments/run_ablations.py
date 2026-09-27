from __future__ import annotations
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
import json
from pathlib import Path
from personalbench.runner import run_detailed_comparison


def main():
    result=run_detailed_comparison(100,60,7)
    rows=[]
    for name,s in result['systems'].items():
        rows.append({'name':name,'config':s['config'],'metrics':s['metrics'],'confidence_intervals_95':s['confidence_intervals_95']})
    Path('data').mkdir(exist_ok=True); Path('data/ablation_results.json').write_text(json.dumps(rows,indent=2))
    print(json.dumps(rows,indent=2))
if __name__=='__main__': main()
