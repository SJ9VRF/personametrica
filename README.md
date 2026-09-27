# PersonaMetrica

> **Stress-Testing Evaluation Protocols for Long-Horizon Personal Agents**

**Aura Yavary · 2026 · v4.1.0**

PersonaMetrica is an evaluation-science project for a specific failure mode in personalized agents: **the apparent winner can change when confidence calibration, action thresholds, or the evaluator itself changes.** The project separates evolving user-state estimation from action gating, then treats the grader as another fallible component that must be calibrated, attacked, versioned, and audited.

The benchmark component, **PersonaMetrica-Bench**, contains controlled long-horizon preference evolution, temporary scope, noisy implicit evidence, provenance, distractors, calibration tests, counterfactual interventions, multi-tool trajectories, and held-out grader attacks. The broader repository contains the executable personal-agent substrate used to generate and verify those behaviors.

**Paper:** [`paper/personametrica_anonymous.pdf`](paper/personametrica_anonymous.pdf)  
**Manuscript:** [`paper/PAPER.md`](paper/PAPER.md)  
**Benchmark:** [`data/personametrica_bench.jsonl`](data/personametrica_bench.jsonl)  
**Novelty audit:** [`reports/NOVELTY_SOTA_AUDIT.md`](reports/NOVELTY_SOTA_AUDIT.md)  
**Agent-eval reliability:** [`reports/GRADER_RELIABILITY.md`](reports/GRADER_RELIABILITY.md)  
**Systems demo:** [`project/index.html`](project/index.html)  
**NeurIPS readiness:** [`docs/NEURIPS_READINESS.md`](docs/NEURIPS_READINESS.md)

## Paper result in one paragraph

The central result is about **evaluation protocol sensitivity**. On the controlled PersonaMetrica-Bench benchmark, PBS has stronger standard state accuracy, calibration, and AURC than a strong time-aware symbolic baseline. But in 800-turn histories, the apparent fixed-threshold utility advantage under native confidence **reverses after every tracker receives the same development-only post-hoc calibration**: calibrated utility is 0.588 for PBS versus 0.687 for time-aware-latest, while PBS still has better selective accuracy and slightly better Brier. Therefore neither raw state accuracy nor fixed-threshold utility on unmatched confidence scales is a safe standalone selection criterion. The paper recommends a reporting stack of **state accuracy + calibration + risk–coverage/AURC + utility under an explicitly shared calibration/action protocol**.

The result is deliberately scoped. PersonaMetrica-Bench begins from structured evidence; it does **not** establish natural-language extraction quality, human-population validity, or frontier-model gains. Human annotation and external-model interfaces are included, but results remain unclaimed until those experiments are actually run.

## What is new in v4.1.0

v4.1 is a **flagship project-page and hiring-surface release**, not a new scientific SOTA claim. The underlying paper findings are unchanged; the public artifact is reorganized so a reviewer can understand and verify the work without digging through the repository.

- **Exact 14-part homepage contract:** Hero → Why it matters → Core idea → Architecture → My contribution → Experiments → Results → Failure analysis → Interactive demo → Scaling → Safety/limitations → Technical deep dive → Artifacts → Citation.
- **60-second Hero contract:** the first screen now states the problem, Aura Yavary's contribution, the main result, and the executable proof path. The first five CTAs are exactly **Paper / Code / Demo / Benchmark / Video**.
- **Research-first experiments:** the page now foregrounds the checked paper setup: 500 synthetic long-horizon users, 27,133 observations, 13,500 queries, six systems, 75 frozen evaluation protocols, ten long-horizon test seeds, 2,000 paired seed bootstraps, 800 gold trajectories, held-out grader attacks, and 540 counterfactual belief interventions.
- **Results at two levels:** the primary leaderboard-stability / seed-uncertainty / evaluator-OOD findings appear first; local mechanism sanity checks remain visible below. A separate baseline→method snapshot reports personalization/proactivity/recovery together with measured local latency and external API cost scope.
- **Failure analysis that explains causes:** the page surfaces belief contamination, grader overfit, metric pathology, what cannot be auto-recovered, and one concrete verifier-guided retry trajectory that does recover.
- **Architecture loops made explicit:** agent loop, recovery loop, and eval/post-training loop are named on-page, with a clear boundary that training-ready correction data are implemented but no completed frontier-model post-training result is claimed.
- **Scaling contract:** model-size boundary, task horizon, tool count, interaction count, latency, cost, and robustness are all explicit rather than scattered across reports.
- **GitHub without fabrication:** the Artifacts section includes a GitHub release handoff document, but no public repository URL is invented before a real repository exists.
- **Hard release gate:** `scripts/project_page_qa.py` now enforces the 14-part numbering, Hero contract, five primary CTAs, architecture loops, ownership, results fields, recovery explanation, scaling fields, artifact inventory, citation, accessibility, and local-link integrity.

