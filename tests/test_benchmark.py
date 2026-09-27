from personalbench import run_comparison

def test_benchmark_runs_and_full_beats_stale_baseline_on_drift():
    r=run_comparison(8,45,seed=1)
    for sys in r.values():
        for v in sys.values(): assert 0 <= v <= 1
    assert r['full_temporal_os']['personalization_accuracy'] > r['first_mention_memory']['personalization_accuracy']
    assert r['full_temporal_os']['stale_memory_rate'] < r['first_mention_memory']['stale_memory_rate']
    assert r['full_temporal_os']['goal_capture_rate'] == 1
