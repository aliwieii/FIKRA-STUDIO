// FIKRA STUDIO V3.1.1 — Aspect-Ratio Aware Video Configuration & Presets
export const PRESETS = {
  VERTICAL_9_16: { width: 1080, height: 1920, fps: 30, tail: 1.0, aspect: '9:16' },
  LANDSCAPE_16_9: { width: 1920, height: 1080, fps: 30, tail: 1.0, aspect: '16:9' },
  SQUARE_1_1: { width: 1080, height: 1080, fps: 30, tail: 1.0, aspect: '1:1' },
} as const;

export type PresetKey = keyof typeof PRESETS;

export function getPresetByAspect(aspect: string = '9:16') {
  if (aspect === '16:9') return PRESETS.LANDSCAPE_16_9;
  if (aspect === '1:1') return PRESETS.SQUARE_1_1;
  return PRESETS.VERTICAL_9_16;
}

export const VIDEO = PRESETS.VERTICAL_9_16;
