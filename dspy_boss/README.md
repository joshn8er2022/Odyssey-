# dspy-boss

A generalized DSPy boss with:

- State machine: idle, awake, executing, researching, thinking, rethink, reflecting, restart, stop
- Assignees: agentic sub-bosses (numbered clones) and human agents
- Config loading:
  - MCP servers from JSON
  - DSP servers from JSON
  - React agent prompt signature from YAML
  - Human agents from YAML
- Async task manager to run tasks concurrently and track human-awaiting tasks
- Pydantic BaseModel for all internal data models
- Typer CLI for quick demos

This is a minimal reference implementation to be adapted for trading, operations, or general workflows.
