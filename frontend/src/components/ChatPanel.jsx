import React, { useState, useRef, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, MicOff, Globe, Bot, User, Loader2, Cpu, MessageSquare, Upload } from 'lucide-react';
import MarkdownRenderer from './MarkdownRenderer';

export default function ChatPanel({
  chatHistory = [],
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
        className="backdrop-blur-md bg-neutral-950/75 border border-[#dc143c]/15 rounded-2xl shadow-[0_0_30px_rgba(0,0,0,0.5)] overflow-hidden flex flex-col transition-all duration-300"
      >
        {/* ── Chat History (only shown when history has items or agent is loading) ── */}
        <AnimatePresence>
          {(chatHistory.length > 0 || agentLoading) && (
            <motion.div 
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="border-b border-[#dc143c]/10 max-h-48 overflow-y-auto hud-scrollbar p-4 flex flex-col gap-3 bg-neutral-950/40"
            >
              {chatHistory.map((msg, i) => (
                <div 
                  key={msg.id || i}
                  className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'self-end flex-row-reverse' : 'self-start'}`}
                >
                  <div className={`w-7 h-7 rounded-lg border flex items-center justify-center shrink-0 ${
                    msg.role === 'user' 
                      ? 'bg-neutral-900 border-[#dc143c]/20 text-[#dc143c]' 
                      : 'bg-[#dc143c]/10 border-[#dc143c]/30 text-[#dc143c]'
                  }`}>
                    {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                  </div>
                  <div className={`p-3 rounded-xl text-sm leading-relaxed border ${
                    msg.role === 'user'
                      ? 'bg-neutral-900/80 border-[#dc143c]/10 text-[#e0d6c2]'
                      : 'bg-[#dc143c]/5 border-[#dc143c]/15 text-white'
                  }`} style={{ fontFamily: 'Rajdhani, sans-serif' }}>
                    {msg.role === 'user' ? (
                      <p className="whitespace-pre-wrap">{msg.text}</p>
                    ) : (
                      <MarkdownRenderer content={msg.text} />
                    )}
                    {msg.mode && (
                      <span className="text-[9px] uppercase tracking-widest text-[#7a7060] block mt-1">
                        {msg.mode} Mode
                      </span>
                    )}
                  </div>
                </div>
              ))}

              {/* Agent Active Processing / Thinking Indicator & Step Progress Timeline */}
              {agentLoading && (
                <div className="flex flex-col gap-3.5 self-start w-full max-w-[480px]">
                  <div className="flex gap-3 items-center">
                    <div className="w-7 h-7 rounded-lg border bg-[#dc143c]/10 border-[#dc143c]/30 text-[#dc143c] flex items-center justify-center animate-pulse">
                      <Bot className="w-4 h-4" />
                    </div>
                    <div className="flex items-center gap-1.5 px-3 py-2 bg-[#dc143c]/5 border border-[#dc143c]/10 rounded-xl text-xs text-[#dc143c]">
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
                      <div className="flex items-center justify-between px-3 py-2 bg-neutral-900/60 border border-[#dc143c]/10 rounded-xl text-[10px] tracking-wider text-neutral-400 font-medium w-full" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                        {/* Planning Step */}
                        <div className="flex items-center gap-1.5">
                          <span className={`w-1.5 h-1.5 rounded-full ${
                            currentPhase === 'Planning' ? 'bg-[#ff4500] animate-pulse' : 'bg-[#dc143c]'
                          }`} />
                          <span className={currentPhase === 'Planning' ? 'text-[#ff4500] font-bold' : 'text-neutral-400'}>PLANNING</span>
                        </div>
                        
                        <span className="text-neutral-600">➔</span>
                        
                        {/* Executing Step */}
                        <div className="flex items-center gap-1.5">
                          <span className={`w-1.5 h-1.5 rounded-full ${
                            currentPhase === 'Executing' ? 'bg-[#ff4500] animate-pulse' : 
                            (currentPhase === 'Reviewing' || currentPhase === 'Done') ? 'bg-[#dc143c]' : 'bg-neutral-600'
                          }`} />
                          <span className={currentPhase === 'Executing' ? 'text-[#ff4500] font-bold' : 
                            (currentPhase === 'Reviewing' || currentPhase === 'Done') ? 'text-neutral-300' : 'text-neutral-600'}>EXECUTING</span>
                        </div>
                        
                        <span className="text-neutral-600">➔</span>
                        
                        {/* Reviewing Step */}
                        <div className="flex items-center gap-1.5">
                          <span className={`w-1.5 h-1.5 rounded-full ${
                            currentPhase === 'Reviewing' ? 'bg-[#ff4500] animate-pulse' : 
                            currentPhase === 'Done' ? 'bg-[#dc143c]' : 'bg-neutral-600'
                          }`} />
                          <span className={currentPhase === 'Reviewing' ? 'text-[#ff4500] font-bold' : 
                            currentPhase === 'Done' ? 'text-neutral-300' : 'text-neutral-600'}>REVIEWING</span>
                        </div>
                        
                        <span className="text-neutral-600">➔</span>
                        
                        {/* Done Step */}
                        <div className="flex items-center gap-1.5">
                          <span className={`w-1.5 h-1.5 rounded-full ${
                            currentPhase === 'Done' ? 'bg-[#dc143c]' : 'bg-neutral-600'
                          }`} />
                          <span className={currentPhase === 'Done' ? 'text-[#dc143c] font-bold' : 'text-neutral-600'}>DONE</span>
                        </div>
                      </div>
                    );
                  })()}
                </div>
              )}
              
              <div ref={historyEndRef} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── Controls Row (Mode & Language Selectors) ── */}
        <div className="flex items-center justify-between px-4 py-2 bg-neutral-950/60 border-b border-[#dc143c]/5 text-xs">
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
                  ? 'bg-[#dc143c]/15 border-[#dc143c]/30 text-[#dc143c] shadow-[0_0_10px_rgba(220, 20, 60,0.1)]'
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
                  ? 'bg-[#dc143c]/15 border-[#dc143c]/30 text-[#dc143c] shadow-[0_0_10px_rgba(220, 20, 60,0.1)]'
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
            <div className="flex items-center gap-1 bg-neutral-900/60 p-0.5 rounded-lg border border-[#dc143c]/5">
              <button
                type="button"
                onClick={() => setLanguage('english')}
                className={`px-2 py-0.5 rounded font-semibold transition-all duration-150 ${
                  language === 'english'
                    ? 'bg-[#dc143c]/20 text-[#dc143c]'
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
                    ? 'bg-[#dc143c]/20 text-[#dc143c]'
                    : 'text-[#7a7060] hover:text-[#e0d6c2]'
                }`}
              >
                HINGLISH
              </button>
            </div>
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
            className="flex-1 bg-neutral-900 border border-[#dc143c]/10 rounded-xl px-4 py-3 text-sm text-white placeholder-[#7a7060] focus:outline-none focus:border-[#dc143c]/30 focus:shadow-[0_0_15px_rgba(220, 20, 60,0.05)] transition-all"
            style={{ fontFamily: 'Rajdhani, sans-serif' }}
          />

          {/* File Upload Paperclip Button */}
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={agentLoading}
            className="w-11 h-11 rounded-xl flex items-center justify-center bg-neutral-900 border border-[#dc143c]/10 text-[#7a7060] hover:text-white hover:border-[#dc143c]/30 transition-all cursor-pointer"
            title="Upload document to Knowledge Base (RAG)"
          >
            <Upload className="w-5 h-5" />
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
            className={`w-11 h-11 rounded-xl flex items-center justify-center border transition-all ${
              isRecording 
                ? 'bg-red-500/20 border-red-500/40 text-red-400 animate-pulse'
                : 'bg-neutral-900 border-[#dc143c]/10 text-[#7a7060] hover:text-white hover:border-[#dc143c]/30'
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
                ? 'bg-neutral-900 border border-[#dc143c]/5 text-[#7a7060] cursor-not-allowed'
                : 'bg-[#dc143c] text-neutral-950 hover:bg-[#ff4500] hover:shadow-[0_0_15px_rgba(220, 20, 60,0.3)]'
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
