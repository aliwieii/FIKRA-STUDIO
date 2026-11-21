// FIKRA STUDIO V3.0 — Zero-Truncation Rolling Arabic Caption Overlay
// Fixes ISS-002:
//   1. Replaces fixed-prefix slicing with time-synced `paginateWords()` so ZERO words are dropped.
//   2. Adds `sceneOffsetSec` so global timeline sync remains exact inside `<Sequence from={...}>`.
import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { TIMING, Word, toSec } from '../timing';
import { FIKRA_COLORS, FIKRA_FONTS, SAFE_ZONE_9_16, rtlStyle } from '../utils/rtl';

export interface ArabicCaptionOverlayProps {
  mode?: 'narrative' | 'quran';
  maxWordsPerLine?: number;
  sceneOffsetSec?: number;
}

/** Split words into non-overlapping pages without ever dropping any word. */
export function paginateWords(words: Word[], maxWordsPerLine = 6): Word[][] {
  const size = Math.max(1, maxWordsPerLine);
  const pages: Word[][] = [];
  for (let i = 0; i < words.length; i += size) {
    pages.push(words.slice(i, i + size));
  }
  return pages;
}

export function selectActivePage(words: Word[], globalSec: number, maxWordsPerLine = 6): Word[] {
  const pages = paginateWords(words, maxWordsPerLine);
  if (pages.length === 0) return [];
  for (const page of pages) {
    const pageEnd = page[page.length - 1]?.end ?? 0;
    if (globalSec <= pageEnd + 0.05) return page;
  }
  return pages[pages.length - 1];
}

export const ArabicCaptionOverlay: React.FC<ArabicCaptionOverlayProps> = ({
  mode = 'narrative',
  maxWordsPerLine = 6,
  sceneOffsetSec = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const globalSec = sceneOffsetSec + toSec(frame);

  const activeLine = TIMING.lines.find((l) => globalSec >= l.start && globalSec <= l.end + 0.15);
  if (!activeLine) return null;

  const visibleWords = selectActivePage(activeLine.words, globalSec, maxWordsPerLine);
  const pageStartSec = visibleWords[0]?.start ?? activeLine.start;

  const isQuran = mode === 'quran';
  const enterProgress = spring({
    frame: Math.max(0, Math.round((globalSec - pageStartSec) * fps)),
    fps,
    config: { damping: 18, stiffness: 160 },
  });

  const translateY = interpolate(enterProgress, [0, 1], [16, 0]);
  const opacity = interpolate(enterProgress, [0, 1], [0, 1]);

  return (
    <div
      style={{
        position: 'absolute',
        left: SAFE_ZONE_9_16.left,
        right: SAFE_ZONE_9_16.right,
        bottom: SAFE_ZONE_9_16.bottom,
        display: 'flex',
        justifyContent: 'center',
        pointerEvents: 'none',
        transform: `translateY(${translateY}px)`,
        opacity,
      }}
    >
      <div
        style={{
          ...rtlStyle(isQuran ? FIKRA_FONTS.quran : FIKRA_FONTS.display),
          background: 'rgba(6, 11, 20, 0.82)',
          border: `1.5px solid ${isQuran ? FIKRA_COLORS.quranGold : 'rgba(148, 163, 184, 0.28)'}`,
          borderRadius: 20,
          padding: '18px 28px',
          maxWidth: '100%',
          boxShadow: isQuran
            ? `0 12px 36px ${FIKRA_COLORS.quranGoldGlow}`
            : '0 12px 30px rgba(0, 0, 0, 0.5)',
          fontSize: isQuran ? 48 : 42,
          fontWeight: isQuran ? 700 : 800,
          lineHeight: 1.48,
          color: isQuran ? FIKRA_COLORS.quranGold : FIKRA_COLORS.narrativeWhite,
        }}
      >
        {visibleWords.map((w, idx) => {
          const isSpoken = globalSec >= w.start;
          const isCurrent = globalSec >= w.start && globalSec <= w.end;
          return (
            <span
              key={`${w.w}-${w.start}-${idx}`}
              style={{
                display: 'inline-block',
                marginInline: 6,
                opacity: isSpoken ? 1 : 0.45,
                color: isCurrent
                  ? isQuran
                    ? '#FDE68A'
                    : FIKRA_COLORS.accentCyan
                  : isQuran
                  ? FIKRA_COLORS.quranGold
                  : FIKRA_COLORS.narrativeWhite,
                transform: isCurrent ? 'scale(1.06)' : 'scale(1)',
              }}
            >
              {w.w}
            </span>
          );
        })}
      </div>
    </div>
  );
};
