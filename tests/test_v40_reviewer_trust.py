import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_reviewer_demo_artifact_passes():
    d=json.loads((ROOT/'data/reviewer_demo.json').read_text())
    assert d['status']=='PASS'
    assert all(d['checks'].values())
    assert d['headline_evidence']['protocol_cells']==75
    assert d['headline_evidence']['heldout_causal_grader_false_accept_rate']==0.0

def test_cold_start_artifact_is_explicit_about_execution_mode():
    d=json.loads((ROOT/'data/cold_start_audit.json').read_text())
    assert d['status']=='PASS'
    assert d['checks']['fresh_venv_created']
    assert d['checks']['package_imports']
    assert d['checks']['module_cli_demo_exit_zero']
    assert d['isolation_mode'] in {'stdlib-path-isolation','editable-install --no-deps --no-build-isolation'}

def test_hiring_docs_have_claim_boundaries():
    ledger=(ROOT/'docs/EVIDENCE_LEDGER.md').read_text()
    brief=(ROOT/'docs/FRONTIER_RESEARCH_BRIEF.md').read_text()
    packet=(ROOT/'docs/HIRING_PACKET.md').read_text()
    assert 'Claims intentionally not made' in ledger
    assert 'not a frontier-model leaderboard' in ledger
    assert 'Research thesis' in brief
    assert '60 seconds' in packet

def test_protocol_fingerprint_still_matches_after_v4_release_update():
    raw=(ROOT/'configs/protocol_registry.json').read_bytes()
    fp=json.loads((ROOT/'data/protocol_registry_fingerprint.json').read_text())
    assert hashlib.sha256(raw).hexdigest()==fp['sha256']
