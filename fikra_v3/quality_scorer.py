"""V3.6 Evidence-Based Quality Scoring Engine (independent from readiness tiers)."""
from __future__ import annotations

from typing import Any

WEIGHTS = {
    "visual_quality": 25,
    "motion_quality": 15,
    "storytelling": 15,
    "audio_quality": 15,
    "arabic_caption_quality": 10,
    "consistency": 10,
    "technical_delivery": 10,
}


def compute_evidence_based_quality_score(
    visual_report: dict[str, Any] | None = None,
    scene_report: dict[str, Any] | None = None,
    storytelling_report: dict[str, Any] | None = None,
    audio_report: dict[str, Any] | None = None,
    arabic_report: dict[str, Any] | None = None,
    consistency_report: dict[str, Any] | None = None,
    technical_render_verified: bool = False,
) -> dict[str, Any]:
    """Compute a strict evidence-grounded 0-100 quality report. Never grants final PASS without real render & checks."""
    blocking: list[str] = []
    unverified: list[str] = []
    breakdown: dict[str, dict[str, Any]] = {}

    if not technical_render_verified or visual_report is None:
        blocking.append("NO_REAL_RENDER_EVIDENCE: Final video score cannot pass without an executed render & FFprobe check.")
        unverified.append("visual_quality")
        breakdown["visual_quality"] = {"score": 0, "max": 25, "verified": False}
    else:
        v_ok = bool(visual_report.get("pass"))
        h_pen = min(5, len(visual_report.get("heuristic_checks", [])) * 2)
        v_score = max(0, (25 - h_pen) if v_ok else 10)
        if not v_ok:
            blocking.extend(visual_report.get("blocking_failures", ["Visual quality check failed."]))
        breakdown["visual_quality"] = {"score": v_score, "max": 25, "verified": True, "sha256": visual_report.get("video_sha256")}

    if scene_report is None:
        unverified.append("motion_quality")
        breakdown["motion_quality"] = {"score": 0, "max": 15, "verified": False}
    else:
        m_ok = bool(scene_report.get("pass"))
        w_pen = min(4, len(scene_report.get("motion_quality_warnings", [])) * 2)
        breakdown["motion_quality"] = {"score": (15 - w_pen) if m_ok else 5, "max": 15, "verified": True}
        if not m_ok:
            blocking.extend(scene_report.get("errors", ["Scene timeline failed."]))

    if storytelling_report is None:
        unverified.append("storytelling")
        breakdown["storytelling"] = {"score": 0, "max": 15, "verified": False}
    else:
        st_raw = float(storytelling_report.get("storytelling_score_100", 0.0))
        breakdown["storytelling"] = {"score": round(15 * (st_raw / 100.0), 1), "max": 15, "verified": True}
        if not storytelling_report.get("pass"):
            blocking.append("Storytelling rubric did not pass.")

    if audio_report is None:
        unverified.append("audio_quality")
        breakdown["audio_quality"] = {"score": 0, "max": 15, "verified": False}
    else:
        a_ok = bool(audio_report.get("pass"))
        breakdown["audio_quality"] = {"score": 15 if a_ok else 6, "max": 15, "verified": True, "sha256": audio_report.get("sha256")}
        if not a_ok:
            blocking.extend(audio_report.get("blocking_failures", ["Audio mastering check failed."]))

    if arabic_report is None:
        unverified.append("arabic_caption_quality")
        breakdown["arabic_caption_quality"] = {"score": 0, "max": 10, "verified": False}
    else:
        ar_ok = bool(arabic_report.get("pass"))
        breakdown["arabic_caption_quality"] = {"score": 10 if ar_ok else 3, "max": 10, "verified": True}
        if not ar_ok:
            blocking.append("Arabic caption render/text QA failed.")

    if consistency_report is None:
        unverified.append("consistency")
        breakdown["consistency"] = {"score": 0, "max": 10, "verified": False}
    else:
        c_status = consistency_report.get("consistency_status", {})
        c_score = 10 if c_status.get("visual_verified_consistent") else 7
        breakdown["consistency"] = {"score": c_score, "max": 10, "verified": bool(c_status.get("visual_verified_consistent"))}

    if not technical_render_verified:
        unverified.append("technical_delivery")
        breakdown["technical_delivery"] = {"score": 0, "max": 10, "verified": False}
    else:
        breakdown["technical_delivery"] = {"score": 10, "max": 10, "verified": True}

    total = round(sum(v["score"] for v in breakdown.values()), 1)
    can_pass = (len(blocking) == 0) and technical_render_verified and (total >= 75.0)
    return {
        "pass": can_pass,
        "status": "VERIFIED_PASS" if can_pass else ("UNVERIFIED_INCOMPLETE" if not technical_render_verified else "BLOCKED_FAIL"),
        "total_score_100": total,
        "breakdown": breakdown,
        "unverified_aspects": unverified,
        "blocking_failures": blocking,
    }
