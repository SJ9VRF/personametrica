from personalagi.training import TrainingDataPipeline, PairwiseLinearRanker


def _rows():
    p=TrainingDataPipeline()
    return [
        p.preference_pair('current preference changed', 'use current preference', 'use stale preference', reason='temporal', metadata={'group':0}),
        p.preference_pair('high stakes action', 'ask for confirmation', 'act immediately', reason='autonomy', metadata={'group':1}),
        p.preference_pair('low confidence intent', 'ask a clarifying question', 'act immediately', reason='uncertainty', metadata={'group':2}),
        p.preference_pair('forget this memory', 'delete the memory', 'keep the memory', reason='privacy', metadata={'group':3}),
    ]


def test_dedup_and_validation():
    p=TrainingDataPipeline(); rows=_rows()
    out, removed=p.deduplicate(rows+[dict(rows[0])])
    assert len(out)==4 and removed==1


def test_pairwise_ranker_learns_small_dataset():
    rows=_rows()*8
    model=PairwiseLinearRanker(min_df=1, epochs=80, lr=.15, seed=1).fit(rows)
    assert model.evaluate(rows).accuracy >= .75
