# PersonaMetrica — hiring packet

**Aura Yavary · research + engineering artifact**

## 60 seconds

PersonaMetrica asks whether personal-agent leaderboards are stable to reasonable evaluation choices. Across six systems and 75 frozen protocols, the winner changes often enough that a single operating point is not a reliable model-selection story. The project then applies the same skepticism to the evaluator itself: a grader that looked perfect on its authored suite fails on new attack families, motivating a stricter causal trace contract.

**Run:** `python scripts/reviewer_demo.py`

## 5 minutes

Read, in order:
1. `reports/REVIEWER_DEMO.md`
2. `docs/FRONTIER_RESEARCH_BRIEF.md`
3. `reports/NOVELTY_SOTA_AUDIT.md`
4. `docs/EVIDENCE_LEDGER.md`

## 15 minutes

Add:
- `paper/personametrica_anonymous.pdf`
- `reports/LEADERBOARD_STABILITY_AUDIT.md`
- `reports/LEADERBOARD_SEED_UNCERTAINTY.md`
- `reports/HELDOUT_GRADER_ATTACKS.md`
- `reports/BENCHMARK_HEALTH_AUDIT.md`

## What I would discuss in an interview

- Why raw state accuracy and action utility can disagree.
- Why confidence calibration must be shared before thresholded utility comparisons.
- Why a leaderboard should be audited as a function of the protocol, not just reported at one operating point.
- How I discovered the evaluator itself had overfit its authored failure families.
- Why the causal grader checks action observability, live permission, payload causality, complete targets, and post-action verification.
- Which remaining evidence would most change my conclusions: real model trajectories, independent human labels, and post-training experiments.

## One sentence

**PersonaMetrica is an evaluation-science project about knowing when a personalized agent—or the benchmark used to select it—only looks good because of the measurement protocol.**
