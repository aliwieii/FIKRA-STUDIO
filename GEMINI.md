# GEMINI.md — Thin Agent Router for FIKRA STUDIO V3.3

> **Activation Charter:** [`ACTIVATION_PROMPT.md`](ACTIVATION_PROMPT.md)

1. Read [`AGENTS.md`](AGENTS.md) first (single source of truth for all rules, modes, and constraints).
2. Read [`SYSTEM_MANIFEST.json`](SYSTEM_MANIFEST.json) for machine-readable paths, counts, and CLI commands.
3. Run `python3 -m fikra_v3 context --mode <MODE>` to load only the files needed for the active task (do not sweep all 280+ files).
4. For Gemini-adapted payload generation, run `python3 -m fikra_v3 adapter --target gemini --mode <MODE>`.
5. Never modify `main` or delete files under `archive/baseline_manifests/` or `99_SOURCE_ORIGINALS/`.
