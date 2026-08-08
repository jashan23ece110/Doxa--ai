import React, { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { STEPS } from '../../data/landingData';

export default function HowItWorks() {
  const containerRef = useRef(null);
  const isInView = useInView(containerRef, { once: true, margin: '-100px' });

  return (
    <section 
      ref={containerRef}
      id="how-it-works" 
      className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10 relative bg-white select-none overflow-hidden"
    >
      {/* Section Header */}
      <div className="text-center max-w-3xl mx-auto mb-20">
        <h2 className="text-xs font-mono font-bold uppercase tracking-widest text-violet-600 mb-3">
          EXECUTION ARCHITECTURE
        </h2>
        <p className="text-3xl sm:text-5xl font-extrabold text-neutral-900 tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          How Doxa Works Under the Hood
        </p>
        <p className="mt-4 text-sm text-neutral-600 max-w-xl mx-auto font-sans leading-relaxed">
          Trace the exact lifecycle of an execution request as it passes from raw prompt to grounded output.
        </p>
      </div>

      {/* Steps Container */}
      <div className="relative">
        {/* Animated Connector Line (Desktop Only) */}
        <div className="absolute top-[3.75rem] left-0 w-full h-[4px] z-0 pointer-events-none hidden xl:block">
          <svg className="w-full h-full overflow-visible" viewBox="0 0 1000 100" preserveAspectRatio="none">
            {/* Background inactive track */}
            <path 
              d="M 125 50 L 875 50" 
              stroke="#e5e7eb" 
              strokeWidth="4" 
              strokeDasharray="8 8"
              fill="none"
            />
            {/* Animated active gradient line */}
            <motion.path 
              d="M 125 50 L 875 50" 
              stroke="url(#flow-gradient)" 
              strokeWidth="5" 
              strokeLinecap="round"
              fill="none"
              initial={{ pathLength: 0 }}
              animate={isInView ? { pathLength: 1 } : { pathLength: 0 }}
              transition={{ duration: 1.5, ease: 'easeInOut', delay: 0.1 }}
            />
            <defs>
              <linearGradient id="flow-gradient" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#8b5cf6" />
                <stop offset="50%" stopColor="#6366f1" />
                <stop offset="100%" stopColor="#06b6d4" />
              </linearGradient>
            </defs>
          </svg>
        </div>

        {/* Horizontal steps columns */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 relative z-10">
          {STEPS.map((s, idx) => {
            const Icon = s.icon;
            
            // Sequential stagger animation config
            const cardVariants = {
              hidden: { opacity: 0, y: 25 },
              visible: { 
                opacity: 1, 
                y: 0,
                transition: { duration: 0.5, ease: 'easeOut', delay: idx * 0.45 }
              }
            };

            return (
              <motion.div
                key={idx}
                variants={cardVariants}
                initial="hidden"
                animate={isInView ? 'visible' : 'hidden'}
                className={`relative p-6 rounded-2xl bg-white border border-neutral-200/80 flex flex-col gap-4 shadow-sm shadow-neutral-100/40 transition-all duration-300 hover:-translate-y-1 hover:shadow-md cursor-default ${s.hoverClass}`}
              >
                {/* Step number badge & Icon */}
                <div className="flex items-center justify-between z-10">
                  <span className={`text-xs font-mono font-bold ${s.colorClass}`}>
                    STEP {s.step}
                  </span>
                  <div className={`p-2.5 rounded-xl border flex items-center justify-center ${s.iconBgClass}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                </div>

                {/* Step Title & Details */}
                <div className="flex flex-col gap-2">
                  <h3 className="text-lg font-bold text-neutral-900 font-sans tracking-tight">
                    {s.title}
                  </h3>
                  <p className="text-xs text-neutral-600 leading-relaxed font-sans">
                    {s.desc}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
