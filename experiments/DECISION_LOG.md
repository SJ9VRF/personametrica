# Decision Log

Format: **Decision → Alternatives → Evidence → Trade-off → Outcome**.

## D-001 — Use shared development-only calibration before comparing action utility
**Decision.** Fit calibration on development seeds only and freeze it before held-out evaluation.  
**Alternatives.** Compare raw confidence directly; tune thresholds on test; ignore confidence and report accuracy only.  
**Evidence.** Raw-vs-calibrated ranking reversal in `data/calibration_protocol_analysis.json`.  
**Trade-off.** Adds protocol complexity and still requires choosing an action threshold/cost model.  
**Outcome.** Shared calibration became mandatory for fixed-threshold utility; unmatched native utility is diagnostic only.

## D-002 — Keep AURC/risk–coverage alongside action utility
**Decision.** Report threshold-free confidence ordering rather than selecting one “best” operating point.  
**Alternatives.** Only fixed-threshold utility; only state accuracy.  
**Evidence.** PBS AURC 0.0107 vs time-aware-latest 0.0208 while calibrated fixed-threshold utility orders them differently.  
**Trade-off.** AURC is less directly tied to one product cost model.  
**Outcome.** The paper distinguishes state correctness, confidence quality, and operating-point utility.

## D-003 — Replace self-reported verification with causal verification
**Decision.** Recompute success from expected/observed state and enforce action timing, allowed tool/action, live permission, and full-target verification.  
**Alternatives.** Trust `success=true`; verify only final state; verify only that a trace event exists.  
**Evidence.** Frozen robust grader false-accepted 96% of held-out attack families.  
**Trade-off.** More evaluator logic and stricter trace schema.  
**Outcome.** Causal grader rejected all authored held-out attacks while preserving the original gold suite.

## D-004 — Do not train on all generated correction pairs as if they were diverse data
**Decision.** Audit semantic-template duplication and keep task-disjoint train/dev/test splits.  
**Alternatives.** Treat every exact-unique pair as independent training signal; random row split.  
**Evidence.** 254 exact-unique pairs but 98.4% semantic-template duplication.  
**Trade-off.** Smaller effective dataset and weaker headline.  
**Outcome.** Structured correction records are kept; post-training improvement remains unclaimed.

## D-005 — Seed-scope synthetic identities
**Decision.** Encode seed in synthetic `user_id`s and audit full-history hashes with identifiers removed.  
**Alternatives.** Reuse display IDs across splits because current deterministic trackers do not learn identity embeddings.  
**Evidence.** Benchmark-health audit and future model-backed leakage risk.  
**Trade-off.** Slightly noisier identifiers and migration of checked-in artifacts.  
**Outcome.** Development/test identity overlap and full-history overlap are both zero.

## D-006 — Treat the leaderboard as an evaluated object, not a single answer
**Decision.** Freeze a 75-cell protocol registry and report winner counts, winner-change probability, Kendall tau, bootstrap uncertainty, and leave-one-level-out sensitivity.  
**Alternatives.** Pick one threshold/calibration/cost combination; report a pairwise comparison only.  
**Evidence.** Three systems win at least one cell; pairwise protocol winner change 51.6%; worst-case Kendall tau 0.20.  
**Trade-off.** Harder story, less “one winner” marketing.  
**Outcome.** PersonaMetrica's central contribution became protocol-sensitive model selection rather than a method leaderboard claim.

## D-007 — Narrow novelty instead of claiming “first personalization benchmark”
**Decision.** Position PersonaMetrica around protocol-sensitive ranking + evaluator validity + counterfactual personal-state checks.  
**Alternatives.** Claim first long-horizon personalization benchmark / first evolving-preference benchmark / first trajectory grader.  
**Evidence.** 2025–2026 closest-work audit in `reports/NOVELTY_SOTA_AUDIT.md`.  
**Trade-off.** Narrower novelty statement.  
**Outcome.** More defensible paper and hiring narrative.

## D-008 — Refuse to invent unavailable external results
**Decision.** Add adapters and schema smoke tests, but leave frontier/open-weight and human results as NOT RUN until actually executed.  
**Alternatives.** Fill tables with synthetic proxies or infer missing confidence.  
**Evidence.** `external_benchmarks/HORIZONBENCH_ADAPTER.md` and release claim boundaries.  
**Trade-off.** Some tables remain incomplete.  
**Outcome.** External validity remains an explicit next experiment rather than a fabricated accomplishment.
