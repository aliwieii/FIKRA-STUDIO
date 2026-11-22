"""Feature G: Style Recommender — ranks the 32 verified styles by topic, mood, and mode."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .knowledge_graph import build_knowledge_graph


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[؀-ۿa-zA-Z0-9]+", text.lower()))


def recommend_styles(
    topic: str,
    mode: str = "UNIVERSAL_VIDEO_MODE",
    max_difficulty: str | None = None,
    top_k: int = 5,
    root: Path | None = None,
) -> list[dict[str, Any]]:
    graph = build_knowledge_graph(root, write_output=False)
    q_tokens = _tokenize(topic)
    scored = []
    for sid, node in graph["styles"].items():
        corpus = " ".join([
            node.get("arabic_name", ""),
            node.get("english_name", ""),
            node.get("family_name", ""),
            node.get("use_cases", ""),
            node.get("slug", ""),
        ])
        c_tokens = _tokenize(corpus)
        overlap = len(q_tokens & c_tokens)
        score = overlap * 20

        # Domain heuristics
        tl = topic.lower()
        en = node.get("english_name", "").lower()
        fam = node.get("family_key", "").lower()
        if any(k in tl for k in ["كون", "فضاء", "ثقب", "علم", "space", "cosmos", "science"]):
            if any(k in en + fam for k in ["3d", "space", "dark", "cinematic", "data", "infographic"]):
                score += 18
        if any(k in tl for k in ["تاريخ", "قص", "وثائق", "history", "story", "documentary"]):
            if any(k in en + fam for k in ["paper", "collage", "editorial", "illustrated", "documentary"]):
                score += 18
        if any(k in tl for k in ["رياضيات", "معادلة", "تعليم", "math", "lesson", "whiteboard", "chalk"]):
            if any(k in en + fam for k in ["whiteboard", "chalk", "motion", "infographic", "2d"]):
                score += 20
        if mode == "STICKMAN_COMEDY_MODE" and "stickman" in (en + corpus.lower()):
            score += 40
        diff_val = node.get("code_difficulty", "").lower()
        if max_difficulty and max_difficulty.lower() in ("low", "سهل") and ("high" in diff_val or "صعب" in diff_val):
            score -= 15

        # Tie-breaker by reference richness
        score += min(10, len(node.get("reference_video_ids", [])) * 2)
        scored.append((score, sid, node))

    scored.sort(key=lambda x: (-x[0], x[1]))
    results = []
    for sc, sid, node in scored[:top_k]:
        results.append({
            "style_id": sid,
            "arabic_name": node["arabic_name"],
            "english_name": node["english_name"],
            "family_name": node["family_name"],
            "score": sc,
            "code_difficulty": node["code_difficulty"],
            "spec_file": node["spec_file"],
            "reference_video_ids": node["reference_video_ids"],
            "execution_requirements": node["execution_requirements"],
        })
    return results


READINESS_REFERENCE_SCORE = {
    "RENDER_TESTED": 10.0,
    "BUILD_TESTED": 9.0,
    "SPEC_READY": 7.0,
    "REFERENCE_ONLY": 6.0,
    "CATALOG_ONLY": 3.5,
}


def compare_styles(
    topic: str,
    mode: str = "UNIVERSAL_VIDEO_MODE",
    target_tool: str = "remotion_motion",
    top_k: int = 3,
    root: Path | None = None,
) -> dict[str, Any]:
    """V3.2 Weighted 6-Criteria Style Comparison Engine (Idea 25%, Visual 25%, Narrative 15%,
    Tool Feasibility 15%, Consistency 10%, Reference Verification 10%). Caps unverified confidence."""
    graph = build_knowledge_graph(root, write_output=False)
    q_tokens = _tokenize(topic)
    candidates = []
    for sid, node in graph["styles"].items():
        corpus = " ".join([
            node.get("arabic_name", ""), node.get("english_name", ""),
            node.get("family_name", ""), node.get("use_cases", ""), node.get("slug", ""),
        ])
        overlap = len(q_tokens & _tokenize(corpus))
        idea_fit = min(25.0, 10.0 + overlap * 5.0)
        visual_fit = 20.0 if ("2d" in corpus.lower() or "motion" in corpus.lower() or "infographic" in corpus.lower()) else 16.0
        if "3d" in node.get("english_name", "").lower() and mode == "FIKRA_CHANNEL_MODE":
            visual_fit -= 4.0  # Prefer 2D / creative motion identity
        narrative_fit = 13.0 if node.get("spec_file") else 9.0
        diff_val = node.get("code_difficulty", "")
        tool_feas = 14.0 if ("سهل" in diff_val or "low" in diff_val.lower()) else (11.0 if "متوسط" in diff_val else 8.0)
        consistency = 9.0 if node.get("prompt_templates") else 6.0
        status = node.get("readiness_status", "CATALOG_ONLY").upper()
        ref_verif = READINESS_REFERENCE_SCORE.get(status, 3.5)
        if node.get("reference_video_ids"):
            ref_verif = min(10.0, ref_verif + 1.5)

        total = round(idea_fit + visual_fit + narrative_fit + tool_feas + consistency + ref_verif, 1)
        confidence = "HIGH" if status in {"RENDER_TESTED", "BUILD_TESTED"} else ("MEDIUM" if status in {"SPEC_READY", "REFERENCE_ONLY"} else "LOW_UNVERIFIED_CATALOG")
        cons = []
        if status == "CATALOG_ONLY":
            cons.append("Catalog-only style — lacks verified visual reference frames.")
        if "صعب" in diff_val:
            cons.append("Higher production/coding complexity.")
        if not node.get("reference_video_ids"):
            cons.append("No linked reference video ID yet.")

        candidates.append({
            "style_id": sid,
            "arabic_name": node["arabic_name"],
            "english_name": node["english_name"],
            "readiness_status": status,
            "confidence": confidence,
            "total_score": total,
            "breakdown": {
                "idea_fit_25": idea_fit,
                "visual_fit_25": visual_fit,
                "narrative_fit_15": narrative_fit,
                "tool_feasibility_15": tool_feas,
                "consistency_10": consistency,
                "reference_verification_10": ref_verif,
            },
            "pros": [f"Matches family: {node['family_name']}", f"Use cases: {node['use_cases'][:80]}"],
            "cons": cons or ["No major blockers identified."],
            "spec_file": node["spec_file"],
            "reference_video_ids": node["reference_video_ids"],
        })

    candidates.sort(key=lambda x: (-x["total_score"], x["style_id"]))
    top = candidates[:max(2, top_k)]
    return {
        "topic": topic,
        "mode": mode,
        "target_tool": target_tool,
        "best_choice": top[0] if top else None,
        "alternative": top[1] if len(top) > 1 else None,
        "compared_styles": top,
    }
