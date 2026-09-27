from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig,generate_user_stream,TRACKERS

def curve_for(cls,streams):
    rows=[]
    for obs,qs in streams:
        tr=cls(); events=sorted([(o.turn,0,o) for o in obs]+[(q.turn,1,q) for q in qs],key=lambda x:(x[0],x[1]))
        for _,k,x in events:
            if k==0: tr.observe(x)
            else:
                p,c=tr.read(x); rows.append((float(c),int(p==x.expected)))
    rows.sort(reverse=True,key=lambda x:x[0]); n=len(rows); points=[]; risks=[]
    correct=0
    for i,(_,ok) in enumerate(rows,1):
        correct+=ok
        if i==n or i%max(1,n//100)==0:
            cov=i/n; risk=1-correct/i; points.append({'coverage':cov,'risk':risk});risks.append((cov,risk))
    # Trapezoidal area over observed risk-coverage curve, with risk=0 at zero coverage.
    area=0.0;pc=0.0;pr=0.0
    for c,r in risks:
        area+=(c-pc)*(r+pr)/2;pc,pr=c,r
    return {'aurc':area,'points':points,'full_accuracy':sum(ok for _,ok in rows)/n,'n':n}

cfg=BenchmarkConfig(users=500,turns=240,seed=31)
streams=[generate_user_stream(i,cfg) for i in range(cfg.users)]
out={cls.name:curve_for(cls,streams) for cls in TRACKERS}
(ROOT/'data'/'belief_risk_coverage.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
lines=['# Risk–Coverage Analysis','', 'Lower area under the risk–coverage curve (AURC) is better. Unlike a single action threshold, AURC evaluates confidence ordering across the full coverage range.','','| Method | Full accuracy | AURC ↓ |','|---|---:|---:|']
for k,v in out.items(): lines.append(f"| {k} | {v['full_accuracy']:.3f} | {v['aurc']:.3f} |")
(ROOT/'reports'/'BELIEF_RISK_COVERAGE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:{'accuracy':v['full_accuracy'],'aurc':v['aurc']} for k,v in out.items()},indent=2))
