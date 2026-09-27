# Trajectory failure-data audit

The failure-derived data is useful as plumbing evidence, but its templated nature can create shortcut learning. This audit makes that limitation explicit and creates task-disjoint splits.

- Rows: 254
- Unique tasks: 80
- Semantic correction templates: 4
- Semantic-template duplication rate: **98.4%**

## Task-disjoint splits

- Train: 179
- Dev: 36
- Test: 39
- Task overlap across splits: 0

## Interpretation

This dataset should not be used to claim semantic post-training generalization in its current form. It is a structured failure-to-data artifact. A model-training paper should replace or augment templated corrections with independently authored/model-generated corrections and evaluate on task- and wording-held-out failures.
