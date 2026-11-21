// FIKRA STUDIO V2.0 — Deterministic Frame-Driven Audio Spectrum Visualizer
// Zero Math.random(); 100% seekable and reproducible across Remotion renders.
import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { FIKRA_COLORS } from '../utils/rtl';

export interface AudioSpectrumBarProps {
  bars?: number;
  color?: string;
  height?: number;
}

export const AudioSpectrumBar: React.FC<AudioSpectrumBarProps> = ({
  bars = 24,
  color = FIKRA_COLORS.quranGold,
  height = 72,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 6,
        height,
      }}
    >
      {Array.from({ length: bars }).map((_, i) => {
        const phase = i * 0.45;
        const wave =
          0.35 +
          0.35 * Math.sin(t * 5.2 + phase) +
          0.2 * Math.cos(t * 8.7 - phase * 1.3);
        const barH = Math.max(10, Math.round(wave * height));
        return (
          <div
            key={i}
            style={{
              width: 6,
              height: barH,
              borderRadius: 999,
              backgroundColor: color,
              opacity: 0.75 + 0.25 * wave,
            }}
          />
        );
      })}
    </div>
  );
};
