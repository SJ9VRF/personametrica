# PersonaMetrica-Bench dataset / benchmark card

## Summary

PersonaMetrica-Bench is a **synthetic controlled evaluation resource**, not a sample of real users. It is designed to isolate a scientific question: whether current-state accuracy is sufficient to evaluate memory systems that drive personalized actions, or whether confidence quality and risk/coverage change the system ranking.

## Standard release

- 500 synthetic users
- 240 turns per user
- 10 preference domains
- 27,133 structured observations
- 13,500 state/decision queries
- five language tags (`en`, `es`, `fr`, `fa`, `zh`) used as metadata only
- observation sources: explicit, implicit choice, implicit behavior, hypothetical, other-person
- durable changes and temporary scoped exceptions

## Unit of data

Each JSONL row is one synthetic user containing an observation sequence and query sequence. Observations include slot, value, source, confidence, turn, optional context, optional expiry, language tag, and provenance. Queries include turn, target slot, expected current value, and optional context.

## Intended uses

- testing temporal/evidence-aware belief updating;
- comparing memory/state representations under controlled noise;
- evaluating confidence calibration and risk-coverage;
- reproducing the paper's controlled findings;
- developing external model adapters before moving to human or natural-language histories.

## Not recommended

Do **not** use PersonaMetrica-Bench to claim:

- human preference distributions;
- demographic representativeness;
- natural-language understanding quality;
- multilingual extraction ability;
- frontier-model personalization performance;
- real-world safety of autonomous actions.

## Known biases and assumptions

The simulator fixes the domain set, source reliability categories, event frequencies, and change process. All ten domains are binary. The Personal Belief State reference implementation encodes source reliabilities that are directionally aligned with the generator; this makes the benchmark suitable for controlled mechanism analysis but insufficient as a sole method-comparison dataset.

## Split hygiene

Synthetic display identities are seed-scoped in v3.8. The release-gated benchmark health audit requires zero development/test identity overlap, zero complete-history overlap after removing identifiers, and zero duplicate complete histories in the 500-user standard cohort. Structured event fragments may repeat because the simulator uses a finite schema; the evolving full history is the unit used for leakage checks. See `reports/BENCHMARK_HEALTH_AUDIT.md`.

## Privacy

No real-person data is used. User IDs and histories are generated. The dataset contains no intentionally inserted secrets, health records, addresses, or other real sensitive attributes.

## Reproducibility

Generate the standard export with:

```bash
python scripts/export_belief_dataset.py
```

Run the primary benchmark with:

```bash
python scripts/run_belief_benchmark.py
python scripts/belief_statistics.py
python scripts/belief_risk_coverage.py
python scripts/belief_sensitivity.py
```

The Croissant-style machine-readable metadata is `data/personalbench_x_croissant.json`.
