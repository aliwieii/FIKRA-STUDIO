"""V3.6 Style Execution Engine: Converts any of the 32 styles into an executable spec without inflating readiness."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import repo_root
from .knowledge_graph import lookup_style

VALID_READINESS = ("CATALOG_ONLY", "SPEC_READY", "REFERENCE_ONLY", "RENDER_TESTED")


def build_executable_style_spec(
    style_id: str,
    mode: str = "UNIVERSAL_VIDEO_MODE",
    root: Path | None = None,
) -> dict[str, Any]:
    """Generate a 15-field executable style specification grounded in repo data."""
    r = root or repo_root()
    kg_info = lookup_style(style_id, root=r)
    if not kg_info or not kg_info.get("style_id"):
        raise KeyError(f"Unknown style_id: {style_id}")
    st = kg_info
    ux_path = r / "03_STYLE_LIBRARY/STYLE_UX_CATALOG_V33.json"
    ux_item = {}
    if ux_path.exists():
        for it in json.loads(ux_path.read_text(encoding="utf-8")).get("styles", []):
            if it["style_id"] == style_id:
                ux_item = it
                break

    spec_file = st.get("spec_file", "")
    has_spec = bool(spec_file and (r / spec_file).exists())
    has_refs = bool(kg_info.get("reference_video_ids"))

    # Honest readiness status — never upgrade to RENDER_TESTED without verified render evidence
    raw_status = str(st.get("readiness_status", "")).upper()
    if raw_status in VALID_READINESS and raw_status != "RENDER_TESTED":
        readiness = raw_status
    elif has_spec:
        readiness = "SPEC_READY"
    elif has_refs:
        readiness = "REFERENCE_ONLY"
    else:
        readiness = "CATALOG_ONLY"

    dark_styles = {"STY-019", "STY-021", "STY-023", "STY-027", "STY-030", "STY-031"}
    is_dark = style_id in dark_styles
    palette = (
        {"bg": "#060B14", "primary": "#F8FAFC", "accent": "#D4AF37", "secondary": "#38BDF8"}
        if is_dark
        else {"bg": "#F7F4EE", "primary": "#18181B", "accent": "#EE7B30", "secondary": "#2563EB"}
    )

    return {
        "style_id": style_id,
        "mode": mode,
        "visual_identity": ux_item.get("simplified_arabic_name", st.get("name", style_id)),
        "color_palette": palette,
        "typography": {"arabic_font": "IBM Plex Sans Arabic / Cairo / Noto Sans Arabic", "rtl": True, "min_mobile_px": 30},
        "composition": "Centered focal subject with clear mobile safe zones (top 14%, bottom 22%, right 12%)" if mode == "FIKRA_CHANNEL_MODE" else "Balanced focal hierarchy matching target aspect ratio",
        "lighting": "Soft rim + subtle key spotlight" if is_dark else "Clean diffuse daylight",
        "background_treatment": "Living background with subtle parallax drift or fine film grain (never static)",
        "motion_language": "Frame-driven spring() & interpolate() with staggered reveals",
        "camera_language": "Motivated push-in (3-5% per beat) and controlled tracking",
        "transition_grammar": "Purposeful iris/wipe/whip-pan matched to narrative beats",
        "character_rules": "2D illustrated or stylized figures; NO photorealistic 3D humans",
        "asset_requirements": ["Vector SVG or verified high-res layer assets", "Clean voiceover + justified SFX only"],
        "rendering_requirements": {"fps": 30, "codec": "h264", "audio_codec": "aac"},
        "negative_constraints": ["NO background music", "NO static pan/zoom slides", "NO Arabic letter splitting"],
        "verified_reference_links": list(kg_info.get("reference_video_ids", [])),
        "readiness_status": readiness,
    }
