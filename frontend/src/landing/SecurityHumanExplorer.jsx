import React, { useState } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { 
  ShieldAlert, 
  Users, 
  Terminal, 
  Search, 
  Cpu, 
  Network, 
  Lock, 
  ArrowRight, 
  CheckCircle2, 
  FileCode2, 
  Activity, 
  Layers,
  Sparkles,
  Eye,
  AlertTriangle
} from 'lucide-react';

const STAGE_6_CAPABILITIES = [
  { title: 'Malware Threat Intelligence', desc: 'Authorized analysis of binary behavioral signatures, memory artifacts, and threat indicators.', icon: Terminal },
  { title: 'Binary Reverse Engineering', desc: 'Disassembly and control-flow analysis for authorized security research.', icon: FileCode2 },
  { title: 'Digital Forensics & IR', desc: 'Incident response telemetry parsing, log correlation, and forensic artifact extraction.', icon: Search },
  { title: 'Defensive Simulation', desc: 'Automated red-team attack scenarios to stress-test enterprise security perimeters.', icon: ShieldAlert },
  { title: 'Threat Vector Analysis', desc: 'Correlating vulnerabilities across distributed endpoints and cloud infrastructure.', icon: Network },
  { title: 'Automated Remediation', desc: 'Orchestrating rapid isolation policies and defensive patching workflows.', icon: Lock }
];

const STAGE_7_CAPABILITIES = [
  { title: 'Influence Analysis', desc: 'Evaluating communication patterns and organizational influence networks for risk modeling.', icon: Network },
  { title: 'Probabilistic Behavior Modeling', desc: 'Context-aware analytics for detecting anomalous access patterns and potential insider risks.', icon: Eye },
  { title: 'Insider Risk Detection', desc: 'Privacy-conscious risk scoring based on behavioral telemetry and access anomalies.', icon: AlertTriangle },
  { title: 'Defensive Social Engineering', desc: 'Simulated phishing and credential awareness exercises for employee resilience.', icon: Users },
  { title: 'Security Awareness Intelligence', desc: 'Adaptive training suggestions tailored to individual role vulnerability profiles.', icon: Sparkles },
  { title: 'Red-Team Human Simulations', desc: 'End-to-end human factor stress testing for organizational resilience.', icon: Activity }
];

const SEC_FLOW = [
  { step: '01', title: 'Telemetry', desc: 'Ingests endpoint & network events' },
  { step: '02', title: 'Threat Detection', desc: 'Identifies behavioral anomalies' },
  { step: '03', title: 'Analysis', desc: 'Parses malware & disassembly' },
  { step: '04', title: 'Correlation', desc: 'Maps indicators to MITRE ATT&CK' },
  { step: '05', title: 'Investigation', desc: 'Synthesizes forensic timeline' },
  { step: '06', title: 'Defensive Response', desc: 'Triggers containment policies' },
];

const HUMAN_FLOW = [
  { step: '01', title: 'Signals', desc: 'Collects privacy-safe telemetry' },
  { step: '02', title: 'Behavioral Patterns', desc: 'Models baseline interactions' },
  { step: '03', title: 'Risk Indicators', desc: 'Flags access anomalies' },
  { step: '04', title: 'Context Analysis', desc: 'Correlates role & intent' },
  { step: '05', title: 'Org Insight', desc: 'Generates risk heatmaps' },
  { step: '06', title: 'Defensive Action', desc: 'Deploys adaptive training' },
];

