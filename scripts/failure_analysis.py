from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from personalagi.agent.core import PersonalAGIAgent
from personalbench.tasks.scenarios import generate_proactivity_scenarios


def bucket(s):
    if s['confidence'] < .5: return 'low_confidence'
    if s['stakes'] >= .8 and s['reversibility'] <= .3: return 'high_stakes_irreversible'
    if s['goal_relevance'] < .25 and s['urgency'] < .25: return 'low_value'
    if s['urgency'] >= .75: return 'urgent'
    return 'ordinary'


def main():
    agent=PersonalAGIAgent('failure-analysis')
    rows=generate_proactivity_scenarios(1000,117)
    by=defaultdict(lambda:{'n':0,'correct':0})
    confusion=Counter(); failures=[]
    for s in rows:
        kwargs={k:v for k,v in s.items() if k not in {'name','expected'}}
        action=agent.proactive_decision(**kwargs).action.value
        ok=action in s['expected']; b=bucket(s)
        by[b]['n']+=1; by[b]['correct']+=int(ok)
        confusion[(tuple(sorted(s['expected'])),action)] += 1
        if not ok and len(failures)<40:
            failures.append({**{k:v for k,v in s.items() if k!='expected'},'expected':sorted(s['expected']),'predicted':action,'slice':b})
    slices={k:{'n':v['n'],'accuracy':v['correct']/v['n'] if v['n'] else 0.0} for k,v in sorted(by.items())}
    out={'scenarios':len(rows),'slices':slices,'confusion':[{'expected':list(k[0]),'predicted':k[1],'count':v} for k,v in confusion.most_common()],'sample_failures':failures}
    (ROOT/'data'/'failure_analysis.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    lines=['# Failure Analysis','', 'Evaluation over 1,000 deterministic proactivity scenarios. This report is diagnostic evidence for the local policy, not a human-behavior claim.','', '| Slice | N | Accuracy |','|---|---:|---:|']
    for k,v in slices.items(): lines.append(f"| {k.replace('_',' ')} | {v['n']} | {100*v['accuracy']:.1f}% |")
    lines += ['', '## Representative errors','']
    for f in failures[:12]:
        lines.append(f"- `{f['slice']}` predicted **{f['predicted']}**, expected `{', '.join(f['expected'])}`; relevance={f['goal_relevance']:.2f}, urgency={f['urgency']:.2f}, confidence={f['confidence']:.2f}, stakes={f['stakes']:.2f}, reversibility={f['reversibility']:.2f}.")
    lines += ['', 'These failures are retained rather than hidden because they define the next policy-learning targets.']
    (ROOT/'reports'/'FAILURE_ANALYSIS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(slices,indent=2))
if __name__=='__main__': main()
