"""V3.4 Motion Craft, Anti-Slide Compliance, Narrative Archetypes & Reel Effects."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from . import repo_root
from .prompt_compiler import assert_no_music_leak


def load_motion_craft_catalog(root: Path | None = None) -> dict[str, Any]:
    r = root or repo_root()
    p = r / "03_STYLE_LIBRARY" / "MOTION_CRAFT_AND_REEL_PRESETS_V34.json"
    if not p.exists():
        raise FileNotFoundError(f"V3.4 catalog missing: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def list_narrative_archetypes(mode: str | None = None, root: Path | None = None) -> list[dict[str, Any]]:
    cat = load_motion_craft_catalog(root)
    items = cat.get("narrative_archetypes", [])
    if not mode:
        return items
    return [a for a in items if mode in a.get("allowed_modes", [])]


def list_reel_effects(root: Path | None = None) -> list[dict[str, Any]]:
    return load_motion_craft_catalog(root).get("reel_effects_catalog", [])


def check_motion_craft_compliance(code_or_spec: str, engine: str = "remotion") -> dict[str, Any]:
    """Audit Remotion/HTML motion code or spec against V3.4 Motion Craft & No-Music rules."""
    text = code_or_spec or ""
    violations: list[dict[str, str]] = []

    music_audit = assert_no_music_leak(text)
    if not music_audit["pass"]:
        violations.append({
            "rule_id": "MC-06",
            "severity": "CRITICAL",
            "message": f"Background music leak detected: {music_audit['leaks']}",
        })

    if "Math.random(" in text:
        violations.append({
            "rule_id": "MC-02",
            "severity": "HIGH",
            "message": "Non-deterministic Math.random() detected; bind motion to frame/timeline clock.",
        })

    if engine.lower() == "remotion":
        if re.search(r"\btransition\s*:", text) or re.search(r"\banimate-(?:pulse|bounce|spin|ping)\b", text):
            violations.append({
                "rule_id": "MC-02",
                "severity": "HIGH",
                "message": "CSS transition or Tailwind animate-* class detected in Remotion; use useCurrentFrame()/spring()/interpolate().",
            })

    # Check explicit tiny font sizes (<30px) in 1080p specs
    for m in re.finditer(r"fontSize\s*[:=]\s*(\d+)", text):
        size = int(m.group(1))
        if 0 < size < 30:
            violations.append({
                "rule_id": "MC-03",
                "severity": "MEDIUM",
                "message": f"Font size {size}px is below the 30px mobile readability floor for 1080w stages.",
            })

    return {
        "pass": len(violations) == 0,
        "engine": engine,
        "violations_count": len(violations),
        "violations": violations,
        "music_audit": music_audit,
    }
