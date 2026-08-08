import React, { useState } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { 
  ShieldCheck, 
  Database, 
  Cpu, 
  GitBranch, 
  Activity, 
  ArrowRight, 
  CheckCircle2,
  Layers,
  Sparkles,
  Zap
} from 'lucide-react';

const STAGES = [
  {
    id: 1,
    stageNum: 'STAGE 1',
    title: 'Intelligent Foundation',
    subtitle: 'Production Infrastructure, Security & RAG Core',
    desc: 'Provides the bedrock of Doxa with enterprise-grade security, deterministic memory primitives, and basic retrieval pipelines.',
    color: 'from-violet-500 to-indigo-500',
    accentColor: '#8b5cf6',
    icon: ShieldCheck,
    capabilities: [
      'Production AI Infrastructure',
      'Zero-Trust Security & Audit Logs',
      'Deterministic Memory Engine',
      'RAG Indexing Engine'
    ],
    modules: ['Kernel Lifecycle', 'Security Sentinel', 'Memory Store']
  },
  {
    id: 2,
    stageNum: 'STAGE 2',
    title: 'Retrieval Intelligence',
    subtitle: 'Contextual Knowledge & Semantic Indexing',
    desc: 'Transforms unstructured enterprise documents into dense semantic vector graphs for zero-hallucination context retrieval.',
    color: 'from-indigo-500 to-cyan-500',
    accentColor: '#6366f1',
    icon: Database,
    capabilities: [
      'Advanced ChromaDB Vectors',
      'Contextual Chunking & Ranking',
      'Tavily Live Web Search',
      'Semantic Citation Engine'
    ],
    modules: ['Vector Database', 'Web Search Connector', 'Citation Builder']
  },
  {
    id: 3,
    stageNum: 'STAGE 3',
    title: 'Cognitive & Multi-Agent Intelligence',
    subtitle: 'Multi-Step Planning & Dual-Model Consensus',
    desc: 'Orchestrates cognitive reasoning loops, iterative self-critique, and dual-model Optimist vs Skeptic debate consensus.',
    color: 'from-cyan-500 to-teal-400',
    accentColor: '#06b6d4',
    icon: Cpu,
    capabilities: [
      'Multi-Step Reasoning Loops',
      'Dual-Model Debate Engine',
      'Self-Correction & Verification',
      'Autonomous Task Execution'
    ],
    modules: ['Planning Engine', 'Debate Referee', 'Tool Orchestrator']
  },
  {
    id: 4,
    stageNum: 'STAGE 4',
    title: 'Distributed AI Operating System',
    subtitle: 'Async Daemons, Workflows & Workspace Sync',
    desc: 'Acts as a full AI OS managing background execution queues, timeline thread branching, and external workspace APIs.',
    color: 'from-purple-500 to-violet-500',
    accentColor: '#a855f7',
    icon: GitBranch,
    capabilities: [
      'Distributed Task Scheduler',
      'Timeline Thread Branching',
      'Background Execution Daemons',
      'Google Workspace Integration'
    ],
    modules: ['Intelligence Scheduler', 'Branch Manager', 'Workspace Gateway']
  },
  {
    id: 5,
    stageNum: 'STAGE 5',
    title: 'Autonomous Enterprise AI',
    subtitle: 'End-to-End Governance, Learning & Operations',
    desc: 'Unifies intelligence, safety, and operations into an autonomous AI operating system with continuous feedback loops.',
    color: 'from-cyan-400 via-indigo-500 to-violet-500',
    accentColor: '#38bdf8',
    icon: Activity,
    capabilities: [
      'Autonomous Enterprise Automation',
      'Continuous Learning & Feedback',
      'Policy Governance & Compliance',
      'Autonomous Operational Recovery'
    ],
    modules: ['AI OS Kernel', 'Governance Engine', 'Operational Dashboard']
  }
];

const FLOW_STEPS = [
  { label: 'User Intent', desc: 'Goal / Prompt' },
  { label: 'Context', desc: 'System State' },
  { label: 'Retrieval', desc: 'RAG & Web' },
  { label: 'Reasoning', desc: 'Multi-Step Plan' },
  { label: 'Agents', desc: 'Debate / Action' },
  { label: 'Action', desc: 'Tool Execution' },
  { label: 'Memory', desc: 'Knowledge Sync' },
];

