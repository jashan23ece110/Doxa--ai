import React, { useState, useRef, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  X,
  Mic,
  MicOff,
  Play,
  Loader2,
  CheckCircle2,
  AlertTriangle,
  Terminal,
  MessageSquare,
  Cpu,
  Send,
} from 'lucide-react';

const overlayVariants = {
  initial: { opacity: 0, scale: 0.95, y: 20 },
  animate: { opacity: 1, scale: 1, y: 0, transition: { duration: 0.3, ease: 'easeOut' } },
  exit: { opacity: 0, scale: 0.95, y: 20, transition: { duration: 0.2, ease: 'easeIn' } },
};

const backdropVariants = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.25 } },
  exit: { opacity: 0, transition: { duration: 0.2 } },
};

const stepVariants = {
  initial: { opacity: 0, x: -12 },
  animate: { opacity: 1, x: 0, transition: { duration: 0.25 } },
};

const TOOL_EMOJI = {
  search: '🔍',
  browse: '🌐',
  code: '💻',
  write: '✍️',
  read: '📖',
  execute: '⚡',
  analyze: '🧠',
  default: '🔧',
};

function getToolEmoji(tool) {
  if (!tool) return TOOL_EMOJI.default;
  const lower = tool.toLowerCase();
  for (const [key, emoji] of Object.entries(TOOL_EMOJI)) {
    if (lower.includes(key)) return emoji;
  }
  return TOOL_EMOJI.default;
}

function StatusBadge({ status }) {
  if (!status) return null;

  const config = {
    running: { icon: Loader2, color: '#ffd60a', label: 'RUNNING', spin: true },
    completed: { icon: CheckCircle2, color: '#00ff88', label: 'COMPLETED', spin: false },
    failed: { icon: AlertTriangle, color: '#ff4757', label: 'FAILED', spin: false },
  };

  const c = config[status] || config.running;
  const Icon = c.icon;

  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
        padding: '4px 12px',
        borderRadius: '9999px',
        border: `1px solid ${c.color}33`,
        backgroundColor: `${c.color}11`,
        fontSize: '11px',
        fontFamily: "'JetBrains Mono', monospace",
        color: c.color,
        textTransform: 'uppercase',
        letterSpacing: '0.08em',
      }}
    >
      <Icon
        size={13}
        style={c.spin ? { animation: 'spin 1.2s linear infinite' } : {}}
      />
      {c.label}
    </div>
  );
}

/* ─── Mode Toggle Switch ─── */
function ModeToggle({ mode, onChange }) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0',
        padding: '3px',
        borderRadius: '10px',
        border: '1px solid rgba(255, 214, 10, 0.15)',
        background: 'rgba(255, 214, 10, 0.03)',
      }}
    >
      <button
        type="button"
        onClick={() => onChange('ask')}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '5px',
          padding: '5px 12px',
          borderRadius: '8px',
          border: 'none',
          cursor: 'pointer',
          fontFamily: "'Rajdhani', sans-serif",
          fontSize: '12px',
          fontWeight: 600,
          letterSpacing: '0.04em',
          transition: 'all 0.2s',
          background: mode === 'ask' ? 'rgba(255, 214, 10, 0.15)' : 'transparent',
          color: mode === 'ask' ? '#ffd60a' : '#7a7060',
          boxShadow: mode === 'ask' ? '0 0 12px rgba(255, 214, 10, 0.12)' : 'none',
        }}
      >
        <MessageSquare size={12} />
        Ask Anything
      </button>
      <button
        type="button"
        onClick={() => onChange('agentic')}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '5px',
          padding: '5px 12px',
          borderRadius: '8px',
          border: 'none',
          cursor: 'pointer',
          fontFamily: "'Rajdhani', sans-serif",
          fontSize: '12px',
          fontWeight: 600,
          letterSpacing: '0.04em',
          transition: 'all 0.2s',
          background: mode === 'agentic' ? 'rgba(255, 214, 10, 0.15)' : 'transparent',
          color: mode === 'agentic' ? '#ffd60a' : '#7a7060',
          boxShadow: mode === 'agentic' ? '0 0 12px rgba(255, 214, 10, 0.12)' : 'none',
        }}
      >
        <Cpu size={12} />
        Agentic
      </button>
    </div>
  );
}

