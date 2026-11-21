"""Feature B: Knowledge Graph linking Styles (32), Logos (17), Ref Videos (52), Prompts & Engines."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from . import MODES, repo_root


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_knowledge_graph(root: Path | None = None, write_output: bool = True) -> dict[str, Any]:
    r = repo_root(root)
    styles_raw = _read_csv(r / "03_STYLE_LIBRARY/STYLE_REGISTRY.csv")
    logos_raw = _read_csv(r / "04_LOGO_ANIMATION_LIBRARY/LOGO_REGISTRY.csv")

    # Locate reference video cards
    ref_cards_dir = r / "07_REFERENCE_MEDIA"
    ref_cards = {
        p.stem.upper(): p.relative_to(r).as_posix()
        for p in sorted(ref_cards_dir.rglob("*.md"))
        if any(tag in p.stem.upper() for tag in ("REF-", "MSTY-", "MLOGO-"))
    }

    # Index style spec files & prompt family files
    style_specs = {}
    for p in sorted((r / "03_STYLE_LIBRARY").rglob("*.md")):
        m = re.search(r"(STY-\d{3})", p.name, re.IGNORECASE)
        if m:
            style_specs[m.group(1).upper()] = p.relative_to(r).as_posix()

    prompt_files = [
        p.relative_to(r).as_posix()
        for base_dir in (r / "03_STYLE_LIBRARY/STYLE_PROMPTS", r / "06_PROMPT_LIBRARY")
        if base_dir.exists()
        for p in sorted(base_dir.rglob("*.md"))
    ]
    family_prompt_map = {
        "typography": "03_STYLE_LIBRARY/STYLE_PROMPTS/01_TYPOGRAPHY_FAMILY_PROMPT.md",
        "2d": "03_STYLE_LIBRARY/STYLE_PROMPTS/02_2D_ILLUSTRATION_FAMILY_PROMPT.md",
        "illustration": "03_STYLE_LIBRARY/STYLE_PROMPTS/02_2D_ILLUSTRATION_FAMILY_PROMPT.md",
        "data": "03_STYLE_LIBRARY/STYLE_PROMPTS/03_DATA_AND_MAPS_FAMILY_PROMPT.md",
        "map": "03_STYLE_LIBRARY/STYLE_PROMPTS/03_DATA_AND_MAPS_FAMILY_PROMPT.md",
        "depth": "03_STYLE_LIBRARY/STYLE_PROMPTS/04_DEPTH_AND_3D_FAMILY_PROMPT.md",
        "3d": "03_STYLE_LIBRARY/STYLE_PROMPTS/04_DEPTH_AND_3D_FAMILY_PROMPT.md",
        "product": "03_STYLE_LIBRARY/STYLE_PROMPTS/05_PRODUCT_AND_UI_FAMILY_PROMPT.md",
        "ui": "03_STYLE_LIBRARY/STYLE_PROMPTS/05_PRODUCT_AND_UI_FAMILY_PROMPT.md",
        "art": "03_STYLE_LIBRARY/STYLE_PROMPTS/06_ART_AND_IDENTITY_FAMILY_PROMPT.md",
        "identity": "03_STYLE_LIBRARY/STYLE_PROMPTS/06_ART_AND_IDENTITY_FAMILY_PROMPT.md",
        "fikra": "03_STYLE_LIBRARY/STYLE_PROMPTS/07_FIKRA_EXTENDED_FAMILY_PROMPT.md",
    }

    styles_nodes: dict[str, Any] = {}
    for row in styles_raw:
        sid = row.get("Style_ID", "").strip().upper()
        if not sid:
            continue
        fam = row.get("Family_Key", "").strip()
        ref_assets = row.get("Reference_Assets", "")
        linked_refs = sorted(set(re.findall(r"(?:REF-\d{3}|MSTY-\d{2}|MLOGO-\d{2})", ref_assets, re.IGNORECASE)))
        matching_prompts = [pf for pf in prompt_files if fam and fam.lower() in pf.lower()]
        for key, fpath in family_prompt_map.items():
            if (key in fam.lower() or key in row.get("Family_Name", "").lower()) and (r / fpath).exists() and fpath not in matching_prompts:
                matching_prompts.append(fpath)
        if not matching_prompts:
            matching_prompts = ["06_PROMPT_LIBRARY/IMPROVED_PROMPTS/UNIVERSAL_PRODUCTION_PROMPT_V1.md"]
        diff = row.get("Code_Difficulty", "Medium")
        engine_req = (
            "Remotion 4 + React 19 (custom motion components)"
            if "high" in diff.lower() or "3d" in row.get("English_Name", "").lower()
            else "Remotion 4 or HyperFrames HTML5 (deterministic 9:16/16:9)"
        )
        styles_nodes[sid] = {
            "style_id": sid,
            "arabic_name": row.get("Arabic_Name", ""),
            "english_name": row.get("English_Name", ""),
            "family_key": fam,
            "family_name": row.get("Family_Name", ""),
            "slug": row.get("Slug", ""),
            "code_difficulty": diff,
            "readiness_status": row.get("Readiness_Status", ""),
            "use_cases": row.get("Use_Cases", ""),
            "spec_file": style_specs.get(sid),
            "prompt_templates": matching_prompts,
            "reference_video_ids": [x.upper() for x in linked_refs],
            "reference_cards": [ref_cards[x.upper()] for x in linked_refs if x.upper() in ref_cards],
            "execution_requirements": engine_req,
        }

    logos_nodes: dict[str, Any] = {}
    for row in logos_raw:
        lid = row.get("Animation_ID", "").strip().upper()
        if not lid:
            continue
        logos_nodes[lid] = {
            "animation_id": lid,
            "arabic_name": row.get("Arabic_Name", ""),
            "english_name": row.get("English_Name", ""),
            "duration_sec": row.get("Duration_Sec", ""),
            "resolution": row.get("Resolution", ""),
            "reference_tsx": row.get("Reference_TSX", ""),
            "reference_videos": row.get("Reference_Videos", ""),
            "prompt_template": "06_PROMPT_LIBRARY/IMPROVED_PROMPTS/LOGO_ANIMATION_PROMPT_V1.md",
            "execution_requirements": "Remotion 4 SVG Path/Spring Animation + SFX",
        }

    graph = {
        "schema_version": "3.0.0",
        "counts": {
            "modes": len(MODES),
            "styles": len(styles_nodes),
            "logo_animations": len(logos_nodes),
            "reference_cards": len(ref_cards),
            "prompt_files": len(prompt_files),
        },
        "modes": list(MODES),
        "styles": styles_nodes,
        "logo_animations": logos_nodes,
        "reference_cards": ref_cards,
    }

    if write_output:
        out = r / "09_ASSET_AND_RIGHTS_REGISTRY/KNOWLEDGE_GRAPH.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

    return graph


def lookup_style(style_id: str, root: Path | None = None) -> dict[str, Any] | None:
    r = repo_root(root)
    gp = r / "09_ASSET_AND_RIGHTS_REGISTRY/KNOWLEDGE_GRAPH.json"
    graph = json.loads(gp.read_text(encoding="utf-8")) if gp.exists() else build_knowledge_graph(r)
    return graph["styles"].get(style_id.strip().upper())


def lookup_logo(logo_id: str, root: Path | None = None) -> dict[str, Any] | None:
    r = repo_root(root)
    gp = r / "09_ASSET_AND_RIGHTS_REGISTRY/KNOWLEDGE_GRAPH.json"
    graph = json.loads(gp.read_text(encoding="utf-8")) if gp.exists() else build_knowledge_graph(r)
    key = logo_id.strip().upper()
    if key in graph["logo_animations"]:
        return graph["logo_animations"][key]
    for k, v in graph["logo_animations"].items():
        if k.startswith(key + "-") or k == key:
            return v
    return None
