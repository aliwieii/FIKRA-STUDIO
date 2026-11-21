# Security Policy — FIKRA STUDIO V3.0

## Secret & Privacy Guardrails
- No API keys, OAuth tokens, private keys, or `.env` files may be committed to this repository or printed in GitHub Actions logs.
- `fikra_v3.integrity_validator` runs an automated secret-pattern scan on every CI run.
- External agent skills must be audited in `SKILLS_AUDIT.md` before adoption.

## Reporting a Vulnerability
Report security issues privately to the repository owner (`aliwieii`) via GitHub Private Vulnerability Reporting rather than opening a public issue.
