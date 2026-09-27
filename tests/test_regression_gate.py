from scripts.regression_gate import evaluate

def test_regression_gate_pass_and_fail():
    gates={'full_temporal_os':{'acc':{'min':.9},'err':{'max':.1}}}
    good={'systems':{'full_temporal_os':{'metrics':{'acc':.95,'err':.05}}}}
    bad={'systems':{'full_temporal_os':{'metrics':{'acc':.8,'err':.2}}}}
    assert evaluate(good,gates)==[]
    assert len(evaluate(bad,gates))==2
