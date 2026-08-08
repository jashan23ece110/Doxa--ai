import React from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import { ArrowRight, ChevronDown, Sparkles, Cpu, Database, Globe, Mic } from 'lucide-react';
import SvgLogo from './logo/SvgLogo';

const CAPABILITY_PILLS = [
  { label: 'Autonomous Reasoning', icon: Cpu },
  { label: 'Document RAG', icon: Database },
  { label: 'Live Web Search', icon: Globe },
  { label: 'Native Voice Mode', icon: Mic },
];

export default function HeroSection({ onLaunchApp }) {
  const shouldReduceMotion = useReducedMotion();

  // Animation variants respecting prefers-reduced-motion
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: shouldReduceMotion ? 0 : 0.12,
        delayChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 24 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: shouldReduceMotion ? 0.2 : 0.7,
        ease: [0.21, 0.47, 0.32, 0.98],
      },
    },
  };

  const scrollToFeatures = () => {
    const el = document.getElementById('features');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section
      aria-label="Hero Section"
      className="relative min-h-[92vh] lg:min-h-screen flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8 pt-28 pb-16 z-10 text-center select-none"
    >
      {/* Ambient background glow & atmospheric radial lighting */}
      <div
        className="absolute inset-0 pointer-events-none -z-10 flex items-center justify-center overflow-hidden"
        aria-hidden="true"
      >
        <div className="w-[600px] sm:w-[900px] h-[400px] sm:h-[600px] bg-[radial-gradient(ellipse_at_center,rgba(124,58,237,0.18)_0%,rgba(99,102,241,0.10)_35%,rgba(6,182,212,0.05)_60%,transparent_80%)] blur-3xl opacity-90" />
      </div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-4xl mx-auto flex flex-col items-center gap-6 sm:gap-8"
      >
        {/* ── 1. Enterprise Tag Badge ── */}
        <motion.div variants={itemVariants}>
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/[0.03] border border-white/[0.12] backdrop-blur-md shadow-inner text-xs sm:text-sm font-medium text-neutral-300">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-400" />
            </span>
            <span className="font-mono text-[11px] sm:text-xs tracking-wider uppercase text-neutral-300 font-semibold">
              DOXA ENTERPRISE AI OPERATING SYSTEM
            </span>
          </div>
        </motion.div>

        {/* ── 2. Primary Headline ── */}
        <motion.h1
          variants={itemVariants}
          className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-white tracking-tight leading-[1.12] max-w-4xl"
        >
          An AI that doesn't just answer —{' '}
          <span className="block mt-2 sm:mt-3 bg-clip-text text-transparent bg-gradient-to-r from-violet-300 via-indigo-200 to-cyan-300 drop-shadow-[0_0_35px_rgba(124,58,237,0.3)]">
            it thinks, retrieves, and acts.
          </span>
        </motion.h1>

        {/* ── 3. Supporting Description ── */}
        <motion.p
          variants={itemVariants}
          className="max-w-2xl text-base sm:text-lg md:text-xl text-neutral-400 font-normal leading-relaxed tracking-normal"
        >
          Orchestrating multi-step autonomous reasoning, vector document intelligence, and real-time enterprise tool execution into a unified AI operating platform.
        </motion.p>

        {/* ── 4. CTA Actions (Primary + Secondary) ── */}
        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row items-center gap-3.5 sm:gap-4 mt-2 sm:mt-4 w-full sm:w-auto"
        >
          {/* Primary CTA Button */}
          <motion.button
            type="button"
            onClick={onLaunchApp}
            whileHover={shouldReduceMotion ? {} : { scale: 1.04 }}
            whileTap={shouldReduceMotion ? {} : { scale: 0.96 }}
            className="group relative w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-full text-[15px] font-semibold text-white cursor-pointer overflow-hidden shadow-[0_0_30px_rgba(124,58,237,0.35)] hover:shadow-[0_0_40px_rgba(6,182,212,0.45)] transition-all duration-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-black"
            style={{
              background: 'linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #06b6d4 100%)',
            }}
            aria-label="Try Doxa AI Operating System"
          >
            <SvgLogo size={20} className="w-5 h-5" />
            <span>Try Doxa</span>
            <ArrowRight className="w-4 h-4 opacity-75 group-hover:translate-x-1 transition-transform duration-200" />
          </motion.button>

          {/* Secondary CTA Button */}
          <motion.button
            type="button"
            onClick={scrollToFeatures}
            whileHover={shouldReduceMotion ? {} : { scale: 1.02 }}
            whileTap={shouldReduceMotion ? {} : { scale: 0.98 }}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-4 rounded-full text-[15px] font-medium text-neutral-300 hover:text-white bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.12] backdrop-blur-md transition-all duration-200 cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-violet-400"
            aria-label="Explore Platform Capabilities"
          >
            <Sparkles className="w-4 h-4 text-violet-400" />
            <span>Explore Capabilities</span>
          </motion.button>
        </motion.div>

        {/* ── 5. System Capability Pills ── */}
        <motion.div
          variants={itemVariants}
          className="flex flex-wrap items-center justify-center gap-2 sm:gap-3 mt-4 sm:mt-6 max-w-3xl"
        >
          {CAPABILITY_PILLS.map((pill, idx) => {
            const Icon = pill.icon;
            return (
              <div
                key={idx}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/[0.03] border border-white/[0.08] backdrop-blur-sm text-[12px] font-mono text-neutral-300 font-medium hover:border-violet-500/40 hover:bg-white/[0.06] transition-colors"
              >
                <Icon className="w-3.5 h-3.5 text-cyan-400" />
                <span>{pill.label}</span>
              </div>
            );
          })}
        </motion.div>
      </motion.div>

      {/* ── 6. Scroll Indicator ── */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: [0, 8, 0] }}
        transition={{
          opacity: { delay: 1, duration: 0.6 },
          y: { repeat: Infinity, duration: 2.5, ease: 'easeInOut' },
        }}
        className="absolute bottom-6 sm:bottom-8 left-1/2 -translate-x-1/2 text-neutral-500 hover:text-white transition-colors cursor-pointer p-2 focus:outline-none focus-visible:ring-2 focus-visible:ring-violet-400 rounded-full"
        onClick={scrollToFeatures}
        aria-label="Scroll down to features"
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === 'Enter' && scrollToFeatures()}
      >
        <ChevronDown className="w-6 h-6 text-violet-400/70" />
      </motion.div>
    </section>
  );
}
