import React from 'react';
import { motion } from 'framer-motion';
import { Upload, Cpu, Database, Sparkles } from 'lucide-react';

const STEPS = [
  { step: '01', title: 'Submit Goal or Upload Data', desc: 'Type your objective or drop documents into Doxa’s knowledge base.', icon: Upload },
  { step: '02', title: 'Autonomous Goal Decomposition', desc: 'Doxa formulates an execution plan and selects required tools.', icon: Cpu },
  { step: '03', title: 'RAG Retrieval & Tool Execution', desc: 'Queries vector database and searches web in parallel.', icon: Database },
  { step: '04', title: 'Verified Stream Synthesis', desc: 'Delivers a citations-backed response with continuous token streaming.', icon: Sparkles }
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10 relative">
      <div className="text-center max-w-3xl mx-auto mb-20">
        <h2 className="text-xs font-mono font-bold uppercase tracking-widest text-cyan-400 mb-3">
          EXECUTION ARCHITECTURE
        </h2>
        <p className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          How Doxa Works Under the Hood.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">
        {STEPS.map((s, idx) => {
          const Icon = s.icon;
          return (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: idx * 0.15 }}
              className="relative p-6 rounded-2xl bg-neutral-950/80 border border-violet-500/20 backdrop-blur-xl flex flex-col gap-4 shadow-xl"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-violet-400">STEP {s.step}</span>
                <div className="p-2.5 rounded-xl bg-violet-500/10 text-violet-300 border border-violet-500/20">
                  <Icon className="w-5 h-5" />
                </div>
              </div>
              <h3 className="text-lg font-bold text-white font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                {s.title}
              </h3>
              <p className="text-xs text-neutral-400 leading-relaxed font-sans">
                {s.desc}
              </p>
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}
