"""V3.5 TikTok Retention & Views Optimizer + Complexity-Removing Quickstart."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from . import repo_root
from .motion_craft import list_narrative_archetypes
from .style_recommender import recommend_styles

THROAT_CLEARERS = (
    "أهلا بكم", "أهلاً بكم", "مرحبا بكم", "مرحباً بكم",
    "في هذا الفيديو", "اليوم سنتكلم", "السلام عليكم ورحمة الله وبركاته في فيديو جديد",
    "hey guys", "welcome back", "in this video",
)
SPAM_HASHTAGS = {"#fyp", "#foryou", "#foryoupage", "#viral", "#trending", "#اكسبلور"}


def audit_tiktok_retention(
    beats: list[dict[str, Any]],
    hashtags: list[str] | None = None,
    loop_ending: bool = True,
) -> dict[str, Any]:
    """Score and audit a short-form script/storyboard against 2026 TikTok retention drivers."""
    if not beats:
        return {"pass": False, "score_100": 0, "issues": ["No beats provided."]}

    issues: list[str] = []
    strengths: list[str] = []
    score = 100

    first_text = str(beats[0].get("text", "")).lower()
    if any(tc in first_text for tc in THROAT_CLEARERS):
        score -= 25
        issues.append("Opening beat uses a slow throat-clearing intro; start with a 3-second curiosity gap or visual shock.")
    elif float(beats[0].get("duration_sec", 3.0)) > 3.2:
        score -= 10
        issues.append("Opening hook beat exceeds 3.2s; tighten to <= 3.0s for 3-second hold.")
    else:
        strengths.append("Strong 3-second hook opening without filler.")

    slow_beats = [i + 1 for i, b in enumerate(beats) if float(b.get("duration_sec", 2.5)) > 3.8]
    if slow_beats:
        score -= min(25, 8 * len(slow_beats))
        issues.append(f"Pattern-interrupt gap > 3.8s on beat(s): {slow_beats}. Keep visual resets every 2.0-3.5s.")
    else:
        strengths.append("Pattern interrupts stay within the 2.0-3.5s retention sweet spot.")

    if not loop_ending:
        score -= 12
        issues.append("Add a loopable ending line/visual that bridges back into frame 1 for >100% watch time.")
    else:
        strengths.append("Seamless loop ending enabled.")

    tags = [t.strip() for t in (hashtags or []) if t.strip()]
    if tags:
        spam_hits = [t for t in tags if t.lower() in SPAM_HASHTAGS]
        if spam_hits:
            score -= 10
            issues.append(f"Replace generic spam tags {spam_hits} with 3-5 niche search-SEO hashtags.")
        if not (3 <= len(tags) <= 8):
            score -= 8
            issues.append(f"Use 3-5 focused TikTok hashtags (5-8 max); found {len(tags)}.")
        else:
            strengths.append(f"Focused hashtag count ({len(tags)}).")

    return {
        "pass": score >= 75,
        "score_100": max(0, score),
        "beats_count": len(beats),
        "strengths": strengths,
        "issues": issues,
        "safe_zone_rule": "Keep captions/subjects clear of top 14%, bottom 22%, and right 12% TikTok UI overlays.",
    }


def quickstart_blueprint(
    topic: str,
    mode: str = "UNIVERSAL_VIDEO_MODE",
    duration_sec: int = 45,
    root: Path | None = None,
) -> dict[str, Any]:
    """One-shot simplified starter blueprint removing workflow complexity for new/fast projects."""
    r = root or repo_root()
    rec = recommend_styles(topic, mode=mode, top_k=2, root=r)
    top_style = rec[0]["style_id"] if rec else "STY-001"
    archs = list_narrative_archetypes(mode=mode, root=r)
    top_arch = archs[0]["slug"] if archs else "CONTINUOUS_ACTION_EXPLAINER"
    beat_count = max(6, round(duration_sec / 2.8))
    return {
        "mode": mode,
        "topic": topic,
        "duration_sec": duration_sec,
        "aspect_ratio": "9:16",
        "recommended_style": top_style,
        "recommended_archetype": top_arch,
        "recommended_beat_count": beat_count,
        "tiktok_retention_structure": [
            "0.0-2.8s: Visual Hook + Open Loop (NO throat-clearing intro)",
            f"2.8-{max(10, duration_sec - 6)}s: Problem -> Escalation -> Proof beats (pattern interrupt every 2.5-3.5s)",
            f"{max(10, duration_sec - 6)}-{duration_sec}s: Payoff + Loopable Bridge back to Beat 1",
        ],
        "recommended_sfx_pack": ["whoosh", "pop", "tick", "chime"],
        "music_policy": "NO BACKGROUND MUSIC (Voiceover + justified SFX + silence only).",
    }
