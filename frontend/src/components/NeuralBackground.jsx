import { useEffect, useRef } from 'react';

const CONNECTION_DISTANCE = 110;
const MIN_SPEED = 0.08;
const MAX_SPEED = 0.25;
const LINE_WIDTH = 0.45;
const MIN_RADIUS = 0.8;
const MAX_RADIUS = 1.8;

function createParticles(count, width, height) {
  const particles = new Array(count);
  for (let i = 0; i < count; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = MIN_SPEED + Math.random() * (MAX_SPEED - MIN_SPEED);
    particles[i] = {
      x: Math.random() * width,
      y: Math.random() * height,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      r: MIN_RADIUS + Math.random() * (MAX_RADIUS - MIN_RADIUS),
      depth: 0.15 + Math.random() * 0.85 // 3D depth parallax scale
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
    
    // Mouse coords for parallax
    let mouseX = 0;
    let mouseY = 0;
    let targetMouseX = 0;
    let targetMouseY = 0;

    const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;
    const particleCount = isMobile ? 35 : 100;

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
      particles = createParticles(particleCount, width, height);
    };

    const handleMouseMove = (e) => {
      // Offset from center: [-0.5, 0.5]
      targetMouseX = (e.clientX / window.innerWidth) - 0.5;
      targetMouseY = (e.clientY / window.innerHeight) - 0.5;
    };

    window.addEventListener('mousemove', handleMouseMove);

    const observer = new ResizeObserver(() => resize());
    observer.observe(document.documentElement);
    resize();

    const tick = () => {
      ctx.clearRect(0, 0, width, height);

      // Smooth mouse interpolation (easing)
      mouseX += (targetMouseX - mouseX) * 0.08;
      mouseY += (targetMouseY - mouseY) * 0.08;

      // Update positions & wrap
      for (let i = 0; i < particleCount; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < -20) p.x += width + 40;
        else if (p.x > width + 20) p.x -= width + 40;
        if (p.y < -20) p.y += height + 40;
        else if (p.y > height + 20) p.y -= height + 40;
      }

      const accentRgb = getComputedStyle(document.documentElement).getPropertyValue('--jarvis-accent-rgb').trim() || '220, 20, 60';

      // Draw connections with parallax offsets
      ctx.strokeStyle = `rgba(${accentRgb}, 0.025)`;
      ctx.lineWidth = LINE_WIDTH;
      ctx.beginPath();
      for (let i = 0; i < particleCount; i++) {
        const a = particles[i];
        const ax = a.x + mouseX * 45 * a.depth;
        const ay = a.y + mouseY * 45 * a.depth;

        for (let j = i + 1; j < particleCount; j++) {
          const b = particles[j];
          const bx = b.x + mouseX * 45 * b.depth;
          const by = b.y + mouseY * 45 * b.depth;

          const dx = ax - bx;
          const by_ay = ay - by;
          if (
            dx < CONNECTION_DISTANCE &&
            dx > -CONNECTION_DISTANCE &&
            by_ay < CONNECTION_DISTANCE &&
            by_ay > -CONNECTION_DISTANCE
          ) {
            const distSq = dx * dx + by_ay * by_ay;
            if (distSq < CONNECTION_DISTANCE * CONNECTION_DISTANCE) {
              ctx.moveTo(ax, ay);
              ctx.lineTo(bx, by);
            }
          }
        }
      }
      ctx.stroke();

      // Draw particles with parallax offsets
      ctx.fillStyle = `rgba(${accentRgb}, 0.05)`;
      ctx.beginPath();
      for (let i = 0; i < particleCount; i++) {
        const p = particles[i];
        const px = p.x + mouseX * 45 * p.depth;
        const py = p.y + mouseY * 45 * p.depth;
        ctx.moveTo(px + p.r, py);
        ctx.arc(px, py, p.r, 0, Math.PI * 2);
      }
      ctx.fill();

      animId = requestAnimationFrame(tick);
    };

    animId = requestAnimationFrame(tick);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('mousemove', handleMouseMove);
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
        opacity: 0.7,
        pointerEvents: 'none',
      }}
      aria-hidden="true"
    />
  );
}
