# Flagship Evidence Layer Contract

Use this contract for every flagship research project. The polished homepage can remain visually clean; the scientific story must expose evidence of iteration.

## Required components

1. **Experiment Log** — each entry: hypothesis, setup, result, interpretation, next decision, evidence path.
2. **Failed Experiments** — failure, why it likely failed, what changed; never invent failures for aesthetics.
3. **Decision Log** — Decision → Alternatives → Evidence → Trade-off → Outcome.
4. **Real Eval Tables** — full comparison tables, seeds/N/CI when actually measured, cost/latency scope labeled.
5. **Unexpected Findings** — results that changed the hypothesis or architecture.
6. **Git History** — incremental commits from the moment real history starts; never backdate or fabricate pre-existing development.
7. **Raw Artifacts** — `artifacts/experiment_logs`, `eval_runs`, `failure_examples`, `plots`, `configs`, `qualitative_cases`, `ablations`.

## Homepage second layer

Add an unnumbered **Inside the research process** section below the polished project narrative. It should show honest counts such as logged experiments, failed/revised hypotheses, major design decisions, and persistent failure modes, then link to:

- View experiment journal →
- What didn’t work →
- Decision log →
- Unexpected findings →
- Raw artifacts →
- Git history policy →
- Reproduce results →

## Integrity rules

- Messy means evidence-rich, not sloppy.
- No fake failed experiment, fake metric, fake commit date, fake GitHub URL, or fake external run.
- A favorable result that fails a stronger test stays in the history and changes the claim.
- Raw artifacts and summarized tables must be traceable to the same canonical outputs.
- External model/human results remain NOT RUN until actually executed.
