from __future__ import annotations
import json, math, sys
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig, generate_user_stream, Query, Observation
from personalagi.user_model.probabilistic_belief import SOURCE_RELIABILITY

class AblatedPBS:
    def __init__(self, *, recency=True, provenance=True, temporary=True, context=True, aggregate=True, half_life=90.0, temperature=.20):
        self.rows=[]; self.recency=recency; self.provenance=provenance; self.temporary=temporary; self.context=context; self.aggregate=aggregate; self.half_life=half_life; self.temperature=temperature
    def observe(self,o): self.rows.append(o)
    def _w(self,o,q):
        rel=SOURCE_RELIABILITY.get(o.source,1.0) if self.provenance else 1.0
        age=max(0,q.turn-o.turn)
        rec=math.exp(-math.log(2)*age/self.half_life) if self.recency else 1.0
        cf=1.0
        if self.context and o.context is not None: cf=1.0 if o.context==q.context else .18
        valid=1.0
        if self.temporary and o.temporary_until is not None and q.turn>o.temporary_until: valid=.08
        return rel*o.confidence*rec*cf*valid
    def read(self,q):
        rows=[o for o in self.rows if o.slot==q.slot and o.turn<=q.turn]
        if not rows: return None,0.0
        if not self.aggregate:
            o=max(rows,key=lambda o:o.turn)
            return o.value,min(1.0,self._w(o,q))
        scores=defaultdict(float)
        for o in rows: scores[o.value]+=self._w(o,q)
        vals=list(scores)
        m=max(scores.values()); ex={v:math.exp((scores[v]-m)/self.temperature) for v in vals}; z=sum(ex.values())
        probs={v:ex[v]/z for v in vals}; best=max(probs,key=probs.get)
        return best,probs[best]

def evaluate(factory, streams, threshold=.70, defer=.10):
    total=correct=acted=acted_correct=asks=0; brier=0.0
    for obs,qs in streams:
        t=factory(); events=sorted([(o.turn,0,o) for o in obs]+[(q.turn,1,q) for q in qs],key=lambda x:(x[0],x[1]))
        for _,k,x in events:
            if k==0: t.observe(x); continue
            p,c=t.read(x); ok=p==x.expected; total+=1; correct+=ok; brier+=(c-float(ok))**2
            if p is None or c<threshold: asks+=1
            else: acted+=1; acted_correct+=ok
    return {
      'accuracy':correct/total,'coverage':acted/total,'selective_accuracy':acted_correct/max(1,acted),
      'decision_utility':(acted_correct-(acted-acted_correct)-defer*asks)/total,'brier':brier/total,'queries':total
    }

def main():
    seeds=range(10,20); variants={
      'full':{},'no_recency':{'recency':False},'no_provenance_reliability':{'provenance':False},
      'no_temporary_expiry':{'temporary':False},'no_context_scope':{'context':False},'no_evidence_aggregation':{'aggregate':False},
    }
    per={k:[] for k in variants}
    for seed in seeds:
        cfg=BenchmarkConfig(users=160,turns=240,seed=seed); streams=[generate_user_stream(i,cfg) for i in range(cfg.users)]
        for name,kw in variants.items(): per[name].append(evaluate(lambda kw=kw:AblatedPBS(**kw),streams))
    out={}
    for name,rows in per.items():
        out[name]={m:sum(r[m] for r in rows)/len(rows) for m in ['accuracy','coverage','selective_accuracy','decision_utility','brier']}
    base=out['full']; out['_deltas_vs_full']={n:{m:out[n][m]-base[m] for m in ['accuracy','decision_utility','brier']} for n in variants if n!='full'}
    (ROOT/'data/pbs_component_ablations.json').write_text(json.dumps(out,indent=2))
    lines=['# PBS component ablations','', 'Held-out seeds 10–19; 160 users × 240 turns per seed. Full PBS hyperparameters remain frozen from development tuning.','', '| Variant | State acc. | Coverage | Utility | Brier ↓ |','|---|---:|---:|---:|---:|']
    for n in variants:
        r=out[n]; lines.append(f"| {n} | {r['accuracy']:.3f} | {r['coverage']:.3f} | {r['decision_utility']:.3f} | {r['brier']:.3f} |")
    lines += ['', 'Interpretation: these ablations isolate which parts of PBS matter under the controlled generator. They do not establish causal importance for natural human conversations.']
    (ROOT/'reports/PBS_COMPONENT_ABLATIONS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
