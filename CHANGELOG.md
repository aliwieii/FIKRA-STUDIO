# Changelog — FIKRA STUDIO

All notable changes to this project are documented here.

## [3.0.0-rc.1] — 2026-11-21 (Branch: `development/v3.0`)
### Added
- **Agent-First Entry Layer:** `AGENTS.md` (Single Source of Truth), `GEMINI.md`, `CLAUDE.md`, `README.md`, `AGENT_ONBOARDING_GUIDE.md`, `PROJECT_MAP.md`, `SYSTEM_MANIFEST.json`, `V3_ARCHITECTURE.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `.gitignore`.
- **Executable `fikra_v3` Package (All 15 Features A–O + CLI):** AI Context Loader, Knowledge Graph (`KNOWLEDGE_GRAPH.json`), Asset Intelligence (`ASSET_REGISTRY.{{json,csv,sqlite}}`), Prompt Compiler, Project State Engine, SHA-256 Approval Protection, Style Recommender, real FFmpeg Media Intelligence, Arabic QA Engine, 4-Persona Multi-Agent Review, Evidence-Gated Production Readiness Scorer, Regression Guard, Model Adapter Layer, Automatic Integrity Validator, Project Bootstrap Generator.
- **Immutable Baseline Preservation:** `archive/baseline_manifests/` storing exact SHA-256 manifests for V1.0 (271 files) and V2.0 (284 files) without modifying `main`.
- **Automated Testing & CI:** Comprehensive `tests/` suite (unit, real FFmpeg media, Arabic RTL, Node timeline, integrity, regression) and `.github/workflows/ci.yml`.
- **Remotion Additions:** `SceneTransition.tsx`, `scripts/validate-timeline.mjs`, and populated 13-word Arabic `src/data/words.json`.

### Fixed
- **ISS-001 (CRITICAL):** Replaced stale V1.0-identical `TEST_RESULTS.md` with freshly executed V3.0 test reports.
- **ISS-002 (CRITICAL):** Eliminated silent Arabic word truncation in `ArabicCaptionOverlay.tsx` via rolling `paginateWords()` and fixed scene-offset sync via `sceneOffsetSec`.
- **ISS-003 (HIGH):** Upgraded `AudioSpectrumBar.tsx` to consume real FFmpeg RMS envelopes (`mode="real_audio"`) instead of misrepresenting synthetic sine waves.
- **ISS-004 (HIGH):** Populated Remotion `src/Video.tsx` `SCENES` registry with `SampleFikraHook` and `FikraChannelOutro`.
- **ISS-005 (HIGH):** Repaired all 28 broken local links in `04_LOGO_ANIMATION_LIBRARY/`.
- **ISS-006 (HIGH):** Built unified 100%-coverage `ASSET_REGISTRY.{{json,csv,sqlite}}` + `KNOWLEDGE_GRAPH.json`.
- **ISS-008 (MEDIUM):** Fixed invalid `typescript: 7.0.2` pin in Remotion `package.json` to `^5.7.2`.
- **ISS-009 (MEDIUM):** Upgraded `fikra_media_qa_pipeline.py` with real FFmpeg `volumedetect`, `silencedetect`, RMS envelope, and Arabic SRT QA.

## [2.0.0] — 2026-11-20 (Tag: `v2.0.0-baseline` on `main`)
- Added `FIKRA_STUDIO_V2_HUB.html`, HyperFrames HTML5 starter, Remotion V2 components, and printable Storyboard template.

## [1.0.0] — 2026-11-20
- Initial archive: Central Mode Router, 32 visual styles, 17 logo animations, 52 reference videos, and `fikra-studio` skill.
