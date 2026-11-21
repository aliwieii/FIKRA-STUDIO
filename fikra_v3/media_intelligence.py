"""Feature H: Media Intelligence — Real FFprobe/FFmpeg audio & video analysis (zero false PASS)."""
from __future__ import annotations

import hashlib
import json
import math
import re
import struct
import subprocess
from pathlib import Path
from typing import Any


def sha256_media(media_path: Path) -> str:
    h = hashlib.sha256()
    with media_path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_media(media_path: Path, timeout: int = 30) -> dict[str, Any]:
    if not media_path.exists():
        raise FileNotFoundError(f"Media file not found: {media_path}")
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(media_path)],
        capture_output=True, text=True, timeout=timeout,
    )
    if res.returncode != 0 or not res.stdout.strip():
        raise RuntimeError(f"ffprobe failed (rc={res.returncode}): {res.stderr.strip()}")
    return json.loads(res.stdout)


def analyze_audio_real(media_path: Path, fps: int = 30, silence_db: float = -45.0, timeout: int = 60) -> dict[str, Any]:
    """Measure real duration, volume (mean/max dB), silence intervals, and per-frame RMS envelope via FFmpeg."""
    info = probe_media(media_path, timeout=timeout)
    duration = float(info.get("format", {}).get("duration", 0.0))
    a_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
    if a_stream is None:
        return {
            "measurement_type": "REAL_FFMPEG_ANALYSIS",
            "has_audio": False,
            "pass": False,
            "duration_sec": duration,
            "error": "No audio stream detected in media file.",
        }

    vol_res = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(media_path),
            "-af", f"volumedetect,silencedetect=noise={silence_db}dB:d=0.35",
            "-f", "null", "-",
        ],
        capture_output=True, text=True, timeout=timeout,
    )
    if vol_res.returncode != 0:
        raise RuntimeError(f"ffmpeg volumedetect failed (rc={vol_res.returncode}): {vol_res.stderr.strip()[:400]}")

    stderr = vol_res.stderr
    mean_m = re.search(r"mean_volume:\s*([-\d.]+)\s*dB", stderr)
    max_m = re.search(r"max_volume:\s*([-\d.]+)\s*dB", stderr)
    if not mean_m or not max_m:
        raise RuntimeError("ffmpeg volumedetect succeeded but returned no volume metrics.")

    sil_starts = [float(x) for x in re.findall(r"silence_start:\s*([\d.]+)", stderr)]
    sil_ends = [float(x) for x in re.findall(r"silence_end:\s*([\d.]+)", stderr)]
    silences = [
        {"start": sil_starts[i], "end": sil_ends[i] if i < len(sil_ends) else duration}
        for i in range(len(sil_starts))
    ]

    sr = 8000
    pcm_res = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(media_path), "-ac", "1", "-ar", str(sr), "-f", "s16le", "pipe:1"],
        capture_output=True, timeout=timeout,
    )
    if pcm_res.returncode != 0:
        raise RuntimeError(f"ffmpeg PCM decode failed (rc={pcm_res.returncode}): {pcm_res.stderr.decode('utf-8', 'ignore')[:400]}")

    raw = pcm_res.stdout
    total_samples = len(raw) // 2
    samples = struct.unpack(f"<{total_samples}h", raw[: total_samples * 2]) if total_samples else ()
    samples_per_frame = max(1, sr // fps)
    envelope = []
    for i in range(0, len(samples), samples_per_frame):
        chunk = samples[i : i + samples_per_frame]
        if not chunk:
            continue
        rms = math.sqrt(sum(s * s for s in chunk) / len(chunk)) / 32768.0
        envelope.append(round(min(1.0, rms * 3.0), 4))

    max_db = float(max_m.group(1))
    return {
        "measurement_type": "REAL_FFMPEG_ANALYSIS",
        "file": media_path.name,
        "sha256": sha256_media(media_path),
        "has_audio": True,
        "pass": duration > 0 and max_db < -0.2,
        "duration_sec": round(duration, 3),
        "sample_rate": int(a_stream.get("sample_rate", 0)),
        "channels": int(a_stream.get("channels", 0)),
        "mean_volume_db": float(mean_m.group(1)),
        "max_volume_db": max_db,
        "clipping_risk": max_db >= -0.2,
        "silence_intervals": silences,
        "fps": fps,
        "envelope_frames": len(envelope),
        "envelope": envelope,
    }


def detect_black_frames(media_path: Path, min_duration: float = 0.2, pix_th: float = 0.10, timeout: int = 60) -> dict[str, Any]:
    """Run real FFmpeg blackdetect filter; strictly fails on non-zero returncode or invalid media."""
    if not media_path.exists():
        raise FileNotFoundError(f"Media file not found: {media_path}")
    # Verify valid video stream via ffprobe first
    info = probe_media(media_path, timeout=timeout)
    v_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    if v_stream is None:
        return {
            "measurement_type": "REAL_FFMPEG_BLACKDETECT",
            "status": "ERROR",
            "error": "No video stream found.",
            "black_intervals_count": 0,
            "black_intervals": [],
            "pass": False,
        }

    res = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(media_path),
            "-vf", f"blackdetect=d={min_duration}:pix_th={pix_th}",
            "-an", "-f", "null", "-",
        ],
        capture_output=True, text=True, timeout=timeout,
    )
    if res.returncode != 0:
        return {
            "measurement_type": "REAL_FFMPEG_BLACKDETECT",
            "status": "ERROR",
            "returncode": res.returncode,
            "error": res.stderr.strip()[:400],
            "black_intervals_count": 0,
            "black_intervals": [],
            "pass": False,
        }

    intervals = []
    for m in re.finditer(r"black_start:([\d.]+)\s+black_end:([\d.]+)\s+black_duration:([\d.]+)", res.stderr):
        intervals.append({
            "start": float(m.group(1)),
            "end": float(m.group(2)),
            "duration": float(m.group(3)),
        })
    return {
        "measurement_type": "REAL_FFMPEG_BLACKDETECT",
        "status": "OK",
        "returncode": 0,
        "black_intervals_count": len(intervals),
        "black_intervals": intervals,
        "pass": len(intervals) == 0,
    }
