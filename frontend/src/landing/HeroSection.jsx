import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, ArrowRight, ChevronDown, Zap, ShieldCheck, Database, Globe } from 'lucide-react';
import doxaLogo from '../assets/logo.png';

export default function HeroSection({ onLaunchApp }) {
  return (
    <section className="relative min-h-screen flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8 pt-24 pb-16 z-10 text-center">
      {/* Background Subtle Logo Watermark Accent */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] sm:w-[650px] sm:h-[650px] pointer-events-none z-0 opacity-[0.06] select-none flex items-center justify-center">
        <img
          src={doxaLogo}
          alt=""
          className="w-full h-full object-contain filter invert brightness-200"
        />
      </div>
      {/* Top Capability Pill */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-violet-500/10 border border-violet-500/30 text-violet-300 text-xs font-mono mb-8 backdrop-blur-md shadow-[0_0_20px_rgba(139,92,246,0.2)]"
      >
        <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
        <span className="font-semibold uppercase tracking-wider text-[11px]">
          NEXT-GEN AUTONOMOUS AGENT + RAG PIPELINE
        </span>
      </motion.div>

      {/* Main Hero Headline */}
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.1, ease: 'easeOut' }}
        className="max-w-5xl text-4xl sm:text-6xl md:text-7xl font-extrabold text-white tracking-tight leading-[1.1] mb-6 font-orbitron"
        style={{ fontFamily: 'Orbitron, sans-serif' }}
      >
        Meet Doxa — An AI That{' '}
        <span className="bg-clip-text text-transparent bg-gradient-to-r from-violet-400 via-indigo-400 to-cyan-400 drop-shadow-[0_0_35px_rgba(139,92,246,0.5)]">
          Thinks, Searches, and Acts.
        </span>
      </motion.h1>

      {/* Subheadline */}
      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2, ease: 'easeOut' }}
        className="max-w-2xl text-base sm:text-xl text-neutral-300 font-sans leading-relaxed mb-10 font-normal"
      >
        Autonomous multi-step reasoning, instant document intelligence, live web citations, and native voice activation — built into a single cinematic platform.
      </motion.p>

      {/* Hero CTA Button */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6, delay: 0.3, ease: 'easeOut' }}
        className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16"
      >
        <motion.button
          type="button"
          onClick={onLaunchApp}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="relative px-8 py-4 rounded-2xl font-bold text-sm uppercase tracking-wider text-white shadow-[0_0_40px_rgba(139,92,246,0.6)] overflow-hidden group cursor-pointer"
          style={{ fontFamily: 'Orbitron, sans-serif' }}
        >
          <span className="absolute inset-0 bg-gradient-to-r from-violet-600 via-indigo-600 to-cyan-500 group-hover:brightness-125 transition-all duration-300" />
          <span className="relative z-10 flex items-center gap-3">
            <Sparkles className="w-5 h-5 text-cyan-300 animate-bounce" />
            <span>Launch Doxa AI</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1.5 transition-transform" />
          </span>
        </motion.button>
      </motion.div>

      {/* Capability Feature Badges Strip */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.4, ease: 'easeOut' }}
        className="grid grid-cols-2 md:grid-cols-4 gap-3 max-w-4xl w-full text-xs font-mono select-none"
      >
        <div className="p-3 rounded-xl bg-black/50 border border-violet-500/20 backdrop-blur-md flex items-center justify-center gap-2 text-neutral-300">
          <Zap className="w-4 h-4 text-violet-400 shrink-0" />
          <span>Multi-Step Agent</span>
        </div>
        <div className="p-3 rounded-xl bg-black/50 border border-indigo-500/20 backdrop-blur-md flex items-center justify-center gap-2 text-neutral-300">
          <Database className="w-4 h-4 text-indigo-400 shrink-0" />
          <span>Vector RAG</span>
        </div>
        <div className="p-3 rounded-xl bg-black/50 border border-cyan-500/20 backdrop-blur-md flex items-center justify-center gap-2 text-neutral-300">
          <Globe className="w-4 h-4 text-cyan-400 shrink-0" />
          <span>Live Web Search</span>
        </div>
        <div className="p-3 rounded-xl bg-black/50 border border-emerald-500/20 backdrop-blur-md flex items-center justify-center gap-2 text-neutral-300">
          <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>Dual Debate</span>
        </div>
      </motion.div>

      {/* Scroll-down Bounce Indicator */}
      <motion.div
        animate={{ y: [0, 10, 0] }}
        transition={{ repeat: Infinity, duration: 2, ease: 'easeInOut' }}
        className="absolute bottom-6 left-1/2 -translate-x-1/2 text-neutral-500 hover:text-white transition-colors cursor-pointer"
        onClick={() => {
          const el = document.getElementById('features');
          if (el) el.scrollIntoView({ behavior: 'smooth' });
        }}
      >
        <ChevronDown className="w-6 h-6 text-violet-400/80" />
      </motion.div>
    </section>
  );
}
