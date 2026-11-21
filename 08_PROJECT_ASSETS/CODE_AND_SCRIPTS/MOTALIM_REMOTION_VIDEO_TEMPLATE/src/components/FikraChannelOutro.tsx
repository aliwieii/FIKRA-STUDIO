// FIKRA STUDIO V2.0 — Channel Closing Identity Card (فِكْرَة)
import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { FIKRA_COLORS, FIKRA_FONTS, rtlStyle } from '../utils/rtl';

export const FikraChannelOutro: React.FC<{ tagline?: string }> = ({
  tagline = 'تأمل في الفكرة... قبل أن تمرّ',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 14, stiffness: 120 } });
  const subOpacity = interpolate(frame, [12, 28], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% 42%, #132540 0%, ${FIKRA_COLORS.obsidianBg} 75%)`,
        alignItems: 'center',
        justifyContent: 'center',
        gap: 24,
      }}
    >
      <div
        style={{
          ...rtlStyle(FIKRA_FONTS.display),
          fontSize: 112,
          fontWeight: 900,
          color: FIKRA_COLORS.quranGold,
          transform: `scale(${scale})`,
          textShadow: `0 0 42px ${FIKRA_COLORS.quranGoldGlow}`,
        }}
      >
        فِكْرَة
      </div>
      <div
        style={{
          ...rtlStyle(FIKRA_FONTS.body),
          fontSize: 38,
          fontWeight: 600,
          color: FIKRA_COLORS.narrativeWhite,
          opacity: subOpacity,
        }}
      >
        {tagline}
      </div>
    </AbsoluteFill>
  );
};
