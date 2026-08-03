import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, Database, Globe, Zap } from 'lucide-react';

const STATS = [
  { label: 'Autonomous Tool Execution', val: '10+ Tools', icon: Cpu, desc: 'Planning, RAG, Web & Code' },
  { label: 'Vector RAG Latency', val: '< 15ms', icon: Database, desc: 'Cosine similarity retrieval' },
  { label: 'Live Web Citations', val: 'Real-Time', icon: Globe, desc: 'Tavily search grounding' },
  { label: 'Streaming Response', val: 'Sub-50ms', icon: Zap, desc: 'Continuous token delivery' }
];

export default function CapabilityStrip() {
  return (
    <section className="py-16 bg-black/60 border-y border-white/10 z-10 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {STATS.map((s, idx) => {
            const Icon = s.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                className="flex flex-col gap-2 p-4 rounded-2xl bg-neutral-950/60 border border-violet-500/15 backdrop-blur-md"
              >
                <div className="flex items-center gap-2 text-violet-400">
                  <Icon className="w-4 h-4" />
                  <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-neutral-400">
                    {s.label}
                  </span>
                </div>
                <span className="text-2xl sm:text-3xl font-extrabold text-white font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                  {s.val}
                </span>
                <span className="text-xs text-neutral-400 font-sans">
                  {s.desc}
                </span>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
