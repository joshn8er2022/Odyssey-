from __future__ import annotations

import asyncio
from typing import Dict, List, Optional
from pydantic import BaseModel, PrivateAttr

from .models import (
    BossState,
    BossEvent,
    BossDecision,
    BossConfig,
    Task,
    TaskStatus,
    AgentIdentity,
    AgentType,
)
from .state_machine import BossStateMachine
from .task_manager import TaskManager


class DSPYBoss(BaseModel):
    config: BossConfig
    _state_machine: BossStateMachine = PrivateAttr(default_factory=BossStateMachine)
    _task_manager: TaskManager = PrivateAttr(default_factory=TaskManager)
    _agentic_counter: int = PrivateAttr(default=0)

    @property
    def state_machine(self) -> BossStateMachine:
        return self._state_machine

    @property
    def task_manager(self) -> TaskManager:
        return self._task_manager

    @property
    def agentic_counter(self) -> int:
        return self._agentic_counter

    def _next_clone_id(self) -> str:
        if self._agentic_counter < self.config.max_agentic_clones:
            self._agentic_counter += 1
        return f"clone-{self._agentic_counter}"

    # Decision policy: choose tools, assignees, and tasks based on state and inputs
    def decide(self, context: Dict) -> BossDecision:
        state = self.state_machine.current_state
        selected_tools: List[str] = []
        selected_assignees: List[str] = []
        new_tasks: List[Task] = []

        # Simple heuristic: if there are humans and context requests human, assign human
        if context.get("requires_human") and self.config.humans:
            human = self.config.humans[0]
            assignee = AgentIdentity(agent_type=AgentType.human, id=human.id, display_name=human.name)
            selected_assignees.append(assignee.id)
        else:
            # create an agentic clone id
            clone_id = self._next_clone_id()
            assignee = AgentIdentity(agent_type=AgentType.agentic, id=clone_id, display_name=f"Agentic {clone_id}")
            selected_assignees.append(assignee.id)

        # Pick tools from first MCP server by default
        if self.config.mcp_servers:
            selected_tools = [tool.name for tool in self.config.mcp_servers[0].tools][:3]

        # Create a task per context instruction
        instruction = context.get("instruction", "General task")
        task = self.task_manager.create_task(title=instruction, created_by=AgentIdentity(agent_type=AgentType.agentic, id="boss"), assignee=assignee)
        new_tasks.append(task)

        return BossDecision(
            state=state,
            reason="Heuristic decision based on context and available resources",
            selected_tools=selected_tools,
            selected_assignees=selected_assignees,
            new_tasks=new_tasks,
        )

    def event(self, event_type: str, payload: Optional[Dict] = None) -> BossState:
        return self.state_machine.handle(BossEvent(type=event_type, payload=payload or {}))

    async def run_once(self, context: Dict) -> List[Task]:
        decision = self.decide(context)
        scheduled_ids = [self.task_manager.schedule(task) for task in decision.new_tasks]
        return [await self.task_manager.wait(task_id) for task_id in scheduled_ids]

    async def run_board_report(self) -> Dict[str, str]:
        report: Dict[str, str] = {}
        for task in self.task_manager.all():
            status = task.status.value
            if task.result and task.result.summary:
                status += f" - {task.result.summary}"
            report[task.id] = status
        return report
