from __future__ import annotations
import hashlib, json, sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import BenchmarkConfig, DOMAINS, generate_user_stream

DEV_SEEDS=(1,2,3); TEST_SEEDS=tuple(range(30,40))

def stream_fp(stream):
    obs,qs=stream
    # Exclude user_id so this detects duplicated content, not just duplicated IDs.
    payload={
      'obs':[{k:v for k,v in asdict(x).items() if k!='user_id'} for x in obs],
      'queries':[{k:v for k,v in asdict(x).items() if k!='user_id'} for x in qs],
    }
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def build(seed,users,turns,qe):
    cfg=BenchmarkConfig(seed=seed,users=users,turns=turns,query_every=qe)
    return [generate_user_stream(i,cfg) for i in range(users)]

def main():
    dev={s:build(s,60,240,24) for s in DEV_SEEDS}
    test={s:build(s,40,800,50) for s in TEST_SEEDS}
    dev_ids={o.user_id for streams in dev.values() for obs,_ in streams for o in obs[:1]}
    test_ids={o.user_id for streams in test.values() for obs,_ in streams for o in obs[:1]}
    dev_fp={stream_fp(x) for streams in dev.values() for x in streams}
    test_fp={stream_fp(x) for streams in test.values() for x in streams}

    std=build(31,500,240,24)
    std_fps=[stream_fp(x) for x in std]
    qslots=Counter(); answers=Counter(); temp=0; qtotal=0; sources=Counter(); domains=Counter()
    for obs,qs in std:
        for o in obs: sources[o.source]+=1; domains[o.slot]+=1
        for q in qs:
            qtotal+=1; qslots[q.slot]+=1; answers[(q.slot,q.expected)]+=1; temp+=q.context is not None
    qvals=list(qslots.values()); imbalance=(max(qvals)-min(qvals))/max(1,sum(qvals)/len(qvals))
    answer_skews={slot:max(answers[(slot,v)] for v in vals)/max(1,sum(answers[(slot,v)] for v in vals)) for slot,vals in DOMAINS.items()}
    top_acc=json.loads((ROOT/'data'/'belief_benchmark_results.json').read_text())['standard']['results']
    best=max(v['accuracy'] for v in top_acc.values())
    checks={
      'dev_test_identity_overlap_zero':len(dev_ids & test_ids)==0,
      'dev_test_full_stream_overlap_zero':len(dev_fp & test_fp)==0,
      'standard_full_stream_duplicates_zero':len(std_fps)==len(set(std_fps)),
      'all_domains_queried':set(qslots)==set(DOMAINS),
      'temporary_queries_present':temp>0,
      'query_slot_imbalance_below_15pct':imbalance<0.15,
      'answer_skew_below_70pct':max(answer_skews.values())<0.70,
      'benchmark_not_saturated':best<0.99,
    }
    out={
      'version':'4.2.0','checks':checks,'all_pass':all(checks.values()),
      'counts':{'dev_identities':len(dev_ids),'test_identities':len(test_ids),'identity_overlap':len(dev_ids&test_ids),'dev_streams':len(dev_fp),'test_streams':len(test_fp),'full_stream_overlap':len(dev_fp&test_fp),'standard_users':len(std),'standard_duplicate_full_streams':len(std_fps)-len(set(std_fps)),'standard_queries':qtotal,'temporary_queries':temp},
      'query_slot_counts':dict(qslots),'query_slot_relative_range':imbalance,'max_answer_skew':max(answer_skews.values()),'answer_skew_by_slot':answer_skews,'observation_source_counts':dict(sources),'observation_domain_counts':dict(domains),'best_standard_state_accuracy':best,
      'note':'Structured sub-records can repeat because the simulator uses a finite schema. This audit hashes complete evolving user histories with identifiers removed; full-history duplication is the leakage-relevant diagnostic.'
    }
    (ROOT/'data'/'benchmark_health_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    lines=['# Benchmark Health Audit','',
           'This release treats benchmark hygiene as a release condition rather than a prose limitation. The scientific unit is a complete evolving user history, not an isolated structured event.','',
           '## Release checks','', '| Check | Status |','|---|---|']
    for k,v in checks.items(): lines.append(f"| {k.replace('_',' ')} | {'PASS' if v else 'FAIL'} |")
    lines += ['', '## Key measurements','',
              f"- Development/test display-identity overlap: **{len(dev_ids & test_ids)}**.",
              f"- Development/test complete-history overlap after removing IDs: **{len(dev_fp & test_fp)}**.",
              f"- Duplicate complete histories in the 500-user standard cohort: **{len(std_fps)-len(set(std_fps))}**.",
              f"- Temporary-scope queries: **{temp} / {qtotal}**.",
              f"- Query-slot relative range: **{imbalance:.3f}**.",
              f"- Maximum binary-answer skew within a slot: **{max(answer_skews.values()):.3f}**.",
              f"- Best standard state accuracy: **{best:.3f}**, so the benchmark is not saturated.",'',
              '## Boundary','',
              'Passing these checks does not make the synthetic population representative of humans, and it does not validate natural-language extraction. It removes avoidable split leakage and duplication shortcuts from the controlled benchmark.']
    (ROOT/'reports'/'BENCHMARK_HEALTH_AUDIT.md').write_text('\n'.join(lines)+'\n')
    if not out['all_pass']: raise SystemExit('Benchmark health audit failed')
    print(json.dumps(out['counts'],indent=2)); print('Benchmark health audit: PASS')

if __name__=='__main__': main()
