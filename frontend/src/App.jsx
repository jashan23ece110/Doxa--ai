// force rebuild v2
import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Activity, Clock, Zap, History, Settings, Bot, Code2, AlertTriangle, LogOut, CheckCircle2, Play, Download, Loader2, FileText, Upload, Trash2, BookOpen, ChevronDown, ChevronUp, Terminal, Menu, X, Cpu, Layers, Inbox, Paintbrush, MessageSquare } from 'lucide-react';
import axios from 'axios';

/* ── new Jarvis components ── */
import Dashboard from './components/Dashboard';
import ChatPanel from './components/ChatPanel';
import VoiceListener from './components/VoiceListener';
import VoiceTelemetry from './components/VoiceTelemetry';
import NeuralBackground from './components/NeuralBackground';
import EmergentAnswerCard from './components/EmergentAnswerCard';
import LibreSidebar from './components/LibreSidebar';
import LandingPage from './landing/LandingPage';
import doxaLogoAsset from './assets/logo.png';
import { THEMES } from './theme';

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

  /* Landing Page vs Working Chat App Route State */
  const [viewMode, setViewMode] = useState(() => {
    if (typeof window !== 'undefined') {
      return (window.location.hash === '#app' || window.location.pathname === '/app') ? 'app' : 'landing';
    }
    return 'landing';
  });

  /* overlay state (null = dashboard visible, string = overlay type) */
  const [activeOverlay, setActiveOverlay] = useState(null);
  const [chatVisible, setChatVisible] = useState(false);
  const [sessionStart] = useState(() => new Date());
  const [sphereMode, setSphereMode] = useState(false);
  const [micPermissionDenied, setMicPermissionDenied] = useState(false);

  const API_BASE = import.meta.env.VITE_API_URL;
  axios.defaults.headers.common['X-Daytona-Skip-Preview-Warning'] = 'true';

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

  /* Theme configuration */
  const [theme, setTheme] = useState(() => localStorage.getItem('doxa_theme') || 'ultron');

  useEffect(() => {
    const t = theme === 'aether' ? THEMES.aether : THEMES.ultron;
    const root = document.documentElement;
    root.style.setProperty('--jarvis-accent', t.accent);
    root.style.setProperty('--jarvis-accent-hover', t.accentHover);
    root.style.setProperty('--jarvis-accent-rgb', t.accentRgb);
    root.style.setProperty('--jarvis-accent-hover-rgb', t.accentHoverRgb);
    root.style.setProperty('--jarvis-bg', t.bg);
    root.style.setProperty('--jarvis-surface', t.surface);
    root.style.setProperty('--jarvis-panel', t.panel);
    root.style.setProperty('--jarvis-border', t.border);
    root.style.setProperty('--jarvis-border-bright', t.borderBright);
    root.style.setProperty('--jarvis-text', t.text);
    root.style.setProperty('--jarvis-text-dim', t.textDim);
    localStorage.setItem('doxa_theme', theme);
  }, [theme]);



  /* RAG state */
  const [useRag, setUseRag] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [docSearchQuery, setDocSearchQuery] = useState('');
  const [activeAlerts, setActiveAlerts] = useState([]);
  const [uploadingDoc, setUploadingDoc] = useState(false);
  const [retrievedContext, setRetrievedContext] = useState(null);
  const [showContext, setShowContext] = useState(false);

  /* agent state */
  const [agentGoal, setAgentGoal] = useState('');
  const [agentLoading, setAgentLoading] = useState(false);
  const [agentRunId, setAgentRunId] = useState(null);
  const [agentStatus, setAgentStatus] = useState(null);
  const [agentError, setAgentError] = useState(null);
  const [sentiment, setSentiment] = useState('neutral');
  const [isDebating, setIsDebating] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voiceFallbackText, setVoiceFallbackText] = useState(null);
  const spokenResultRef = useRef('');
  const synthRef = useRef(window.speechSynthesis);

  const [chatMode, setChatMode] = useState('ask');
  const [language, setLanguage] = useState(() => localStorage.getItem('doxa_language') || 'english');
  
  // Conversational Sessions Management
  const [sessions, setSessions] = useState(() => {
    const saved = localStorage.getItem('doxa_sessions');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.error("Error loading sessions from storage", e);
      }
    }
    const defaultSessionId = 'session_' + Date.now();
    return [{
      id: defaultSessionId,
      title: 'New Conversation',
      history: [],
      timestamp: new Date().toISOString()
    }];
  });

  const [currentSessionId, setCurrentSessionId] = useState(() => {
    const saved = localStorage.getItem('doxa_current_session_id');
    if (saved) return saved;
    return sessions[0]?.id || 'session_' + Date.now();
  });

  const [sidebarOpen, setSidebarOpen] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('doxa_sidebar_open');
      if (saved !== null) return JSON.parse(saved);
      return window.innerWidth >= 768; // open by default on desktop
    }
    return false;
  });

  useEffect(() => {
    localStorage.setItem('doxa_sidebar_open', JSON.stringify(sidebarOpen));
  }, [sidebarOpen]);

  const [chatHistory, setChatHistory] = useState([]);
  const [activeMessageId, setActiveMessageId] = useState(null);
  const [proactiveSuggestions, setProactiveSuggestions] = useState([]);
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
  };
  
  // Auto-dismiss toast effect
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(null), 4000);
    return () => clearTimeout(timer);
  }, [toast]);

  // Fetch proactive ambient suggestions from backend
  const fetchSuggestions = async (historyList) => {
    if (!historyList || historyList.length === 0) return;
    try {
      const getActiveChain = () => {
        if (!activeMessageId || !Array.isArray(historyList)) return [];
        const chain = [];
        let current = historyList.find(m => m && m.id === activeMessageId);
        const visited = new Set();
        while (current && !visited.has(current.id)) {
          visited.add(current.id);
          chain.unshift(current);
          current = historyList.find(m => m && m.id === current.parentId);
        }
        return chain;
      };
      const activeChain = getActiveChain();
      if (activeChain.length === 0) return;

      const res = await fetch(`${API_BASE}/agent/proactive_suggestions`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-Daytona-Skip-Preview-Warning': 'true'
        },
        body: JSON.stringify({
          history: activeChain.map(m => ({ role: m.role, text: m.text })),
          language: language
        })
      });
      if (res.ok) {
        const data = await res.json();
        setProactiveSuggestions(data.suggestions || []);
      }
    } catch (e) {
      console.error("Failed to fetch suggestions:", e);
    }
  };

  // Clear suggestions on session switch
  useEffect(() => {
    setProactiveSuggestions([]);
  }, [currentSessionId]);

  // Sync active session's history to chatHistory
  useEffect(() => {
    const active = sessions.find(s => s.id === currentSessionId);
    if (active) {
      let history = active.history || [];
      let modified = false;
      
      // Auto-assign IDs and parent IDs if they are missing (for legacy history support)
      history = history.map((msg, idx) => {
        let updated = { ...msg };
        if (!updated.id) {
          updated.id = 'legacy_' + idx + '_' + Date.now();
          modified = true;
        }
        if (idx > 0 && !updated.parentId) {
          updated.parentId = history[idx - 1].id;
          modified = true;
        }
        return updated;
      });

      setChatHistory(history);
      if (history.length > 0) {
        setActiveMessageId(active.activeMessageId || history[history.length - 1].id);
      } else {
        setActiveMessageId(null);
      }

      if (modified) {
        setSessions(prev =>
          prev.map(s =>
            s.id === currentSessionId ? { ...s, history } : s
          )
        );
      }
    } else {
      setChatHistory([]);
      setActiveMessageId(null);
    }
  }, [currentSessionId]);

  // Sync real-time chatHistory changes back to session list
  useEffect(() => {
    setSessions(prev =>
      prev.map(s => {
        if (s.id !== currentSessionId) return s;
        let title = s.title;
        // Auto-assign title based on the first user message if title is default
        if ((title === 'New Conversation' || !title) && chatHistory.length > 0) {
          const firstUserMsg = chatHistory.find(m => m && m.role === 'user');
          if (firstUserMsg && firstUserMsg.text) {
            title = firstUserMsg.text.substring(0, 24) + (firstUserMsg.text.length > 24 ? '...' : '');
          }
        }
        return { ...s, history: chatHistory, activeMessageId, title };
      })
    );
  }, [chatHistory, currentSessionId, activeMessageId]);

  // Persist sessions and active session ID to localStorage
  useEffect(() => {
    localStorage.setItem('doxa_sessions', JSON.stringify(sessions));
    localStorage.setItem('doxa_current_session_id', currentSessionId);
  }, [sessions, currentSessionId]);

  const handleLanguageChange = (lang) => {
    setLanguage(lang);
    localStorage.setItem('doxa_language', lang);
  };

  const handleExportChat = () => {
    if (chatHistory.length === 0) {
      showToast("No conversation to export.", "info");
      return;
    }
    const mdContent = chatHistory.map(msg => {
      const header = msg.role === 'user' ? '## User' : '## Doxa (Assistant)';
      return `${header} [${msg.mode || 'normal'}]\n\n${msg.text}\n\n---\n`;
    }).join('\n');
    
    const blob = new Blob([mdContent], { type: 'text/markdown;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', `doxa_conversation_${currentSessionId}.md`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast("Conversation exported!", "success");
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
  useEffect(() => { if (activeOverlay === 'documents' && user) fetchDocuments(); }, [activeOverlay, user]);

  const handleUploadDoc = async (file) => {
    if (!file) return;
    
    // File format validation
    const allowedExtensions = ['.txt', '.pdf', '.md', '.csv', '.json'];
    const fileName = file.name || '';
    const fileExtension = fileName.substring(fileName.lastIndexOf('.')).toLowerCase();
    if (!allowedExtensions.includes(fileExtension)) {
      showToast('Unsupported file format. Please upload TXT, PDF, MD, CSV, or JSON.', 'error');
      return;
    }

    setUploadingDoc(true);
    const fd = new FormData(); fd.append('file', file);
    try { 
      await axios.post(`${API_BASE}/documents/upload`, fd, { headers: { 'Content-Type': 'multipart/form-data' } }); 
      await fetchDocuments(); 
      showToast('Document uploaded successfully!', 'success');
    }
    catch (err) { 
      showToast('Failed to upload document.', 'error'); 
    }
    finally { setUploadingDoc(false); }
  };
  const handleDeleteDoc = async (docId) => {
    if (!window.confirm('Delete this document?')) return;
    try { 
      await axios.delete(`${API_BASE}/documents/${docId}`); 
      await fetchDocuments(); 
      showToast('Document deleted.', 'info');
    } catch {
      showToast('Failed to delete document.', 'error');
    }
  };

  /* ── eval ── */
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    setLoading(true); setError(null); setResults(null); setRetrievedContext(null); setShowContext(false);
    try {
      const res = await fetch(`${API_BASE}/evaluate`, { 
        method: 'POST', 
        headers: { 
          'Content-Type': 'application/json',
          'X-Daytona-Skip-Preview-Warning': 'true'
        }, 
        body: JSON.stringify({ prompt, use_rag: useRag }) 
      });
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
  /* ── agent polling loop ── */
  useEffect(() => {
    let intervalId;
    if (agentRunId) {
      setAgentLoading(true);
      
      const pollStatus = async () => {
        try {
          const res = await fetch(`${API_BASE}/agent/status/${agentRunId}`, {
            headers: {
              'X-Daytona-Skip-Preview-Warning': 'true'
            }
          });
          if (res.status === 404) {
            setAgentError('Run ID not found');
            setAgentLoading(false);
            if (intervalId) clearInterval(intervalId);
            return;
          }
          if (!res.ok) return;

          const data = await res.json();

          if (data.sentiment) {
            setSentiment(data.sentiment);
          }
          if (data.is_debating !== undefined) {
            setIsDebating(data.is_debating);
          }

          setAgentStatus({
            status: data.status,
            plan: data.plan || [],
            steps: data.steps || [],
            self_check: data.self_check,
            error: data.error,
            final_result: data.final_result || "",
            debate_a: data.debate_a || "",
            debate_b: data.debate_b || ""
          });

          if (data.status === 'completed' || data.status === 'failed') {
            setAgentLoading(false);
            if (intervalId) clearInterval(intervalId);
            if (data.status === 'failed') {
              setAgentError(`Agent Execution Failed: ${data.error || 'Unknown error'}`);
            } else {
              setTimeout(() => {
                fetchSuggestions(chatHistory);
              }, 500);
            }
          }
        } catch (err) {
          console.error("Error polling agent status:", err);
        }
      };

      pollStatus();
      intervalId = setInterval(pollStatus, 800);
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [agentRunId, API_BASE]);

  const handleStartAgent = async (eOrGoal) => {
    let goalToSend = agentGoal;
    if (typeof eOrGoal === 'string') {
      goalToSend = eOrGoal;
    } else if (eOrGoal && eOrGoal.preventDefault) {
      eOrGoal.preventDefault();
    }
    if (!goalToSend.trim()) return;
    setAgentLoading(true); setAgentError(null); setAgentRunId(null); setAgentStatus(null);
    setSentiment('neutral');
    setIsDebating(false);
    setVoiceFallbackText(null);
    spokenResultRef.current = '';
    
    // Resolve active message chain for LLM memory context
    const getActiveChain = () => {
      if (!activeMessageId) return [];
      const chain = [];
      let current = chatHistory.find(m => m.id === activeMessageId);
      while (current) {
        chain.unshift(current);
        current = chatHistory.find(m => m.id === current.parentId);
      }
      return chain;
    };
    const activeChain = getActiveChain();
    const historyPayload = activeChain.map(msg => ({
      role: msg.role,
      text: msg.text
    }));

    // Add user query to chat history
    const userMsgId = Date.now();
    const userMsg = { 
      id: userMsgId, 
      parentId: activeMessageId, 
      role: 'user', 
      text: goalToSend, 
      mode: chatMode 
    };
    
    setChatHistory(prev => [...prev, userMsg]);
    setActiveMessageId(userMsgId);
    setAgentGoal(''); // clear the input

    try {
      const res = await fetch(`${API_BASE}/agent/start`, { 
          method: 'POST', 
          headers: { 
            'Content-Type': 'application/json',
            'X-Daytona-Skip-Preview-Warning': 'true'
          }, 
          body: JSON.stringify({ 
            goal: goalToSend,
            language: language,
            mode: chatMode,
            history: historyPayload
          }) 
      });
      if (!res.ok) { const d = await res.json(); throw new Error(d.detail || 'Failed to start agent'); }
      const data = await res.json();
      
      // Update session title if it is new
      const active = sessions.find(s => s.id === currentSessionId);
      if (active && active.title === 'New Conversation') {
        const firstLine = goalToSend.split('\n')[0];
        const newTitle = firstLine.length > 22 ? firstLine.substring(0, 22) + '...' : firstLine;
        setSessions(prev =>
          prev.map(s =>
            s.id === currentSessionId ? { ...s, title: newTitle } : s
          )
        );
      }

      setAgentRunId(data.run_id);
      setAgentStatus({ status: 'running', steps: [], final_result: '' });
      
      // Add placeholder assistant message that will be updated in real-time
      const assistantMsgId = Date.now() + 10;
      setChatHistory(prev => [
        ...prev,
        { id: assistantMsgId, parentId: userMsgId, role: 'assistant', text: '', mode: chatMode, runId: data.run_id, isStreaming: true }
      ]);
      setActiveMessageId(assistantMsgId);
    } catch (err) { 
      setAgentError(err.message); 
      setAgentLoading(false); 
      const errorMsgId = Date.now() + 20;
      setChatHistory(prev => [...prev, { id: errorMsgId, parentId: userMsgId, role: 'assistant', text: `Error starting agent: ${err.message}` }]);
      setActiveMessageId(errorMsgId);
    }
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

  // Handle real-time updates of the streaming response in chatHistory
  useEffect(() => {
    if (agentRunId && agentStatus) {
      setChatHistory(prev =>
        prev.map(msg => {
          if (msg.runId === agentRunId) {
            let txt = msg.text;
            if (agentStatus.final_result) {
              txt = agentStatus.final_result;
            } else if (agentStatus.status === 'failed') {
              txt = `Execution failed: ${agentStatus.error || 'Unknown error'}`;
            }
            return { ...msg, text: txt, isStreaming: agentStatus.status === 'running' };
          }
          return msg;
        })
      );
    }
  }, [agentStatus, agentRunId]);

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
      <div className="flex items-center justify-between px-4 py-3 border-b border-[rgba(var(--jarvis-accent-rgb),0.1)] bg-[#0a0a0a]">
        <h3 className="font-medium text-[14px] text-white" style={{ fontFamily: 'Rajdhani, sans-serif' }}>{title}</h3>
        <div className="flex items-center gap-2">
          {data?.latency_ms && (
            <span className="text-[11px] px-2 py-0.5 bg-[#0a0a0a] border panel-glow rounded text-[#7a7060]" style={{ fontFamily: 'JetBrains Mono, monospace' }}>{data.latency_ms}ms</span>
          )}
          {data && (
            <span className={`text-[11px] font-medium px-2 py-0.5 rounded border ${data._useRag ? 'bg-[rgba(var(--jarvis-accent-rgb),0.1)] border-[rgba(var(--jarvis-accent-rgb),0.2)] text-[var(--jarvis-accent)]' : 'bg-[#0a0a0a] border-[rgba(var(--jarvis-accent-rgb),0.1)] text-[#7a7060]'}`}>
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
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="border-t border-[rgba(var(--jarvis-accent-rgb),0.1)] overflow-hidden">
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
                        <span className="text-[var(--jarvis-accent)] font-medium flex items-center gap-1"><FileText className="w-3 h-3" />{c.filename || 'Unknown'}</span>
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
      <div className="min-h-screen bg-[var(--jarvis-bg)] flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8 selection:bg-[rgba(var(--jarvis-accent-rgb),0.2)]" style={{ fontFamily: 'Rajdhani, sans-serif' }}>
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }} className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="flex justify-center mb-6">
            <div className="p-3 bg-[#141414] rounded-xl border panel-glow"><Sparkles className="w-8 h-8 text-[var(--jarvis-accent)]" /></div>
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
              <motion.button type="submit" whileHover={hoverScale} whileTap={tapScale} className="w-full py-2.5 px-4 rounded-lg text-sm font-bold text-[#0a0a0a] bg-[var(--jarvis-accent)] hover:bg-[var(--jarvis-accent-hover)] hover:shadow-[0_0_25px_rgba(var(--jarvis-accent-rgb),0.4)] transition-all duration-100" style={{ fontFamily: 'Orbitron, sans-serif', letterSpacing: '0.1em' }}>
                {authMode === 'login' ? 'SIGN IN' : authMode === 'signup' ? 'CREATE ACCOUNT' : authMode === 'phone' ? 'SEND CODE' : 'VERIFY'}
              </motion.button>
            </form>

            <div className="mt-6">
              <div className="relative"><div className="absolute inset-0 flex items-center"><div className="w-full border-t border-[rgba(var(--jarvis-accent-rgb),0.1)]" /></div><div className="relative flex justify-center text-sm"><span className="px-2 bg-[var(--jarvis-surface)] text-[#7a7060]">Or continue with</span></div></div>
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

  const renderSidebarContent = () => {
    return (
      <LibreSidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSelectSession={(id) => {
          setCurrentSessionId(id);
          if (window.innerWidth < 768) setSidebarOpen(false);
        }}
        onNewSession={() => {
          const newId = 'session_' + Date.now();
          setSessions(prev => [
            {
              id: newId,
              title: 'New Conversation',
              history: [],
              timestamp: new Date().toISOString()
            },
            ...prev
          ]);
          setCurrentSessionId(newId);
          if (window.innerWidth < 768) setSidebarOpen(false);
        }}
        onDeleteSession={(id) => {
          setSessions(prev => prev.filter(s => s.id !== id));
        }}
        onRenameSession={(id, newTitle) => {
          setSessions(prev => prev.map(s => s.id === id ? { ...s, title: newTitle } : s));
        }}
        isOpen={sidebarOpen}
        onToggleSidebar={() => setSidebarOpen(false)}
        userEmail={user?.email || 'user@doxa.ai'}
      />
    );
  };

  const [isTransitioning, setIsTransitioning] = useState(false);

  const handleLaunchApp = () => {
    setIsTransitioning(true);
    setTimeout(() => {
      setViewMode('app');
      if (typeof window !== 'undefined') window.location.hash = 'app';
      setIsTransitioning(false);
    }, 550);
  };

  /* ═══════════════════════════════════════════
     MAIN LAYOUT — Landing Page vs Chat Dashboard
     ═══════════════════════════════════════════ */
  if (isTransitioning) {
    return (
      <div className="fixed inset-0 z-50 bg-black flex flex-col items-center justify-center gap-4 select-none">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: [0.9, 1.1, 1], opacity: 1 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="relative w-20 h-20 flex items-center justify-center"
        >
          <div className="absolute inset-0 rounded-full bg-gradient-to-r from-violet-600 to-cyan-500 blur-xl opacity-60 animate-pulse" />
          <img
            src={doxaLogoAsset}
            alt="Doxa Logo"
            className="w-16 h-16 object-contain relative z-10 filter invert brightness-200"
          />
        </motion.div>
        <span className="text-xs font-mono tracking-widest text-violet-400 font-bold uppercase animate-pulse" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          INITIALIZING DOXA AGENT CORE...
        </span>
      </div>
    );
  }

  if (viewMode === 'landing') {
    return (
      <AnimatePresence mode="wait">
        <motion.div
          key="landing-view"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0, scale: 0.96, filter: 'blur(10px)' }}
          transition={{ duration: 0.35 }}
        >
          <LandingPage onLaunchApp={handleLaunchApp} />
        </motion.div>
      </AnimatePresence>
    );
  }

  return (
    <div className="h-screen w-screen bg-[var(--jarvis-bg)] overflow-hidden flex flex-row relative" style={{ fontFamily: 'Rajdhani, sans-serif' }}>
      <NeuralBackground />

      {/* ── Voice Listener (always active) ── */}
      <VoiceListener
        isSphereMode={sphereMode}
        onActivate={() => {
          try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.frequency.setValueAtTime(640, ctx.currentTime);
            gain.gain.setValueAtTime(0.1, ctx.currentTime);
            osc.start();
            osc.stop(ctx.currentTime + 0.1);
          } catch {}
          setSphereMode(true);
        }}
        onDeactivate={() => {
          setSphereMode(false);
        }}
        onPermissionError={() => {
          setMicPermissionDenied(true);
        }}
        onQueryCaptured={(query) => {
          if (query) {
            setAgentGoal(query);
            handleStartAgent(query);
          }
        }}
      />

      {/* ── Sphere Mode Top Exit Bar & Emergent Particle Answer Card ── */}
      {sphereMode && (
        <>
          <div className="fixed top-5 right-5 z-50 flex items-center gap-3">
            <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-neutral-950/80 border border-[var(--jarvis-accent)]/30 backdrop-blur-md text-xs text-[#e0d6c2]">
              <span className="w-2 h-2 rounded-full bg-[var(--jarvis-accent)] animate-ping" />
              <span className="font-mono text-[11px] uppercase tracking-widest text-[var(--jarvis-accent)] font-bold">Sphere Mode</span>
            </div>
            <button
              onClick={() => setSphereMode(false)}
              className="p-2 rounded-full bg-neutral-900/90 border border-neutral-700 text-neutral-300 hover:text-white hover:border-[var(--jarvis-accent)] transition-all cursor-pointer shadow-lg hover:scale-105 active:scale-95 flex items-center justify-center"
              title="Exit Sphere Mode (or say 'exit')"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <EmergentAnswerCard
            text={agentStatus?.final_result}
            isThinking={agentLoading || agentStatus?.status === 'running'}
            steps={agentStatus?.steps}
            onClose={() => setAgentStatus(null)}
            onSpeakToggle={() => {
              if ('speechSynthesis' in window) {
                if (window.speechSynthesis.speaking) {
                  window.speechSynthesis.cancel();
                  setIsSpeaking(false);
                } else if (agentStatus?.final_result) {
                  const uttr = new SpeechSynthesisUtterance(agentStatus.final_result);
                  uttr.onend = () => setIsSpeaking(false);
                  setIsSpeaking(true);
                  window.speechSynthesis.speak(uttr);
                }
              }
            }}
            isSpeaking={isSpeaking}
          />
        </>
      )}

      {/* ── Microphone Permission Toast Notice ── */}
      {micPermissionDenied && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-3 px-4 py-2.5 rounded-xl bg-neutral-900/90 border border-amber-500/40 text-amber-300 text-xs shadow-2xl backdrop-blur-md">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>Enable microphone access in browser settings for voice activation ("Hey Doxa")</span>
          <button onClick={() => setMicPermissionDenied(false)} className="p-1 hover:text-white cursor-pointer">
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* ── Desktop Inline Collapsible History Sidebar (side-by-side layout) ── */}
      <AnimatePresence initial={false}>
        {sidebarOpen && !sphereMode && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 280, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="hidden md:flex flex-col border-r border-[var(--jarvis-accent)]/15 bg-neutral-950/45 backdrop-blur-lg shrink-0 h-full p-4 gap-4 z-20"
            style={{ fontFamily: 'Rajdhani, sans-serif' }}
          >
            {renderSidebarContent()}
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Main App Content Wrapper ── */}
      <div className="flex-1 flex flex-col min-w-0 h-full relative">
        {/* ── Dashboard Area (takes remaining vertical space) ── */}
        <div className="flex-1 min-h-0 relative">
          <Dashboard
            user={user}
            agentLoading={agentLoading}
            agentStatus={agentStatus}
            isSpeaking={isSpeaking}
            queriesCount={history.length}
            sessionStart={sessionStart}
            activeOverlay={activeOverlay}
            onNavigate={handleNavigate}
            themeName={theme}
            sentiment={sentiment}
            isDebating={isDebating}
            steps={agentStatus?.steps || []}
            morphText={agentStatus?.final_result || ''}
            toggleSidebar={() => setSidebarOpen(!sidebarOpen)}
            sidebarOpen={sidebarOpen}
            isSphereMode={sphereMode}
            onToggleSphereMode={() => setSphereMode(!sphereMode)}
          />
        </div>

        {/* ── Voice Speaking Telemetry HUD ── */}
        <AnimatePresence>
          {isSpeaking && (
            <div className="px-6 pb-2 shrink-0 z-20">
              <VoiceTelemetry isSpeaking={isSpeaking} />
            </div>
          )}
        </AnimatePresence>

        {/* ── Sleek Fixed Bottom Chat Panel ── */}
        {!sphereMode && (
          <ChatPanel
            chatHistory={(() => {
              if (!activeMessageId || !Array.isArray(chatHistory)) return [];
              const chain = [];
              let current = chatHistory.find(m => m && m.id === activeMessageId);
              const visited = new Set();
              while (current && !visited.has(current.id)) {
                visited.add(current.id);
                chain.unshift(current);
                current = chatHistory.find(m => m && m.id === current.parentId);
              }
              return chain;
            })()}
            fullHistory={chatHistory}
            activeMessageId={activeMessageId}
            setActiveMessageId={setActiveMessageId}
            agentGoal={agentGoal}
            setAgentGoal={setAgentGoal}
            agentLoading={agentLoading}
            agentStatus={agentStatus}
            agentError={agentError}
            onStartAgent={handleStartAgent}
            chatMode={chatMode}
            setChatMode={setChatMode}
            language={language}
            setLanguage={handleLanguageChange}
            toggleSidebar={() => setSidebarOpen(!sidebarOpen)}
            onExportChat={handleExportChat}
            onUploadDoc={handleUploadDoc}
            proactiveSuggestions={proactiveSuggestions}
            setProactiveSuggestions={setProactiveSuggestions}
          />
        )}
      </div>

      {/* ── Mobile Sidebar Drawer Overlay ── */}
      <AnimatePresence>
        {sidebarOpen && (
          <div className="md:hidden">
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.4 }}
              exit={{ opacity: 0 }}
              onClick={() => setSidebarOpen(false)}
              className="fixed inset-0 bg-black/60 z-40"
            />
            {/* Sidebar drawer panel */}
            <motion.div
              initial={{ x: -280 }}
              animate={{ x: 0 }}
              exit={{ x: -280 }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed left-0 top-0 bottom-0 w-[280px] bg-neutral-950/95 border-r border-[var(--jarvis-accent)]/15 backdrop-blur-lg z-50 p-4 flex flex-col gap-4 shadow-2xl"
              style={{ fontFamily: 'Rajdhani, sans-serif' }}
            >
              {renderSidebarContent()}
            </motion.div>
          </div>
        )}
      </AnimatePresence>

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
              border: '1px solid rgba(var(--jarvis-accent-rgb), 0.2)',
              background: 'linear-gradient(145deg, rgba(10, 18, 36, 0.96), rgba(6, 12, 28, 0.98))',
              backdropFilter: 'blur(12px)',
              boxShadow: '0 0 30px rgba(var(--jarvis-accent-rgb), 0.1)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ fontFamily: "'Orbitron', sans-serif", fontSize: '10px', color: 'var(--jarvis-accent)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>Voice not supported — showing text</span>
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
              {/* overlay header with consolidated tab navigation */}
              <div className="flex items-center justify-between px-5 py-3 border-b border-[rgba(var(--jarvis-accent-rgb),0.15)] flex-wrap gap-3 select-none">
                <div className="flex items-center gap-4 sm:gap-6 flex-wrap">
                  <span className="text-[10px] font-black tracking-widest text-[#7a7060] font-orbitron uppercase hidden md:inline" style={{ fontFamily: 'Orbitron, sans-serif' }}>CONTROL PANEL</span>
                  <div className="flex gap-1 bg-[#141414] p-0.5 rounded-lg border border-[var(--jarvis-accent)]/10">
                    {[
                      { id: 'eval', label: 'EVAL' },
                      { id: 'documents', label: 'DOCS' },
                      { id: 'history', label: 'HISTORY' },
                      { id: 'settings', label: 'CONFIG' }
                    ].map(tab => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveOverlay(tab.id)}
                        className={`px-3 py-1 rounded-md text-[10px] sm:text-xs font-bold font-orbitron tracking-wider transition-all cursor-pointer ${
                          activeOverlay === tab.id
                            ? 'bg-[var(--jarvis-accent)] text-[#0a0a0a] shadow-[0_0_8px_rgba(var(--jarvis-accent-rgb),0.25)] font-black'
                            : 'text-neutral-500 hover:text-neutral-300 hover:bg-neutral-900/40'
                        }`}
                        style={{ fontFamily: 'Orbitron, sans-serif' }}
                      >
                        {tab.label}
                      </button>
                    ))}
                  </div>
                </div>
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
                              useRag ? 'bg-[rgba(var(--jarvis-accent-rgb),0.1)] text-[var(--jarvis-accent)] border-[rgba(var(--jarvis-accent-rgb),0.2)]' : 'bg-[#141414] text-[#7a7060] border-[rgba(var(--jarvis-accent-rgb),0.1)] hover:border-[rgba(var(--jarvis-accent-rgb),0.2)]'
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
                                !prompt.trim() || loading ? 'bg-[#1e1e1e] text-[#7a7060] cursor-not-allowed' : 'bg-[var(--jarvis-accent)] hover:bg-[var(--jarvis-accent-hover)] text-[#0a0a0a] hover:shadow-[0_0_25px_rgba(var(--jarvis-accent-rgb),0.4)]'
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
                          uploadingDoc ? 'border-[rgba(var(--jarvis-accent-rgb),0.5)] bg-[rgba(var(--jarvis-accent-rgb),0.05)]' : 'hover:border-[rgba(var(--jarvis-accent-rgb),0.3)] hover:bg-[#141414]'
                        }`}
                        onDragOver={(e) => { e.preventDefault(); e.stopPropagation(); }}
                        onDrop={(e) => { e.preventDefault(); e.stopPropagation(); const f = e.dataTransfer.files[0]; if (f) handleUploadDoc(f); }}
                      >
                        <input type="file" className="hidden" accept=".txt,.pdf,.md,.csv,.json" onChange={(e) => { const f = e.target.files[0]; if (f) handleUploadDoc(f); }} />
                        {uploadingDoc ? <Loader2 className="w-7 h-7 text-[var(--jarvis-accent)] animate-spin" /> : <Upload className="w-7 h-7 text-[#7a7060]" />}
                        <div className="text-center">
                          <p className="text-sm font-medium text-[#e0d6c2]">{uploadingDoc ? 'Uploading…' : 'Drop files here or click to upload'}</p>
                          <p className="text-[11px] text-[#7a7060] mt-1" style={{ fontFamily: 'JetBrains Mono, monospace' }}>TXT, PDF, MD, CSV, JSON</p>
                        </div>
                      </label>
                    </motion.div>

                    {/* Search filter input */}
                    {documents.length > 0 && (
                      <motion.div variants={staggerItem}>
                        <input
                          type="text"
                          placeholder="Search uploaded files by name..."
                          value={docSearchQuery}
                          onChange={(e) => setDocSearchQuery(e.target.value)}
                          className="w-full bg-[#141414] border border-[rgba(var(--jarvis-accent-rgb),0.15)] rounded-lg px-4 py-2.5 text-sm text-[#e0d6c2] placeholder-[#7a7060] focus:outline-none focus:border-[var(--jarvis-accent)] transition-all font-medium"
                          style={{ fontFamily: 'Rajdhani, sans-serif' }}
                        />
                      </motion.div>
                    )}

                    {documents.length === 0 ? (
                      <motion.div variants={staggerItem} className="text-center py-16 hud-panel border-dashed">
                        <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-[#141414] flex items-center justify-center">
                          <FileText className="w-6 h-6 text-[#7a7060]" />
                        </div>
                        <p className="text-[#e0d6c2] text-sm font-medium">No documents uploaded</p>
                        <p className="text-[#7a7060] text-xs mt-1">Upload files to enable RAG-powered evaluations.</p>
                      </motion.div>
                    ) : documents.filter(doc => doc.filename.toLowerCase().includes(docSearchQuery.toLowerCase())).length === 0 ? (
                      <motion.div variants={staggerItem} className="text-center py-12 hud-panel border-dashed">
                        <p className="text-[#7a7060] text-sm">No files matching "{docSearchQuery}" found.</p>
                      </motion.div>
                    ) : (
                      documents.filter(doc => doc.filename.toLowerCase().includes(docSearchQuery.toLowerCase())).map((doc, idx) => (
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
                    
                    <motion.div variants={staggerItem} className="pt-5 mt-4 border-t border-[rgba(var(--jarvis-accent-rgb),0.15)]">
                      <h3 className="text-[15px] font-medium text-white mb-1" style={{ fontFamily: 'Rajdhani, sans-serif' }}>Theme Switcher</h3>
                      <p className="text-xs text-[#7a7060] mb-4">Choose the visual style of your Mission Control interface.</p>
                      <div className="flex gap-4">
                        <button
                          type="button"
                          onClick={() => setTheme('ultron')}
                          className={`flex-1 py-3 px-4 rounded-xl border flex items-center justify-center gap-2.5 transition-all font-bold tracking-wider text-xs uppercase cursor-pointer ${
                            theme === 'ultron'
                              ? 'bg-[rgba(var(--jarvis-accent-rgb),0.12)] border-[var(--jarvis-accent)] text-white shadow-[0_0_15px_rgba(var(--jarvis-accent-rgb),0.25)]'
                              : 'bg-neutral-900/60 border-neutral-800 text-neutral-400 hover:text-neutral-200 hover:border-neutral-700'
                          }`}
                          style={{ fontFamily: 'Orbitron, sans-serif' }}
                        >
                          <span className="w-2.5 h-2.5 rounded-full bg-[var(--jarvis-accent)]" />
                          Ultron Crimson
                        </button>
                        <button
                          type="button"
                          onClick={() => setTheme('aether')}
                          className={`flex-1 py-3 px-4 rounded-xl border flex items-center justify-center gap-2.5 transition-all font-bold tracking-wider text-xs uppercase cursor-pointer ${
                            theme === 'aether'
                              ? 'bg-[rgba(0,217,255,0.12)] border-[var(--jarvis-accent)] text-white shadow-[0_0_15px_rgba(0,217,255,0.25)]'
                              : 'bg-neutral-900/60 border-neutral-800 text-neutral-400 hover:text-neutral-200 hover:border-neutral-700'
                          }`}
                          style={{ fontFamily: 'Orbitron, sans-serif' }}
                        >
                          <span className="w-2.5 h-2.5 rounded-full bg-[#00d9ff]" />
                          Aether Blue
                        </button>
                      </div>
                    </motion.div>

                    <motion.div variants={staggerItem} className="pt-5 mt-4 border-t border-[rgba(var(--jarvis-accent-rgb),0.15)]">
                      <h3 className="text-[15px] font-medium text-white mb-1" style={{ fontFamily: 'Rajdhani, sans-serif' }}>Integration Roadmap</h3>
                      <p className="text-xs text-[#7a7060] mb-4">Third-party automations and companion services on the development path.</p>
                      <div className="grid grid-cols-3 gap-3 text-center text-[10px] uppercase font-bold tracking-wider" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                        <div className="p-3.5 bg-neutral-900/40 border border-neutral-800/80 rounded-xl text-neutral-500 relative overflow-hidden group">
                          <span className="text-[8px] bg-[rgba(var(--jarvis-accent-rgb),0.1)] text-[var(--jarvis-accent)] px-1.5 py-0.5 rounded absolute top-0.5 right-0.5 scale-90">SOON</span>
                          WhatsApp
                        </div>
                        <div className="p-3.5 bg-neutral-900/40 border border-neutral-800/80 rounded-xl text-neutral-500 relative overflow-hidden group">
                          <span className="text-[8px] bg-[rgba(var(--jarvis-accent-rgb),0.1)] text-[var(--jarvis-accent)] px-1.5 py-0.5 rounded absolute top-0.5 right-0.5 scale-90">SOON</span>
                          Spotify
                        </div>
                        <div className="p-3.5 bg-neutral-900/40 border border-neutral-800/80 rounded-xl text-neutral-500 relative overflow-hidden group">
                          <span className="text-[8px] bg-[rgba(var(--jarvis-accent-rgb),0.1)] text-[var(--jarvis-accent)] px-1.5 py-0.5 rounded absolute top-0.5 right-0.5 scale-90">SOON</span>
                          Desktop UI
                        </div>
                      </div>
                    </motion.div>

                    <motion.div variants={staggerItem} className="pt-5 mt-4 border-t border-[rgba(var(--jarvis-accent-rgb),0.15)]">
                      <h3 className="text-[15px] font-medium text-white mb-1">Account</h3>
                      <p className="text-xs text-[#7a7060] mb-3">Signed in as <span className="text-[var(--jarvis-accent)] font-medium">{user}</span></p>
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

      {/* ── Active HUD Notifications Alerts Overlay ── */}
      <div className="fixed top-4 right-4 z-[90] flex flex-col gap-3 max-w-sm pointer-events-auto">
        <AnimatePresence>
          {activeAlerts.map(alert => (
            <motion.div
              key={alert.id}
              initial={{ opacity: 0, x: 50, scale: 0.9 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, x: 50, scale: 0.9 }}
              transition={{ duration: 0.3 }}
              className="hud-panel hud-panel-bright p-4 bg-neutral-950/95 border-l-4 border-l-[#00ff88] flex flex-col gap-1.5 shadow-[0_10px_30px_rgba(0,255,136,0.15)] relative"
            >
              <button
                type="button"
                onClick={() => setActiveAlerts(prev => prev.filter(x => x.id !== alert.id))}
                className="absolute top-2.5 right-2.5 text-neutral-500 hover:text-white transition-colors cursor-pointer"
              >
                <X className="w-3.5 h-3.5" />
              </button>
              <div className="text-[10px] tracking-wider uppercase font-bold text-[#00ff88] font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                SYSTEM ALERT // TIMER COMPLETE
              </div>
              <div className="text-sm font-semibold text-white">
                {alert.title || "Untitled Reminder"}
              </div>
              <div className="text-[10px] text-neutral-500 font-mono">
                TRIGGERED AT: {alert.timestamp}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Toast Notification */}
      <AnimatePresence>
        {toast && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            className={`fixed bottom-6 right-6 z-[100] px-4 py-3 rounded-xl border backdrop-blur-md shadow-2xl flex items-center gap-3 text-sm ${
              toast.type === 'error'
                ? 'bg-red-950/85 border-red-500/35 text-red-200 shadow-[0_0_20px_rgba(239,68,68,0.15)]'
                : toast.type === 'info'
                ? 'bg-neutral-900/90 border-[var(--jarvis-accent)]/20 text-[#c8d6e5] shadow-[0_0_20px_rgba(var(--jarvis-accent-rgb),0.1)]'
                : 'bg-emerald-950/85 border-emerald-500/35 text-emerald-200 shadow-[0_0_20px_rgba(16,185,129,0.15)]'
            }`}
            style={{ fontFamily: 'Rajdhani, sans-serif' }}
          >
            <span className={`w-2 h-2 rounded-full ${
              toast.type === 'error' ? 'bg-red-500 animate-pulse' : toast.type === 'info' ? 'bg-[var(--jarvis-accent)] animate-pulse' : 'bg-emerald-500 animate-pulse'
            }`} />
            <p className="font-semibold">{toast.message}</p>
          </motion.div>
        )}
      </AnimatePresence>

    </div>
  );
}

export default App;
