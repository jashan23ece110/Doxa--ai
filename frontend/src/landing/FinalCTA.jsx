import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, ArrowRight } from 'lucide-react';

export default function FinalCTA({ onLaunchApp }) {
  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10 relative">
      <div className="relative rounded-3xl p-10 sm:p-16 overflow-hidden border border-violet-500/30 text-center flex flex-col items-center justify-center bg-gradient-to-b from-neutral-950 via-neutral-900 to-black shadow-[0_0_60px_rgba(139,92,246,0.3)]">
        {/* Ambient Radial Gradient Glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-violet-600/20 blur-[100px] pointer-events-none" />

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="relative z-10 flex flex-col items-center"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-violet-500/10 border border-violet-500/30 text-violet-300 text-xs font-mono mb-6">
            <Sparkles className="w-4 h-4 text-cyan-400 animate-pulse" />
            <span className="font-semibold uppercase tracking-wider">EXPERIENCE AUTONOMOUS AI TODAY</span>
          </div>

          <h2 className="text-3xl sm:text-6xl font-extrabold text-white tracking-tight mb-6 font-orbitron max-w-3xl" style={{ fontFamily: 'Orbitron, sans-serif' }}>
            Ready to See What Doxa Can Do?
          </h2>

          <p className="text-base sm:text-xl text-neutral-300 font-sans max-w-2xl mb-10">
            Launch the live Doxa AI agent platform now. Upload documents, execute multi-step goals, and interact in real time.
          </p>

          <motion.button
            type="button"
            onClick={onLaunchApp}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="relative px-9 py-4 rounded-2xl font-bold text-sm uppercase tracking-wider text-white shadow-[0_0_50px_rgba(139,92,246,0.7)] overflow-hidden group cursor-pointer"
            style={{ fontFamily: 'Orbitron, sans-serif' }}
          >
            <span className="absolute inset-0 bg-gradient-to-r from-violet-600 via-indigo-600 to-cyan-500 group-hover:brightness-125 transition-all duration-300" />
            <span className="relative z-10 flex items-center gap-3">
              <Sparkles className="w-5 h-5 text-cyan-300 animate-bounce" />
              <span>Launch Doxa App</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1.5 transition-transform" />
            </span>
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
}
