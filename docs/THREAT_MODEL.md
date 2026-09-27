# Threat Model and Trust Boundaries

PersonaMetrica is a research prototype. The trust model explicitly separates **stored user state**, **model/inference output**, **tool execution**, and **evaluation evidence**.

## Assets to protect
- user memories and provenance
- explicit forget/delete intent
- goals and commitments
- tool/world state
- feedback history
- evaluation integrity

## Main failure classes

### Memory poisoning
Incorrect or adversarial inferred preferences can contaminate future behavior. Mitigations in this prototype: source/provenance fields, confidence, temporal supersession, user-visible correction/forget paths, and audit events.

### Stale-state persistence
Old preferences may continue influencing decisions after a change. Mitigations: temporal validity, supersession, contradiction handling, drift benchmarks, and regression gates.

### Over-autonomy
The agent may act when it should ask or remain quiet. Mitigations: stakes/reversibility-aware policy, confirmation ladder, autonomy metrics, and adversarial proactivity slices.

### Sensitive persistence
A personal agent can over-store details. The current guard blocks a narrow auditable class of synthetic sensitive strings. It is deliberately not described as a production privacy classifier.

### Tool-result hallucination
An agent can assume a tool succeeded. Mitigation: explicit outcome verification against observed sandbox state.

### Evaluation gaming / leakage
Synthetic preference pairs can leak canonical answer wording across splits. v1.5 explicitly audits this and adds leave-one-family-out and unseen-paraphrase stress tests.

## Out of scope
Production authentication/authorization, encrypted storage, real external account actions, adversarial web content, comprehensive PII classification, and clinical/financial/legal decision making are not claimed or simulated as solved.
