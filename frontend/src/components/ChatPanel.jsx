import React, { useState, useRef, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, MicOff, Globe, Bot, User, Loader2, Cpu, MessageSquare, Upload, GitBranch, Sparkles } from 'lucide-react';
import MarkdownRenderer from './MarkdownRenderer';
import TaskChecklistCard from './TaskChecklistCard';
import ReasoningViewCard from './ReasoningViewCard';
import CitationPanel from './CitationPanel';

export default function ChatPanel({
  chatHistory = [],
  fullHistory = [],
  activeMessageId = null,
  setActiveMessageId,
  agentGoal = '',
  setAgentGoal,
  agentLoading = false,
  agentStatus = null,
  agentError = null,
  onStartAgent,
  chatMode = 'ask',
  setChatMode,
  language = 'english',
  setLanguage,
  toggleSidebar,
  onExportChat,
  onUploadDoc,
  proactiveSuggestions = [],
  setProactiveSuggestions,
}) {
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef(null);
  const historyEndRef = useRef(null);
  const inputRef = useRef(null);
  const fileInputRef = useRef(null);

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
        className="backdrop-blur-xl bg-black/15 border border-[var(--jarvis-accent)]/20 rounded-2xl shadow-[0_0_40px_rgba(0,0,0,0.6)] overflow-hidden flex flex-col transition-all duration-300"
      >
        {/* ── Chat History Drawer (Floating Upward Answer Stream) ── */}
        <AnimatePresence>
          {true && (
            <motion.div 
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="border-b border-[var(--jarvis-accent)]/10 max-h-[380px] overflow-y-auto hud-scrollbar p-4 flex flex-col gap-4 bg-transparent"
            >
              {chatHistory.length === 0 && !agentLoading ? (
                <div className="flex flex-col items-center justify-center py-6 text-center text-neutral-500 font-mono text-xs select-none">
                  <Sparkles className="w-5 h-5 mb-1.5 text-[var(--jarvis-accent)]/40 animate-pulse" />
                  <p className="tracking-wider text-[#7a7060] font-semibold">No conversations yet — start by asking something!</p>
                </div>
              ) : (
                <>
                  {/* Time-Travel Branch Switcher Header */}
                  {(() => {
                    const leaves = (fullHistory || []).filter(msg => msg && msg.id && !(fullHistory || []).some(m => m && m.parentId === msg.id));
                    if (leaves.length <= 1) return null;
                    return (
                      <div className="flex flex-col gap-2 pb-3 mb-2 border-b border-[var(--jarvis-accent)]/10">
                        <div className="flex items-center gap-2 text-[#7a7060] font-mono text-[9px] uppercase tracking-wider">
                          <GitBranch className="w-3.5 h-3.5 text-[var(--jarvis-accent)]" />
                          <span>Conversational Timelines</span>
                        </div>
                        <div className="flex gap-2 flex-wrap max-h-12 overflow-y-auto hud-scrollbar">
                          {leaves.map((leaf, idx) => {
                            if (!leaf) return null;
                            const chain = [];
                            let curr = leaf;
                            const visited = new Set();
                            while (curr && !visited.has(curr.id)) {
                              visited.add(curr.id);
                              chain.unshift(curr);
                              curr = (fullHistory || []).find(m => m && m.id === curr.parentId);
                            }
                            const lastUser = [...chain].reverse().find(m => m && m.role === 'user');
                            const label = lastUser ? `"${(lastUser.text || lastUser.content || "").substring(0, 16)}..."` : `Timeline ${idx + 1}`;
                            const isActive = activeMessageId === leaf.id || chain.some(m => m && m.id === activeMessageId);
                            
                            return (
                              <button
                                key={leaf.id}
                                onClick={() => setActiveMessageId(leaf.id)}
                                className={`px-2 py-0.5 rounded text-[9px] font-mono border transition-all duration-100 ${
                                  isActive 
                                    ? 'bg-[var(--jarvis-accent)]/15 border-[var(--jarvis-accent)]/40 text-[var(--jarvis-accent)] font-semibold shadow-[0_0_8px_rgba(var(--jarvis-accent-rgb),0.15)]' 
                                    : 'bg-neutral-900 border-neutral-800 text-[#7a7060] hover:text-[#e0d6c2] hover:border-neutral-700'
                                }`}
                              >
                                {label}
                              </button>
                            );
                          })}
                        </div>
                      </div>
                    );
                  })()}

                  {chatHistory.map((msg, i) => {
                    if (!msg) return null;
                    return (
                      <div 
                        key={msg.id || i}
                        className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'self-end flex-row-reverse' : 'self-start'}`}
                      >
                        <div className={`w-7 h-7 rounded-lg border flex items-center justify-center shrink-0 ${
                          msg.role === 'user' 
                            ? 'bg-neutral-900 border-[var(--jarvis-accent)]/20 text-[var(--jarvis-accent)]' 
                            : 'bg-[var(--jarvis-accent)]/10 border-[var(--jarvis-accent)]/30 text-[var(--jarvis-accent)]'
                        }`}>
                          {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                        </div>
                        <div className={`p-4 rounded-xl text-sm leading-relaxed border transition-all duration-300 ${
                          msg.role === 'user'
                            ? 'bg-neutral-950/70 backdrop-blur-md border-[var(--jarvis-accent)]/15 text-[#e0d6c2] shadow-lg'
                            : 'bg-black/45 backdrop-blur-xl border-[var(--jarvis-accent)]/25 text-white shadow-[0_10px_30px_rgba(0,0,0,0.7)]'
                        }`} style={{ fontFamily: 'Rajdhani, sans-serif' }}>
                          {msg.role === 'user' ? (
                            <p className="whitespace-pre-wrap">{msg.text}</p>
                          ) : (
                            <MarkdownRenderer content={msg.text} />
                          )}
                          {msg.role === 'assistant' && (
                            <CitationPanel text={msg.text} steps={agentStatus?.steps} />
                          )}
                          <div className="flex items-center justify-between gap-4 mt-2 pt-1.5 border-t border-[var(--jarvis-accent)]/5 text-[9px] text-[#7a7060] min-w-[140px] font-mono">
                            <span>{msg.mode ? `${msg.mode.toUpperCase()} MODE` : 'DIRECT'}</span>
                            {msg.id && (
                              <button
                                onClick={() => {
                                  setActiveMessageId(msg.id);
                                  setTimeout(() => {
                                    const inputEl = document.querySelector('input[placeholder*="Ask"]');
                                    if (inputEl) inputEl.focus();
                                  }, 100);
                                }}
                                className="flex items-center gap-1 hover:text-[var(--jarvis-accent)] transition-colors cursor-pointer"
                                title="Branch conversation from this message"
                              >
                                <GitBranch className="w-2.5 h-2.5" />
                                <span>BRANCH</span>
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}

                  {/* Sticky Plan Execution Checklist */}
                  {agentStatus?.plan && agentStatus.plan.length > 0 && (
                    <TaskChecklistCard 
                      plan={agentStatus.plan} 
                      steps={agentStatus.steps} 
                      isCompleted={agentStatus.status === 'completed'} 
                    />
                  )}

                  {/* Collapsible Reasoning & Tool Call View */}
                  {agentStatus?.steps && agentStatus.steps.length > 0 && (
                    <ReasoningViewCard 
                      steps={agentStatus.steps} 
                      selfCheck={agentStatus.self_check} 
                    />
                  )}

                  {/* Parallel Debate Panel */}
                  {(agentStatus?.debate_a || agentStatus?.debate_b || (agentLoading && agentStatus?.steps?.some(s => s.step.toLowerCase().includes('debate')))) && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-3 w-full animate-fade-in font-mono text-xs">
                      {/* Perspective A: Optimist */}
                      <div className="backdrop-blur-md bg-[rgba(220,20,60,0.06)] border border-red-500/25 p-4 rounded-xl shadow-lg flex flex-col gap-2 relative overflow-hidden">
                        <div className="absolute top-0 right-0 px-2 py-0.5 bg-red-600/35 border-l border-b border-red-500/30 text-[8px] tracking-wider uppercase font-bold text-red-400">
                          OPTIMIST CORE
                        </div>
                        <div className="text-[10px] tracking-widest text-red-400 uppercase font-semibold border-b border-red-500/10 pb-1 flex items-center gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-ping" />
                          Perspective A
                        </div>
                        <p className="text-[#e0d6c2]/90 leading-relaxed text-[11px] font-sans">
                          {agentStatus?.debate_a || "Generating optimistic argument..."}
                        </p>
                      </div>

                      {/* Perspective B: Skeptic */}
                      <div className="backdrop-blur-md bg-[rgba(0,217,255,0.06)] border border-cyan-500/25 p-4 rounded-xl shadow-lg flex flex-col gap-2 relative overflow-hidden">
                        <div className="absolute top-0 right-0 px-2 py-0.5 bg-cyan-600/35 border-l border-b border-cyan-500/30 text-[8px] tracking-wider uppercase font-bold text-cyan-400">
                          SKEPTIC CORE
                        </div>
                        <div className="text-[10px] tracking-widest text-cyan-400 uppercase font-semibold border-b border-cyan-500/10 pb-1 flex items-center gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-ping" />
                          Perspective B
                        </div>
                        <p className="text-[#e0d6c2]/90 leading-relaxed text-[11px] font-sans">
                          {agentStatus?.debate_b || "Generating skeptical counter-argument..."}
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Agent Active Processing / Thinking Indicator & Step Progress Timeline */}
                  {agentLoading && (
                    <div className="flex flex-col gap-3.5 self-start w-full max-w-[480px]">
                      <div className="flex gap-3 items-center">
                        <div className="w-7 h-7 rounded-lg border bg-[var(--jarvis-accent)]/10 border-[var(--jarvis-accent)]/30 text-[var(--jarvis-accent)] flex items-center justify-center animate-pulse">
                          <Bot className="w-4 h-4" />
                        </div>
                        <div className="flex items-center gap-1.5 px-3 py-2 bg-[var(--jarvis-accent)]/5 border border-[var(--jarvis-accent)]/10 rounded-xl text-xs text-[var(--jarvis-accent)]">
                          <Loader2 className="w-3.5 h-3.5 animate-spin" />
                          <span>
                            {(() => {
                              const status = agentStatus?.status || 'running';
                              const steps = agentStatus?.steps || [];
                              let currentPhase = 'Planning';
                              if (status === 'completed') currentPhase = 'Done';
                              else if (status === 'failed') currentPhase = 'Failed';
                              else if (steps.length > 0) {
                                const lastStep = steps[steps.length - 1].step || '';
                                if (lastStep.includes('Self Check')) currentPhase = 'Reviewing';
                                else if (lastStep.includes('Executing') || lastStep.includes('Direct') || lastStep.includes('Retrying')) currentPhase = 'Executing';
                              }

                              if (currentPhase === 'Planning') return 'Doxa is analyzing and planning...';
                              if (currentPhase === 'Executing') return 'Doxa is searching & gathering context...';
                              if (currentPhase === 'Reviewing') return 'Doxa is evaluating results...';
                              if (currentPhase === 'Done') return 'Response complete.';
                              return 'Doxa processing...';
                            })()}
                          </span>
                        </div>
                      </div>
                      
                      {/* Step-by-Step Visual Progress Timeline (sci-fi HUD styling) */}
                      {(() => {
                        const status = agentStatus?.status || 'running';
                        const steps = agentStatus?.steps || [];
                        let currentPhase = 'Planning';
                        if (status === 'completed') currentPhase = 'Done';
                        else if (status === 'failed') currentPhase = 'Failed';
                        else if (steps.length > 0) {
                          const lastStep = steps[steps.length - 1].step || '';
                          if (lastStep.includes('Self Check')) currentPhase = 'Reviewing';
                          else if (lastStep.includes('Executing') || lastStep.includes('Direct') || lastStep.includes('Retrying')) currentPhase = 'Executing';
                        }

                        return (
                          <div className="flex items-center justify-between px-3 py-2 bg-neutral-900/60 border border-[var(--jarvis-accent)]/10 rounded-xl text-[10px] tracking-wider text-neutral-400 font-medium w-full" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                            {/* Planning Step */}
                            <div className="flex items-center gap-1.5">
                              <span className={`w-1.5 h-1.5 rounded-full ${
                                currentPhase === 'Planning' ? 'bg-[var(--jarvis-accent-hover)] animate-pulse' : 'bg-[var(--jarvis-accent)]'
                              }`} />
                              <span className={currentPhase === 'Planning' ? 'text-[var(--jarvis-accent-hover)] font-bold' : 'text-neutral-400'}>PLANNING</span>
                            </div>
                            
                            <span className="text-neutral-600">➔</span>
                            
                            {/* Executing Step */}
                            <div className="flex items-center gap-1.5">
                              <span className={`w-1.5 h-1.5 rounded-full ${
                                currentPhase === 'Executing' ? 'bg-[var(--jarvis-accent-hover)] animate-pulse' : 
                                (currentPhase === 'Reviewing' || currentPhase === 'Done') ? 'bg-[var(--jarvis-accent)]' : 'bg-neutral-600'
                              }`} />
                              <span className={currentPhase === 'Executing' ? 'text-[var(--jarvis-accent-hover)] font-bold' : 
                                (currentPhase === 'Reviewing' || currentPhase === 'Done') ? 'text-neutral-300' : 'text-neutral-600'}>EXECUTING</span>
                            </div>
                            
                            <span className="text-neutral-600">➔</span>
                            
                            {/* Reviewing Step */}
                            <div className="flex items-center gap-1.5">
                              <span className={`w-1.5 h-1.5 rounded-full ${
                                currentPhase === 'Reviewing' ? 'bg-[var(--jarvis-accent-hover)] animate-pulse' : 
                                currentPhase === 'Done' ? 'bg-[var(--jarvis-accent)]' : 'bg-neutral-600'
                              }`} />
                              <span className={currentPhase === 'Reviewing' ? 'text-[var(--jarvis-accent-hover)] font-bold' : 
                                currentPhase === 'Done' ? 'text-neutral-300' : 'text-neutral-600'}>REVIEWING</span>
                            </div>
                            
                            <span className="text-neutral-600">➔</span>
                            
                            {/* Done Step */}
                            <div className="flex items-center gap-1.5">
                              <span className={`w-1.5 h-1.5 rounded-full ${
                                currentPhase === 'Done' ? 'bg-[var(--jarvis-accent)]' : 'bg-neutral-600'
                              }`} />
                              <span className={currentPhase === 'Done' ? 'text-[var(--jarvis-accent)] font-bold' : 'text-neutral-600'}>DONE</span>
                            </div>
                          </div>
                        );
                      })()}
                    </div>
                  )}
                </>
              )}
              
              <div ref={historyEndRef} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── Controls Row (Mode & Language Selectors) ── */}
        <div className="flex items-center justify-between px-4 py-2 bg-neutral-950/60 border-b border-[var(--jarvis-accent)]/5 text-xs">
          {/* Mode Selector & Sidebar Toggle */}
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={toggleSidebar}
              className="flex items-center gap-1.5 px-2 py-1 rounded-lg font-semibold border border-neutral-800 text-[#7a7060] hover:text-[#e0d6c2] hover:border-neutral-700 transition-all"
              title="Toggle Conversational History Sidebar"
            >
              <MessageSquare className="w-3.5 h-3.5" />
              Chats
            </button>
            <div className="w-px h-3.5 bg-neutral-800 mx-1" />
            <button
              type="button"
              onClick={() => setChatMode('ask')}
              className={`flex items-center gap-1 px-3 py-1 rounded-lg font-semibold transition-all duration-200 border ${
                chatMode === 'ask'
                  ? 'bg-[var(--jarvis-accent)]/15 border-[var(--jarvis-accent)]/30 text-[var(--jarvis-accent)] shadow-[0_0_10px_rgba(var(--jarvis-accent-rgb),0.1)]'
                  : 'bg-transparent border-transparent text-[#7a7060] hover:text-[#e0d6c2]'
              }`}
            >
              Ask Anything
            </button>
            <button
              type="button"
              onClick={() => setChatMode('agentic')}
              className={`flex items-center gap-1 px-3 py-1 rounded-lg font-semibold transition-all duration-200 border ${
                chatMode === 'agentic'
                  ? 'bg-[var(--jarvis-accent)]/15 border-[var(--jarvis-accent)]/30 text-[var(--jarvis-accent)] shadow-[0_0_10px_rgba(var(--jarvis-accent-rgb),0.1)]'
                  : 'bg-transparent border-transparent text-[#7a7060] hover:text-[#e0d6c2]'
              }`}
            >
              <Cpu className="w-3.5 h-3.5" />
              Agentic Mode
            </button>
          </div>

          {/* Language Selector & Export Chat */}
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onExportChat}
              disabled={chatHistory.length === 0}
              className={`px-2.5 py-1 rounded-lg font-semibold border transition-all ${
                chatHistory.length === 0 
                  ? 'border-transparent text-neutral-800 cursor-not-allowed'
                  : 'border-neutral-800 text-[#7a7060] hover:text-[#e0d6c2] hover:border-neutral-700'
              }`}
              title="Export conversation to Markdown"
            >
              Export
            </button>
            <div className="flex items-center gap-1 bg-neutral-900/60 p-0.5 rounded-lg border border-[var(--jarvis-accent)]/5">
              <button
                type="button"
                onClick={() => setLanguage('english')}
                className={`px-2 py-0.5 rounded font-semibold transition-all duration-150 ${
                  language === 'english'
                    ? 'bg-[var(--jarvis-accent)]/20 text-[var(--jarvis-accent)]'
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
                    ? 'bg-[var(--jarvis-accent)]/20 text-[var(--jarvis-accent)]'
                    : 'text-[#7a7060] hover:text-[#e0d6c2]'
                }`}
              >
                HINGLISH
              </button>
            </div>
          </div>
        </div>

        {/* Proactive Suggestions Chips */}
        {proactiveSuggestions.length > 0 && !agentLoading && (
          <div className="flex items-center gap-2 px-4 py-2 border-b border-[var(--jarvis-accent)]/5 bg-neutral-950/30 flex-wrap">
            <span className="text-[9px] font-mono text-[#7a7060] uppercase tracking-wider select-none mr-1 flex items-center gap-1">
              <Sparkles className="w-2.5 h-2.5 text-[var(--jarvis-accent)] animate-pulse" />
              Suggested:
            </span>
            {proactiveSuggestions.map((s, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => {
                  setAgentGoal(s.prompt);
                  setProactiveSuggestions([]);
                  setTimeout(() => {
                    if (inputRef.current) {
                      const form = inputRef.current.form;
                      if (form) {
                        const event = new Event('submit', { cancelable: true, bubbles: true });
                        form.dispatchEvent(event);
                      }
                    }
                  }, 100);
                }}
                className="px-2.5 py-1 bg-neutral-900/60 border border-neutral-850 rounded-lg text-[10px] text-[#e0d6c2] hover:text-[var(--jarvis-accent)] hover:border-[var(--jarvis-accent)]/30 hover:bg-neutral-800 transition-all duration-150 font-medium cursor-pointer"
              >
                {s.text}
              </button>
            ))}
          </div>
        )}

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
            className="flex-1 bg-neutral-900 border border-[var(--jarvis-accent)]/10 rounded-xl px-3 md:px-4 py-2.5 md:py-3 text-xs md:text-sm text-white placeholder-[#7a7060] focus:outline-none focus:border-[var(--jarvis-accent)]/30 focus:shadow-[0_0_15px_rgba(var(--jarvis-accent-rgb),0.05)] transition-all min-w-0"
            style={{ fontFamily: 'Rajdhani, sans-serif' }}
          />

          {/* File Upload Paperclip Button */}
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={agentLoading}
            className="w-10 h-10 md:w-11 md:h-11 rounded-xl flex items-center justify-center shrink-0 bg-neutral-900 border border-[var(--jarvis-accent)]/10 text-[#7a7060] hover:text-white hover:border-[var(--jarvis-accent)]/30 transition-all cursor-pointer"
            title="Upload document to Knowledge Base (RAG)"
          >
            <Upload className="w-4 h-4 md:w-5 md:h-5" />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            accept=".txt,.pdf,.md,.csv,.json"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file && onUploadDoc) {
                onUploadDoc(file);
              }
            }}
          />

          {/* Mic (Voice input) Button */}
          <button
            type="button"
            onClick={toggleVoiceInput}
            disabled={agentLoading}
            className={`w-10 h-10 md:w-11 md:h-11 rounded-xl flex items-center justify-center shrink-0 border transition-all ${
              isRecording 
                ? 'bg-red-500/20 border-red-500/40 text-red-400 animate-pulse'
                : 'bg-neutral-900 border-[var(--jarvis-accent)]/10 text-[#7a7060] hover:text-white hover:border-[var(--jarvis-accent)]/30'
            }`}
          >
            {isRecording ? <MicOff className="w-4 h-4 md:w-5 md:h-5" /> : <Mic className="w-4 h-4 md:w-5 md:h-5" />}
          </button>

          {/* Send Button */}
          <button
            type="submit"
            disabled={agentLoading || !agentGoal.trim()}
            className={`w-10 h-10 md:w-11 md:h-11 rounded-xl flex items-center justify-center shrink-0 transition-all ${
              !agentGoal.trim() || agentLoading
                ? 'bg-neutral-900 border border-[var(--jarvis-accent)]/5 text-[#7a7060] cursor-not-allowed'
                : 'bg-[var(--jarvis-accent)] text-neutral-950 hover:bg-[var(--jarvis-accent-hover)] hover:shadow-[0_0_15px_rgba(var(--jarvis-accent-rgb),0.3)]'
            }`}
          >
            <Send className="w-4 h-4 md:w-5 md:h-5" />
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
