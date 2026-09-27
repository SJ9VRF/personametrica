# Evidence Layer

PersonaMetrica keeps the polished paper/homepage separate from a lower-level research-process layer. The goal is evidence-rich research history, not manufactured messiness.

## Process snapshot

- **13** explicitly logged experiments with checked-in outputs.
- **7** failed or materially revised hypotheses.
- **8** major design decisions recorded with alternatives and trade-offs.
- **5** persistent failure modes surfaced in the public project story.
- Git history begins honestly at the imported **v4.1.0** release snapshot; no earlier commit history is reconstructed or backdated.

## Read the process

- [Experiment journal](../experiments/EXPERIMENT_JOURNAL.md)
- [What did not work](../experiments/FAILED_EXPERIMENTS.md)
- [Decision log](../experiments/DECISION_LOG.md)
- [Unexpected findings](../experiments/UNEXPECTED_FINDINGS.md)
- [Git history policy](GIT_HISTORY.md)
- [Raw artifact index](../artifacts/README.md)
- [Evidence ledger](EVIDENCE_LEDGER.md)

## Persistent failure modes

1. **Stale personalization** when older preferences are not superseded.
2. **Protocol-sensitive model selection** when confidence scales / action economics differ.
3. **Evaluator overfitting and grader gaming** under unseen trajectory attacks.
4. **Belief contamination** from irrelevant other-person evidence near decision boundaries.
5. **Synthetic-data semantic collapse** where many exact-unique rows share a tiny number of templates.

## Research shape

The released history is deliberately not `idea → perfect implementation → amazing result`. The actual evidence chain contains repeated revisions:

`hypothesis → controlled experiment → surprising/negative result → narrower claim → new evaluator/data check → regression gate`

The strongest examples are the calibration-induced ranking reversal and the held-out grader attack failure. Both changed the project's central framing after an initially favorable result failed a stronger test.
