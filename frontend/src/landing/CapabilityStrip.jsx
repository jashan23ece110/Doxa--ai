import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, Database, GitBranch, ShieldCheck, Activity, Network } from 'lucide-react';

const CAPABILITIES = [
  {
    label: 'Multi-Agent Intelligence',
    desc: 'Multi-step planning, tool orchestration & consensus.',
    icon: Cpu,
    accentColor: 'text-violet-400',
    iconBgClass: 'bg-violet-500/10 text-violet-400 border-violet-500/20',
  },
  {
    label: 'Enterprise RAG',
    desc: 'Vector semantic indexing over unstructured documents.',
    icon: Database,
    accentColor: 'text-indigo-400',
    iconBgClass: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20',
  },
  {
    label: 'Autonomous Workflows',
    desc: 'Background daemons, timers & timeline thread branching.',
    icon: GitBranch,
    accentColor: 'text-cyan-400',
    iconBgClass: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
  },
  {
    label: 'Persistent Memory',
    desc: 'Long-term session state & knowledge graph sync.',
    icon: Network,
    accentColor: 'text-purple-400',
    iconBgClass: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  },
  {
    label: 'Enterprise Security',
    desc: 'Zero-Trust access control, PII masking & audit logs.',
    icon: ShieldCheck,
    accentColor: 'text-emerald-400',
    iconBgClass: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  },
  {
    label: 'AI OS Operations',
    desc: 'Unified kernel telemetry, routing & fallback recovery.',
    icon: Activity,
    accentColor: 'text-sky-400',
    iconBgClass: 'bg-sky-500/10 text-sky-400 border-sky-500/20',
  }
];

export default function CapabilityStrip() {
  return (
    <section className="py-12 bg-black border-y border-white/[0.08] z-10 relative select-none">
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
                className="flex flex-col gap-3 p-4.5 rounded-2xl bg-neutral-950/80 border border-white/[0.08] backdrop-blur-md shadow-lg transition-all duration-300 hover:border-violet-500/40 hover:-translate-y-1 cursor-default group"
              >
                {/* Icon Container */}
                <div className={`w-9 h-9 rounded-xl border flex items-center justify-center ${cap.iconBgClass} shrink-0 group-hover:scale-105 transition-transform`}>
                  <Icon className="w-4.5 h-4.5" />
                </div>

                {/* Text Content */}
                <div className="flex flex-col gap-1">
                  <span className="text-[13px] font-bold text-white font-sans tracking-tight leading-snug">
                    {cap.label}
                  </span>
                  <span className="text-[11px] text-neutral-400 font-sans leading-normal">
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
