"""Feature O: Project Bootstrap Generator — safe overwrite-protected runnable project scaffold."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .approval_guard import lock_decision
from .knowledge_graph import lookup_style
from .project_state import create_project_state, save_state
from .prompt_compiler import compile_production_prompt

ASPECT_DIMENSIONS = {
    "9:16": (1080, 1920),
    "16:9": (1920, 1080),
    "1:1": (1080, 1080),
}


def bootstrap_project(
    output_dir: Path,
    project_id: str,
    title: str,
    mode: str = "UNIVERSAL_VIDEO_MODE",
    style_id: str = "STY-001",
    aspect_ratio: str | None = None,
    force: bool = False,
    root: Path | None = None,
) -> dict[str, Any]:
    # Validate style belongs strictly to the 32-style library (FIK-009)
    if not lookup_style(style_id, root=root):
        raise ValueError(f"Unknown style_id '{style_id}'. Must be one of STY-001..STY-032.")

    state_file = output_dir / "project_state.json"
    if state_file.exists() and not force:
        raise FileExistsError(
            f"Project already exists at {output_dir}. Pass force=True to overwrite existing files."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "scenes").mkdir(exist_ok=True)
    (output_dir / "assets").mkdir(exist_ok=True)

    state = create_project_state(project_id=project_id, title=title, mode=mode, aspect_ratio=aspect_ratio)
    lock_decision(state, "style", style_id, approved_by="bootstrap")
    state["evidence"]["prompt_compiled"] = True

    compiled = compile_production_prompt(state, root=root)
    state_path = save_state(state, state_file)
    prompt_path = output_dir / "compiled_prompt.md"
    prompt_path.write_text(compiled["prompt_markdown"], encoding="utf-8")

    w_px, h_px = ASPECT_DIMENSIONS.get(state["aspect_ratio"], (1080, 1920))
    vars_path = output_dir / "variables.json"
    vars_path.write_text(json.dumps({
        "project_id": project_id,
        "episode_title": title,
        "mode": mode,
        "style_id": style_id,
        "aspect_ratio": state["aspect_ratio"],
        "fps": 30,
        "width": w_px,
        "height": h_px,
        "no_music_enforced": True,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    readme_path = output_dir / "RUN_GUIDE.md"
    readme_path.write_text(
        f"# {title} ({project_id})\n"
        f"- Mode: `{mode}` | Style: `{style_id}` | Aspect: `{state['aspect_ratio']}` ({w_px}x{h_px})\n"
        "- Validate QA: `python3 -m fikra_v3 readiness --state project_state.json`\n",
        encoding="utf-8",
    )

    return {
        "output_dir": str(output_dir),
        "files_created": [state_path.name, prompt_path.name, vars_path.name, readme_path.name],
        "mode": mode,
        "aspect_ratio": state["aspect_ratio"],
        "resolution": f"{w_px}x{h_px}",
        "isolation_clean": compiled["isolation_clean"],
    }
