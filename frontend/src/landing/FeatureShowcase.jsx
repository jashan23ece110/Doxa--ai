import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Cpu, 
  Database, 
  Globe, 
  Zap, 
  Mic, 
  ShieldCheck, 
  GitBranch, 
  Sparkles, 
  Clock, 
  Calendar, 
  Languages, 
  CheckCircle2, 
  ArrowUpRight,
  ArrowRight,
  Play,
  Layers,
  Terminal,
  Activity,
  Volume2
} from 'lucide-react';

const FEATURES = [
  {
    id: 'agent',
    title: 'Autonomous Agent Loop',
    headline: 'Multi-Step Planning, Tool Orchestration & Action',
    desc: 'Doxa doesn’t just answer questions — it formulates execution plans, invokes external search and document tools, evaluates its own intermediate results, and synthesizes accurate final answers.',
    badges: ['Multi-Step Planning', 'Tool Execution', 'Self-Critique'],
    icon: Cpu,
    color: 'from-violet-500 to-indigo-600',
    type: 'agent'
  },
  {
    id: 'rag',
    title: 'RAG-Powered Knowledge Base',
    headline: 'Instant Semantic Intelligence Over Your Documents',
    desc: 'Upload PDFs, text documents, or markdown files. Doxa chunks, embeds, and indexes your data into persistent vector storage using cosine similarity for context-grounded answers.',
    badges: ['ChromaDB Vectors', 'Cosine Similarity', 'Zero Hallucinations'],
    icon: Database,
    color: 'from-indigo-500 to-cyan-500',
    type: 'rag'
  },
  {
    id: 'search',
    title: 'Live Web Search',
    headline: 'Real-Time Grounded Web Intelligence via Tavily',
    desc: 'Access real-time web info. Doxa autonomously queries search APIs, parses live web pages, extracts context, and returns answers backed by citations.',
    badges: ['Live Citations', 'Real-Time Web', 'Source Extraction'],
    icon: Globe,
    color: 'from-cyan-500 to-emerald-500',
    type: 'search'
  },
  {
    id: 'streaming',
    title: 'Real-Time Streaming Responses',
    headline: 'Sub-50ms Low-Latency Continuous Token Stream',
    desc: 'Experience instant response generation. Tokens stream directly from the model to your screen in real time with polling fallback support.',
    badges: ['Sub-50ms Stream', 'Real-Time Tokens', 'Zero Waiting'],
    icon: Zap,
    color: 'from-amber-500 to-orange-500',
    type: 'streaming'
  },
  {
    id: 'voice',
    title: 'Native Voice Mode',
    headline: 'Hands-Free Wake-Word Listener & Speech Synthesis',
    desc: 'Speak naturally to Doxa. Powered by continuous Web Speech API wake-phrase detection and natural text-to-speech voice synthesis.',
    badges: ['Hands-Free Wake Phrase', 'Speech Recognition', 'TTS Audio'],
    icon: Mic,
    color: 'from-rose-500 to-pink-500',
    type: 'voice'
  },
  {
    id: 'debate',
    title: 'Multi-Model Debate Engine',
    headline: 'Dual-Core Optimist vs Skeptic Counter-Arguments',
    desc: 'Eliminate single-model bias. Doxa spawns parallel Optimist and Skeptic evaluator instances that critique hypotheses before delivering a consensus verdict.',
    badges: ['Dual Perspective', 'Fact Verification', 'Consensus Synthesis'],
    icon: ShieldCheck,
    color: 'from-purple-500 to-violet-600',
    type: 'debate'
  },
  {
    id: 'branching',
    title: 'Sessions & Timeline Branching',
    headline: 'Non-Linear Conversational History & Thread Forking',
    desc: 'Explore alternative problem-solving paths. Fork any message in a conversation to create a new timeline branch without losing original context.',
    badges: ['Thread Forking', 'Time-Travel Switcher', 'Session Storage'],
    icon: GitBranch,
    color: 'from-blue-500 to-indigo-600',
    type: 'branching'
  },
  {
    id: 'suggestions',
    title: 'Proactive Suggestions',
    headline: 'Context-Aware Anticipatory Prompt Generation',
    desc: 'Doxa analyzes previous message turns to suggest relevant follow-up questions and next logical steps before you even type them.',
    badges: ['Anticipatory AI', '1-Click Prompts', 'Smart Recommendations'],
    icon: Sparkles,
    color: 'from-teal-500 to-cyan-500',
    type: 'suggestions'
  },
  {
    id: 'timers',
    title: 'Timers & Reminders',
    headline: 'Autonomous Reminders & Background Task Scheduling',
    desc: 'Set timers and background execution schedules. Doxa runs background polling daemons and notifies you when tasks complete.',
    badges: ['Background Daemons', 'Timed Reminders', 'Async Execution'],
    icon: Clock,
    color: 'from-amber-400 to-yellow-500',
    type: 'timers'
  },
  {
    id: 'calendar',
    title: 'Calendar & Workspace Sync',
    headline: 'Productivity Workflow & Event Management',
    desc: 'Create, query, and manage calendar events directly through natural conversational goals integrated with your daily schedule.',
    badges: ['Event Management', 'Workflow Automation', 'Schedule Sync'],
    icon: Calendar,
    color: 'from-emerald-400 to-teal-500',
    type: 'calendar'
  },
  {
    id: 'hinglish',
    title: 'Bilingual Language Engine',
    headline: 'Fluid Toggle Between English & Hinglish',
    desc: 'Communicate in standard English or natural conversational Hinglish. Doxa adapts its prompt synthesis and response tone automatically.',
    badges: ['English Mode', 'Hinglish Mode', 'Tone Adaptation'],
    icon: Languages,
    color: 'from-fuchsia-500 to-pink-600',
    type: 'hinglish'
  }
];

