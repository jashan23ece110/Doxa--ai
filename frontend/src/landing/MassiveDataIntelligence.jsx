import React, { useState } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { 
  Database, 
  FileText, 
  Globe, 
  Network, 
  Cpu, 
  Layers, 
  ArrowRight, 
  Sparkles, 
  Workflow, 
  Boxes, 
  GitMerge, 
  Zap,
  Share2,
  CheckCircle2
} from 'lucide-react';

const DATA_SOURCES = [
  { id: 'docs', label: 'Unstructured Documents', type: 'PDFs, Markdown, Contracts', icon: FileText, color: 'text-violet-400', desc: 'Dense semantic chunking & vector embedding.' },
  { id: 'dbs', label: 'Structured Databases', type: 'PostgreSQL, SQL, NoSQL', icon: Database, color: 'text-indigo-400', desc: 'Schema-aware SQL query synthesis & entity mapping.' },
  { id: 'apis', label: 'Enterprise APIs', type: 'REST, GraphQL, Webhooks', icon: Globe, color: 'text-cyan-400', desc: 'Dynamic API schema parsing & tool execution.' },
  { id: 'events', label: 'Real-Time Event Streams', type: 'Kafka, WebSockets, Pub/Sub', icon: Zap, color: 'text-purple-400', desc: 'Continuous stream correlation & anomaly detection.' },
  { id: 'systems', label: 'Business Applications', type: 'Workspace, CRM, Issue Trackers', icon: Boxes, color: 'text-emerald-400', desc: 'Unified context aggregation across operational tools.' }
];

const KNOWLEDGE_GRAPH_NODES = [
  { label: 'Entities', desc: 'People, Products, System IDs', icon: Boxes },
  { label: 'Relationships', desc: 'Graph Edges & Cross-References', icon: Share2 },
  { label: 'Context', desc: 'Temporal & Semantic Alignment', icon: GitMerge },
  { label: 'Insights', desc: 'Actionable Intelligence Output', icon: Sparkles }
];

const CAPABILITIES = [
  { title: 'Heterogeneous Ingestion', desc: 'Unifies structured tables, unstructured text, and real-time event telemetry into one vector space.', icon: Database },
  { title: 'Cross-Source Correlation', desc: 'Automatically maps entity relationships across isolated databases, docs, and external APIs.', icon: GitMerge },
  { title: 'Enterprise Knowledge Graphs', desc: 'Builds dynamic, queryable knowledge graphs connecting unstructured facts to business logic.', icon: Network },
  { title: 'Context-Aware Retrieval', desc: 'Retrieves relevant context based on multi-source semantic proximity rather than keyword matches.', icon: Workflow },
  { title: 'Continuous Intelligence', desc: 'Monitors ongoing stream events to keep vector indices and knowledge graphs constantly updated.', icon: Zap },
  { title: 'Agent-Ready Context Delivery', desc: 'Delivers structured, citation-backed context directly to autonomous agent execution loops.', icon: Cpu }
];

