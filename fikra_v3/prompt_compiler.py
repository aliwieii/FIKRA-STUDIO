"""Feature D: Prompt Compiler — compiles mode-isolated, approval-locked Production Prompts."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .approval_guard import verify_approval_integrity
from .knowledge_graph import lookup_logo, lookup_style


def compile_production_prompt(state: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    integrity = verify_approval_integrity(state)
    if not integrity["valid"]:
        raise ValueError(f"Cannot compile prompt: tampered approval locks {integrity['tampered_locks']}")

    mode = state["mode"]
    decisions = state.get("decisions", {})
    style_id = decisions.get("style")
    logo_id = decisions.get("logo_animation")
    style_info = lookup_style(style_id, root) if isinstance(style_id, str) and style_id.startswith("STY-") else None
    logo_info = lookup_logo(logo_id, root) if isinstance(logo_id, str) and logo_id.startswith("L") else None

    guardrails = [
        "Preserve Arabic RTL shaping; never split Arabic words into isolated letters.",
        "Never truncate long Arabic captions; paginate words across time-synced chunks.",
        "Never claim unexecuted renders or synthetic audio measurements.",
    ]
    if mode == "FIKRA_CHANNEL_MODE":
        guardrails.extend([
            "FIKRA CHANNEL POLICY: Strict NO-MUSIC rule (voiceover, verified external Quran recitation, justified SFX, or silence only).",
            "VOICE IDENTITY: FIKRA VOICE 01 (adult Arab male, warm medium-deep documentary tone).",
            "TYPOGRAPHY: Gold (#F59E0B) for Quranic verses, White (#F8FAFC) for narrative text.",
            "ASPECT RATIO: Vertical 9:16 (1080x1920, 30 FPS).",
        ])
    elif mode == "QURAN_MODE":
        guardrails.extend([
            "QURAN GUARDRAIL: Use verified exact Uthmani/Quranic text only; never break meaning mid-verse.",
            "AUDIO GUARDRAIL: External verified recitation only; ZERO music, ZERO SFX, ZERO nasheed over recitation.",
        ])
    elif mode == "UNIVERSAL_VIDEO_MODE":
        guardrails.append(
            "UNIVERSAL MODE ISOLATION: No FIKRA Channel constraints, no forced 9:16, no forced FIKRA VOICE 01, no forced no-music rule."
        )
    elif mode == "LOGO_ANIMATION_MODE":
        guardrails.append("LOGO MODE: Animate only the user-supplied SVG logo; never embed third-party logos.")

    lines = [
        f"# PRODUCTION PROMPT — {state.get('title', 'Untitled Project')}",
        f"- **Project ID:** {state.get('project_id')}",
        f"- **Operating Mode:** `{mode}`",
        f"- **Aspect Ratio:** `{state.get('aspect_ratio')}`",
        f"- **Locked Approvals Verified:** `{integrity['verified_locks']}`",
        "",
        "## 1. Creative Direction & Script",
        f"- **Idea:** {decisions.get('idea', '(pending user approval)')}",
        f"- **Script:** {decisions.get('script', '(pending user approval)')}",
        "",
        "## 2. Visual Style & Engine",
    ]
    if style_info:
        lines.extend([
            f"- **Style:** `{style_info['style_id']}` — {style_info['arabic_name']} ({style_info['english_name']})",
            f"- **Spec File:** `{style_info['spec_file']}`",
            f"- **Reference Videos:** `{', '.join(style_info['reference_video_ids']) or 'None'}`",
            f"- **Execution Engine:** {style_info['execution_requirements']}",
        ])
    elif logo_info:
        lines.extend([
            f"- **Logo Animation:** `{logo_info['animation_id']}` — {logo_info['arabic_name']} ({logo_info['english_name']})",
            f"- **Reference TSX:** `{logo_info['reference_tsx']}`",
            f"- **Execution Engine:** {logo_info['execution_requirements']}",
        ])
    else:
        lines.append("- **Style:** Custom / Not yet selected")

    lines.append("")
    lines.append("## 3. Mandatory Guardrails")
    for g in guardrails:
        lines.append(f"- {g}")

    prompt_text = "\n".join(lines) + "\n"
    return {
        "mode": mode,
        "isolation_clean": not (
            mode == "UNIVERSAL_VIDEO_MODE"
            and ("FIKRA CHANNEL POLICY" in prompt_text or "FIKRA VOICE 01 (" in prompt_text)
        ),
        "prompt_markdown": prompt_text,
    }
