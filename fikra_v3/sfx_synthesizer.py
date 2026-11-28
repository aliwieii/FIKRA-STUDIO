"""V3.5 Zero-Music SFX Synthesizer (13 Procedural Sound Effects, ZERO Background Music)."""
from __future__ import annotations

import json
import math
import random
import struct
import wave
from pathlib import Path
from typing import Any

SUPPORTED_SFX = (
    "whoosh", "swell", "soft", "pop", "tick", "click",
    "chime", "ding", "thud", "step", "sparkle", "riser", "heartbeat",
)
SR = 44100


def _stdlib_sfx(name: str) -> list[float]:
    """Pure-Python zero-dependency fallback synthesizer for clean CI environments."""
    rng = random.Random(1)
    durations = {
        "whoosh": 0.45, "swell": 0.62, "soft": 0.50, "pop": 0.12,
        "tick": 0.04, "click": 0.03, "chime": 1.20, "ding": 0.90,
        "thud": 0.35, "step": 0.09, "sparkle": 0.80, "riser": 1.00, "heartbeat": 1.40,
    }
    d = durations.get(name, 0.25)
    n = int(SR * d)
    out = [0.0] * n
    for i in range(n):
        t = i / SR
        k = i / max(1, n - 1)
        if name in {"whoosh", "soft", "step"}:
            env = math.sin(math.pi * k) ** 2
            out[i] = (rng.uniform(-1, 1) * 0.5) * env
        elif name in {"pop", "thud"}:
            f0, f1 = (900.0, 320.0) if name == "pop" else (110.0, 40.0)
            freq = f0 + (f1 - f0) * k
            env = math.exp(-t / 0.05)
            out[i] = math.sin(2 * math.pi * freq * t) * env
        elif name in {"tick", "click"}:
            env = math.exp(-t / 0.006)
            val = math.sin(2 * math.pi * 2600 * t) if name == "tick" else rng.uniform(-1, 1)
            out[i] = val * env
        elif name in {"chime", "ding", "sparkle"}:
            env = math.exp(-t / 0.32)
            out[i] = (math.sin(2 * math.pi * 1046.5 * t) + 0.45 * math.sin(2 * math.pi * 1568 * t)) * env * 0.5
        elif name in {"swell", "riser"}:
            freq = 220.0 + 700.0 * (k ** 2)
            out[i] = math.sin(2 * math.pi * freq * t) * (k ** 2) * (1 - k * 0.2) * 0.6
        elif name == "heartbeat":
            p1 = math.exp(-((t - 0.05) / 0.04) ** 2) if t < 0.25 else 0.0
            p2 = 0.7 * math.exp(-((t - 0.23) / 0.04) ** 2) if 0.18 < t < 0.45 else 0.0
            out[i] = math.sin(2 * math.pi * 65 * t) * (p1 + p2)
    return out


def synthesize_sfx_wav(
    cues: list[dict[str, Any]],
    duration_sec: float,
    output_wav: Path,
) -> dict[str, Any]:
    """Render a real stereo WAV file containing ONLY justified SFX (zero music)."""
    if duration_sec <= 0:
        raise ValueError("duration_sec must be > 0")
    total_samples = int(SR * (duration_sec + 0.3))
    buf = [0.0] * total_samples
    placed = []

    for c in cues:
        name = str(c.get("name", "pop")).lower().strip()
        if name not in SUPPORTED_SFX:
            raise ValueError(f"Unsupported SFX '{name}'. Allowed: {SUPPORTED_SFX}")
        t_sec = max(0.0, float(c.get("time_sec", 0.0)))
        gain_db = float(c.get("gain_db", -4.0))
        gain = (10 ** (gain_db / 20.0)) * 0.55
        samples = _stdlib_sfx(name)
        idx = int(t_sec * SR)
        for j, v in enumerate(samples):
            if idx + j < total_samples:
                buf[idx + j] += v * gain
        placed.append({"name": name, "time_sec": round(t_sec, 3), "gain_db": gain_db})

    peak = max((abs(x) for x in buf), default=0.0)
    scale = (0.85 / peak) if peak > 1e-6 else 1.0
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        frames = bytearray()
        for x in buf:
            val = max(-32767, min(32767, int(x * scale * 32767)))
            frames.extend(struct.pack("<hh", val, val))
        wf.writeframes(bytes(frames))

    return {
        "pass": True,
        "output_wav": str(output_wav),
        "duration_sec": round(duration_sec + 0.3, 2),
        "sample_rate": SR,
        "channels": 2,
        "cues_placed": len(placed),
        "sfx_only_zero_music": True,
        "cues": placed,
    }


def synthesize_from_meta(meta_json: Path, output_wav: Path) -> dict[str, Any]:
    """Generate SFX WAV directly from Khatt-w-Noor / FIKRA meta.json beats."""
    meta = json.loads(meta_json.read_text(encoding="utf-8"))
    cues: list[dict[str, Any]] = []
    for idx, b in enumerate(meta.get("beats", [])):
        t0 = float(b.get("t", 0.0))
        if idx > 0:
            tr = b.get("tr", "iris")
            if tr == "wipe":
                cues.append({"time_sec": max(0.0, t0 - 0.22), "name": "whoosh", "gain_db": -5.0})
            elif tr == "iris":
                cues.append({"time_sec": max(0.0, t0 - 0.45), "name": "swell", "gain_db": -6.0})
            elif tr == "fade":
                cues.append({"time_sec": max(0.0, t0 - 0.20), "name": "soft", "gain_db": -7.0})
        for s in b.get("sfx", []):
            lt, name = float(s[0]), str(s[1])
            gdb = float(s[2]) if len(s) > 2 else -4.0
            cues.append({"time_sec": max(0.0, t0 + lt), "name": name, "gain_db": gdb})
    return synthesize_sfx_wav(cues, float(meta.get("dur", 10.0)), output_wav)
