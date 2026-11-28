"""Feature I: Arabic QA Engine — RTL, shaping, diacritics, BiDi, zero-drop caption pagination, SRT QA."""
from __future__ import annotations
from pathlib import Path

import re
from typing import Any

ARABIC_RANGE = re.compile(r"[\u0600-\u06FF]")
LATIN_RANGE = re.compile(r"[A-Za-z]")
DIACRITICS = re.compile(r"[\u064B-\u065F\u0670]")
ISOLATED_FORMS = re.compile(r"[\uFE70-\uFEFF]")
BROKEN_SPACED_LETTERS = re.compile(r"(?:^|\s)([\u0621-\u064A]\s+){3,}[\u0621-\u064A](?:\s|$)")


def paginate_arabic_caption(words: list[dict[str, Any]], max_words_per_line: int = 6) -> list[list[dict[str, Any]]]:
    """Split a word-timed Arabic caption into non-overlapping pages with ZERO word deletion."""
    if max_words_per_line < 1:
        raise ValueError("max_words_per_line must be >= 1")
    if not words:
        return []
    return [words[i : i + max_words_per_line] for i in range(0, len(words), max_words_per_line)]


def active_caption_page(
    words: list[dict[str, Any]],
    current_sec: float,
    max_words_per_line: int = 6,
) -> list[dict[str, Any]]:
    """Return the active rolling page of words for `current_sec` without ever dropping words."""
    pages = paginate_arabic_caption(words, max_words_per_line=max_words_per_line)
    if not pages:
        return []
    for page in pages:
        p_end = page[-1].get("end", 0.0)
        if current_sec <= p_end + 0.05:
            return page
    return pages[-1]


def analyze_arabic_text(text: str, duration_sec: float | None = None, max_chars_mobile: int = 42) -> dict[str, Any]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    issues = []
    has_arabic = bool(ARABIC_RANGE.search(text))
    has_latin = bool(LATIN_RANGE.search(text))
    diacritics_count = len(DIACRITICS.findall(text))
    isolated_forms_count = len(ISOLATED_FORMS.findall(text))
    spaced_letters_hits = len(BROKEN_SPACED_LETTERS.findall(text))

    if isolated_forms_count > 0:
        issues.append(f"Found {isolated_forms_count} presentation-form/isolated Arabic glyphs (risk of broken shaping).")
    if spaced_letters_hits > 0:
        issues.append("Detected split single Arabic letters separated by spaces (letter-by-letter animation anti-pattern).")

    long_lines = [ln for ln in lines if len(ln) > max_chars_mobile]
    if long_lines:
        issues.append(f"{len(long_lines)} line(s) exceed mobile readability limit ({max_chars_mobile} chars) — paginate without deleting words.")

    mixed_bidi_warning = False
    if has_arabic and has_latin and ("\u2066" not in text and "\u200f" not in text):
        mixed_bidi_warning = True

    words = re.findall(r"\S+", text)
    cps = round(len(text.replace("\n", " ")) / duration_sec, 2) if duration_sec and duration_sec > 0 else None
    wpm = round((len(words) / duration_sec) * 60.0, 1) if duration_sec and duration_sec > 0 else None
    if cps is not None and cps > 22.0:
        issues.append(f"Reading speed too fast for mobile ({cps} chars/sec > 22 CPS).")

    return {
        "has_arabic": has_arabic,
        "has_mixed_latin": has_latin,
        "mixed_bidi_isolation_recommended": mixed_bidi_warning,
        "word_count": len(words),
        "line_count": len(lines),
        "diacritics_count": diacritics_count,
        "isolated_forms_count": isolated_forms_count,
        "spaced_letters_hits": spaced_letters_hits,
        "long_lines_count": len(long_lines),
        "cps": cps,
        "wpm": wpm,
        "issues": issues,
        "pass": isolated_forms_count == 0 and spaced_letters_hits == 0 and (cps is None or cps <= 22.0),
    }


