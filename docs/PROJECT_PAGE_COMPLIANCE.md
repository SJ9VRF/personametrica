# Project Page Compliance Matrix — PersonaMetrica v4.2.0

The homepage is a first-class hiring and research artifact. The release gate treats the following fourteen blocks as mandatory, not optional copy.

| # | Required block | Concrete evidence in the page |
|---:|---|---|
| 1 | Hero | `header#hero[data-section="01"]`; project name, one-sentence problem, main result, Aura Yavary, and the first five CTAs are Paper / Code / Demo / Benchmark / Video. A four-card 60-second strip states problem, contribution, result, and executable proof. |
| 2 | Why this problem matters | `#problem`; evolving-user state, difficulty, autonomy risk, and why naive memory/proactivity/reward approaches fail. |
| 3 | Core idea | `#idea`; protocol-sensitive model selection, evaluator-under-evaluation, counterfactual user-state checks, plus explicit non-claims. |
| 4 | Architecture | `#architecture`; main system diagram plus explicit agent loop, recovery loop, and eval/post-training loop. |
| 5 | My contribution | `#contribution`; research framing, implementation ownership, and named technical decisions owned by Aura Yavary. |
| 6 | Experiments | `#experiments`; datasets/tasks, baselines, ablations, robustness seeds, adversarial sequences, and setup scope. |
| 7 | Results | `#results`; baseline→method mechanism table plus a compact system-level snapshot with success/accuracy, recovery, measured local latency, and external API cost scope. |
| 8 | Failure analysis | `#failures`; visible failure cases, root-cause explanation, and a concrete verified recovery path from the runtime trajectory. |
| 9 | Interactive demo | `#demo`; inspectable trajectory with state, decision, tool action, verification, correction, retry, and embedded walkthrough video. |
| 10 | Scaling | `#scaling`; model-size boundary, task horizon, tool count, max interactions, measured latency/cost, and robustness scope. |
| 11 | Safety / limitations | `#safety`; irreversible actions, permission boundaries, user control, human escalation, and known limits. |
| 12 | Technical deep dive | `#technical`; engineering design, post-training baseline, eval methodology, threat model, statistics, evidence ledger, frontier research brief, and hiring packet. |
| 13 | Artifacts | `#artifacts`; Paper, Code, GitHub release handoff, Benchmark, Dataset, Demo, Video, Technical report, Blog post, and reproducibility/audit artifacts. |
| 14 | Citation | `#citation`; Aura Yavary, 2026, v4.2.0, copyable BibTeX. |

## Integrity boundary

The public page does **not** claim external leaderboard SOTA, frontier-model improvement, completed human validation, or completed frontier-model post-training. GitHub is represented by the release-ready handoff document until a real public repository URL exists; no URL is fabricated.

## Release enforcement

`scripts/project_page_qa.py` checks the exact 14-part numbering, the five primary Hero CTAs, the 60-second contract, architecture loops, ownership language, result-snapshot fields, failure/recovery explanation, scaling fields, artifact inventory, citation, accessibility, and local-link integrity. `scripts/release_check.py` runs that QA before a release can pass.

## Evidence Layer compliance

The unnumbered `#research-process` layer sits beneath the polished narrative and does not change the 14 numbered sections. It exposes 13 logged experiments, 7 failed/revised hypotheses, 8 major design decisions, 5 persistent failure modes, real eval tables, unexpected findings, raw artifacts, Git-history policy, and the reproduction path. `scripts/evidence_layer_audit.py` hash-checks copied eval outputs against canonical data files.
