#!/usr/bin/env python3
"""FIKRA STUDIO V2.0 — Automated Media & Production QA Pipeline.
Inspired by hyperframes-media + verification-before-completion.
Usage:
    python3 fikra_media_qa_pipeline.py --video output.mp4 [--srt captions.srt]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def probe_video(video_path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", str(video_path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {res.stderr.strip()}")
    return json.loads(res.stdout)


def validate_srt(srt_path: Path) -> dict:
    txt = srt_path.read_text(encoding="utf-8-sig", errors="replace")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", txt.strip()) if b.strip()]
    ts_pat = re.compile(r"\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}")
    valid_ts = sum(1 for b in blocks if ts_pat.search(b))
    return {"total_blocks": len(blocks), "valid_timestamps": valid_ts, "pass": len(blocks) > 0 and valid_ts == len(blocks)}


def main():
    parser = argparse.ArgumentParser(description="FIKRA STUDIO V2.0 Media QA Gate")
    parser.add_argument("--video", required=True, help="Path to rendered MP4 video")
    parser.add_argument("--srt", help="Optional path to SRT subtitle file")
    parser.add_argument("--expect-width", type=int, default=1080)
    parser.add_argument("--expect-height", type=int, default=1920)
    args = parser.parse_args()

    vpath = Path(args.video)
    if not vpath.exists():
        print(f"FAIL: Video not found: {vpath}")
        sys.exit(1)

    info = probe_video(vpath)
    v_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    a_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)

    checks = {
        "has_video": v_stream is not None,
        "has_audio": a_stream is not None,
        "resolution_match": bool(v_stream and v_stream.get("width") == args.expect_width and v_stream.get("height") == args.expect_height),
        "codec_h264": bool(v_stream and v_stream.get("codec_name") == "h264"),
        "duration_sec": float(info.get("format", {}).get("duration", 0.0)),
    }
    if args.srt:
        checks["srt"] = validate_srt(Path(args.srt))

    passed = checks["has_video"] and checks["has_audio"] and checks["resolution_match"] and checks["codec_h264"]
    if args.srt:
        passed = passed and checks["srt"]["pass"]

    print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": checks}, ensure_ascii=False, indent=2))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
