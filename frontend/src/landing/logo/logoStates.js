/**
 * Doxa Logo Motion System — 5-State Micro-Interaction Model
 *
 * STATE 1 — FORM: Canonical resting state (balanced, stable, subtle glow)
 * STATE 2 — DEFORM: Independent ring shift (translation, scaling, rotation, timing offsets)
 * STATE 3 — TRANSFORM: Dynamic expansion & offset configuration
 * STATE 4 — REFORM: System self-reorganization returning toward baseline
 * STATE 5 — FINAL FORM: Snap alignment with peak glow pulse before settling back to FORM
 */

export const LOGO_STATES = {
  FORM: 'FORM',
  DEFORM: 'DEFORM',
  TRANSFORM: 'TRANSFORM',
  REFORM: 'REFORM',
  FINAL_FORM: 'FINAL_FORM',
};

// Timing parameters (in seconds)
export const MOTION_TIMINGS = {
  totalDuration: 1.35,
  times: [0, 0.22, 0.52, 0.78, 0.92, 1.0], // Normalized timeline steps
};

// Outer Ring Keyframes (cx=50, cy=40, r=32, strokeWidth=3.6)
export const OUTER_RING_KEYFRAMES = {
  x: [0, -2.5, 3.5, 0.8, 0, 0],
  y: [0, -2.0, -3.8, -0.8, 0, 0],
  scale: [1, 1.03, 1.07, 1.02, 1.0, 1.0],
  rotate: [0, 6, -14, -3, 0, 0],
  strokeWidth: [3.6, 3.8, 4.1, 3.7, 3.6, 3.6],
  opacity: [0.95, 1, 1, 0.95, 1, 0.95],
};

// Middle Ring Keyframes (cx=45, cy=53, r=22, strokeWidth=3.4)
export const MIDDLE_RING_KEYFRAMES = {
  x: [0, 3.2, -4.5, -1.0, 0, 0],
  y: [0, -1.5, 3.2, 1.0, 0, 0],
  scale: [1, 0.95, 1.05, 0.98, 1.0, 1.0],
  rotate: [0, -10, 18, 4, 0, 0],
  strokeWidth: [3.4, 3.6, 3.9, 3.5, 3.4, 3.4],
  opacity: [0.9, 0.85, 1, 0.9, 1, 0.9],
};

// Inner Ring Keyframes (cx=42, cy=64, r=13, strokeWidth=3.2)
export const INNER_RING_KEYFRAMES = {
  x: [0, -1.8, 4.2, 0.9, 0, 0],
  y: [0, 2.8, -3.2, -0.9, 0, 0],
  scale: [1, 1.06, 0.91, 1.01, 1.0, 1.0],
  rotate: [0, 14, -22, -5, 0, 0],
  strokeWidth: [3.2, 3.5, 3.8, 3.3, 3.2, 3.2],
  opacity: [1, 1, 0.95, 1, 1, 1],
};

// Glow filter keyframes across states
export const GLOW_KEYFRAMES = {
  filter: [
    'drop-shadow(0 0 3px rgba(168, 85, 247, 0.25))',
    'drop-shadow(0 0 6px rgba(168, 85, 247, 0.45)) drop-shadow(0 0 10px rgba(6, 182, 212, 0.3))',
    'drop-shadow(0 0 10px rgba(6, 182, 212, 0.6)) drop-shadow(0 0 16px rgba(168, 85, 247, 0.5))',
    'drop-shadow(0 0 7px rgba(168, 85, 247, 0.4)) drop-shadow(0 0 12px rgba(6, 182, 212, 0.4))',
    'drop-shadow(0 0 12px rgba(6, 182, 212, 0.7)) drop-shadow(0 0 18px rgba(168, 85, 247, 0.6))',
    'drop-shadow(0 0 3px rgba(168, 85, 247, 0.25))',
  ],
};
