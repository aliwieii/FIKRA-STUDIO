"""Unified CLI for FIKRA STUDIO V3.0 (`python3 -m fikra_v3 <command>`)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__, repo_root
from .arabic_qa import analyze_arabic_text, validate_srt
from .asset_intelligence import build_asset_registry, query_assets
from .context_loader import load_context
from .integrity_validator import run_integrity_audit
from .knowledge_graph import build_knowledge_graph, lookup_logo, lookup_style
from .media_intelligence import analyze_audio_real
from .model_adapter import build_adapter_payload
from .project_bootstrap import bootstrap_project
from .project_state import load_state
from .prompt_compiler import compile_production_prompt
from .readiness_scorer import score_readiness
from .regression_guard import run_regression_checks
from .style_recommender import recommend_styles


def _p(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="fikra_v3", description=f"FIKRA STUDIO V{__version__} CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ctx = sub.add_parser("context", help="AI Context Loader (Feature A)")
    p_ctx.add_argument("--mode")
    p_ctx.add_argument("--query", default="")
    p_ctx.add_argument("--style")
    p_ctx.add_argument("--logo")

    p_reg = sub.add_parser("build-registry", help="Build unified ASSET_REGISTRY & KNOWLEDGE_GRAPH (Features B+C)")
    p_q = sub.add_parser("search-assets", help="Search SQLite asset registry (Feature C)")
    p_q.add_argument("keyword")
    p_q.add_argument("--category")

    p_g = sub.add_parser("graph", help="Lookup style or logo in Knowledge Graph (Feature B)")
    p_g.add_argument("--style")
    p_g.add_argument("--logo")

    p_rec = sub.add_parser("recommend", help="Recommend visual styles (Feature G)")
    p_rec.add_argument("--topic", required=True)
    p_rec.add_argument("--mode", default="UNIVERSAL_VIDEO_MODE")
    p_rec.add_argument("--top-k", type=int, default=5)

    p_ar = sub.add_parser("arabic-qa", help="Run Arabic RTL & caption QA (Feature I)")
    p_ar.add_argument("--text")
    p_ar.add_argument("--srt")

    p_med = sub.add_parser("media-qa", help="Run real FFmpeg audio/media analysis (Feature H)")
    p_med.add_argument("--file", required=True)

    p_ad = sub.add_parser("adapter", help="Generate agent-specific payload (Feature M)")
    p_ad.add_argument("--target", default="gemini")
    p_ad.add_argument("--mode", default="UNIVERSAL_VIDEO_MODE")

    p_bs = sub.add_parser("bootstrap", help="Scaffold a new project workspace (Feature O)")
    p_bs.add_argument("--out", required=True)
    p_bs.add_argument("--id", required=True)
    p_bs.add_argument("--title", required=True)
    p_bs.add_argument("--mode", default="UNIVERSAL_VIDEO_MODE")
    p_bs.add_argument("--style", default="STY-001")

    p_cp = sub.add_parser("compile-prompt", help="Compile Production Prompt from project_state.json (Feature D)")
    p_cp.add_argument("--state", required=True)

    p_rd = sub.add_parser("readiness", help="Score project readiness (Feature K)")
    p_rd.add_argument("--state", required=True)

    sub.add_parser("integrity", help="Run Automatic Integrity Validator (Feature N)")
    sub.add_parser("regression", help="Run Regression Guard (Feature L)")

    args = parser.parse_args(argv)
    r = repo_root()

    if args.cmd == "context":
        _p(load_context(mode=args.mode, query=args.query, style_id=args.style, logo_id=args.logo, root=r))
    elif args.cmd == "build-registry":
        reg = build_asset_registry(r, write_outputs=True)
        kg = build_knowledge_graph(r, write_output=True)
        _p({"total_assets": reg["total_assets"], "graph_counts": kg["counts"]})
    elif args.cmd == "search-assets":
        _p(query_assets(args.keyword, category=args.category, root=r))
    elif args.cmd == "graph":
        if args.style:
            _p(lookup_style(args.style, root=r))
        elif args.logo:
            _p(lookup_logo(args.logo, root=r))
        else:
            _p(build_knowledge_graph(r, write_output=False)["counts"])
    elif args.cmd == "recommend":
        _p(recommend_styles(args.topic, mode=args.mode, top_k=args.top_k, root=r))
    elif args.cmd == "arabic-qa":
        if args.srt:
            _p(validate_srt(Path(args.srt).read_text(encoding="utf-8-sig")))
        else:
            _p(analyze_arabic_text(args.text or ""))
    elif args.cmd == "media-qa":
        _p(analyze_audio_real(Path(args.file)))
    elif args.cmd == "adapter":
        _p(build_adapter_payload(target=args.target, mode=args.mode, root=r))
    elif args.cmd == "bootstrap":
        _p(bootstrap_project(Path(args.out), args.id, args.title, mode=args.mode, style_id=args.style, root=r))
    elif args.cmd == "compile-prompt":
        _p(compile_production_prompt(load_state(Path(args.state)), root=r))
    elif args.cmd == "readiness":
        _p(score_readiness(load_state(Path(args.state))))
    elif args.cmd == "integrity":
        res = run_integrity_audit(r)
        _p(res)
        return 0 if res["pass"] else 1
    elif args.cmd == "regression":
        res = run_regression_checks(r)
        _p(res)
        return 0 if res["pass"] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
