/**
 * Doxa Logo Motion System — 5-Mode State Machine & Timing Definition
 *
 * MODE 1 — FORM: Canonical 3-ring baseline (Resting)
 * MODE 2 — DEFORM: Organic triangular wave shield envelope
 * MODE 3 — TRANSFORM: Intertwined double-helix swirl vortex
 * MODE 4 — RETRIEVE: Information particle spiral galaxy
 * MODE 5 — REFORM: Restructuring particle-to-ring convergence
 */

export const MODES = {
  FORM: 1,
  DEFORM: 2,
  TRANSFORM: 3,
  RETRIEVE: 4,
  REFORM: 5,
};

export const MODE_NAMES = {
  1: 'FORM',
  2: 'DEFORM',
  3: 'TRANSFORM',
  4: 'RETRIEVE',
  5: 'REFORM',
};

// Durations for each phase in milliseconds
export const TIMINGS = {
  DEFORM_DURATION: 350,
  TRANSFORM_DURATION: 450,
  RETRIEVE_DURATION: 500,
  REFORM_DURATION: 500,
  FINAL_REST_DURATION: 400,
  TOTAL_ANIMATION_TIME: 2200, // ~2.2 seconds
};

// Mode timeline breakpoints (normalized 0 to 1)
export const TIMELINE_BREAKPOINTS = [
  { modeFrom: 1, modeTo: 2, start: 0, end: 0.16 },       // 0 - 350ms
  { modeFrom: 2, modeTo: 3, start: 0.16, end: 0.36 },    // 350 - 800ms
  { modeFrom: 3, modeTo: 4, start: 0.36, end: 0.59 },    // 800 - 1300ms
  { modeFrom: 4, modeTo: 5, start: 0.59, end: 0.82 },    // 1300 - 1800ms
  { modeFrom: 5, modeTo: 1, start: 0.82, end: 1.0 },     // 1800 - 2200ms
];

// Color palette mapping
export const PALETTE = {
  purple: '#a855f7',
  indigo: '#818cf8',
  cyan: '#06b6d4',
  pink: '#ec4899',
  glowPurple: 'rgba(168, 85, 247, 0.65)',
  glowCyan: 'rgba(6, 182, 212, 0.75)',
};
