// FIKRA STUDIO V2.0 — Video Configuration & Presets
// Backwards-compatible `VIDEO` export + vertical 9:16 preset for Shorts/TikTok/Reels.
export const PRESETS = {
  VERTICAL_9_16: { width: 1080, height: 1920, fps: 30, tail: 1.0 },
  LANDSCAPE_16_9: { width: 1920, height: 1080, fps: 30, tail: 1.0 },
  SQUARE_1_1: { width: 1080, height: 1080, fps: 30, tail: 1.0 },
} as const;

export const VIDEO = PRESETS.VERTICAL_9_16;
