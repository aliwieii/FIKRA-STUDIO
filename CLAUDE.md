# CLAUDE.md — Thin Agent Router for FIKRA STUDIO V3.0

> **Activation Charter:** [`ACTIVATION_PROMPT.md`](ACTIVATION_PROMPT.md)

1. Read [`AGENTS.md`](AGENTS.md) first (single source of truth for all rules, modes, and constraints).
2. Read [`SYSTEM_MANIFEST.json`](SYSTEM_MANIFEST.json) for machine-readable paths, counts, and CLI commands.
3. Run `python3 -m fikra_v3 context --mode <MODE>` to retrieve the exact minimal context bundle.
4. For Claude-adapted payload generation, run `python3 -m fikra_v3 adapter --target claude --mode <MODE>`.
5. Run `python3 -m unittest discover -s tests -v` and `python3 -m fikra_v3 integrity` after every code or registry change.
