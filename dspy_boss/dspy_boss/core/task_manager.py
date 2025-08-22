from __future__ import annotations

import asyncio
import uuid
from typing import Any, Awaitable, Callable, Dict, List, Optional
from pydantic import BaseModel

from .models import Task, TaskStatus, AgentIdentity, AgentType
from .agents import AgenticClone, HumanProxyAgent


class TaskManager(BaseModel):
    concurrency: int = 5

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._semaphore = asyncio.Semaphore(self.concurrency)
        self._tasks: Dict[str, Task] = {}
        self._running: Dict[str, asyncio.Task[Task]] = {}

    def create_task(
        self,
        title: str,
        created_by: AgentIdentity,
        description: str = "",
        assignee: Optional[AgentIdentity] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Task:
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            title=title,
            description=description,
            created_by=created_by,
            assignee=assignee,
            status=TaskStatus.created,
            metadata=metadata or {},
        )
        self._tasks[task_id] = task
        return task

    async def _execute_with_agent(self, task: Task) -> Task:
        agent_identity = task.assignee or task.created_by
        agent: AgenticClone | HumanProxyAgent
        if agent_identity.agent_type == AgentType.human:
            agent = HumanProxyAgent(identity=agent_identity)
        else:
            agent = AgenticClone(identity=agent_identity)

        async with self._semaphore:
            task.status = TaskStatus.running
            task.history.append("Task started")
            result_task = await agent.run_task(task)
            if result_task.status not in (TaskStatus.completed, TaskStatus.waiting_human, TaskStatus.failed):
                # Ensure terminal or waiting state set by agent
                result_task.status = TaskStatus.completed
            return result_task

    def schedule(self, task: Task) -> str:
        task.status = TaskStatus.queued
        coro = self._execute_with_agent(task)
        atask = asyncio.create_task(coro)
        self._running[task.id] = atask
        return task.id

    async def wait(self, task_id: str) -> Task:
        atask = self._running.get(task_id)
        if atask is None:
            return self._tasks[task_id]
        result = await atask
        self._running.pop(task_id, None)
        self._tasks[task_id] = result
        return result

    def get(self, task_id: str) -> Task:
        return self._tasks[task_id]

    def all(self) -> List[Task]:
        return list(self._tasks.values())

    def mark_human_completed(self, task_id: str, summary: str) -> Task:
        task = self._tasks[task_id]
        if task.status != TaskStatus.waiting_human:
            return task
        task.status = TaskStatus.completed
        task.history.append("Human completed task")
        from .models import TaskResult, OutcomeStatus
        task.result = TaskResult(status=OutcomeStatus.success, summary=summary)
        return task
