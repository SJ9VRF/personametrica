# PersonaMetrica v4.2.0 — Final Release Summary

## What this release proves

The paper-first contribution, PersonaMetrica-Bench, evaluates long-horizon personalization as belief updating plus action under uncertainty. The broader repository remains an end-to-end systems substrate. All headline evidence is controlled and synthetic; human and frontier-model outcomes are intentionally left unclaimed until executed.

## QA

- **77 tests passed**
- **67-stage reproduction pipeline**
- behavioral regression gates pass
- release metadata/version consistency is enforced

## PersonaMetrica-Bench paper evidence

- standard PBS state accuracy: **0.932** vs. time-aware-latest **0.906**
- standard PBS decision utility: **0.768** vs. time-aware-latest **0.572**
- 800-turn native-confidence utility initially favors PBS, but equal development-only post-hoc calibration flips the fixed-threshold utility ordering; AURC remains lower for PBS.
- full six-system 75-cell audit: winner-change probability **0.516**, mean Kendall tau **0.699**, minimum **0.20**; winner counts = {'time-aware-latest': 45, 'personal-belief-state': 27, 'first-mention': 3}.
- paired seed-bootstrap diagnostic: winner-change **0.516**, 95% CI **[0.507, 0.538]**; P(change > .40) = **1.000**.
- 13 leave-one-level-out protocol-grid perturbations: winner-change range **0.327–0.564**; all retain multiple winners.
- benchmark health: identity overlap **0**, full-history overlap **0**, standard duplicate full histories **0**.

## Agent-eval reliability

- robust trajectory grader accuracy on authored suite: **1.000**
- end-state-only false-accept rate: **0.443**
- benign mutation invariance: **100.0%**
- missing-evidence abstention: **100.0%**
- failure-correction semantic-template duplication: **98.4%** (explicit limitation)

## Legacy systems regression evidence

- `personalization_accuracy`: **1.000**
- `stale_memory_rate`: **0.000**
- `contradiction_rate`: **0.000**
- `proactive_decision_accuracy`: **0.865**
- `autonomy_violation_rate`: **0.000**
- `high_stakes_confirmation_rate`: **0.941**
- `low_confidence_clarification_rate`: **0.939**
- `failure_detection_rate`: **1.000**
- `verified_recovery_rate`: **1.000**
- `goal_lifecycle_accuracy`: **1.000**
- `forget_success_rate`: **1.000**
- `privacy_sensitive_block_rate`: **1.000**
- `language_stress_accuracy`: **0.933**

## Training path

- unique validated preference pairs: **724**
- exact duplicate rows: **0**
- standard lexical test accuracy: **1.000**
- random-label control: **0.493**
- lexical contrast accuracy: **0.500**

## Generalization audit

- standard test rows with a response pair already seen in train: **98.6%**
- unseen paraphrase accuracy: **0.667**
- bidirectional calibration Brier: **0.072**
- bidirectional calibration ECE: **0.260**

## Important boundaries

- synthetic users and hand-defined evaluation oracles
- transparent/rule-based default state extractor rather than a frontier learned model
- lexical reward baseline shows weak unseen-paraphrase semantic generalization
- no executed longitudinal human study
- deterministic tool sandbox rather than open-world account actions

## Reviewer path

Read `paper/personametrica_anonymous.pdf` → `reports/LEADERBOARD_STABILITY_AUDIT.md` → `reports/LEADERBOARD_SEED_UNCERTAINTY.md` → `reports/PROTOCOL_GRID_ROBUSTNESS.md` → `reports/BENCHMARK_HEALTH_AUDIT.md` → `reports/NOVELTY_SOTA_AUDIT.md` → `docs/NEURIPS_READINESS.md`; use `project/index.html` for the broader systems/portfolio view. Then run `python scripts/reproduce.py`.
