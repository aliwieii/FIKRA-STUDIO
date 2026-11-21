// FIKRA STUDIO V2.0 — Frame-Driven Word-Synced Arabic Caption Overlay
// Follows remotion-best-practices: 100% driven by useCurrentFrame(), zero CSS transitions.
import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { TIMING, toSec } from '../timing';
import { FIKRA_COLORS, FIKRA_FONTS, SAFE_ZONE_9_16, rtlStyle } from '../utils/rtl';

export interface ArabicCaptionOverlayProps {
  mode?: 'narrative' | 'quran';
  maxWordsPerLine?: number;
}

export const ArabicCaptionOverlay: React.FC<ArabicCaptionOverlayProps> = ({
  mode = 'narrative',
  maxWordsPerLine = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = toSec(frame);

  const activeLine = TIMING.lines.find((l) => t >= l.start && t <= l.end + 0.15);
  if (!activeLine) return null;

  const isQuran = mode === 'quran';
  const enterProgress = spring({
    frame: Math.max(0, frame - Math.round(activeLine.start * fps)),
    fps,
    config: { damping: 18, stiffness: 160 },
  });

  const translateY = interpolate(enterProgress, [0, 1], [18, 0]);
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
          background: 'rgba(6, 11, 20, 0.78)',
          border: `1.5px solid ${isQuran ? FIKRA_COLORS.quranGold : 'rgba(148, 163, 184, 0.25)'}`,
          borderRadius: 20,
          padding: '18px 28px',
          maxWidth: '100%',
          boxShadow: isQuran
            ? `0 12px 36px ${FIKRA_COLORS.quranGoldGlow}`
            : '0 12px 30px rgba(0, 0, 0, 0.5)',
          fontSize: isQuran ? 48 : 42,
          fontWeight: isQuran ? 700 : 800,
          lineHeight: 1.45,
          color: isQuran ? FIKRA_COLORS.quranGold : FIKRA_COLORS.narrativeWhite,
        }}
      >
        {activeLine.words.slice(0, maxWordsPerLine).map((w, idx) => {
          const isSpoken = t >= w.start;
          const isCurrent = t >= w.start && t <= w.end;
          return (
            <span
              key={`${w.w}-${idx}`}
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
