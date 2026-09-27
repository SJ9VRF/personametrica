# Privacy and User-Control Evaluation

Personalization should not imply indiscriminate retention. The local system therefore contains a conservative persistence guard for obvious secrets plus explicit forgetting and an append-only audit trail for memory lifecycle events.

## Controlled results

- Safe ordinary-memory recall: **100.0%**
- Sensitive-memory block rate: **100.0%**
- Without the privacy guard: **0.0%** block rate
- Explicit forget success: **100.0%**
- Deleted-memory retrieval rate: **0.0%**
- Memory audit coverage: **100.0%**

## Scope boundary

The privacy guard detects a narrow set of obvious credential, financial, and government-ID phrases. It is not a production PII classifier and does not replace encryption, authorization, retention policy, data residency controls, or consent UX. Its purpose is to make persistence policy explicit and ablatable in the research substrate.
