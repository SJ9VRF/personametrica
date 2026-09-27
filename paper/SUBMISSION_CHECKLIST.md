# Submission checklist — paper-first v3

## Scientific claim

- [x] One primary thesis: long-horizon personalization evaluation should couple state belief to downstream action risk.
- [x] Strong structured baselines including time-aware latest state.
- [x] Dev/test separation for PBS hyperparameter selection.
- [x] Threshold-free risk–coverage metric.
- [x] Utility sensitivity analysis.
- [x] Standard + high-noise + implicit-heavy + temporary-heavy + 800-turn regimes.
- [x] Ten-seed held-out standard statistics.
- [x] Ten-seed held-out long-horizon ranking analysis.
- [ ] Frontier/open-model end-to-end results — requires real model execution.
- [ ] Independent human labels — requires actual annotators/participants.
- [ ] Real downstream user task — requires model/human execution.

## Related work

- [x] LongMemEval
- [x] PrefEval
- [x] HorizonBench
- [x] PerMemBench
- [x] ProactiveBench
- [x] UserVille / PPP
- [x] MemoryBank
- [x] Generative Agents

## Reproducibility

- [x] Dataset generator and exported benchmark.
- [x] Exact configuration and seeds.
- [x] Baselines executable from source.
- [x] Figures generated from checked-in JSON.
- [x] Croissant-style dataset metadata.
- [x] Data card with limitations/biases/privacy.
- [x] Anonymous paper PDF + TeX + BibTeX.
- [x] Annotation UI and scoring code.
- [x] External model output schema/evaluator.

## Double blind

The anonymous paper PDF contains no author identity. Camera-ready author metadata is stored separately and should not be included in an anonymous submission bundle.
