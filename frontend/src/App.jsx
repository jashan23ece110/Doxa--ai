import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Activity, Clock, Zap, History, Settings, Bot, Code2, AlertTriangle, LogOut, CheckCircle2, Play, Download, Loader2, FileText, Upload, Trash2, BookOpen, ChevronDown, ChevronUp, Terminal, Menu, X, Cpu, Layers, Inbox } from 'lucide-react';
import axios from 'axios';

/* ── new Jarvis components ── */
import Dashboard from './components/Dashboard';
import ChatOverlay from './components/ChatOverlay';
import VoiceListener from './components/VoiceListener';

/* ── animation variants (kept for overlay tab views) ── */
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

/* ════════════════════════════════════════════
   MAIN APP
   ════════════════════════════════════════════ */
function App() {
  /* ── state ── */
  const [user, setUser] = useState(() => localStorage.getItem('ai_eval_user'));
  const [authMode, setAuthMode] = useState('login');

  /* overlay state (null = dashboard visible, string = overlay type) */
  const [activeOverlay, setActiveOverlay] = useState(null);
  const [chatVisible, setChatVisible] = useState(false);
  const [sessionStart] = useState(() => new Date());

  const API_BASE = import.meta.env.VITE_API_URL;

  /* eval state */
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [settings, setSettings] = useState({
    model1Name: 'Llama 3.1 8B (Instant)',
    model2Name: 'Llama 3.3 70B (Versatile)',
  });

  /* RAG state */
  const [useRag, setUseRag] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [uploadingDoc, setUploadingDoc] = useState(false);
  const [retrievedContext, setRetrievedContext] = useState(null);
  const [showContext, setShowContext] = useState(false);

  /* agent state */
  const [agentGoal, setAgentGoal] = useState('');
  const [agentLoading, setAgentLoading] = useState(false);
  const [agentRunId, setAgentRunId] = useState(null);
  const [agentStatus, setAgentStatus] = useState(null);
  const [agentError, setAgentError] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voiceFallbackText, setVoiceFallbackText] = useState(null);
  const spokenResultRef = useRef('');
  const synthRef = useRef(window.speechSynthesis);

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
  useEffect(() => { if (activeOverlay === 'documents' && user) fetchDocuments(); }, [activeOverlay, user]);

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
    setVoiceFallbackText(null);
    spokenResultRef.current = '';
    // Auto-close the chat overlay so user sees the sphere
    setChatVisible(false);
    try {
      const res = await fetch(`${API_BASE}/agent/start`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ goal: agentGoal }) });
      if (!res.ok) { const d = await res.json(); throw new Error(d.detail || 'Failed to start agent'); }
      const data = await res.json();
      setAgentRunId(data.run_id);
      setAgentStatus({ status: 'running', steps: [], final_result: null });
    } catch (err) { setAgentError(err.message); setAgentLoading(false); setChatVisible(true); }
  };

  /* ── Voice output: speak final_result when it arrives ── */
  useEffect(() => {
    if (
      agentStatus?.final_result &&
      agentStatus.final_result !== spokenResultRef.current
    ) {
      spokenResultRef.current = agentStatus.final_result;
      const synth = synthRef.current;

      // Check TTS support
      if (!synth || typeof SpeechSynthesisUtterance === 'undefined') {
        // Fallback: show text notification
        setVoiceFallbackText(agentStatus.final_result);
        setTimeout(() => setVoiceFallbackText(null), 15000);
        return;
      }

      const utterance = new SpeechSynthesisUtterance(agentStatus.final_result);
      utterance.rate = 1;
      utterance.pitch = 1;

      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => {
        setIsSpeaking(false);
        // Fallback on TTS error
        setVoiceFallbackText(agentStatus.final_result);
        setTimeout(() => setVoiceFallbackText(null), 15000);
      };

      synth.speak(utterance);
    }
  }, [agentStatus?.final_result]);

  /* ── overlay navigation ── */
  const handleNavigate = (view) => {
    setActiveOverlay(activeOverlay === view ? null : view);
  };

  const closeOverlay = () => setActiveOverlay(null);

  /* ═══════════════════════════════════════════
     SUB-COMPONENTS (for overlay tabs)
     ═══════════════════════════════════════════ */

  /* result panel (eval) */
  const ResultPanel = ({ title, data, delay }) => (
    <motion.div
      variants={staggerItem}
      className="bg-[#141414] border panel-glow rounded-xl flex flex-col overflow-hidden shadow-sm h-full"
    >
      <div className="flex items-center justify-between px-4 py-3 border-b border-[rgba(255,214,10,0.1)] bg-[#0a0a0a]">
        <h3 className="font-medium text-[14px] text-white" style={{ fontFamily: 'Rajdhani, sans-serif' }}>{title}</h3>
        <div className="flex items-center gap-2">
          {data?.latency_ms && (
            <span className="text-[11px] px-2 py-0.5 bg-[#0a0a0a] border panel-glow rounded text-[#7a7060]" style={{ fontFamily: 'JetBrains Mono, monospace' }}>{data.latency_ms}ms</span>
          )}
          {data && (
            <span className={`text-[11px] font-medium px-2 py-0.5 rounded border ${data._useRag ? 'bg-[rgba(255,214,10,0.1)] border-[rgba(255,214,10,0.2)] text-[#ffd60a]' : 'bg-[#0a0a0a] border-[rgba(255,214,10,0.1)] text-[#7a7060]'}`}>
              {data._useRag ? 'RAG' : 'Model'}
            </span>
          )}
        </div>
      </div>
      <div className="flex-1 p-4 overflow-y-auto hud-scrollbar">
        {loading ? <SkeletonLoader /> : data ? (
          data.error
            ? <div className="p-3 bg-[rgba(255,51,102,0.1)] border border-[rgba(255,51,102,0.2)] rounded text-[#ff3366] text-sm">Error: {data.error}</div>
            : <div className="text-[14px] text-[#e0d6c2] leading-relaxed whitespace-pre-wrap" style={{ fontFamily: 'Rajdhani, sans-serif' }}>{data.content}</div>
        ) : (
          <div className="h-full flex items-center justify-center text-[#7a7060] italic text-sm">Awaiting evaluation…</div>
        )}
      </div>

      {/* context drawer */}
      <AnimatePresence>
        {retrievedContext?.length > 0 && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="border-t border-[rgba(255,214,10,0.1)] overflow-hidden">
            <button onClick={() => setShowContext(!showContext)} className="w-full flex items-center justify-between px-4 py-2 text-[12px] text-[#7a7060] hover:bg-[#141414] transition-colors">
              <span className="flex items-center gap-1.5"><BookOpen className="w-3.5 h-3.5" /> Context ({retrievedContext.length})</span>
              {showContext ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
            <AnimatePresence>
              {showContext && (
                <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="flex flex-col gap-2 px-4 pb-3 max-h-44 overflow-y-auto hud-scrollbar">
                  {retrievedContext.map((c, i) => (
                    <div key={i} className="p-2.5 bg-[#0a0a0a] rounded border panel-glow text-[12px]">
                      <div className="flex justify-between mb-1">
                        <span className="text-[#ffd60a] font-medium flex items-center gap-1"><FileText className="w-3 h-3" />{c.filename || 'Unknown'}</span>
                        <span className="text-[#7a7060]" style={{ fontFamily: 'JetBrains Mono, monospace' }}>{c.similarity ? `${(c.similarity * 100).toFixed(1)}%` : ''}</span>
                      </div>
                      <p className="text-[#e0d6c2] leading-relaxed whitespace-pre-wrap">{c.text}</p>
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
      <div className="min-h-screen bg-[#0a0a0a] flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8 selection:bg-[rgba(255,214,10,0.2)]" style={{ fontFamily: 'Rajdhani, sans-serif' }}>
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }} className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="flex justify-center mb-6">
            <div className="p-3 bg-[#141414] rounded-xl border panel-glow"><Sparkles className="w-8 h-8 text-[#ffd60a]" /></div>
          </div>
          <h2 className="text-center text-2xl font-bold text-white" style={{ fontFamily: 'Orbitron, sans-serif' }}>DOXA</h2>
          <p className="mt-2 text-center text-sm text-[#7a7060]">
            {authMode === 'login' && 'Sign in to your account'}
            {authMode === 'signup' && 'Create an account to get started'}
            {authMode === 'phone' && 'Enter your phone number'}
            {authMode === 'otp' && 'Enter the verification code'}
          </p>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.06, duration: 0.2 }} className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="hud-panel py-8 px-4 sm:rounded-xl sm:px-10">
            <form className="space-y-6" onSubmit={handleAuth}>
              {(authMode === 'login' || authMode === 'signup') && (
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-[#e0d6c2]">Email address</label>
                  <input id="email" name="email" type="email" required className="mt-1 block w-full px-3 py-2.5 border panel-glow rounded-lg bg-[#141414] text-white placeholder-[#7a7060] input-glow sm:text-sm" style={{ fontFamily: 'JetBrains Mono, monospace' }} />
                </div>
              )}
              {authMode === 'phone' && (
                <div>
                  <label htmlFor="phone" className="block text-sm font-medium text-[#e0d6c2]">Phone number</label>
                  <input id="phone" name="phone" type="tel" required className="mt-1 block w-full px-3 py-2.5 border panel-glow rounded-lg bg-[#141414] text-white placeholder-[#7a7060] input-glow sm:text-sm" style={{ fontFamily: 'JetBrains Mono, monospace' }} />
                </div>
              )}
              {authMode === 'otp' && (
                <div>
                  <label htmlFor="otp" className="block text-sm font-medium text-[#e0d6c2]">Verification Code</label>
                  <input id="otp" name="otp" type="text" required placeholder="123456" className="mt-1 block w-full px-3 py-2.5 border panel-glow rounded-lg bg-[#141414] text-white placeholder-[#7a7060] input-glow sm:text-sm text-center tracking-widest text-lg" style={{ fontFamily: 'JetBrains Mono, monospace' }} />
                </div>
              )}
              <motion.button type="submit" whileHover={hoverScale} whileTap={tapScale} className="w-full py-2.5 px-4 rounded-lg text-sm font-bold text-[#0a0a0a] bg-[#ffd60a] hover:bg-[#ffe44d] hover:shadow-[0_0_25px_rgba(255,214,10,0.4)] transition-all duration-100" style={{ fontFamily: 'Orbitron, sans-serif', letterSpacing: '0.1em' }}>
                {authMode === 'login' ? 'SIGN IN' : authMode === 'signup' ? 'CREATE ACCOUNT' : authMode === 'phone' ? 'SEND CODE' : 'VERIFY'}
              </motion.button>
            </form>

            <div className="mt-6">
              <div className="relative"><div className="absolute inset-0 flex items-center"><div className="w-full border-t border-[rgba(255,214,10,0.1)]" /></div><div className="relative flex justify-center text-sm"><span className="px-2 bg-[#0a0a0a] text-[#7a7060]">Or continue with</span></div></div>
              <div className="mt-6 grid grid-cols-2 gap-3">
                <button type="button" onClick={() => setAuthMode('phone')} className="w-full py-2 px-4 border panel-glow rounded-lg bg-[#141414] text-sm font-medium text-[#e0d6c2] hover:bg-[#1e1e1e] transition-colors">Phone</button>
                <button type="button" onClick={() => setAuthMode(authMode === 'login' ? 'signup' : 'login')} className="w-full py-2 px-4 border panel-glow rounded-lg bg-[#141414] text-sm font-medium text-[#e0d6c2] hover:bg-[#1e1e1e] transition-colors">
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
     MAIN LAYOUT — Dashboard + Overlays
     ═══════════════════════════════════════════ */
  return (
    <div className="h-screen w-screen bg-[#0a0a0a] overflow-hidden relative" style={{ fontFamily: 'Rajdhani, sans-serif' }}>

      {/* ── Voice Listener (always active) ── */}
      <VoiceListener
        onActivate={() => setChatVisible(true)}
        onDeactivate={() => setChatVisible(false)}
      />

      {/* ── Dashboard (always rendered) ── */}
      <Dashboard
        user={user}
        agentLoading={agentLoading}
        agentStatus={agentStatus}
        isSpeaking={isSpeaking}
        queriesCount={history.length}
        sessionStart={sessionStart}
        activeOverlay={activeOverlay}
        onNavigate={handleNavigate}
        onOpenChat={() => setChatVisible(true)}
      />

      {/* ── Chat Overlay (hidden by default) ── */}
      <ChatOverlay
        visible={chatVisible}
        onClose={() => setChatVisible(false)}
        agentGoal={agentGoal}
        setAgentGoal={setAgentGoal}
        agentLoading={agentLoading}
        agentStatus={agentStatus}
        agentError={agentError}
        onStartAgent={handleStartAgent}
      />

      {/* Voice fallback notification */}
      <AnimatePresence>
        {voiceFallbackText && (
          <motion.div
            key="voice-fallback"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 40 }}
            transition={{ duration: 0.3 }}
            style={{
              position: 'fixed',
              bottom: '24px',
              left: '50%',
              transform: 'translateX(-50%)',
              zIndex: 100,
              maxWidth: '560px',
              width: '90%',
              padding: '16px 20px',
              borderRadius: '14px',
              border: '1px solid rgba(255, 214, 10, 0.2)',
              background: 'linear-gradient(145deg, rgba(10, 18, 36, 0.96), rgba(6, 12, 28, 0.98))',
              backdropFilter: 'blur(12px)',
              boxShadow: '0 0 30px rgba(255, 214, 10, 0.1)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ fontFamily: "'Orbitron', sans-serif", fontSize: '10px', color: '#ffd60a', letterSpacing: '0.12em', textTransform: 'uppercase' }}>Voice not supported — showing text</span>
              <button onClick={() => setVoiceFallbackText(null)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', padding: '2px', display: 'flex' }}>
                <X className="w-4 h-4" style={{ color: '#7a7060' }} />
              </button>
            </div>
            <pre style={{ fontFamily: "'Rajdhani', sans-serif", fontSize: '13px', color: '#e0d6c2', lineHeight: 1.6, margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-word', maxHeight: '200px', overflowY: 'auto' }}>{voiceFallbackText}</pre>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Tab Overlays (Eval, Docs, History, Settings) ── */}
      <AnimatePresence>
        {activeOverlay && (
          <motion.div
            key="tab-overlay-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 z-40 chat-backdrop flex items-center justify-center p-4"
            onClick={closeOverlay}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              transition={{ duration: 0.25, ease: [0.25, 0.1, 0.25, 1] }}
              className="hud-panel hud-panel-bright w-full max-w-5xl max-h-[85vh] overflow-hidden flex flex-col"
              onClick={(e) => e.stopPropagation()}
            >
              {/* overlay header */}
              <div className="flex items-center justify-between px-5 py-3 border-b border-[rgba(255,214,10,0.15)]">
                <h2 className="text-sm font-bold text-[#ffd60a] uppercase tracking-[0.15em]" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                  {activeOverlay === 'eval' && 'MODEL EVALUATION'}
                  {activeOverlay === 'documents' && 'KNOWLEDGE BASE'}
                  {activeOverlay === 'history' && 'EVALUATION HISTORY'}
                  {activeOverlay === 'settings' && 'SYSTEM CONFIG'}
                </h2>
                <button onClick={closeOverlay} className="p-1.5 text-[#7a7060] hover:text-white transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* overlay content */}
              <div className="flex-1 overflow-y-auto hud-scrollbar p-5">

                {/* ━━━ EVAL ━━━ */}
                {activeOverlay === 'eval' && (
                  <motion.div variants={staggerContainer} initial="initial" animate="animate" className="flex flex-col gap-5">
                    <motion.section variants={staggerItem} className="hud-panel p-4 sm:p-5">
                      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                        <div className="flex items-center justify-between flex-wrap gap-2">
                          <label htmlFor="prompt" className="text-[11px] font-semibold text-[#7a7060] tracking-widest uppercase" style={{ fontFamily: 'Orbitron, sans-serif' }}>Prompt</label>
                          <button
                            type="button" onClick={() => setUseRag(!useRag)}
                            className={`flex items-center gap-2 px-2.5 py-1.5 rounded-md text-xs font-medium transition-all border ${
                              useRag ? 'bg-[rgba(255,214,10,0.1)] text-[#ffd60a] border-[rgba(255,214,10,0.2)]' : 'bg-[#141414] text-[#7a7060] border-[rgba(255,214,10,0.1)] hover:border-[rgba(255,214,10,0.2)]'
                            }`}
                          >
                            <BookOpen className="w-3.5 h-3.5" /> KB {useRag ? 'ON' : 'OFF'}
                          </button>
                        </div>
                        <textarea
                          id="prompt" value={prompt} onChange={(e) => setPrompt(e.target.value)}
                          placeholder="Type your prompt here…"
                          className="w-full bg-[#141414] border panel-glow rounded-lg p-4 text-white placeholder:text-[#7a7060] input-glow text-sm leading-relaxed resize-y min-h-[100px] transition-all duration-100"
                          style={{ fontFamily: 'Rajdhani, sans-serif' }}
                          disabled={loading}
                          onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); if (prompt.trim() && !loading) handleSubmit(e); } }}
                        />
                        <div className="flex justify-between items-center gap-3">
                          <div className="flex-1 min-w-0">
                            {error && <span className="text-[#ff3366] text-sm px-3 py-1.5 bg-[rgba(255,51,102,0.1)] rounded-md border border-[rgba(255,51,102,0.2)] inline-block">{error}</span>}
                          </div>
                          <div className="flex items-center gap-3 shrink-0">
                            {results && (
                              <motion.button type="button" onClick={handleExportCSV} whileHover={hoverScale} whileTap={tapScale}
                                className="flex items-center gap-2 px-3 py-2 bg-[#141414] hover:bg-[#1e1e1e] text-[#e0d6c2] rounded-lg text-sm font-medium border panel-glow">
                                <Download className="w-4 h-4" /> Export
                              </motion.button>
                            )}
                            <motion.button type="submit" disabled={!prompt.trim() || loading} whileHover={prompt.trim() && !loading ? hoverScale : {}} whileTap={prompt.trim() && !loading ? tapScale : {}}
                              className={`flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-bold transition-all duration-100 ${
                                !prompt.trim() || loading ? 'bg-[#1e1e1e] text-[#7a7060] cursor-not-allowed' : 'bg-[#ffd60a] hover:bg-[#ffe44d] text-[#0a0a0a] hover:shadow-[0_0_25px_rgba(255,214,10,0.4)]'
                              } ${loading ? 'btn-glow-pulse' : ''}`}
                              style={{ fontFamily: 'Orbitron, sans-serif', letterSpacing: '0.1em' }}
                            >
                              {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> RUNNING…</> : <><Play className="w-4 h-4 fill-current" /> EVALUATE</>}
                            </motion.button>
                          </div>
                        </div>
                      </form>
                    </motion.section>

                    <motion.section variants={staggerItem} className="flex-1 min-h-[300px]">
                      <motion.div variants={staggerContainer} initial="initial" animate="animate" className="grid grid-cols-1 lg:grid-cols-2 gap-4 h-full">
                        <ResultPanel title={settings.model1Name} data={results?.groq_1} delay={0.1} />
                        <ResultPanel title={settings.model2Name} data={results?.groq_2} delay={0.2} />
                      </motion.div>
                    </motion.section>
                  </motion.div>
                )}

                {/* ━━━ DOCUMENTS ━━━ */}
                {activeOverlay === 'documents' && (
                  <motion.div variants={staggerContainer} initial="initial" animate="animate" className="flex flex-col gap-4">
                    <motion.div variants={staggerItem}>
                      <label
                        className={`flex flex-col items-center justify-center gap-3 py-8 sm:py-10 hud-panel border-dashed cursor-pointer transition-all ${
                          uploadingDoc ? 'border-[rgba(255,214,10,0.5)] bg-[rgba(255,214,10,0.05)]' : 'hover:border-[rgba(255,214,10,0.3)] hover:bg-[#141414]'
                        }`}
                        onDragOver={(e) => { e.preventDefault(); e.stopPropagation(); }}
                        onDrop={(e) => { e.preventDefault(); e.stopPropagation(); const f = e.dataTransfer.files[0]; if (f) handleUploadDoc(f); }}
                      >
                        <input type="file" className="hidden" accept=".txt,.pdf,.md,.csv,.json" onChange={(e) => { const f = e.target.files[0]; if (f) handleUploadDoc(f); }} />
                        {uploadingDoc ? <Loader2 className="w-7 h-7 text-[#ffd60a] animate-spin" /> : <Upload className="w-7 h-7 text-[#7a7060]" />}
                        <div className="text-center">
                          <p className="text-sm font-medium text-[#e0d6c2]">{uploadingDoc ? 'Uploading…' : 'Drop files here or click to upload'}</p>
                          <p className="text-[11px] text-[#7a7060] mt-1" style={{ fontFamily: 'JetBrains Mono, monospace' }}>TXT, PDF, MD, CSV, JSON</p>
                        </div>
                      </label>
                    </motion.div>

                    {documents.length === 0 ? (
                      <motion.div variants={staggerItem} className="text-center py-16 hud-panel border-dashed">
                        <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-[#141414] flex items-center justify-center">
                          <FileText className="w-6 h-6 text-[#7a7060]" />
                        </div>
                        <p className="text-[#e0d6c2] text-sm font-medium">No documents uploaded</p>
                        <p className="text-[#7a7060] text-xs mt-1">Upload files to enable RAG-powered evaluations.</p>
                      </motion.div>
                    ) : (
                      documents.map((doc, idx) => (
                        <motion.div key={doc.id || idx} variants={staggerItem} whileHover={cardHover}
                          className="hud-panel p-3.5 flex items-center justify-between gap-3"
                        >
                          <div className="flex items-center gap-3 min-w-0">
                            <div className="p-2 bg-[#141414] rounded-md border panel-glow shrink-0">
                              <FileText className="w-4 h-4 text-[#7a7060]" />
                            </div>
                            <div className="min-w-0">
                              <p className="text-sm font-medium text-[#e0d6c2] truncate">{doc.filename}</p>
                              <div className="flex items-center gap-3 mt-0.5">
                                {doc.chunk_count !== undefined && <span className="text-[11px] text-[#7a7060]" style={{ fontFamily: 'JetBrains Mono, monospace' }}>{doc.chunk_count} chunks</span>}
                                {doc.uploaded_at && <span className="text-[11px] text-[#7a7060]">{new Date(doc.uploaded_at).toLocaleDateString()}</span>}
                              </div>
                            </div>
                          </div>
                          <motion.button onClick={() => handleDeleteDoc(doc.id)} whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}
                            className="p-2 text-[#7a7060] hover:text-[#ff3366] hover:bg-[rgba(255,51,102,0.1)] rounded-md transition-colors shrink-0">
                            <Trash2 className="w-4 h-4" />
                          </motion.button>
                        </motion.div>
                      ))
                    )}
                  </motion.div>
                )}

                {/* ━━━ HISTORY ━━━ */}
                {activeOverlay === 'history' && (
                  <motion.div variants={staggerContainer} initial="initial" animate="animate" className="flex flex-col gap-3">
                    {history.length === 0 ? (
                      <motion.div variants={staggerItem} className="text-center py-20 hud-panel border-dashed">
                        <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-[#141414] flex items-center justify-center">
                          <Inbox className="w-6 h-6 text-[#7a7060]" />
                        </div>
                        <p className="text-[#e0d6c2] text-sm font-medium">No history yet</p>
                        <p className="text-[#7a7060] text-xs mt-1">Your evaluation results will appear here.</p>
                      </motion.div>
                    ) : (
                      history.map(item => (
                        <motion.div key={item.id} variants={staggerItem} whileHover={cardHover} className="hud-panel p-4 sm:p-5">
                          <span className="text-[11px] text-[#7a7060]" style={{ fontFamily: 'JetBrains Mono, monospace' }}>{new Date(item.timestamp).toLocaleString()}</span>
                          <div className="text-[14px] text-[#e0d6c2] mt-2 mb-3 bg-[#0a0a0a] p-3 rounded-lg border panel-glow leading-relaxed">"{item.prompt}"</div>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {[{ m: item.models.model1, d: item.results.groq_1 }, { m: item.models.model2, d: item.results.groq_2 }].map((col, i) => (
                              <div key={i} className="bg-[#0a0a0a] p-3 rounded-lg border panel-glow">
                                <div className="text-[11px] text-[#7a7060] font-semibold uppercase tracking-wider mb-2 flex items-center justify-between">
                                  <span className="truncate">{col.m}</span>
                                  <span className="text-[#7a7060] shrink-0 ml-2" style={{ fontFamily: 'JetBrains Mono, monospace' }}>{col.d?.latency_ms || 0}ms</span>
                                </div>
                                <div className="text-xs text-[#e0d6c2] leading-relaxed max-h-28 overflow-y-auto hud-scrollbar whitespace-pre-wrap">{col.d?.content || 'Error'}</div>
                              </div>
                            ))}
                          </div>
                        </motion.div>
                      ))
                    )}
                  </motion.div>
                )}

                {/* ━━━ SETTINGS ━━━ */}
                {activeOverlay === 'settings' && (
                  <motion.div variants={staggerContainer} initial="initial" animate="animate" className="flex flex-col gap-5">
                    <motion.div variants={staggerItem}>
                      <h3 className="text-[15px] font-medium text-white mb-1" style={{ fontFamily: 'Rajdhani, sans-serif' }}>Model Configuration</h3>
                      <p className="text-xs text-[#7a7060] mb-4">Customize the display names for the AI models.</p>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-[11px] font-semibold text-[#7a7060] uppercase tracking-wider mb-1.5 block" style={{ fontFamily: 'Orbitron, sans-serif' }}>Model 1</label>
                          <input type="text" value={settings.model1Name} onChange={(e) => setSettings({ ...settings, model1Name: e.target.value })}
                            className="w-full bg-[#141414] border panel-glow rounded-md px-3 py-2 text-sm text-[#e0d6c2] input-glow transition-all duration-100" style={{ fontFamily: 'JetBrains Mono, monospace' }} />
                        </div>
                        <div>
                          <label className="text-[11px] font-semibold text-[#7a7060] uppercase tracking-wider mb-1.5 block" style={{ fontFamily: 'Orbitron, sans-serif' }}>Model 2</label>
                          <input type="text" value={settings.model2Name} onChange={(e) => setSettings({ ...settings, model2Name: e.target.value })}
                            className="w-full bg-[#141414] border panel-glow rounded-md px-3 py-2 text-sm text-[#e0d6c2] input-glow transition-all duration-100" style={{ fontFamily: 'JetBrains Mono, monospace' }} />
                        </div>
                      </div>
                    </motion.div>
                    <motion.div variants={staggerItem} className="pt-5 mt-4 border-t border-[rgba(255,214,10,0.1)]">
                      <h3 className="text-[15px] font-medium text-white mb-1">Account</h3>
                      <p className="text-xs text-[#7a7060] mb-3">Signed in as <span className="text-[#ffd60a] font-medium">{user}</span></p>
                      <motion.button onClick={handleLogout} whileHover={hoverScale} whileTap={tapScale}
                        className="px-4 py-2 bg-[rgba(255,51,102,0.1)] hover:bg-[rgba(255,51,102,0.2)] text-[#ff3366] border border-[rgba(255,51,102,0.2)] rounded-md text-sm font-medium transition-colors flex items-center gap-2">
                        <LogOut className="w-4 h-4" /> Sign Out
                      </motion.button>
                    </motion.div>
                  </motion.div>
                )}

              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
