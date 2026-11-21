// FIKRA STUDIO V3.0 — Frame-Driven Scene Transition Wrapper
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export const SceneTransition: React.FC<{
  durationInFrames: number;
  fadeFrames?: number;
  children: React.ReactNode;
}> = ({ durationInFrames, fadeFrames = 10, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fade = Math.min(fadeFrames, Math.floor(durationInFrames / 3), Math.round(fps * 0.4));
  const fadeIn = fade > 0 ? interpolate(frame, [0, fade], [0, 1], { extrapolateRight: 'clamp' }) : 1;
  const fadeOut =
    fade > 0
      ? interpolate(frame, [Math.max(0, durationInFrames - fade), durationInFrames], [1, 0], {
          extrapolateLeft: 'clamp',
        })
      : 1;

  return <AbsoluteFill style={{ opacity: Math.min(fadeIn, fadeOut) }}>{children}</AbsoluteFill>;
};
