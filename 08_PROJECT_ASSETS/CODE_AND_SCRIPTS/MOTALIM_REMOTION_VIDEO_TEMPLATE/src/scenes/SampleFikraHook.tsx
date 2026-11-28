// FIKRA STUDIO V2.0 — Sample 9:16 Vertical Scene (Frame-Driven Push-In + RTL Kinetic Title)
import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { AudioSpectrumBar } from '../components/AudioSpectrumBar';
import { FIKRA_COLORS, FIKRA_FONTS, SAFE_ZONE_9_16, rtlStyle } from '../utils/rtl';

export const SampleFikraHook: React.FC<{ from: number; headline?: string }> = ({
  headline = 'لحظة واحدة قد تغيّر نظرتك للكون',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bgScale = interpolate(frame, [0, 150], [1.0, 1.08], { extrapolateRight: 'clamp' });
  const titleSpring = spring({ frame, fps, config: { damping: 16, stiffness: 140 } });

  return (
    <AbsoluteFill style={{ backgroundColor: FIKRA_COLORS.obsidianBg, overflow: 'hidden' }}>
      <AbsoluteFill
        style={{
          background: 'radial-gradient(circle at 50% 30%, #17335C 0%, #060B14 72%)',
          transform: `scale(${bgScale})`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          top: SAFE_ZONE_9_16.top + 80,
          left: SAFE_ZONE_9_16.left,
          right: SAFE_ZONE_9_16.right,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 32,
        }}
      >
        <div
          style={{
            ...rtlStyle(FIKRA_FONTS.display),
            fontSize: 64,
            fontWeight: 900,
            color: FIKRA_COLORS.narrativeWhite,
            lineHeight: 1.3,
            transform: `translateY(${interpolate(titleSpring, [0, 1], [30, 0])}px)`,
            opacity: titleSpring,
          }}
        >
          {headline}
        </div>
        <AudioSpectrumBar bars={20} color={FIKRA_COLORS.accentCyan} height={56} />
      </div>
    </AbsoluteFill>
  );
};
