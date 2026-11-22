# ARCHITECTURE — FIKRA STUDIO V3.3 (Agent-First Universal Creative Production System)

## 1. Architectural Principles
1. **Single Source of Truth:** `AGENTS.md` + `SYSTEM_MANIFEST.json` govern all agents; `GEMINI.md` and `CLAUDE.md` are thin pointers.
2. **Non-Destructive Layering:** All V1.0/V2.0 libraries (`01_SYSTEM_CORE/`..`99_SOURCE_ORIGINALS/`) remain intact; V3.0 adds an executable intelligence layer (`fikra_v3/`), unified registries (`09_ASSET_AND_RIGHTS_REGISTRY/`), engine fixes (`08_PROJECT_ASSETS/`), and automated QA (`tests/`, `.github/`).
3. **Zero Unverified Claims:** Strict 5-tier readiness state machine (`PROMPT_READY` → `SPEC_READY` → `CODE_READY` → `BUILD_TESTED` → `RENDER_TESTED`), each gated by verifiable artifacts.
4. **Strict Mode Isolation:** 9 operating modes enforced programmatically in `fikra_v3.context_loader` and `fikra_v3.prompt_compiler`.
5. **Arabic-First Engineering:** Native RTL, zero-truncation rolling caption pagination, diacritics preservation, mixed Arabic-English BiDi safety, and real FFmpeg audio measurements.

## 2. Layered System Diagram
```text
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 1: AGENT ENTRY & ADAPTERS                                     │
│  README.md · AGENTS.md (SSOT) · GEMINI.md · CLAUDE.md · MANIFEST     │
│  fikra_v3.model_adapter · fikra_v3.context_loader                    │
├──────────────────────────────────────────────────────────────────────┤
│  LAYER 2: KNOWLEDGE & ASSET INTELLIGENCE                             │
│  ASSET_REGISTRY.{json,csv,sqlite} · KNOWLEDGE_GRAPH.json             │
│  fikra_v3.asset_intelligence · knowledge_graph · style_recommender   │
├──────────────────────────────────────────────────────────────────────┤
│  LAYER 3: STATE, GOVERNANCE & PROMPT COMPILER                        │
│  fikra_v3.project_state · approval_guard (SHA-256) · prompt_compiler │
│  fikra_v3.multi_agent_review · readiness_scorer · project_bootstrap  │
├──────────────────────────────────────────────────────────────────────┤
│  LAYER 4: ARABIC QA, MEDIA INTELLIGENCE & PRODUCTION ENGINES         │
│  fikra_v3.arabic_qa · media_intelligence (FFmpeg/FFprobe)            │
│  Remotion 4 Template (fixed) · HyperFrames HTML Template · Scripts   │
├──────────────────────────────────────────────────────────────────────┤
│  LAYER 5: CONTINUOUS FORENSIC QA & REGRESSION PROTECTION             │
│  fikra_v3.integrity_validator · regression_guard · tests/ · CI       │
│  archive/baseline_manifests/ (Immutable V1.0 & V2.0 SHA-256)         │
└──────────────────────────────────────────────────────────────────────┘
```

## 3. Feature Modules (`fikra_v3/`)
| Code | Feature | Module | Inputs | Outputs |
|---|---|---|---|---|
| A | AI Context Loader | `fikra_v3/context_loader.py` | Mode, query, style ID | Minimal prioritized file list + token estimate |
| B | Knowledge Graph | `fikra_v3/knowledge_graph.py` | Style/Logo/Mode/Ref ID | Linked specs + prompt + refs + engine requirements |
| C | Asset Intelligence | `fikra_v3/asset_intelligence.py` | Repo filesystem | `ASSET_REGISTRY.{json,csv,sqlite}` (SHA-256, rights, usage) |
| D | Prompt Compiler | `fikra_v3/prompt_compiler.py` | `project_state.json` + mode | Mode-isolated, approval-locked Production Prompt |
| E | Project State Engine | `fikra_v3/project_state.py` | Project metadata, stage updates | Versioned `project_state.json` with stage history |
| F | Approval Protection | `fikra_v3/approval_guard.py` | Decision key + payload | SHA-256 lock; blocks silent mutation without explicit override |
| G | Style Recommender | `fikra_v3/style_recommender.py` | Topic, mood, mode, difficulty | Ranked top-N styles from the 32 verified styles |
| H | Media Intelligence | `fikra_v3/media_intelligence.py` | Real audio/video path | Real `ffprobe`/`ffmpeg` duration, LUFS/dB, silence, RMS envelope |
| I | Arabic QA Engine | `fikra_v3/arabic_qa.py` | Arabic text / SRT / words.json | RTL, shaping, zero-drop pagination, BiDi, CPS/WPM report |
| J | Multi-Agent Review | `fikra_v3/multi_agent_review.py` | Project state + script + prompt | 4-persona scorecard (Director, Linguist, Engineer, Compliance) |
| K | Production Readiness Score | `fikra_v3/readiness_scorer.py` | Project state + evidence paths | 0–100 score + strictly gated tier (`PROMPT_READY`..`RENDER_TESTED`) |
| L | Regression Protection | `fikra_v3/regression_guard.py` | Repo root | Pass/fail checks guarding all 12 historical V1/V2 defects |
| M | Model Adapter Layer | `fikra_v3/model_adapter.py` | Target (`gemini`/`claude`/`chatgpt`) | Platform-tailored compact context payload from `AGENTS.md` |
| N | Automatic Integrity Validator | `fikra_v3/integrity_validator.py` | Repo root | Hash check, zero broken links, JSON/CSV schema, secret scan |
| O | Project Bootstrap Generator | `fikra_v3/project_bootstrap.py` | Mode, title, style, engine | Ready-to-run project directory (state, config, prompt, storyboard) |
