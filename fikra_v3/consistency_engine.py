"""V3.6 Consistency Engine: Character/Style Bible + Asset Identity Records & Visual vs Textual separation."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .media_intelligence import sha256_media


def build_consistency_manifest(
    project_id: str,
    style_spec: dict[str, Any],
    characters: list[dict[str, Any]] | None = None,
    fixed_assets: list[Path] | None = None,
) -> dict[str, Any]:
    """Create a Consistency Manifest binding Style Bible, Character Bible, and Asset SHA-256 hashes."""
    asset_records = []
    for p in (fixed_assets or []):
        if p.exists() and p.is_file():
            asset_records.append({
                "asset_name": p.name,
                "path": str(p),
                "sha256": sha256_media(p),
                "size_bytes": p.stat().st_size,
                "visual_verified": False,
            })
        else:
            asset_records.append({
                "asset_name": str(p),
                "path": str(p),
                "sha256": None,
                "missing": True,
                "visual_verified": False,
            })

    return {
        "project_id": project_id,
        "style_bible": {
            "style_id": style_spec.get("style_id"),
            "color_palette": style_spec.get("color_palette"),
            "typography": style_spec.get("typography"),
            "lighting": style_spec.get("lighting"),
            "background_treatment": style_spec.get("background_treatment"),
        },
        "character_bible": characters or [],
        "asset_identity_records": asset_records,
        "consistency_status": {
            "textual_spec_consistent": True,
            "visual_verified_consistent": False,
            "note": "Textual consistency in Character/Style Bible does not prove visual frame consistency until Contact Sheet inspection.",
        },
    }
