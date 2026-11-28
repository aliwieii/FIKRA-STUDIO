# TEST STRATEGY — FIKRA STUDIO V3.0

## Verification Philosophy
- Every `PASS` requires **executable command evidence** — theoretical reviews never count as test passes.
- Blocked tests (e.g. `npm install` / full Remotion Chromium video render in an offline sandbox) are explicitly labeled **`BLOCKED`** with exact root cause and reproduction steps.

## Test Layers
1. **Unit & Contract Tests (`tests/test_context_and_modes.py`, `test_state_approvals_prompt.py`):**
   - Mode routing & strict Universal vs FIKRA Channel isolation.
   - SHA-256 Approval Protection (blocks silent overwrite; permits audited explicit override).
   - Evidence-gated Readiness Scorer (`PROMPT_READY` → `RENDER_TESTED`).
   - 4-persona Multi-Agent Review & Project Bootstrap scaffolding.
2. **Asset & Knowledge Graph Tests (`tests/test_asset_and_graph.py`):**
   - 100% file SHA-256 coverage in `ASSET_REGISTRY.{{json,csv,sqlite}}`.
   - Knowledge Graph exact counts (32 styles, 17 logo animations, 52 reference cards).
   - End-to-end Style lookup (`STY-001` → spec + prompt + refs + engine) & Style Recommender.
3. **Arabic Technical QA Tests (`tests/test_arabic_qa.py`):**
   - Zero-drop rolling pagination on 13-word Arabic sentence.
   - Isolated-form & letter-splitting detection, diacritics preservation, mixed Arabic-English BiDi check, SRT timestamp & CPS validation.
4. **Real FFmpeg Media Intelligence Tests (`tests/test_media_intelligence.py`):**
   - Generates a real 2-second 1080×1920 H.264/AAC MP4 with tone + silence gap via `ffmpeg`, executes `analyze_audio_real()` and `fikra_media_qa_pipeline.py`, and verifies real dB, silence detection, and per-frame RMS envelope extraction.
5. **Engine, Integrity & Regression Tests (`tests/test_engines_and_regression.py`):**
   - Executes Node.js `validate-timeline.mjs`.
   - Validates HyperFrames `variables.json` schema and `index.html` RTL/`seekToFrame`.
   - Runs `integrity_validator` (0 broken links, 0 JSON errors, 0 leaked secrets, 100% hash match) and `regression_guard` (all 7 automated regression invariants).

## V3.6 Quality Evolution Additions
- Evidence-based quality scoring (`quality_scorer.py`), Visual Quality Engine (`visual_quality.py`), EBU R128 audio mastering (`analyze_audio_mastering`), render-level Arabic caption PNG fixtures, and Scene Schema validation (`tests/test_v36_quality_evolution.py`).
