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
        if max_difficulty and max_difficulty.lower() == "low" and "high" in node.get("code_difficulty", "").lower():
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