/* ─── Thinking Dots Animation ─── */
function ThinkingDots() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '24px 0' }}>
      <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1.1, 0.8] }}
            transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.2 }}
            style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              background: '#ffd60a',
            }}
          />
        ))}
      </div>
      <span
        style={{
          fontFamily: "'Rajdhani', sans-serif",
          fontSize: '14px',
          color: '#7a7060',
        }}
      >
        Thinking...
      </span>
    </div>
  );
}

export default function ChatOverlay({
  visible,
  onClose,
  agentGoal,
  setAgentGoal,
  agentLoading,
  agentStatus,
  agentError,
  onStartAgent,
}) {
  const [chatMode, setChatMode] = useState('ask'); // 'ask' or 'agentic'
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef(null);
  const inputRef = useRef(null);

  // Focus input when overlay becomes visible
  useEffect(() => {
    if (visible && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 350);
    }
  }, [visible]);

  // Voice input via Web Speech API
  const toggleVoiceInput = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    if (isRecording && recognitionRef.current) {
      recognitionRef.current.stop();
      setIsRecording(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
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
  }, [isRecording, setAgentGoal]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (recognitionRef.current) recognitionRef.current.abort();
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (agentGoal?.trim() && onStartAgent) {
      onStartAgent(e);
    }
  };

  const isAskMode = chatMode === 'ask';
  const isAgenticMode = chatMode === 'agentic';

  return (
    <AnimatePresence>
      {visible && (
        <>
          {/* Backdrop */}
          <motion.div
            className="chat-backdrop"
            variants={backdropVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            onClick={onClose}
            style={{
              position: 'fixed',
              inset: 0,
              backgroundColor: 'rgba(2, 6, 18, 0.78)',
              backdropFilter: 'blur(6px)',
              zIndex: 90,
            }}
          />

          {/* Center Panel */}
          <motion.div
            className="hud-panel hud-panel-bright"
            variants={overlayVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            style={{
              position: 'fixed',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              zIndex: 95,
              width: '100%',
              maxWidth: '672px',
              maxHeight: '85vh',
              overflowY: 'auto',
              padding: '28px 32px',
              borderRadius: '16px',
              border: '1px solid rgba(255, 214, 10, 0.18)',
              background:
                'linear-gradient(145deg, rgba(10, 18, 36, 0.96), rgba(6, 12, 28, 0.98))',
              boxShadow:
                '0 0 40px rgba(255, 214, 10, 0.08), inset 0 1px 0 rgba(255, 214, 10, 0.06)',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '16px',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                {isAskMode ? (
                  <MessageSquare size={18} color="#ffd60a" />
                ) : (
                  <Terminal size={18} color="#ffd60a" />
                )}
                <h2
                  style={{
                    fontFamily: "'Orbitron', sans-serif",
                    fontSize: '15px',
                    fontWeight: 700,
                    color: '#ffd60a',
                    letterSpacing: '0.18em',
                    margin: 0,
                    textTransform: 'uppercase',
                  }}
                >
                  {isAskMode ? 'Ask Anything' : 'Agentic Mode'}
                </h2>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                {/* Close */}
                <button
                  type="button"
                  onClick={onClose}
                  style={{
                    background: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    padding: '4px',
                    display: 'flex',
                    alignItems: 'center',
                  }}
                >
                  <X size={18} color="#7a7060" />
                </button>
              </div>
            </div>

            {/* Mode Toggle */}
            <div style={{ marginBottom: '16px' }}>
              <ModeToggle mode={chatMode} onChange={setChatMode} />
            </div>

            {/* Goal Input Form */}
            <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
              <div
                style={{
                  display: 'flex',
                  gap: '10px',
                  alignItems: 'stretch',
                }}
              >
                <div style={{ flex: 1, position: 'relative' }}>
                  <input
                    ref={inputRef}
                    type="text"
                    className="input-glow"
                    value={agentGoal || ''}
                    onChange={(e) => setAgentGoal(e.target.value)}
                    placeholder={isAskMode ? 'Ask me anything...' : 'Describe your mission objective...'}
                    disabled={agentLoading}
                    style={{
                      width: '100%',
                      padding: '12px 16px',
                      paddingRight: '42px',
                      borderRadius: '10px',
                      border: '1px solid rgba(255, 214, 10, 0.2)',
                      background: 'rgba(255, 214, 10, 0.04)',
                      color: '#e0d6c2',
                      fontFamily: "'Rajdhani', sans-serif",
                      fontSize: '15px',
                      fontWeight: 500,
                      outline: 'none',
                      boxSizing: 'border-box',
                      transition: 'border-color 0.2s',
                    }}
                  />

                  {/* Mic button inside input */}
                  <button
                    type="button"
                    onClick={toggleVoiceInput}
                    title={isRecording ? 'Stop recording' : 'Voice input'}
                    style={{
                      position: 'absolute',
                      right: '8px',
                      top: '50%',
                      transform: 'translateY(-50%)',
                      background: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      padding: '4px',
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    {isRecording ? (
                      <Mic size={16} color="#ff4757" style={{ animation: 'pulse-glow 1s ease infinite' }} />
                    ) : (
                      <MicOff size={16} color="#7a7060" />
                    )}
                  </button>
                </div>

                {/* Execute / Send button */}
                <button
                  type="submit"
                  disabled={agentLoading || !agentGoal?.trim()}
                  className={agentLoading ? 'btn-glow-pulse' : ''}
                  style={{
                    padding: isAskMode ? '12px 20px' : '12px 24px',
                    borderRadius: '10px',
                    border: 'none',
                    background: agentLoading
                      ? 'rgba(255, 214, 10, 0.3)'
                      : 'linear-gradient(135deg, #ffd60a, #ccab00)',
                    color: '#020612',
                    fontFamily: "'Orbitron', sans-serif",
                    fontSize: '12px',
                    fontWeight: 700,
                    letterSpacing: '0.14em',
                    cursor: agentLoading || !agentGoal?.trim() ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    textTransform: 'uppercase',
                    transition: 'all 0.2s',
                    opacity: !agentGoal?.trim() ? 0.4 : 1,
                    whiteSpace: 'nowrap',
                  }}
                >
                  {agentLoading ? (
                    <Loader2 size={15} style={{ animation: 'spin 1.2s linear infinite' }} />
                  ) : isAskMode ? (
                    <Send size={14} />
                  ) : (
                    <Play size={14} />
                  )}
                  {isAskMode ? 'Ask' : 'Execute'}
                </button>
              </div>
            </form>

            {/* Error Display */}
            {agentError && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '10px 14px',
                  borderRadius: '8px',
                  border: '1px solid rgba(255, 71, 87, 0.25)',
                  background: 'rgba(255, 71, 87, 0.08)',
                  marginBottom: '16px',
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: '12px',
                  color: '#ff6b7a',
                }}
              >
                <AlertTriangle size={14} color="#ff4757" />
                {agentError}
              </motion.div>
            )}

            {/* ═══ ASK ANYTHING MODE ═══ */}
            {isAskMode && agentStatus && (
              <div
                style={{
                  borderTop: '1px solid rgba(255, 214, 10, 0.1)',
                  paddingTop: '16px',
                }}
              >
                {/* Show thinking dots while running, no trace details */}
                {agentStatus.status === 'running' && !agentStatus.final_result && (
                  <ThinkingDots />
                )}

                {/* Final result — clean, no labels */}
                {agentStatus.final_result && (
                  <motion.div
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, ease: 'easeOut' }}
                    style={{
                      padding: '16px 18px',
                      borderRadius: '12px',
                      background: 'rgba(255, 214, 10, 0.03)',
                      border: '1px solid rgba(255, 214, 10, 0.1)',
                    }}
                  >
                    <pre
                      style={{
                        fontFamily: "'Rajdhani', sans-serif",
                        fontSize: '14px',
                        color: '#e0d6c2',
                        lineHeight: 1.7,
                        margin: 0,
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word',
                      }}
                    >
                      {agentStatus.final_result}
                    </pre>
                  </motion.div>
                )}
              </div>
            )}

            {/* ═══ AGENTIC MODE ═══ */}
            {isAgenticMode && agentStatus && (
              <div
                style={{
                  borderTop: '1px solid rgba(255, 214, 10, 0.1)',
                  paddingTop: '16px',
                }}
              >
                {/* Status badge row */}
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    marginBottom: '14px',
                  }}
                >
                  <span
                    style={{
                      fontFamily: "'Orbitron', sans-serif",
                      fontSize: '11px',
                      fontWeight: 600,
                      color: '#7a7060',
                      letterSpacing: '0.14em',
                      textTransform: 'uppercase',
                    }}
                  >
                    Execution Trace
                  </span>
                  <StatusBadge status={agentStatus.status} />
                </div>

                {/* Steps list */}
                {agentStatus.steps && agentStatus.steps.length > 0 && (
                  <div
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '6px',
                      marginBottom: '16px',
                      maxHeight: '220px',
                      overflowY: 'auto',
                      paddingRight: '4px',
                    }}
                  >
                    {agentStatus.steps.map((step, idx) => (
                      <motion.div
                        key={idx}
                        variants={stepVariants}
                        initial="initial"
                        animate="animate"
                        transition={{ delay: idx * 0.05 }}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '10px',
                          padding: '8px 12px',
                          borderRadius: '8px',
                          background: 'rgba(255, 214, 10, 0.03)',
                          border: '1px solid rgba(255, 214, 10, 0.06)',
                        }}
                      >
                        <span
                          style={{
                            fontFamily: "'JetBrains Mono', monospace",
                            fontSize: '10px',
                            color: '#3a4d62',
                            minWidth: '22px',
                          }}
                        >
                          {String(idx + 1).padStart(2, '0')}
                        </span>

                        {step.tool_used && (
                          <span
                            style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '4px',
                              padding: '2px 8px',
                              borderRadius: '6px',
                              background: 'rgba(255, 214, 10, 0.08)',
                              fontFamily: "'JetBrains Mono', monospace",
                              fontSize: '10px',
                              color: '#ffd60a',
                              whiteSpace: 'nowrap',
                            }}
                          >
                            {getToolEmoji(step.tool_used)} {step.tool_used}
                          </span>
                        )}

                        <span
                          style={{
                            fontFamily: "'Rajdhani', sans-serif",
                            fontSize: '13px',
                            color: '#e0d6c2',
                            flex: 1,
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                          }}
                        >
                          {step.step}
                        </span>
                      </motion.div>
                    ))}
                  </div>
                )}

                {/* Self-check */}
                {agentStatus.self_check && (
                  <div
                    style={{
                      padding: '8px 12px',
                      borderRadius: '8px',
                      background: 'rgba(0, 255, 136, 0.04)',
                      border: '1px solid rgba(0, 255, 136, 0.1)',
                      marginBottom: '12px',
                      fontFamily: "'JetBrains Mono', monospace",
                      fontSize: '11px',
                      color: '#00ff88',
                    }}
                  >
                    <CheckCircle2
                      size={12}
                      style={{ display: 'inline', marginRight: '6px', verticalAlign: 'middle' }}
                    />
                    {agentStatus.self_check}
                  </div>
                )}

                {/* Final result */}
                {agentStatus.final_result && (
                  <div
                    style={{
                      padding: '14px 16px',
                      borderRadius: '10px',
                      background: 'rgba(255, 214, 10, 0.04)',
                      border: '1px solid rgba(255, 214, 10, 0.12)',
                    }}
                  >
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        marginBottom: '8px',
                      }}
                    >
                      <span
                        style={{
                          fontFamily: "'Orbitron', sans-serif",
                          fontSize: '10px',
                          fontWeight: 600,
                          color: '#7a7060',
                          letterSpacing: '0.12em',
                          textTransform: 'uppercase',
                        }}
                      >
                        Output
                      </span>
                    </div>
                    <pre
                      style={{
                        fontFamily: "'JetBrains Mono', monospace",
                        fontSize: '12px',
                        color: '#e0d6c2',
                        lineHeight: 1.6,
                        margin: 0,
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word',
                      }}
                    >
                      {agentStatus.final_result}
                    </pre>
                  </div>
                )}
              </div>
            )}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
