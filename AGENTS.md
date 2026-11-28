# AGENTS.md — FIKRA STUDIO V3.6 (Single Source of Truth)

> **Activation Charter:** [`ACTIVATION_PROMPT.md`](ACTIVATION_PROMPT.md)

> **Identity:** `AGENT-FIRST UNIVERSAL CREATIVE PRODUCTION SYSTEM`
> **Target Audience:** Gemini, Claude, ChatGPT, Antigravity, Cursor, Codex, and any modern AI agent.
> **Rule:** This file is the **single canonical entry point** for agent rules and routing. Platform files (`GEMINI.md`, `CLAUDE.md`) are thin routers pointing here — never duplicate full rules into platform-specific files.

---

## 1. What Is FIKRA STUDIO?
FIKRA STUDIO V3.6 is a modular, forensic-grade creative production direction, prompt engineering, asset intelligence, and programmatic video engineering system supporting Arabic-first and universal video workflows.

## 2. What Can It Do?
- Route any creative request into **9 strictly isolated operating modes** (`UNIVERSAL_VIDEO_MODE`, `FIKRA_CHANNEL_MODE`, `QURAN_MODE`, `PODCAST_SHORT_MODE`, `LOGO_ANIMATION_MODE`, `PROMPT_ONLY_MODE`, `REFERENCE_AUDIT_MODE`, `VISUAL_UPGRADE_MODE`, `STICKMAN_COMEDY_MODE`).
- Recommend and retrieve full specifications for **32 verified visual styles** (`STY-001`..`STY-032`), **17 SVG logo animations** (`L01`..`L17`), and **52 cataloged reference videos** (`REF-001`..`REF-022`, `MSTY-01`..`MSTY-10`, `MLOGO-01`..`MLOGO-20`).
- Compile self-contained Production Prompts, lock user approvals with SHA-256 cryptographic protection (`fikra_v3.approval_guard`), validate Arabic RTL & caption integrity without word truncation (`fikra_v3.arabic_qa`), run real `ffmpeg`/`ffprobe` audio/video analysis (`fikra_v3.media_intelligence`), and scaffold Remotion 4 / HyperFrames HTML video projects (`fikra_v3.project_bootstrap`).

## 3. What Does It NOT Claim to Do?
- It **never** claims to render video, synthesize voiceover, or watch a video unless those tools actually executed and produced verified outputs.
- It **never** reports synthetic sine waves as real audio analysis.
- It **never** upgrades a project's readiness level (`PROMPT_READY` → `SPEC_READY` → `CODE_READY` → `BUILD_TESTED` → `RENDER_TESTED`) without verifiable build/render artifacts.

## 4. Where Are the Rules, Libraries & Assets?
Use `SYSTEM_MANIFEST.json` and `python3 -m fikra_v3 context --mode <MODE>` instead of scanning hundreds of files:
- **Core Rules & Conflict Policy:** `01_SYSTEM_CORE/SYSTEM_RULES.md`, `01_SYSTEM_CORE/MODE_ROUTER.md`, `01_SYSTEM_CORE/APPROVAL_POLICY.md`
- **Workflows:** `02_WORKFLOWS/UNIVERSAL_VIDEO_WORKFLOW.md`, `02_WORKFLOWS/FIKRA_CHANNEL_WORKFLOW.md`, `02_WORKFLOWS/SPECIAL_MODES.md`
- **Visual Styles (32):** `03_STYLE_LIBRARY/STYLE_REGISTRY.csv` & `03_STYLE_LIBRARY/STYLE_INDEX.md`
- **Logo Animations (17):** `04_LOGO_ANIMATION_LIBRARY/LOGO_REGISTRY.csv` & `04_LOGO_ANIMATION_LIBRARY/LOGO_ANIMATION_INDEX.md`
- **Prompt Templates:** `06_PROMPT_LIBRARY/`
- **Unified Asset Registry & Knowledge Graph:** `09_ASSET_AND_RIGHTS_REGISTRY/ASSET_REGISTRY.json`, `ASSET_REGISTRY.csv`, `ASSET_REGISTRY.sqlite`, `KNOWLEDGE_GRAPH.json`
- **Production Engines:** `08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/`, `HYPERFRAMES_HTML_VIDEO_TEMPLATE/`, `MOTALIM_PYTHON_SCRIPTS/`
- **V3.0 Executable CLI & Modules:** `fikra_v3/`

## 5. Strict Mode Isolation & 6-Level Conflict Hierarchy
1. Safety, copyright, technical integrity, and Quranic/religious guardrails (highest priority).
2. Explicit current user request.
3. Locked approved project decisions (`project_state.json` + SHA-256 lock).
4. Active mode rules (never leak FIKRA Channel's 10 categories, `FIKRA VOICE 01`, no-music policy, or 9:16 default into `UNIVERSAL_VIDEO_MODE`).
5. General system rules.
6. Defaults (lowest priority).

## 6. Agent Execution Loop (Fast 5-Step Protocol)
1. **Load Context:** Run `python3 -m fikra_v3 context --mode <MODE> [--style STY-XXX]` to get the exact minimal file list.
2. **Initialize / Load State:** Run `python3 -m fikra_v3 state init ...` or load `project_state.json`.
3. **Lock Approvals:** Record every user approval (`idea`, `script`, `voiceover`, `style`, `character`, `storyboard`) via `fikra_v3.approval_guard` — never silently mutate a locked decision.
4. **Compile & Inspect:** Compile Production Prompt via `python3 -m fikra_v3 compile-prompt ...`, run Arabic QA (`python3 -m fikra_v3 arabic-qa ...`), and score readiness (`python3 -m fikra_v3 readiness ...`).
5. **Verify Before Delivery:** Run `python3 -m unittest discover -s tests -v` and `python3 -m fikra_v3 integrity` before claiming completion.
