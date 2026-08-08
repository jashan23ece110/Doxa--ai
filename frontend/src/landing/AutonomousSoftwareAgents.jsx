import React, { useState } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { 
  Bot, 
  Search, 
  Cpu, 
  Play, 
  ShieldCheck, 
  UserCheck, 
  Layers, 
  ArrowRight, 
  CheckCircle2, 
  Sparkles, 
  Terminal, 
  Workflow, 
  GitBranch,
  Activity,
  Lock
} from 'lucide-react';

const AGENT_NODES = [
  {
    id: 'research',
    role: 'Research Agent',
    type: 'DATA & RAG',
    desc: 'Queries vector stores and live web search to gather grounded factual context.',
    icon: Search,
    color: 'from-violet-500 to-indigo-600',
    accentColor: '#8b5cf6',
    status: 'ACTIVE',
    tools: ['ChromaDB Vectors', 'Tavily Search', 'Document Chunking']
  },
  {
    id: 'analysis',
    role: 'Analysis Agent',
    type: 'COGNITIVE EVAL',
    desc: 'Evaluates hypotheses, runs Optimist vs Skeptic debate, and identifies edge cases.',
    icon: Cpu,
    color: 'from-indigo-500 to-cyan-500',
    accentColor: '#6366f1',
    status: 'DEBATING',
    tools: ['Optimist Core', 'Skeptic Core', 'Consensus Engine']
  },
  {
    id: 'planning',
    role: 'Planning Agent',
    type: 'ORCHESTRATION',
    desc: 'Deconstructs complex goals into optimal multi-step tool execution graphs.',
    icon: Workflow,
    color: 'from-cyan-500 to-teal-400',
    accentColor: '#06b6d4',
    status: 'PLANNING',
    tools: ['Task Decomposer', 'Dependency Graph', 'Tool Router']
  },
  {
    id: 'action',
    role: 'Action Agent',
    type: 'TOOL EXECUTION',
    desc: 'Invokes external workspace APIs, runs scripts, and streams response tokens.',
    icon: Play,
    color: 'from-purple-500 to-violet-500',
    accentColor: '#a855f7',
    status: 'EXECUTING',
    tools: ['Workspace Gateway', 'Token Streamer', 'API Connector']
  },
  {
    id: 'verification',
    role: 'Verification Agent',
    type: 'SECURITY & GOVERNANCE',
    desc: 'Verifies output against policy rules, PII filters, and human approval gates.',
    icon: ShieldCheck,
    color: 'from-emerald-500 to-teal-500',
    accentColor: '#10b981',
    status: 'VERIFYING',
    tools: ['Policy Sentinel', 'PII Masking', 'Audit Logger']
  }
];

const EXECUTION_SEQUENCE = [
  { step: '01', title: 'Intent Received', desc: 'Goal parsed by Doxa Orchestrator' },
  { step: '02', title: 'Context Gathered', desc: 'Research agent queries vectors & web' },
  { step: '03', title: 'Task Decomposed', desc: 'Planning agent maps dependencies' },
  { step: '04', title: 'Agents Assigned', desc: 'Sub-tasks delegated to worker agents' },
  { step: '05', title: 'Tools Executed', desc: 'Action agent executes workspace APIs' },
  { step: '06', title: 'Human Checkpoint', desc: 'Policy gate evaluates approval' },
  { step: '07', title: 'Verified Result', desc: 'Citation-backed outcome delivered' },
];

