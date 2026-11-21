"""Feature K: Production Readiness Score — evidence-gated 0-100 score using REAL ffprobe & SHA-256 verification."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .approval_guard import verify_approval_integrity
from .media_intelligence import probe_media, sha256_media


def score_readiness(state: dict[str, Any]) -> dict[str, Any]:
    ev = state.get("evidence", {})
    locks = verify_approval_integrity(state)
    score = 0
    reasons = []

    # 1. PROMPT_READY (25)
    prompt_ready = bool(ev.get("prompt_compiled")) and locks["valid"]
    if prompt_ready:
        score += 25
    else:
        reasons.append("Prompt not compiled or approval locks invalid.")

    # 2. SPEC_READY (45)
    spec_ready = prompt_ready and bool(ev.get("spec_validated")) and bool(state.get("decisions", {}).get("style"))
    if spec_ready:
        score += 20
    else:
        reasons.append("Style/storyboard specification not validated.")

    # 3. CODE_READY (65)
    code_ready = spec_ready and bool(ev.get("code_validated"))
    if code_ready:
        score += 20
    else:
        reasons.append("Production engine code/timeline not validated.")

    # 4. BUILD_TESTED (85) — requires non-empty build log with no fatal errors
    build_log = ev.get("build_log_path")
    build_tested = False
    if code_ready and build_log and Path(build_log).exists():
        log_txt = Path(build_log).read_text(encoding="utf-8", errors="ignore").strip()
        if log_txt and "BUILD FAILED" not in log_txt.upper() and "ERROR:" not in log_txt.upper():
            build_tested = True
    if build_tested:
        score += 20
    else:
        reasons.append("No verified clean build log artifact (BUILD_TESTED blocked).")

    # 5. RENDER_TESTED (100) — MUST verify real MP4 via ffprobe AND matching SHA-256 QA report JSON
    render_out = ev.get("render_output_path")
    qa_report_path = ev.get("qa_report_path")
    render_tested = False
    if build_tested and render_out and Path(render_out).exists() and qa_report_path and Path(qa_report_path).exists():
        try:
            mp4 = Path(render_out)
            actual_sha = sha256_media(mp4)
            info = probe_media(mp4)
            v_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
            qa_data = json.loads(Path(qa_report_path).read_text(encoding="utf-8"))
            if (
                v_stream is not None
                and float(info.get("format", {}).get("duration", 0.0)) > 0
                and qa_data.get("pass") is True
                and qa_data.get("video_sha256") == actual_sha
            ):
                render_tested = True
            else:
                reasons.append("QA report failed or video SHA-256 does not match rendered MP4.")
        except Exception as exc:
            reasons.append(f"Real media verification failed: {exc}")
    else:
        reasons.append("Missing real rendered MP4 or SHA-256-bound QA report JSON (RENDER_TESTED blocked).")

    if render_tested:
        score += 15

    tier = "UNVERIFIED"
    if render_tested:
        tier = "RENDER_TESTED"
    elif build_tested:
        tier = "BUILD_TESTED"
    elif code_ready:
        tier = "CODE_READY"
    elif spec_ready:
        tier = "SPEC_READY"
    elif prompt_ready:
        tier = "PROMPT_READY"

    return {
        "score": score,
        "max_score": 100,
        "readiness_tier": tier,
        "blocking_reasons": reasons,
    }
