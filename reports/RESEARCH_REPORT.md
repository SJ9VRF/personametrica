# Research Report — PersonaMetrica

## 1. Research question

Can an assistant accumulate useful personal state over repeated interactions while controlling stale memory, contradictory beliefs, intrusive proactivity, overconfidence, and unverified actions?

The project treats personal intelligence as a closed-loop systems problem rather than a retrieval feature. The agent receives interaction events, updates a temporal user state, reasons about goals and intervention, acts inside a deterministic tool environment, verifies outcomes, records feedback, and exposes failures as training/evaluation data.

## 2. Hypotheses

**H1 — Temporal update.** Replacing a user's current preference when an explicit reversal occurs should reduce stale-memory error relative to a first-mention memory policy.

**H2 — Conflict resolution.** Superseding semantically conflicting values should reduce simultaneously active contradictions relative to retaining all observations as active.

**H3 — Calibrated proactivity.** Explicit treatment of uncertainty, stakes, reversibility, and interruptibility should improve normative intervention decisions and reduce autonomy violations relative to a utility-only heuristic.

**H4 — Confidence tracking.** Preserving confidence distinctions between explicit, habitual, and tentative statements should improve calibration compared with assigning confidence 1.0 to every memory.

**H5 — Outcome verification.** Comparing expected and observed post-action state should detect injected execution mismatches that an unverified pipeline cannot detect.

## 3. Experimental substrate

The checked-in benchmark uses 100 deterministic synthetic personas over 60 turns each. Personas vary initial work-time preference, response-detail preference, autonomy tendency, and whether/when a preference reversal occurs. Background utterances are deterministic under the seed. A separate set of 200 proactivity scenarios varies goal relevance, urgency, confidence, stakes, reversibility, historical acceptance, and interruptibility.

The simulator is not intended to represent a population of humans. Its purpose is controlled mechanism validation and regression testing.

## 4. Systems compared

- **Full temporal OS:** latest-valid memory, contradiction resolution, confidence tracking, goal model, calibrated proactivity, outcome verification.
- **No temporal update:** preserves the first active value for a preference slot.
- **Stateless:** does not write memory.
- **No contradiction resolution:** leaves conflicting values simultaneously active.
- **No goal model:** observes goal language but does not add goal state.
- **Uncalibrated proactivity:** uses a benefit heuristic without dedicated uncertainty/high-stakes gates.
- **No confidence tracking:** forces extracted-memory confidence to 1.0.
- **No outcome verification:** skips expected-vs-observed verification.

Every ablation is implemented as a real configuration change and evaluated by the same runner.

## 5. Results

See the machine-generated `reports/RESULTS.md` for the exact values tied to `data/eval_results.json`.

The main controlled findings are:

- the full temporal memory path keeps current explicit preference state aligned with the simulator after reversals, while the first-mention policy accumulates substantial stale-state error;
- disabling contradiction resolution leaves conflicting values active for most users who experience drift;
- calibrated proactivity strongly outperforms the uncalibrated heuristic on the benchmark oracle and eliminates measured high-stakes autonomy violations in this scenario set;
- confidence tracking exactly reconstructs the confidence levels emitted by the transparent extractor in the calibration microbenchmark, while forcing all memories to confidence 1.0 increases Brier error;
- outcome verification detects all injected state mismatches in the deterministic action-verification suite; disabling verification detects none.

## 6. Why these results are not enough

The current experiment has deliberately favorable structural assumptions: preference slots are canonical, the extractor uses transparent patterns, the simulator emits known linguistic forms, and the proactivity oracle is hand-defined. Therefore 100% on some mechanism-level metrics is evidence that the implementation obeys the designed semantics, not evidence of general human personalization.

A publication-strength next stage requires model-backed language variation, independent human labels for intervention quality, diverse longitudinal users, adversarial state ambiguity, and evaluation of learned policies on held-out distributions.

## 7. Failure taxonomy

The project records failures under memory, personalization, autonomy, behavior, tools, and goals. Important cases include stale memory, false memory, missing memory, unresolved contradiction, over-personalization, wrong inference, unnecessary intervention, missed intervention, autonomy violation, sycophancy, tool execution failure, tool verification failure, goal misidentification, and plan failure.

## 8. Research interpretation

The useful conclusion from the current artifact is architectural: personal intelligence benefits from explicit state semantics and regression surfaces. A system that only retrieves semantically similar past text cannot directly represent whether a belief is current, superseded, tentative, or context-dependent. Likewise, a system that optimizes intervention benefit without stakes and reversibility can appear helpful while violating autonomy.

## 9. Next experiments

1. Replace deterministic extraction with a model-backed structured extractor and evaluate precision/recall on paraphrased and adversarial statements.
2. Add independently labeled proactivity judgments and grader calibration.
3. Run held-out multilingual and code-switching memory tests.
4. Train a small open-weight policy using the 1,000 generated preference pairs, then compare architecture-only versus post-trained behavior.
5. Execute the human longitudinal protocol and report pre-registered primary/secondary endpoints.
6. Add cost/latency measurements for model-backed components.

## Post-training pipeline hardening (v1.4)

The release now runs a learned pairwise reward baseline after preference-pair generation. Training data is validated, exact-deduplicated, family-tagged, and audited. The learned scorer is evaluated on a group-aware held-out split, randomized-label control, per-family slices, and a lexically matched compositional contrast set. The contrast set remains at chance, which is retained as a documented failure surface and a concrete motivation for the next model-backed experiment.
