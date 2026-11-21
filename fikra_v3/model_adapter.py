"""Feature M: Model Adapter Layer — generates compact platform payloads from AGENTS.md SSOT."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from . import repo_root
from .context_loader import load_context

ADAPTER_HINTS = {
    "gemini": "Use tool-grounded retrieval, respect RTL Arabic output, and invoke `python3 -m fikra_v3` for validation.",
    "claude": "Load `AGENTS.md` once, run `python3 -m unittest discover -s tests -v` after edits, and keep commits atomic.",
    "chatgpt": "Read `SYSTEM_MANIFEST.json` first, follow the active mode workflow strictly, and never fabricate render outputs.",
    "generic": "Start from `AGENTS.md` + `SYSTEM_MANIFEST.json` and follow `AGENT_ONBOARDING_GUIDE.md`.",
}


def build_adapter_payload(target: str = "gemini", mode: str = "UNIVERSAL_VIDEO_MODE", root: Path | None = None) -> dict[str, Any]:
    t = target.lower() if target.lower() in ADAPTER_HINTS else "generic"
    r = repo_root(root)
    ctx = load_context(mode=mode, root=r)
    return {
        "target_agent": t,
        "source_of_truth": "AGENTS.md",
        "manifest": "SYSTEM_MANIFEST.json",
        "platform_hint": ADAPTER_HINTS[t],
        "active_mode": ctx["mode"],
        "minimal_files_to_read": [f["path"] for f in ctx["files"]],
        "estimated_tokens": ctx["estimated_tokens"],
    }
