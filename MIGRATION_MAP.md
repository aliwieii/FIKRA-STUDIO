# MIGRATION MAP — FIKRA STUDIO V1.0 → V2.0 → V3.0

## Non-Destructive Preservation Guarantee
- **0 original V1.0/V2.0 source files deleted.**
- **`main` branch** remains untouched at tag `v2.0.0-baseline` (284 files).
- **Immutable SHA-256 baseline manifests** stored in `archive/baseline_manifests/` for V1.0 Core (271 files), V1.0 Audit (27 files), V2.0 Core (280 files), and V2.0 Pro (284 files).

## Component Migration Table
| Area | V1.0 Baseline | V2.0 State | V3.0 (`development/v3.0`) | Action |
|---|---|---|---|---|
| Agent Entry | `00_START_HERE/README_AR.md` | Added `FIKRA_STUDIO_V2_HUB.html` | Root `AGENTS.md` (SSOT) + `GEMINI.md` + `CLAUDE.md` + `SYSTEM_MANIFEST.json` | **Added (Preserved V2 Hub)** |
| Asset Registry | Static CSV | 282/284 CSV (missing self) | `ASSET_REGISTRY.{json,csv,sqlite}` + `KNOWLEDGE_GRAPH.json` | **Upgraded** |
| Visual Styles | 32 styles (`STY-001`..`STY-032`) | 32 styles + gallery | 32 styles preserved intact + Graph & Recommender indexed | **Preserved & Indexed** |
| Logo Animations | 17 animations (`L01`..`L17`) | 17 animations (broken local gallery links) | 17 animations preserved + fixed broken doc/gallery links | **Fixed & Indexed** |
| Remotion Engine | Basic template | Empty `SCENES=[]`, truncated Arabic captions, synthetic audio bars | Populated `SCENES`, zero-drop rolling Arabic pagination + scene offset sync, real audio envelope support, `validate-timeline.mjs` | **Refactored & Fixed** |
| HyperFrames Engine | Absent | Added without tests | Preserved + automated schema & RTL validation tests | **Validated** |
| Media QA Script | Basic `analyze.py` | Basic `ffprobe` + SRT regex | Integrated `fikra_v3.media_intelligence` (`volumedetect`, `silencedetect`, RMS envelope) + `arabic_qa` | **Upgraded** |
| QA & Testing | V1 `TEST_RESULTS.md` | Stale V1 copy + flawed `V2_FORENSIC_QA_REPORT.md` | Live `tests/` suite + `.github/workflows/ci.yml` + fresh `TEST_STRATEGY.md`, `TEST_RESULTS.md`, `REGRESSION_REPORT.md` | **Replaced Stale Reports** |