## 60-second executable reviewer path

```bash
python scripts/reviewer_demo.py
```

This validates the frozen protocol fingerprint, benchmark-health gates, full-leaderboard instability artifacts, seed-bootstrap support, all 13 grid perturbations, and then reruns two live mechanisms: the held-out causal-grader attack suite and a temporal preference update. See [`reports/REVIEWER_DEMO.md`](reports/REVIEWER_DEMO.md).

A separate clean-interpreter check is available via `python scripts/cold_start_audit.py`; see [`reports/COLD_START_AUDIT.md`](reports/COLD_START_AUDIT.md). The public claim contract is [`docs/EVIDENCE_LEDGER.md`](docs/EVIDENCE_LEDGER.md).

## Reviewer path

**60 seconds:** `python scripts/reviewer_demo.py` + [`reports/REVIEWER_DEMO.md`](reports/REVIEWER_DEMO.md).  
**5 minutes:** [`reports/LEADERBOARD_STABILITY_AUDIT.md`](reports/LEADERBOARD_STABILITY_AUDIT.md), [`reports/LEADERBOARD_SEED_UNCERTAINTY.md`](reports/LEADERBOARD_SEED_UNCERTAINTY.md), [`reports/PROTOCOL_GRID_ROBUSTNESS.md`](reports/PROTOCOL_GRID_ROBUSTNESS.md), and [`reports/NOVELTY_SOTA_AUDIT.md`](reports/NOVELTY_SOTA_AUDIT.md).  
**15 minutes:** [`paper/PAPER.md`](paper/PAPER.md), [`reports/RELATED_WORK_POSITIONING.md`](reports/RELATED_WORK_POSITIONING.md), and [`docs/NEURIPS_READINESS.md`](docs/NEURIPS_READINESS.md).  
**Systems/portfolio view:** [`project/index.html`](project/index.html).

---

The remainder of this repository is the **PersonaMetrica systems substrate** used for longitudinal memory, calibrated intervention, tool verification, evaluator attacks, failure analysis, and failure-to-data experiments. Its controlled mechanism tests are useful engineering regressions, but they are not the main scientific evidence for the PersonaMetrica-Bench paper.

## Flagship project page

The reviewer-facing project homepage is `project/index.html`. It follows a 14-part research-project flow: hero, problem, core idea/novelty, architecture, contribution, experiments, results, failure analysis, interactive trajectory demo, scaling, safety/limitations, technical deep dive, artifacts, and citation. It is static, mobile-responsive, keyboard-accessible, has no third-party runtime dependencies, and is release-gated by `python scripts/project_page_qa.py`. The exact contract is documented in `docs/PROJECT_PAGE_SPEC.md`; `make page-qa` currently enforces 134 structural, evidence, accessibility, and artifact-integrity checks.

## Project homepage

Open **`project/index.html`** for the standalone project page designed for a 60-second hiring-manager review. It includes the hero claim, problem/novelty, architecture, contribution, experiments, results, failure analysis, interactive trajectory, measured scaling, safety boundaries, technical deep dives, artifact links, demo video, and BibTeX citation.

## Why this project exists

Most assistant demos optimize one turn at a time. Personal intelligence is longitudinal: the system must distinguish current preferences from stale ones, preserve uncertainty and provenance, decide when *not* to intervene, verify actions in the world, and improve without trading away truthfulness or autonomy.

The central question is:

> **Can a personal agent become more useful over time without becoming stale, intrusive, overconfident, or wrong?**

