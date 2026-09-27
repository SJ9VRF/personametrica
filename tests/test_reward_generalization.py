from scripts.reward_generalization_eval import sigmoid, calibration
from personalagi.training import PairwiseLinearRanker

def test_sigmoid_is_bounded_and_ordered():
    assert 0 < sigmoid(-5) < sigmoid(0) < sigmoid(5) < 1

def test_bidirectional_calibration_has_two_orientations():
    rows=[{'prompt':'x','chosen':'good helpful response','rejected':'bad harmful response'} for _ in range(4)]
    m=PairwiseLinearRanker(min_df=1,epochs=2).fit(rows)
    c=calibration(m,rows,bins=5)
    assert c['n']==8
    assert 0 <= c['brier'] <= 1
    assert 0 <= c['ece'] <= 1
