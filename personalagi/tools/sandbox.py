from __future__ import annotations
from personalagi.schemas import ToolResult


class SandboxTools:
    """Safe deterministic world for experiments: notes/tasks/reminders, no external side effects."""
    def __init__(self):
        self.tasks: dict[str, dict] = {}
        self.notes: list[str] = []
        self.reminders: dict[str, dict] = {}

    def call(self, tool: str, action: str, payload: dict) -> ToolResult:
        try:
            if tool == "task_store" and action in {"create", "execute_next_step"}:
                title = payload.get("title") or payload.get("objective") or "untitled"
                self.tasks[title] = {"title": title, "status": payload.get("status", "open")}
                return ToolResult(tool, action, True, self.tasks[title].copy())
            if tool == "notes" and action == "add":
                self.notes.append(str(payload["text"]))
                return ToolResult(tool, action, True, {"text": payload["text"]})
            if tool == "reminders" and action == "create":
                rid = str(len(self.reminders) + 1)
                self.reminders[rid] = dict(payload)
                return ToolResult(tool, action, True, {"id": rid, **payload})
            return ToolResult(tool, action, False, error="unsupported tool/action")
        except Exception as e:
            return ToolResult(tool, action, False, error=str(e))

    def snapshot(self) -> dict:
        return {"tasks": self.tasks.copy(), "notes": list(self.notes), "reminders": self.reminders.copy()}


    def restore(self, snapshot: dict) -> None:
        self.tasks = {str(k): dict(v) for k, v in snapshot.get("tasks", {}).items()}
        self.notes = [str(x) for x in snapshot.get("notes", [])]
        self.reminders = {str(k): dict(v) for k, v in snapshot.get("reminders", {}).items()}
