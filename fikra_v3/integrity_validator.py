"""Feature N: Automatic Integrity Validator — links, hashes, schemas, entrypoints, secrets."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from . import repo_root
from .asset_intelligence import EXCLUDE_DIRS, sha256_file

REQUIRED_ENTRYPOINTS = [
    "README.md",
    "AGENTS.md",
    "GEMINI.md",
    "CLAUDE.md",
    "AGENT_ONBOARDING_GUIDE.md",
    "ARCHITECTURE.md",
    "V3_ARCHITECTURE.md",
    "PROJECT_MAP.md",
    "SYSTEM_MANIFEST.json",
    "V3_DEVELOPMENT_PLAN.md",
    "SKILLS_AUDIT.md",
    "ISSUES_REGISTER.md",
    "MIGRATION_MAP.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
]

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"sk-[A-Za-z0-9]{32,}"),
    re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]

MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']""")


def check_links(root: Path) -> list[dict[str, str]]:
    broken = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in {".md", ".html"}:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        links = MD_LINK_RE.findall(text) if p.suffix.lower() == ".md" else HTML_LINK_RE.findall(text)
        for lk in links:
            clean = lk.split("#")[0].split("?")[0].strip()
            if not clean or clean.startswith(("http://", "https://", "mailto:", "data:", "javascript:", "#", "${")):
                continue
            if "${" in clean:
                continue
            target = (p.parent / clean).resolve()
            try:
                target.relative_to(root.resolve())
                if not target.exists():
                    broken.append({"source": p.relative_to(root).as_posix(), "target": lk})
            except ValueError:
                broken.append({"source": p.relative_to(root).as_posix(), "target": f"OUTSIDE_ROOT:{lk}"})
    return broken


def check_json_files(root: Path) -> list[dict[str, str]]:
    errors = []
    for p in sorted(root.rglob("*.json")):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append({"file": p.relative_to(root).as_posix(), "error": str(exc)})
    return errors


def check_secrets(root: Path) -> list[dict[str, str]]:
    hits = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in {".md", ".py", ".ts", ".tsx", ".js", ".mjs", ".json", ".yml", ".yaml", ".html", ".csv"}:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                hits.append({"file": p.relative_to(root).as_posix(), "pattern": pat.pattern})
    return hits


def check_registry_hashes(root: Path) -> dict[str, Any]:
    reg_path = root / "09_ASSET_AND_RIGHTS_REGISTRY/ASSET_REGISTRY.json"
    if not reg_path.exists():
        return {"pass": False, "error": "ASSET_REGISTRY.json missing"}
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    mismatches = []
    missing = []
    for item in reg.get("assets", []):
        fp = root / item["path"]
        if not fp.exists():
            missing.append(item["path"])
        elif sha256_file(fp) != item["sha256"]:
            mismatches.append(item["path"])
    return {
        "pass": len(missing) == 0 and len(mismatches) == 0,
        "checked_assets": len(reg.get("assets", [])),
        "missing": missing,
        "hash_mismatches": mismatches,
    }


def run_integrity_audit(root: Path | None = None) -> dict[str, Any]:
    r = repo_root(root)
    missing_entry = [f for f in REQUIRED_ENTRYPOINTS if not (r / f).exists()]
    broken_links = check_links(r)
    json_errors = check_json_files(r)
    secrets = check_secrets(r)
    hashes = check_registry_hashes(r)
    overall = (
        len(missing_entry) == 0
        and len(broken_links) == 0
        and len(json_errors) == 0
        and len(secrets) == 0
        and hashes.get("pass", False)
    )
    return {
        "pass": overall,
        "missing_entrypoints": missing_entry,
        "broken_links_count": len(broken_links),
        "broken_links": broken_links[:25],
        "json_errors": json_errors,
        "secret_hits": secrets,
        "registry_hash_check": hashes,
    }
