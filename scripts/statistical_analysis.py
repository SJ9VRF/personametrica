from __future__ import annotations
import json, random, statistics, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from personalagi.config import AgentConfig
from personalbench.simulator.users import generate_personas
from personalbench.runner import (
    _eval_memory_system, _eval_proactivity, _eval_outcome_verification,
    _eval_privacy_guard, _eval_goal_lifecycle,
)

def mean(xs): return statistics.fmean(xs) if xs else 0.0

def bootstrap_effect(values, seed=1103, samples=3000):
    if not values: return {"mean":0.0,"ci95":[0.0,0.0]}
    r=random.Random(seed); n=len(values); draws=[]
    for _ in range(samples):
        draws.append(mean([values[r.randrange(n)] for _ in range(n)]))
    draws.sort()
    return {"mean":mean(values),"ci95":[draws[int(.025*samples)],draws[min(samples-1,int(.975*samples))]]}

def main():
    seeds=[3,7,11,19,29,43,59,71,89,101]
    effects={k:[] for k in [
        "temporal_personalization_gain","temporal_stale_memory_reduction",
        "conflict_resolution_gain","proactivity_accuracy_gain",
        "verification_failure_detection_gain","privacy_sensitive_block_gain",
        "goal_lifecycle_gain",
    ]}
    per_seed=[]
    full=AgentConfig.full(); first=AgentConfig(memory_update_policy='first')
    conflict=AgentConfig(memory_update_policy='all',contradiction_resolution=False)
    uncal=AgentConfig(calibrated_proactivity=False); nover=AgentConfig(outcome_verification=False)
    nopriv=AgentConfig(privacy_guard=False); nogoal=AgentConfig(goal_model=False)
    for seed in seeds:
        fmem,_,_=_eval_memory_system(generate_personas(100,seed),60,full)
        firstmem,_,_=_eval_memory_system(generate_personas(100,seed),60,first)
        confmem,_,_=_eval_memory_system(generate_personas(100,seed),60,conflict)
        fp=_eval_proactivity(full,seed); up=_eval_proactivity(uncal,seed)
        fv=_eval_outcome_verification(full); nv=_eval_outcome_verification(nover)
        fpriv=_eval_privacy_guard(full); npriv=_eval_privacy_guard(nopriv)
        fg=_eval_goal_lifecycle(full); ng=_eval_goal_lifecycle(nogoal)
        pairs={
            "temporal_personalization_gain": fmem['personalization_accuracy']-firstmem['personalization_accuracy'],
            "temporal_stale_memory_reduction": firstmem['stale_memory_rate']-fmem['stale_memory_rate'],
            "conflict_resolution_gain": confmem['contradiction_rate']-fmem['contradiction_rate'],
            "proactivity_accuracy_gain": fp['proactive_decision_accuracy']-up['proactive_decision_accuracy'],
            "verification_failure_detection_gain": fv['failure_detection_rate']-nv['failure_detection_rate'],
            "privacy_sensitive_block_gain": fpriv['privacy_sensitive_block_rate']-npriv['privacy_sensitive_block_rate'],
            "goal_lifecycle_gain": fg['goal_lifecycle_accuracy']-ng['goal_lifecycle_accuracy'],
        }
        row={"seed":seed,**pairs}
        for k,v in pairs.items(): effects[k].append(v)
        per_seed.append(row)
    out={"seeds":seeds,"paired_effects":{k:bootstrap_effect(v) for k,v in effects.items()},"per_seed":per_seed}
    (ROOT/'data'/'statistical_analysis.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    lines=['# Statistical Analysis','', 'Paired effects across 10 deterministic benchmark seeds; 95% CIs are bootstrap intervals over seed-level effects.','', '| Effect | Mean | 95% CI |','|---|---:|---:|']
    for k,v in out['paired_effects'].items(): lines.append(f"| {k.replace('_',' ')} | {v['mean']:.3f} | [{v['ci95'][0]:.3f}, {v['ci95'][1]:.3f}] |")
    lines += ['', '> These intervals quantify robustness across this synthetic benchmark generator, not uncertainty for human populations or frontier models.']
    (ROOT/'reports'/'STATISTICAL_ANALYSIS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(out['paired_effects'],indent=2))
if __name__=='__main__': main()
