from __future__ import annotations
from personalagi.adapters.base import InferenceBundle
from personalagi.user_model.state_estimator import TemporalStateEstimator

class RuleBasedInferenceAdapter:
    name = "transparent-rule-based-v1"
    def __init__(self) -> None:
        self.estimator = TemporalStateEstimator()
    def infer(self, event, state) -> InferenceBundle:
        memories, goals = self.estimator.infer(event, state)
        return InferenceBundle(memories=memories, goals=goals)
    def extract_preference(self, text: str):
        return self.estimator._extract_preference(text)
