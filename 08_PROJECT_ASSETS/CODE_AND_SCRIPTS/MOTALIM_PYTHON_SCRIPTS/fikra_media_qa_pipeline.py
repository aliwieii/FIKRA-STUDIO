#!/usr/bin/env python3
"""FIKRA STUDIO V3.1.1 — Full Real Media & Arabic QA Pipeline (Fixes FIK-006).
Executes ffprobe stream verification, FFmpeg volumedetect/silencedetect/RMS envelope,
FFmpeg blackdetect (unintended black frames), Arabic SRT QA, and SHA-256 binding.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fikra_v3.arabic_qa import validate_srt
from fikra_v3.media_intelligence import analyze_audio_real, detect_black_frames, probe_media, sha256_media


def run_pipeline(
    video_path: Path,
    srt_path: Path | None = None,
    expect_w: int = 1080,
    expect_h: int = 1920,
    require_audio: bool = True,
) -> dict:
    info = probe_media(video_path)
    v_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    audio_report = analyze_audio_real(video_path)
    black_report = detect_black_frames(video_path)
    srt_report = validate_srt(srt_path.read_text(encoding="utf-8-sig")) if srt_path and srt_path.exists() else None

    checks = {
        "has_video": v_stream is not None,
        "resolution_match": bool(v_stream and v_stream.get("width") == expect_w and v_stream.get("height") == expect_h),
        "has_audio": True if not require_audio else bool(audio_report.get("has_audio")),
        "no_clipping": True if not audio_report.get("has_audio") else (not bool(audio_report.get("clipping_risk"))),
        "no_black_frames": bool(black_report.get("pass")),
        "srt_pass": True if srt_report is None else bool(srt_report.get("pass")),
    }
    return {
        "pass": all(checks.values()),
        "video_file": video_path.name,
        "video_sha256": sha256_media(video_path),
        "checks": checks,
        "video_stream": {
            "width": v_stream.get("width") if v_stream else None,
            "height": v_stream.get("height") if v_stream else None,
            "codec": v_stream.get("codec_name") if v_stream else None,
            "r_frame_rate": v_stream.get("r_frame_rate") if v_stream else None,
        },
        "audio_analysis": {k: v for k, v in audio_report.items() if k != "envelope"},
        "envelope_frames": audio_report.get("envelope_frames", 0),
        "black_frame_analysis": black_report,
        "srt_analysis": srt_report,
    }


def main():
    parser = argparse.ArgumentParser(description="FIKRA STUDIO V3.1.1 Full Media & Arabic QA Gate")
    parser.add_argument("--video", required=True)
    parser.add_argument("--srt")
    parser.add_argument("--expect-width", type=int, default=1080)
    parser.add_argument("--expect-height", type=int, default=1920)
    parser.add_argument("--write-report", help="Optional path to save SHA-256-bound QA report JSON")
    args = parser.parse_args()

    report = run_pipeline(Path(args.video), Path(args.srt) if args.srt else None, args.expect_width, args.expect_height)
    if args.write_report:
        Path(args.write_report).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()
