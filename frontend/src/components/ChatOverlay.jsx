import React, { useState, useRef, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  X,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Play,
  Loader2,
  CheckCircle2,
  AlertTriangle,
  Terminal,
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
    running: { icon: Loader2, color: '#00d9ff', label: 'RUNNING', spin: true },
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
  const [isRecording, setIsRecording] = useState(false);
  const [speakEnabled, setSpeakEnabled] = useState(false);
  const recognitionRef = useRef(null);
  const synthRef = useRef(window.speechSynthesis);
  const spokenResultRef = useRef('');
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

  // Voice output — speak final_result
  useEffect(() => {
    if (
      speakEnabled &&
      agentStatus?.final_result &&
      agentStatus.final_result !== spokenResultRef.current
    ) {
      spokenResultRef.current = agentStatus.final_result;
      const utterance = new SpeechSynthesisUtterance(agentStatus.final_result);
      utterance.rate = 1;
      utterance.pitch = 1;
      synthRef.current.speak(utterance);
    }
  }, [speakEnabled, agentStatus?.final_result]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (recognitionRef.current) recognitionRef.current.abort();
      synthRef.current.cancel();
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (agentGoal?.trim() && onStartAgent) {
      onStartAgent(e);
    }
  };

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
              border: '1px solid rgba(0, 217, 255, 0.18)',
              background:
                'linear-gradient(145deg, rgba(10, 18, 36, 0.96), rgba(6, 12, 28, 0.98))',
              boxShadow:
                '0 0 40px rgba(0, 217, 255, 0.08), inset 0 1px 0 rgba(0, 217, 255, 0.06)',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '20px',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Terminal size={18} color="#00d9ff" />
                <h2
                  style={{
                    fontFamily: "'Orbitron', sans-serif",
                    fontSize: '15px',
                    fontWeight: 700,
                    color: '#00d9ff',
                    letterSpacing: '0.18em',
                    margin: 0,
                    textTransform: 'uppercase',
                  }}
                >
                  Doxa Agent
                </h2>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                {/* TTS toggle */}
                <button
                  type="button"
                  onClick={() => {
                    setSpeakEnabled((v) => !v);
                    if (speakEnabled) synthRef.current.cancel();
                  }}
                  title={speakEnabled ? 'Disable voice output' : 'Enable voice output'}
                  style={{
                    background: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    padding: '4px',
                    display: 'flex',
                    alignItems: 'center',
                  }}
                >
                  {speakEnabled ? (
                    <Volume2 size={16} color="#00d9ff" />
                  ) : (
                    <VolumeX size={16} color="#5a6d82" />
                  )}
                </button>

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
                  <X size={18} color="#5a6d82" />
                </button>
              </div>
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
                    placeholder="Describe your mission objective..."
                    disabled={agentLoading}
                    style={{
                      width: '100%',
                      padding: '12px 16px',
                      paddingRight: '42px',
                      borderRadius: '10px',
                      border: '1px solid rgba(0, 217, 255, 0.2)',
                      background: 'rgba(0, 217, 255, 0.04)',
                      color: '#c8d6e5',
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
                      <MicOff size={16} color="#5a6d82" />
                    )}
                  </button>
                </div>

                {/* Execute button */}
                <button
                  type="submit"
                  disabled={agentLoading || !agentGoal?.trim()}
                  className={agentLoading ? 'btn-glow-pulse' : ''}
                  style={{
                    padding: '12px 24px',
                    borderRadius: '10px',
                    border: 'none',
                    background: agentLoading
                      ? 'rgba(0, 217, 255, 0.3)'
                      : 'linear-gradient(135deg, #00d9ff, #0099cc)',
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
                  ) : (
                    <Play size={14} />
                  )}
                  Execute
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

            {/* Execution Trace */}
            {agentStatus && (
              <div
                style={{
                  borderTop: '1px solid rgba(0, 217, 255, 0.1)',
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
                      color: '#5a6d82',
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
                          background: 'rgba(0, 217, 255, 0.03)',
                          border: '1px solid rgba(0, 217, 255, 0.06)',
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
                              background: 'rgba(0, 217, 255, 0.08)',
                              fontFamily: "'JetBrains Mono', monospace",
                              fontSize: '10px',
                              color: '#00d9ff',
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
                            color: '#c8d6e5',
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
                      background: 'rgba(0, 217, 255, 0.04)',
                      border: '1px solid rgba(0, 217, 255, 0.12)',
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
                          color: '#5a6d82',
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
                        color: '#c8d6e5',
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
