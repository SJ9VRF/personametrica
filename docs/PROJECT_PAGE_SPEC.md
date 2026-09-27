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