def _parse_srt_ts(ts: str) -> float:
    h, m, s_ms = ts.strip().split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def validate_srt(srt_text: str) -> dict[str, Any]:
    blocks = [b.strip() for b in re.split(r"\r?\n\s*\r?\n", srt_text.strip()) if b.strip()]
    ts_re = re.compile(r"^(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})$")
    errors = []
    prev_end = 0.0
    total_words = 0
    for idx, blk in enumerate(blocks, 1):
        lines = blk.splitlines()
        if len(lines) < 3:
            errors.append(f"Block {idx}: incomplete SRT block.")
            continue
        m = ts_re.match(lines[1].strip())
        if not m:
            errors.append(f"Block {idx}: invalid timestamp '{lines[1]}'.")
            continue
        start, end = _parse_srt_ts(m.group(1)), _parse_srt_ts(m.group(2))
        if end <= start:
            errors.append(f"Block {idx}: end <= start ({start} -> {end}).")
        if start < prev_end - 0.001:
            errors.append(f"Block {idx}: timestamp overlap ({start:.3f} < {prev_end:.3f}).")
        prev_end = end
        body = "\n".join(lines[2:])
        qa = analyze_arabic_text(body, duration_sec=max(0.1, end - start))
        total_words += qa["word_count"]
        if not qa["pass"]:
            errors.append(f"Block {idx}: Arabic QA failed ({'; '.join(qa['issues'])})")

    return {
        "total_blocks": len(blocks),
        "total_words": total_words,
        "errors": errors,
        "pass": len(blocks) > 0 and len(errors) == 0,
    }


def render_arabic_caption_fixture(
    text: str,
    output_png: Path,
    aspect_ratio: str = "9:16",
    font_size: int | None = None,
) -> dict[str, Any]:
    """V3.6 Render-level Arabic Caption QA: renders caption inside safe zones and verifies zero overflow."""
    dims = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080)}
    w, h = dims.get(aspect_ratio, (1080, 1920))
    fsize = font_size or (48 if w == 1080 else 54)
    text_qa = analyze_arabic_text(text)

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return {
            "pass": text_qa["pass"],
            "render_executed": False,
            "reason": "Pillow unavailable; text-level QA only.",
            "text_qa": text_qa,
        }

    # Safe-zone bounds per aspect ratio
    margin_x = int(w * 0.08)
    safe_top = int(h * (0.14 if aspect_ratio == "9:16" else 0.08))
    safe_bottom = int(h * (0.78 if aspect_ratio == "9:16" else 0.90))
    max_text_w = w - 2 * margin_x

    im = Image.new("RGB", (w, h), (10, 15, 28))
    draw = ImageDraw.Draw(im)
    # Safe-zone guide rectangle
    draw.rectangle([margin_x, safe_top, w - margin_x, safe_bottom], outline=(56, 189, 248), width=2)

    font = None
    for candidate in (
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(candidate).exists():
            font = ImageFont.truetype(candidate, fsize)
            break
    if font is None:
        font = ImageFont.load_default()

    # Word wrap cleanly without dropping words
    words = text.split()
    lines, cur = [], []
    for wd in words:
        trial = " ".join(cur + [wd])
        bbox = draw.textbbox((0, 0), trial, font=font)
        if (bbox[2] - bbox[0]) <= max_text_w or not cur:
            cur.append(wd)
        else:
            lines.append(" ".join(cur))
            cur = [wd]
    if cur:
        lines.append(" ".join(cur))

    y = int(h * 0.22) if aspect_ratio == "9:16" else int(h * 0.72)
    overflow = False
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        if lw > max_text_w or (y + lh) > safe_bottom:
            overflow = True
        draw.text((max(margin_x, (w - lw) // 2), y), ln, fill=(248, 250, 252), font=font)
        y += int(lh * 1.45) + 6

    output_png.parent.mkdir(parents=True, exist_ok=True)
    im.save(output_png)

    return {
        "pass": text_qa["pass"] and (not overflow) and output_png.exists(),
        "render_executed": True,
        "output_png": str(output_png),
        "aspect_ratio": aspect_ratio,
        "canvas": f"{w}x{h}",
        "lines_rendered": len(lines),
        "words_preserved": len(words),
        "overflow_detected": overflow,
        "text_qa": text_qa,
    }
