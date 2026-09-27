from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]

def test_evidence_layer_counts_and_paths():
    s=json.loads((ROOT/'data/evidence_layer_summary.json').read_text())
    assert len(re.findall(r'^## EXP-\d{3}',(ROOT/'experiments/EXPERIMENT_JOURNAL.md').read_text(),re.M))==s['logged_experiments']
    assert len(re.findall(r'^## F-\d{3}',(ROOT/'experiments/FAILED_EXPERIMENTS.md').read_text(),re.M))==s['failed_or_revised_hypotheses']
    assert len(re.findall(r'^## D-\d{3}',(ROOT/'experiments/DECISION_LOG.md').read_text(),re.M))==s['major_design_changes']
    assert len(list((ROOT/'artifacts/experiment_logs').glob('EXP-*.md')))==s['logged_experiments']

def test_evidence_layer_homepage_and_git_policy():
    html=(ROOT/'project/index.html').read_text()
    assert 'id="research-process"' in html
    for x in ['EXPERIMENT_JOURNAL.md','FAILED_EXPERIMENTS.md','DECISION_LOG.md','artifacts/README.md','GIT_HISTORY.md']:
        assert x in html
    policy=(ROOT/'docs/GIT_HISTORY.md').read_text()
    assert 'does **not** fabricate an earlier commit history' in policy

def test_raw_eval_copies_match_canonical():
    import hashlib
    for p in (ROOT/'artifacts/eval_runs').glob('*.json'):
        src=ROOT/'data'/p.name
        assert src.exists()
        assert hashlib.sha256(src.read_bytes()).digest()==hashlib.sha256(p.read_bytes()).digest()
