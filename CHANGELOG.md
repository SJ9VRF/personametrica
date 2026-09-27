# Changelog

## v4.2.0 — Evidence Layer and honest research history

- Added a 13-entry experiment journal with hypothesis, setup, result, interpretation, next decision, and canonical evidence path.
- Added seven failed/revised hypotheses, eight decision records, seven unexpected findings, and three end-to-end research-process traces.
- Added a self-contained `artifacts/` tree with raw eval outputs, failure examples, plots, frozen configs, trajectories, and ablations.
- Added real evaluation tables that retain N/seeds/CI and scope boundaries instead of reducing the project to one hero metric.
- Added an unnumbered `Inside the research process` homepage layer beneath the polished 14-part project narrative.
- Added `scripts/evidence_layer_audit.py` plus homepage/release gates so the layer cannot silently disappear or drift from canonical outputs.
- Started a real Git history from the imported v4.1 release snapshot and committed v4.2 work incrementally; no earlier history is fabricated or backdated.
- Added a reusable Evidence Layer contract for the other flagship projects.

## v4.1.0 — Flagship Project Page Contract

- Enforces the full 14-part project-page structure from Hero through Citation.
- Puts Paper / Code / Demo / Benchmark / Video first in the Hero and adds a 60-second problem / contribution / result / proof strip.
- Expands architecture into explicit agent, recovery, and eval/post-training loops.
- Adds a baseline-to-method result snapshot with measured latency and external-API-cost scope.
- Adds concrete failure-root-cause and verified-recovery explanation.
- Makes model-size, task-horizon, tool-count, latency/cost, and robustness scope explicit.
- Adds a GitHub release handoff without fabricating a public repository URL.
- Extends automated project-page QA so removal of any required section or artifact fails release.


## v4.0.0 — reviewer trust and cold-start release

- Added a sub-second `scripts/reviewer_demo.py` that verifies headline evidence and reruns live temporal-update and held-out causal-grader mechanisms.
- Added a fresh-venv cold-start execution audit with explicit reporting of whether a true editable install or stdlib path isolation was available.
- Rebuilt the Evidence Ledger as a public claim contract: every headline claim maps to checked evidence, a fast executable check, and a boundary.
- Added `docs/FRONTIER_RESEARCH_BRIEF.md` and `docs/HIRING_PACKET.md` for 60-second / 5-minute / 15-minute review paths.
- Added a release-gated hiring-surface audit for author/version consistency, claim boundaries, placeholders, and reviewer-demo links.
- No new scientific SOTA claim is introduced in v4.0; this release hardens inspectability, reproducibility, and hiring-manager trust.

## v3.9.0 — statistical decision robustness and external-result contract

- Added a 2,000-replicate paired bootstrap over long-horizon simulator seeds on a separate 10-user-per-seed diagnostic cohort. Winner-change probability is 0.516 with a 95% seed-bootstrap interval of [0.507, 0.538]; mean Kendall tau is 0.702 [0.692, 0.720].
- Added 13 leave-one-level-out protocol-grid perturbations covering calibration families, thresholds, and deferral costs. Every perturbation retains multiple winners; winner-change probability ranges 0.327–0.564.
- Added an executable adapter for the official HorizonBench per-item result JSONL schema with explicit refusal to invent missing confidence; checked-in rows are synthetic schema fixtures only and are not external benchmark results.
- Added release gates and regression tests for seed uncertainty, grid robustness, and external-result claim boundaries.
- Updated the paper, hiring-manager README, homepage, anonymous bundle, reproduction path, and release summary to report uncertainty rather than only point estimates.

## v3.8.0 — full-leaderboard stability and benchmark-health release

- Extended protocol sensitivity from one pair to all six released baselines across the same 75 frozen protocol cells.
- Added winner-change probability, complete-ranking Kendall tau, rank variance, winner entropy, and pairwise reversal diagnostics.
- Found that time-aware-latest wins 45 cells, PBS 27, and first-mention 3; two protocol cells select different winners 51.6% of the time.
- Added seed-scoped synthetic identities so development and held-out cohorts cannot share display IDs.
- Added a release-gated benchmark health audit covering exact dev/test stream overlap, duplicate histories, query/domain balance, temporary-scope coverage, answer imbalance, and saturation.
- Updated 2026 positioning for PIPE and SEAGym, further narrowing novelty claims around protocol perturbation and multi-view agent evaluation.
- Updated paper, hiring-manager path, homepage, anonymous bundle, reproduction pipeline, and release gates for the new evidence.

## v3.6.0 — PersonaMetrica novelty-audited research release

- Renamed the public research artifact to **PersonaMetrica: Stress-Testing Evaluation Protocols for Long-Horizon Personal Agents**.
- Audited 2025–2026 closest work and removed broad novelty claims around personalized memory, evolving preferences, and proactivity.
- Reframed the defensible contribution around ranking stability under shared calibration/action protocols and evaluator validity under held-out attacks.
- Added `reports/NOVELTY_SOTA_AUDIT.md` with closest-work comparison, claim boundaries, name audit, and explicit requirements for any future external SOTA claim.
- Reworked the public project page so protocol sensitivity and grader generalization—not a legacy personalization-gain number—are the first-screen evidence.
- Added canonical PersonaMetrica aliases for the anonymous paper, benchmark data/metadata, and submission bundle while retaining legacy internal filenames for reproducibility.
- Public author metadata is **Aura Yavary**; anonymous review artifacts remain identity-free.

