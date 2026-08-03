import React from 'react';
import { motion } from 'framer-motion';
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
  Layers, 
  CheckCircle2, 
  ArrowUpRight 
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
    title: 'Timers & Background Operations',
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
  },
  {
    id: 'sphereteaser',
    title: 'Sphere Mode Teaser',
    headline: 'Cinematic Live Diagnostics Dashboard',
    desc: 'Coming soon into view — an interactive 3D WebGL telemetry sphere for monitoring real-time agent neural frequencies and system health.',
    badges: ['Coming Soon', '3D WebGL Telemetry', 'Live Diagnostics'],
    icon: Layers,
    color: 'from-neutral-700 to-neutral-900',
    type: 'teaser'
  }
];

function RenderFeatureVisual({ type }) {
  switch (type) {
    case 'agent':
      return (
        <div className="relative w-full h-64 sm:h-72 rounded-2xl bg-neutral-950/80 border border-violet-500/20 p-5 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-xl group">
          <div className="flex items-center justify-between text-xs font-mono text-violet-400 border-b border-neutral-800 pb-2">
            <span>PLANNING_GRAPH // ACTIVE</span>
            <span className="animate-pulse">● EXECUTING</span>
          </div>
          <div className="flex flex-col gap-2.5 my-auto">
            <div className="p-3 rounded-xl bg-violet-500/10 border border-violet-500/30 text-white text-xs font-mono flex items-center justify-between shadow-md">
              <span className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" /> 1. Query vector database & web search
              </span>
              <span className="text-[10px] text-emerald-400">DONE</span>
            </div>
            <div className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/40 text-cyan-300 text-xs font-mono flex items-center justify-between shadow-lg animate-pulse">
              <span className="flex items-center gap-2 font-semibold">
                <Cpu className="w-4 h-4 text-cyan-400 animate-spin" /> 2. Synthesize multi-source reasoning
              </span>
              <span className="text-[10px] text-cyan-400">RUNNING</span>
            </div>
            <div className="p-3 rounded-xl bg-neutral-900 border border-neutral-800 text-neutral-500 text-xs font-mono flex items-center justify-between">
              <span>3. Format final answer & citations</span>
              <span className="text-[10px]">PENDING</span>
            </div>
          </div>
        </div>
      );

    case 'rag':
      return (
        <div className="relative w-full h-64 sm:h-72 rounded-2xl bg-neutral-950/80 border border-indigo-500/20 p-5 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-xl">
          <div className="flex items-center justify-between text-xs font-mono text-indigo-400 border-b border-neutral-800 pb-2">
            <span>CHROMADB // VECTOR_STORE</span>
            <span>COSINE: 0.942</span>
          </div>
          <div className="grid grid-cols-2 gap-3 my-auto">
            <div className="p-3 rounded-xl bg-indigo-950/40 border border-indigo-500/30 text-xs font-mono flex flex-col gap-1 text-indigo-200">
              <span className="text-[10px] text-indigo-400 font-bold">company_policy.txt</span>
              <span className="text-[11px] text-neutral-300 truncate">Chunk #42: PTO & remote work</span>
              <span className="text-[9px] text-emerald-400 mt-1">Match score: 96.8%</span>
            </div>
            <div className="p-3 rounded-xl bg-indigo-950/40 border border-indigo-500/30 text-xs font-mono flex flex-col gap-1 text-indigo-200">
              <span className="text-[10px] text-indigo-400 font-bold">resume_guide.pdf</span>
              <span className="text-[11px] text-neutral-300 truncate">Chunk #12: Action verbs</span>
              <span className="text-[9px] text-emerald-400 mt-1">Match score: 91.2%</span>
            </div>
          </div>
        </div>
      );

    case 'search':
      return (
        <div className="relative w-full h-64 sm:h-72 rounded-2xl bg-neutral-950/80 border border-cyan-500/20 p-5 flex flex-col justify-between overflow-hidden shadow-2xl backdrop-blur-xl">
          <div className="flex items-center justify-between text-xs font-mono text-cyan-400 border-b border-neutral-800 pb-2">
            <span>TAVILY_SEARCH // RADAR</span>
            <span className="text-emerald-400">3 SOURCES</span>
          </div>
          <div className="flex flex-col gap-2 my-auto">
            {['docs.doxa.ai/api', 'github.com/vstorm-co/template', 'arxiv.org/abs/2401.09'].map((url, idx) => (
              <div key={idx} className="p-2.5 rounded-lg bg-black/60 border border-cyan-500/20 text-xs font-mono flex items-center justify-between text-neutral-300">
                <span className="truncate text-cyan-300">{url}</span>
                <ArrowUpRight className="w-3.5 h-3.5 text-neutral-500" />
              </div>
            ))}
          </div>
        </div>
      );

    default:
      return (
        <div className="relative w-full h-64 sm:h-72 rounded-2xl bg-neutral-950/80 border border-white/10 p-5 flex items-center justify-center overflow-hidden shadow-2xl backdrop-blur-xl">
          <div className="p-4 rounded-2xl bg-violet-500/10 border border-violet-500/20 text-violet-300 text-center font-mono text-xs flex flex-col items-center gap-2">
            <Sparkles className="w-8 h-8 text-violet-400 animate-pulse" />
            <span className="font-bold tracking-wider uppercase">Doxa Core Feature</span>
          </div>
        </div>
      );
  }
}

export default function FeatureShowcase() {
  return (
    <section id="features" className="relative py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto z-10">
      <div className="text-center max-w-3xl mx-auto mb-20">
        <h2 className="text-xs font-mono font-bold uppercase tracking-widest text-violet-400 mb-3">
          PLATFORM CAPABILITIES
        </h2>
        <p className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          Engineered for Full Autonomy & Precision.
        </p>
      </div>

      {/* Feature Blocks (Alternating Left / Right) */}
      <div className="flex flex-col gap-20">
        {FEATURES.map((feature, idx) => {
          const isEven = idx % 2 === 0;
          const Icon = feature.icon;

          return (
            <motion.div
              key={feature.id}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-100px' }}
              transition={{ duration: 0.7, ease: 'easeOut' }}
              className={`flex flex-col ${isEven ? 'lg:flex-row' : 'lg:flex-row-reverse'} items-center gap-10 lg:gap-16`}
            >
              {/* Text Side */}
              <div className="flex-1 flex flex-col gap-4">
                <div className="flex items-center gap-3">
                  <div className={`p-2.5 rounded-xl bg-gradient-to-r ${feature.color} text-white shadow-lg`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className="text-xs font-mono font-bold tracking-wider text-violet-400 uppercase">
                    {feature.title}
                  </span>
                </div>

                <h3 className="text-2xl sm:text-3xl font-bold text-white tracking-tight font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                  {feature.headline}
                </h3>

                <p className="text-sm sm:text-base text-neutral-300 leading-relaxed font-sans font-normal">
                  {feature.desc}
                </p>

                {/* Badges */}
                <div className="flex flex-wrap gap-2 pt-2">
                  {feature.badges.map((b, bIdx) => (
                    <span key={bIdx} className="px-3 py-1 rounded-full bg-neutral-900 border border-neutral-800 text-[10px] font-mono text-neutral-400">
                      {b}
                    </span>
                  ))}
                </div>
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
