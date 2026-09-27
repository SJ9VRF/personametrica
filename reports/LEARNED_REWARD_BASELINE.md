# Learned Reward Baseline

A real pairwise ranking baseline is trained locally with logistic SGD over unigram/bigram response features. It is intentionally small and auditable; it is **not** presented as an LLM reward model.

## Split

- Train: 582
- Validation: 71
- Test: 71
- Split is group-aware rather than row-random.

## Results

- Train pairwise accuracy: **1.000**
- Validation pairwise accuracy: **1.000**
- Test pairwise accuracy: **1.000**
- Random-label negative-control accuracy: **0.493**
- Lexically matched contrast accuracy: **0.500**

## Test accuracy by family

- `high_stakes_autonomy`: 1.000 (n=5)
- `low_value_proactivity`: 1.000 (n=2)
- `reversible_assistance`: 1.000 (n=29)
- `temporal_memory`: 1.000 (n=1)
- `uncertainty_calibration`: 1.000 (n=34)

## Interpretation

This establishes that the post-training data path can train and evaluate a learned preference scorer end-to-end. High lexical-baseline performance should not be interpreted as evidence that the underlying preference problem is solved; the dataset is synthetic and intentionally structured.

## Negative control

The randomized held-out labels should drive accuracy toward chance. The lexically matched contrast set intentionally uses nearly identical words with opposite meanings; it exposes the expected limitation of a bag-of-words/bigram reward baseline.
