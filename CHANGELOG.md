# Changelog — FIKRA STUDIO

All notable changes to this project are documented here.

## [3.3.0] — 2026-11-22 (Merged to `main`, Release `v3.3.0`)
### Added & Improved
- **32-Style Arabic UX Catalog (`03_STYLE_LIBRARY/STYLE_UX_CATALOG_V33.json`):** Plain-Arabic creative names, multi-category tags, and honest `STY-014` Fake 3D labeling.
- **External Open-License Visual Gallery (`03_STYLE_LIBRARY/STYLE_EXTERNAL_GALLERY.json` & `FIKRA_STYLE_GALLERY_V33.html`):** Verified external Wikimedia Commons image links with zero heavy binary bloat in Git.
- **Creative Experience Engine (`fikra_v3/creative_experience.py`):** 12-section `build_style_bible()`, `recommend_styles_v33()`, strict `assert_no_music_leak()` across all 9 modes, and `compile_v33_production_prompt()`.
- **Zero-Dependency CI Contact Sheet Fallback:** `extract_contact_sheet()` falls back cleanly to native FFmpeg `tile` when `Pillow` is absent (50/50 tests green on GitHub Actions `ubuntu-latest`).
- **Full V3.3 Documentation Sync:** Unified `GEMINI.md`, `CLAUDE.md`, `PROJECT_MAP.md`, `ARCHITECTURE.md`, `V3_ARCHITECTURE.md`, `AGENT_ONBOARDING_GUIDE.md`, `CHANGELOG.md`, and `fikra_v3/__init__.py` to V3.3.

## [3.2.0] — 2026-11-22
### Added
- **Visual Intelligence Layer (`fikra_v3/visual_intelligence.py`):** 5-level `VISUAL_REVIEW_STATUS`, truthful reference access verification, real FFmpeg contact sheet extraction, 7-dimension analysis card, 6-criteria weighted style comparison, 15-point prompt QA scorer, and adaptive interview questions (`tests/test_v32_visual_intelligence.py`).

## [3.1.1] — 2026-11-21
### Fixed
- Resolved `FIK-004`..`FIK-019` production-readiness issues: locked decision overwrite guard, strict state machine transitions, FFmpeg `blackdetect` + SHA-256 bound readiness QA, logo regex & registry sync, `music.py` quarantine guard, and Remotion TypeScript `^5.7.2` alignment.

## [3.1.0] — 2026-11-21 (Branch: `development/v3.0` / `main`)
### Added
- **Interactive One-Question-at-a-Time Interview & Visual Hook Narrative Arc** (`Problem -> Escalation -> Resolution`) in `ACTIVATION_PROMPT.md` and `fikra_v3/prompt_compiler.py`.
- **Mandatory Stage Closure Footer** (`format_stage_footer()`) in `fikra_v3/project_state.py` enforcing explicit user approval after every stage.
- **Real FFmpeg Black-Frame QC (`detect_black_frames()`)** in `fikra_v3/media_intelligence.py` catching unintended black frames/flashes programmatically.
- **Focused Publishing Pack Generator (`generate_publishing_pack()`)** enforcing 5–8 hashtags, cover text, short Arabic description, and comment hook.
- **Strict NO-MUSIC Default & 2D/Motion Non-Photorealistic Human Identity Guardrail** across all prompts and workflows.
- **New Automated Test Suite (`tests/test_v31_upgrades.py`)** verifying all V3.1.0 features including live FFmpeg black-frame detection.

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
