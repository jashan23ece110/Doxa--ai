import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, Database, Globe, Zap, Mic, MessageSquare } from 'lucide-react';

const CAPABILITIES = [
  {
    label: 'Autonomous Reasoning',
    desc: 'Multi-step planning, tool use & self-correction loop.',
    icon: Cpu,
    colorClass: 'text-violet-600',
    iconBgClass: 'bg-violet-50 text-violet-600 border-violet-100',
    hoverClass: 'hover:border-violet-300 hover:shadow-violet-100/60'
  },
  {
    label: 'Real-Time RAG',
    desc: 'Instant context-aware search and retrieval indexing.',
    icon: Database,
    colorClass: 'text-indigo-600',
    iconBgClass: 'bg-indigo-50 text-indigo-600 border-indigo-100',
    hoverClass: 'hover:border-indigo-300 hover:shadow-indigo-100/60'
  },
  {
    label: 'Live Web Search',
    desc: 'Grounding responses with real-time web citations.',
    icon: Globe,
    colorClass: 'text-cyan-600',
    iconBgClass: 'bg-cyan-50 text-cyan-600 border-cyan-100',
    hoverClass: 'hover:border-cyan-300 hover:shadow-cyan-100/60'
  },
  {
    label: 'Streaming Responses',
    desc: 'Continuous token delivery with sub-50ms latency.',
    icon: Zap,
    colorClass: 'text-violet-600',
    iconBgClass: 'bg-violet-50 text-violet-600 border-violet-100',
    hoverClass: 'hover:border-violet-300 hover:shadow-violet-100/60'
  },
  {
    label: 'Native Voice Engine',
    desc: 'Integrated speech recognition & vocal responses.',
    icon: Mic,
    colorClass: 'text-indigo-600',
    iconBgClass: 'bg-indigo-50 text-indigo-600 border-indigo-100',
    hoverClass: 'hover:border-indigo-300 hover:shadow-indigo-100/60'
  },
  {
    label: 'Multi-Model Debate',
    desc: 'Cross-consensus checking and argument checks.',
    icon: MessageSquare,
    colorClass: 'text-cyan-600',
    iconBgClass: 'bg-cyan-50 text-cyan-600 border-cyan-100',
    hoverClass: 'hover:border-cyan-300 hover:shadow-cyan-100/60'
  }
];

export default function CapabilityStrip() {
  return (
    <section className="py-10 bg-white border-t border-neutral-100 z-10 relative select-none">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          {CAPABILITIES.map((cap, idx) => {
            const Icon = cap.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 15 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-50px' }}
                transition={{ duration: 0.4, delay: idx * 0.08, ease: 'easeOut' }}
                className={`flex flex-col gap-3 p-4.5 rounded-2xl bg-white border border-neutral-200/80 shadow-sm shadow-neutral-100/40 transition-all duration-300 hover:-translate-y-1 hover:shadow-md cursor-default ${cap.hoverClass}`}
              >
                {/* Icon Container */}
                <div className={`w-8 h-8 rounded-xl border flex items-center justify-center ${cap.iconBgClass} shrink-0`}>
                  <Icon className="w-4 h-4" />
                </div>

                {/* Text content */}
                <div className="flex flex-col gap-1">
                  <span className="text-[13px] font-bold text-neutral-900 font-sans tracking-tight leading-snug">
                    {cap.label}
                  </span>
                  <span className="text-[11px] text-neutral-600 font-sans leading-normal">
                    {cap.desc}
                  </span>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