function RenderFeatureVisual({ type }) {
  const [streamText, setStreamText] = useState('Doxa is synthesizing autonomous reasoning tokens...');
  const [hinglishText, setHinglishText] = useState('English Mode Active');

  useEffect(() => {
    if (type === 'streaming') {
      const interval = setInterval(() => {
        setStreamText(prev => prev.length > 50 ? 'Doxa is analyzing...' : prev + ' ⚡ verified chunk');
      }, 1200);
      return () => clearInterval(interval);
    }
    if (type === 'hinglish') {
      const interval = setInterval(() => {
        setHinglishText(prev => prev === 'English Mode Active' ? 'Hinglish Mode: Doxa tension mat le, sab handle kar lega!' : 'English Mode Active');
      }, 2500);
      return () => clearInterval(interval);
    }
  }, [type]);

  switch (type) {
    case 'agent':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-violet-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl group">
          <div className="flex items-center justify-between text-xs font-mono text-violet-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <Terminal className="w-4 h-4 text-violet-400" /> REASONING_LOOP // ACTIVE
            </span>
            <span className="flex items-center gap-1.5 text-emerald-400 font-semibold animate-pulse">
              <span className="w-2 h-2 rounded-full bg-emerald-400" /> EXECUTING
            </span>
          </div>

          <div className="flex flex-col gap-3 my-auto">
            <div className="p-3.5 rounded-2xl bg-violet-500/10 border border-violet-500/30 text-white text-xs font-mono flex items-center justify-between shadow-md">
              <span className="flex items-center gap-2.5">
                <CheckCircle2 className="w-4.5 h-4.5 text-emerald-400 shrink-0" /> 1. Query vector database & web search
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">DONE</span>
            </div>
            <div className="p-3.5 rounded-2xl bg-cyan-500/10 border border-cyan-500/40 text-cyan-200 text-xs font-mono flex items-center justify-between shadow-lg animate-pulse">
              <span className="flex items-center gap-2.5 font-semibold">
                <Cpu className="w-4.5 h-4.5 text-cyan-400 animate-spin shrink-0" /> 2. Synthesize multi-source reasoning
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-bold">RUNNING</span>
            </div>
            <div className="p-3.5 rounded-2xl bg-neutral-900/80 border border-neutral-800 text-neutral-500 text-xs font-mono flex items-center justify-between">
              <span>3. Format final answer & citations</span>
              <span className="text-[10px] px-2 py-0.5 rounded bg-neutral-800 text-neutral-400">PENDING</span>
            </div>
          </div>
        </div>
      );

    case 'rag':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-indigo-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl">
          <div className="flex items-center justify-between text-xs font-mono text-indigo-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <Database className="w-4 h-4 text-indigo-400" /> CHROMADB // VECTOR_STORE
            </span>
            <span className="text-emerald-400 font-bold">COSINE: 0.948</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 my-auto">
            <div className="p-4 rounded-2xl bg-indigo-950/40 border border-indigo-500/30 text-xs font-mono flex flex-col gap-1.5 text-indigo-200 shadow-md">
              <span className="text-[10px] text-indigo-400 font-bold uppercase tracking-wider">company_policy.txt</span>
              <span className="text-xs text-neutral-200 font-sans truncate">Chunk #42: PTO & remote guidelines</span>
              <div className="flex items-center justify-between mt-2 pt-2 border-t border-indigo-500/20">
                <span className="text-[10px] text-neutral-400">Similarity</span>
                <span className="text-[11px] font-bold text-emerald-400">96.8% MATCH</span>
              </div>
            </div>
            <div className="p-4 rounded-2xl bg-indigo-950/40 border border-indigo-500/30 text-xs font-mono flex flex-col gap-1.5 text-indigo-200 shadow-md">
              <span className="text-[10px] text-indigo-400 font-bold uppercase tracking-wider">resume_guide.pdf</span>
              <span className="text-xs text-neutral-200 font-sans truncate">Chunk #12: Action verbs strategy</span>
              <div className="flex items-center justify-between mt-2 pt-2 border-t border-indigo-500/20">
                <span className="text-[10px] text-neutral-400">Similarity</span>
                <span className="text-[11px] font-bold text-emerald-400">91.4% MATCH</span>
              </div>
            </div>
          </div>
        </div>
      );

    case 'search':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-cyan-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl">
          <div className="flex items-center justify-between text-xs font-mono text-cyan-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <Globe className="w-4 h-4 text-cyan-400" /> TAVILY_SEARCH // RADAR
            </span>
            <span className="text-emerald-400 font-bold">3 LIVE SOURCES</span>
          </div>

          <div className="flex flex-col gap-2.5 my-auto">
            {['docs.doxa.ai/api/v2', 'github.com/vstorm-co/template', 'arxiv.org/abs/2401.0912'].map((url, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-black/60 border border-cyan-500/20 text-xs font-mono flex items-center justify-between text-neutral-300">
                <span className="truncate text-cyan-300 font-sans">{url}</span>
                <ArrowUpRight className="w-4 h-4 text-cyan-400 shrink-0" />
              </div>
            ))}
          </div>
        </div>
      );

    case 'streaming':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-amber-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl">
          <div className="flex items-center justify-between text-xs font-mono text-amber-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <Zap className="w-4 h-4 text-amber-400" /> STREAMING_ENGINE // LOW_LATENCY
            </span>
            <span className="text-amber-400 font-bold">38ms / TOKEN</span>
          </div>

          <div className="p-4 rounded-2xl bg-amber-950/30 border border-amber-500/20 text-xs font-mono text-neutral-200 my-auto min-h-[100px] flex flex-col justify-between">
            <p className="leading-relaxed font-sans text-sm text-neutral-200">
              {streamText}
            </p>
            <div className="flex items-center gap-1.5 mt-3 text-amber-400 font-mono text-[10px]">
              <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping" />
              <span>TOKEN_STREAM_ACTIVE</span>
            </div>
          </div>
        </div>
      );

    case 'voice':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-rose-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl">
          <div className="flex items-center justify-between text-xs font-mono text-rose-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <Mic className="w-4 h-4 text-rose-400" /> VOICE_LISTENER // CONTINUOUS
            </span>
            <span className="text-emerald-400 font-bold">WAKE PHRASE: 'DOXA'</span>
          </div>

          <div className="flex flex-col items-center justify-center gap-4 my-auto">
            <div className="relative w-20 h-20 rounded-full bg-rose-500/10 border border-rose-500/30 flex items-center justify-center">
              <div className="absolute inset-0 rounded-full bg-rose-500/20 animate-ping" />
              <Volume2 className="w-8 h-8 text-rose-400 relative z-10" />
            </div>
            <span className="text-xs font-mono text-neutral-300 font-semibold">Listening for wake phrase...</span>
          </div>
        </div>
      );

    case 'debate':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-purple-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl">
          <div className="flex items-center justify-between text-xs font-mono text-purple-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <ShieldCheck className="w-4 h-4 text-purple-400" /> DUAL_ENGINE // CONSENSUS
            </span>
            <span className="text-purple-300 font-bold">VERDICT: VERIFIED</span>
          </div>

          <div className="grid grid-cols-2 gap-3 my-auto text-xs font-mono">
            <div className="p-3.5 rounded-2xl bg-violet-950/40 border border-violet-500/30 flex flex-col gap-1 text-violet-200">
              <span className="text-[10px] text-violet-400 font-bold uppercase">Optimist Model</span>
              <span className="text-[11px] font-sans text-neutral-300">Proposes hypothesis plan</span>
            </div>
            <div className="p-3.5 rounded-2xl bg-cyan-950/40 border border-cyan-500/30 flex flex-col gap-1 text-cyan-200">
              <span className="text-[10px] text-cyan-400 font-bold uppercase">Skeptic Model</span>
              <span className="text-[11px] font-sans text-neutral-300">Cross-checks edge cases</span>
            </div>
          </div>
        </div>
      );

    case 'branching':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-blue-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl">
          <div className="flex items-center justify-between text-xs font-mono text-blue-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <GitBranch className="w-4 h-4 text-blue-400" /> TIMELINE_BRANCH // GIT_TREE
            </span>
            <span className="text-emerald-400 font-bold">3 BRANCHES</span>
          </div>

          <div className="flex flex-col gap-2.5 my-auto text-xs font-mono">
            <div className="p-3 rounded-xl bg-blue-500/10 border border-blue-500/30 text-white flex items-center justify-between">
              <span>Main Thread (Active)</span>
              <span className="text-[10px] text-blue-400 font-bold">CURRENT</span>
            </div>
            <div className="p-3 rounded-xl bg-neutral-900 border border-neutral-800 text-neutral-400 flex items-center justify-between">
              <span>Fork #1: Explore Python RAG</span>
              <span className="text-[10px] text-neutral-500">FORKED</span>
            </div>
          </div>
        </div>
      );

    case 'suggestions':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-teal-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl">
          <div className="flex items-center justify-between text-xs font-mono text-teal-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <Sparkles className="w-4 h-4 text-teal-400" /> ANTICIPATORY // SUGGESTIONS
            </span>
            <span className="text-teal-300 font-bold">CONTEXT_AWARE</span>
          </div>

          <div className="flex flex-col gap-2.5 my-auto text-xs font-sans">
            <div className="p-3 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-200 flex items-center justify-between">
              <span>"Can you summarize the vector search performance benchmarks?"</span>
              <ArrowRight className="w-4 h-4 text-teal-400" />
            </div>
            <div className="p-3 rounded-xl bg-neutral-900 border border-neutral-800 text-neutral-300 flex items-center justify-between">
              <span>"Show me how to set up custom document embeddings."</span>
              <ArrowRight className="w-4 h-4 text-neutral-500" />
            </div>
          </div>
        </div>
      );

    case 'timers':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-amber-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl">
          <div className="flex items-center justify-between text-xs font-mono text-amber-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <Clock className="w-4 h-4 text-amber-400" /> DAEMON_SCHEDULER // TIMER
            </span>
            <span className="text-amber-400 font-bold">ACTIVE DAEMON</span>
          </div>

          <div className="flex flex-col items-center justify-center gap-3 my-auto">
            <span className="text-4xl font-extrabold font-orbitron text-amber-400" style={{ fontFamily: 'Orbitron, sans-serif' }}>
              00:04:59
            </span>
            <span className="text-xs font-mono text-neutral-400">Background reminder running...</span>
          </div>
        </div>
      );

    case 'calendar':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-emerald-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl">
          <div className="flex items-center justify-between text-xs font-mono text-emerald-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <Calendar className="w-4 h-4 text-emerald-400" /> GOOGLE_WORKSPACE // SYNC
            </span>
            <span className="text-emerald-400 font-bold font-mono">CONNECTED</span>
          </div>

          <div className="grid grid-cols-1 gap-2.5 my-auto text-xs font-sans">
            <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-200 flex items-center justify-between">
              <span>📅 Product Architecture Review @ 2:00 PM</span>
              <span className="text-[10px] font-mono text-emerald-400 font-bold">TODAY</span>
            </div>
            <div className="p-3 rounded-xl bg-neutral-900 border border-neutral-800 text-neutral-300 flex items-center justify-between">
              <span>📅 Vector Store Deployment Sync @ 4:30 PM</span>
              <span className="text-[10px] font-mono text-neutral-500">SCHEDULED</span>
            </div>
          </div>
        </div>
      );

    case 'hinglish':
      return (
        <div className="relative w-full h-80 rounded-3xl bg-neutral-950/90 border border-fuchsia-500/30 p-6 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-2xl">
          <div className="flex items-center justify-between text-xs font-mono text-fuchsia-400 border-b border-neutral-800 pb-3">
            <span className="flex items-center gap-2 font-bold">
              <Languages className="w-4 h-4 text-fuchsia-400" /> BILINGUAL_ENGINE // ADAPTIVE
            </span>
            <span className="text-fuchsia-300 font-bold">ENGLISH ↔ HINGLISH</span>
          </div>

          <div className="p-4 rounded-2xl bg-fuchsia-950/30 border border-fuchsia-500/20 text-xs font-mono text-neutral-200 my-auto min-h-[100px] flex items-center justify-center text-center">
            <p className="text-sm font-sans font-semibold text-fuchsia-200 transition-all duration-300">
              "{hinglishText}"
            </p>
          </div>
        </div>
      );

    default:
      return null;
  }
}

