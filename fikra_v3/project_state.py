"""Feature E: Project State Engine — persistent versioned project_state.json manager."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import MODES


def create_project_state(
    project_id: str,
    title: str,
    mode: str = "UNIVERSAL_VIDEO_MODE",
    aspect_ratio: str | None = None,
) -> dict[str, Any]:
    if mode not in MODES:
        raise ValueError(f"Invalid mode '{mode}'. Allowed: {MODES}")
    default_ar = "9:16" if mode in {"FIKRA_CHANNEL_MODE", "QURAN_MODE", "PODCAST_SHORT_MODE"} else (aspect_ratio or "16:9")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "schema_version": "3.0.0",
        "project_id": project_id,
        "title": title,
        "mode": mode,
        "aspect_ratio": aspect_ratio or default_ar,
        "created_at_utc": now,
        "updated_at_utc": now,
        "stage": "INIT",
        "readiness_tier": "UNVERIFIED",
        "decisions": {},
        "approvals": {},
        "evidence": {
            "prompt_compiled": False,
            "spec_validated": False,
            "code_validated": False,
            "build_log_path": None,
            "render_output_path": None,
            "media_qa_passed": False,
        },
        "audit_log": [{"action": "INIT_PROJECT", "mode": mode, "timestamp_utc": now}],
    }


def save_state(state: dict[str, Any], path: Path) -> Path:
    state["updated_at_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_state(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
