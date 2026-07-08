import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Activity, Clock, Zap, History, Settings, Bot, Code2, AlertTriangle, LogOut, CheckCircle2, Play, Download, Loader2, FileText, Upload, Trash2, BookOpen, ChevronDown, ChevronUp, Terminal, Menu, X, Cpu, Layers, Inbox } from 'lucide-react';
import axios from 'axios';

/* ── animation variants ── */
const pageVariants = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.14, ease: [0.25, 0.1, 0.25, 1] } },
  exit:    { opacity: 0, y: -8, transition: { duration: 0.08 } },
};

const staggerContainer = {
  animate: { transition: { staggerChildren: 0.04 } },
};

const staggerItem = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.14, ease: 'easeOut' } },
};

const cardHover = {
  scale: 1.008,
  transition: { type: 'spring', stiffness: 500, damping: 30 },
};

const tapScale = { scale: 0.97, transition: { duration: 0.08 } };
const hoverScale = { scale: 1.02, transition: { duration: 0.08 } };

/* ── skeleton ── */
const SkeletonLoader = () => (
  <div className="flex flex-col gap-4 py-3">
    {[75, 100, 83, 50].map((w, i) => (
      <div key={i} className={`h-4 bg-neutral-800/80 rounded-md animate-pulse`} style={{ width: `${w}%`, animationDelay: `${i * 150}ms` }} />
    ))}
  </div>
);

/* ── nav items ── */
const NAV_ITEMS = [
  { id: 'agent',     label: 'Agent',     icon: Bot },
  { id: 'eval',      label: 'Eval',      icon: Code2 },
  { id: 'documents', label: 'Docs',      icon: FileText },
  { id: 'history',   label: 'History',   icon: History },
  { id: 'settings',  label: 'Settings',  icon: Settings },
];

/* ════════════════════════════════════════════════
   MAIN APP
   ════════════════════════════════════════════════ */
