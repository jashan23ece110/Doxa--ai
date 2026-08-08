import React, { useRef, useEffect } from 'react';
import { motion, useInView } from 'framer-motion';
import { Sparkles, ArrowRight } from 'lucide-react';
import SvgLogo from './logo/SvgLogo';

export default function FinalCTA({ onLaunchApp }) {
  const containerRef = useRef(null);
  const canvasRef = useRef(null);
  const isInView = useInView(containerRef, { once: true, margin: '-100px' });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId;
    let width = canvas.width = canvas.offsetWidth;
    let height = canvas.height = canvas.offsetHeight;

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = canvas.offsetWidth;
      height = canvas.height = canvas.offsetHeight;
    };
    window.addEventListener('resize', handleResize);

    const particles = [];
    const particleCount = 40;
    
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        r: 1 + Math.random() * 1.5,
        vx: (Math.random() - 0.5) * 0.18,
        vy: (Math.random() - 0.5) * 0.18,
        alpha: 0.15 + Math.random() * 0.35,
        color: Math.random() > 0.5 ? '#8b5cf6' : '#06b6d4'
      });
    }

    const draw = () => {
      ctx.clearRect(0, 0, width, height);

      for (let i = 0; i < particleCount; i++) {
        for (let j = i + 1; j < particleCount; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 110) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            const lineAlpha = (1 - dist / 110) * 0.07;
            ctx.strokeStyle = `rgba(139, 92, 246, ${lineAlpha})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }

      particles.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.fill();

        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0) p.x = width;
        if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height;
        if (p.y > height) p.y = 0;
      });
      ctx.globalAlpha = 1.0;

      animationFrameId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div ref={containerRef} className="w-full bg-black">
      {/* ── Dark Cinematic Final CTA Section ── */}
      <section className="w-full bg-black py-28 relative overflow-hidden flex flex-col items-center justify-center text-white border-t border-white/[0.08]">
        {/* Canvas background for light particle flow */}
        <canvas ref={canvasRef} className="absolute inset-0 z-0 pointer-events-none opacity-40" />

        {/* Ambient Radial Gradient Glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[550px] rounded-full bg-gradient-to-r from-violet-600/10 via-indigo-600/10 to-cyan-500/10 blur-[130px] pointer-events-none z-0" />

        {/* Content Centering Container */}
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center flex flex-col items-center justify-center z-10 relative select-none">
          
          {/* Eyebrow Label */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 15 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/[0.03] border border-white/[0.08] text-violet-300 text-xs font-mono mb-8"
          >
            <Sparkles className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
            <span className="font-bold uppercase tracking-wider text-[10px]">EXPERIENCE AUTONOMOUS AI TODAY</span>
          </motion.div>

          {/* Headline */}
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight mb-6 font-orbitron max-w-3xl leading-tight"
            style={{ fontFamily: 'Orbitron, sans-serif' }}
          >
            Ready to Experience Doxa?
          </motion.h2>

          {/* Subtext */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="text-base sm:text-lg text-neutral-400 font-sans max-w-2xl mb-12 leading-relaxed"
          >
            Deploy multi-step reasoning loops, index vector repositories, and orchestrate autonomous tools in a single unified AI operating system.
          </motion.p>

          {/* Large Primary Try Doxa Button */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={isInView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <button
              type="button"
              onClick={onLaunchApp}
              className="relative px-10 py-4.5 rounded-full font-bold text-sm tracking-wide text-white overflow-hidden group cursor-pointer shadow-[0_0_40px_rgba(124,58,237,0.35)] transition-all duration-300 hover:shadow-[0_0_50px_rgba(6,182,212,0.5)] hover:scale-105 active:scale-95 border border-white/10"
              style={{
                background: 'linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #06b6d4 100%)',
              }}
              aria-label="Try Doxa Now"
            >
              <span className="relative z-10 flex items-center gap-3">
                <SvgLogo size={20} className="w-5 h-5" />
                <span>Try Doxa Now</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1.5 transition-transform duration-200" />
              </span>
            </button>
          </motion.div>

        </div>
      </section>
    </div>
  );
}
