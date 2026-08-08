import React, { useState } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { 
  Sparkles, 
  Layers, 
  ArrowRight, 
  CheckCircle2, 
  UserCheck, 
  Workflow, 
  RefreshCw, 
  Sliders
} from 'lucide-react';

const STAGE_STACK = [
  { id: '1-5', label: 'Stages 1–5 Core AI OS', desc: 'Foundation, RAG, Reasoning, Daemons & Enterprise Automation', color: 'border-violet-500/30 text-violet-400 bg-violet-500/10' },
  { id: '6-7', label: 'Stages 6–7 Security & Risk', desc: 'Threat Intelligence, Reverse Engineering & Human Behavior Modeling', color: 'border-indigo-500/30 text-indigo-400 bg-indigo-500/10' },
  { id: '8', label: 'Stage 8 Data Intelligence', desc: 'Heterogeneous Ingestion & Enterprise Knowledge Graphs', color: 'border-cyan-500/30 text-cyan-400 bg-cyan-500/10' },
  { id: '9', label: 'Stage 9 Autonomous Agents', desc: 'Multi-Agent Swarm Orchestration & Tool Execution Loops', color: 'border-purple-500/30 text-purple-400 bg-purple-500/10' },
  { id: '10', label: 'Stage 10 Decision Platform', desc: 'Executive Decision Support, Scenario Analysis & Feedback Loops', color: 'border-emerald-500/50 text-emerald-400 bg-emerald-500/15 shadow-[0_0_20px_rgba(16,185,129,0.25)] font-bold' }
];

const SCENARIOS = [
  {
    id: 'optA',
    name: 'Option A: Accelerated Autonomous Rollout',
    riskLevel: 'MODERATE RISK',
    considerations: 'High deployment velocity with continuous automated rollback monitoring.',
    dependencies: ['Stage 4 Async Daemons', 'Stage 6 Security Sentinel'],
    action: 'Deploy automated deployment pipelines with continuous vector telemetry checks.'
  },
  {
    id: 'optB',
    name: 'Option B: Stage-Gated Human Approval Path',
    riskLevel: 'LOW RISK',
    considerations: 'Mandatory human approval checkpoints attached to all critical workspace API calls.',
    dependencies: ['Stage 7 Human Risk Model', 'Stage 9 Policy Gate'],
    action: 'Route execution streams through human approval checkpoints prior to commit.'
  },
  {
    id: 'optC',
    name: 'Option C: Hybrid Agentic Simulation',
    riskLevel: 'OPTIMIZED BALANCE',
    considerations: 'Simulate scenario outcomes across parallel Optimist vs Skeptic evaluator nodes.',
    dependencies: ['Stage 3 Debate Engine', 'Stage 8 Knowledge Graph'],
    action: 'Run 100-step predictive simulation loop before executing real-world tool actions.'
  }
];

const DECISION_PIPELINE = [
  { step: '01', title: 'Signals', desc: 'Ingests multi-source data' },
  { step: '02', title: 'Context', desc: 'Vector graph correlation' },
  { step: '03', title: 'Reasoning', desc: 'Dual-model debate analysis' },
  { step: '04', title: 'Options', desc: 'Generates scenario paths' },
  { step: '05', title: 'Evaluation', desc: 'Risk & constraint scoring' },
  { step: '06', title: 'Decision', desc: 'Human + AI consensus' },
  { step: '07', title: 'Action', desc: 'Agent tool execution' },
  { step: '08', title: 'Feedback', desc: 'Continuous learning loop ↺' },
];

