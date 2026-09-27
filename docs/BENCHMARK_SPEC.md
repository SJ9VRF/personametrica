# PersonalBench Benchmark Specification

## Purpose
PersonalBench is a controlled research harness for testing longitudinal mechanisms in PersonaMetrica. It is not a claim of frontier-model or human-level performance.

## Evaluation layers

1. **Temporal memory** — current-preference correctness, stale-state rate, active contradictions.
2. **Conditional personalization** — context-scoped preferences must coexist with general preferences.
3. **User control** — explicit forgetting must remove active retrieval without re-learning the command.
4. **Privacy persistence policy** — narrow synthetic sensitive-memory cases are blocked while ordinary preferences remain storable.
5. **Goal lifecycle** — creation, completion, and abandonment transitions.
6. **Proactivity judgment** — action/ask/suggest/remind/wait/none under urgency, uncertainty, stakes, reversibility, and interruptibility.
7. **Outcome verification** — injected world-state mismatches must be detected.
8. **Language stress** — reversals, hedges, ellipsis, negation, and conditional language.
9. **Reward-data learning** — pairwise training path, controls, leakage audit, family holdout, and unseen paraphrases.

## Reproducibility
The default checked-in run uses seed 7 for the primary benchmark and a 10-seed paired analysis for major ablations. `python scripts/reproduce.py` regenerates release evidence.

## Statistical reporting
Per-user longitudinal metrics include bootstrap 95% intervals. Major mechanism effects are evaluated as paired differences across seeds. These intervals quantify variability under the synthetic generator only.

## Claim boundaries
- Synthetic users are not substitutes for longitudinal human participants.
- Rule-based extraction is a controlled substrate, not a frontier personalization model.
- The lexical pairwise ranker is a training-path baseline, not an LLM reward model.
- Privacy tests cover narrow synthetic phrase classes, not general PII detection.
- Deterministic tool sandbox results do not establish reliability on open-world APIs.
