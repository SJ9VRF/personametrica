import json
from pathlib import Path
import pytest
from external_benchmarks.horizonbench_adapter import load_results, compare_models, utility

ROOT=Path(__file__).resolve().parents[1]

def test_protocol_grid_leave_one_level_robustness():
    d=json.loads((ROOT/'data'/'protocol_grid_robustness.json').read_text())
    r=d['robustness_summary']
    assert r['perturbations']==13
    assert r['perturbations_with_multiple_winners']==13
    assert r['min_winner_change_probability']>0.30
    assert r['max_mean_kendall_tau']<0.91

def test_seed_bootstrap_diagnostic_supports_instability():
    d=json.loads((ROOT/'data'/'leaderboard_seed_uncertainty.json').read_text())
    assert d['diagnostic_users_per_seed']==10
    assert d['bootstrap_replicates']>=2000
    lo,hi=d['bootstrap_95_ci']['winner_change_probability']
    assert lo>0.40 and hi<0.60
    assert d['bootstrap_claim_support']['p_winner_change_gt_0_40']>=0.99
    assert d['bootstrap_claim_support']['p_mean_tau_lt_0_90']>=0.99

def test_horizonbench_adapter_fixture_contract():
    fx=ROOT/'external_benchmarks'/'fixtures'
    a=load_results(fx/'horizonbench_results_model_a.jsonl')
    b=load_results(fx/'horizonbench_results_model_b.jsonl')
    s=compare_models({'a':a,'b':b})
    assert s['a']['n']==6 and s['b']['n']==6
    assert s['a']['evolved_n']==3 and s['a']['static_n']==3
    assert utility(a,.70,.10)==pytest.approx(.3)

def test_horizonbench_adapter_refuses_invented_confidence(tmp_path):
    p=tmp_path/'r.jsonl'
    p.write_text('{"id":"x","generator":"g","has_evolved":true,"correct_letter":"A","predicted_letter":"A","correct":true}\n')
    rows=load_results(p)
    with pytest.raises(ValueError,match='requires confidence'):
        utility(rows,.7,.1)
