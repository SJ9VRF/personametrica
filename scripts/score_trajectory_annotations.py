from __future__ import annotations
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(); parser.add_argument('responses',nargs='+'); args=parser.parse_args()
queue={r['review_id']:r for r in (json.loads(x) for x in (ROOT/'data'/'grader_disagreement_queue.jsonl').read_text().splitlines() if x.strip())}
by=defaultdict(list)
for path in args.responses:
    data=json.loads(Path(path).read_text())
    for r in data: by[r['review_id']].append(r['verdict'])
rows=[]; correct=0; known=0
cats=('pass','fail','unknown')
for rid,vals in by.items():
    majority=Counter(vals).most_common(1)[0][0]; gold='pass' if queue[rid]['gold_pass'] else 'fail'
    if majority!='unknown': known+=1; correct+=int(majority==gold)
    rows.append({'review_id':rid,'n':len(vals),'majority':majority,'gold':gold,'agreement':Counter(vals).most_common(1)[0][1]/len(vals),'counts':{c:vals.count(c) for c in cats}})
# Fleiss' kappa when every item has the same number of >=2 ratings.
kappa=None
if rows and len({r['n'] for r in rows})==1 and rows[0]['n']>=2:
    n=rows[0]['n']; N=len(rows)
    P_i=[]
    totals={c:0 for c in cats}
    for r in rows:
        P_i.append((sum(v*v for v in r['counts'].values())-n)/(n*(n-1)))
        for c,v in r['counts'].items(): totals[c]+=v
    Pbar=sum(P_i)/N; p={c:totals[c]/(N*n) for c in cats}; Pe=sum(x*x for x in p.values())
    kappa=(Pbar-Pe)/(1-Pe) if Pe<1 else 1.0
out={'items':len(rows),'known_items':known,'majority_accuracy_on_known':correct/max(1,known),'mean_raw_agreement':sum(r['agreement'] for r in rows)/max(1,len(rows)),'fleiss_kappa':kappa,'rows':rows}
print(json.dumps(out,indent=2))
