from __future__ import annotations
from personalagi.schemas import VerificationResult


class OutcomeVerifier:
    def verify_subset(self, expected: dict, observed: dict) -> VerificationResult:
        discrepancies = []
        for k, v in expected.items():
            if observed.get(k) != v:
                discrepancies.append(f"{k}: expected={v!r}, observed={observed.get(k)!r}")
        return VerificationResult(not discrepancies, expected, observed, discrepancies)
