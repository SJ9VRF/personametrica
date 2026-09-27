from pathlib import Path
import json
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'paper/figures'; OUT.mkdir(parents=True,exist_ok=True)
# Component ablations
x=json.load(open(ROOT/'data/pbs_component_ablations.json'))
names=['full','no_recency','no_provenance_reliability','no_temporary_expiry','no_context_scope','no_evidence_aggregation']
labels=['Full PBS','No recency','No provenance','No expiry','No context','No aggregation']
vals=[x[n]['decision_utility'] for n in names]
fig,ax=plt.subplots(figsize=(7.4,3.5)); ax.bar(range(len(vals)),vals); ax.set_xticks(range(len(vals)),labels,rotation=25,ha='right'); ax.set_ylabel('Decision utility'); ax.set_ylim(0,0.85); ax.set_title('PBS component ablations (held-out seeds 10–19)'); fig.tight_layout(); fig.savefig(OUT/'pbs_component_ablations.png',dpi=180); plt.close(fig)
# stress grid plot: utility delta vs behavior noise split by temporary rate, average over distractor rate
s=json.load(open(ROOT/'data/belief_stress_grid.json'))['rows']
from collections import defaultdict
d=defaultdict(list)
for r in s: d[(r['behavior_noise_rate'],r['temporary_rate'])].append(r['utility_delta'])
fig,ax=plt.subplots(figsize=(6.8,3.5))
for t in sorted({r['temporary_rate'] for r in s}):
 xs=sorted({r['behavior_noise_rate'] for r in s}); ys=[sum(d[(b,t)])/len(d[(b,t)]) for b in xs]; ax.plot(xs,ys,marker='o',label=f'temporary={t:.2f}')
ax.axhline(0,linewidth=1); ax.set_xlabel('Behavioral evidence error rate'); ax.set_ylabel('PBS − time-aware utility'); ax.set_title('Stress grid averaged over distractor noise'); ax.legend(frameon=False,ncol=3,fontsize=8); fig.tight_layout(); fig.savefig(OUT/'belief_stress_grid.png',dpi=180); plt.close(fig)
