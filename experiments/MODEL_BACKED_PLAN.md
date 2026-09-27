# Model-backed experiment plan

This is the external evidence required before making claims about LLM personalization quality.

## Experiment M1 — evidence extraction

Input: natural-language conversation turn + prior structured belief state.  
Output: structured evidence records (`slot`, `value`, `source`, `confidence`, `context`, `temporary_until`).

Compare at least:

1. small open-weight instruct model;
2. stronger open-weight instruct model;
3. multiple frontier hosted models, subject to access;
4. rule-based local extractor as transparent lower baseline.

Primary metrics: slot/value F1, source classification, temporary-scope accuracy, abstention, Brier/ECE.

## Experiment M2 — end-to-end long-horizon personalization

Evaluate the full extraction + state-update stack on official external benchmarks where licensing permits:

- HorizonBench official split;
- PrefEval explicit and implicit variants;
- LongMemEval knowledge-update / temporal subsets;
- PerMemBench storage-policy evaluation.

Do not reimplement official graders when an official evaluator exists. Preserve benchmark licenses and version hashes.

## Experiment M3 — independent proactivity labels

Run system decisions against held-out human annotations from `annotation/`, not the simulator oracle. Report agreement, coverage, selective accuracy, autonomy-violation slices, and ambiguity-conditioned performance.

## Experiment M4 — downstream tasks

At minimum one recommendation/planning task and one tool-use task where a preference error changes task outcome. Report task success, preference satisfaction, constraint violation, confirmations, latency and cost.

## Reporting rule

A table cell remains `NOT RUN` until an actual model/participant run is available. Replayed example JSON is infrastructure validation only.
