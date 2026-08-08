import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, ChevronDown } from 'lucide-react';
import SvgLogo from '../logo/SvgLogo';
import DoxaLogoMotion from '../logo/DoxaLogoMotion';

export default function HeroSection({ onLaunchApp }) {
  return (
    <section className="relative min-h-screen flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8 pt-24 pb-16 z-10 text-center">

      {/* ── Prominent Animated Logo Integration ── */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9, y: -20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 1, delay: 0.2, ease: 'easeOut' }}
        className="mb-10 flex flex-col items-center cursor-pointer group"
        title="Hover to process information"
      >
        <DoxaLogoMotion className="w-28 h-28 text-white/90 drop-shadow-[0_0_15px_rgba(139,92,246,0.3)] transition-colors duration-500 group-hover:text-cyan-300" />
      </motion.div>

      {/* ── Single bold headline ── */}
      <motion.h1
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 0.4, ease: 'easeOut' }}
        className="max-w-4xl text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-white tracking-tight leading-[1.12] mb-10"
      >
        An AI that doesn't just answer —{' '}
        <span className="bg-clip-text text-transparent bg-gradient-to-r from-violet-400 via-indigo-400 to-cyan-400">
          it thinks, retrieves, and acts.
        </span>
      </motion.h1>

      {/* ── Single CTA button ── */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.7, ease: 'easeOut' }}
      >
        <motion.button
          type="button"
          onClick={onLaunchApp}
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.96 }}
          className="group relative inline-flex items-center gap-2.5 px-7 py-3.5 rounded-full text-[15px] font-semibold text-white cursor-pointer overflow-hidden shadow-lg"
          style={{
            background: 'linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #06b6d4 100%)',
          }}
        >
          <SvgLogo className="w-5 h-5 text-white" />
          <span>Try Doxa</span>
          <ArrowRight className="w-4 h-4 opacity-70 group-hover:translate-x-0.5 transition-transform" />
        </motion.button>
      </motion.div>

      {/* ── Scroll indicator ── */}
      <motion.div
        animate={{ y: [0, 8, 0] }}
        transition={{ repeat: Infinity, duration: 2.5, ease: 'easeInOut' }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 text-neutral-500 hover:text-white transition-colors cursor-pointer"
        onClick={() => {
          const el = document.getElementById('features');
          if (el) el.scrollIntoView({ behavior: 'smooth' });
        }}
      >
        <ChevronDown className="w-6 h-6 text-violet-400/60" />
      </motion.div>
    </section>
  );
}
