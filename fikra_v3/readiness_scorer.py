"""Feature K: Production Readiness Score — evidence-gated 0-100 score & strict tier separation."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .approval_guard import verify_approval_integrity


def score_readiness(state: dict[str, Any]) -> dict[str, Any]:
    ev = state.get("evidence", {})
    locks = verify_approval_integrity(state)
    score = 0
    reasons = []

    # 1. PROMPT_READY (up to 25)
    prompt_ready = bool(ev.get("prompt_compiled")) and locks["valid"]
    if prompt_ready:
        score += 25
    else:
        reasons.append("Prompt not compiled or approval locks invalid.")

    # 2. SPEC_READY (up to 45)
    spec_ready = prompt_ready and bool(ev.get("spec_validated")) and bool(state.get("decisions", {}).get("style"))
    if spec_ready:
        score += 20
    else:
        reasons.append("Style/storyboard specification not validated.")

    # 3. CODE_READY (up to 65)
    code_ready = spec_ready and bool(ev.get("code_validated"))
    if code_ready:
        score += 20
    else:
        reasons.append("Production engine code/timeline not validated.")

    # 4. BUILD_TESTED (up to 85) — requires existing build log file
    build_log = ev.get("build_log_path")
    build_tested = code_ready and bool(build_log and Path(build_log).exists())
    if build_tested:
        score += 20
    else:
        reasons.append("No verified build log artifact (BUILD_TESTED blocked).")

    # 5. RENDER_TESTED (up to 100) — requires existing render output + media QA pass
    render_out = ev.get("render_output_path")
    render_tested = build_tested and bool(render_out and Path(render_out).exists()) and bool(ev.get("media_qa_passed"))
    if render_tested:
        score += 15
    else:
        reasons.append("No verified rendered video + Media QA pass (RENDER_TESTED blocked).")

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
