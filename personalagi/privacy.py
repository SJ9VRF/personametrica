from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass(slots=True)
class PrivacyDecision:
    allow_persistent_memory: bool
    reason: str
    category: str = "ordinary"

class PrivacyGuard:
    """Conservative local guard preventing obvious secrets from persistent memory.

    It is intentionally narrow and auditable: it does not claim full PII detection.
    """
    _patterns = {
        "credential": re.compile(r"\b(password|passcode|api[ -]?key|secret key|private key)\b", re.I),
        "financial": re.compile(r"\b(credit card|debit card|cvv|bank account|routing number)\b", re.I),
        "government_id": re.compile(r"\b(ssn|social security number|passport number)\b", re.I),
    }

    def evaluate(self, text: str) -> PrivacyDecision:
        for category, pattern in self._patterns.items():
            if pattern.search(text):
                return PrivacyDecision(False, f"blocked sensitive category: {category}", category)
        return PrivacyDecision(True, "allowed by conservative local policy")
