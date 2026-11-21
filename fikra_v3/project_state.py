"""Feature E: Project State Engine & Stage State Machine."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import MODES

STAGE_SEQUENCE = (
    "INIT",
    "IDEA_LOCKED",
    "SCRIPT_LOCKED",
    "VOICE_LOCKED",
    "STYLE_LOCKED",
    "STORYBOARD_LOCKED",
    "PRODUCTION_READY",
    "QC_VERIFIED",
    "DELIVERED",
)

STAGE_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "INIT": (),
    "IDEA_LOCKED": ("idea",),
    "SCRIPT_LOCKED": ("idea", "script"),
    "VOICE_LOCKED": ("idea", "script"),
    "STYLE_LOCKED": ("idea", "script", "style"),
    "STORYBOARD_LOCKED": ("idea", "script", "style"),
    "PRODUCTION_READY": ("idea", "script", "style"),
    "QC_VERIFIED": ("idea", "script", "style"),
    "DELIVERED": ("idea", "script", "style"),
}


class StageTransitionError(ValueError):
    """Raised when attempting an illegal stage skip or transitioning without required locked approvals."""


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
        "schema_version": "3.1.1",
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
            "qa_report_path": None,
            "qa_video_sha256": None,
            "media_qa_passed": False,
        },
        "audit_log": [{"action": "INIT_PROJECT", "mode": mode, "timestamp_utc": now}],
    }


def advance_stage(state: dict[str, Any], target_stage: str, user_approved: bool = False) -> dict[str, Any]:
    """Enforce sequential stage progression without skipping and verify required locked approvals."""
    if target_stage not in STAGE_SEQUENCE:
        raise StageTransitionError(f"Unknown target stage '{target_stage}'.")
    current = state.get("stage", "INIT")
    cur_idx = STAGE_SEQUENCE.index(current)
    tgt_idx = STAGE_SEQUENCE.index(target_stage)
    if tgt_idx != cur_idx + 1:
        raise StageTransitionError(
            f"Illegal stage transition '{current}' -> '{target_stage}'. "
            f"Next allowed stage is '{STAGE_SEQUENCE[cur_idx + 1] if cur_idx + 1 < len(STAGE_SEQUENCE) else 'NONE'}'."
        )
    if not user_approved:
        raise StageTransitionError(f"Explicit user_approved=True is required to advance to '{target_stage}'.")

    approvals = state.get("approvals", {})
    missing_locks = [req for req in STAGE_REQUIREMENTS.get(target_stage, ()) if not approvals.get(req, {}).get("locked")]
    if missing_locks:
        raise StageTransitionError(
            f"Cannot advance to '{target_stage}': missing locked approvals {missing_locks}."
        )

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state["stage"] = target_stage
    state["updated_at_utc"] = now
    state.setdefault("audit_log", []).append({
        "action": "ADVANCE_STAGE",
        "from_stage": current,
        "to_stage": target_stage,
        "timestamp_utc": now,
    })
    return state


def save_state(state: dict[str, Any], path: Path) -> Path:
    state["updated_at_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_state(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def format_stage_footer(completed: str, remaining: str, next_step: str) -> str:
    """Standard V3.1 stage-closure summary enforcing explicit user approval before advancing."""
    return (
        f"- **ما تم إنجازه:** {completed}\n"
        f"- **ما المتبقي:** {remaining}\n"
        f"- **الخطوة التالية:** {next_step}\n"
        "- **تنبيه:** لن يتم الانتقال للمرحلة التالية قبل مراجعتك وموافقتك الصريحة."
    )