## Implemented system

```text
User / World
    ↓
Interaction Event
    ↓
Temporal Personal World Model
    ├── structured memory + provenance
    ├── confidence + stability
    ├── supersession + contradiction handling
    ├── conditional preferences
    └── goal state
    ↓
Calibrated Proactivity Policy
    ├── urgency / relevance
    ├── confidence
    ├── stakes / reversibility
    ├── autonomy preference
    └── interruptibility
    ↓
Planner → Safe Tool Sandbox → Outcome Verification
    ↓
Structured Feedback → Multi-objective Reward
    ↓
PersonalBench → Failure Mining → Preference Training Data
```

## What is implemented, and what is not

Implemented and executed:

- temporal preference update and history
- cross-session JSON snapshots with schema-versioned restore of memory, goals, events, feedback, audit history, and sandbox tool state
- stale-memory and contradiction evaluation
- confidence-aware memory records
- goal capture, completion/abandonment lifecycle, and deterministic decomposition
- calibrated `ask / suggest / remind / wait / none` policy
- autonomy and high-stakes confirmation tests
- deterministic tool sandbox and outcome verifier
- feedback and auditable multi-objective reward vector
- synthetic longitudinal simulator with preference drift
- 200-scenario proactivity benchmark
- real feature-toggle ablations
- bootstrap confidence intervals for per-user memory metrics
- paired 10-seed effect analysis with bootstrap 95% intervals
- slice-based failure analysis over 1,000 proactivity scenarios
- conditional-preference, adversarial-language, privacy/user-control, and goal-lifecycle benchmarks
- 6,000-row synthetic interaction dataset
- 724 unique validated preference pairs for local post-training experiments
- dashboard, app demo, research/system reports
- full one-command reproduction

Not claimed:

- no invented human-study outcome
- no claim of training a frontier model
- no claim that the local sparse linear reward baseline is a frontier/semantic reward model
- no live actions on user accounts
- no synthetic metric presented as production evidence

## Reproduce everything

Requires Python 3.11+ and `pytest` for tests.

```bash
python scripts/reproduce.py
```

That command runs:

```text
63 tests
→ 100-user × 60-turn longitudinal benchmark
→ 6,000-row PersonalBench dataset
→ 724 unique validated preference pairs
→ real feature-toggle ablations
→ multi-seed robustness + 10-seed paired statistical analysis
→ measured scaling/runtime profile
→ evaluation dashboard + SVG research assets
→ standalone project homepage + interactive trajectory + demo video
→ result summary + SHA-256 manifest
→ app benchmark refresh
→ release validation
```

Individual commands:

```bash
python demo.py
python -m personalagi demo
python -m personalagi eval --users 100 --turns 60 --seed 7
python -m pytest -q
python evals/run_eval.py --users 100 --turns 60 --seed 7
python data/generate_dataset.py --users 100 --turns 60
python experiments/build_preference_data.py
python experiments/run_ablations.py
python scripts/robustness.py
python scripts/statistical_analysis.py
python scripts/failure_analysis.py
python dashboard/build_dashboard.py
python scripts/release_check.py
```

## Installable CLI

The repository is also a standard Python package. From the repository root:

```bash
pip install -e .
personametrica demo
personametrica eval --users 100 --turns 60 --seed 7
# legacy alias remains available: personal-agi-os
```

The core runtime intentionally has zero third-party dependencies; `pytest` is only required for development/testing.

## Current controlled results

The checked-in `data/eval_results.json` was generated with seed 7 using 100 synthetic users × 60 turns and 200 proactivity scenarios.

| Mechanism | Full system | Ablated system |
|---|---:|---:|
| personalization accuracy | 100.0% | 37.1% without temporal update |
| stale-memory rate | 0.0% | 62.9% without temporal update |
| active contradiction rate | 0.0% | 82.0% without conflict resolution |
| proactive decision accuracy | 86.5% | 17.0% uncalibrated |
| autonomy-violation rate | 0.0% | 5.9% uncalibrated |
| low-value non-interruption | 100.0% | 100.0% uncalibrated |
| outcome-failure detection | 100.0% | 0.0% without verifier |
| memory-confidence Brier error ↓ | 0.000 | 0.070 without confidence tracking |
| adversarial preference-language accuracy | 93.3% | — |
| goal lifecycle accuracy | 100.0% | 0.0% without goal model |
| sensitive-memory block rate | 100.0% | 0.0% without privacy guard |

