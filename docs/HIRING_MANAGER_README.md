# PersonaMetrica — 5-minute review

**Aura Yavary · sole researcher / engineer · 2026 · v4.1.0**

> **Fast verification:** `python scripts/reviewer_demo.py` (sub-second in the checked environment). It checks the frozen evidence chain and reruns the held-out causal-grader and temporal-update mechanisms live.

## The question

Long-horizon personal agents are usually compared as if an evaluation score were an intrinsic property of the system. PersonaMetrica asks a harder question: **would the same system still look better if confidence were calibrated fairly, the action protocol changed, or the grader itself were attacked?**

The project combines an evolving user-state benchmark with selective-risk metrics, shared development-only calibration, trajectory grading, held-out evaluator attacks, causal verification, abstention on missing evidence, and counterfactual user-state interventions.

## The result I would inspect first

On 800-turn histories, the fixed-threshold utility ordering between the strongest structured baseline and the Personal Belief State **reverses after equal development-only confidence calibration**. The threshold-free AURC ordering does not reverse in the checked-in benchmark. That is the central result: a seemingly reasonable decision metric can select a different system because of evaluation protocol, not just underlying state quality.

I then froze a broader protocol grid rather than stopping at one illustrative reversal. Across **75 protocol cells** (native/bucket/isotonic confidence × five thresholds × five deferral costs), I rank **all six released baselines**. Time-aware-latest wins 45 cells, PBS 27, and first-mention 3. Two randomly selected protocol cells disagree on the winner with probability **51.6%**; mean complete-ranking Kendall tau is **0.699** and the minimum is **0.20**. A weak stale baseline winning at all is itself a diagnostic: some operating protocols can reward coverage/confidence economics enough to swamp state quality.

I then tested whether that conclusion was itself fragile. On a separate 10-user-per-seed diagnostic, **2,000 paired bootstrap resamples of the ten long-horizon seeds** give winner-change probability **0.516 [0.507, 0.538]** and mean Kendall tau **0.702 [0.692, 0.720]**. Thirteen leave-one-level-out perturbations of the protocol grid all retain multiple winners; winner-change probability ranges **0.327–0.564**. The largest stabilization occurs when native confidence is removed, strengthening the interpretation that confidence comparability—not just state quality—drives model selection.

A separate evaluator-generalization experiment freezes the v3.4 trajectory grader and attacks it with five unseen failure families. The frozen grader false-accepts **96%** of the constructed attacks; a stricter causal-contract grader reduces false accepts to **0%** on that held-out attack set while preserving the original gold-suite labels.

These are controlled synthetic mechanism results—not claims about human preference quality, frontier-model performance, or external-leaderboard SOTA.

## What is actually novel

The 2025–2026 literature already contains strong benchmarks for preference following, evolving preferences, personalized memory, proactivity, over-personalization, and personalized tool use. PersonaMetrica therefore does **not** claim to be the first benchmark in any of those categories.

Its narrower contribution is evaluation science: **protocol-sensitive system selection in evolving personal agents, plus evaluator validity under distribution shift and counterfactual user-state tests**. Ranking instability, trajectory attacks, and disagreement-aware evaluation already exist elsewhere in the 2026 literature; PersonaMetrica connects those measurement concerns to confidence-gated personalized action. The grader is treated as another fallible model: frozen, attacked out of distribution, allowed to abstain when evidence is missing, fingerprinted, and routed to disagreement review.

See `reports/NOVELTY_SOTA_AUDIT.md` for the closest-work comparison and explicit claim boundaries.

## What I owned

I designed the benchmark question, temporal belief representation, shared-calibration protocol, selective-risk analysis, trajectory contracts, causal grader, held-out attack families, counterfactual interventions, failure-to-data pipeline, and release gates. I implemented the runtime, eval harnesses, data generation, grader reliability tooling, paper, reproducibility scripts, and reviewer-facing artifacts.

## Known failures kept visible

- PBS nuisance invariance is **98.0%**, not 100%; high-confidence evidence about another person can still flip a close belief decision in a small slice.
- Failure-derived text corrections remain highly templated and are not presented as evidence of successful post-training.
- No independent human grader calibration or frontier/open-weight model run is claimed yet.

## Project page contract

`project/index.html` is a standalone 14-part flagship page designed for a 60-second first pass. The Hero states the problem, my contribution, the main result, and an executable proof path before the reader scrolls. The first five CTAs are **Paper / Code / Demo / Benchmark / Video**; the rest of the page exposes architecture loops, ownership decisions, experiments, a baseline→method results snapshot, real failure modes, an inspectable recovery trajectory, scaling/cost scope, safety boundaries, technical reports, artifacts, and BibTeX. The structure is release-gated by `scripts/project_page_qa.py`.

## Review path

- **60 seconds:** `project/index.html`
- **5 minutes:** this file + `reports/NOVELTY_SOTA_AUDIT.md`
- **15 minutes:** `paper/PAPER.md` + `reports/LEADERBOARD_STABILITY_AUDIT.md` + `reports/LEADERBOARD_SEED_UNCERTAINTY.md` + `reports/PROTOCOL_GRID_ROBUSTNESS.md` + `reports/HELDOUT_GRADER_ATTACKS.md`
- **Deep review:** `docs/BENCHMARK_SPEC.md`, `docs/GRADER_CALIBRATION_PROTOCOL.md`, `docs/EVIDENCE_LEDGER.md`

The repository is deliberately explicit about what is synthetic, what was measured, what failed, and what still requires external evidence.