# Changelog

## v3.4.0 — evaluator reliability, multi-tool traces, and calibration workflow

- Expanded the controlled agent-eval suite to reminders, notes, and tasks with explicit tool+action contracts.
- Expanded to 80 tasks × 10 trials = 800 trajectories covering ten perturbations, including wrong-action and partial-state failures.
- Added an evidence-aware grader that abstains on missing critical observations rather than fabricating certainty.
- Added a dense, auditable trajectory reward diagnostic with dimension-level scores.
- Added grader metamorphic tests, score calibration metrics, composite-threshold drift, and repeated-trial uncertainty analysis.
- Added a prioritized grader-disagreement queue and blinded trajectory-annotation pack for independent human calibration.
- Added content fingerprints binding results to the exact evaluator implementation.
- Added structured failure corrections, task-disjoint train/dev/test splits, and an audit showing the current text corrections remain highly templated.
- Corrected stale paper/README wording so unmatched native-confidence utility is explicitly diagnostic; shared-calibration protocol sensitivity remains the scientific headline.

## v3.3.0 — trajectory-aware eval and grader-gaming hardening

- Added a task/trial/grader/trajectory agent-evaluation layer with 80 tasks and 640 controlled trials.
- Added end-state, trajectory-policy, composite, and evidence-recomputing robust graders.
- Added unsafe-shortcut, missing-verification, wrong-tool, redundant-loop, false-claim, and forged-verification perturbations.
- Added failure-driven conversion of grader false accepts into 280 post-training-ready correction pairs.
- Added a runtime grader-ready trace path for verified bounded recovery.
- Added a small reward-hacking diagnostic contrasting satisfaction-only and multi-objective selection.
- Added an OpenAI/Anthropic research-readiness audit while keeping frontier-model/human results explicitly unclaimed.

## v3.2.0 — PersonaMetrica-Bench paper-first research release

- Added equal-opportunity post-hoc confidence calibration for every tracker on development seeds only.
- Found and documented a calibration-induced long-horizon utility ranking flip: native confidence favors PBS, while dev-calibrated fixed-threshold utility favors time-aware-latest.
- Promoted risk–coverage/AURC and explicit calibration protocol as the primary decision-risk comparison; demoted unmatched native-confidence utility to a diagnostic.
- Added exact metric definitions, claim-to-evidence matrix, calibration protocol appendix, and a page-budget audit path.
- Compressed the main manuscript so the generic draft reaches References on page 9 (8 content pages before references), leaving margin for the official 9-page NeurIPS limit.
- Reframed the scientific contribution around belief updating and decision risk in long-horizon personalization.
- Added Personal Belief State (PBS), six executable baselines, noisy implicit evidence, temporary scope, distractors, and 800-turn stress tests.
- Added development-only hyperparameter selection and held-out 10-seed statistical evaluation.
- Added threshold-free risk–coverage/AURC analysis and utility sensitivity across confidence thresholds and defer costs.
- Added PersonaMetrica-Bench export, data card, Croissant-style metadata, human-annotation pack, and external-model evaluation contract.
- Added related-work positioning against LongMemEval, PrefEval, HorizonBench, PerMemBench, ProactiveBench, UserVille, MemoryBank, and Generative Agents.
- Added an anonymous submission-style manuscript, bibliography, figures, and PDF build artifacts.
- No human-participant or frontier-model result is claimed unless actually executed.

## v2.0.0 — Human-reviewed portfolio release

- Rewrote the flagship page for a restrained, researcher/engineer voice rather than template-like portfolio copy.
- Reduced first-screen metrics to the evidence a hiring manager can interpret quickly; synthetic 100% mechanism scores remain in the detailed results section with scope labels.
- Reframed contribution language around concrete design choices, implementation ownership, and limitations.
- Reworked the project page into an editorial research layout with clearer hierarchy and fewer decorative signals.
- Added `docs/HIRING_MANAGER_README.md` as a concise reviewer path.
- Kept the 14-section project-page contract, reproducibility checks, and all research evidence intact.

## v1.9.0 — Final compliance audit

- Added a requirement-by-requirement project-page compliance matrix.
- Made the Results table explicitly report baseline→method, success/accuracy, recovery, latency, and external cost.
- Added a GitHub-ready release/publishing artifact without fabricating a public repository URL.
- Re-audited all 14 flagship project-page sections against the user-facing specification.

## v1.9.0 — Exact 14-section flagship-page compliance
- Renumbered the project page so Hero is section 01 and Citation is section 14.
- Added a 60-second Problem / Contribution / Result / Does-it-work proof strip to the Hero.
- Made agent, recovery, and training/post-training loops explicit in Architecture.
- Expanded My Contribution into designed / implemented / technical decisions owned.
- Added a baseline→method results table with success/recovery/latency/cost scope.
- Reworked Failure Analysis to show concrete cause and recovery status for each failure.
- Made model-size boundary explicit in Scaling and strengthened automatic page-compliance checks.

