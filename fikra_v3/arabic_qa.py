"""Feature I: Arabic QA Engine — RTL, shaping, diacritics, BiDi, zero-drop caption pagination, SRT QA."""
from __future__ import annotations

import re
from typing import Any

ARABIC_RANGE = re.compile(r"[؀-ۿ]")
LATIN_RANGE = re.compile(r"[A-Za-z]")
DIACRITICS = re.compile(r"[ً-ٰٟ]")
ISOLATED_FORMS = re.compile(r"[ﹰ-﻿]")
BROKEN_SPACED_LETTERS = re.compile(r"(?:^|\s)([ء-ي]\s+){3,}[ء-ي](?:\s|$)")


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
        p_start = page[0].get("start", 0.0)
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
    if has_arabic and has_latin:
        # Check if raw unmatched punctuation sits at boundary without isolation
        if "⁦" not in text and "‏" not in text:
            mixed_bidi_warning = True

    words = re.findall(r"\S+", text)
    cps = round(len(text.replace("
", " ")) / duration_sec, 2) if duration_sec and duration_sec > 0 else None
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
    blocks = [b.strip() for b in re.split(r"?
\s*?
", srt_text.strip()) if b.strip()]
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
        body = "
".join(lines[2:])
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
