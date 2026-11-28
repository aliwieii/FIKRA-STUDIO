"""V3.6 Visual Quality Engine: Objective FFmpeg/FFprobe/Pillow metrics + Heuristic & Review separation."""
from __future__ import annotations

import json
import math
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .media_intelligence import detect_black_frames, probe_media, sha256_media
from .visual_intelligence import extract_contact_sheet

ASPECT_TARGETS = {
    "9:16": (1080, 1920),
    "16:9": (1920, 1080),
    "1:1": (1080, 1080),
}


def detect_freeze_frames(video_path: Path, noise_db: float = -60.0, duration_sec: float = 1.5) -> dict[str, Any]:
    """Run real FFmpeg freezedetect filter (distinguishing intentional holds from long freezes)."""
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    cmd = [
        "ffmpeg", "-hide_banner", "-i", str(video_path),
        "-vf", f"freezedetect=n={noise_db}dB:d={duration_sec}",
        "-f", "null", "-",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {"measurement_type": "REAL_FFMPEG_FREEZEDETECT", "status": "ERROR", "returncode": res.returncode, "freezes": []}
    freezes = []
    cur: dict[str, float] = {}
    for line in res.stderr.splitlines():
        if "freeze_start:" in line:
            cur = {"start": float(line.split("freeze_start:")[1].strip().split()[0])}
        elif "freeze_duration:" in line and cur:
            cur["duration"] = float(line.split("freeze_duration:")[1].strip().split()[0])
        elif "freeze_end:" in line and cur:
            cur["end"] = float(line.split("freeze_end:")[1].strip().split()[0])
            freezes.append(cur)
            cur = {}
    return {
        "measurement_type": "REAL_FFMPEG_FREEZEDETECT",
        "status": "OK",
        "freeze_count": len(freezes),
        "freezes": freezes,
    }


def _sample_frame_stats(video_path: Path, num_samples: int = 5) -> dict[str, Any]:
    """Extract sample PNGs via FFmpeg and compute objective sharpness, contrast, exposure & flicker."""
    info = probe_media(video_path)
    duration = float(info.get("format", {}).get("duration", 0.0))
    if duration <= 0:
        return {"available": False, "reason": "Zero duration"}

    try:
        from PIL import Image, ImageStat
    except ImportError:
        return {"available": False, "reason": "Pillow unavailable in environment"}

    luma_means, contrasts, sharpnesses, saturations, frame_hashes = [], [], [], [], []
    with tempfile.TemporaryDirectory() as td:
        for i in range(num_samples):
            ts = round(min(max(0.0, duration - 0.05), (duration * i) / max(1, num_samples - 1)), 3)
            fp = Path(td) / f"s_{i}.png"
            r = subprocess.run(
                ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{ts:.3f}", "-i", str(video_path), "-frames:v", "1", "-vf", "scale=360:-2", str(fp)],
                capture_output=True, text=True,
            )
            if r.returncode != 0 or not fp.exists():
                continue
            im = Image.open(fp).convert("RGB")
            gray = im.convert("L")
            st = ImageStat.Stat(gray)
            luma_means.append(st.mean[0])
            contrasts.append(st.stddev[0])

            # Simple finite-difference gradient sharpness
            px = list(gray.getdata())
            w, h = gray.size
            grad_sum = 0.0
            step = 2
            cnt = 0
            for y in range(0, h - 1, step):
                row = y * w
                for x in range(0, w - 1, step):
                    grad_sum += abs(px[row + x + 1] - px[row + x]) + abs(px[row + w + x] - px[row + x])
                    cnt += 1
            sharpnesses.append(grad_sum / max(1, cnt))

            hsv = im.convert("HSV")
            saturations.append(ImageStat.Stat(hsv).mean[1])
            frame_hashes.append(tuple(px[::97]))

    if not luma_means:
        return {"available": False, "reason": "No frames sampled"}

    mean_luma = sum(luma_means) / len(luma_means)
    mean_contrast = sum(contrasts) / len(contrasts)
    mean_sharpness = sum(sharpnesses) / len(sharpnesses)
    mean_sat = sum(saturations) / len(saturations)
    flicker_delta = max(luma_means) - min(luma_means)
    dup_count = sum(1 for i in range(1, len(frame_hashes)) if frame_hashes[i] == frame_hashes[i - 1])

    return {
        "available": True,
        "samples": len(luma_means),
        "mean_luma_0_255": round(mean_luma, 2),
        "contrast_stddev": round(mean_contrast, 2),
        "sharpness_gradient": round(mean_sharpness, 2),
        "color_saturation_mean": round(mean_sat, 2),
        "brightness_flicker_range": round(flicker_delta, 2),
        "consecutive_duplicate_samples": dup_count,
    }


def evaluate_visual_quality(
    video_path: Path,
    expected_aspect: str = "9:16",
    contact_sheet_out: Path | None = None,
    allow_intentional_dark: bool = True,
) -> dict[str, Any]:
    """Comprehensive V3.6 Visual Quality evaluation separating Objective, Heuristic, and Human review."""
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    info = probe_media(video_path)
    v_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    if v_stream is None:
        return {"pass": False, "error": "No video stream found."}

    w, h = int(v_stream.get("width", 0)), int(v_stream.get("height", 0))
    bit_rate = int(info.get("format", {}).get("bit_rate", 0) or 0)
    tw, th = ASPECT_TARGETS.get(expected_aspect, (1080, 1920))
    res_ok = (w >= min(tw, th) and h >= min(tw, th)) and ((w < h) == (tw < th) if tw != th else w == h)

    black = detect_black_frames(video_path)
    freeze = detect_freeze_frames(video_path)
    stats = _sample_frame_stats(video_path, num_samples=5)

    sheet_res = None
    if contact_sheet_out is not None:
        sheet_res = extract_contact_sheet(video_path, contact_sheet_out, ref_id=video_path.stem, num_frames=6)

    # Objective checks
    blocking_failures = []
    if not res_ok:
        blocking_failures.append(f"Resolution {w}x{h} does not match aspect {expected_aspect}")
    if not black["pass"] and not allow_intentional_dark:
        blocking_failures.append(f"Black frames detected: {black['black_intervals_count']}")

    # Heuristic checks (warn without falsely failing intentional dark/minimalist scenes)
    heuristics: list[str] = []
    if stats.get("available"):
        if stats["contrast_stddev"] < 12.0:
            heuristics.append("Low contrast (<12 stddev) — verify subject separation.")
        if stats["sharpness_gradient"] < 2.5:
            heuristics.append("Low edge sharpness — check compression or blur.")
        if stats["brightness_flicker_range"] > 120.0:
            heuristics.append("Large brightness swing across samples — verify intentional palette switches.")
    if bit_rate and bit_rate < 400_000:
        heuristics.append(f"Low bitrate ({bit_rate} bps) may introduce compression artifacts.")

    return {
        "pass": len(blocking_failures) == 0,
        "video_file": video_path.name,
        "video_sha256": sha256_media(video_path),
        "objective_checks": {
            "resolution": f"{w}x{h}",
            "expected_aspect": expected_aspect,
            "resolution_adequate": res_ok,
            "bitrate_bps": bit_rate,
            "black_frames": black,
            "freeze_frames": freeze,
            "frame_stats": stats,
        },
        "heuristic_checks": heuristics,
        "ai_assisted_visual_review": "CONTACT_SHEET_EXTRACTED" if sheet_res else "PENDING_CONTACT_SHEET_INSPECTION",
        "human_review_required": True,
        "disclaimer": "Objective frame metrics and heuristics do not prove storytelling quality or artistic beauty.",
        "contact_sheet": sheet_res,
        "blocking_failures": blocking_failures,
    }
