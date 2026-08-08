/**
 * Doxa Logo Geometry Engine — 5-Mode Transformation Model
 *
 * Generates exact point & particle target positions for 5 distinct states:
 * MODE 1 — FORM: Canonical 3 nested offset rings
 * MODE 2 — DEFORM: Organic triangular wave shield envelope with internal striations
 * MODE 3 — TRANSFORM: Intertwined double-helix swirl vortex
 * MODE 4 — RETRIEVE: Information particle spiral galaxy / vortex stream
 * MODE 5 — REFORM: Restructuring particle-to-ring convergence
 */

export const NUM_POINTS_PER_RING = 120;
export const TOTAL_POINTS = NUM_POINTS_PER_RING * 3;

// Canonical ring parameters for Mode 1 (viewBox 0 0 100 100)
export const CANONICAL_RINGS = [
  { cx: 50, cy: 40, r: 32, strokeWidth: 3.6, color: '#a855f7' }, // Outer (Purple)
  { cx: 45, cy: 53, r: 22, strokeWidth: 3.4, color: '#818cf8' }, // Middle (Indigo)
  { cx: 42, cy: 64, r: 13, strokeWidth: 3.2, color: '#06b6d4' }, // Inner (Cyan)
];

/**
 * Generate 2D point targets for a given mode (1..5)
 * Returns array of objects: { x, y, ringIndex, angle, size, alpha }
 */
export function getPointsForMode(mode) {
  const points = [];

  for (let ringIdx = 0; ringIdx < 3; ringIdx++) {
    const ring = CANONICAL_RINGS[ringIdx];
    
    for (let i = 0; i < NUM_POINTS_PER_RING; i++) {
      const u = i / NUM_POINTS_PER_RING;
      const angle = u * Math.PI * 2;
      let x, y, size = 1.8, alpha = 0.9, glow = false;

      if (mode === 1) {
        // MODE 1 — FORM: Clean Canonical Rings
        x = ring.cx + ring.r * Math.cos(angle);
        y = ring.cy + ring.r * Math.sin(angle);
        size = 1.6 + ringIdx * 0.3;
        alpha = 0.95;
      } 
      else if (mode === 2) {
        // MODE 2 — DEFORM: Organic Rounded Triangular Shield Wave (Ref Image Mode 2)
        // Top vertex at -pi/2, bottom right at +pi/6, bottom left at +5pi/6
        const triRadius = (ring.r * 1.1) * (1 + 0.32 * Math.cos(3 * angle - Math.PI / 2) + 0.08 * Math.sin(6 * angle));
        const centerOffsetY = ringIdx === 0 ? 46 : ringIdx === 1 ? 52 : 60;
        const centerOffsetX = 50 + (ringIdx - 1) * 3;
        
        x = centerOffsetX + triRadius * Math.cos(angle);
        y = centerOffsetY + triRadius * Math.sin(angle);

        // Internal wave line striations across lower interior
        if (i % 6 === 0) {
          x += Math.sin(angle * 12) * 3.5;
          y += Math.cos(angle * 8) * 2.5;
        }
        size = 1.5 + Math.abs(Math.sin(angle * 3)) * 1.2;
        alpha = 0.9;
      } 
      else if (mode === 3) {
        // MODE 3 — TRANSFORM: Intertwined Swirl Vortex (Ref Image Mode 3)
        const swirlAngle = angle + (ringIdx * Math.PI * 0.65);
        const radiusMod = ring.r * (1 + 0.35 * Math.sin(2 * angle + ringIdx));
        
        x = 50 + radiusMod * Math.cos(swirlAngle + 0.4 * Math.sin(3 * angle));
        y = 50 + radiusMod * Math.sin(swirlAngle + 0.4 * Math.cos(3 * angle));

        // Adding overlapping swirl crest details
        if (i % 4 === 0) {
          x += Math.cos(swirlAngle * 4) * 4;
          y += Math.sin(swirlAngle * 4) * 4;
        }
        size = 1.8 + Math.sin(angle * 4) * 0.8;
        alpha = 0.95;
      } 
      else if (mode === 4) {
        // MODE 4 — RETRIEVE: Particle Spiral Galaxy / Information Stream (Ref Image Mode 4)
        // 6 spiraling arms collapsing inward with dynamic particle cloud
        const armOffset = (ringIdx * 2 + (i % 2)) * (Math.PI / 3);
        const spiralNorm = ((i * 7) % NUM_POINTS_PER_RING) / NUM_POINTS_PER_RING;
        const radius = 6 + spiralNorm * 38;
        const spiralAngle = angle * 2.5 + armOffset + (1 - spiralNorm) * 3.5;
        
        // Jitter for particle vortex turbulence
        const jitterX = (Math.sin(i * 99.3) - 0.5) * 4.5;
        const jitterY = (Math.cos(i * 47.7) - 0.5) * 4.5;

        x = 50 + radius * Math.cos(spiralAngle) + jitterX;
        y = 50 + radius * Math.sin(spiralAngle) + jitterY;
        size = 1.0 + Math.random() * 2.2;
        alpha = 0.6 + Math.random() * 0.4;
        glow = true;
      } 
      else if (mode === 5) {
        // MODE 5 — REFORM: Restructuring Particle-to-Path Convergence (Ref Image Mode 5)
        // High density snap back toward canonical rings with cyan/violet pulse
        const targetX = ring.cx + ring.r * Math.cos(angle);
        const targetY = ring.cy + ring.r * Math.sin(angle);
        
        // Slightly expanded pre-snap positions
        x = targetX + Math.sin(angle * 8) * 1.5;
        y = targetY + Math.cos(angle * 8) * 1.5;
        size = 2.0;
        alpha = 1.0;
        glow = true;
      }

      points.push({
        x,
        y,
        ringIndex: ringIdx,
        angle,
        size,
        alpha,
        glow,
        color: ring.color,
      });
    }
  }

  return points;
}
