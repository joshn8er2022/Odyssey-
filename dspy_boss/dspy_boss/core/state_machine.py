from __future__ import annotations

from typing import Callable, Dict, Optional
from enum import Enum
from pydantic import BaseModel

from .models import BossState, BossEvent


class TransitionGuard(BaseModel):
    allowed: bool
    reason: str = ""


class StateTransition(BaseModel):
    source: BossState
    target: BossState
    guard: Optional[Callable[[BossEvent], TransitionGuard]] = None


class BossStateMachine:
    def __init__(self) -> None:
        self.current_state: BossState = BossState.idle
        self.transitions: Dict[BossState, Dict[str, StateTransition]] = {}
        self._register_default_transitions()

    def _register_default_transitions(self) -> None:
        for state in BossState:
            self.transitions[state] = {}
        # Avail transitions from any state
        for state in BossState:
            self._add(state, "restart", BossState.restart)
            self._add(state, "stop", BossState.stop)
        # Main cycle transitions
        self._add(BossState.idle, "wake", BossState.awake)
        self._add(BossState.awake, "plan", BossState.thinking)
        self._add(BossState.thinking, "research", BossState.researching)
        self._add(BossState.thinking, "execute", BossState.executing)
        self._add(BossState.researching, "rethink", BossState.rethink)
        self._add(BossState.rethink, "execute", BossState.executing)
        self._add(BossState.executing, "reflect", BossState.reflecting)
        self._add(BossState.reflecting, "plan", BossState.thinking)
        self._add(BossState.reflecting, "idle", BossState.idle)

    def _add(self, source: BossState, event_type: str, target: BossState) -> None:
        self.transitions[source][event_type] = StateTransition(source=source, target=target)

    def handle(self, event: BossEvent) -> BossState:
        transitions_for_state = self.transitions.get(self.current_state, {})
        transition = transitions_for_state.get(event.type)
        if transition is None:
            # No transition, remain in state
            return self.current_state
        if transition.guard is not None:
            guard_result = transition.guard(event)
            if not guard_result.allowed:
                return self.current_state
        self.current_state = transition.target
        return self.current_state