These numbers are intentionally interpreted narrowly: the benchmark is designed to test the repository's mechanisms. See `reports/RESULTS.md` and `reports/RESEARCH_REPORT.md`.

## Real ablations

Ablations are not post-hoc metric edits. Each variant changes an actual system feature:

- `no_temporal_update`: first learned value remains active
- `stateless`: no memory is written
- `no_contradiction_resolution`: conflicting values remain active simultaneously
- `no_goal_model`: extracted goals are not added to goal state
- `uncalibrated_proactivity`: policy ignores uncertainty/stakes-specific safeguards
- `no_confidence_tracking`: all extracted memories receive confidence 1.0
- `no_outcome_verification`: action results are returned without verification
- `no_privacy_guard`: obvious sensitive-memory candidates are no longer blocked


## Learned-model adapter boundary

The checked-in benchmark uses a transparent deterministic estimator for reproducibility, but the runtime is not tied to it. `personalagi/adapters/` defines a structured inference contract. `ReplayInferenceAdapter` can take saved JSON outputs from any external learned model and run those outputs through the exact same memory, privacy, goal, persistence and evaluation machinery. See `examples/replay_model_outputs.py`.

This separation makes model-backed experiments comparable without requiring a live API for reproduction.

## Behavioral regression gates

`configs/regression_gates.json` defines minimum/maximum acceptable values for core behaviors (personalization, stale memory, contradiction, autonomy, high-stakes confirmation, forgetting, privacy, verification and adversarial-language accuracy).

```bash
python scripts/regression_gate.py
```

The gate is part of both the one-command reproduction pipeline and release validation. A release fails rather than silently shipping a behavioral regression.

## Repository map

```text
personalagi/        agent, schemas, memory, goals, policy, tools, verifier, reward
personalbench/      personas, scenarios, metrics, benchmark runner
configs/            configuration + behavioral regression gates
evals/              evaluation entry point
experiments/        ablations, preference-data creation, research log
data/               generated benchmark artifacts
scripts/            full reproduction + generated summaries
app/                user-facing static inspection demo
dashboard/          research-facing benchmark dashboard
reports/            results, system design, dataset/model cards, study protocol
paper/              paper draft
 tests/              unit, integration, ablation, reproducibility tests
```

## Research artifacts

- `paper/PAPER.md` — paper-style technical manuscript
- `reports/RESULTS.md` — generated result summary
- `reports/RESEARCH_REPORT.md` — experiments, interpretation, limitations
- `reports/ROBUSTNESS.md` — multi-seed robustness analysis
- `reports/STATISTICAL_ANALYSIS.md` — paired 10-seed effect estimates and bootstrap intervals
- `reports/FAILURE_ANALYSIS.md` — slice-level diagnostics and representative policy errors
- `reports/ADVERSARIAL_EVAL.md` — language-form stress evaluation
- `reports/PRIVACY_USER_CONTROL.md` — persistence privacy, forgetting, and audit evaluation
- `docs/EVIDENCE_LEDGER.md` — claim-to-evidence map and explicit evidence boundaries
- `reports/SYSTEM_DESIGN.md` — architecture and engineering tradeoffs
- `reports/DATASET_CARD.md` — synthetic data specification
- `reports/MODEL_SYSTEM_CARD.md` — intended use and failure modes
- `reports/HUMAN_STUDY_PROTOCOL.md` — unexecuted next-stage validation protocol
- `reports/REPRODUCIBILITY.md` — exact reproduction instructions
- `reports/RESEARCH_TALK.md` — 8–10 minute talk outline
- `docs/architecture.svg` — generated architecture figure
- `docs/results.svg` — generated benchmark figure
- `docs/PORTFOLIO_COPY.md` — project-page copy
- `docs/DEMO_SCRIPT.md` — three-minute demo script
- `docs/RELEASE_CHECKLIST.md` — release audit

