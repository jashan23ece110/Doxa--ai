import React, { useRef, useState, useEffect, useCallback } from 'react';
import { useReducedMotion } from 'framer-motion';
import { getPointsForMode, CANONICAL_RINGS } from './logoGeometry';
import { TIMINGS, TIMELINE_BREAKPOINTS, PALETTE } from './logoStates';

/**
 * React Error Boundary for Hero Logo Overlay
 * Guarantees that even if an unexpected runtime error occurs inside the canvas,
 * the entire application continues rendering safely without a blank screen.
 */
export class HeroLogoErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.warn('HeroLogoMotion captured an isolated runtime exception:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || null;
    }
    return this.props.children;
  }
}

/**
 * HeroLogoMotion — Cinematic 5-Mode Intelligence Cycle Overlay for Hero Section
 *
 * Renders an independent 2D Canvas overlay above HeroStarfield.jsx performing:
 * MODE 1 — FORM (Canonical baseline)
 * MODE 2 — DEFORM (Organic triangular wave shield)
 * MODE 3 — TRANSFORM (Intertwined swirl vortex)
 * MODE 4 — RETRIEVE (Particle spiral galaxy stream)
 * MODE 5 — REFORM (Particle-to-ring snap-back)
 */
export default function HeroLogoMotion({
  size = 140,
  className = '',
  color = 'currentColor',
  ariaLabel = 'Doxa Hero Intelligence Logo',
  style = {},
  ...props
}) {
  const canvasRef = useRef(null);
  const animFrameRef = useRef(null);
  const startTimeRef = useRef(null);
  const shouldReduceMotion = useReducedMotion();
  const [isAnimating, setIsAnimating] = useState(false);

  // Pre-calculated target point sets for Modes 1..5
  const modePoints = useRef({
    1: getPointsForMode(1),
    2: getPointsForMode(2),
    3: getPointsForMode(3),
    4: getPointsForMode(4),
    5: getPointsForMode(5),
  }).current;

  // 60 FPS HTML5 Canvas Morphing Engine
  const renderFrame = useCallback((timestamp) => {
    if (!startTimeRef.current) startTimeRef.current = timestamp;
    const elapsed = timestamp - startTimeRef.current;
    const progress = Math.min(elapsed / TIMINGS.TOTAL_ANIMATION_TIME, 1);

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const scaleFactor = canvas.width / 100;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Active timeline breakpoint
    let bp = TIMELINE_BREAKPOINTS[0];
    for (let i = 0; i < TIMELINE_BREAKPOINTS.length; i++) {
      if (progress >= TIMELINE_BREAKPOINTS[i].start && progress <= TIMELINE_BREAKPOINTS[i].end) {
        bp = TIMELINE_BREAKPOINTS[i];
        break;
      }
    }

    const localProgress = (progress - bp.start) / (bp.end - bp.start);
    const ease = localProgress < 0.5 
      ? 4 * localProgress * localProgress * localProgress 
      : 1 - Math.pow(-2 * localProgress + 2, 3) / 2;

    const fromSet = modePoints[bp.modeFrom];
    const toSet = modePoints[bp.modeTo];

    // Radial background glow aura during transform & retrieve modes
    if (progress > 0.25 && progress < 0.95) {
      const glowGrad = ctx.createRadialGradient(
        50 * scaleFactor, 50 * scaleFactor, 4 * scaleFactor,
        50 * scaleFactor, 50 * scaleFactor, 46 * scaleFactor
      );
      const intensity = Math.sin((progress - 0.25) / 0.7 * Math.PI) * 0.55;
      glowGrad.addColorStop(0, `rgba(168, 85, 247, ${intensity})`);
      glowGrad.addColorStop(0.5, `rgba(6, 182, 212, ${intensity * 0.75})`);
      glowGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = glowGrad;
      ctx.beginPath();
      ctx.arc(50 * scaleFactor, 50 * scaleFactor, 46 * scaleFactor, 0, Math.PI * 2);
      ctx.fill();
    }

    // Point position & size interpolation
    const interpolated = [];
    for (let i = 0; i < fromSet.length; i++) {
      const p1 = fromSet[i];
      const p2 = toSet[i];

      const x = (p1.x + (p2.x - p1.x) * ease) * scaleFactor;
      const y = (p1.y + (p2.y - p1.y) * ease) * scaleFactor;
      const pSize = (p1.size + (p2.size - p1.size) * ease) * scaleFactor * 0.9;
      const alpha = p1.alpha + (p2.alpha - p1.alpha) * ease;
      const ringIdx = p1.ringIndex;

      interpolated.push({ x, y, size: pSize, alpha, ringIdx, color: p1.color });
    }

    // Path stroke rendering for connected geometry modes
    if (bp.modeFrom !== 4 && bp.modeTo !== 4) {
      for (let r = 0; r < 3; r++) {
        const ringPoints = interpolated.filter(p => p.ringIdx === r);
        if (ringPoints.length > 2) {
          ctx.beginPath();
          ctx.moveTo(ringPoints[0].x, ringPoints[0].y);
          for (let k = 1; k < ringPoints.length; k++) {
            ctx.lineTo(ringPoints[k].x, ringPoints[k].y);
          }
          ctx.closePath();
          ctx.strokeStyle = ringPoints[0].color === '#a855f7' ? PALETTE.purple :
                            ringPoints[0].color === '#818cf8' ? PALETTE.indigo : PALETTE.cyan;
          ctx.lineWidth = (4.0 - r * 0.3) * (scaleFactor / 3.6);
          ctx.shadowColor = PALETTE.glowPurple;
          ctx.shadowBlur = 8 * scaleFactor;
          ctx.stroke();
        }
      }
    }

    // Particle rendering
    for (let i = 0; i < interpolated.length; i++) {
      const pt = interpolated[i];
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, Math.max(pt.size, 1), 0, Math.PI * 2);
      ctx.fillStyle = pt.color;
      ctx.globalAlpha = Math.min(Math.max(pt.alpha, 0.2), 1);
      ctx.shadowColor = pt.ringIdx === 2 ? PALETTE.cyan : PALETTE.purple;
      ctx.shadowBlur = 5 * scaleFactor;
      ctx.fill();
      ctx.globalAlpha = 1.0;
    }

    if (progress < 1) {
      animFrameRef.current = requestAnimationFrame(renderFrame);
    } else {
      setIsAnimating(false);
      startTimeRef.current = null;
    }
  }, [modePoints]);

  const triggerAnimation = useCallback(() => {
    if (shouldReduceMotion || isAnimating) return;
    setIsAnimating(true);
    startTimeRef.current = null;
    animFrameRef.current = requestAnimationFrame(renderFrame);
  }, [shouldReduceMotion, isAnimating, renderFrame]);

  useEffect(() => {
    return () => {
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    };
  }, []);

  return (
    <div
      className={`relative inline-flex items-center justify-center cursor-pointer select-none shrink-0 ${className}`}
      style={{ width: size, height: size, ...style }}
      onMouseEnter={triggerAnimation}
      onClick={triggerAnimation}
      onTouchStart={triggerAnimation}
      role="img"
      aria-label={ariaLabel}
      {...props}
    >
      {/* 60 FPS Morphing Overlay Canvas */}
      <canvas
        ref={canvasRef}
        width={240}
        height={240}
        className={`absolute inset-0 w-full h-full transition-opacity duration-300 ${
          isAnimating ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
      />

      {/* Baseline Form Vector Logo (Resting State) */}
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={`w-full h-full transition-opacity duration-300 ${
          isAnimating ? 'opacity-0' : 'opacity-100'
        }`}
        style={{
          filter: 'drop-shadow(0 0 8px rgba(168, 85, 247, 0.45)) drop-shadow(0 0 16px rgba(6, 182, 212, 0.3))',
        }}
      >
        {CANONICAL_RINGS.map((ring, idx) => (
          <circle
            key={idx}
            cx={ring.cx}
            cy={ring.cy}
            r={ring.r}
            stroke={color === 'currentColor' ? ring.color : color}
            strokeWidth={ring.strokeWidth}
            strokeLinecap="round"
            className="transition-colors duration-300"
          />
        ))}
      </svg>
    </div>
  );
}
