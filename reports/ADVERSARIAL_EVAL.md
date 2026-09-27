# Adversarial Language Evaluation

This report evaluates the transparent local preference estimator on language forms that are intentionally more varied than the main simulator templates. It is a stress test of parsing and temporal slot continuity, not a claim of general natural-language understanding.

## Results

- Preference-language stress accuracy: **93.3%**
- Stress-suite Brier error: **0.0149**
- Multi-turn reversal-sequence accuracy: **100.0%**

The suite includes explicit preferences, hedges, within-utterance reversals (`used to ... but now ...`), elliptical multi-turn updates, conditional technical-detail preferences, likes, and dislikes.

## Known failure surface

The local estimator remains pattern-based. Unsupported paraphrases, implicit preferences requiring pragmatic inference, multilingual utterances, and references requiring world knowledge are intentionally outside the evidence boundary. A learned extractor should be evaluated against this same interface before any stronger claim is made.
