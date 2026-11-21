# Contributing to FIKRA STUDIO V3.0

1. **Branching:** Never commit directly to `main`. Create a feature branch from `development/v3.0`.
2. **Non-Destructive Rule:** Never delete or overwrite historical manifests in `archive/baseline_manifests/` or `99_SOURCE_ORIGINALS/`.
3. **Mandatory Verification Before PR:**
   ```bash
   python3 -m unittest discover -s tests -v
   python3 -m fikra_v3 integrity
   python3 -m fikra_v3 regression
   node 08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/scripts/validate-timeline.mjs
   ```
4. **No Unverified Claims:** Every `PASS` in `TEST_RESULTS.md` must cite executable command output.
5. **Security:** Never commit API keys, tokens, `.env` files, or private user media.
