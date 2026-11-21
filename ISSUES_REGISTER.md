# FORENSIC ISSUES REGISTER — FIKRA STUDIO V2.0 → V3.0

Every issue below was discovered by direct file inspection and automated verification of the untouched V1.0 (271 files) and V2.0 (284 files) archives.

---

### ISS-001 — V1.0 and V2.0 QA Test Reports Are Byte-for-Byte Identical
- **Severity:** `CRITICAL`
- **File Path:** `10_QA_AND_TESTING/TEST_RESULTS.md`, `TEST_PLAN.md`, `QA_SYSTEM.md`, `KNOWN_LIMITATIONS.md`
- **Evidence:** SHA-256 comparison between `V1.0_CORE_SYSTEM_AND_CODE` and `V2.0_PRO_8SKILLS_CORE` returned `identical_to_V1=True` for all 4 files; `TEST_RESULTS.md` header still reads `FIKRA STUDIO V1.0`.
- **Root Cause:** V2.0 added `V2_FORENSIC_QA_REPORT.md` without updating the canonical test plan/results files.
- **Impact:** Agents reading `TEST_RESULTS.md` receive stale V1.0 metrics instead of actual V2.0/V3.0 test evidence.
- **Proposed Fix:** Replace with freshly executed V3.0 `TEST_STRATEGY.md`, `TEST_RESULTS.md`, and `REGRESSION_REPORT.md` generated from live automated test runs.
- **Reproduction Test:** Compare SHA-256 of V1 `TEST_RESULTS.md` vs V2 `TEST_RESULTS.md`.
- **Verification Test:** `tests/test_regression.py::TestRegressionGuard::test_v3_test_reports_not_stale_v1`

---

### ISS-002 — Silent Word Deletion & Scene-Offset Desync in `ArabicCaptionOverlay.tsx`
- **Severity:** `CRITICAL`
- **File Path:** `08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/src/components/ArabicCaptionOverlay.tsx` (lines 20, 60)
- **Evidence:** Line 60 executes `activeLine.words.slice(0, maxWordsPerLine).map(...)` (default `maxWordsPerLine = 6`), silently discarding word #7 onward on long Arabic lines. Additionally, `useCurrentFrame()` inside `<Sequence from={...}>` is local (starts at 0), yet line 20 compares `toSec(frame)` directly to global `TIMING.lines` timestamps without adding `sceneOffsetSec`.
- **Root Cause:** Hard array slice used instead of rolling time-synced pagination, and local sequence frame confused with global timeline time.
- **Impact:** Long Arabic captions lose words on screen; captions after Scene 0 display wrong timestamps.
- **Proposed Fix:** Implement rolling word pagination (`paginateWords()`) so 100% of words render across time-synced chunks with zero deletion, and add `sceneOffsetSec` prop (`globalSec = sceneOffsetSec + toSec(frame)`).
- **Reproduction Test:** Pass a 12-word Arabic line to V2 `ArabicCaptionOverlay` logic → only 6 words appear.
- **Verification Test:** `tests/test_arabic_qa.py` + `tests/test_regression.py::test_no_arabic_caption_word_truncation` + Node `validate-timeline.mjs`.

---

### ISS-003 — Synthetic Sine-Wave Audio Visualizer Masquerading as Audio Spectrum
- **Severity:** `HIGH`
- **File Path:** `08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/src/components/AudioSpectrumBar.tsx` (lines 29–33)
- **Evidence:** Computes `wave = 0.35 + 0.35 * Math.sin(t * 5.2 + phase) + 0.2 * Math.cos(t * 8.7 - phase * 1.3)` with zero audio input.
- **Root Cause:** No real `ffmpeg` / `ffprobe` audio envelope extractor was wired into the component.
- **Impact:** Violates FIKRA technical honesty rules ("لا تستخدم بيانات اصطناعية باعتبارها قياسات صوت حقيقية").
- **Proposed Fix:** Upgrade `AudioSpectrumBar.tsx` to accept real pre-computed `envelope: number[]` extracted by `fikra_v3.media_intelligence` (`ffmpeg` RMS frames) and explicitly label `mode="real_audio"` vs `mode="preview_only"` when no audio file is attached.
- **Reproduction Test:** Inspect `AudioSpectrumBar.tsx` for audio data props → none exist.
- **Verification Test:** `tests/test_media_intelligence.py` + `tests/test_regression.py::test_audio_spectrum_supports_real_envelope`.

---

