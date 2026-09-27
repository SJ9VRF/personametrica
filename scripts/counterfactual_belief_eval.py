from __future__ import annotations
import copy, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig, generate_user_stream, TimeAwareLatestTracker, BeliefStateTracker, Observation, Query, _alternative

TRACKERS=(TimeAwareLatestTracker,BeliefStateTracker)

def state_before_query(obs,q): return [o for o in obs if o.turn<=q.turn]

def evaluate(n_users=180, seed=101):
    cfg=BenchmarkConfig(users=n_users,turns=240,seed=seed)
    cases=[]
    for i in range(n_users):
        obs,qs=generate_user_stream(i,cfg)
        for q in qs[-3:]:
            history=state_before_query(obs,q)
            alt=_alternative(q.slot,q.expected)
            cases.append((history,q,alt))
    results={}
    for cls in TRACKERS:
        counts={'n':0,'nuisance_invariant':0,'weak_conflict_invariant':0,'explicit_update_sensitive':0}
        examples=[]
        for history,q,alt in cases:
            def pred(extra=None):
                tr=cls()
                for o in history:
                    tr.observe(o)
                if extra: tr.observe(extra)
                return tr.read(q)[0]
            base=pred()
            nuisance=Observation(q.user_id,q.turn,q.slot,alt,'other_person',.99,provenance='counterfactual-nuisance')
            weak=Observation(q.user_id,q.turn,q.slot,alt,'implicit_behavior',.35,provenance='counterfactual-weak-conflict')
            explicit=Observation(q.user_id,q.turn,q.slot,alt,'explicit',1.0,provenance='counterfactual-explicit-update')
            pn=pred(nuisance); pw=pred(weak); pe=pred(explicit)
            counts['n']+=1
            counts['nuisance_invariant']+=int(pn==base)
            counts['weak_conflict_invariant']+=int(pw==base)
            counts['explicit_update_sensitive']+=int(pe==alt)
            if len(examples)<6 and (pe!=alt or pw!=base):
                examples.append({'slot':q.slot,'base':base,'expected':q.expected,'alternative':alt,'nuisance':pn,'weak':pw,'explicit':pe})
        n=counts['n']
        results[cls.name]={
            'pairs':n,
            'nuisance_invariance':counts['nuisance_invariant']/n,
            'weak_conflict_invariance':counts['weak_conflict_invariant']/n,
            'explicit_update_sensitivity':counts['explicit_update_sensitive']/n,
            'examples':examples,
        }
    return {'design':{'users':n_users,'pairs':len(cases),'seed':seed,'paired_interventions':['other-person high-confidence distractor','weak implicit conflict','explicit current update']},'results':results}

out=evaluate(); (ROOT/'data'/'counterfactual_belief_eval.json').write_text(json.dumps(out,indent=2)+'\n')
lines=['# Counterfactual belief-state checks','','Paired interventions test whether a tracker is invariant to irrelevant evidence yet sensitive to a genuinely relevant current update. This is a controlled causal diagnostic over structured evidence, not a natural-language or human-validity result.','', '| Tracker | Pairs | Nuisance invariance | Weak-conflict invariance | Explicit-update sensitivity |','|---|---:|---:|---:|---:|']
for name,m in out['results'].items(): lines.append(f"| {name} | {m['pairs']} | {m['nuisance_invariance']:.1%} | {m['weak_conflict_invariance']:.1%} | {m['explicit_update_sensitivity']:.1%} |")
lines += ['', 'The three rates intentionally measure different desiderata. A system that is invariant to everything is not adaptive; a system that flips on every weak cue is not robust. These checks therefore complement, rather than replace, state accuracy and calibration.']
(ROOT/'reports'/'COUNTERFACTUAL_BELIEF_EVAL.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(out['results'],indent=2))
