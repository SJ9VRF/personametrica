from __future__ import annotations
import json
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'paper'/'figures';OUT.mkdir(parents=True,exist_ok=True)

# Figure 1: accuracy vs decision utility under standard benchmark.
d=json.loads((ROOT/'data'/'belief_benchmark_results.json').read_text())['standard']['results']
names=list(d); x=[d[n]['accuracy'] for n in names]; y=[d[n]['decision_utility'] for n in names]
fig,ax=plt.subplots(figsize=(7.2,4.8)); ax.scatter(x,y,s=55)
for n,a,b in zip(names,x,y): ax.annotate(n.replace('-',' '),(a,b),xytext=(5,5),textcoords='offset points',fontsize=8)
ax.set_xlabel('Raw state accuracy');ax.set_ylabel('Decision utility');ax.set_title('Accuracy and action-level utility can rank systems differently');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'accuracy_vs_utility.png',dpi=180);plt.close(fig)

# Figure 2: risk coverage trusted vs PBS.
r=json.loads((ROOT/'data'/'belief_risk_coverage.json').read_text())
fig,ax=plt.subplots(figsize=(7.2,4.8))
for n in ['trusted-latest','personal-belief-state']:
    pts=r[n]['points'];ax.plot([p['coverage'] for p in pts],[p['risk'] for p in pts],label=f"{n} (AURC={r[n]['aurc']:.3f})")
ax.set_xlabel('Coverage');ax.set_ylabel('Risk (1 − selective accuracy)');ax.set_title('Risk–coverage: confidence quality beyond state accuracy');ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'risk_coverage.png',dpi=180);plt.close(fig)

# Figure 3: utility by shift.
allr=json.loads((ROOT/'data'/'belief_benchmark_results.json').read_text())
splits=list(allr); p=[allr[s]['results']['personal-belief-state']['decision_utility'] for s in splits]; t=[allr[s]['results']['trusted-latest']['decision_utility'] for s in splits]
import numpy as np
idx=np.arange(len(splits));w=.35
fig,ax=plt.subplots(figsize=(8,4.8));ax.bar(idx-w/2,p,w,label='PBS');ax.bar(idx+w/2,t,w,label='trusted-latest');ax.set_xticks(idx,[s.replace('_','\n') for s in splits]);ax.set_ylabel('Decision utility');ax.set_title('Decision utility under controlled distribution shifts');ax.legend();ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(OUT/'distribution_shifts.png',dpi=180);plt.close(fig)
print('wrote paper figures')