### ISS-004 — Empty Remotion `SCENES` Registry & Stub `words.json`
- **Severity:** `HIGH`
- **File Path:** `08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/src/Video.tsx` (line 13) & `src/data/words.json`
- **Evidence:** `const SCENES: Scene[] = [];` leaves `SampleFikraHook.tsx` and `FikraChannelOutro.tsx` unregistered; `words.json` is a 114-byte stub.
- **Root Cause:** V2.0 created scene components without registering them in `Video.tsx` or providing a valid sample timeline.
- **Impact:** Running Remotion renders an empty black placeholder screen.
- **Proposed Fix:** Register `SampleFikraHook` and `FikraChannelOutro` in `Video.tsx` via a typed `SCENES` registry with transitions (`SceneTransition.tsx`), populate `src/data/words.json` with a real 12-word Arabic timeline, and add `scripts/validate-timeline.mjs`.
- **Reproduction Test:** Parse `Video.tsx` → `SCENES = []`.
- **Verification Test:** `tests/test_regression.py::test_remotion_scene_registry_non_empty` + `node scripts/validate-timeline.mjs`.

---

### ISS-005 — 28 Broken Local Links Despite V2 QA Claiming `0 Broken Links`
- **Severity:** `HIGH`
- **File Path:** `04_LOGO_ANIMATION_LIBRARY/ANIMATION_SPECS/00_LOGO_ANIMATION_SKILL_REFERENCE.md`, `04_LOGO_ANIMATION_LIBRARY/LOGO_REFERENCES/motalim_17_logo_gallery.html`, `10_QA_AND_TESTING/V2_FORENSIC_QA_REPORT.md`
- **Evidence:** Automated scan detected 5 broken `references/*.md` links in `00_LOGO_ANIMATION_SKILL_REFERENCE.md`, 21 missing `videos/L*.mp4` links in `motalim_17_logo_gallery.html`, and 2 unresolved JS template paths in `motalim_26_styles_gallery.html`. Also `V2_FORENSIC_QA_REPORT.md` reports `280` files while `V2.0_PRO_8SKILLS_CORE` contains `284` files.
- **Root Cause:** V2 QA checked only a narrow subset of HTML hrefs and ignored Markdown relative links and missing media targets.
- **Impact:** Agents and users encounter dead links and inflated `100.0/100` QA confidence.
- **Proposed Fix:** Fix Markdown relative links in `00_LOGO_ANIMATION_SKILL_REFERENCE.md`, annotate external-archive video references in `motalim_17_logo_gallery.html` cleanly without dead local `src=` attributes, and run `fikra_v3.integrity_validator` across 100% of `.md` and `.html` files.
- **Reproduction Test:** Run link scanner on untouched V2.0 baseline → 28 broken links.
- **Verification Test:** `tests/test_integrity.py::test_zero_broken_internal_links`.

---

### ISS-006 — Incomplete Asset Registry Coverage (282/284) & Missing Knowledge Graph
- **Severity:** `HIGH`
- **File Path:** `09_ASSET_AND_RIGHTS_REGISTRY/ASSET_INDEX.csv`, `HASH_MANIFEST.csv`
- **Evidence:** `HASH_MANIFEST.csv` lists 282 of 284 files (omitting itself and `ASSET_INDEX.csv`), and no machine-queryable JSON/SQLite registry or cross-entity Knowledge Graph exists linking Style IDs (`STY-001`..`STY-032`) to Prompts, Reference Videos, and Engines.
- **Root Cause:** Static CSV generator skipped registry files and had no relational/graph schema.
- **Impact:** Agents cannot traverse `Style → Prompt → Reference Videos → Engine` in one deterministic lookup.
- **Proposed Fix:** Build `fikra_v3.asset_intelligence` + `fikra_v3.knowledge_graph` generating `ASSET_REGISTRY.json`, `ASSET_REGISTRY.csv`, `ASSET_REGISTRY.sqlite`, and `KNOWLEDGE_GRAPH.json` with 100% repo file coverage (excluding only self-referential registry digests recorded in a separate checksum sidecar).
- **Reproduction Test:** Compare `len(all_files)` vs `len(HASH_MANIFEST.csv)` in V2.0 → 284 vs 282.
- **Verification Test:** `tests/test_asset_and_graph.py`.

---

