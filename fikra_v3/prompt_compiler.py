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
        "STRICT NO-MUSIC DEFAULT: Zero background music across all productions (voiceover, verified external Quran recitation, justified SFX, or intentional silence only).",
        "VISUAL IDENTITY GUARDRAIL: Use 2D animation and creative motion graphics from the 32-style library; avoid photorealistic 3D humans and static slide decks.",
        "NARRATIVE ARC: Open with a strong visual hook in the first seconds, follow Problem -> Escalation -> Resolution, and maintain character/palette consistency across scenes.",
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


def generate_publishing_pack(
    title: str,
    short_description: str,
    cover_text: str,
    engagement_question: str,
    hashtags: list[str],
) -> dict[str, Any]:
    """Build a V3.1 focused Arabic publishing pack (enforcing 5-8 hashtags)."""
    clean_tags = [t if t.startswith("#") else f"#{t}" for t in hashtags if t.strip()]
    if not (5 <= len(clean_tags) <= 8):
        raise ValueError(f"Publishing pack must contain 5-8 hashtags, got {len(clean_tags)}.")
    return {
        "title": title.strip(),
        "short_description": short_description.strip(),
        "cover_text": cover_text.strip(),
        "engagement_question": engagement_question.strip(),
        "hashtags": clean_tags,
        "hashtag_count": len(clean_tags),
    }


TOOL_ADAPTER_GUIDES: dict[str, str] = {
    "video_gen": "Focus on concise camera trajectories, lighting continuity, negative prompt constraints, and 4-6s shot durations.",
    "image_gen": "Specify exact framing, subject pose, color palette hex codes, lighting angle, and text-free clean composition.",
    "remotion_motion": "Use 100% frame-driven useCurrentFrame() springs/interpolations, RTL Arabic safe zones, and zero CSS transitions.",
    "hyperframes": "Drive all motion from seekToFrame(frame) and separate episode text/colors into variables.json.",
    "3d_scene": "Specify camera focal length, key/rim/fill lighting rig, stylized non-photorealistic shaders, and keyframe curves.",
    "video_editor": "Provide exact timecode cut sheet, SFX placement, RTL caption SRT sync, and export specs (H.264/AAC).",
}

INTERVIEW_BANK: dict[str, list[dict[str, str]]] = {
    "product_ad": [
        {"key": "topic", "question": "ما المنتج أو الخدمة وما المشكلة الأساسية التي يحلّها؟", "default": "تطبيق إنتاجي يختصر وقت العمل اليومي"},
        {"key": "audience", "question": "من الجمهور المستهدف والمنصة الأساسية للنشر؟", "default": "روّاد الأعمال والمصممون على Reels وTikTok"},
        {"key": "duration", "question": "ما المدة المستهدفة والمقاس (9:16 أم 16:9 أم 1:1)؟", "default": "30 ثانية بمقاس 9:16"},
    ],
    "documentary": [
        {"key": "topic", "question": "ما الموضوع أو السؤال المركزي الذي تريد أن يشدّ المشاهد في أول 3 ثوانٍ؟", "default": "حقيقة علمية أو تاريخية مدهشة"},
        {"key": "tone", "question": "ما الإحساس المطلوب (تأملي، حماسي، غامض، تعليمي)؟", "default": "تأملي معرفي هادئ مع تصاعد بصري"},
        {"key": "duration", "question": "ما المدة المستهدفة للفيديو؟", "default": "60 ثانية عمودي 9:16"},
    ],
    "educational": [
        {"key": "topic", "question": "ما المفهوم التعليمي الذي نريد تبسيطه وما الفئة العمرية؟", "default": "شرح مفهوم علمي/رياضي بمثال بصري حي"},
        {"key": "example", "question": "هل لديك مثال عملي محدد أم أقترح لك مثالًا بصريًا؟", "default": "مثال بصري تفاعلي من الحياة اليومية"},
    ],
}


def get_adaptive_interview_question(project_type: str, known_answers: dict[str, Any]) -> dict[str, Any]:
    """V3.2 Adaptive One-Question-at-a-Time Interview skipping already-known facts."""
    bank = INTERVIEW_BANK.get(project_type, INTERVIEW_BANK["documentary"])
    for item in bank:
        if not known_answers.get(item["key"]):
            return {
                "complete": False,
                "next_key": item["key"],
                "question": item["question"],
                "recommended_default": item["default"],
            }
    return {"complete": True, "next_key": None, "question": None}


