"""Feature C: Asset Intelligence — Unified ASSET_REGISTRY (JSON, CSV, SQLite) with SHA-256."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import repo_root

SELF_GENERATED = {
    "09_ASSET_AND_RIGHTS_REGISTRY/ASSET_REGISTRY.json",
    "09_ASSET_AND_RIGHTS_REGISTRY/ASSET_REGISTRY.csv",
    "09_ASSET_AND_RIGHTS_REGISTRY/ASSET_REGISTRY.sqlite",
    "09_ASSET_AND_RIGHTS_REGISTRY/ASSET_REGISTRY_CHECKSUMS.json",
    "09_ASSET_AND_RIGHTS_REGISTRY/KNOWLEDGE_GRAPH.json",
    "SYSTEM_MANIFEST.json",
}

EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".pytest_cache"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_asset(rel: str) -> tuple[str, str, str]:
    """Return (category, usage_type, rights_status)."""
    top = rel.split("/")[0]
    if top == "03_STYLE_LIBRARY":
        return "style_library", "visual_direction", "Internal/Open-Source"
    if top == "04_LOGO_ANIMATION_LIBRARY":
        return "logo_library", "logo_motion", "Internal/Open-Source"
    if top == "06_PROMPT_LIBRARY":
        return "prompt_library", "prompt_engineering", "Internal/Proprietary"
    if top == "07_REFERENCE_MEDIA":
        return "reference_media", "reference_analysis", "Reference-Only/Attribution-Required"
    if top == "08_PROJECT_ASSETS":
        return "production_engine", "code_and_templates", "Internal/MIT-Compatible"
    if top == "fikra_v3":
        return "v3_runtime", "executable_engine", "Internal/MIT"
    if top == "tests":
        return "qa_tests", "automated_verification", "Internal/MIT"
    if top == "archive":
        return "baseline_archive", "immutable_reference", "Immutable-Baseline"
    if top == "99_SOURCE_ORIGINALS":
        return "source_originals", "immutable_source", "Original-Source"
    if top in {"00_START_HERE", "01_SYSTEM_CORE", "02_WORKFLOWS"}:
        return "system_core", "agent_governance", "Internal/Core"
    if top in {"05_IDEAS_AND_KNOWLEDGE"}:
        return "knowledge_base", "content_research", "Internal/Research"
    if top in {"09_ASSET_AND_RIGHTS_REGISTRY", "10_QA_AND_TESTING", "11_VERSIONING_AND_DOCUMENTATION"}:
        return "governance_qa", "audit_and_registry", "Internal/Governance"
    return "root_documentation", "agent_entrypoint", "Internal/Open-Source"


def extract_linked_ids(rel: str) -> dict[str, list[str]]:
    name = Path(rel).name
    styles = sorted(set(re.findall(r"STY-\d{3}", name, re.IGNORECASE)))
    logos = sorted(set(re.findall(r"L(?:0[1-9]|1[0-7])", name)))
    refs = sorted(set(re.findall(r"(?:REF-\d{3}|MSTY-\d{2}|MLOGO-\d{2})", name, re.IGNORECASE)))
    return {
        "style_ids": [s.upper() for s in styles],
        "logo_ids": [l.upper() for l in logos],
        "ref_ids": [r.upper() for r in refs],
    }


def build_asset_registry(root: Path | None = None, write_outputs: bool = True) -> dict[str, Any]:
    r = repo_root(root)
    records = []
    idx = 0
    for p in sorted(r.rglob("*")):
        if not p.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        rel = p.relative_to(r).as_posix()
        if rel in SELF_GENERATED:
            continue
        idx += 1
        cat, usage, rights = classify_asset(rel)
        links = extract_linked_ids(rel)
        records.append({
            "asset_id": f"AST-{idx:04d}",
            "path": rel,
            "name": p.name,
            "extension": p.suffix.lower() or "(none)",
            "size_bytes": p.stat().st_size,
            "sha256": sha256_file(p),
            "category": cat,
            "usage_type": usage,
            "rights_status": rights,
            "style_ids": links["style_ids"],
            "logo_ids": links["logo_ids"],
            "ref_ids": links["ref_ids"],
            "verified": True,
        })

    registry = {
        "schema_version": "3.0.0",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_assets": len(records),
        "total_bytes": sum(x["size_bytes"] for x in records),
        "excluded_self_generated": sorted(SELF_GENERATED),
        "assets": records,
    }

    if write_outputs:
        reg_dir = r / "09_ASSET_AND_RIGHTS_REGISTRY"
        reg_dir.mkdir(parents=True, exist_ok=True)
        json_path = reg_dir / "ASSET_REGISTRY.json"
        csv_path = reg_dir / "ASSET_REGISTRY.csv"
        db_path = reg_dir / "ASSET_REGISTRY.sqlite"

        json_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

        with csv_path.open("w", encoding="utf-8", newline="") as f:
            cols = [
                "asset_id", "path", "name", "extension", "size_bytes", "sha256",
                "category", "usage_type", "rights_status", "style_ids", "logo_ids", "ref_ids", "verified",
            ]
            writer = csv.DictWriter(f, fieldnames=cols)
            writer.writeheader()
            for rec in records:
                row = dict(rec)
                row["style_ids"] = ";".join(rec["style_ids"])
                row["logo_ids"] = ";".join(rec["logo_ids"])
                row["ref_ids"] = ";".join(rec["ref_ids"])
                writer.writerow(row)

        if db_path.exists():
            db_path.unlink()
        conn = sqlite3.connect(str(db_path))
        try:
            conn.execute("""
                CREATE TABLE assets (
                    asset_id TEXT PRIMARY KEY,
                    path TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    extension TEXT,
                    size_bytes INTEGER NOT NULL,
                    sha256 TEXT NOT NULL,
                    category TEXT,
                    usage_type TEXT,
                    rights_status TEXT,
                    style_ids TEXT,
                    logo_ids TEXT,
                    ref_ids TEXT,
                    verified INTEGER
                )
            """)
            conn.execute("CREATE INDEX idx_assets_category ON assets(category)")
            conn.execute("CREATE INDEX idx_assets_sha256 ON assets(sha256)")
            conn.executemany(
                "INSERT INTO assets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                [
                    (
                        rec["asset_id"], rec["path"], rec["name"], rec["extension"],
                        rec["size_bytes"], rec["sha256"], rec["category"], rec["usage_type"],
                        rec["rights_status"], ";".join(rec["style_ids"]), ";".join(rec["logo_ids"]),
                        ";".join(rec["ref_ids"]), 1 if rec["verified"] else 0,
                    )
                    for rec in records
                ],
            )
            conn.commit()
        finally:
            conn.close()

        # Write sidecar checksums for the generated registry artifacts themselves
        sidecar = {
            "ASSET_REGISTRY.json": sha256_file(json_path),
            "ASSET_REGISTRY.csv": sha256_file(csv_path),
            "ASSET_REGISTRY.sqlite": sha256_file(db_path),
        }
        (reg_dir / "ASSET_REGISTRY_CHECKSUMS.json").write_text(
            json.dumps(sidecar, indent=2), encoding="utf-8"
        )

    return registry


def query_assets(keyword: str, category: str | None = None, root: Path | None = None) -> list[dict[str, Any]]:
    r = repo_root(root)
    db_path = r / "09_ASSET_AND_RIGHTS_REGISTRY/ASSET_REGISTRY.sqlite"
    if not db_path.exists():
        build_asset_registry(r, write_outputs=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        sql = "SELECT * FROM assets WHERE (path LIKE ? OR name LIKE ? OR style_ids LIKE ? OR logo_ids LIKE ? OR ref_ids LIKE ?)"
        pat = f"%{keyword}%"
        params: list[Any] = [pat, pat, pat, pat, pat]
        if category:
            sql += " AND category = ?"
            params.append(category)
        sql += " ORDER BY asset_id LIMIT 50"
        return [dict(row) for row in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()