export default function MassiveDataIntelligence() {
  const [activeSourceId, setActiveSourceId] = useState('docs');
  const shouldReduceMotion = useReducedMotion();

  const activeSource = DATA_SOURCES.find(s => s.id === activeSourceId) || DATA_SOURCES[0];

  return (
    <section 
      id="massive-data-intelligence"
      className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10 relative select-none"
    >
      {/* ── Architecture Bridge Banner ── */}
      <div className="mb-16 p-4 sm:p-6 rounded-2xl bg-neutral-950/60 border border-white/[0.08] backdrop-blur-xl flex flex-wrap items-center justify-between gap-4 text-xs font-mono text-neutral-400">
        <div className="flex items-center gap-2 text-violet-400 font-bold">
          <Layers className="w-4 h-4" />
          <span className="uppercase tracking-wider">STAGE 8 EXTENSION</span>
        </div>
        <div className="flex flex-wrap items-center gap-2 text-[11px]">
          <span className="px-2.5 py-1 rounded bg-white/[0.04] text-neutral-300">Stages 1–5 Core AI OS</span>
          <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
          <span className="px-2.5 py-1 rounded bg-white/[0.04] text-neutral-300">Stages 6–7 Security & Human Risk</span>
          <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
          <span className="px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 font-bold border border-purple-500/30">Stage 8 Data Intelligence</span>
        </div>
      </div>

      {/* Section Header */}
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-purple-500/10 border border-purple-500/20 mb-4">
          <Database className="w-3.5 h-3.5 text-purple-400" />
          <span className="text-xs font-mono font-semibold text-purple-300 uppercase tracking-wider">
            STAGE 8: MASSIVE-SCALE DATA INTELLIGENCE
          </span>
        </div>
        <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          Turn Enterprise Data into Usable Intelligence
        </h2>
        <p className="mt-4 text-base text-neutral-400 max-w-2xl mx-auto font-sans leading-relaxed">
          Doxa connects structured and unstructured information across heterogeneous sources, building context graphs that empower autonomous agents and enterprise decisions.
        </p>
      </div>

      {/* ── Visual Data Flow Pipeline (Data → Context → Correlation → Intelligence → Action) ── */}
      <div className="mb-16 p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/[0.08] backdrop-blur-2xl shadow-2xl overflow-x-auto hud-scrollbar">
        <div className="flex items-center justify-between mb-6">
          <span className="text-xs font-mono text-cyan-400 font-bold uppercase tracking-widest flex items-center gap-2">
            <Workflow className="w-4 h-4" />
            <span>ENTERPRISE DATA CONTEXTUALIZATION PIPELINE</span>
          </span>
          <span className="text-[10px] font-mono px-3 py-1 rounded-full bg-white/[0.04] border border-white/[0.08] text-neutral-400">
            HETEROGENEOUS SOURCE AGGREGATION
          </span>
        </div>

        {/* 5-Step Pipeline Flow */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative min-w-[650px]">
          {[
            { step: '01', title: 'Data', desc: 'Ingests docs, DBs & APIs' },
            { step: '02', title: 'Context', desc: 'Semantic chunking & vector indexing' },
            { step: '03', title: 'Correlation', desc: 'Cross-source entity graph mapping' },
            { step: '04', title: 'Intelligence', desc: 'Multi-source factual synthesis' },
            { step: '05', title: 'Action', desc: 'Agent execution & workflow sync' },
          ].map((st, idx) => (
            <div key={idx} className="flex flex-col items-center text-center p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] hover:border-purple-500/40 transition-all">
              <span className="text-[10px] font-mono text-purple-400 font-bold">LIFECYCLE {st.step}</span>
              <span className="text-sm font-bold text-white font-sans mt-1">{st.title}</span>
              <span className="text-[11px] text-neutral-400 font-sans mt-1 leading-snug">{st.desc}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ── Interactive Data Sources & Knowledge Graph Explorer ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-16">
        {/* Left Column: Data Sources Picker */}
        <div className="lg:col-span-5 flex flex-col gap-3">
          <span className="text-xs font-mono font-bold text-neutral-400 uppercase tracking-wider mb-1 block">
            HETEROGENEOUS DATA SOURCES
          </span>
          {DATA_SOURCES.map((src) => {
            const isActive = src.id === activeSourceId;
            const Icon = src.icon;
            return (
              <button
                key={src.id}
                type="button"
                onClick={() => setActiveSourceId(src.id)}
                className={`flex items-center justify-between p-4 rounded-2xl border text-left transition-all duration-300 cursor-pointer ${
                  isActive
                    ? 'bg-neutral-900/90 border-purple-500/50 shadow-[0_0_25px_rgba(168,85,247,0.25)] text-white'
                    : 'bg-neutral-950/50 border-white/[0.06] hover:bg-neutral-900/40 text-neutral-400 hover:text-neutral-200'
                }`}
              >
                <div className="flex items-center gap-3.5">
                  <div className={`p-2.5 rounded-xl border flex items-center justify-center shrink-0 ${
                    isActive ? 'bg-purple-500/20 border-purple-500/40 text-cyan-300' : 'bg-white/[0.03] border-white/[0.08] text-neutral-400'
                  }`}>
                    <Icon className="w-4.5 h-4.5" />
                  </div>
                  <div>
                    <span className="text-sm font-bold text-white block font-sans">{src.label}</span>
                    <span className="text-[11px] text-neutral-400 font-mono block">{src.type}</span>
                  </div>
                </div>
                <ArrowRight className={`w-4 h-4 transition-transform duration-200 ${isActive ? 'translate-x-1 text-cyan-400' : 'opacity-30'}`} />
              </button>
            );
          })}
        </div>

        {/* Right Column: Knowledge Graph Detail Surface */}
        <div className="lg:col-span-7">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeSource.id}
              initial={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, x: -20 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
              className="p-6 sm:p-8 rounded-3xl bg-neutral-950/90 border border-white/[0.1] backdrop-blur-2xl shadow-2xl flex flex-col justify-between min-h-[440px]"
            >
              <div>
                <div className="flex items-center justify-between border-b border-white/[0.08] pb-4 mb-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 rounded-xl bg-purple-500/15 border border-purple-500/30 text-cyan-300">
                      <activeSource.icon className="w-5 h-5" />
                    </div>
                    <div>
                      <span className="text-xs font-mono font-bold text-purple-400 uppercase tracking-widest block">
                        SOURCE CONNECTOR ACTIVE
                      </span>
                      <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                        {activeSource.label}
                      </h3>
                    </div>
                  </div>
                  <span className="text-xs font-mono px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 font-semibold">
                    KNOWLEDGE GRAPH INTEGRATED
                  </span>
                </div>

                <p className="text-sm text-neutral-300 font-sans leading-relaxed mb-6">
                  {activeSource.desc} Doxa parses raw information into normalized vector entities and connects them across enterprise knowledge graphs.
                </p>

                {/* Knowledge Graph Nodes Visualization */}
                <div className="mb-6">
                  <span className="text-xs font-mono font-bold text-neutral-400 uppercase tracking-wider block mb-3">
                    KNOWLEDGE GRAPH CONNECTIONS
                  </span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {KNOWLEDGE_GRAPH_NODES.map((node, nIdx) => {
                      const NodeIcon = node.icon;
                      return (
                        <div key={nIdx} className="p-3.5 rounded-xl bg-white/[0.02] border border-white/[0.06] flex items-center gap-3 text-xs">
                          <div className="p-2 rounded-lg bg-purple-500/10 border border-purple-500/20 text-cyan-300 shrink-0">
                            <NodeIcon className="w-4 h-4" />
                          </div>
                          <div>
                            <span className="font-bold text-white block font-sans">{node.label}</span>
                            <span className="text-[10px] text-neutral-400 font-mono block">{node.desc}</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-white/[0.08] flex items-center justify-between text-xs font-mono text-neutral-400">
                <span className="flex items-center gap-2 text-cyan-400 font-semibold">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" /> UNIFIED CONTEXT CORRELATION
                </span>
                <span className="text-[11px] text-neutral-500">DYNAMIC INDEXING ACTIVE</span>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      {/* ── 6 Core Data Capabilities Grid ── */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {CAPABILITIES.map((cap, cIdx) => {
          const Icon = cap.icon;
          return (
            <motion.div
              key={cIdx}
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-50px' }}
              transition={{ duration: 0.4, delay: cIdx * 0.08 }}
              className="p-6 rounded-3xl bg-neutral-950/80 border border-white/[0.08] backdrop-blur-2xl flex flex-col justify-between gap-4 shadow-2xl transition-all duration-300 hover:border-purple-500/40 hover:-translate-y-1 group"
            >
              <div className="flex items-center justify-between">
                <div className="p-3 rounded-2xl bg-purple-500/10 border border-purple-500/20 text-cyan-300 group-hover:scale-105 transition-transform">
                  <Icon className="w-5 h-5" />
                </div>
                <CheckCircle2 className="w-4 h-4 text-emerald-400 opacity-60" />
              </div>

              <div className="flex flex-col gap-2">
                <h3 className="text-lg font-bold text-white font-sans tracking-tight">
                  {cap.title}
                </h3>
                <p className="text-xs text-neutral-400 leading-relaxed font-sans">
                  {cap.desc}
                </p>
              </div>
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}