## v1.7.0 — Project-page production hardening

- Rebuilt the flagship project page around the requested 14-part reviewer flow.
- Added explicit novelty bullets, scaling facts (model path, horizon, tools, cost/latency, robustness), and human-escalation safety boundary.
- Added responsive result visualization, accessible keyboard/focus states, skip navigation, reduced-motion support, semantic landmarks, ARIA states, and screen-reader status messaging.
- Added Open Graph/Twitter metadata, JSON-LD scholarly/software metadata, web manifest, robots metadata, theme color, and deployment notes.
- Added automated project-page QA for required sections, local links, alt text, metadata, zero external runtime dependencies, and artifact integrity.
- Added headless Chromium desktop/mobile render smoke tests and checked-in preview screenshots for reviewer QA.
- Added static deployment guide and page QA report to the release gate.

## v1.6.0 — 2026-09-23

- Added a standalone hiring-manager project homepage with the full 14-part research/project narrative: hero, problem, novelty, architecture, contribution, experiments, results, failures, interactive demo, scaling, safety, deep dive, artifacts, and citation.
- Added an interactive trajectory generated by the real `PersonalAGIAgent` runtime.
- Added a bounded verified-retry recovery primitive and end-to-end recovery test.
- Added measured local scaling/runtime benchmarks across user counts and task horizons, with explicit cost/latency scope boundaries.
- Added a self-contained 36-second project walkthrough video and poster asset.
- Corrected public authorship metadata to Aura Yavary and strengthened project-page/release artifact validation.

## v1.5.0 — 2026-09-23

- Added reward-model leakage auditing; the standard split now explicitly reports canonical response-pair overlap.
- Added leave-one-family-out reward generalization, bidirectional calibration (Brier/ECE), and unseen-paraphrase stress evaluation.
- Added `docs/BENCHMARK_SPEC.md` and a concrete research threat model covering memory poisoning, stale state, over-autonomy, sensitive persistence, tool-result hallucination, and evaluation leakage.
- Made `pyproject.toml` the single source of truth for release versioning; manifest/CITATION/changelog mismatches now fail release validation.
- Upgraded GitHub CI to Python 3.11/3.12/3.13 plus behavioral-gate checks.
- Expanded release tests and required artifacts; preserved weak reward-baseline generalization as an explicit limitation rather than tuning it away.

## v1.4.0 — 2026-09-23

- Rebuilt preference-data generation to emit diverse metadata-tagged families and remove exact duplicate pairs before export.
- Added schema validation, deduplication, and a reproducible training-data quality audit.
- Added a real locally trained pairwise linear reward/ranking baseline using logistic SGD with no external ML dependency.
- Added group-aware train/validation/test splits, per-family metrics, a randomized-label negative control, and a lexically matched contrast set.
- Preserved the contrast-set failure (50% accuracy) as explicit evidence of the lexical baseline's semantic limitation rather than hiding it.
- Wired data audit and learned-baseline training into one-command reproduction and release validation.
- Expanded the test suite to 36 tests.

## v1.2.0 — 2026-09-23

- Added goal completion/abandonment lifecycle handling and benchmark.
- Added conservative persistent-memory privacy guard with a real no-guard ablation.
- Added memory lifecycle audit events for write, supersede, expire, and explicit forget.
- Made explicit forget commands atomic so they cannot immediately re-create the deleted preference.
- Added adversarial preference-language and temporal-reversal stress suites.
- Added conversational context carry-forward for elliptical preference updates.
- Upgraded snapshot schema to v2, restoring events, feedback, audit history, and sandbox tool state; v1 remains readable.
- Added adversarial, privacy/user-control, and claim-to-evidence reports.
- Expanded the release test suite from 24 to 31 tests.

## 1.3.0
- Added a pluggable inference-adapter contract so learned model outputs can enter the same runtime/eval stack.
- Added deterministic structured-output replay for offline model-backed experiments.
- Added behavioral regression gates with release-failing thresholds.
- Wired regression gates into full reproduction and release validation.
- Added reviewer and interview walkthrough guides plus a model-output replay example.

## v3.2.0 — submission-rigor hardening

- Added PBS component ablations on held-out seeds.
- Added 48-cell noise/temporary stress grid and explicit failure region.
- Added exact paired sign/sign-flip tests for primary held-out effects.
- Added benchmark integrity audit and corrected stale standard observation count (27,133).
- Added measured compute-resource report.
- Added all 15 NeurIPS checklist answers after references/appendix in the local draft.
- Added official-NeurIPS-2026-ready LaTeX source generator without fabricating the unavailable style file.
- Upgraded Croissant metadata to core 1.1 fields plus minimal RAI metadata; hosted reviewer URL remains an explicit external submission blocker.
- Added automated NeurIPS E&D submission-readiness checker separating local completeness from external hosting/style requirements.
