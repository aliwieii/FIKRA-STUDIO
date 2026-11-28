# FIKRA STUDIO V3.6 — Agent-First Universal Creative Production System

> **AI Agents Start Here:** Read [`ACTIVATION_PROMPT.md`](ACTIVATION_PROMPT.md) first as your complete operating charter, then [`AGENTS.md`](AGENTS.md) and [`SYSTEM_MANIFEST.json`](SYSTEM_MANIFEST.json).


[![Version](https://img.shields.io/badge/version-3.0.0--rc.1-blue.svg)](CHANGELOG.md)
[![Branch](https://img.shields.io/badge/branch-development%2Fv3.0-orange.svg)](V3_DEVELOPMENT_PLAN.md)
[![Architecture](https://img.shields.io/badge/architecture-Agent--First-emerald.svg)](AGENTS.md)

**FIKRA STUDIO V3.6** transforms FIKRA STUDIO V2.0 into an executable, verifiable, **Agent-First Creative Production System** that Gemini, Claude, ChatGPT, Antigravity, Cursor, and Codex can understand, query, validate, and operate without relying on prior chat history.

## Start Here (For AI Agents & Engineers)
- **Single Source of Truth:** [`AGENTS.md`](AGENTS.md)
- **Thin Platform Routers:** [`GEMINI.md`](GEMINI.md) · [`CLAUDE.md`](CLAUDE.md)
- **60-Second Onboarding:** [`AGENT_ONBOARDING_GUIDE.md`](AGENT_ONBOARDING_GUIDE.md)
- **Machine-Readable Manifest:** [`SYSTEM_MANIFEST.json`](SYSTEM_MANIFEST.json)
- **Architecture & Map:** [`V3_ARCHITECTURE.md`](V3_ARCHITECTURE.md) · [`PROJECT_MAP.md`](PROJECT_MAP.md)

## Quick Start (Zero External Python Dependencies)
```bash
# 1. Load minimal context for any operating mode
python3 -m fikra_v3 context --mode FIKRA_CHANNEL_MODE --style STY-001

# 2. Query the Knowledge Graph (Style Specs + Prompt + Ref Videos + Engine)
python3 -m fikra_v3 graph --style STY-001

# 3. Recommend styles for a topic
python3 -m fikra_v3 recommend --topic "الكون والثقوب السوداء" --mode FIKRA_CHANNEL_MODE

# 4. Scaffold a new project workspace
python3 -m fikra_v3 bootstrap --out /tmp/demo_proj --id DEMO-01 --title "تجربة" --mode UNIVERSAL_VIDEO_MODE

# 5. Run full automated QA, Integrity & Regression checks
python3 -m unittest discover -s tests -v
python3 -m fikra_v3 integrity
python3 -m fikra_v3 regression
node 08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/scripts/validate-timeline.mjs
```

## Version Map
| Version | Status | Highlights |
|---|---|---|
| **V1.0** | Immutable Baseline (`archive/baseline_manifests/v1_core_sha256_manifest.json`) | 271 files: Central Mode Router, 32 visual styles, 17 logo animations, 52 reference video cards. |
| **V2.0** | Tagged `v2.0.0-baseline` on `main` (284 files) | RTL Command Hub, Remotion 4 starter, HyperFrames HTML starter, visual storyboard. |
| **V3.0 RC** | Active on `development/v3.0` | Agent-First entrypoints, 15 executable `fikra_v3` modules (A–O), unified JSON/CSV/SQLite Asset Registry + Knowledge Graph, fixed Remotion Arabic pagination & real FFmpeg audio analysis, 0 broken links, automated CI & regression tests. |

## Core Governance & Reports
- [`V3_DEVELOPMENT_PLAN.md`](V3_DEVELOPMENT_PLAN.md) · [`SKILLS_AUDIT.md`](SKILLS_AUDIT.md) · [`ISSUES_REGISTER.md`](ISSUES_REGISTER.md)
- [`MIGRATION_MAP.md`](MIGRATION_MAP.md) · [`TEST_STRATEGY.md`](TEST_STRATEGY.md) · [`TEST_RESULTS.md`](TEST_RESULTS.md)
- [`REGRESSION_REPORT.md`](REGRESSION_REPORT.md) · [`V3_READINESS_REPORT.md`](V3_READINESS_REPORT.md) · [`SECURITY.md`](SECURITY.md)
