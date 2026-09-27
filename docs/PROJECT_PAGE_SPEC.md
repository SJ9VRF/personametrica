# Flagship Project Page Specification

The project page is a first-class research artifact. It must let a hiring manager understand the problem, the author's contribution, the main result, and whether the system actually works in roughly 60 seconds without reading the paper.

## Required structure

1. **Hero** — project name, one-sentence problem, one primary result, and `Paper / Code / Demo / Benchmark / Video`.
2. **Why this problem matters** — problem, difficulty, and why current approaches fail.
3. **Core idea** — 2–3 sentence idea and explicit novelty.
4. **Architecture** — main system diagram plus agent, recovery, and training/post-training loops.
5. **My contribution** — what Aura Yavary designed, implemented, and which technical decisions she owned.
6. **Experiments** — tasks/data, baselines, ablations, setup.
7. **Results** — clean baseline→method comparison plus success/recovery/latency/cost scope.
8. **Failure analysis** — real failures, causes, and whether/how the system recovered.
9. **Interactive demo** — runnable/inspectable task trajectory.
10. **Scaling** — model-size boundary, task horizon, tool count, latency/cost, robustness.
11. **Safety / limitations** — failure boundaries, irreversible actions, permission boundaries, human escalation.
12. **Technical deep dive** — engineering report, training/post-training detail, evaluation methodology.
13. **Artifacts** — Paper, GitHub/Code, Benchmark, Dataset, Demo, Video, Technical report, Blog post.
14. **Citation** — BibTeX, authors, year, release version.

## 60-second acceptance test

Before release, the Hero must answer four questions without scrolling deeply: **What problem? What did Aura contribute? What is the result? Does it actually work?**

The automated `scripts/project_page_qa.py` turns this specification into a release gate so future edits cannot silently remove a required section or artifact.

## Required Evidence Layer beneath the 14-part page

After the polished 14-part narrative, every flagship project must expose an **Inside the research process** layer with:

1. experiment journal with hypothesis / setup / result / interpretation / next decision;
2. failed experiments / revised hypotheses;
3. decision log in Decision → Alternatives → Evidence → Trade-off → Outcome format;
4. real evaluation tables with seed/N/CI scope when actually available;
5. unexpected findings that changed the project;
6. honest Git history policy — never backdate or synthesize earlier commits;
7. raw artifacts: eval runs, failure examples, plots, configs, qualitative cases, and ablations.

The layer must link to executable evidence and reproduction, not just prose. `scripts/evidence_layer_audit.py` and `scripts/project_page_qa.py` release-gate this contract.