def compile_v32_production_prompt(
    state: dict[str, Any],
    target_tool: str = "remotion_motion",
    required_assets: list[dict[str, str]] | None = None,
    motion_specs: list[dict[str, str]] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """V3.2 Tool-Adapted Production Prompt Compiler with REQUIRED INPUT ASSETS,
    executable motion specs, Negative Prompt, and strict NO-MUSIC enforcement."""
    base = compile_production_prompt(state, root=root)
    tool_key = target_tool if target_tool in TOOL_ADAPTER_GUIDES else "remotion_motion"
    assets_list = required_assets or [
        {"file": "voiceover.wav", "role": "Master Arabic narration audio (NO background music)"},
        {"file": "style_contact_sheet.png", "role": "Visual style & palette reference"},
    ]
    motions = motion_specs or [
        {
            "scene": "S01_HOOK",
            "subject": "Primary title + hero graphic",
            "motion": "Starts off-screen bottom (+40px), rises with cubic ease-out in 0.55s, holds 2.0s, dissolves into S02",
            "camera": "Subtle push-in 1.00 -> 1.06 scale over 3.0s",
        }
    ]
    extra = [
        "",
        f"## 4. Target Production Tool Adapter (`{tool_key}`)",
        f"- **Tool Guidance:** {TOOL_ADAPTER_GUIDES[tool_key]}",
        "",
        "## 5. Executable Motion & Camera Specifications",
    ]
    for m in motions:
        extra.append(f"- **{m['scene']}** | Subject: {m['subject']} | Motion: {m['motion']} | Camera: {m['camera']}")
    extra.extend([
        "",
        "## 6. REQUIRED INPUT ASSETS",
    ])
    for a in assets_list:
        extra.append(f"- `{a['file']}` — {a['role']}")
    extra.extend([
        "",
        "## 7. REFERENCE USAGE INSTRUCTIONS",
        "- Match pacing, composition, and lighting contrast from verified reference frames only; never copy copyrighted logos or watermarks.",
        "",
        "## 8. Negative Prompt & Generation Constraints",
        "- NO background music, NO photorealistic 3D human faces, NO static slide decks, NO truncated Arabic captions, NO split isolated Arabic letters, NO watermarks.",
    ])
    full_prompt = base["prompt_markdown"] + "\n".join(extra) + "\n"
    qa_gate = score_prompt_quality(full_prompt, state)
    return {
        "mode": base["mode"],
        "target_tool": tool_key,
        "isolation_clean": base["isolation_clean"],
        "prompt_markdown": full_prompt,
        "prompt_qa_gate": qa_gate,
    }


def score_prompt_quality(prompt_markdown: str, state: dict[str, Any]) -> dict[str, Any]:
    """V3.2 15-Criterion Pre-Delivery Prompt Quality Gate (0-100)."""
    checks = {
        "project_identity": bool(state.get("project_id") and state.get("title")),
        "mode_declared": state.get("mode", "") in prompt_markdown,
        "aspect_ratio_declared": bool(state.get("aspect_ratio")) and str(state.get("aspect_ratio")) in prompt_markdown,
        "idea_present": bool(state.get("decisions", {}).get("idea")),
        "script_present": bool(state.get("decisions", {}).get("script")),
        "style_selected": bool(state.get("decisions", {}).get("style")),
        "visual_hook_arc": "Problem -> Escalation -> Resolution" in prompt_markdown,
        "no_music_guardrail": "STRICT NO-MUSIC DEFAULT" in prompt_markdown,
        "arabic_rtl_guardrail": "Arabic RTL" in prompt_markdown,
        "no_truncation_guardrail": "Never truncate" in prompt_markdown,
        "tool_adapter_present": "Target Production Tool Adapter" in prompt_markdown,
        "executable_motion_specs": "Executable Motion & Camera Specifications" in prompt_markdown,
        "required_input_assets": "REQUIRED INPUT ASSETS" in prompt_markdown,
        "reference_usage_instructions": "REFERENCE USAGE INSTRUCTIONS" in prompt_markdown,
        "negative_prompt_present": "Negative Prompt" in prompt_markdown,
    }
    passed = sum(1 for v in checks.values() if v)
    score = round((passed / len(checks)) * 100)
    missing = [k for k, v in checks.items() if not v]
    return {
        "score": score,
        "max_score": 100,
        "passed_criteria": passed,
        "total_criteria": len(checks),
        "pass": score >= 80 and "no_music_guardrail" not in missing and "required_input_assets" not in missing,
        "missing_criteria": missing,
    }
