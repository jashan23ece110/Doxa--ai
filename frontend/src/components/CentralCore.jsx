import React, { useRef, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';

const CYAN = '#00d9ff';
const PARTICLE_COUNT = 300;
const CONNECTION_DISTANCE = 60;
const SPHERE_RADIUS_RATIO = 0.3; // proportion of min(width, height)

function createParticles(count) {
  const particles = [];
  const goldenAngle = Math.PI * (3 - Math.sqrt(5)); // ~2.39996 rad

  for (let i = 0; i < count; i++) {
    const y = 1 - (i / (count - 1)) * 2; // y goes from 1 to -1
    const radiusAtY = Math.sqrt(1 - y * y);
    const theta = goldenAngle * i;

    particles.push({
      // Unit sphere coordinates
      baseX: Math.cos(theta) * radiusAtY,
      baseY: y,
      baseZ: Math.sin(theta) * radiusAtY,
      // Drift offset for active state
      driftOffset: 0,
      driftTarget: 0,
      driftSpeed: 0.01 + Math.random() * 0.02,
      // Whether this particle drifts outward in active mode
      isDrifter: Math.random() < 0.15,
    });
  }
  return particles;
}

function CentralCore({ isActive = false, isThinking = false }) {
  const canvasRef = useRef(null);
  const animFrameRef = useRef(null);
  const particlesRef = useRef(createParticles(PARTICLE_COUNT));
  const angleRef = useRef(0);
  const glowPulseRef = useRef(0);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    const cx = width / 2;
    const cy = height / 2;
    const sphereRadius = Math.min(width, height) * SPHERE_RADIUS_RATIO;
    const focalLength = Math.min(width, height) * 0.8;

    // Determine state parameters
    let rotationSpeed, particleAlpha, glowIntensity, glowColor;
    if (isThinking) {
      rotationSpeed = 0.012;
      particleAlpha = 0.85;
      glowIntensity = 0.7;
      glowColor = 'rgba(200,240,255,';
    } else if (isActive) {
      rotationSpeed = 0.008;
      particleAlpha = 0.8;
      glowIntensity = 0.5;
      glowColor = 'rgba(0,217,255,';
    } else {
      rotationSpeed = 0.002;
      particleAlpha = 0.4;
      glowIntensity = 0.25;
      glowColor = 'rgba(0,217,255,';
    }

    // Update rotation angle
    angleRef.current += rotationSpeed;
    const angle = angleRef.current;
    const cosA = Math.cos(angle);
    const sinA = Math.sin(angle);

    // Glow pulse
    glowPulseRef.current += 0.03;
    const pulseValue =
      Math.sin(glowPulseRef.current) * 0.15 * (isActive ? 2 : 1) +
      glowIntensity;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // --- Draw radial glow behind sphere ---
    const glowRadius = sphereRadius * 2.2;
    const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, glowRadius);
    gradient.addColorStop(0, glowColor + (pulseValue * 0.6).toFixed(3) + ')');
    gradient.addColorStop(0.4, glowColor + (pulseValue * 0.2).toFixed(3) + ')');
    gradient.addColorStop(1, glowColor + '0)');
    ctx.fillStyle = gradient;
    ctx.fillRect(cx - glowRadius, cy - glowRadius, glowRadius * 2, glowRadius * 2);

    // --- Project particles ---
    const particles = particlesRef.current;
    const projected = [];

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];

      // Update drift
      if (isActive && p.isDrifter) {
        p.driftTarget = 0.3 + Math.random() * 0.1;
      } else if (isThinking) {
        p.driftTarget = -0.1;
      } else {
        p.driftTarget = 0;
      }
      p.driftOffset += (p.driftTarget - p.driftOffset) * p.driftSpeed;

      const scale = 1 + p.driftOffset;

      // Rotate around Y-axis
      const rx = p.baseX * cosA + p.baseZ * sinA;
      const ry = p.baseY;
      const rz = -p.baseX * sinA + p.baseZ * cosA;

      // Scale to sphere radius
      const wx = rx * sphereRadius * scale;
      const wy = ry * sphereRadius * scale;
      const wz = rz * sphereRadius * scale;

      // Perspective projection
      const depth = wz + focalLength;
      const projScale = focalLength / depth;
      const sx = cx + wx * projScale;
      const sy = cy + wy * projScale;

      // Depth-based alpha and size
      const depthNorm = (rz + 1) / 2; // 0 = far, 1 = near
      const alpha = particleAlpha * (0.3 + depthNorm * 0.7);
      const radius = 2 + depthNorm * 2; // 2-4px

      projected.push({ sx, sy, alpha, radius, depthNorm, wz });
    }

    // Sort by depth (draw far particles first)
    projected.sort((a, b) => a.wz - b.wz);

    // --- Draw connecting lines ---
    ctx.lineWidth = 0.5;
    for (let i = 0; i < projected.length; i++) {
      for (let j = i + 1; j < projected.length; j++) {
        const dx = projected[i].sx - projected[j].sx;
        const dy = projected[i].sy - projected[j].sy;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONNECTION_DISTANCE) {
          const lineAlpha =
            (1 - dist / CONNECTION_DISTANCE) *
            0.15 *
            Math.min(projected[i].alpha, projected[j].alpha);
          ctx.strokeStyle = `rgba(0,217,255,${lineAlpha.toFixed(3)})`;
          ctx.beginPath();
          ctx.moveTo(projected[i].sx, projected[i].sy);
          ctx.lineTo(projected[j].sx, projected[j].sy);
          ctx.stroke();
        }
      }
    }

    // --- Draw particles ---
    for (let i = 0; i < projected.length; i++) {
      const { sx, sy, alpha, radius } = projected[i];
      ctx.beginPath();
      ctx.arc(sx, sy, radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0,217,255,${alpha.toFixed(3)})`;
      ctx.fill();

      // Subtle glow per particle
      if (alpha > 0.5) {
        ctx.beginPath();
        ctx.arc(sx, sy, radius * 2.5, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0,217,255,${(alpha * 0.15).toFixed(3)})`;
        ctx.fill();
      }
    }

    animFrameRef.current = requestAnimationFrame(draw);
  }, [isActive, isThinking]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const parent = canvas.parentElement;

    const resize = () => {
      const dpr = window.devicePixelRatio || 1;
      const rect = parent.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      canvas.style.width = `${rect.width}px`;
      canvas.style.height = `${rect.height}px`;
      const ctx = canvas.getContext('2d');
      if (ctx) ctx.scale(dpr, dpr);
      // Reset canvas dimensions used for drawing to CSS pixels
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
    };

    const observer = new ResizeObserver(resize);
    observer.observe(parent);
    resize();

    // Start animation loop
    animFrameRef.current = requestAnimationFrame(draw);

    return () => {
      observer.disconnect();
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [draw]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8, ease: 'easeOut' }}
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
      }}
    >
      <canvas
        ref={canvasRef}
        style={{
          display: 'block',
          width: '100%',
          height: '100%',
          background: 'transparent',
        }}
      />
    </motion.div>
  );
}

export default CentralCore;