export default function FeatureShowcase({ onLaunchApp }) {
  return (
    <section id="features" className="relative py-28 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10">
      <div className="text-center max-w-3xl mx-auto mb-24">
        <h2 className="text-xs font-mono font-bold uppercase tracking-widest text-violet-400 mb-3">
          COMPLETE FEATURE SHOWCASE
        </h2>
        <p className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          Built for Autonomous Precision & Scale.
        </p>
      </div>

      {/* 11 Full Alternating Feature Blocks */}
      <div className="flex flex-col gap-24 sm:gap-32">
        {FEATURES.map((feature, idx) => {
          const isEven = idx % 2 === 0;
          const Icon = feature.icon;

          return (
            <motion.div
              key={feature.id}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-100px' }}
              transition={{ duration: 0.7, ease: 'easeOut' }}
              className={`flex flex-col ${isEven ? 'lg:flex-row' : 'lg:flex-row-reverse'} items-center gap-12 lg:gap-20`}
            >
              {/* Text Side */}
              <div className="flex-1 flex flex-col gap-5">
                <div className="flex items-center gap-3">
                  <div className={`p-3 rounded-2xl bg-gradient-to-r ${feature.color} text-white shadow-xl`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className="text-xs font-mono font-bold tracking-wider text-violet-400 uppercase">
                    {feature.title}
                  </span>
                </div>

                <h3 className="text-2xl sm:text-4xl font-bold text-white tracking-tight font-orbitron leading-snug" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                  {feature.headline}
                </h3>

                <p className="text-sm sm:text-base text-neutral-300 leading-relaxed font-sans font-normal">
                  {feature.desc}
                </p>

                {/* Badges */}
                <div className="flex flex-wrap gap-2 pt-2">
                  {feature.badges.map((b, bIdx) => (
                    <span key={bIdx} className="px-3.5 py-1.5 rounded-full bg-neutral-900/90 border border-neutral-800 text-[11px] font-mono text-neutral-400">
                      {b}
                    </span>
                  ))}
                </div>

                {/* Try Feature CTA */}
                {onLaunchApp && (
                  <div className="pt-2">
                    <button
                      type="button"
                      onClick={onLaunchApp}
                      className="inline-flex items-center gap-2 text-xs font-bold font-mono text-violet-400 hover:text-cyan-300 transition-colors group cursor-pointer"
                    >
                      <span>TEST THIS IN DOXA</span>
                      <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                    </button>
                  </div>
                )}
              </div>

              {/* Visual Graphic Side */}
              <div className="flex-1 w-full">
                <RenderFeatureVisual type={feature.type} />
              </div>
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}
