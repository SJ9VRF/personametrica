from __future__ import annotations
from personalagi.schemas import Goal, PlanStep


class HierarchicalPlanner:
    def plan(self, goal: Goal) -> list[PlanStep]:
        return [
            PlanStep(objective="Clarify goal state", action="inspect", success_condition="goal requirements are explicit"),
            PlanStep(objective="Advance goal", action="execute_next_step", tool="task_store",
                     success_condition="task is recorded or completed", failure_condition="tool result unsuccessful",
                     fallback="ask_user"),
            PlanStep(objective="Verify outcome", action="verify", success_condition="observed state matches expected state"),
        ]
