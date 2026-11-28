# AGENT ONBOARDING GUIDE — FIKRA STUDIO V3.5

This guide enables any fresh AI agent (Gemini, Claude, ChatGPT, Antigravity, Codex, Cursor) to operate FIKRA STUDIO V3.5 accurately in under 60 seconds with zero prior chat history.

## 10-Question Instant Orientation
| # | Question | Authoritative Answer / Entry Point |
|---|---|---|
| 1 | **What is FIKRA STUDIO?** | Agent-First Universal Creative Production System for video direction, prompt engineering, Arabic RTL QA, and Remotion/HyperFrames production (`AGENTS.md`). |
| 2 | **What can it do?** | Mode-isolated creative direction across 9 modes, 32 visual styles, 17 logo animations, 52 reference video cards, automated QA, and project scaffolding. |
| 3 | **What does it NOT claim?** | Never claims unexecuted video renders, synthetic TTS audio, unwatched videos, or synthetic sine waves as real audio measurements. |
| 4 | **Where are the rules?** | `AGENTS.md` (index) → `01_SYSTEM_CORE/SYSTEM_RULES.md`, `MODE_ROUTER.md`, `APPROVAL_POLICY.md`. |
| 5 | **Where are the libraries?** | `03_STYLE_LIBRARY/` (32 styles), `04_LOGO_ANIMATION_LIBRARY/` (17 logo animations), `06_PROMPT_LIBRARY/` (production prompts). |
| 6 | **How do I retrieve assets?** | `python3 -m fikra_v3 graph --style STY-001` or query `09_ASSET_AND_RIGHTS_REGISTRY/ASSET_REGISTRY.sqlite` / `ASSET_REGISTRY.json`. |
| 7 | **How do I choose the operating mode?** | Follow `01_SYSTEM_CORE/MODE_ROUTER.md` or run `python3 -m fikra_v3 context --query "<user request>"`. |
| 8 | **How do I save user approvals?** | Use `fikra_v3.approval_guard.ApprovalGuard` to lock each decision with a SHA-256 digest in `project_state.json`. |
| 9 | **How do I build a Production Prompt?** | Run `python3 -m fikra_v3 compile-prompt --state project_state.json` (enforces mode isolation and locked approvals). |
| 10 | **How do I test the result?** | Run `python3 -m fikra_v3 arabic-qa`, `python3 -m fikra_v3 media-qa`, `python3 -m fikra_v3 readiness`, `python3 -m fikra_v3 integrity`, and `python3 -m unittest discover -s tests -v`. |

## Quick CLI Commands
```bash
# 1. Load minimal context for a FIKRA Channel episode
python3 -m fikra_v3 context --mode FIKRA_CHANNEL_MODE --style STY-001

# 2. Query the Knowledge Graph for a style (specs + prompt + refs + engine)
python3 -m fikra_v3 graph --style STY-001

# 3. Recommend styles for a topic
python3 -m fikra_v3 recommend --topic "الكون والثقوب السوداء" --mode FIKRA_CHANNEL_MODE

# 4. Run full integrity & regression verification
python3 -m fikra_v3 integrity
python3 -m fikra_v3 regression
python3 -m unittest discover -s tests -v
```
