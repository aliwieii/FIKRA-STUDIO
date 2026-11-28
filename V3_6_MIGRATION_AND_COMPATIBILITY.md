# FIKRA STUDIO V3.6 — Migration & Compatibility Guide

- **Backward Compatibility with V3.5.0:** 100% preserved.
  - All 9 modes (`MODES`), 32 visual styles (`STY-001`..`STY-032`), 17 logo animations (`L01`..`L17`), and 52 reference videos remain intact.
  - `quickstart_blueprint(topic, mode, duration_sec)` still defaults to `"9:16"` when `aspect_ratio` is omitted, while newly supporting `aspect_ratio="16:9"` and `"1:1"`.
  - `readiness_scorer.py` (`PROMPT_READY` → `RENDER_TESTED`) is unchanged; `quality_scorer.py` operates as an independent evidence-based quality gate.
- **New V3.6 CLI Commands:**
  - `python3 -m fikra_v3 quality-audit --video <path.mp4> --aspect 9:16 --sheet <sheet.png>`
  - `python3 -m fikra_v3 quickstart --topic "..." --aspect 16:9`
