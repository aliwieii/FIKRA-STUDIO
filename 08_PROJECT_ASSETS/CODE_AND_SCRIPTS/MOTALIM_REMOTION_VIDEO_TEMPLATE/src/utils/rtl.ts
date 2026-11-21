// FIKRA STUDIO V2.0 — Arabic RTL Typography & Safe-Zone Utilities
// Grounded in FIKRA visual standards (gold for Quranic text, white for narrative, RTL shaping).

export const FIKRA_FONTS = {
  display: "'Cairo', 'Noto Kufi Arabic', 'Tajawal', sans-serif",
  body: "'Tajawal', 'Cairo', 'Noto Sans Arabic', sans-serif",
  quran: "'Amiri', 'Scheherazade New', serif",
} as const;

export const FIKRA_COLORS = {
  obsidianBg: '#060B14',
  navyCard: '#0F1B2E',
  narrativeWhite: '#F8FAFC',
  quranGold: '#F59E0B',
  quranGoldGlow: 'rgba(245, 158, 11, 0.35)',
  accentCyan: '#38BDF8',
  accentEmerald: '#10B981',
  mutedSlate: '#94A3B8',
} as const;

/** Safe zones for 1080x1920 vertical video (TikTok / YouTube Shorts / Reels). */
export const SAFE_ZONE_9_16 = {
  top: 220,
  bottom: 360,
  left: 72,
  right: 120,
} as const;

export function rtlStyle(fontFamily: string = FIKRA_FONTS.display): React.CSSProperties {
  return {
    direction: 'rtl',
    unicodeBidi: 'plaintext',
    fontFamily,
    textAlign: 'center',
  };
}
