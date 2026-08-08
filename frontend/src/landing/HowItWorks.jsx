import React, { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { Brain, Database, Cpu, GitBranch, Play, RefreshCw } from 'lucide-react';

const STEPS = [
  {
    step: '01',
    title: 'Understand',
    desc: 'Parses user intent, context parameters, and security policies to construct the initial reasoning state.',
    icon: Brain,
    accentColor: 'text-violet-400',
    iconBgClass: 'bg-violet-500/10 text-violet-400 border-violet-500/20',
  },
  {
    step: '02',
    title: 'Retrieve',
    desc: 'Executes parallel vector document search and live Tavily web queries for zero-hallucination grounding.',
    icon: Database,
    accentColor: 'text-indigo-400',
    iconBgClass: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20',
  },
  {
    step: '03',
    title: 'Reason',
    desc: 'Synthesizes retrieved facts, triggers dual-model Optimist vs Skeptic debate, and evaluates evidence.',
    icon: Cpu,
    accentColor: 'text-cyan-400',
    iconBgClass: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
  },
  {
    step: '04',
    title: 'Plan',
    desc: 'Deconstructs complex goals into optimal multi-step tool invocation sequences and agent sub-tasks.',
    icon: GitBranch,
    accentColor: 'text-purple-400',
    iconBgClass: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  },
  {
    step: '05',
    title: 'Act',
    desc: 'Streams real-time citation-backed tokens, executes external workspace APIs, and triggers daemons.',
    icon: Play,
    accentColor: 'text-emerald-400',
    iconBgClass: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  },
  {
    step: '06',
    title: 'Learn',
    desc: 'Consolidates execution telemetry into persistent memory and feeds back learnings to refine future decisions.',
    icon: RefreshCw,
    accentColor: 'text-sky-400',
    iconBgClass: 'bg-sky-500/10 text-sky-400 border-sky-500/20',
  }
];

export default function HowItWorks() {
  const containerRef = useRef(null);
  const isInView = useInView(containerRef, { once: true, margin: '-100px' });

  return (
    <section 
      ref={containerRef}
      id="how-it-works" 
      className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10 relative select-none overflow-hidden"
    >
      {/* Section Header */}
      <div className="text-center max-w-3xl mx-auto mb-20">
        <h2 className="text-xs font-mono font-bold uppercase tracking-widest text-violet-400 mb-3">
          INTELLIGENCE LIFECYCLE
        </h2>
        <h3 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          How Doxa Works Under the Hood
        </h3>
        <p className="mt-4 text-base text-neutral-400 max-w-xl mx-auto font-sans leading-relaxed">
          Trace the exact 6-stage lifecycle of an execution request from initial prompt to persistent memory.
        </p>
      </div>

      {/* Steps Container Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 relative z-10">
        {STEPS.map((s, idx) => {
          const Icon = s.icon;
          
          const cardVariants = {
            hidden: { opacity: 0, y: 25 },
            visible: { 
              opacity: 1, 
              y: 0,
              transition: { duration: 0.5, ease: 'easeOut', delay: idx * 0.15 }
            }
          };

          return (
            <motion.div
              key={idx}
              variants={cardVariants}
              initial="hidden"
              animate={isInView ? 'visible' : 'hidden'}
              className="relative p-6 rounded-3xl bg-neutral-950/80 border border-white/[0.08] backdrop-blur-2xl flex flex-col justify-between gap-4 shadow-2xl transition-all duration-300 hover:border-violet-500/40 hover:-translate-y-1 cursor-default group"
            >
              {/* Step Number Badge & Icon */}
              <div className="flex items-center justify-between z-10">
                <span className={`text-xs font-mono font-bold ${s.accentColor} tracking-wider`}>
                  LIFECYCLE {s.step}
                </span>
                <div className={`p-3 rounded-2xl border flex items-center justify-center ${s.iconBgClass} group-hover:scale-110 transition-transform duration-300`}>
                  <Icon className="w-5 h-5" />
                </div>
              </div>

              {/* Step Title & Details */}
              <div className="flex flex-col gap-2">
                <h4 className="text-xl font-bold text-white font-sans tracking-tight">
                  {s.title}
                </h4>
                <p className="text-xs text-neutral-400 leading-relaxed font-sans">
                  {s.desc}
                </p>
              </div>
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}
