from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from .models import (
    AgentIdentity,
    AgentType,
    Task,
    TaskResult,
    TaskStatus,
    OutcomeStatus,
)


class BaseAgent(BaseModel):
    identity: AgentIdentity

    async def run_task(self, task: Task) -> Task:
        raise NotImplementedError


class AgenticClone(BaseAgent):
    async def run_task(self, task: Task) -> Task:
        # Placeholder autonomous behavior
        await asyncio.sleep(0)
        task.status = TaskStatus.completed
        task.result = TaskResult(status=OutcomeStatus.success, summary=f"Agent {self.identity.id} completed task")
        task.history.append(f"Completed by {self.identity.display_name or self.identity.id}")
        return task


class HumanProxyAgent(BaseAgent):
    # Each instance gets its own inbox list
    inbox: List[str] = Field(default_factory=list)

    async def run_task(self, task: Task) -> Task:
        # Represent sending a notification to human and waiting
        task.status = TaskStatus.waiting_human
        task.history.append("Sent to human, awaiting response")
        return task
