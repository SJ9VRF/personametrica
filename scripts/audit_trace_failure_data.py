from __future__ import annotations
import hashlib, json, random
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows=[json.loads(x) for x in (ROOT/'data'/'trajectory_failure_pairs.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
# Semantic-template hashes remove IDs so duplicates are not hidden by unique trial identifiers.
def normalize(s):
    import re
    s=re.sub(r'agent-task-\d+-trial-\d+','<trial>',s)
    return ' '.join(s.lower().split())
semantic=[hashlib.sha256((normalize(r['chosen'])+'||'+normalize(r['rejected'])).encode()).hexdigest() for r in rows]
by_task=defaultdict(list)
for r in rows: by_task[r['task_id']].append(r)
tasks=sorted(by_task)
r=random.Random(41); r.shuffle(tasks)
n=len(tasks); train=set(tasks[:int(.7*n)]); dev=set(tasks[int(.7*n):int(.85*n)]); test=set(tasks[int(.85*n):])
def split_name(t): return 'train' if t in train else ('dev' if t in dev else 'test')
splits={'train':[],'dev':[],'test':[]}
for row in rows: splits[split_name(row['task_id'])].append(row['id'])
(ROOT/'data'/'trajectory_failure_splits.json').write_text(json.dumps({'seed':41,'task_disjoint':True,'splits':splits},indent=2),encoding='utf-8')
out={
    'rows':len(rows),'unique_task_ids':len(by_task),'exact_unique_pairs':len({(r['chosen'],r['rejected']) for r in rows}),
    'semantic_template_count':len(set(semantic)),'semantic_template_duplication_rate':1-len(set(semantic))/max(1,len(rows)),
    'perturbation_counts':dict(Counter(r['perturbation'] for r in rows)),
    'split_sizes':{k:len(v) for k,v in splits.items()},
    'task_overlap':{
        'train_dev':len(train&dev),'train_test':len(train&test),'dev_test':len(dev&test),
    }
}
(ROOT/'data'/'trajectory_failure_data_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
lines=['# Trajectory failure-data audit','',
'The failure-derived data is useful as plumbing evidence, but its templated nature can create shortcut learning. This audit makes that limitation explicit and creates task-disjoint splits.','',
f"- Rows: {out['rows']}",f"- Unique tasks: {out['unique_task_ids']}",f"- Semantic correction templates: {out['semantic_template_count']}",f"- Semantic-template duplication rate: **{100*out['semantic_template_duplication_rate']:.1f}%**",'',
'## Task-disjoint splits','',f"- Train: {out['split_sizes']['train']}",f"- Dev: {out['split_sizes']['dev']}",f"- Test: {out['split_sizes']['test']}",'- Task overlap across splits: 0','',
'## Interpretation','',
'This dataset should not be used to claim semantic post-training generalization in its current form. It is a structured failure-to-data artifact. A model-training paper should replace or augment templated corrections with independently authored/model-generated corrections and evaluate on task- and wording-held-out failures.']
(ROOT/'reports'/'TRACE_FAILURE_DATA_AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
