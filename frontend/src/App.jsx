import { useState, useEffect } from 'react';
import { Sparkles, Send, Loader2, Clock, Bot, Download, History, Settings, LogOut, Code2, Phone, ArrowRight } from 'lucide-react';
import { motion, animate, AnimatePresence } from 'framer-motion';

// --- Custom Sub-Components ---



// CountUp Number
const CountUp = ({ end, duration = 1 }) => {
  const [value, setValue] = useState(0);
  
  useEffect(() => {
    const controls = animate(0, end, {
      duration,
      onUpdate(v) {
        setValue(Math.round(v));
      },
    });
    return () => controls.stop();
  }, [end, duration]);

  return <span>{value}</span>;
};

// Skeleton Loading
const SkeletonLoader = () => (
  <div className="flex flex-col gap-4 py-2">
    <motion.div className="h-4 bg-slate-800/50 rounded-full w-3/4" animate={{ opacity: [0.3, 0.7, 0.3] }} transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }} />
    <motion.div className="h-4 bg-slate-800/50 rounded-full w-full" animate={{ opacity: [0.3, 0.7, 0.3] }} transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut", delay: 0.2 }} />
    <motion.div className="h-4 bg-slate-800/50 rounded-full w-5/6" animate={{ opacity: [0.3, 0.7, 0.3] }} transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut", delay: 0.4 }} />
    <motion.div className="h-4 bg-slate-800/50 rounded-full w-1/2" animate={{ opacity: [0.3, 0.7, 0.3] }} transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut", delay: 0.6 }} />
  </div>
);

// Google Icon SVG
const GoogleIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 24 24">
    <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
    <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
    <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
    <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
  </svg>
);

// GitHub Icon SVG
const GithubIcon = () => (
  <svg className="w-5 h-5 group-hover:text-white transition-colors" viewBox="0 0 24 24">
    <path fill="currentColor" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.418 22 12c0-5.523-4.477-10-10-10z" />
  </svg>
);

// Floating Particles
const FloatingParticles = () => {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {[...Array(30)].map((_, i) => {
        const size = Math.random() * 4 + 2;
        return (
          <motion.div
            key={i}
            className="absolute bg-indigo-500/20 rounded-full"
            style={{ width: size, height: size }}
            initial={{
              x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1000),
              y: Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 1000),
              scale: Math.random() * 0.5 + 0.5,
            }}
            animate={{
              y: [null, Math.random() * -500],
              opacity: [0, 0.8, 0],
            }}
            transition={{
              duration: Math.random() * 10 + 15,
              repeat: Infinity,
              ease: "linear",
              delay: Math.random() * 10,
            }}
          />
        );
      })}
    </div>
  );
};

// --- Main App ---

