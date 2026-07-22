/* ═══════════════════════════════════════════
   DOXA — Centralized Theme Configuration
   ═══════════════════════════════════════════
   All colors defined here so future palette
   changes only require editing this file.
   ═══════════════════════════════════════════ */

export const THEME = {
  // Backgrounds
  bg: '#0a0a0a',
  surface: '#141414',
  panel: 'rgba(10, 10, 10, 0.85)',

  // Primary accent — electric yellow/amber
  accent: '#dc143c',
  accentHover: '#ff4500',
  accentDim: '#8b0000',
  accentRgb: '255,214,10',      // for rgba() template literals
  accentDimRgb: '184,134,11',   // muted gold for rgba()

  // Glow presets
  accentGlow: 'rgba(220, 20, 60,0.4)',
  accentGlowSoft: 'rgba(220, 20, 60,0.15)',
  accentGlowSubtle: 'rgba(220, 20, 60,0.06)',

  // Text
  text: '#e0d6c2',
  textDim: '#7a7060',
  textBright: '#fff8e1',

  // Borders
  border: 'rgba(220, 20, 60,0.15)',
  borderBright: 'rgba(220, 20, 60,0.35)',

  // Semantic colors (unchanged)
  green: '#00ff88',
  red: '#ff3366',
  amber: '#ffaa00',

  // Three.js specific
  particleColor: 0xdc143c,      // hex int for THREE.Color
  glowColor: 0xdc143c,
  thinkingGlowColor: 0xfff8e1,  // warm white-yellow for thinking state
};

export default THEME;
