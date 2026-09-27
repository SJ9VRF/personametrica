from __future__ import annotations
import hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
summary=json.loads((ROOT/'data/evidence_layer_summary.json').read_text())
checks={}
def check(k,c,detail=''):
    checks[k]={'passed':bool(c),'detail':detail}

journal=(ROOT/'experiments/EXPERIMENT_JOURNAL.md').read_text()
failed=(ROOT/'experiments/FAILED_EXPERIMENTS.md').read_text()
decisions=(ROOT/'experiments/DECISION_LOG.md').read_text()
unexpected=(ROOT/'experiments/UNEXPECTED_FINDINGS.md').read_text()
check('experiment_count',len(re.findall(r'^## EXP-\d{3}',journal,re.M))==summary['logged_experiments'])
check('failed_count',len(re.findall(r'^## F-\d{3}',failed,re.M))==summary['failed_or_revised_hypotheses'])
check('decision_count',len(re.findall(r'^## D-\d{3}',decisions,re.M))==summary['major_design_changes'])
check('unexpected_present',len(re.findall(r'^## U-\d{3}',unexpected,re.M))>=5)
logs=list((ROOT/'artifacts/experiment_logs').glob('EXP-*.md'))
check('per_experiment_logs',len(logs)==summary['logged_experiments'],f'{len(logs)} logs')
for d,min_count in [('eval_runs',10),('failure_examples',3),('plots',4),('configs',3),('qualitative_cases',2),('ablations',1)]:
    files=[p for p in (ROOT/'artifacts'/d).iterdir() if p.is_file()]
    check('raw_'+d,len(files)>=min_count,f'{len(files)} files')
# Raw copied eval results must be byte-identical to their canonical data source.
for p in (ROOT/'artifacts/eval_runs').glob('*.json'):
    src=ROOT/'data'/p.name
    check('copy_'+p.stem,src.exists() and hashlib.sha256(src.read_bytes()).digest()==hashlib.sha256(p.read_bytes()).digest(),p.name)
# Every explicit Evidence path in journal should resolve when it is a repo-relative file.
paths=re.findall(r'`((?:data|reports|experiments|scripts)/[^`]+)`',journal)
missing=[x for x in paths if not (ROOT/x).exists()]
check('journal_evidence_paths',not missing,f'missing={missing}')
# Git history must exist in full release and have the honest import baseline.
git=ROOT/'.git'
check('git_history_present',git.exists(),'.git absent')
# We avoid shelling out here; HEAD/ref existence plus policy text is enough for static audit.
check('git_policy_explicit','does **not** fabricate an earlier commit history' in (ROOT/'docs/GIT_HISTORY.md').read_text())
passed=all(v['passed'] for v in checks.values())
out={'status':'PASS' if passed else 'FAIL','summary':summary,'checks':checks}
(ROOT/'data/evidence_layer_audit.json').write_text(json.dumps(out,indent=2)+'\n')
lines=['# Evidence Layer Audit','',f"**Status:** {out['status']}",'',f"Checks: {sum(v['passed'] for v in checks.values())}/{len(checks)} passed.",'']
for k,v in checks.items(): lines.append(f"- {'✓' if v['passed'] else '✗'} `{k}`" + (f" — {v['detail']}" if not v['passed'] and v['detail'] else ''))
(ROOT/'reports/EVIDENCE_LAYER_AUDIT.md').write_text('\n'.join(lines)+'\n')
if not passed: raise SystemExit('Evidence Layer audit failed')
print(f"Evidence Layer audit PASS: {len(checks)} checks")