### ISS-007 — Missing Root Agent-First Entry Points & Rule Duplication
- **Severity:** `HIGH`
- **File Path:** Repository root (missing `README.md`, `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `SYSTEM_MANIFEST.json`, `PROJECT_MAP.md`, `ARCHITECTURE.md`)
- **Evidence:** Root contains only numbered folders `00_START_HERE/`..`99_SOURCE_ORIGINALS/`; instructions are repeated across `00_START_HERE/README_AR.md`, `PROJECT_BOOTSTRAP_PROMPT_AR.md`, `01_SYSTEM_CORE/`, and `02_WORKFLOWS/`.
- **Root Cause:** V1/V2 were structured as Google Drive ZIP archives rather than an Agent-First GitHub repository.
- **Impact:** Any new AI agent must scan dozens of files before knowing the rules, modes, or CLI entrypoints.
- **Proposed Fix:** Establish `AGENTS.md` as the single source of truth, thin platform routers (`GEMINI.md`, `CLAUDE.md`), `SYSTEM_MANIFEST.json`, `README.md`, and `fikra_v3.context_loader`.
- **Reproduction Test:** Check root directory of V2.0 baseline → 0 root `.md`/`.json` entrypoints.
- **Verification Test:** `tests/test_integrity.py::test_agent_first_entrypoints_exist`.

---

### ISS-008 — Unverified/Invalid Dependency Versions in Remotion `package.json`
- **Severity:** `MEDIUM`
- **File Path:** `08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/package.json`
- **Evidence:** Declares `"typescript": "7.0.2"` and `"@remotion/cli": "4.0.533"` without a lockfile or verified install.
- **Root Cause:** Unchecked manual version bump.
- **Impact:** `npm install` will fail in standard Node/npm environments when resolving non-existent `typescript@7.0.2`.
- **Proposed Fix:** Pin realistic stable semver ranges (`typescript: ^5.7.2`, `remotion: ^4.0.0`, `react: ^19.0.0`) and add `validate-timeline` npm script.
- **Reproduction Test:** Inspect `package.json` `devDependencies.typescript` → `"7.0.2"`.
- **Verification Test:** `tests/test_regression.py::test_remotion_package_json_valid_versions`.

---

### ISS-009 — Limited Media QA Script (No Real Audio Loudness/Silence/Arabic QA)
- **Severity:** `MEDIUM`
- **File Path:** `08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_PYTHON_SCRIPTS/fikra_media_qa_pipeline.py`
- **Evidence:** Only checks container resolution/codec via `ffprobe` and basic SRT timestamp regex; does not run `ffmpeg volumedetect`, `silencedetect`, or Arabic RTL/truncation QA.
- **Root Cause:** Minimal V2.0 prototype script.
- **Impact:** Silent audio, clipping, or broken Arabic captions pass QA undetected.
- **Proposed Fix:** Upgrade `fikra_media_qa_pipeline.py` to call `fikra_v3.media_intelligence` and `fikra_v3.arabic_qa` for real audio loudness, silence intervals, RMS envelope extraction, and Arabic caption validation.
- **Reproduction Test:** Run V2 script on a muted video with truncated Arabic SRT → passes with no audio/Arabic warning.
- **Verification Test:** `tests/test_media_intelligence.py` using real FFmpeg-generated WAV/MP4 fixtures.

---

### ISS-010 — HyperFrames Template Lacks Schema & Determinism Validation
- **Severity:** `MEDIUM`
- **File Path:** `08_PROJECT_ASSETS/CODE_AND_SCRIPTS/HYPERFRAMES_HTML_VIDEO_TEMPLATE/`
- **Evidence:** `variables.json` has no automated schema check, and `index.html` lacks an automated test confirming `seekToFrame` and Arabic RTL attributes.
- **Root Cause:** Added in V2.0 without an accompanying test harness.
- **Impact:** Malformed `variables.json` or missing `dir="rtl"` breaks deterministic renders silently.
- **Proposed Fix:** Add `validate_hyperframes()` check inside `fikra_v3` and unit tests covering `variables.json` schema and `index.html` RTL + `seekToFrame` presence.
- **Reproduction Test:** Check `tests/` in V2.0 → directory does not exist.
- **Verification Test:** `tests/test_engines.py::test_hyperframes_template_valid`.

---

### ISS-011 — Missing `.gitignore`, Automated Test Suite, and CI Pipeline
- **Severity:** `MEDIUM`
- **File Path:** Repository root (`.gitignore`, `tests/`, `.github/workflows/ci.yml`, `SECURITY.md`)
- **Evidence:** No automated test runner or GitHub Actions CI existed in V2.0; no `.gitignore` prevented `__pycache__` or massive `.mp4` commits.
- **Root Cause:** V2.0 was distributed as a ZIP archive without GitHub CI/CD governance.
- **Impact:** Regressions go undetected between edits.
- **Proposed Fix:** Add `.gitignore`, `SECURITY.md`, comprehensive `tests/` suite, and `.github/workflows/ci.yml` (secret-safe).
- **Reproduction Test:** Inspect V2.0 root → missing `.gitignore` and `.github/`.
- **Verification Test:** `tests/test_integrity.py` + `python3 -m unittest discover -s tests -v`.

---

### ISS-012 — No Immutable V1/V2 Baseline Freeze Manifests or Migration Map
- **Severity:** `LOW`
- **File Path:** `archive/baseline_manifests/`, `MIGRATION_MAP.md`
- **Evidence:** No machine-verifiable record existed comparing all V1.0 (271) and V2.0 (284) file SHA-256 hashes inside the repo.
- **Root Cause:** Version transitions were summarized in prose only.
- **Impact:** Difficult to prove non-destructive preservation of historical assets.
- **Proposed Fix:** Store immutable JSON SHA-256 manifests for V1.0 and V2.0 under `archive/baseline_manifests/` and document every transition in `MIGRATION_MAP.md`.
- **Reproduction Test:** Check `archive/` in V2.0 → absent.
- **Verification Test:** `tests/test_integrity.py::test_baseline_manifests_intact`.
