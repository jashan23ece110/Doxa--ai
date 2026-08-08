import {
  Cpu,
  Database,
  Globe,
  Zap,
  Mic,
  MessageSquare,
  Upload,
  Sparkles,
  ShieldCheck,
  GitBranch,
  Clock,
  Calendar,
  Languages
} from 'lucide-react';

export const CAPABILITIES = [
  {
    label: 'Autonomous Reasoning',
    desc: 'Multi-step planning, tool use & self-correction loop.',
    icon: Cpu,
    colorClass: 'text-violet-600',
    iconBgClass: 'bg-violet-50 text-violet-600 border-violet-100',
    hoverClass: 'hover:border-violet-300 hover:shadow-violet-100/60'
  },
  {
    label: 'Real-Time RAG',
    desc: 'Instant context-aware search and retrieval indexing.',
    icon: Database,
    colorClass: 'text-indigo-600',
    iconBgClass: 'bg-indigo-50 text-indigo-600 border-indigo-100',
    hoverClass: 'hover:border-indigo-300 hover:shadow-indigo-100/60'
  },
  {
    label: 'Live Web Search',
    desc: 'Grounding responses with real-time web citations.',
    icon: Globe,
    colorClass: 'text-cyan-600',
    iconBgClass: 'bg-cyan-50 text-cyan-600 border-cyan-100',
    hoverClass: 'hover:border-cyan-300 hover:shadow-cyan-100/60'
  },
  {
    label: 'Streaming Responses',
    desc: 'Continuous token delivery with sub-50ms latency.',
    icon: Zap,
    colorClass: 'text-violet-600',
    iconBgClass: 'bg-violet-50 text-violet-600 border-violet-100',
    hoverClass: 'hover:border-violet-300 hover:shadow-violet-100/60'
  },
  {
    label: 'Native Voice Engine',
    desc: 'Integrated speech recognition & vocal responses.',
    icon: Mic,
    colorClass: 'text-indigo-600',
    iconBgClass: 'bg-indigo-50 text-indigo-600 border-indigo-100',
    hoverClass: 'hover:border-indigo-300 hover:shadow-indigo-100/60'
  },
  {
    label: 'Multi-Model Debate',
    desc: 'Cross-consensus checking and argument checks.',
    icon: MessageSquare,
    colorClass: 'text-cyan-600',
    iconBgClass: 'bg-cyan-50 text-cyan-600 border-cyan-100',
    hoverClass: 'hover:border-cyan-300 hover:shadow-cyan-100/60'
  }
];

export const NAV_CAPABILITIES = [
  { label: 'Autonomous Reasoning', desc: 'Multi-step planning & tool execution', icon: Cpu },
  { label: 'RAG Knowledge Base', desc: 'Vector document search over your data', icon: Database },
  { label: 'Live Web Search', desc: 'Real-time Tavily web citations', icon: Globe },
  { label: 'Native Voice Mode', desc: 'Conversational voice synthesis', icon: Mic },
  { label: 'Timeline Branching', desc: 'Non-linear thread exploration', icon: GitBranch },
  { label: 'Dual Model Debate', desc: 'Optimist vs Skeptic consensus engine', icon: ShieldCheck }
];

export const WHATS_NEW = [
  { label: 'Voice Mode 2.0', desc: 'Natural conversation with streaming TTS' },
  { label: 'Timeline Branching', desc: 'Explore alternative reasoning paths' },
  { label: 'Processing Engine Selector', desc: 'Choose your AI model on-the-fly' },
];

export const STEPS = [
  {
    step: '01',
    title: 'Ask or Upload',
    desc: 'Submit a goal or upload documents to seed Doxa’s reasoning space.',
    icon: Upload,
    colorClass: 'text-violet-600',
    iconBgClass: 'bg-violet-50 text-violet-600 border-violet-100',
    hoverClass: 'hover:border-violet-300 hover:shadow-violet-100/60'
  },
  {
    step: '02',
    title: 'Doxa Plans',
    desc: 'The planning core breaks the goal down into an optimal multi-step tool sequence.',
    icon: Cpu,
    colorClass: 'text-indigo-600',
    iconBgClass: 'bg-indigo-50 text-indigo-600 border-indigo-100',
    hoverClass: 'hover:border-indigo-300 hover:shadow-indigo-100/60'
  },
  {
    step: '03',
    title: 'Retrieves & Searches',
    desc: 'Runs parallel queries against RAG databases and live web search for factual grounding.',
    icon: Database,
    colorClass: 'text-cyan-600',
    iconBgClass: 'bg-cyan-50 text-cyan-600 border-cyan-100',
    hoverClass: 'hover:border-cyan-300 hover:shadow-cyan-100/60'
  },
  {
    step: '04',
    title: 'Responds & Acts',
    desc: 'Streams the citation-backed response and runs calendar/scheduler actions.',
    icon: Sparkles,
    colorClass: 'text-violet-600',
    iconBgClass: 'bg-violet-50 text-violet-600 border-violet-100',
    hoverClass: 'hover:border-violet-300 hover:shadow-violet-100/60'
  }
];

