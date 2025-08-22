from __future__ import annotations

import asyncio
from pathlib import Path
import typer
from rich import print

from .config.loaders import build_boss_config
from .core.boss import DSPYBoss

app = typer.Typer(help="DSPY Boss CLI")


@app.command()
def demo(
    name: str = typer.Option("DSPY Boss", help="Boss name"),
    mcp_json: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, help="Path to MCP servers JSON"),
    dsp_json: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, help="Path to DSP servers JSON"),
    react_yaml: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, help="Path to React prompt YAML"),
    humans_yaml: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, help="Path to humans YAML"),
    requires_human: bool = typer.Option(False, help="Require human assignment"),
    auto_complete_human: bool = typer.Option(False, help="Auto-complete human tasks for demo"),
    instruction: str = typer.Option("Prepare a plan", help="Instruction for the task"),
):
    """Run a demo cycle of the boss with provided configs."""

    config = build_boss_config(
        name=name,
        mcp_json=str(mcp_json),
        dsp_json=str(dsp_json),
        react_yaml=str(react_yaml),
        humans_yaml=str(humans_yaml),
    )

    boss = DSPYBoss(config=config)
    boss.event("wake")
    boss.event("plan")

    async def _run():
        results = await boss.run_once({"requires_human": requires_human, "instruction": instruction})
        if auto_complete_human:
            for task in boss.task_manager.all():
                if task.status.name == "waiting_human":
                    boss.task_manager.mark_human_completed(task.id, summary="Demo human approved the outcome")
        report = await boss.run_board_report()
        print({"results": [r.model_dump() for r in results], "report": report})

    asyncio.run(_run())


if __name__ == "__main__":
    app()
