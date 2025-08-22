from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class BossState(str, Enum):
    idle = "idle"
    awake = "awake"
    executing = "executing"
    researching = "researching"
    thinking = "thinking"
    rethink = "rethink"
    reflecting = "reflecting"
    restart = "restart"
    stop = "stop"


class OutcomeStatus(str, Enum):
    success = "success"
    failure = "failure"
    pending = "pending"


class MCPTool(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    description: Optional[str] = None
    # Arbitrary fields from MCP tool spec are allowed via extra


class MCPServer(BaseModel):
    name: str
    base_url: str
    api_key: Optional[str] = None
    tools: List[MCPTool] = Field(default_factory=list)


class DSPServer(BaseModel):
    name: str
    base_url: str
    api_key: Optional[str] = None
    model: Optional[str] = None


class HumanAgent(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    role: Optional[str] = None
    timezone: Optional[str] = None


class AgentType(str, Enum):
    agentic = "agentic"
    human = "human"


class AgentIdentity(BaseModel):
    agent_type: AgentType
    id: str
    display_name: Optional[str] = None


class TaskStatus(str, Enum):
    created = "created"
    queued = "queued"
    running = "running"
    waiting_human = "waiting_human"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class TaskResult(BaseModel):
    status: OutcomeStatus
    summary: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    created_by: AgentIdentity
    assignee: Optional[AgentIdentity] = None
    status: TaskStatus = TaskStatus.created
    history: List[str] = Field(default_factory=list)
    result: Optional[TaskResult] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Report(BaseModel):
    task_id: str
    reporter: AgentIdentity
    status: OutcomeStatus
    summary: str
    details: Optional[Dict[str, Any]] = None


class PromptSignature(BaseModel):
    name: str
    system_prompt: str
    user_prompt_template: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)


class BossConfig(BaseModel):
    name: str = "DSPY Boss"
    max_agentic_clones: int = 3
    mcp_servers: List[MCPServer] = Field(default_factory=list)
    dspy_servers: List[DSPServer] = Field(default_factory=list)
    react_prompt: Optional[PromptSignature] = None
    humans: List[HumanAgent] = Field(default_factory=list)


class BossEvent(BaseModel):
    type: str
    payload: Dict[str, Any] = Field(default_factory=dict)


class BossDecision(BaseModel):
    state: BossState
    reason: str
    selected_tools: List[str] = Field(default_factory=list)
    selected_assignees: List[str] = Field(default_factory=list)
    new_tasks: List[Task] = Field(default_factory=list)
