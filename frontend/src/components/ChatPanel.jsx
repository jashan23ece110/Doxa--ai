import React, { useState, useRef, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, MicOff, Globe, Bot, User, Loader2, Cpu, MessageSquare } from 'lucide-react';

export default function ChatPanel({
  chatHistory = [],
  agentGoal = '',
  setAgentGoal,
  agentLoading = false,
  agentError = null,
  onStartAgent,
  chatMode = 'ask',
  setChatMode,
  language = 'english',
  setLanguage,
}) {
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef(null);
  const historyEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll chat history to bottom
  useEffect(() => {
    if (historyEndRef.current) {
      historyEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatHistory, agentLoading]);

  // Voice recording logic via Web Speech API
  const toggleVoiceInput = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Voice recognition not supported in this browser.');
      return;
    }

    if (isRecording && recognitionRef.current) {
      recognitionRef.current.stop();
      setIsRecording(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = language === 'hinglish' ? 'hi-IN' : 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setAgentGoal((prev) => (prev ? `${prev} ${transcript}` : transcript));
      setIsRecording(false);
    };

    recognition.onerror = () => setIsRecording(false);
    recognition.onend = () => setIsRecording(false);

    recognitionRef.current = recognition;
    recognition.start();
    setIsRecording(true);
  }, [isRecording, setAgentGoal, language]);

  // Clean up recording on unmount
  useEffect(() => {
    return () => {
      if (recognitionRef.current) recognitionRef.current.abort();
    };
  }, []);

  return (
    <div className="w-full max-w-4xl mx-auto px-4 pb-6 pt-2 z-30 pointer-events-auto">
      <div 
        className="backdrop-blur-md bg-neutral-950/75 border border-[#ffd60a]/15 rounded-2xl shadow-[0_0_30px_rgba(0,0,0,0.5)] overflow-hidden flex flex-col transition-all duration-300"
      >
        {/* ── Chat History (only shown when history has items or agent is loading) ── */}
        <AnimatePresence>
          {(chatHistory.length > 0 || agentLoading) && (
            <motion.div 
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="border-b border-[#ffd60a]/10 max-h-48 overflow-y-auto hud-scrollbar p-4 flex flex-col gap-3 bg-neutral-950/40"
            >
              {chatHistory.map((msg, i) => (
                <div 
                  key={msg.id || i}
                  className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'self-end flex-row-reverse' : 'self-start'}`}
                >
                  <div className={`w-7 h-7 rounded-lg border flex items-center justify-center shrink-0 ${
                    msg.role === 'user' 
                      ? 'bg-neutral-900 border-[#ffd60a]/20 text-[#ffd60a]' 
                      : 'bg-[#ffd60a]/10 border-[#ffd60a]/30 text-[#ffd60a]'
                  }`}>
                    {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                  </div>
                  <div className={`p-3 rounded-xl text-sm leading-relaxed border ${
                    msg.role === 'user'
                      ? 'bg-neutral-900/80 border-[#ffd60a]/10 text-[#e0d6c2]'
                      : 'bg-[#ffd60a]/5 border-[#ffd60a]/15 text-white'
                  }`} style={{ fontFamily: 'Rajdhani, sans-serif' }}>
                    <p className="whitespace-pre-wrap">{msg.text}</p>
                    {msg.mode && (
                      <span className="text-[9px] uppercase tracking-widest text-[#7a7060] block mt-1">
                        {msg.mode} Mode
                      </span>
                    )}
                  </div>
                </div>
              ))}

              {/* Agent Active Processing / Thinking Indicator */}
              {agentLoading && (
                <div className="flex gap-3 self-start items-center">
                  <div className="w-7 h-7 rounded-lg border bg-[#ffd60a]/10 border-[#ffd60a]/30 text-[#ffd60a] flex items-center justify-center animate-pulse">
                    <Bot className="w-4 h-4" />
                  </div>
                  <div className="flex items-center gap-1.5 px-3 py-2 bg-[#ffd60a]/5 border border-[#ffd60a]/10 rounded-xl text-xs text-[#ffd60a]">
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Doxa processing...</span>
                  </div>
                </div>
              )}
              
              <div ref={historyEndRef} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── Controls Row (Mode & Language Selectors) ── */}
        <div className="flex items-center justify-between px-4 py-2 bg-neutral-950/60 border-b border-[#ffd60a]/5 text-xs">
          {/* Mode Selector */}
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={() => setChatMode('ask')}
              className={`flex items-center gap-1 px-3 py-1 rounded-lg font-semibold transition-all duration-200 border ${
                chatMode === 'ask'
                  ? 'bg-[#ffd60a]/15 border-[#ffd60a]/30 text-[#ffd60a] shadow-[0_0_10px_rgba(255,214,10,0.1)]'
                  : 'bg-transparent border-transparent text-[#7a7060] hover:text-[#e0d6c2]'
              }`}
            >
              <MessageSquare className="w-3.5 h-3.5" />
              Ask Anything
            </button>
            <button
              type="button"
              onClick={() => setChatMode('agentic')}
              className={`flex items-center gap-1 px-3 py-1 rounded-lg font-semibold transition-all duration-200 border ${
                chatMode === 'agentic'
                  ? 'bg-[#ffd60a]/15 border-[#ffd60a]/30 text-[#ffd60a] shadow-[0_0_10px_rgba(255,214,10,0.1)]'
                  : 'bg-transparent border-transparent text-[#7a7060] hover:text-[#e0d6c2]'
              }`}
            >
              <Cpu className="w-3.5 h-3.5" />
              Agentic Mode
            </button>
          </div>

          {/* Language Selector */}
          <div className="flex items-center gap-1 bg-neutral-900/60 p-0.5 rounded-lg border border-[#ffd60a]/5">
            <button
              type="button"
              onClick={() => setLanguage('english')}
              className={`px-2 py-0.5 rounded font-semibold transition-all duration-150 ${
                language === 'english'
                  ? 'bg-[#ffd60a]/20 text-[#ffd60a]'
                  : 'text-[#7a7060] hover:text-[#e0d6c2]'
              }`}
            >
              EN
            </button>
            <button
              type="button"
              onClick={() => setLanguage('hinglish')}
              className={`px-2 py-0.5 rounded font-semibold transition-all duration-150 ${
                language === 'hinglish'
                  ? 'bg-[#ffd60a]/20 text-[#ffd60a]'
                  : 'text-[#7a7060] hover:text-[#e0d6c2]'
              }`}
            >
              HINGLISH
            </button>
          </div>
        </div>

        {/* ── Main Input Form ── */}
        <form onSubmit={onStartAgent} className="flex items-center p-3 gap-2 bg-neutral-950/20">
          <input
            ref={inputRef}
            type="text"
            value={agentGoal}
            onChange={(e) => setAgentGoal(e.target.value)}
            disabled={agentLoading}
            placeholder={
              isRecording 
                ? 'Listening...' 
                : chatMode === 'agentic'
                  ? 'Ask Doxa to execute a complex task...'
                  : 'Ask Doxa anything...'
            }
            className="flex-1 bg-neutral-900 border border-[#ffd60a]/10 rounded-xl px-4 py-3 text-sm text-white placeholder-[#7a7060] focus:outline-none focus:border-[#ffd60a]/30 focus:shadow-[0_0_15px_rgba(255,214,10,0.05)] transition-all"
            style={{ fontFamily: 'Rajdhani, sans-serif' }}
          />

          {/* Mic (Voice input) Button */}
          <button
            type="button"
            onClick={toggleVoiceInput}
            disabled={agentLoading}
            className={`w-11 h-11 rounded-xl flex items-center justify-center border transition-all ${
              isRecording 
                ? 'bg-red-500/20 border-red-500/40 text-red-400 animate-pulse'
                : 'bg-neutral-900 border-[#ffd60a]/10 text-[#7a7060] hover:text-white hover:border-[#ffd60a]/30'
            }`}
          >
            {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
          </button>

          {/* Send Button */}
          <button
            type="submit"
            disabled={agentLoading || !agentGoal.trim()}
            className={`w-11 h-11 rounded-xl flex items-center justify-center transition-all ${
              !agentGoal.trim() || agentLoading
                ? 'bg-neutral-900 border border-[#ffd60a]/5 text-[#7a7060] cursor-not-allowed'
                : 'bg-[#ffd60a] text-neutral-950 hover:bg-[#ffe44d] hover:shadow-[0_0_15px_rgba(255,214,10,0.3)]'
            }`}
          >
            <Send className="w-5 h-5" />
          </button>
        </form>

        {/* ── Error Output (if any) ── */}
        {agentError && (
          <div className="px-4 py-2 bg-red-500/10 border-t border-red-500/20 text-red-400 text-xs font-semibold flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-ping" />
            <span>{agentError}</span>
          </div>
        )}
      </div>
    </div>
  );
}
