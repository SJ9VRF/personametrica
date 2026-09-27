from __future__ import annotations
import re
from personalagi.schemas import Goal, UserState


class GoalManager:
    def add(self, state: UserState, description: str, *, priority: float = .7, deadline: str | None = None) -> Goal:
        if deadline is None:
            m = re.search(r"\b(?:by|before)\s+(.+)$", description, re.I)
            deadline = m.group(1).strip() if m else None
        goal = Goal(description=description, user_id=state.user_id, priority=priority, deadline=deadline)
        state.goals[goal.goal_id] = goal
        return goal

    def active(self, state: UserState) -> list[Goal]:
        return [g for g in state.goals.values() if g.status == "active"]

    def update_progress(self, state: UserState, goal_id: str, progress: float) -> Goal:
        g = state.goals[goal_id]
        g.progress = max(0.0, min(1.0, progress))
        if g.progress >= 1.0:
            g.status = "completed"
        return g

    def decompose(self, goal: Goal) -> list[str]:
        # Deterministic fallback usable without an external LLM.
        if goal.subtasks:
            return goal.subtasks
        goal.subtasks = [f"Clarify success criteria for: {goal.description}",
                         f"Execute the next concrete step for: {goal.description}",
                         f"Verify progress on: {goal.description}"]
        return goal.subtasks


    def match_active(self, state: UserState, text: str) -> Goal | None:
        tokens = set(re.findall(r"[a-z0-9]+", text.lower())) - {"i","my","the","a","an","to","is","was","done","finished","completed","cancelled","canceled"}
        best=None; best_score=0.0
        for g in self.active(state):
            gt=set(re.findall(r"[a-z0-9]+", g.description.lower()))
            score=len(tokens & gt)/max(1,len(tokens | gt))
            if score>best_score:
                best,best_score=g,score
        return best if best_score >= 0.12 else None

    def apply_lifecycle_message(self, state: UserState, text: str) -> Goal | None:
        lower=text.lower()
        completed=bool(re.search(r"\b(i (?:finished|completed|did)|it(?:'s| is) done)\b", lower))
        abandoned=bool(re.search(r"\b(i (?:cancelled|canceled|dropped)|no longer (?:want|need) to)\b", lower))
        if not (completed or abandoned):
            return None
        g=self.match_active(state,text)
        if not g:
            return None
        if completed:
            g.progress=1.0; g.status="completed"
        else:
            g.status="abandoned"
        return g
