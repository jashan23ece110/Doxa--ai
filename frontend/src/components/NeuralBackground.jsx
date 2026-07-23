import { useEffect, useRef } from 'react';

const PARTICLE_COUNT = 120;
const CONNECTION_DISTANCE = 120;
const MIN_SPEED = 0.1;
const MAX_SPEED = 0.3;
const LINE_WIDTH = 0.5;
const MIN_RADIUS = 1;
const MAX_RADIUS = 2;

function createParticles(width, height) {
  const particles = new Array(PARTICLE_COUNT);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = MIN_SPEED + Math.random() * (MAX_SPEED - MIN_SPEED);
    particles[i] = {
      x: Math.random() * width,
      y: Math.random() * height,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      r: MIN_RADIUS + Math.random() * (MAX_RADIUS - MIN_RADIUS),
    };
  }
  return particles;
}

export default function NeuralBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d', { alpha: true });
    let width = 0;
    let height = 0;
    let particles = [];
    let animId = 0;

    const resize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      const dpr = window.devicePixelRatio || 1;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // Re-scatter particles when viewport changes
      particles = createParticles(width, height);
    };

    const observer = new ResizeObserver(() => resize());
    observer.observe(document.documentElement);
    resize();

    const tick = () => {
      ctx.clearRect(0, 0, width, height);

      // Update positions & wrap
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0) p.x += width;
        else if (p.x > width) p.x -= width;
        if (p.y < 0) p.y += height;
        else if (p.y > height) p.y -= height;
      }

      // Draw connections
      const accentRgb = getComputedStyle(document.documentElement).getPropertyValue('--jarvis-accent-rgb').trim() || '220, 20, 60';
      ctx.strokeStyle = `rgba(${accentRgb}, 0.03)`;
      ctx.lineWidth = LINE_WIDTH;
      ctx.beginPath();
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        const a = particles[i];
        for (let j = i + 1; j < PARTICLE_COUNT; j++) {
          const b = particles[j];
          const dx = a.x - b.x;
          const dy = a.y - b.y;
          if (
            dx < CONNECTION_DISTANCE &&
            dx > -CONNECTION_DISTANCE &&
            dy < CONNECTION_DISTANCE &&
            dy > -CONNECTION_DISTANCE
          ) {
            const distSq = dx * dx + dy * dy;
            if (distSq < CONNECTION_DISTANCE * CONNECTION_DISTANCE) {
              ctx.moveTo(a.x, a.y);
              ctx.lineTo(b.x, b.y);
            }
          }
        }
      }
      ctx.stroke();

      // Draw particles
      ctx.fillStyle = `rgba(${accentRgb}, 0.06)`;
      ctx.beginPath();
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        const p = particles[i];
        ctx.moveTo(p.x + p.r, p.y);
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      }
      ctx.fill();

      animId = requestAnimationFrame(tick);
    };

    animId = requestAnimationFrame(tick);

    return () => {
      cancelAnimationFrame(animId);
      observer.disconnect();
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 0,
        opacity: 0.5,
        pointerEvents: 'none',
      }}
      aria-hidden="true"
    />
  );
}
