from __future__ import annotations
import argparse,json,math
from pathlib import Path

def ece(rows,bins=10):
    out=0.0;n=len(rows)
    for b in range(bins):
        lo,hi=b/bins,(b+1)/bins
        xs=[r for r in rows if lo <= r['confidence'] < hi or (b==bins-1 and r['confidence']==1)]
        if xs:
            acc=sum(r['correct'] for r in xs)/len(xs); conf=sum(r['confidence'] for r in xs)/len(xs)
            out += len(xs)/n*abs(acc-conf)
    return out

def main():
    ap=argparse.ArgumentParser(description='Evaluate structured outputs from an external model without coupling the benchmark to a vendor API.')
    ap.add_argument('jsonl'); ap.add_argument('--out',default='data/external_model_results.json'); args=ap.parse_args()
    rows=[]
    for line in Path(args.jsonl).read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        x=json.loads(line); expected=x['expected']; pred=x.get('prediction'); conf=float(x.get('confidence',1.0))
        if not 0<=conf<=1: raise ValueError('confidence must be [0,1]')
        rows.append({'correct':int(pred==expected),'confidence':conf})
    n=len(rows); acc=sum(r['correct'] for r in rows)/max(1,n); brier=sum((r['confidence']-r['correct'])**2 for r in rows)/max(1,n)
    result={'n':n,'accuracy':acc,'brier':brier,'ece':ece(rows) if rows else 0.0}
    Path(args.out).write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps(result,indent=2))
if __name__=='__main__': main()