export default function StageExplorer() {
  const [activeStageId, setActiveStageId] = useState(1);
  const shouldReduceMotion = useReducedMotion();
  const activeStage = STAGES.find(s => s.id === activeStageId) || STAGES[0];
  const StageIcon = activeStage.icon;

  return (
    <section 
      id="stage-explorer"
      className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10 relative select-none"
    >
      {/* Section Header */}
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-violet-500/10 border border-violet-500/20 mb-4">
          <Layers className="w-3.5 h-3.5 text-violet-400" />
          <span className="text-xs font-mono font-semibold text-violet-300 uppercase tracking-wider">
            STAGES 1–5 ARCHITECTURE EVOLUTION
          </span>
        </div>
        <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          Explore Doxa’s Intelligence Layers
        </h2>
        <p className="mt-4 text-base text-neutral-400 max-w-2xl mx-auto font-sans leading-relaxed">
          Discover how Doxa evolves from foundational infrastructure to an autonomous enterprise AI operating system.
        </p>
      </div>

      {/* ── System Flow Lifecycle Diagram ── */}
      <div className="mb-16 p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/[0.08] backdrop-blur-2xl shadow-2xl overflow-x-auto hud-scrollbar">
        <div className="text-xs font-mono text-neutral-400 font-bold uppercase tracking-widest mb-6 flex items-center gap-2">
          <Zap className="w-4 h-4 text-cyan-400" />
          <span>DOXA SYSTEM EXECUTION LIFECYCLE</span>
        </div>
        <div className="flex items-center justify-between min-w-[700px] gap-2 relative">
          {FLOW_STEPS.map((step, idx) => (
            <React.Fragment key={idx}>
              <div className="flex flex-col items-center text-center gap-1.5 p-3 rounded-2xl bg-white/[0.02] border border-white/[0.06] hover:border-violet-500/40 transition-all w-28 shrink-0">
                <span className="text-[10px] font-mono text-cyan-400 font-bold">0{idx + 1}</span>
                <span className="text-xs font-bold text-white tracking-tight font-sans">{step.label}</span>
                <span className="text-[10px] text-neutral-500 font-mono">{step.desc}</span>
              </div>
              {idx < FLOW_STEPS.length - 1 && (
                <div className="flex items-center justify-center shrink-0 text-violet-500/50">
                  <ArrowRight className="w-4 h-4 animate-pulse" />
                </div>
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* ── Interactive Stage Explorer ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left: Stage Selection Tabs */}
        <div className="lg:col-span-4 flex flex-col gap-3">
          {STAGES.map((stg) => {
            const isActive = stg.id === activeStageId;
            const Icon = stg.icon;
            return (
              <button
                key={stg.id}
                type="button"
                onClick={() => setActiveStageId(stg.id)}
                className={`relative flex items-center justify-between p-4 rounded-2xl border text-left transition-all duration-300 cursor-pointer ${
                  isActive
                    ? 'bg-neutral-900/90 border-violet-500/50 shadow-[0_0_25px_rgba(124,58,237,0.2)] text-white'
                    : 'bg-neutral-950/50 border-white/[0.06] hover:bg-neutral-900/40 text-neutral-400 hover:text-neutral-200'
                }`}
              >
                <div className="flex items-center gap-3.5">
                  <div 
                    className={`w-9 h-9 rounded-xl border flex items-center justify-center shrink-0 transition-colors ${
                      isActive 
                        ? 'bg-violet-500/20 border-violet-500/40 text-cyan-400' 
                        : 'bg-white/[0.03] border-white/[0.08] text-neutral-500'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[10px] font-mono font-bold text-violet-400 tracking-wider uppercase">
                      {stg.stageNum}
                    </span>
                    <span className="text-sm font-bold tracking-tight text-white font-sans">
                      {stg.title}
                    </span>
                  </div>
                </div>

                <ArrowRight className={`w-4 h-4 transition-transform duration-200 ${isActive ? 'translate-x-1 text-cyan-400' : 'opacity-30'}`} />
              </button>
            );
          })}
        </div>

        {/* Right: Active Stage Detail View */}
        <div className="lg:col-span-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeStage.id}
              initial={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, x: -20 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
              className="p-6 sm:p-8 rounded-3xl bg-neutral-950/90 border border-white/[0.1] backdrop-blur-2xl shadow-2xl flex flex-col justify-between min-h-[420px]"
            >
              <div>
                {/* Header */}
                <div className="flex items-center justify-between border-b border-white/[0.08] pb-4 mb-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 rounded-xl bg-violet-500/15 border border-violet-500/30 text-cyan-400">
                      <StageIcon className="w-5 h-5" />
                    </div>
                    <div>
                      <span className="text-xs font-mono font-bold text-violet-400 uppercase tracking-widest block">
                        {activeStage.stageNum} ARCHITECTURE
                      </span>
                      <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                        {activeStage.title}
                      </h3>
                    </div>
                  </div>
                  <span className="text-xs font-mono px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-300 font-semibold">
                    STAGE {activeStage.id} ACTIVE
                  </span>
                </div>

                {/* Subtitle & Description */}
                <h4 className="text-sm font-semibold text-neutral-200 mb-2 font-sans">
                  {activeStage.subtitle}
                </h4>
                <p className="text-sm text-neutral-400 font-sans leading-relaxed mb-6">
                  {activeStage.desc}
                </p>

                {/* Capabilities Grid */}
                <div className="mb-6">
                  <span className="text-xs font-mono font-bold text-neutral-400 uppercase tracking-wider block mb-3">
                    KEY CAPABILITIES
                  </span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {activeStage.capabilities.map((cap, cIdx) => (
                      <div 
                        key={cIdx}
                        className="flex items-center gap-2.5 p-3 rounded-xl bg-white/[0.02] border border-white/[0.06] text-xs font-medium text-neutral-200 font-sans"
                      >
                        <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0" />
                        <span>{cap}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Modules Footer */}
              <div className="pt-4 border-t border-white/[0.08] flex flex-wrap items-center justify-between gap-3 text-xs font-mono text-neutral-400">
                <span className="flex items-center gap-1.5 text-violet-400 font-semibold">
                  <Sparkles className="w-3.5 h-3.5" /> ARCHITECTURE MODULES:
                </span>
                <div className="flex flex-wrap gap-2">
                  {activeStage.modules.map((m, mIdx) => (
                    <span key={mIdx} className="px-2.5 py-1 rounded bg-white/[0.04] border border-white/[0.08] text-[11px] text-neutral-300">
                      {m}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}
