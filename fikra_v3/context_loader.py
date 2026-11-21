"""Feature A: AI Context Loader — deterministic minimal file routing per mode/query."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from . import MODES, repo_root

MODE_FILES: dict[str, list[str]] = {
    "UNIVERSAL_VIDEO_MODE": [
        "AGENTS.md",
        "SYSTEM_MANIFEST.json",
        "01_SYSTEM_CORE/SYSTEM_RULES.md",
        "01_SYSTEM_CORE/MODE_ROUTER.md",
        "01_SYSTEM_CORE/APPROVAL_POLICY.md",
        "02_WORKFLOWS/UNIVERSAL_VIDEO_WORKFLOW.md",
        "06_PROMPT_LIBRARY/PRODUCTION_TEMPLATES/UNIVERSAL_PRODUCTION_PROMPT_V1.md",
        "03_STYLE_LIBRARY/STYLE_REGISTRY.csv",
    ],
    "FIKRA_CHANNEL_MODE": [
        "AGENTS.md",
        "SYSTEM_MANIFEST.json",
        "01_SYSTEM_CORE/SYSTEM_RULES.md",
        "01_SYSTEM_CORE/MODE_ROUTER.md",
        "01_SYSTEM_CORE/APPROVAL_POLICY.md",
        "02_WORKFLOWS/FIKRA_CHANNEL_WORKFLOW.md",
        "06_PROMPT_LIBRARY/PRODUCTION_TEMPLATES/FIKRA_CHANNEL_PRODUCTION_PROMPT_V1.md",
        "06_PROMPT_LIBRARY/VOICE_AND_TTS/FIKRA_VOICE_01_TTS_PROMPT.md",
        "03_STYLE_LIBRARY/STYLE_REGISTRY.csv",
    ],
    "QURAN_MODE": [
        "AGENTS.md",
        "01_SYSTEM_CORE/SYSTEM_RULES.md",
        "02_WORKFLOWS/SPECIAL_MODES.md",
        "02_WORKFLOWS/FIKRA_CHANNEL_WORKFLOW.md",
    ],
    "PODCAST_SHORT_MODE": [
        "AGENTS.md",
        "01_SYSTEM_CORE/SYSTEM_RULES.md",
        "02_WORKFLOWS/SPECIAL_MODES.md",
    ],
    "LOGO_ANIMATION_MODE": [
        "AGENTS.md",
        "01_SYSTEM_CORE/SYSTEM_RULES.md",
        "02_WORKFLOWS/SPECIAL_MODES.md",
        "04_LOGO_ANIMATION_LIBRARY/LOGO_REGISTRY.csv",
        "04_LOGO_ANIMATION_LIBRARY/LOGO_ANIMATION_INDEX.md",
        "06_PROMPT_LIBRARY/PRODUCTION_TEMPLATES/LOGO_ANIMATION_PROMPT_V1.md",
    ],
    "PROMPT_ONLY_MODE": [
        "AGENTS.md",
        "01_SYSTEM_CORE/SYSTEM_RULES.md",
        "02_WORKFLOWS/SPECIAL_MODES.md",
        "06_PROMPT_LIBRARY/PRODUCTION_TEMPLATES/UNIVERSAL_PRODUCTION_PROMPT_V1.md",
    ],
    "REFERENCE_AUDIT_MODE": [
        "AGENTS.md",
        "01_SYSTEM_CORE/SYSTEM_RULES.md",
        "02_WORKFLOWS/SPECIAL_MODES.md",
        "09_ASSET_AND_RIGHTS_REGISTRY/ASSET_REGISTRY.json",
    ],
    "VISUAL_UPGRADE_MODE": [
        "AGENTS.md",
        "01_SYSTEM_CORE/APPROVAL_POLICY.md",
        "02_WORKFLOWS/SPECIAL_MODES.md",
        "03_STYLE_LIBRARY/STYLE_REGISTRY.csv",
    ],
    "STICKMAN_COMEDY_MODE": [
        "AGENTS.md",
        "01_SYSTEM_CORE/SYSTEM_RULES.md",
        "02_WORKFLOWS/SPECIAL_MODES.md",
        "03_STYLE_LIBRARY/STYLE_REGISTRY.csv",
    ],
}

FORBIDDEN_LEAKS: dict[str, list[str]] = {
    "UNIVERSAL_VIDEO_MODE": [
        "FIKRA_CHANNEL_WORKFLOW.md",
        "FIKRA_VOICE_01_TTS_PROMPT.md",
        "FIKRA_CHANNEL_PRODUCTION_PROMPT_V1.md",
    ],
}


def detect_mode(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["قناة فكرة", "فيديو قناة فكرة", "fikra channel", "fikra_channel"]):
        return "FIKRA_CHANNEL_MODE"
    if any(k in q for k in ["قرآن", "آية", "تلاوة", "quran"]):
        return "QURAN_MODE"
    if any(k in q for k in ["تحريك الشعار", "لوجو", "شعار", "logo animation", "svg logo"]):
        return "LOGO_ANIMATION_MODE"
    if any(k in q for k in ["بودكاست", "podcast"]):
        return "PODCAST_SHORT_MODE"
    if any(k in q for k in ["ستيك مان", "stickman"]):
        return "STICKMAN_COMEDY_MODE"
    if any(k in q for k in ["فيديو مرجعي", "reference audit", "تدقيق مرجع"]):
        return "REFERENCE_AUDIT_MODE"
    if any(k in q for k in ["ترقية بصرية", "visual upgrade"]):
        return "VISUAL_UPGRADE_MODE"
    if any(k in q for k in ["برومبت فقط", "prompt only"]):
        return "PROMPT_ONLY_MODE"
    return "UNIVERSAL_VIDEO_MODE"


def load_context(
    mode: str | None = None,
    query: str = "",
    style_id: str | None = None,
    logo_id: str | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    r = repo_root(root)
    active_mode = mode if mode in MODES else detect_mode(query)
    files = list(MODE_FILES.get(active_mode, MODE_FILES["UNIVERSAL_VIDEO_MODE"]))

    if style_id:
        sid = style_id.upper()
        spec_dir = r / "03_STYLE_LIBRARY"
        for p in sorted(spec_dir.rglob(f"*{sid}*")):
            if p.is_file():
                rel = p.relative_to(r).as_posix()
                if rel not in files:
                    files.append(rel)

    if logo_id:
        lid = logo_id.upper()
        logo_dir = r / "04_LOGO_ANIMATION_LIBRARY"
        for p in sorted(logo_dir.rglob(f"*{lid}*")):
            if p.is_file():
                rel = p.relative_to(r).as_posix()
                if rel not in files:
                    files.append(rel)

    # Filter existing and check mode isolation
    resolved = []
    missing = []
    total_bytes = 0
    forbidden = FORBIDDEN_LEAKS.get(active_mode, [])
    for rel in files:
        if any(f in rel for f in forbidden):
            continue
        p = r / rel
        if p.exists():
            sz = p.stat().st_size
            total_bytes += sz
            resolved.append({"path": rel, "size_bytes": sz})
        else:
            missing.append(rel)

    return {
        "mode": active_mode,
        "isolation_verified": not any(
            any(f in item["path"] for f in forbidden) for item in resolved
        ),
        "file_count": len(resolved),
        "total_bytes": total_bytes,
        "estimated_tokens": max(1, total_bytes // 4),
        "files": resolved,
        "missing": missing,
    }
