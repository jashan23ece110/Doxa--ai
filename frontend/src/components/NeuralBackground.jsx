import { useEffect, useRef } from 'react';

const MIN_SPEED = 0.05;
const MAX_SPEED = 0.22;
const CONNECTION_DISTANCE = 90;

function createParticles(count, width, height) {
  const particles = new Array(count);
  for (let i = 0; i < count; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = MIN_SPEED + Math.random() * (MAX_SPEED - MIN_SPEED);
    const depth = 0.1 + Math.random() * 0.9; // 3D depth scale [0.1, 1.0]
    particles[i] = {
      x: Math.random() * width,
      y: Math.random() * height,
      vx: Math.cos(angle) * speed * depth,
      vy: Math.sin(angle) * speed * depth,
      r: 0.5 + depth * 2.2, // size scales with depth
      depth: depth,
      alpha: 0.04 + depth * 0.35, // opacity scales with depth
      hueOffset: (Math.random() - 0.5) * 30 // slight hue variance
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
    
    // Smooth mouse coordinates for parallax
    let mouseX = 0;
    let mouseY = 0;
    let targetMouseX = 0;
    let targetMouseY = 0;

    const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;
    const particleCount = isMobile ? 300 : 900;

    const resize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      const dpr = window.devicePixelRatio || 1;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      particles = createParticles(particleCount, width, height);
    };

    const handleMouseMove = (e) => {
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
      mouseX += (targetMouseX - mouseX) * 0.05;
      mouseY += (targetMouseY - mouseY) * 0.05;

      const accentRgb = getComputedStyle(document.documentElement).getPropertyValue('--jarvis-accent-rgb').trim() || '0, 217, 255';

      // Update positions & wrap edges
      for (let i = 0; i < particleCount; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < -20) p.x += width + 40;
        else if (p.x > width + 20) p.x -= width + 40;
        if (p.y < -20) p.y += height + 40;
        else if (p.y > height + 20) p.y -= height + 40;
      }

      // Draw faint connections for closer foreground particles
      ctx.strokeStyle = `rgba(${accentRgb}, 0.02)`;
      ctx.lineWidth = 0.4;
      ctx.beginPath();
      const step = isMobile ? 3 : 2;
      for (let i = 0; i < particleCount; i += step) {
        const a = particles[i];
        if (a.depth < 0.5) continue; // only connect foreground particles
        const ax = a.x + mouseX * 25 * a.depth;
        const ay = a.y + mouseY * 25 * a.depth;

        for (let j = i + step; j < particleCount; j += step) {
          const b = particles[j];
          if (b.depth < 0.5) continue;
          const bx = b.x + mouseX * 25 * b.depth;
          const by = b.y + mouseY * 25 * b.depth;

          const dx = ax - bx;
          const dy = ay - by;
          if (dx < CONNECTION_DISTANCE && dx > -CONNECTION_DISTANCE && dy < CONNECTION_DISTANCE && dy > -CONNECTION_DISTANCE) {
            if (dx * dx + dy * dy < CONNECTION_DISTANCE * CONNECTION_DISTANCE) {
              ctx.moveTo(ax, ay);
              ctx.lineTo(bx, by);
            }
          }
        }
      }
      ctx.stroke();

      // Draw ambient particle field with depth opacity & sizing
      for (let i = 0; i < particleCount; i++) {
        const p = particles[i];
        const px = p.x + mouseX * 25 * p.depth;
        const py = p.y + mouseY * 25 * p.depth;

        ctx.fillStyle = `rgba(${accentRgb}, ${p.alpha})`;
        ctx.beginPath();
        ctx.arc(px, py, p.r, 0, Math.PI * 2);
        ctx.fill();
      }

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
        opacity: 0.85,
        pointerEvents: 'none',
      }}
      aria-hidden="true"
    />
  );
}