export default function EnterpriseDecisionIntelligence() {
  const [selectedScenarioId, setSelectedScenarioId] = useState('optB');
  const shouldReduceMotion = useReducedMotion();

  const selectedScenario = SCENARIOS.find(s => s.id === selectedScenarioId) || SCENARIOS[1];

  return (
    <section 
      id="enterprise-decision-intelligence"
      className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10 relative select-none"
    >
      {/* ── Architecture Culmination Stack Banner ── */}
      <div className="mb-16 p-6 rounded-3xl bg-neutral-950/80 border border-white/[0.1] backdrop-blur-2xl shadow-2xl">
        <div className="flex items-center justify-between mb-6 border-b border-white/[0.08] pb-4">
          <span className="text-xs font-mono text-emerald-400 font-bold uppercase tracking-widest flex items-center gap-2">
            <Layers className="w-4 h-4" />
            <span>DOXA ENTERPRISE INTELLIGENCE STAGE PROGRESSION</span>
          </span>
          <span className="text-[10px] font-mono px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 font-bold">
            STAGE 10 CULMINATION
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          {STAGE_STACK.map((stg) => (
            <div key={stg.id} className={`p-4 rounded-2xl border flex flex-col justify-between gap-2 text-xs font-mono ${stg.color}`}>
              <span className="font-bold">{stg.label}</span>
              <span className="text-[10px] text-neutral-400 font-sans leading-tight">{stg.desc}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Section Header */}
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-4">
          <Sparkles className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
          <span className="text-xs font-mono font-semibold text-emerald-300 uppercase tracking-wider">
            STAGE 10: ENTERPRISE DECISION INTELLIGENCE
          </span>
        </div>
        <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          From Intelligence to Better Decisions
        </h2>
        <p className="mt-4 text-base text-neutral-400 max-w-2xl mx-auto font-sans leading-relaxed">
          Doxa brings together enterprise context, retrieval, reasoning, agents, security, and execution to help leadership evaluate scenarios and act with clarity.
        </p>
      </div>

      {/* ── Continuous Decision Pipeline (with Feedback Loop ↺) ── */}
      <div className="mb-16 p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/[0.08] backdrop-blur-2xl shadow-2xl overflow-x-auto hud-scrollbar">
        <div className="flex items-center justify-between mb-6">
          <span className="text-xs font-mono text-cyan-400 font-bold uppercase tracking-widest flex items-center gap-2">
            <Workflow className="w-4 h-4" />
            <span>CONTINUOUS DECISION-TO-ACTION FEEDBACK LOOP</span>
          </span>
          <span className="text-[10px] font-mono px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-300 flex items-center gap-1.5 font-semibold">
            <RefreshCw className="w-3.5 h-3.5 text-cyan-400 animate-spin" />
            <span>CONTINUOUS FEEDBACK LOOP ACTIVE</span>
          </span>
        </div>

        <div className="flex items-center justify-between min-w-[850px] gap-2 relative">
          {DECISION_PIPELINE.map((seq, idx) => (
            <React.Fragment key={idx}>
              <div className={`flex flex-col items-center text-center gap-1.5 p-3 rounded-2xl border transition-all w-28 shrink-0 ${
                idx === 7 ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-white/[0.02] border-white/[0.06] text-white'
              }`}>
                <span className="text-[10px] font-mono text-cyan-400 font-bold">{seq.step}</span>
                <span className="text-xs font-bold font-sans">{seq.title}</span>
                <span className="text-[10px] text-neutral-400 font-mono leading-tight">{seq.desc}</span>
              </div>
              {idx < DECISION_PIPELINE.length - 1 && (
                <ArrowRight className="w-4 h-4 text-emerald-500/50 shrink-0 animate-pulse" />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* ── Interactive Scenario & Decision Evaluator ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-16">
        {/* Left Column: Scenario Options Selector */}
        <div className="lg:col-span-5 flex flex-col gap-3">
          <span className="text-xs font-mono font-bold text-neutral-400 uppercase tracking-wider mb-1 block">
            STRATEGIC SCENARIO ANALYSIS
          </span>
          {SCENARIOS.map((sc) => {
            const isActive = sc.id === selectedScenarioId;
            return (
              <button
                key={sc.id}
                type="button"
                onClick={() => setSelectedScenarioId(sc.id)}
                className={`flex items-center justify-between p-4 rounded-2xl border text-left transition-all duration-300 cursor-pointer ${
                  isActive
                    ? 'bg-neutral-900/90 border-emerald-500/50 shadow-[0_0_25px_rgba(16,185,129,0.25)] text-white'
                    : 'bg-neutral-950/50 border-white/[0.06] hover:bg-neutral-900/40 text-neutral-400 hover:text-neutral-200'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Sliders className={`w-4.5 h-4.5 ${isActive ? 'text-emerald-400' : 'text-neutral-500'}`} />
                  <div>
                    <span className="text-sm font-bold text-white block font-sans">{sc.name}</span>
                    <span className="text-[10px] font-mono text-emerald-400 font-bold block">{sc.riskLevel}</span>
                  </div>
                </div>
                <ArrowRight className={`w-4 h-4 transition-transform duration-200 ${isActive ? 'translate-x-1 text-emerald-400' : 'opacity-30'}`} />
              </button>
            );
          })}
        </div>

        {/* Right Column: Scenario Evaluator Surface */}
        <div className="lg:col-span-7">
          <AnimatePresence mode="wait">
            <motion.div
              key={selectedScenario.id}
              initial={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, x: -20 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
              className="p-6 sm:p-8 rounded-3xl bg-neutral-950/90 border border-white/[0.1] backdrop-blur-2xl shadow-2xl flex flex-col justify-between min-h-[440px]"
            >
              <div>
                <div className="flex items-center justify-between border-b border-white/[0.08] pb-4 mb-6">
                  <div>
                    <span className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest block">
                      SCENARIO EVALUATION ANALYSIS
                    </span>
                    <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                      {selectedScenario.name}
                    </h3>
                  </div>
                  <span className="text-xs font-mono px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 font-bold">
                    {selectedScenario.riskLevel}
                  </span>
                </div>

                <div className="mb-6">
                  <span className="text-xs font-mono font-bold text-neutral-400 uppercase tracking-wider block mb-2">
                    KEY CONSIDERATIONS
                  </span>
                  <p className="text-sm text-neutral-300 font-sans leading-relaxed p-3.5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                    {selectedScenario.considerations}
                  </p>
                </div>

                <div className="mb-6">
                  <span className="text-xs font-mono font-bold text-neutral-400 uppercase tracking-wider block mb-2">
                    CROSS-STAGE DEPENDENCIES
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {selectedScenario.dependencies.map((dep, dIdx) => (
                      <span key={dIdx} className="px-3 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-300 font-medium">
                        {dep}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <span className="text-xs font-mono font-bold text-neutral-400 uppercase tracking-wider block mb-2">
                    RECOMMENDED ACTION PLAN
                  </span>
                  <p className="text-xs font-mono text-neutral-200 p-3.5 rounded-xl bg-neutral-900 border border-white/[0.08] flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>{selectedScenario.action}</span>
                  </p>
                </div>
              </div>

              {/* Human Oversight Model Footer */}
              <div className="pt-4 border-t border-white/[0.08] flex items-center justify-between text-xs font-mono text-neutral-400">
                <span className="flex items-center gap-2 text-cyan-400 font-semibold">
                  <UserCheck className="w-4 h-4" /> HUMAN EXPERTISE ↕ DOXA INTELLIGENCE ↕ ENTERPRISE SYSTEMS
                </span>
                <span className="text-[11px] text-neutral-500 font-bold">DECISION SUPPORT ONLY</span>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}