## Cross-session persistence

The local research agent can save and restore temporal state without an external database:

```python
agent.save_snapshot("state.json")
restored = PersonalAGIAgent(agent.state.user_id)
restored.load_snapshot("state.json")
```

Snapshots preserve current beliefs, superseded memory history, goals, interaction style, provenance, interaction events, feedback history, memory audit events, and deterministic sandbox tool state. User-ID mismatch and unsupported schema versions fail closed.

## User-facing demo

Open `app/index.html`. It exposes the product surfaces that matter for trustworthy personalization:

- Chat
- Memory: current / changed / uncertain
- Goals
- Why: structured decision factors, not hidden chain-of-thought
- Feedback
- Evolution

Open `dashboard/index.html` for the research view and ablation comparison.

## Design principles

1. **Current state beats stale history.** History is preserved, not silently erased.
2. **Uncertainty is data.** Inferred or tentative preferences should not be treated like explicit durable facts.
3. **Personalization is not agreement.** User adaptation must not override truthfulness.
4. **Proactivity is a calibration problem.** Benefit must be balanced against interruption, stakes, reversibility, and autonomy.
5. **Actions require verification.** A tool call is not success until its outcome matches the intended state.
6. **Every improvement needs a regression surface.** Gains in personalization should be checked against memory errors and autonomy failures.

## Next empirical layer

The repository is intentionally ready for two extensions without redesigning the surrounding system:

- plug a model-backed extractor/policy or LoRA/DPO training job into the existing interfaces;
- execute the preregistered human longitudinal study and replace synthetic-only evidence with human measurements.

Until those runs exist, this repository keeps their outputs explicitly labeled as future work.

## v1.4: learned post-training baseline

The post-training path now includes a **real learned baseline**, not only exported preference pairs. `scripts/train_reward_baseline.py` trains an auditable pairwise linear reward/ranking model with logistic SGD using only the Python standard library.

```bash
python experiments/build_preference_data.py
python scripts/audit_training_data.py
python scripts/train_reward_baseline.py
```

The checked-in v1.4 run contains **724 unique validated preference pairs** across temporal memory, privacy/user control, uncertainty calibration, high-stakes autonomy, low-value proactivity, and reversible assistance. Exact duplicates are removed before export.

The learned lexical baseline reaches 1.00 pairwise accuracy on the structured held-out set, while a randomized-label negative control is ~0.49 and a deliberately lexically matched contrast set is **0.50**. That contrast failure is intentional evidence: the local baseline learns the synthetic preference signal, but it does not solve compositional semantics. See `reports/LEARNED_REWARD_BASELINE.md` and `reports/TRAINING_DATA_AUDIT.md`.

This closes the local training loop as:

```text
failures / scenarios
→ validated preference pairs
→ deduplication + audit
→ learned reward/ranking baseline
→ held-out evaluation + negative controls
→ regression/evidence reports
```

It still does **not** claim LLM reward-model quality, DPO/RL improvements on a foundation model, or human preference validity.

## v1.5: leakage-aware reward evaluation

The lexical reward baseline is now evaluated under deliberately stronger conditions. The standard group-aware split still reaches 1.00 pairwise accuracy, but a leakage audit shows that **98.6% of test rows reuse an exact normalized chosen/rejected response pair seen in training**. That number is now part of the release evidence rather than hidden behind the 1.00 headline.

Additional checks:

```bash
python scripts/reward_generalization_eval.py
```

The checked-in v1.5 run reports:

- standard test pairwise accuracy: **1.000**
- bidirectional calibration Brier: **0.072**
- bidirectional ECE: **0.260**
- leave-one-family-out macro accuracy: **1.000**
- unseen response-paraphrase accuracy: **0.667**

The family-holdout result shows that the lexical signals shared across behavioral families are strong; the paraphrase drop is the more important warning that semantic generalization is not solved. See `reports/REWARD_GENERALIZATION.md` and `docs/BENCHMARK_SPEC.md`.

Release provenance is also stricter in v1.5: `pyproject.toml` is the version source of truth and release validation fails if `CITATION.cff`, `MANIFEST.json`, or `CHANGELOG.md` disagree.