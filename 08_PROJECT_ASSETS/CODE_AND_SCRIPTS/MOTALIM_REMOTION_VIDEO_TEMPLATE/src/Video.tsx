// FIKRA STUDIO V3.0 — Registered Scene Pipeline (Fixes ISS-004)
import React from 'react';
import { AbsoluteFill, Html5Audio, Sequence, staticFile } from 'remotion';
import { ArabicCaptionOverlay } from './components/ArabicCaptionOverlay';
import { FikraChannelOutro } from './components/FikraChannelOutro';
import { SceneTransition } from './components/SceneTransition';
import { SampleFikraHook } from './scenes/SampleFikraHook';
import { TIMING, toFrame } from './timing';

export type Scene = {
  id: string;
  from: number;
  to: number;
  C: React.FC<{ from: number }>;
};

const OutroScene: React.FC<{ from: number }> = () => <FikraChannelOutro />;

const totalDur = Math.max(6.0, TIMING.duration || 8.0);
const outroStart = Math.max(3.5, totalDur - 2.5);

export const SCENES: Scene[] = [
  { id: 'hook', from: 0, to: outroStart, C: SampleFikraHook },
  { id: 'outro', from: outroStart, to: totalDur, C: OutroScene },
];

export const Video: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#060B14' }}>
    {TIMING.audio ? <Html5Audio src={staticFile(TIMING.audio)} /> : null}
    {SCENES.map((s) => {
      const durFrames = Math.max(1, toFrame(s.to) - toFrame(s.from));
      return (
        <Sequence key={s.id} name={s.id} from={toFrame(s.from)} durationInFrames={durFrames} premountFor={30}>
          <SceneTransition durationInFrames={durFrames}>
            <s.C from={s.from} />
          </SceneTransition>
        </Sequence>
      );
    })}
    {/* Global timeline caption overlay prevents local-sequence offset drift */}
    <ArabicCaptionOverlay mode="narrative" maxWordsPerLine={6} sceneOffsetSec={0} />
  </AbsoluteFill>
);
