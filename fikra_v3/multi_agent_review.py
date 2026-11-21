"""Feature J: Multi-Agent Review — 4-persona automated production review rubric."""
from __future__ import annotations

from typing import Any

from .approval_guard import verify_approval_integrity
from .arabic_qa import analyze_arabic_text


def run_multi_agent_review(state: dict[str, Any], prompt_markdown: str = "") -> dict[str, Any]:
    decisions = state.get("decisions", {})
    mode = state.get("mode", "UNIVERSAL_VIDEO_MODE")
    script = str(decisions.get("script", ""))

    # 1. Creative Director
    director_ok = bool(decisions.get("idea") and decisions.get("style"))
    director_notes = [] if director_ok else ["Missing approved idea or visual style selection."]

    # 2. Arabic Linguist
    arabic_rep = analyze_arabic_text(script) if script else {"pass": False, "issues": ["No script provided."]}

    # 3. Technical Engineer
    tech_ok = bool(state.get("aspect_ratio") and prompt_markdown.strip())
    tech_notes = [] if tech_ok else ["Missing aspect ratio or compiled Production Prompt."]

    # 4. Rights & Compliance Auditor
    lock_check = verify_approval_integrity(state)
    compliance_notes = []
    if not lock_check["valid"]:
        compliance_notes.append(f"Tampered approval locks: {lock_check['tampered_locks']}")
    if mode == "UNIVERSAL_VIDEO_MODE" and "FIKRA CHANNEL POLICY" in prompt_markdown:
        compliance_notes.append("Mode leakage detected: FIKRA Channel policy inside Universal mode.")
    compliance_ok = len(compliance_notes) == 0

    personas = {
        "creative_director": {"pass": director_ok, "notes": director_notes},
        "arabic_linguist": {"pass": arabic_rep["pass"], "notes": arabic_rep["issues"]},
        "technical_engineer": {"pass": tech_ok, "notes": tech_notes},
        "rights_compliance_auditor": {"pass": compliance_ok, "notes": compliance_notes},
    }
    passed = sum(1 for p in personas.values() if p["pass"])
    return {
        "overall_pass": passed == len(personas),
        "passed_personas": passed,
        "total_personas": len(personas),
        "personas": personas,
    }
