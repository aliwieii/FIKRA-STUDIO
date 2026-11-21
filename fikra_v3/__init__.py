"""FIKRA STUDIO V3.0 — Agent-First Universal Creative Production System."""
from pathlib import Path

__version__ = "3.1.1"

MODES = (
    "UNIVERSAL_VIDEO_MODE",
    "FIKRA_CHANNEL_MODE",
    "QURAN_MODE",
    "PODCAST_SHORT_MODE",
    "LOGO_ANIMATION_MODE",
    "PROMPT_ONLY_MODE",
    "REFERENCE_AUDIT_MODE",
    "VISUAL_UPGRADE_MODE",
    "STICKMAN_COMEDY_MODE",
)

READINESS_TIERS = (
    "UNVERIFIED",
    "PROMPT_READY",
    "SPEC_READY",
    "CODE_READY",
    "BUILD_TESTED",
    "RENDER_TESTED",
)


def repo_root(start: Path | None = None) -> Path:
    cur = (start or Path(__file__).resolve().parent).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "AGENTS.md").exists() or (candidate / "01_SYSTEM_CORE").exists():
            return candidate
    return Path.cwd().resolve()