export default function SecurityHumanExplorer() {
  const [activeTab, setActiveTab] = useState('stage6'); // 'stage6' | 'stage7'
  const shouldReduceMotion = useReducedMotion();

  const isStage6 = activeTab === 'stage6';
  const capabilities = isStage6 ? STAGE_6_CAPABILITIES : STAGE_7_CAPABILITIES;
  const flowSteps = isStage6 ? SEC_FLOW : HUMAN_FLOW;

  return (
    <section 
      id="security-human-intelligence"
      className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10 relative select-none"
    >
      {/* ── Architecture Bridge Connection Banner ── */}
      <div className="mb-16 p-4 sm:p-6 rounded-2xl bg-neutral-950/60 border border-white/[0.08] backdrop-blur-xl flex flex-wrap items-center justify-between gap-4 text-xs font-mono text-neutral-400">
        <div className="flex items-center gap-2 text-violet-400 font-bold">
          <Layers className="w-4 h-4" />
          <span className="uppercase tracking-wider">INTELLIGENCE EXTENSION</span>
        </div>
        <div className="flex flex-wrap items-center gap-2 text-[11px]">
          <span className="px-2.5 py-1 rounded bg-white/[0.04] text-neutral-300">Stages 1–5 Core AI OS</span>
          <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
          <span className="px-2.5 py-1 rounded bg-violet-500/20 text-cyan-300 font-bold border border-violet-500/30">Stage 6 Security Intelligence</span>
          <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
          <span className="px-2.5 py-1 rounded bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/30">Stage 7 Human Intelligence</span>
        </div>
      </div>

      {/* Section Header */}
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 mb-4">
          <ShieldAlert className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-xs font-mono font-semibold text-cyan-300 uppercase tracking-wider">
            ADVANCED ENTERPRISE DEFENSE & RISK LAYERS
          </span>
        </div>
        <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          Cybersecurity & Human Intelligence
        </h2>
        <p className="mt-4 text-base text-neutral-400 max-w-2xl mx-auto font-sans leading-relaxed">
          Extending Doxa’s cognitive reasoning core with authorized security research, malware threat analysis, and privacy-first behavioral risk modeling.
        </p>
      </div>

      {/* ── Interactive Stage Switcher Tabs ── */}
      <div className="flex justify-center mb-12">
        <div className="inline-flex p-1.5 rounded-2xl bg-neutral-950/90 border border-white/[0.1] backdrop-blur-2xl">
          <button
            type="button"
            onClick={() => setActiveTab('stage6')}
            className={`flex items-center gap-2.5 px-6 py-3 rounded-xl text-xs font-bold transition-all duration-300 cursor-pointer ${
              isStage6
                ? 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-[0_0_20px_rgba(124,58,237,0.4)]'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            <ShieldAlert className="w-4 h-4 text-cyan-300" />
            <span className="font-mono uppercase tracking-wider">STAGE 6: CYBERSECURITY</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('stage7')}
            className={`flex items-center gap-2.5 px-6 py-3 rounded-xl text-xs font-bold transition-all duration-300 cursor-pointer ${
              !isStage6
                ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-[0_0_20px_rgba(6,182,212,0.4)]'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            <Users className="w-4 h-4 text-cyan-300" />
            <span className="font-mono uppercase tracking-wider">STAGE 7: HUMAN INTELLIGENCE</span>
          </button>
        </div>
      </div>

      {/* ── Dynamic Stage Content View ── */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          exit={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, y: -15 }}
          transition={{ duration: 0.35, ease: 'easeOut' }}
          className="flex flex-col gap-12"
        >
          {/* Conceptual Intelligence Pipeline Diagram */}
          <div className="p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/[0.08] backdrop-blur-2xl shadow-2xl overflow-x-auto hud-scrollbar">
            <div className="flex items-center justify-between mb-6">
              <span className="text-xs font-mono text-cyan-400 font-bold uppercase tracking-widest flex items-center gap-2">
                <Cpu className="w-4 h-4" />
                <span>{isStage6 ? 'DEFENSIVE THREAT ANALYSIS PIPELINE' : 'HUMAN BEHAVIORAL RISK PIPELINE'}</span>
              </span>
              <span className="text-[10px] font-mono px-3 py-1 rounded-full bg-white/[0.04] border border-white/[0.08] text-neutral-400">
                {isStage6 ? 'AUTHORIZED DEFENSIVE OPERATIONS' : 'PRIVACY-SAFE RISK MODELING'}
              </span>
            </div>

            <div className="flex items-center justify-between min-w-[700px] gap-2 relative">
              {flowSteps.map((step, idx) => (
                <React.Fragment key={idx}>
                  <div className="flex flex-col items-center text-center gap-1.5 p-3.5 rounded-2xl bg-white/[0.02] border border-white/[0.06] hover:border-cyan-500/40 transition-all w-28 shrink-0">
                    <span className="text-[10px] font-mono text-cyan-400 font-bold">{step.step}</span>
                    <span className="text-xs font-bold text-white font-sans">{step.title}</span>
                    <span className="text-[10px] text-neutral-500 font-mono leading-tight">{step.desc}</span>
                  </div>
                  {idx < flowSteps.length - 1 && (
                    <ArrowRight className="w-4 h-4 text-violet-500/50 shrink-0 animate-pulse" />
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>

          {/* Capabilities Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {capabilities.map((cap, cIdx) => {
              const Icon = cap.icon;
              return (
                <motion.div
                  key={cIdx}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: cIdx * 0.08 }}
                  className="p-6 rounded-3xl bg-neutral-950/80 border border-white/[0.08] backdrop-blur-2xl flex flex-col justify-between gap-4 shadow-2xl transition-all duration-300 hover:border-violet-500/40 hover:-translate-y-1 group"
                >
                  <div className="flex items-center justify-between">
                    <div className="p-3 rounded-2xl bg-violet-500/10 border border-violet-500/20 text-cyan-400 group-hover:scale-105 transition-transform">
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
        </motion.div>
      </AnimatePresence>
    </section>
  );
}