export const FEATURES = [
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
    color: 'from-cyan-500 to-violet-500',
    type: 'search'
  },
  {
    id: 'streaming',
    title: 'Real-Time Streaming Responses',
    headline: 'Sub-50ms Low-Latency Continuous Token Stream',
    desc: 'Experience instant response generation. Tokens stream directly from the model to your screen in real time with polling fallback support.',
    badges: ['Sub-50ms Stream', 'Real-Time Tokens', 'Zero Waiting'],
    icon: Zap,
    color: 'from-violet-500 to-cyan-500',
    type: 'streaming'
  },
  {
    id: 'voice',
    title: 'Native Voice Mode',
    headline: 'Hands-Free Wake-Word Listener & Speech Synthesis',
    desc: 'Speak naturally to Doxa. Powered by continuous Web Speech API wake-phrase detection and natural text-to-speech voice synthesis.',
    badges: ['Hands-Free Wake Phrase', 'Speech Recognition', 'TTS Audio'],
    icon: Mic,
    color: 'from-indigo-500 to-violet-500',
    type: 'voice'
  },
  {
    id: 'debate',
    title: 'Multi-Model Debate Engine',
    headline: 'Dual-Core Optimist vs Skeptic Counter-Arguments',
    desc: 'Eliminate single-model bias. Doxa spawns parallel Optimist and Skeptic evaluator instances that critique hypotheses before delivering a consensus verdict.',
    badges: ['Dual Perspective', 'Fact Verification', 'Consensus Synthesis'],
    icon: ShieldCheck,
    color: 'from-violet-500 to-indigo-600',
    type: 'debate'
  },
  {
    id: 'branching',
    title: 'Sessions & Timeline Branching',
    headline: 'Non-Linear Conversational History & Thread Forking',
    desc: 'Explore alternative problem-solving paths. Fork any message in a conversation to create a new timeline branch without losing original context.',
    badges: ['Thread Forking', 'Time-Travel Switcher', 'Session Storage'],
    icon: GitBranch,
    color: 'from-indigo-500 to-cyan-500',
    type: 'branching'
  },
  {
    id: 'suggestions',
    title: 'Proactive Suggestions',
    headline: 'Context-Aware Anticipatory Prompt Generation',
    desc: 'Doxa analyzes previous message turns to suggest relevant follow-up questions and next logical steps before you even type them.',
    badges: ['Anticipatory AI', '1-Click Prompts', 'Smart Recommendations'],
    icon: Sparkles,
    color: 'from-cyan-500 to-violet-500',
    type: 'suggestions'
  },
  {
    id: 'timers',
    title: 'Timers & Reminders',
    headline: 'Autonomous Reminders & Background Task Scheduling',
    desc: 'Set timers and background execution schedules. Doxa runs background polling daemons and notifies you when tasks complete.',
    badges: ['Background Daemons', 'Timed Reminders', 'Async Execution'],
    icon: Clock,
    color: 'from-violet-500 to-cyan-500',
    type: 'timers'
  },
  {
    id: 'calendar',
    title: 'Calendar & Workspace Sync',
    headline: 'Productivity Workflow & Event Management',
    desc: 'Create, query, and manage calendar events directly through natural conversational goals integrated with your daily schedule.',
    badges: ['Event Management', 'Workflow Automation', 'Schedule Sync'],
    icon: Calendar,
    color: 'from-indigo-500 to-cyan-500',
    type: 'calendar'
  },
  {
    id: 'hinglish',
    title: 'Bilingual Language Engine',
    headline: 'Fluid Toggle Between English & Hinglish',
    desc: 'Communicate in standard English or natural conversational Hinglish. Doxa adapts its prompt synthesis and response tone automatically.',
    badges: ['English Mode', 'Hinglish Mode', 'Tone Adaptation'],
    icon: Languages,
    color: 'from-violet-500 to-indigo-500',
    type: 'hinglish'
  }
];
