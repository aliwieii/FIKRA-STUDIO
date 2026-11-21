"""Feature O: Project Bootstrap Generator — scaffolds a ready-to-run project workspace."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .approval_guard import lock_decision
from .project_state import create_project_state, save_state
from .prompt_compiler import compile_production_prompt


def bootstrap_project(
    output_dir: Path,
    project_id: str,
    title: str,
    mode: str = "UNIVERSAL_VIDEO_MODE",
    style_id: str = "STY-001",
    aspect_ratio: str | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    state = create_project_state(project_id=project_id, title=title, mode=mode, aspect_ratio=aspect_ratio)
    lock_decision(state, "style", style_id, approved_by="bootstrap")
    state["evidence"]["prompt_compiled"] = True

    compiled = compile_production_prompt(state, root=root)
    state_path = save_state(state, output_dir / "project_state.json")
    prompt_path = output_dir / "compiled_prompt.md"
    prompt_path.write_text(compiled["prompt_markdown"], encoding="utf-8")

    vars_path = output_dir / "variables.json"
    w_px, h_px = (1080, 1920) if state["aspect_ratio"] == "9:16" else (1920, 1080)
    vars_path.write_text(json.dumps({
        "project_id": project_id,
        "episode_title": title,
        "mode": mode,
        "style_id": style_id,
        "fps": 30,
        "width": w_px,
        "height": h_px,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "output_dir": str(output_dir),
        "files_created": [state_path.name, prompt_path.name, vars_path.name],
        "mode": mode,
        "isolation_clean": compiled["isolation_clean"],
    }
