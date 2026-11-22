# FIKRA STUDIO V3.2.0 Changelog

## [3.2.0] — 2026-11-22 (Branch: `feature/v3.2-visual-intelligence`)
### Added
- **Visual Intelligence Engine (`fikra_v3/visual_intelligence.py`):**
  - Honest 5-level `VISUAL_REVIEW_STATUS` taxonomy (`ORIGINAL_WATCHED`, `EXTRACTED_FRAME`, `CARD_TEXT_ONLY`, `AI_CONCEPT_PREVIEW`, `UNVERIFIED`) + `verify_reference_access()`.
  - Real FFmpeg multi-timestamp **Contact Sheet generator** (`extract_contact_sheet()`) stamping Reference ID, filename, timecode, frame number, and review status onto PNG grids.
  - 7-Dimension Structured Visual Analysis template (`create_visual_analysis_template()`) and localized Post-Production Video Review Diff (`build_video_review_report()`).
- **6-Criteria Weighted Style Comparison Engine (`compare_styles()` in `fikra_v3/style_recommender.py`):**
  - Idea Fit (25%), Visual Fit (25%), Narrative Fit (15%), Tool Feasibility (15%), Consistency (10%), Reference Verification (10%) with confidence cap on unverified `CATALOG_ONLY` styles, plus pros, cons, best pick, and alternative.
- **Tool-Adapted Production Prompt Compiler & 15-Point QA Gate (`compile_v32_production_prompt()`, `score_prompt_quality()`, `get_adaptive_interview_question()`):**
  - Supports 6 target production tools, executable motion/camera specs, `REQUIRED INPUT ASSETS`, `REFERENCE USAGE INSTRUCTIONS`, and `Negative Prompt` while preserving **strict NO-MUSIC across all modes** per owner directive.
- **New CLI Commands:** `contact-sheet` and `compare-styles`.
- **Comprehensive V3.2 Test Suite (`tests/test_v32_visual_intelligence.py`):** Covers all 8 mandatory tests (`Test A`–`Test H`).
