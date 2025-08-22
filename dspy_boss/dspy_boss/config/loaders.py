from __future__ import annotations

import json
from typing import Any
from pathlib import Path

import yaml
from pydantic import ValidationError

from ..core.models import (
    BossConfig,
    MCPServer,
    DSPServer,
    PromptSignature,
    HumanAgent,
)


def _read_text(path: str | Path) -> str:
    return Path(path).expanduser().read_text(encoding="utf-8")


def load_mcp_servers_from_json(path: str | Path) -> list[MCPServer]:
    raw = json.loads(_read_text(path))
    if isinstance(raw, dict):
        raw = raw.get("servers", [])
    return [MCPServer.model_validate(item) for item in raw]


def load_dsp_servers_from_json(path: str | Path) -> list[DSPServer]:
    raw = json.loads(_read_text(path))
    if isinstance(raw, dict):
        raw = raw.get("servers", [])
    return [DSPServer.model_validate(item) for item in raw]


def load_prompt_signature_from_yaml(path: str | Path) -> PromptSignature:
    raw = yaml.safe_load(_read_text(path))
    return PromptSignature.model_validate(raw)


def load_humans_from_yaml(path: str | Path) -> list[HumanAgent]:
    raw = yaml.safe_load(_read_text(path))
    if isinstance(raw, dict):
        raw = raw.get("humans", [])
    return [HumanAgent.model_validate(item) for item in raw]


def build_boss_config(
    name: str,
    mcp_json: str | Path,
    dsp_json: str | Path,
    react_yaml: str | Path,
    humans_yaml: str | Path,
    max_agentic_clones: int = 3,
) -> BossConfig:
    mcp = load_mcp_servers_from_json(mcp_json)
    dsp = load_dsp_servers_from_json(dsp_json)
    react = load_prompt_signature_from_yaml(react_yaml)
    humans = load_humans_from_yaml(humans_yaml)
    return BossConfig(
        name=name,
        max_agentic_clones=max_agentic_clones,
        mcp_servers=mcp,
        dspy_servers=dsp,
        react_prompt=react,
        humans=humans,
    )
