from __future__ import annotations
import json,sys,hashlib
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig,generate_user_stream,DOMAINS

def main():
    cfg=BenchmarkConfig(users=500,turns=240,seed=31)
    src=Counter(); slots=Counter(); langs=Counter(); prov=Counter(); vals=Counter(); qslots=Counter(); contexts=Counter(); fingerprints=Counter(); obs_n=q_n=0
    users_with_queries=0
    for i in range(cfg.users):
        obs,qs=generate_user_stream(i,cfg); obs_n+=len(obs);q_n+=len(qs); users_with_queries+=bool(qs)
        for o in obs:
            src[o.source]+=1; slots[o.slot]+=1; langs[o.language]+=1; prov[o.provenance]+=1; vals[(o.slot,o.value)]+=1
            fp=(o.turn,o.slot,o.value,o.source,o.context,o.temporary_until,o.provenance); fingerprints[fp]+=1
        for q in qs: qslots[q.slot]+=1; contexts['temporary' if q.context else 'general']+=1
    duplicate_obs=sum(c-1 for c in fingerprints.values() if c>1)
    # deterministic replay digest
    def digest():
      h=hashlib.sha256()
      for i in range(25):
       o,q=generate_user_stream(i,cfg)
       for x in o: h.update(repr(x).encode())
       for x in q: h.update(repr(x).encode())
      return h.hexdigest()
    d1,d2=digest(),digest()
    audit={'config':cfg.__dict__ if hasattr(cfg,'__dict__') else {k:getattr(cfg,k) for k in cfg.__dataclass_fields__},'observations':obs_n,'queries':q_n,
           'users_with_queries':users_with_queries,'source_counts':src,'slot_counts':slots,'language_tag_counts':langs,'provenance_counts':prov,'query_slot_counts':qslots,'query_context_counts':contexts,
           'duplicate_observation_fingerprints':duplicate_obs,'deterministic_replay':d1==d2,'replay_sha256':d1}
    # JSON convert Counters/tuple keys
    clean={k:(dict(v) if isinstance(v,Counter) else v) for k,v in audit.items() if k!='slot_value_counts'}
    (ROOT/'data/benchmark_integrity_audit.json').write_text(json.dumps(clean,indent=2,default=str))
    lines=['# PersonaMetrica-Bench integrity audit','',f"Standard generator: {cfg.users} users × {cfg.turns} turns; {obs_n:,} observations; {q_n:,} queries.",'',f"- Deterministic replay: **{d1==d2}**",f"- Users with queries: **{users_with_queries}/{cfg.users}**",f"- Exact structured observation fingerprint duplicates across users: **{duplicate_obs:,}** (expected because the benchmark is generated from a finite structured schema; user histories/sequences differ).",'', '## Evidence-source counts','']
    for k,v in src.most_common(): lines.append(f"- `{k}`: {v:,}")
    lines += ['', '## Query contexts',''] + [f"- `{k}`: {v:,}" for k,v in contexts.items()]
    lines += ['', '## Audit boundary','', 'This audit checks generator determinism, coverage, and structured duplication. It does **not** establish natural-language novelty because PersonaMetrica-Bench v3.x begins after evidence extraction.']
    (ROOT/'reports/BENCHMARK_INTEGRITY_AUDIT.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'observations':obs_n,'queries':q_n,'deterministic':d1==d2,'duplicate_fingerprints':duplicate_obs},indent=2))
if __name__=='__main__': main()
