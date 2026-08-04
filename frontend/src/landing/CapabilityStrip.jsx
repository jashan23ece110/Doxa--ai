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
    <section className="py-16 bg-transparent z-10 relative">
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
                className="flex flex-col gap-2 p-5 rounded-2xl bg-white border border-neutral-200/80 shadow-md shadow-neutral-100/50 hover:border-violet-500/20 transition-all duration-300 hover:-translate-y-1"
              >
                <div className="flex items-center gap-2 text-violet-600">
                  <Icon className="w-4 h-4 text-violet-500" />
                  <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-neutral-500">
                    {s.label}
                  </span>
                </div>
                <span className="text-2xl sm:text-3xl font-extrabold text-neutral-900 font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                  {s.val}
                </span>
                <span className="text-xs text-neutral-600 font-sans">
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
