# Model/System Card — PersonaMetrica

## System type

Local research prototype for longitudinal personalization and agent-policy evaluation. It is not a deployed general-purpose assistant and contains no frontier model.

## Capabilities

- maintains temporal structured memory;
- preserves superseded history and provenance;
- captures simple goals;
- selects among ask/suggest/remind/wait/none;
- executes deterministic low-stakes sandbox tools;
- verifies expected versus observed outcomes;
- records structured feedback and reward components;
- produces reproducible synthetic benchmark data.

## Known limitations

- rule-based language understanding;
- no persistent database across program restart;
- no external accounts/tools;
- no learned personalization policy;
- synthetic benchmark distribution is narrow;
- no executed human validation;
- no privacy/security hardening for deployment.

## Key failure risks

Stale or false memories, incorrect inference, over-personalization, contradictory state, excessive proactivity, missed interventions, autonomy violations, tool mismatch, and misplaced confidence.

## Mitigations in this artifact

Provenance/confidence fields, temporal supersession, conflict inspection, explicit proactivity gates, sandbox-only actions, outcome verification, failure taxonomy, reproducible ablations, and user-facing memory/decision inspection surfaces.

## Result interpretation

Checked-in metrics show expected mechanism behavior under controlled synthetic inputs. They should not be extrapolated to real users or model capability without additional studies.
