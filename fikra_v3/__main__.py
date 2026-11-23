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
from .approval_guard import lock_decision
from .media_intelligence import analyze_audio_real, detect_black_frames
from .model_adapter import build_adapter_payload
from .project_bootstrap import bootstrap_project
from .project_state import advance_stage, create_project_state, load_state, save_state
from .prompt_compiler import compile_production_prompt, compile_v32_production_prompt
from .readiness_scorer import score_readiness
from .regression_guard import run_regression_checks
from .style_recommender import compare_styles, recommend_styles
from .motion_craft import check_motion_craft_compliance, list_narrative_archetypes, list_reel_effects
from .visual_intelligence import extract_contact_sheet, verify_reference_access


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
    p_st = sub.add_parser("state", help="Manage Project State Machine (Feature E)")
    st_sub = p_st.add_subparsers(dest="state_cmd", required=True)
    p_si = st_sub.add_parser("init", help="Initialize a new project_state.json")
    p_si.add_argument("--out", required=True)
    p_si.add_argument("--id", required=True)
    p_si.add_argument("--title", required=True)
    p_si.add_argument("--mode", default="UNIVERSAL_VIDEO_MODE")
    p_si.add_argument("--aspect", default=None)
    p_sa = st_sub.add_parser("advance", help="Advance stage with explicit approval")
    p_sa.add_argument("--state", required=True)
    p_sa.add_argument("--to", required=True)
    p_sa.add_argument("--approve", action="store_true")
    p_bd = sub.add_parser("blackdetect", help="Run FFmpeg black-frame detector (Feature H)")
    p_bd.add_argument("--file", required=True)
    p_cs = sub.add_parser("contact-sheet", help="Extract labeled FFmpeg Contact Sheet (V3.2)")
    p_cs.add_argument("--video", required=True)
    p_cs.add_argument("--out", required=True)
    p_cs.add_argument("--ref-id", default="REF-CUSTOM")
    p_cs.add_argument("--frames", type=int, default=6)
    p_cmp = sub.add_parser("compare-styles", help="6-Criteria Weighted Style Comparison (V3.2)")
    p_cmp.add_argument("--topic", required=True)
    p_cmp.add_argument("--mode", default="UNIVERSAL_VIDEO_MODE")
    p_cmp.add_argument("--tool", default="remotion_motion")
    p_pr = sub.add_parser("presets", help="List V3.4 Narrative Archetypes & Reel Effects")
    p_pr.add_argument("--mode")
    p_cc = sub.add_parser("craft-check", help="Run V3.4 Anti-Slide & No-Music compliance audit")
    p_cc.add_argument("--file")
    p_cc.add_argument("--text", default="")
    p_cc.add_argument("--engine", default="remotion")

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
    elif args.cmd == "state":
        if args.state_cmd == "init":
            st = create_project_state(args.id, args.title, mode=args.mode, aspect_ratio=args.aspect)
            saved = save_state(st, Path(args.out))
            _p({"saved": str(saved), "stage": st["stage"], "mode": st["mode"]})
        elif args.state_cmd == "advance":
            sp = Path(args.state)
            st = advance_stage(load_state(sp), args.to, user_approved=args.approve)
            save_state(st, sp)
            _p({"stage": st["stage"], "updated_at_utc": st["updated_at_utc"]})
    elif args.cmd == "blackdetect":
        rep = detect_black_frames(Path(args.file))
        _p(rep)
        return 0 if rep["pass"] else 1
    elif args.cmd == "contact-sheet":
        _p(extract_contact_sheet(Path(args.video), Path(args.out), args.ref_id, num_frames=args.frames))
    elif args.cmd == "compare-styles":
        _p(compare_styles(args.topic, mode=args.mode, target_tool=args.tool, root=r))
    elif args.cmd == "presets":
        _p({"archetypes": list_narrative_archetypes(mode=args.mode, root=r), "reel_effects": list_reel_effects(root=r)})
    elif args.cmd == "craft-check":
        payload = Path(args.file).read_text(encoding="utf-8") if args.file else args.text
        rep = check_motion_craft_compliance(payload, engine=args.engine)
        _p(rep)
        return 0 if rep["pass"] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
