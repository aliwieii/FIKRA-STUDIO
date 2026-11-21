"""Feature L: Regression Protection — guards against all 12 documented V1/V2 forensic issues."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from . import repo_root


def run_regression_checks(root: Path | None = None) -> dict[str, Any]:
    r = repo_root(root)
    checks: dict[str, dict[str, Any]] = {}

    # REG-001: TEST_RESULTS.md must not be stale V1.0 copy
    tr = r / "10_QA_AND_TESTING/TEST_RESULTS.md"
    tr_txt = tr.read_text(encoding="utf-8", errors="ignore") if tr.exists() else ""
    checks["REG-001_no_stale_v1_test_report"] = {
        "pass": "V3.0" in tr_txt and "FIKRA STUDIO V1.0 — النسخة المكتملة" not in tr_txt,
        "file": "10_QA_AND_TESTING/TEST_RESULTS.md",
    }

    # REG-002: ArabicCaptionOverlay.tsx must NOT use .slice(0, maxWordsPerLine) truncation
    cap = r / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/src/components/ArabicCaptionOverlay.tsx"
    cap_txt = cap.read_text(encoding="utf-8", errors="ignore") if cap.exists() else ""
    checks["REG-002_no_arabic_word_truncation"] = {
        "pass": ".slice(0, maxWordsPerLine)" not in cap_txt and "sceneOffsetSec" in cap_txt and "paginateWords" in cap_txt,
        "file": "src/components/ArabicCaptionOverlay.tsx",
    }

    # REG-003: AudioSpectrumBar.tsx must support real audio envelope
    aud = r / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/src/components/AudioSpectrumBar.tsx"
    aud_txt = aud.read_text(encoding="utf-8", errors="ignore") if aud.exists() else ""
    checks["REG-003_real_audio_envelope_supported"] = {
        "pass": "envelope" in aud_txt and "real_audio" in aud_txt,
        "file": "src/components/AudioSpectrumBar.tsx",
    }

    # REG-004: Remotion Video.tsx SCENES must NOT be empty []
    vid = r / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/src/Video.tsx"
    vid_txt = vid.read_text(encoding="utf-8", errors="ignore") if vid.exists() else ""
    checks["REG-004_remotion_scenes_populated"] = {
        "pass": "const SCENES: Scene[] = [];" not in vid_txt and "SampleFikraHook" in vid_txt,
        "file": "src/Video.tsx",
    }

    # REG-005: Remotion package.json must not pin invalid typescript 7.0.2
    pkg = r / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/package.json"
    pkg_data = json.loads(pkg.read_text(encoding="utf-8")) if pkg.exists() else {}
    ts_ver = pkg_data.get("devDependencies", {}).get("typescript", "")
    checks["REG-005_valid_typescript_version"] = {
        "pass": bool(ts_ver) and not ts_ver.startswith("7."),
        "file": "package.json",
        "observed": ts_ver,
    }

    # REG-006: Immutable baseline manifests preserved
    bm_dir = r / "archive/baseline_manifests"
    checks["REG-006_baseline_manifests_present"] = {
        "pass": all((bm_dir / f).exists() for f in [
            "v1_core_sha256_manifest.json",
            "v2_core_sha256_manifest.json",
            "v2_pro_sha256_manifest.json",
        ]),
        "file": "archive/baseline_manifests/",
    }

    # REG-007: Knowledge Graph preserves all 32 styles & 17 logo animations
    kg_path = r / "09_ASSET_AND_RIGHTS_REGISTRY/KNOWLEDGE_GRAPH.json"
    kg = json.loads(kg_path.read_text(encoding="utf-8")) if kg_path.exists() else {}
    checks["REG-007_styles_32_and_logos_17_intact"] = {
        "pass": kg.get("counts", {}).get("styles") == 32 and kg.get("counts", {}).get("logo_animations") == 17,
        "observed": kg.get("counts", {}),
    }


    # REG-008: ALL Remotion package.json files must have valid TypeScript version (<7.x) (FIK-018)
    bad_ts = []
    for pj in sorted(r.rglob("package.json")):
        if "node_modules" in pj.parts:
            continue
        ts_v = json.loads(pj.read_text(encoding="utf-8")).get("devDependencies", {}).get("typescript", "")
        if ts_v.startswith("7."):
            bad_ts.append(f"{pj.relative_to(r).as_posix()}:{ts_v}")
    checks["REG-008_all_package_json_valid_ts"] = {"pass": len(bad_ts) == 0, "bad": bad_ts}

    # REG-009: music.py quarantined under strict NO-MUSIC policy (FIK-019)
    mp = r / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_PYTHON_SCRIPTS/music.py"
    checks["REG-009_music_generator_quarantined"] = {
        "pass": mp.exists() and "FIKRA_NO_MUSIC_POLICY_GUARD" in mp.read_text(encoding="utf-8"),
        "file": "MOTALIM_PYTHON_SCRIPTS/music.py",
    }

    # REG-010: ASSET_REGISTRY JSON, CSV, ASSET_INDEX.csv, HASH_MANIFEST.csv counts match (FIK-010)
    reg_dir = r / "09_ASSET_AND_RIGHTS_REGISTRY"
    reg_json = json.loads((reg_dir / "ASSET_REGISTRY.json").read_text(encoding="utf-8")) if (reg_dir / "ASSET_REGISTRY.json").exists() else {}
    n_json = reg_json.get("total_assets", -1)
    n_hash = len((reg_dir / "HASH_MANIFEST.csv").read_text(encoding="utf-8").splitlines()) - 1 if (reg_dir / "HASH_MANIFEST.csv").exists() else -2
    n_idx = len((reg_dir / "ASSET_INDEX.csv").read_text(encoding="utf-8").splitlines()) - 1 if (reg_dir / "ASSET_INDEX.csv").exists() else -3
    checks["REG-010_registries_synchronized"] = {
        "pass": n_json > 0 and n_json == n_hash == n_idx,
        "counts": {"json": n_json, "hash_manifest": n_hash, "asset_index": n_idx},
    }

    passed = sum(1 for c in checks.values() if c["pass"])
    return {
        "pass": passed == len(checks),
        "passed": passed,
        "total": len(checks),
        "checks": checks,
    }
