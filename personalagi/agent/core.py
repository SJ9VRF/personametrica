from __future__ import annotations
from personalagi.schemas import InteractionEvent, UserState
from personalagi.config import AgentConfig
from personalagi.memory.store import InMemoryMemoryStore
from personalagi.user_model.state_estimator import TemporalStateEstimator
from personalagi.adapters import RuleBasedInferenceAdapter
from personalagi.goals.manager import GoalManager
from personalagi.proactivity.policy import CalibratedProactivityPolicy
from personalagi.behavior import BehaviorController
from personalagi.feedback import FeedbackEngine
from personalagi.planner import HierarchicalPlanner
from personalagi.tools import SandboxTools
from personalagi.verification import OutcomeVerifier
from personalagi.privacy import PrivacyGuard
import re


class PersonalAGIAgent:
    def __init__(self, user_id: str, config: AgentConfig | None = None, inference_adapter=None) -> None:
        self.config = config or AgentConfig.full()
        self.state = UserState(user_id=user_id)
        self.memory = InMemoryMemoryStore(update_policy=self.config.memory_update_policy,
                                         contradiction_resolution=self.config.contradiction_resolution)
        self.inference_adapter = inference_adapter or RuleBasedInferenceAdapter()
        # Backward-compatible handle used by older callers/tests.
        self.estimator = getattr(self.inference_adapter, "estimator", TemporalStateEstimator())
        self.goals = GoalManager()
        self.proactivity = CalibratedProactivityPolicy(calibrated=self.config.calibrated_proactivity)
        self.behavior = BehaviorController()
        self.feedback = FeedbackEngine()
        self.planner = HierarchicalPlanner()
        self.tools = SandboxTools()
        self.verifier = OutcomeVerifier()
        self.privacy = PrivacyGuard()
        self.events: list[InteractionEvent] = []

    def observe(self, message: str, *, context: dict | None = None, timestamp: str | None = None) -> dict:
        kwargs = {'user_id': self.state.user_id, 'user_message': message, 'context': context or {}}
        if timestamp:
            kwargs['timestamp'] = timestamp
        event = InteractionEvent(**kwargs)
        # Explicit forgetting is processed before new inference so user control wins.
        forgotten_keys = []
        fm = re.search(r"\bforget that (.+?)(?:[.!]|$)", message, re.I)
        if fm:
            extractor = getattr(self.inference_adapter, "extract_preference", self.estimator._extract_preference)
            candidate = extractor(fm.group(1))
            if candidate and self.memory.forget(self.state.user_id, candidate[0]):
                forgotten_keys.append(candidate[0])

        bundle = self.inference_adapter.infer(event, self.state)
        new_memories, new_goals = bundle.memories, bundle.goals
        if fm:
            # A user-control command is not evidence for re-learning the forgotten fact.
            new_memories = []
        if not self.config.confidence_tracking:
            for m in new_memories:
                m.confidence = 1.0
        blocked_memories = []
        if self.config.memory_enabled:
            for m in new_memories:
                decision = self.privacy.evaluate(m.content) if self.config.privacy_guard else None
                if decision is not None and not decision.allow_persistent_memory:
                    blocked_memories.append({"key": m.key, "reason": decision.reason})
                    continue
                self.memory.add(m)
        if self.config.goal_model:
            for goal_text in new_goals:
                goal = self.goals.add(self.state, goal_text)
                event.detected_goals.append(goal.goal_id)
        lifecycle_goal = self.goals.apply_lifecycle_message(self.state, message) if self.config.goal_model else None
        event.detected_preferences.extend(m.memory_id for m in new_memories)
        self.events.append(event)
        return {'event': event, 'new_memories': new_memories, 'blocked_memories': blocked_memories, 'forgotten_keys': forgotten_keys, 'lifecycle_goal': lifecycle_goal,
                'active_goals': self.goals.active(self.state),
                'active_memories': self.memory.active(self.state.user_id)}

    def proactive_decision(self, **features):
        features.setdefault('historical_acceptance', self.feedback.acceptance_rate())
        return self.proactivity.decide(autonomy_preference=self.state.autonomy_preference, **features)

    def execute_and_verify(self, tool: str, action: str, payload: dict, expected: dict):
        result = self.tools.call(tool, action, payload)
        if not self.config.outcome_verification:
            return result, None
        verification = self.verifier.verify_subset(expected, result.payload if result.success else {})
        return result, verification

    def execute_verify_recover(self, tool: str, action: str, payload: dict, expected: dict) -> dict:
        """Execute, verify, and perform one deterministic corrective retry on mismatch.

        This is intentionally a bounded research recovery primitive rather than an open-ended
        autonomous loop: expected fields override the retry payload and the second outcome is
        verified again.
        """
        first_result, first_verification = self.execute_and_verify(tool, action, payload, expected)
        trace = [{"attempt": 1, "result": first_result, "verification": first_verification}]
        if first_verification is None or first_verification.success:
            return {"recovered": False, "success": bool(first_result.success), "trace": trace}
        retry_payload = dict(payload)
        retry_payload.update(expected)
        second_result, second_verification = self.execute_and_verify(tool, action, retry_payload, expected)
        trace.append({"attempt": 2, "result": second_result, "verification": second_verification})
        return {"recovered": bool(second_verification and second_verification.success),
                "success": bool(second_result.success and second_verification and second_verification.success),
                "trace": trace}

    def execute_verify_recover_trace(self, tool: str, action: str, payload: dict, expected: dict, *, confirmation_granted: bool | None = None) -> dict:
        """Run the bounded recovery primitive and emit a grader-ready trajectory.

        The trace records observable tool/verification evidence only; it does not expose hidden
        chain-of-thought. This makes the same schema usable for local deterministic runs and
        externally supplied model-agent traces.
        """
        events=[]
        if confirmation_granted is not None:
            events.append({'type':'confirmation','granted':bool(confirmation_granted)})
        first_result, first_verification = self.execute_and_verify(tool, action, payload, expected)
        events.append({'type':'tool_call','tool':tool,'action':action,'payload':dict(payload),'success':bool(first_result.success)})
        if first_verification is not None:
            events.append({'type':'verification','success':bool(first_verification.success),'expected':dict(first_verification.expected),'observed':dict(first_verification.observed),'discrepancies':list(first_verification.discrepancies)})
        recovered=False
        final_result=first_result; final_verification=first_verification
        if first_verification is not None and not first_verification.success:
            retry_payload=dict(payload); retry_payload.update(expected)
            second_result, second_verification=self.execute_and_verify(tool,action,retry_payload,expected)
            events.append({'type':'tool_call','tool':tool,'action':action,'payload':dict(retry_payload),'success':bool(second_result.success)})
            if second_verification is not None:
                events.append({'type':'verification','success':bool(second_verification.success),'expected':dict(second_verification.expected),'observed':dict(second_verification.observed),'discrepancies':list(second_verification.discrepancies)})
            recovered=bool(second_verification and second_verification.success)
            final_result=second_result; final_verification=second_verification
        return {
            'events':events,
            'final_state':dict(final_result.payload) if final_result.success else {},
            'success':bool(final_result.success and (final_verification is None or final_verification.success)),
            'recovered':recovered,
        }

    def explain_state(self) -> dict:
        return {'user_id': self.state.user_id,
                'memories': [m.to_dict() for m in self.memory.active(self.state.user_id)],
                'memory_history': [m.to_dict() for m in self.memory.history(self.state.user_id)],
                'memory_conflicts': {k: [r.to_dict() for r in rs] for k, rs in self.memory.conflicts(self.state.user_id).items()},
                'memory_audit': [a.to_dict() for a in self.memory.audit_log],
                'goals': [g.to_dict() for g in self.state.goals.values()],
                'behavior': self.state.interaction_style.copy(),
                'autonomy_preference': self.state.autonomy_preference,
                'config': {name: getattr(self.config, name) for name in self.config.__dataclass_fields__}}
    def save_snapshot(self, path: str):
        from personalagi.persistence import dump_agent
        return dump_agent(self, path)

    def load_snapshot(self, path: str):
        from personalagi.persistence import load_agent
        return load_agent(self, path)

