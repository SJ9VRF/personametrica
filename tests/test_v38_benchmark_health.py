from personalbench.belief_benchmark import BenchmarkConfig, generate_user_stream
from scripts.leaderboard_stability_audit import kendall_tau


def test_synthetic_ids_are_seed_scoped():
    a,_=generate_user_stream(0,BenchmarkConfig(users=1,turns=60,seed=1))
    b,_=generate_user_stream(0,BenchmarkConfig(users=1,turns=60,seed=30))
    assert a[0].user_id != b[0].user_id
    assert 's00001' in a[0].user_id
    assert 's00030' in b[0].user_id


def test_generation_remains_deterministic_with_seed_scoped_ids():
    cfg=BenchmarkConfig(users=1,turns=80,seed=7)
    a=generate_user_stream(0,cfg)
    b=generate_user_stream(0,cfg)
    assert a == b


def test_kendall_tau_detects_rank_reversal():
    a=['a','b','c','d']
    assert kendall_tau(a,a) == 1.0
    assert kendall_tau(a,list(reversed(a))) == -1.0
