"""V3.2 Visual Intelligence Engine — Honest Reference Access, FFmpeg Contact Sheets,
7-Dimension Visual Analysis, and Localized Post-Production Video Review Diff."""
from __future__ import annotations

import math
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .media_intelligence import probe_media, sha256_media

VISUAL_REVIEW_STATUSES = (
    "ORIGINAL_WATCHED",
    "EXTRACTED_FRAME",
    "CARD_TEXT_ONLY",
    "AI_CONCEPT_PREVIEW",
    "UNVERIFIED",
)

AI_CONCEPT_WATERMARK_LABEL = "AI-GENERATED STYLE CONCEPT — NOT AN ORIGINAL REFERENCE"


def verify_reference_access(ref_id: str, media_path: Path | None = None, card_path: Path | None = None) -> dict[str, Any]:
    """Honestly report whether a reference video/image was actually accessed vs card-text-only or unavailable."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if media_path and media_path.exists():
        info = probe_media(media_path)
        v_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
        a_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
        return {
            "reference_id": ref_id,
            "accessible": True,
            "source_type": "ORIGINAL_MEDIA",
            "visual_review_status": "EXTRACTED_FRAME" if v_stream else "UNVERIFIED",
            "source_path": str(media_path),
            "sha256": sha256_media(media_path),
            "duration_sec": round(float(info.get("format", {}).get("duration", 0.0)), 3),
            "width": v_stream.get("width") if v_stream else None,
            "height": v_stream.get("height") if v_stream else None,
            "has_audio": a_stream is not None,
            "last_verified": now,
        }
    if card_path and card_path.exists():
        return {
            "reference_id": ref_id,
            "accessible": False,
            "source_type": "ANALYSIS_CARD_ONLY",
            "visual_review_status": "CARD_TEXT_ONLY",
            "source_path": str(card_path),
            "warning": "Original video file not locally accessible; rely ONLY on text card metadata and never claim to have watched the video.",
            "last_verified": now,
        }
    return {
        "reference_id": ref_id,
        "accessible": False,
        "source_type": "MISSING",
        "visual_review_status": "UNVERIFIED",
        "warning": "Reference media and analysis card unavailable; do not fabricate visual analysis.",
        "last_verified": now,
    }


def extract_contact_sheet(
    video_path: Path,
    output_png: Path,
    ref_id: str,
    num_frames: int = 6,
    thumb_width: int = 320,
) -> dict[str, Any]:
    """Extract evenly distributed frames (including first & final) via FFmpeg and build a labeled Contact Sheet PNG."""
    if not video_path.exists():
        raise FileNotFoundError(f"Cannot extract Contact Sheet: video not found at {video_path}")
    if num_frames < 2:
        raise ValueError("num_frames must be >= 2 to inspect more than a single frame.")

    try:
        from PIL import Image, ImageDraw
        has_pil = True
    except ImportError:
        has_pil = False

    info = probe_media(video_path)
    duration = float(info.get("format", {}).get("duration", 0.0))
    v_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    if v_stream is None or duration <= 0:
        raise RuntimeError(f"Invalid video stream or zero duration in {video_path}")

    fps_str = str(v_stream.get("r_frame_rate", "30/1"))
    if "/" in fps_str:
        n, d = fps_str.split("/", 1)
        fps = float(n) / max(1.0, float(d))
    else:
        fps = float(fps_str or 30.0)

    # First frame (0.0s), intermediate frames, and near-final frame
    timestamps = [round(min(max(0.0, duration - 0.05), (duration * i) / (num_frames - 1)), 3) for i in range(num_frames)]
    timestamps[-1] = round(max(0.0, duration - 0.05), 3)

    sampled = []
    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        thumbs = []
        for idx, ts in enumerate(timestamps):
            frame_png = td_p / f"f_{idx:02d}.png"
            res = subprocess.run(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", f"{ts:.3f}", "-i", str(video_path),
                    "-frames:v", "1", "-vf", f"scale={thumb_width}:-2",
                    str(frame_png),
                ],
                capture_output=True, text=True,
            )
            if res.returncode != 0 or not frame_png.exists():
                raise RuntimeError(f"FFmpeg frame extraction failed at t={ts}s: {res.stderr.strip()}")
            fno = int(round(ts * fps))
            if has_pil:
                im = Image.open(frame_png).convert("RGB")
                thumbs.append((ts, fno, im))
            sampled.append({"index": idx + 1, "timecode_sec": ts, "frame_number": fno})

        cols = min(3, num_frames)
        rows = math.ceil(num_frames / cols)
        output_png.parent.mkdir(parents=True, exist_ok=True)

        if has_pil:
            tw, th = thumbs[0][2].size
            header_h, label_h, pad = 54, 24, 12
            sheet_w = cols * tw + (cols + 1) * pad
            sheet_h = header_h + rows * (th + label_h + pad) + pad
            sheet = Image.new("RGB", (sheet_w, sheet_h), (10, 15, 28))
            draw = ImageDraw.Draw(sheet)
            draw.text(
                (pad, 12),
                f"FIKRA V3.3 CONTACT SHEET | {ref_id} | {video_path.name} | {duration:.2f}s | STATUS: EXTRACTED_FRAME",
                fill=(245, 158, 11),
            )
            for idx, (ts, fno, im) in enumerate(thumbs):
                r_i, c_i = divmod(idx, cols)
                x = pad + c_i * (tw + pad)
                y = header_h + r_i * (th + label_h + pad)
                sheet.paste(im, (x, y))
                draw.text((x + 4, y + th + 4), f"t={ts:05.2f}s | f#{fno}", fill=(226, 232, 240))
            sheet.save(output_png)
        else:
            # Zero-dependency FFmpeg native tile fallback (works in clean CI without Pillow)
            tile_res = subprocess.run(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-framerate", "1", "-i", str(td_p / "f_%02d.png"),
                    "-vf", f"tile={cols}x{rows}:padding=12:margin=12:color=0x0a0f1c",
                    "-frames:v", "1", str(output_png),
                ],
                capture_output=True, text=True,
            )
            if tile_res.returncode != 0 or not output_png.exists():
                raise RuntimeError(f"FFmpeg contact sheet tiling failed: {tile_res.stderr.strip()}")

    return {
        "reference_id": ref_id,
        "source_file": video_path.name,
        "source_sha256": sha256_media(video_path),
        "visual_review_status": "EXTRACTED_FRAME",
        "output_contact_sheet": str(output_png),
        "duration_sec": round(duration, 3),
        "fps": round(fps, 2),
        "frames_extracted": len(sampled),
        "samples": sampled,
    }


def create_visual_analysis_template(ref_id: str, access_info: dict[str, Any]) -> dict[str, Any]:
    """Build a 7-dimension structured visual analysis card honoring source truth."""
    has_audio = bool(access_info.get("has_audio"))
    return {
        "reference_id": ref_id,
        "visual_review_status": access_info.get("visual_review_status", "UNVERIFIED"),
        "dimensions": {
            "A_visual_composition": "Pending human/vision review of extracted frames",
            "B_animation": "Pending motion velocity, easing & beat-sync inspection",
            "C_camera": "Pending shot scale, angle & movement inspection",
            "D_lighting_and_materials": "Pending lighting direction, contrast & texture notes",
            "E_typography_rtl": "Pending Arabic RTL shaping, font & legibility inspection",
            "F_editing_and_timing": "Pending cut rhythm & transition inspection",
            "G_audio": "Ready for FFmpeg audio analysis" if has_audio else "UNAVAILABLE — no audio stream verified",
        },
        "timecode_columns": ["Timecode", "Visual Event", "Camera", "Motion", "Text", "Audio", "Transition"],
        "timecode_rows": [],
    }


def build_video_review_report(scenes_diff: list[dict[str, str]]) -> dict[str, Any]:
    """Generate a localized Scene|Expected|Actual|Difference|Severity|Prompt Fix review report."""
    lines = [
        "| Scene | Expected | Actual | Difference | Severity | Prompt Fix |",
        "|---|---|---|---|---|---|",
    ]
    affected = []
    for row in scenes_diff:
        sev = row.get("severity", "LOW").upper()
        if sev in {"CRITICAL", "HIGH", "MEDIUM"}:
            affected.append(row.get("scene", ""))
        lines.append(
            f"| {row.get('scene','')} | {row.get('expected','')} | {row.get('actual','')} "
            f"| {row.get('difference','')} | {sev} | {row.get('prompt_fix','')} |"
        )
    return {
        "total_scenes_reviewed": len(scenes_diff),
        "localized_fix_scenes": affected,
        "full_rerender_required": len(affected) > max(1, len(scenes_diff) // 2),
        "markdown_table": "\n".join(lines),
    }


def build_style_bible(
    style_id: str,
    simplified_arabic_name: str,
    technical_name: str,
    access_info: dict[str, Any],
    aspect_ratio: str = "9:16",
) -> dict[str, Any]:
    """V3.3 Structured 12-Section STYLE BIBLE grounded in actual reference review status."""
    status = access_info.get("visual_review_status", "UNVERIFIED")
    return {
        "style_id": style_id,
        "visual_review_status": status,
        "sections": {
            "1_visual_identity": f"{simplified_arabic_name} ({technical_name})",
            "2_color_palette": {"bg": "#060B14", "surface": "#0F1B2E", "primary_text": "#F8FAFC", "accent_gold": "#F59E0B", "accent_cyan": "#38BDF8"},
            "3_typography": "Arabic RTL (Noto Kufi / Cairo / Amiri for Quran), zero isolated letters, rolling zero-drop captions.",
            "4_composition": f"Safe-zone framed for {aspect_ratio}, clear visual hierarchy and generous negative space.",
            "5_camera_language": "Controlled purposeful push-ins, smooth tracking, zero disorienting jitter.",
            "6_animation_language": "100% frame-driven purposeful motion; zero static slides.",
            "7_transitions": "Dynamic motivated cuts, soft cross-dissolves, or geometric wipes.",
            "8_lighting": "Clean directional stylized lighting with readable figure-ground contrast.",
            "9_timing": "Visual hook within 0-3s; Problem -> Escalation -> Resolution pacing.",
            "10_sound_direction": "STRICT NO BACKGROUND MUSIC (voiceover, justified SFX, ambience, or intentional silence only).",
            "11_production_constraints": "No photorealistic 3D humans; preserve locked user approvals; honor copyright.",
            "12_reference_evidence": {
                "accessible": bool(access_info.get("accessible")),
                "status": status,
                "source_path": access_info.get("source_path"),
            },
        },
    }