function App() {
  /* state */
  const [user, setUser] = useState(() => localStorage.getItem('ai_eval_user'));
  const [authMode, setAuthMode] = useState('login');
  const [currentView, setCurrentView] = useState('agent');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const API_BASE = import.meta.env.VITE_API_URL;

  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [settings, setSettings] = useState({
    model1Name: 'Llama 3.1 8B (Instant)',
    model2Name: 'Llama 3.3 70B (Versatile)',
  });

  const [useRag, setUseRag] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [uploadingDoc, setUploadingDoc] = useState(false);
  const [retrievedContext, setRetrievedContext] = useState(null);
  const [showContext, setShowContext] = useState(false);

  const [agentGoal, setAgentGoal] = useState('');
  const [agentLoading, setAgentLoading] = useState(false);
  const [agentRunId, setAgentRunId] = useState(null);
  const [agentStatus, setAgentStatus] = useState(null);
  const [agentError, setAgentError] = useState(null);

  /* close mobile sidebar on nav */
  const navigate = (view) => {
    setCurrentView(view);
    setSidebarOpen(false);
  };

  /* ── auth ── */
  const handleAuth = (e) => {
    e.preventDefault();
    if (authMode === 'login' || authMode === 'signup') {
      const email = e.target.email.value;
      if (email) { setUser(email); localStorage.setItem('ai_eval_user', email); }
    } else if (authMode === 'phone') {
      setAuthMode('otp');
    } else if (authMode === 'otp') {
      setUser('phone_user'); localStorage.setItem('ai_eval_user', 'phone_user');
    }
  };
  const handleLogout = () => { setUser(null); localStorage.removeItem('ai_eval_user'); setAuthMode('login'); };

  /* ── documents ── */
  const fetchDocuments = async () => {
    try { const res = await axios.get(`${API_BASE}/documents`); setDocuments(res.data.documents || []); }
    catch (err) { console.error('Failed to fetch documents', err); }
  };
  useEffect(() => { if (currentView === 'documents' && user) fetchDocuments(); }, [currentView, user]);

  const handleUploadDoc = async (file) => {
    if (!file) return;
    setUploadingDoc(true);
    const fd = new FormData(); fd.append('file', file);
    try { await axios.post(`${API_BASE}/documents/upload`, fd, { headers: { 'Content-Type': 'multipart/form-data' } }); await fetchDocuments(); }
    catch { alert('Failed to upload document.'); }
    finally { setUploadingDoc(false); }
  };
  const handleDeleteDoc = async (docId) => {
    if (!window.confirm('Delete this document?')) return;
    try { await axios.delete(`${API_BASE}/documents/${docId}`); await fetchDocuments(); } catch {}
  };

  /* ── eval ── */
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    setLoading(true); setError(null); setResults(null); setRetrievedContext(null); setShowContext(false);
    try {
      const res = await fetch(`${API_BASE}/evaluate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ prompt, use_rag: useRag }) });
      if (!res.ok) throw new Error('Evaluation failed');
      const data = await res.json();
      setResults({ ...data, _useRag: data.use_rag });
      if (data.retrieved_context) setRetrievedContext(data.retrieved_context);
      setHistory(prev => [{ id: Date.now(), timestamp: new Date().toISOString(), prompt, models: { model1: settings.model1Name, model2: settings.model2Name }, results: data, useRag: data.use_rag }, ...prev]);
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  const handleExportCSV = () => {
    if (history.length === 0) return;
    const headers = ['Timestamp','Prompt','Model 1','Latency 1 (ms)','Model 2','Latency 2 (ms)'];
    const csv = [headers.join(','), ...history.map(r => {
      const d = new Date(r.timestamp).toLocaleString().replace(',','');
      return `${d},"${r.prompt.replace(/"/g,'""')}",${r.models.model1},${r.results.groq_1?.latency_ms||0},${r.models.model2},${r.results.groq_2?.latency_ms||0}`;
    })].join('\n');
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8;' }));
    link.setAttribute('download', 'evaluation_history.csv');
    document.body.appendChild(link); link.click(); document.body.removeChild(link);
  };

  /* ── agent ── */
  useEffect(() => {
    let id;
    if (agentRunId && agentStatus?.status !== 'completed' && agentStatus?.status !== 'failed') {
      id = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/agent/status/${agentRunId}`);
          if (res.ok) { 
            const d = await res.json(); 
            setAgentStatus(d); 
            if (d.status === 'completed' || d.status === 'failed') { 
              setAgentLoading(false); 
              clearInterval(id); 
              if (d.status === 'failed' && d.error) {
                setAgentError(`Agent Execution Failed: ${d.error}`);
              }
            } 
          }
        } catch {}
      }, 1000);
    }
    return () => { if (id) clearInterval(id); };
  }, [agentRunId, agentStatus, API_BASE]);

  const handleStartAgent = async (e) => {
    e.preventDefault();
    if (!agentGoal.trim()) return;
    setAgentLoading(true); setAgentError(null); setAgentRunId(null); setAgentStatus(null);
    try {
      const res = await fetch(`${API_BASE}/agent/start`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ goal: agentGoal }) });
      if (!res.ok) { const d = await res.json(); throw new Error(d.detail || 'Failed to start agent'); }
      const data = await res.json();
      setAgentRunId(data.run_id);
      setAgentStatus({ status: 'running', steps: [], final_result: null });
    } catch (err) { setAgentError(err.message); setAgentLoading(false); }
  };

  /* ═══════════════════════════════════════════
     SUB-COMPONENTS
     ═══════════════════════════════════════════ */

  /* result panel (eval) */
  const ResultPanel = ({ title, data, delay }) => (
    <motion.div
      variants={staggerItem}
      className="bg-[#111] border panel-glow rounded-xl flex flex-col overflow-hidden shadow-sm h-full"
    >
      <div className="flex items-center justify-between px-4 py-3 border-b border-neutral-800 bg-[#161616]">
        <h3 className="font-medium text-[14px] text-white">{title}</h3>
        <div className="flex items-center gap-2">
          {data?.latency_ms && (
            <span className="text-[11px] font-mono px-2 py-0.5 bg-neutral-900 border panel-glow rounded text-neutral-400">{data.latency_ms}ms</span>
          )}
          {data && (
            <span className={`text-[11px] font-medium px-2 py-0.5 rounded border ${data._useRag ? 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400' : 'bg-neutral-900 border-neutral-800 text-neutral-400'}`}>
              {data._useRag ? 'RAG' : 'Model'}
            </span>
          )}
        </div>
      </div>
      <div className="flex-1 p-4 overflow-y-auto custom-scrollbar">
        {loading ? <SkeletonLoader /> : data ? (
          data.error
            ? <div className="p-3 bg-red-500/10 border border-red-500/20 rounded text-red-400 text-sm">Error: {data.error}</div>
            : <div className="text-[14px] text-neutral-300 leading-relaxed whitespace-pre-wrap">{data.content}</div>
        ) : (
          <div className="h-full flex items-center justify-center text-neutral-600 italic text-sm">Awaiting evaluation…</div>
        )}
      </div>

      {/* context drawer */}
      <AnimatePresence>
        {retrievedContext?.length > 0 && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="border-t border-neutral-800 overflow-hidden">
            <button onClick={() => setShowContext(!showContext)} className="w-full flex items-center justify-between px-4 py-2 text-[12px] text-neutral-400 hover:bg-[#161616] transition-colors">
              <span className="flex items-center gap-1.5"><BookOpen className="w-3.5 h-3.5" /> Context ({retrievedContext.length})</span>
              {showContext ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
            <AnimatePresence>
              {showContext && (
                <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="flex flex-col gap-2 px-4 pb-3 max-h-44 overflow-y-auto custom-scrollbar">
                  {retrievedContext.map((c, i) => (
                    <div key={i} className="p-2.5 bg-[#1a1a1a] rounded border panel-glow text-[12px]">
                      <div className="flex justify-between mb-1">
                        <span className="text-indigo-400 font-medium flex items-center gap-1"><FileText className="w-3 h-3" />{c.filename || 'Unknown'}</span>
                        <span className="text-neutral-500 font-mono">{c.similarity ? `${(c.similarity * 100).toFixed(1)}%` : ''}</span>
                      </div>
                      <p className="text-neutral-400 leading-relaxed whitespace-pre-wrap">{c.text}</p>
                    </div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );

  /* ═══════════════════════════════════════════
     LOGIN SCREEN
     ═══════════════════════════════════════════ */
  if (!user) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8 font-sans selection:bg-indigo-500/30">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }} className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="flex justify-center mb-6">
            <div className="p-3 bg-[#111] rounded-xl border panel-glow"><Sparkles className="w-8 h-8 text-indigo-500" /></div>
          </div>
          <h2 className="text-center text-2xl font-semibold text-white">Doxa</h2>
          <p className="mt-2 text-center text-sm text-neutral-500">
            {authMode === 'login' && 'Sign in to your account'}
            {authMode === 'signup' && 'Create an account to get started'}
            {authMode === 'phone' && 'Enter your phone number'}
            {authMode === 'otp' && 'Enter the verification code'}
          </p>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.06, duration: 0.2 }} className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-[#111] py-8 px-4 shadow-sm border panel-glow sm:rounded-xl sm:px-10">
            <form className="space-y-6" onSubmit={handleAuth}>
              {(authMode === 'login' || authMode === 'signup') && (
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-neutral-300">Email address</label>
                  <input id="email" name="email" type="email" required className="mt-1 block w-full px-3 py-2.5 border panel-glow rounded-lg bg-[#161616] text-white placeholder-neutral-500 input-glow panel-glow-hover sm:text-sm" />
                </div>
              )}
              {authMode === 'phone' && (
                <div>
                  <label htmlFor="phone" className="block text-sm font-medium text-neutral-300">Phone number</label>
                  <input id="phone" name="phone" type="tel" required className="mt-1 block w-full px-3 py-2.5 border panel-glow rounded-lg bg-[#161616] text-white placeholder-neutral-500 input-glow panel-glow-hover sm:text-sm" />
                </div>
              )}
              {authMode === 'otp' && (
                <div>
                  <label htmlFor="otp" className="block text-sm font-medium text-neutral-300">Verification Code</label>
                  <input id="otp" name="otp" type="text" required placeholder="123456" className="mt-1 block w-full px-3 py-2.5 border panel-glow rounded-lg bg-[#161616] text-white placeholder-neutral-500 input-glow panel-glow-hover sm:text-sm text-center tracking-widest text-lg font-mono" />
                </div>
              )}
              <motion.button type="submit" whileHover={hoverScale} whileTap={tapScale} className="w-full py-2.5 px-4 rounded-lg text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-500 hover:shadow-[0_0_20px_rgba(99,102,241,0.3)] transition-all duration-100">
                {authMode === 'login' ? 'Sign in' : authMode === 'signup' ? 'Create Account' : authMode === 'phone' ? 'Send Code' : 'Verify'}
              </motion.button>
            </form>

            <div className="mt-6">
              <div className="relative"><div className="absolute inset-0 flex items-center"><div className="w-full border-t border-neutral-800" /></div><div className="relative flex justify-center text-sm"><span className="px-2 bg-[#111] text-neutral-500">Or continue with</span></div></div>
              <div className="mt-6 grid grid-cols-2 gap-3">
                <button type="button" onClick={() => setAuthMode('phone')} className="w-full py-2 px-4 border panel-glow rounded-lg bg-[#161616] text-sm font-medium text-neutral-300 hover:bg-neutral-800 transition-colors">Phone</button>
                <button type="button" onClick={() => setAuthMode(authMode === 'login' ? 'signup' : 'login')} className="w-full py-2 px-4 border panel-glow rounded-lg bg-[#161616] text-sm font-medium text-neutral-300 hover:bg-neutral-800 transition-colors">
                  {authMode === 'login' ? 'Sign up' : 'Sign in'}
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    );
  }

  /* ═══════════════════════════════════════════
     MAIN LAYOUT — sidebar + content
     ═══════════════════════════════════════════ */
  return (
    <div className="min-h-screen flex bg-[#0a0a0a] text-neutral-200 selection:bg-indigo-500/30 font-sans">

      {/* ── mobile overlay ── */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            key="overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={() => setSidebarOpen(false)}
            className="fixed inset-0 bg-black/60 z-40 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* ── sidebar ── */}
      <aside
        className={`
          fixed lg:sticky top-0 left-0 z-50 h-screen
          w-56 bg-[#0e0e0e] border-r border-neutral-800
          flex flex-col
          transition-transform duration-200 ease-out
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0
        `}
      >
        {/* logo row */}
        <div className="flex items-center justify-between px-4 h-14 shrink-0 border-b border-neutral-800/60">
          <div className="flex items-center gap-2.5 cursor-pointer" onClick={() => navigate('agent')}>
            <div className="p-1 bg-neutral-900 rounded-md border panel-glow">
              <Sparkles className="w-4 h-4 text-indigo-500" />
            </div>
            <span className="text-[15px] font-semibold text-white tracking-tight">Doxa</span>
          </div>
          {/* close on mobile */}
          <button onClick={() => setSidebarOpen(false)} className="lg:hidden p-1 text-neutral-500 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* nav list */}
        <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
          {NAV_ITEMS.map(({ id, label, icon: Icon }) => (
            <motion.button
              key={id}
              onClick={() => navigate(id)}
              whileHover={{ x: 2 }}
              whileTap={tapScale}
              className={`
                w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-[13px] font-medium transition-all duration-100
                ${currentView === id
                  ? 'bg-neutral-800/80 text-white shadow-[0_0_12px_rgba(99,102,241,0.15)]'
                  : 'text-neutral-500 hover:text-neutral-200 hover:bg-neutral-800/40'
                }
              `}
            >
              <Icon className={`w-4 h-4 shrink-0 ${currentView === id ? 'text-indigo-400' : ''}`} />
              {label}
            </motion.button>
          ))}
        </nav>

        {/* bottom – user / sign out */}
        <div className="border-t border-neutral-800/60 px-3 py-3">
          <div className="text-[11px] text-neutral-500 truncate mb-2 px-1">{user}</div>
          <motion.button
            onClick={handleLogout}
            whileHover={{ x: 2 }}
            whileTap={tapScale}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-[13px] font-medium text-neutral-500 hover:text-red-400 hover:bg-red-400/5 transition-colors"
          >
            <LogOut className="w-4 h-4" /> Sign Out
          </motion.button>
        </div>
      </aside>

      {/* ── content column ── */}
      <div className="flex-1 flex flex-col min-w-0 relative overflow-x-hidden">
        
        {/* ambient background glow */}
        <div className="absolute inset-0 pointer-events-none z-0">
          <div className="absolute -top-[10%] -right-[5%] w-[600px] h-[600px] rounded-full bg-[radial-gradient(circle,rgba(99,102,241,0.12)_0%,transparent_65%)]" />
          <div className="absolute top-[40%] -left-[10%] w-[500px] h-[500px] rounded-full bg-[radial-gradient(circle,rgba(168,85,247,0.1)_0%,transparent_60%)]" />
        </div>

        {/* mobile top bar */}
        <div className="lg:hidden flex items-center h-14 px-4 border-b border-neutral-800/60 bg-[#0a0a0a] sticky top-0 z-30">
          <button onClick={() => setSidebarOpen(true)} className="p-1.5 -ml-1 text-neutral-400 hover:text-white transition-colors">
            <Menu className="w-5 h-5" />
          </button>
          <span className="ml-3 text-[15px] font-semibold text-white tracking-tight">Doxa</span>
        </div>

        {/* page content */}
        <AnimatePresence mode="wait">

          {/* ━━━ AGENT ━━━ */}
          {currentView === 'agent' && (
            <motion.main key="agent" variants={pageVariants} initial="initial" animate="animate" exit="exit" className="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-8 flex flex-col gap-5">
              <motion.div variants={staggerContainer} initial="initial" animate="animate" className="flex flex-col gap-5">
                {/* header */}
                <motion.div variants={staggerItem} className="flex items-center gap-3">
                  <div className="p-2 bg-indigo-500/10 rounded-lg border border-indigo-500/20">
                    <Terminal className="w-5 h-5 text-indigo-400" />
                  </div>
                  <div>
                    <h2 className="text-lg sm:text-xl font-semibold text-white">Agentic AI</h2>
                    <p className="text-xs sm:text-sm text-neutral-400 mt-0.5">Define a goal — the agent plans and executes it.</p>
                  </div>
                </motion.div>

                {/* model + complexity info */}
                <motion.div variants={staggerItem} className="flex flex-wrap items-center gap-2">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[#161616] border panel-glow text-[11px] font-medium text-neutral-400">
                    <Cpu className="w-3 h-3 text-indigo-400" /> Llama 3.1 8B Instant
                  </span>
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[#161616] border panel-glow text-[11px] font-medium text-neutral-400">
                    <Layers className="w-3 h-3 text-indigo-400" /> Multi-step · Max 8 iterations
                  </span>
                </motion.div>

                {/* input */}
                <motion.section variants={staggerItem} className="bg-[#111] border panel-glow panel-glow-hover rounded-xl p-4 sm:p-5 shadow-sm">
                  <form onSubmit={handleStartAgent} className="flex flex-col gap-3">
                    <label htmlFor="agentGoal" className="text-[11px] font-semibold text-neutral-400 tracking-widest uppercase">Agent Goal</label>
                    <div className="flex flex-col sm:flex-row gap-3">
                      <input
                        id="agentGoal" type="text" value={agentGoal}
                        onChange={(e) => setAgentGoal(e.target.value)}
                        placeholder="e.g. Research our remote work policy and draft a summary email…"
                        className="flex-1 bg-[#161616] border panel-glow rounded-lg px-4 py-2.5 text-white placeholder:text-neutral-600 input-glow panel-glow-hover text-sm transition-all duration-100"
                        disabled={agentLoading || agentStatus?.status === 'running'}
                      />
                      <motion.button
                        type="submit"
                        disabled={!agentGoal.trim() || agentLoading || agentStatus?.status === 'running'}
                        whileHover={hoverScale} whileTap={tapScale}
                        className={`flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-all duration-100 shrink-0 ${
                          !agentGoal.trim() || agentLoading || agentStatus?.status === 'running'
                            ? 'bg-neutral-800 text-neutral-500 cursor-not-allowed'
                            : 'bg-indigo-600 hover:bg-indigo-500 text-white hover:shadow-[0_0_20px_rgba(99,102,241,0.3)]'
                        } ${(agentLoading || agentStatus?.status === 'running') ? 'btn-glow-pulse' : ''}`}
                      >
                        {agentLoading || agentStatus?.status === 'running'
                          ? <><Loader2 className="w-4 h-4 animate-spin" /> Running…</>
                          : <><Play className="w-4 h-4 fill-current" /> Start</>
                        }
                      </motion.button>
                    </div>
                    {agentError && <div className="text-red-400 text-sm px-3 py-2 bg-red-500/10 rounded-md border border-red-500/20">{agentError}</div>}
                  </form>
                </motion.section>
              </motion.div>

              {/* execution trace */}
              <AnimatePresence>
                {agentStatus && (
                  <motion.section
                    initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -6 }}
                    transition={{ duration: 0.15 }}
                    className="bg-[#111] border panel-glow rounded-xl overflow-hidden shadow-sm flex flex-col flex-1 min-h-[350px]"
                  >
                    <div className="flex items-center justify-between px-4 py-3 border-b border-neutral-800 bg-[#161616]">
                      <h3 className="font-medium text-[14px] text-white">Execution Trace</h3>
                      <div className="flex items-center gap-2">
                        {agentStatus.status === 'running' && (
                          <span className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-[11px] font-medium uppercase tracking-wider">
                            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />In Progress
                          </span>
                        )}
                        {agentStatus.status === 'completed' && (
                          <span className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[11px] font-medium uppercase tracking-wider">
                            <CheckCircle2 className="w-3.5 h-3.5" /> Done
                          </span>
                        )}
                        {agentStatus.status === 'failed' && (
                          <span className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-red-500/10 border border-red-500/20 text-red-400 text-[11px] font-medium uppercase tracking-wider">
                            <AlertTriangle className="w-3.5 h-3.5" /> Failed
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="flex flex-col md:flex-row flex-1 overflow-hidden">
                      {/* steps */}
                      <div className="w-full md:w-1/3 border-b md:border-b-0 md:border-r border-neutral-800 bg-[#141414] overflow-y-auto custom-scrollbar p-4">
                        <h4 className="text-[11px] font-semibold text-neutral-500 uppercase tracking-wider mb-3">Live Steps</h4>
                        <div className="flex flex-col gap-2">
                          <AnimatePresence>
                            {agentStatus.steps?.length > 0 ? agentStatus.steps.map((step, idx) => (
                              <motion.div
                                key={idx} layout
                                initial={{ opacity: 0, x: -12 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.12, delay: idx * 0.04 }}
                                className="flex gap-2.5 bg-[#1a1a1a] p-2.5 rounded-lg border panel-glow"
                              >
                                <div className="mt-0.5 shrink-0">
                                  {step.status === 'completed' ? <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                                   : step.status === 'failed' ? <AlertTriangle className="w-4 h-4 text-red-500" />
                                   : <Loader2 className="w-4 h-4 text-indigo-400 animate-spin" />}
                                </div>
                                <div className="min-w-0">
                                  <p className="text-sm font-medium text-neutral-200 truncate">{step.name || `Step ${idx + 1}`}</p>
                                  {step.tool && <p className="text-[11px] text-neutral-500 mt-0.5 font-mono truncate">Tool: {step.tool}</p>}
                                </div>
                              </motion.div>
                            )) : <div className="text-sm text-neutral-500 italic">Initializing…</div>}
                          </AnimatePresence>
                        </div>
                      </div>
                      {/* output */}
                      <div className="w-full md:w-2/3 flex flex-col p-4 sm:p-5 overflow-y-auto custom-scrollbar">
                        <h4 className="text-[11px] font-semibold text-neutral-500 uppercase tracking-wider mb-3">Final Output</h4>
                        {agentStatus.final_result ? (
                          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.15 }} className="text-[14px] text-neutral-300 leading-relaxed whitespace-pre-wrap">
                            {agentStatus.final_result}
                          </motion.div>
                        ) : (
                          <div className="flex-1 flex items-center justify-center"><div className="flex flex-col items-center gap-3 text-neutral-600"><Activity className="w-8 h-8 opacity-30" /><p className="text-sm italic">Working…</p></div></div>
                        )}
                      </div>
                    </div>
                  </motion.section>
                )}
              </AnimatePresence>
            </motion.main>
          )}

          {/* ━━━ EVAL ━━━ */}
          {currentView === 'eval' && (
            <motion.main key="eval" variants={pageVariants} initial="initial" animate="animate" exit="exit" className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8 flex flex-col gap-5">
              <motion.div variants={staggerContainer} initial="initial" animate="animate" className="flex flex-col gap-5">
                {/* input */}
                <motion.section variants={staggerItem} className="bg-[#111] border panel-glow panel-glow-hover rounded-xl p-4 sm:p-5 shadow-sm">
                  <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <div className="flex items-center justify-between flex-wrap gap-2">
                      <label htmlFor="prompt" className="text-[11px] font-semibold text-neutral-400 tracking-widest uppercase">Prompt</label>
                      <button
                        type="button" onClick={() => setUseRag(!useRag)}
                        className={`flex items-center gap-2 px-2.5 py-1.5 rounded-md text-xs font-medium transition-all border ${
                          useRag ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20' : 'bg-neutral-900 text-neutral-500 border-neutral-800 hover:border-neutral-700'
                        }`}
                      >
                        <BookOpen className="w-3.5 h-3.5" /> KB {useRag ? 'ON' : 'OFF'}
                      </button>
                    </div>
                    <textarea
                      id="prompt" value={prompt} onChange={(e) => setPrompt(e.target.value)}
                      placeholder="Type your prompt here… (Enter to run, Shift+Enter for new line)"
                      className="w-full bg-[#161616] border panel-glow rounded-lg p-4 text-white placeholder:text-neutral-600 input-glow panel-glow-hover text-sm leading-relaxed resize-y min-h-[100px] sm:min-h-[120px] transition-all duration-100"
                      disabled={loading}
                      onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); if (prompt.trim() && !loading) handleSubmit(e); } }}
                    />
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                      <div className="flex-1 min-w-0">
                        {error && <span className="text-red-400 text-sm px-3 py-1.5 bg-red-500/10 rounded-md border border-red-500/20 inline-block">{error}</span>}
                      </div>
                      <div className="flex items-center gap-3 shrink-0">
                        {results && (
                          <motion.button type="button" onClick={handleExportCSV} whileHover={hoverScale} whileTap={tapScale}
                            className="flex items-center gap-2 px-3 py-2 bg-[#1a1a1a] hover:bg-[#222] text-neutral-300 rounded-lg text-sm font-medium border panel-glow">
                            <Download className="w-4 h-4" /> Export
                          </motion.button>
                        )}
                        <motion.button type="submit" disabled={!prompt.trim() || loading} whileHover={prompt.trim() && !loading ? hoverScale : {}} whileTap={prompt.trim() && !loading ? tapScale : {}}
                          className={`flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-medium transition-all duration-100 ${
                            !prompt.trim() || loading ? 'bg-neutral-800 text-neutral-500 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-500 text-white hover:shadow-[0_0_20px_rgba(99,102,241,0.3)]'
                          } ${loading ? 'btn-glow-pulse' : ''}`}
                        >
                          {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Running…</> : <><Play className="w-4 h-4 fill-current" /> Evaluate</>}
                        </motion.button>
                      </div>
                    </div>
                  </form>
                </motion.section>

                {/* results */}
                <motion.section variants={staggerItem} className="flex-1 min-h-[300px]">
                  <motion.div variants={staggerContainer} initial="initial" animate="animate" className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-5 h-full">
                    <ResultPanel title={settings.model1Name} data={results?.groq_1} delay={0.1} />
                    <ResultPanel title={settings.model2Name} data={results?.groq_2} delay={0.2} />
                  </motion.div>
                </motion.section>
              </motion.div>
            </motion.main>
          )}

          {/* ━━━ HISTORY ━━━ */}
          {currentView === 'history' && (
            <motion.main key="history" variants={pageVariants} initial="initial" animate="animate" exit="exit" className="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-8 flex flex-col">
              <h2 className="text-lg sm:text-xl font-semibold mb-5 text-white flex items-center gap-2">
                <History className="w-5 h-5 text-neutral-400" /> Evaluation History
              </h2>
              <motion.div variants={staggerContainer} initial="initial" animate="animate" className="flex flex-col gap-3 pb-12">
                {history.length === 0 ? (
                  <motion.div variants={staggerItem} className="text-center py-20 bg-[#111] rounded-xl border panel-glow border-dashed">
                    <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-neutral-800/50 flex items-center justify-center">
                      <Inbox className="w-6 h-6 text-neutral-600" />
                    </div>
                    <p className="text-neutral-400 text-sm font-medium">No history yet</p>
                    <p className="text-neutral-600 text-xs mt-1">Your evaluation results will appear here.</p>
                  </motion.div>
                ) : (
                  history.map(item => (
                    <motion.div key={item.id} variants={staggerItem} whileHover={cardHover} className="bg-[#111] border panel-glow panel-glow-hover rounded-xl p-4 sm:p-5 shadow-sm">
                      <span className="text-[11px] text-neutral-500">{new Date(item.timestamp).toLocaleString()}</span>
                      <div className="text-[14px] text-neutral-300 mt-2 mb-3 bg-[#161616] p-3 rounded-lg border panel-glow/80 leading-relaxed">"{item.prompt}"</div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {[{ m: item.models.model1, d: item.results.groq_1 }, { m: item.models.model2, d: item.results.groq_2 }].map((col, i) => (
                          <div key={i} className="bg-[#161616] p-3 rounded-lg border panel-glow">
                            <div className="text-[11px] text-neutral-400 font-semibold uppercase tracking-wider mb-2 flex items-center justify-between">
                              <span className="truncate">{col.m}</span>
                              <span className="text-neutral-500 font-mono shrink-0 ml-2">{col.d?.latency_ms || 0}ms</span>
                            </div>
                            <div className="text-xs text-neutral-300 leading-relaxed max-h-28 overflow-y-auto custom-scrollbar whitespace-pre-wrap">{col.d?.content || 'Error'}</div>
                          </div>
                        ))}
                      </div>
                    </motion.div>
                  ))
                )}
              </motion.div>
            </motion.main>
          )}

          {/* ━━━ DOCS ━━━ */}
          {currentView === 'documents' && (
            <motion.main key="documents" variants={pageVariants} initial="initial" animate="animate" exit="exit" className="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-8 flex flex-col">
              <h2 className="text-lg sm:text-xl font-semibold mb-5 text-white flex items-center gap-2">
                <FileText className="w-5 h-5 text-neutral-400" /> Knowledge Base
              </h2>

              <motion.div variants={staggerContainer} initial="initial" animate="animate" className="flex flex-col gap-4">
                {/* upload */}
                <motion.div variants={staggerItem}>
                  <label
                    className={`flex flex-col items-center justify-center gap-3 py-8 sm:py-10 bg-[#111] border border-dashed rounded-xl cursor-pointer transition-all ${
                      uploadingDoc ? 'border-indigo-500/50 bg-indigo-500/5' : 'border-neutral-700 hover:border-neutral-600 hover:bg-[#161616]'
                    }`}
                    onDragOver={(e) => { e.preventDefault(); e.stopPropagation(); }}
                    onDrop={(e) => { e.preventDefault(); e.stopPropagation(); const f = e.dataTransfer.files[0]; if (f) handleUploadDoc(f); }}
                  >
                    <input type="file" className="hidden" accept=".txt,.pdf,.md,.csv,.json" onChange={(e) => { const f = e.target.files[0]; if (f) handleUploadDoc(f); }} />
                    {uploadingDoc ? <Loader2 className="w-7 h-7 text-indigo-400 animate-spin" /> : <Upload className="w-7 h-7 text-neutral-500" />}
                    <div className="text-center">
                      <p className="text-sm font-medium text-neutral-300">{uploadingDoc ? 'Uploading…' : 'Drop files here or click to upload'}</p>
                      <p className="text-[11px] text-neutral-500 mt-1">TXT, PDF, MD, CSV, JSON</p>
                    </div>
                  </label>
                </motion.div>

                {/* list */}
                {documents.length === 0 ? (
                  <motion.div variants={staggerItem} className="text-center py-16 bg-[#111] rounded-xl border panel-glow border-dashed">
                    <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-neutral-800/50 flex items-center justify-center">
                      <FileText className="w-6 h-6 text-neutral-600" />
                    </div>
                    <p className="text-neutral-400 text-sm font-medium">No documents uploaded</p>
                    <p className="text-neutral-600 text-xs mt-1">Upload files above to enable RAG-powered evaluations.</p>
                  </motion.div>
                ) : (
                  documents.map((doc, idx) => (
                    <motion.div key={doc.id || idx} variants={staggerItem} whileHover={cardHover}
                      className="bg-[#111] border panel-glow panel-glow-hover rounded-lg p-3.5 shadow-sm flex items-center justify-between gap-3"
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        <div className="p-2 bg-neutral-900 rounded-md border panel-glow shrink-0">
                          <FileText className="w-4 h-4 text-neutral-400" />
                        </div>
                        <div className="min-w-0">
                          <p className="text-sm font-medium text-neutral-200 truncate">{doc.filename}</p>
                          <div className="flex items-center gap-3 mt-0.5">
                            {doc.chunk_count !== undefined && <span className="text-[11px] text-neutral-500">{doc.chunk_count} chunks</span>}
                            {doc.uploaded_at && <span className="text-[11px] text-neutral-500">{new Date(doc.uploaded_at).toLocaleDateString()}</span>}
                          </div>
                        </div>
                      </div>
                      <motion.button onClick={() => handleDeleteDoc(doc.id)} whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}
                        className="p-2 text-neutral-500 hover:text-red-400 hover:bg-red-400/10 rounded-md transition-colors shrink-0">
                        <Trash2 className="w-4 h-4" />
                      </motion.button>
                    </motion.div>
                  ))
                )}
              </motion.div>
            </motion.main>
          )}

          {/* ━━━ SETTINGS ━━━ */}
          {currentView === 'settings' && (
            <motion.main key="settings" variants={pageVariants} initial="initial" animate="animate" exit="exit" className="flex-1 w-full max-w-3xl mx-auto px-4 sm:px-6 py-6 sm:py-8 flex flex-col">
              <h2 className="text-lg sm:text-xl font-semibold mb-5 text-white flex items-center gap-2">
                <Settings className="w-5 h-5 text-neutral-400" /> Settings
              </h2>
              <motion.div variants={staggerContainer} initial="initial" animate="animate" className="bg-[#111] border panel-glow rounded-xl p-5 sm:p-6 shadow-sm">
                <motion.div variants={staggerItem}>
                  <h3 className="text-[15px] font-medium text-white mb-1">Model Configuration</h3>
                  <p className="text-xs text-neutral-500 mb-4">Customize the display names for the AI models.</p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider mb-1.5 block">Model 1</label>
                      <input type="text" value={settings.model1Name} onChange={(e) => setSettings({ ...settings, model1Name: e.target.value })}
                        className="w-full bg-[#161616] border panel-glow rounded-md px-3 py-2 text-sm text-neutral-200 input-glow panel-glow-hover transition-all duration-100" />
                    </div>
                    <div>
                      <label className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider mb-1.5 block">Model 2</label>
                      <input type="text" value={settings.model2Name} onChange={(e) => setSettings({ ...settings, model2Name: e.target.value })}
                        className="w-full bg-[#161616] border panel-glow rounded-md px-3 py-2 text-sm text-neutral-200 input-glow panel-glow-hover transition-all duration-100" />
                    </div>
                  </div>
                </motion.div>
                <motion.div variants={staggerItem} className="pt-5 mt-4 border-t border-neutral-800">
                  <h3 className="text-[15px] font-medium text-white mb-1">Account</h3>
                  <p className="text-xs text-neutral-500 mb-3">Signed in as <span className="text-indigo-400 font-medium">{user}</span></p>
                  <motion.button onClick={handleLogout} whileHover={hoverScale} whileTap={tapScale}
                    className="px-4 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 rounded-md text-sm font-medium transition-colors flex items-center gap-2">
                    <LogOut className="w-4 h-4" /> Sign Out
                  </motion.button>
                </motion.div>
              </motion.div>
            </motion.main>
          )}

        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
