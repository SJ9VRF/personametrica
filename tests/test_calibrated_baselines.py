from scripts.calibrated_baseline_eval import fit_bucket_calibrator, eval_rows

def test_bucket_calibrator_is_smoothed_and_bounded():
    rows=[('a','a',1.0,True),('a','b',1.0,False),('a','a',0.8,True)]
    mapping,cal=fit_bucket_calibrator(rows)
    assert 0 < mapping[1.0] < 1
    assert 0 < mapping[0.8] < 1
    assert 0 <= cal(.91) <= 1

def test_eval_rows_changes_utility_with_calibration():
    rows=[('a','a',1.0,True),('a','b',1.0,False)]
    _,cal=fit_bucket_calibrator(rows)
    native=eval_rows(rows,lambda x:x)
    calibrated=eval_rows(rows,cal)
    assert native['coverage']==1.0
    assert calibrated['coverage']==0.0
    assert calibrated['decision_utility'] != native['decision_utility']
