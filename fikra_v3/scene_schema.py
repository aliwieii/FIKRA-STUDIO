"""V3.6 Data-Driven Scene Schema & Motion Quality Validator."""
from __future__ import annotations

from typing import Any

from .prompt_compiler import assert_no_music_leak

REQUIRED_SCENE_FIELDS = (
    "scene_id", "start_frame", "duration_frames", "visual_style", "scene_objective",
    "background", "assets", "characters", "camera_motion", "element_animations",
    "narration_segment", "captions", "sound_effects", "transition_in", "transition_out", "safe_zones",
)
SUPPORTED_ASPECTS = ("9:16", "16:9", "1:1")


def validate_scene_timeline(
    scenes: list[dict[str, Any]],
    fps: int = 30,
    aspect_ratio: str = "9:16",
    audio_duration_sec: float | None = None,
) -> dict[str, Any]:
    """Validate multi-scene timeline continuity, non-overlap, motion quality, and music policy."""
    if not scenes:
        return {"pass": False, "errors": ["Scenes list cannot be empty."]}
    if aspect_ratio not in SUPPORTED_ASPECTS:
        return {"pass": False, "errors": [f"Unsupported aspect_ratio '{aspect_ratio}'."]}

    errors: list[str] = []
    warnings: list[str] = []
    ordered = sorted(scenes, key=lambda s: int(s.get("start_frame", 0)))

    expected_start = 0
    repeated_transitions = 0
    prev_tr = None

    for idx, sc in enumerate(ordered):
        missing = [f for f in REQUIRED_SCENE_FIELDS if f not in sc]
        if missing:
            errors.append(f"Scene[{idx}] missing required schema fields: {missing}")
            continue
        sf = int(sc["start_frame"])
        df = int(sc["duration_frames"])
        if df <= 0:
            errors.append(f"{sc['scene_id']}: duration_frames must be > 0.")
        if sf < expected_start:
            errors.append(f"{sc['scene_id']}: timeline overlap (starts at {sf}, previous ended at {expected_start}).")
        elif sf > expected_start:
            errors.append(f"{sc['scene_id']}: unintended timeline gap ({expected_start} -> {sf}).")
        expected_start = sf + df

        # Motion quality checks
        cam = str(sc.get("camera_motion", "")).strip().lower()
        anims = sc.get("element_animations") or []
        if (not cam or cam == "none") and not anims:
            warnings.append(f"{sc['scene_id']}: static scene with neither camera_motion nor element_animations.")

        tr = sc.get("transition_in")
        if tr and tr == prev_tr and tr != "cut":
            repeated_transitions += 1
        prev_tr = tr

        # No-music check across scene spec
        ma = assert_no_music_leak(f"{sc.get('sound_effects', '')} {sc.get('narration_segment', '')}")
        if not ma["pass"]:
            errors.append(f"{sc['scene_id']}: music policy leak {ma['leaks']}")

    total_frames = expected_start
    total_sec = round(total_frames / max(1, fps), 2)
    if audio_duration_sec is not None and abs(total_sec - audio_duration_sec) > 2.5:
        warnings.append(f"Video duration {total_sec}s differs from audio duration {audio_duration_sec}s by >2.5s.")
    if repeated_transitions >= 3:
        warnings.append(f"Transition '{prev_tr}' repeated {repeated_transitions + 1} times consecutively; vary transitions purposefully.")

    return {
        "pass": len(errors) == 0,
        "scenes_count": len(ordered),
        "aspect_ratio": aspect_ratio,
        "total_frames": total_frames,
        "total_duration_sec": total_sec,
        "errors": errors,
        "motion_quality_warnings": warnings,
    }