export default function AutonomousSoftwareAgents() {
  const [activeAgentId, setActiveAgentId] = useState('research');
  const shouldReduceMotion = useReducedMotion();

  const activeAgent = AGENT_NODES.find(a => a.id === activeAgentId) || AGENT_NODES[0];

  return (
    <section 
      id="autonomous-software-agents"
      className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10 relative select-none"
    >
      {/* ── Architecture Bridge Banner ── */}
      <div className="mb-16 p-4 sm:p-6 rounded-2xl bg-neutral-950/60 border border-white/[0.08] backdrop-blur-xl flex flex-wrap items-center justify-between gap-4 text-xs font-mono text-neutral-400">
        <div className="flex items-center gap-2 text-violet-400 font-bold">
          <Layers className="w-4 h-4" />
          <span className="uppercase tracking-wider">STAGE 9 CULMINATION</span>
        </div>
        <div className="flex flex-wrap items-center gap-2 text-[11px]">
          <span className="px-2.5 py-1 rounded bg-white/[0.04] text-neutral-300">Stages 1–5 Core AI OS</span>
          <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
          <span className="px-2.5 py-1 rounded bg-white/[0.04] text-neutral-300">Stages 6–7 Security & Risk</span>
          <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
          <span className="px-2.5 py-1 rounded bg-white/[0.04] text-neutral-300">Stage 8 Data Intelligence</span>
          <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
          <span className="px-2.5 py-1 rounded bg-violet-500/20 text-cyan-300 font-bold border border-violet-500/30">Stage 9 Autonomous Software Agents</span>
        </div>
      </div>

      {/* Section Header */}
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-violet-500/10 border border-violet-500/20 mb-4">
          <Bot className="w-3.5 h-3.5 text-violet-400" />
          <span className="text-xs font-mono font-semibold text-violet-300 uppercase tracking-wider">
            STAGE 9: AUTONOMOUS SOFTWARE AGENTS
          </span>
        </div>
        <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          From Intelligence to Execution
        </h2>
        <p className="mt-4 text-base text-neutral-400 max-w-2xl mx-auto font-sans leading-relaxed">
          Doxa coordinates specialized agent roles, contextual memory, and workspace tools to transform complex enterprise goals into verified outcomes under strict human oversight.
        </p>
      </div>

      {/* ── Agentic Execution Sequence Pipeline ── */}
      <div className="mb-16 p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/[0.08] backdrop-blur-2xl shadow-2xl overflow-x-auto hud-scrollbar">
        <div className="flex items-center justify-between mb-6">
          <span className="text-xs font-mono text-cyan-400 font-bold uppercase tracking-widest flex items-center gap-2">
            <Activity className="w-4 h-4" />
            <span>AGENTIC WORKFLOW ORCHESTRATION PIPELINE</span>
          </span>
          <span className="text-[10px] font-mono px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center gap-1.5 font-semibold">
            <UserCheck className="w-3.5 h-3.5" />
            <span>HUMAN-IN-THE-LOOP CONTROLS ACTIVE</span>
          </span>
        </div>

        <div className="flex items-center justify-between min-w-[800px] gap-2 relative">
          {EXECUTION_SEQUENCE.map((seq, idx) => (
            <React.Fragment key={idx}>
              <div className="flex flex-col items-center text-center gap-1.5 p-3 rounded-2xl bg-white/[0.02] border border-white/[0.06] hover:border-violet-500/40 transition-all w-28 shrink-0">
                <span className="text-[10px] font-mono text-cyan-400 font-bold">{seq.step}</span>
                <span className="text-xs font-bold text-white font-sans">{seq.title}</span>
                <span className="text-[10px] text-neutral-500 font-mono leading-tight">{seq.desc}</span>
              </div>
              {idx < EXECUTION_SEQUENCE.length - 1 && (
                <ArrowRight className="w-4 h-4 text-violet-500/50 shrink-0 animate-pulse" />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* ── Interactive Agent Swarm Architecture ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-16">
        {/* Left Column: Agent Node Picker */}
        <div className="lg:col-span-5 flex flex-col gap-3">
          <span className="text-xs font-mono font-bold text-neutral-400 uppercase tracking-wider mb-1 block">
            SPECIALIZED AGENT SWARM
          </span>
          {AGENT_NODES.map((ag) => {
            const isActive = ag.id === activeAgentId;
            const Icon = ag.icon;
            return (
              <button
                key={ag.id}
                type="button"
                onClick={() => setActiveAgentId(ag.id)}
                className={`flex items-center justify-between p-4 rounded-2xl border text-left transition-all duration-300 cursor-pointer ${
                  isActive
                    ? 'bg-neutral-900/90 border-violet-500/50 shadow-[0_0_25px_rgba(124,58,237,0.25)] text-white'
                    : 'bg-neutral-950/50 border-white/[0.06] hover:bg-neutral-900/40 text-neutral-400 hover:text-neutral-200'
                }`}
              >
                <div className="flex items-center gap-3.5">
                  <div className={`p-2.5 rounded-xl border flex items-center justify-center shrink-0 ${
                    isActive ? 'bg-violet-500/20 border-violet-500/40 text-cyan-300' : 'bg-white/[0.03] border-white/[0.08] text-neutral-400'
                  }`}>
                    <Icon className="w-4.5 h-4.5" />
                  </div>
                  <div>
                    <span className="text-sm font-bold text-white block font-sans">{ag.role}</span>
                    <span className="text-[11px] text-neutral-400 font-mono block">{ag.type}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-bold">
                    {ag.status}
                  </span>
                  <ArrowRight className={`w-4 h-4 transition-transform duration-200 ${isActive ? 'translate-x-1 text-cyan-400' : 'opacity-30'}`} />
                </div>
              </button>
            );
          })}
        </div>

        {/* Right Column: Agent Node Inspector */}
        <div className="lg:col-span-7">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeAgent.id}
              initial={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, x: -20 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
              className="p-6 sm:p-8 rounded-3xl bg-neutral-950/90 border border-white/[0.1] backdrop-blur-2xl shadow-2xl flex flex-col justify-between min-h-[440px]"
            >
              <div>
                <div className="flex items-center justify-between border-b border-white/[0.08] pb-4 mb-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 rounded-xl bg-violet-500/15 border border-violet-500/30 text-cyan-300">
                      <activeAgent.icon className="w-5 h-5" />
                    </div>
                    <div>
                      <span className="text-xs font-mono font-bold text-violet-400 uppercase tracking-widest block">
                        AGENT NODE STATE
                      </span>
                      <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                        {activeAgent.role}
                      </h3>
                    </div>
                  </div>
                  <span className="text-xs font-mono px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-300 font-semibold flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
                    {activeAgent.status}
                  </span>
                </div>

                <p className="text-sm text-neutral-300 font-sans leading-relaxed mb-6">
                  {activeAgent.desc} Operating as a specialized autonomous node under the Doxa Orchestrator kernel.
                </p>

                {/* Agent Tool Integrations */}
                <div className="mb-6">
                  <span className="text-xs font-mono font-bold text-neutral-400 uppercase tracking-wider block mb-3">
                    INTEGRATED AGENT TOOLS
                  </span>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    {activeAgent.tools.map((t, tIdx) => (
                      <div key={tIdx} className="p-3 rounded-xl bg-white/[0.02] border border-white/[0.06] text-xs font-mono text-neutral-200 flex items-center gap-2">
                        <Terminal className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                        <span className="truncate">{t}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Human Oversight Control Footer */}
              <div className="pt-4 border-t border-white/[0.08] flex items-center justify-between text-xs font-mono text-neutral-400">
                <span className="flex items-center gap-2 text-emerald-400 font-semibold">
                  <UserCheck className="w-4 h-4" /> HUMAN APPROVAL CHECKPOINT ATTACHED
                </span>
                <span className="flex items-center gap-1 text-neutral-500">
                  <Lock className="w-3.5 h-3.5 text-neutral-400" /> POLICY PROTECTED
                </span>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}