function App() {
  // State for Features
  const [user, setUser] = useState(() => localStorage.getItem('ai_eval_user'));
  const [authMode, setAuthMode] = useState('login'); // login, signup, phone, otp
  const [currentView, setCurrentView] = useState('eval'); // eval, history, settings
  
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('ai_eval_history');
    return saved ? JSON.parse(saved) : [];
  });
  
  const [settings, setSettings] = useState(() => {
    const saved = localStorage.getItem('ai_eval_settings');
    return saved ? JSON.parse(saved) : { model1Name: 'Llama 3.1 8B (Instant)', model2Name: 'Llama 3.3 70B (Versatile)' };
  });

  // Eval State
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Sync to localStorage
  useEffect(() => {
    if (user) localStorage.setItem('ai_eval_user', user);
    else localStorage.removeItem('ai_eval_user');
  }, [user]);

  useEffect(() => localStorage.setItem('ai_eval_history', JSON.stringify(history)), [history]);
  useEffect(() => localStorage.setItem('ai_eval_settings', JSON.stringify(settings)), [settings]);

  // Auth Handlers
  const handleLogin = (e) => {
    e.preventDefault();
    if (authMode === 'phone') {
      setAuthMode('otp');
      return;
    }
    const identifier = e.target.email?.value || e.target.phone?.value || e.target.otp?.value || 'Mock User';
    setUser(identifier);
  };
  const handleSocialLogin = (provider) => {
    setUser(`${provider} User`);
  };
  const handleLogout = () => {
    setUser(null);
    setCurrentView('eval');
    setResults(null);
    setPrompt('');
  };

  // Evaluation Handler
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const res = await fetch('http://localhost:8000/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!res.ok) throw new Error(`Server responded with status: ${res.status}`);

      const data = await res.json();
      setResults(data.results);

      // Save to History
      const evalRecord = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        prompt,
        results: data.results,
        models: { model1: settings.model1Name, model2: settings.model2Name }
      };
      setHistory(prev => [evalRecord, ...prev]);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // CSV Export Handler
  const handleExportCSV = () => {
    if (!results) return;
    const escapeCSV = (str) => `"${String(str).replace(/"/g, '""')}"`;
    
    const headers = ['Prompt', `${settings.model1Name} Content`, `${settings.model1Name} Latency (ms)`, `${settings.model2Name} Content`, `${settings.model2Name} Latency (ms)`];
    const row = [
      prompt,
      results.groq_1?.content || results.groq_1?.error || '',
      results.groq_1?.latency_ms || 0,
      results.groq_2?.content || results.groq_2?.error || '',
      results.groq_2?.latency_ms || 0,
    ];
    
    const csvContent = [headers.map(escapeCSV).join(','), row.map(escapeCSV).join(',')].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `evaluation_${new Date().getTime()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // UI Components
  const ResultPanel = ({ title, data, delay }) => (
    <div className="relative h-full flex flex-col z-10">
      <motion.div 
        className="absolute -inset-1 bg-gradient-to-r from-indigo-500/40 to-purple-500/40 rounded-2xl blur-xl"
        animate={{ opacity: [0.3, 0.6, 0.3], scale: [0.98, 1.01, 0.98] }}
        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay }}
      />
      <motion.div 
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        whileHover={{ scale: 1.02, boxShadow: "0px 0px 30px rgba(99,102,241,0.4)" }}
        transition={{ delay, duration: 0.15, ease: "easeOut", whileHover: { type: "spring", stiffness: 400, damping: 20 } }}
        className="bg-slate-900/60 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 flex flex-col h-full relative overflow-hidden group shadow-xl transition-colors duration-300 hover:border-indigo-400/60"
      >
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-400 to-purple-400 opacity-20 group-hover:opacity-100 transition-opacity duration-500"></div>
        <div className="flex items-center justify-between mb-5 pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
              <Bot className="w-5 h-5 text-indigo-400" />
            </div>
            <h3 className="font-semibold text-xl tracking-tight text-slate-100">{title}</h3>
          </div>
          {data && (
            <motion.div 
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="flex items-center gap-1.5 px-3 py-1 bg-emerald-500/10 rounded-full border border-emerald-500/20 shadow-inner"
            >
              <Clock className="w-3.5 h-3.5 text-emerald-400" />
              <span className="text-xs font-semibold text-emerald-300 tracking-wide uppercase">
                <CountUp end={data.latency_ms} />ms
              </span>
            </motion.div>
          )}
        </div>
        <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
          {loading ? <SkeletonLoader /> : data ? (
            data.error ? <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm font-medium">Error: {data.error}</div> 
                       : <div className="prose prose-invert max-w-none text-slate-300 text-[15px] leading-relaxed whitespace-pre-wrap">{data.content}</div>
          ) : <div className="h-full flex items-center justify-center text-slate-500/80 italic text-sm font-medium">Awaiting prompt evaluation...</div>}
        </div>
      </motion.div>
    </div>
  );

  // Render Login
  if (!user) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-sans selection:bg-indigo-500/30 relative overflow-hidden">
        <FloatingParticles />
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
          <div className="flex justify-center relative mb-6">
            <motion.div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 blur-2xl rounded-full opacity-30" animate={{ opacity: [0.2, 0.4, 0.2] }} transition={{ duration: 3, repeat: Infinity }} />
            <div className="relative p-3 bg-indigo-500/20 rounded-xl border border-indigo-500/30">
              <Sparkles className="w-10 h-10 text-indigo-400" />
            </div>
          </div>
          <h2 className="mt-2 text-center text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 to-purple-300">
            AI Evaluation Pipeline
          </h2>
          <p className="mt-2 text-center text-sm text-slate-400">
            {authMode === 'login' && 'Sign in to start evaluating models'}
            {authMode === 'signup' && 'Create an account to get started'}
            {authMode === 'phone' && 'Enter your phone number'}
            {authMode === 'otp' && 'Enter the verification code'}
          </p>
        </motion.div>

        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
          <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500/30 to-purple-500/30 rounded-[2.5rem] blur-xl" animate={{ opacity: [0.3, 0.6, 0.3] }} transition={{ duration: 4, repeat: Infinity }} />
          <div className="relative bg-slate-900/60 backdrop-blur-xl py-8 px-4 shadow-2xl sm:rounded-3xl sm:px-10 border border-slate-700/50">
            
            {(authMode === 'login' || authMode === 'signup') && (
              <>
                <div className="flex flex-col gap-3 mb-6">
                  <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={() => handleSocialLogin('Google')}
                    className="w-full flex items-center justify-center gap-3 py-3 px-4 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl transition-colors text-slate-200 font-semibold text-sm shadow-sm group">
                    <GoogleIcon />
                    Continue with Google
                  </motion.button>
                  <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={() => handleSocialLogin('GitHub')}
                    className="w-full flex items-center justify-center gap-3 py-3 px-4 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl transition-colors text-slate-200 font-semibold text-sm shadow-sm group">
                    <GithubIcon />
                    Continue with GitHub
                  </motion.button>
                  <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={() => setAuthMode('phone')}
                    className="w-full flex items-center justify-center gap-3 py-3 px-4 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl transition-colors text-slate-200 font-semibold text-sm shadow-sm">
                    <Phone className="w-5 h-5 text-indigo-400" />
                    Continue with Phone
                  </motion.button>
                </div>

                <div className="relative mb-6">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-slate-700"></div>
                  </div>
                  <div className="relative flex justify-center text-xs">
                    <span className="px-3 bg-slate-900/60 backdrop-blur-sm text-slate-500 font-medium">OR</span>
                  </div>
                </div>
              </>
            )}

            <form onSubmit={handleLogin} className="space-y-6">
              {(authMode === 'login' || authMode === 'signup') && (
                <>
                  {authMode === 'signup' && (
                    <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} className="overflow-hidden">
                      <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Full Name</label>
                      <input type="text" placeholder="John Doe"
                        className="w-full bg-slate-950/50 border border-slate-700 rounded-xl p-3 text-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-colors" />
                    </motion.div>
                  )}
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Email Address</label>
                    <input name="email" type="email" required placeholder="you@example.com"
                      className="w-full bg-slate-950/50 border border-slate-700 rounded-xl p-3 text-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-colors" />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Password</label>
                    <input name="password" type="password" required placeholder="••••••••"
                      className="w-full bg-slate-950/50 border border-slate-700 rounded-xl p-3 text-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-colors" />
                  </div>
                </>
              )}

              {authMode === 'phone' && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Phone Number</label>
                  <input name="phone" type="tel" required placeholder="+1 (555) 000-0000"
                    className="w-full bg-slate-950/50 border border-slate-700 rounded-xl p-3 text-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-colors" />
                </motion.div>
              )}

              {authMode === 'otp' && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 text-center">6-Digit Code</label>
                  <input name="otp" type="text" required placeholder="123456" maxLength={6}
                    className="w-full bg-slate-950/50 border border-slate-700 rounded-xl p-3 text-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-colors tracking-[0.5em] text-center text-xl font-mono" />
                </motion.div>
              )}

              <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} type="submit"
                className="w-full flex items-center justify-center gap-2 py-3.5 px-4 border border-transparent rounded-xl shadow-lg shadow-indigo-500/25 text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-500 focus:outline-none transition-colors">
                {authMode === 'login' ? 'Sign In' : authMode === 'signup' ? 'Create Account' : authMode === 'phone' ? 'Send Code' : 'Verify & Continue'}
                <ArrowRight className="w-4 h-4" />
              </motion.button>
            </form>

            <div className="mt-6 text-center text-sm text-slate-400">
              {authMode === 'login' ? (
                <span>Don't have an account? <button onClick={() => setAuthMode('signup')} type="button" className="text-indigo-400 hover:text-indigo-300 font-semibold transition-colors">Sign up</button></span>
              ) : authMode === 'signup' ? (
                <span>Already have an account? <button onClick={() => setAuthMode('login')} type="button" className="text-indigo-400 hover:text-indigo-300 font-semibold transition-colors">Sign in</button></span>
              ) : (
                <button onClick={() => setAuthMode('login')} type="button" className="text-indigo-400 hover:text-indigo-300 font-semibold transition-colors">Back to Email Login</button>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-200 selection:bg-indigo-500/30 font-sans">
      {/* Header */}
      <header className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border-b border-indigo-500/10 sticky top-0 z-50 shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 py-4 flex items-center justify-between">
          <motion.div className="flex items-center gap-3 relative cursor-pointer" onClick={() => setCurrentView('eval')}>
            <motion.div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 blur-2xl rounded-full" animate={{ opacity: [0.2, 0.5, 0.2] }} transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }} />
            <motion.div className="relative p-2 bg-indigo-500/20 rounded-lg backdrop-blur-sm border border-indigo-500/30" animate={{ y: [-4, 4, -4] }} transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}>
              <Sparkles className="w-6 h-6 text-indigo-400" />
            </motion.div>
            <h1 className="relative text-2xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 to-purple-300 drop-shadow-md hidden sm:block">
              AI Evaluation Pipeline
            </h1>
          </motion.div>

          <div className="flex items-center gap-4">
            <nav className="flex items-center gap-1 bg-slate-900/50 p-1 rounded-xl border border-slate-800">
              <button onClick={() => setCurrentView('eval')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${currentView === 'eval' ? 'bg-indigo-500/20 text-indigo-300' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}>
                <Code2 className="w-4 h-4 inline-block mr-2" />Eval
              </button>
              <button onClick={() => setCurrentView('history')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${currentView === 'history' ? 'bg-indigo-500/20 text-indigo-300' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}>
                <History className="w-4 h-4 inline-block mr-2" />History
              </button>
              <button onClick={() => setCurrentView('settings')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${currentView === 'settings' ? 'bg-indigo-500/20 text-indigo-300' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}>
                <Settings className="w-4 h-4 inline-block mr-2" />Settings
              </button>
            </nav>
            <div className="h-6 w-px bg-slate-800 hidden sm:block"></div>
            <button onClick={handleLogout} className="hidden sm:block p-2 text-slate-400 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-colors" title="Sign Out">
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Areas */}
      <AnimatePresence mode="wait">
        
        {/* EVAL VIEW */}
        {currentView === 'eval' && (
          <motion.main key="eval" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.15 }} className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 flex flex-col gap-10">
            {/* Input Section */}
            <motion.section className="bg-slate-900/40 backdrop-blur-sm border border-slate-800 rounded-2xl p-6 shadow-xl">
              <form onSubmit={handleSubmit} className="flex flex-col gap-5">
                <label htmlFor="prompt" className="text-sm font-semibold text-slate-300 tracking-wide ml-1">PROMPT</label>
                <div className="relative group z-10">
                  <motion.div className="absolute -inset-1.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-500 rounded-2xl blur-xl" animate={{ opacity: [0.4, 0.7, 0.4], scale: [0.98, 1.02, 0.98] }} transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }} />
                  <motion.textarea
                    id="prompt" value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Type your prompt here... (Enter to run, Shift+Enter for new line)"
                    whileHover={{ scale: 1.01, boxShadow: "0px 0px 20px rgba(99,102,241,0.4)" }} transition={{ duration: 0.15 }}
                    className="relative w-full bg-slate-900/80 backdrop-blur-lg border border-slate-700/80 rounded-xl p-5 text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-indigo-400 focus:ring-1 focus:ring-indigo-400 text-base leading-relaxed resize-y min-h-[140px] shadow-inner transition-colors"
                    disabled={loading}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        if (prompt.trim() && !loading) handleSubmit(e);
                      }
                    }}
                  />
                </div>
                
                <div className="flex justify-between items-center mt-2">
                  <div className="flex-1">
                    {error && <span className="text-red-400 text-sm font-medium px-4 py-2 bg-red-500/10 rounded-lg border border-red-500/20">{error}</span>}
                  </div>
                  <div className="flex items-center gap-3">
                    {results && (
                      <motion.button type="button" onClick={handleExportCSV} initial={{ opacity: 0 }} animate={{ opacity: 1 }} whileHover={{ scale: 1.05 }}
                        className="flex items-center gap-2 px-5 py-3.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl font-semibold transition-colors border border-slate-700 shadow-lg">
                        <Download className="w-5 h-5" /> Export CSV
                      </motion.button>
                    )}
                    <motion.button type="submit" disabled={loading || !prompt.trim()}
                      whileHover={(!loading && prompt.trim()) ? { scale: 1.02 } : {}} whileTap={(!loading && prompt.trim()) ? { scale: 0.98 } : {}}
                      animate={{ boxShadow: (!loading && prompt.trim()) ? ["0px 0px 0px rgba(79,70,229,0)", "0px 0px 25px rgba(79,70,229,0.5)", "0px 0px 0px rgba(79,70,229,0)"] : "0px 0px 0px rgba(79,70,229,0)" }}
                      transition={{ duration: 2, repeat: Infinity, whileHover: { duration: 0.15 } }}
                      className="group relative flex items-center gap-2 px-8 py-3.5 bg-indigo-600 disabled:bg-slate-800 disabled:text-slate-500 text-white font-semibold tracking-wide rounded-xl transition-colors disabled:cursor-not-allowed overflow-hidden">
                      <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]"></div>
                      {loading ? <><Loader2 className="w-5 h-5 animate-spin" /><span>Evaluating...</span></> : <><Send className="w-5 h-5 group-hover:translate-x-1 transition-transform" /><span>Run Evaluation</span></>}
                    </motion.button>
                  </div>
                </div>
              </form>
            </motion.section>

            <motion.section className="flex-1 grid grid-cols-1 xl:grid-cols-2 gap-8 min-h-[500px]">
              <ResultPanel title={settings.model1Name} data={results?.groq_1} delay={0.1} />
              <ResultPanel title={settings.model2Name} data={results?.groq_2} delay={0.2} />
            </motion.section>
          </motion.main>
        )}

        {/* HISTORY VIEW */}
        {currentView === 'history' && (
          <motion.main key="history" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.15 }} className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 flex flex-col">
            <h2 className="text-3xl font-extrabold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-slate-100 to-slate-400 flex items-center gap-3">
              <History className="w-8 h-8 text-indigo-400" /> Evaluation History
            </h2>
            <div className="flex flex-col gap-6 pb-20">
              {history.length === 0 ? (
                <div className="text-center py-20 bg-slate-900/40 rounded-3xl border border-slate-800 border-dashed">
                  <History className="w-12 h-12 text-slate-600 mx-auto mb-4 opacity-50" />
                  <p className="text-slate-400 font-medium">No evaluations recorded yet.</p>
                </div>
              ) : (
                history.map(item => (
                  <motion.div key={item.id} initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} className="bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-3xl p-6 shadow-xl hover:border-indigo-500/30 transition-colors">
                    <div className="flex justify-between items-center mb-4">
                      <span className="text-xs font-semibold px-3 py-1 rounded-full bg-slate-800 text-slate-400">{new Date(item.timestamp).toLocaleString()}</span>
                    </div>
                    <div className="font-medium text-slate-200 mb-6 bg-slate-950/80 p-5 rounded-2xl border border-slate-800/80 shadow-inner leading-relaxed">"{item.prompt}"</div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="bg-slate-950/50 p-5 rounded-2xl border border-slate-800">
                        <div className="text-xs text-indigo-400 font-bold uppercase tracking-wider mb-3 flex items-center justify-between">
                          {item.models.model1}
                          <span className="text-emerald-400/80 font-mono">{item.results.groq_1?.latency_ms || 0}ms</span>
                        </div>
                        <div className="text-sm text-slate-300 leading-relaxed max-h-40 overflow-y-auto custom-scrollbar pr-2 whitespace-pre-wrap">{item.results.groq_1?.content || 'Error'}</div>
                      </div>
                      <div className="bg-slate-950/50 p-5 rounded-2xl border border-slate-800">
                        <div className="text-xs text-indigo-400 font-bold uppercase tracking-wider mb-3 flex items-center justify-between">
                          {item.models.model2}
                          <span className="text-emerald-400/80 font-mono">{item.results.groq_2?.latency_ms || 0}ms</span>
                        </div>
                        <div className="text-sm text-slate-300 leading-relaxed max-h-40 overflow-y-auto custom-scrollbar pr-2 whitespace-pre-wrap">{item.results.groq_2?.content || 'Error'}</div>
                      </div>
                    </div>
                  </motion.div>
                ))
              )}
            </div>
          </motion.main>
        )}

        {/* SETTINGS VIEW */}
        {currentView === 'settings' && (
          <motion.main key="settings" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.15 }} className="flex-1 max-w-3xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 flex flex-col">
            <h2 className="text-3xl font-extrabold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-slate-100 to-slate-400 flex items-center gap-3">
              <Settings className="w-8 h-8 text-indigo-400" /> Pipeline Settings
            </h2>
            <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-3xl p-8 shadow-xl">
              <div className="flex flex-col gap-8">
                <div>
                  <h3 className="text-lg font-semibold text-slate-200 mb-1">Model Configuration</h3>
                  <p className="text-sm text-slate-500 mb-6">Customize the display names for the AI models used in the evaluation pipeline.</p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 block ml-1">Model 1 Display Name</label>
                      <input type="text" value={settings.model1Name} onChange={(e) => setSettings({...settings, model1Name: e.target.value})} 
                        className="w-full bg-slate-950/80 border border-slate-700 rounded-xl p-4 text-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-colors" />
                    </div>
                    <div>
                      <label className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 block ml-1">Model 2 Display Name</label>
                      <input type="text" value={settings.model2Name} onChange={(e) => setSettings({...settings, model2Name: e.target.value})} 
                        className="w-full bg-slate-950/80 border border-slate-700 rounded-xl p-4 text-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-colors" />
                    </div>
                  </div>
                </div>
                
                <div className="pt-8 mt-4 border-t border-slate-800/80">
                  <h3 className="text-lg font-semibold text-slate-200 mb-1">Account</h3>
                  <p className="text-sm text-slate-500 mb-6">Signed in as <span className="text-indigo-400 font-medium">{user}</span></p>
                  <button onClick={handleLogout} className="px-6 py-3 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 rounded-xl font-semibold transition-colors flex items-center gap-2">
                    <LogOut className="w-4 h-4" /> Sign Out
                  </button>
                </div>
              </div>
            </div>
          </motion.main>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
