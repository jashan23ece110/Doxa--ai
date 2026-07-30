import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Sparkles, Volume2, VolumeX, Bot, ShieldCheck } from 'lucide-react';

export default function EmergentAnswerCard({ text, isThinking, steps, onClose, onSpeakToggle, isSpeaking }) {
  const [autoCollapseTimer, setAutoCollapseTimer] = useState(null);

  useEffect(() => {
    // Reset auto-collapse timer whenever new complete text arrives
    if (text && !isThinking) {
      const timer = setTimeout(() => {
        onClose?.();
      }, 9000); // 9 seconds auto-collapse
      return () => clearTimeout(timer);
    }
  }, [text, isThinking, onClose]);

  // Spring animation from origin particle point (center-scale + spring bounce)
  const emergenceVariants = {
    hidden: {
      opacity: 0,
      scale: 0,
      y: 60,
      filter: 'blur(16px)',
      boxShadow: '0 0 0px rgba(var(--jarvis-accent-rgb), 0)',
    },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      filter: 'blur(0px)',
      boxShadow: '0 0 35px rgba(var(--jarvis-accent-rgb), 0.25), 0 20px 40px rgba(0,0,0,0.8)',
      transition: {
        type: 'spring',
        stiffness: 260,
        damping: 22,
        mass: 0.8,
      },
    },
    exit: {
      opacity: 0,
      scale: 0.1,
      y: -40,
      filter: 'blur(20px)',
      transition: {
        duration: 0.35,
        ease: [0.4, 0, 0.2, 1],
      },
    },
  };

  if (!text && !isThinking && (!steps || steps.length === 0)) return null;

  return (
    <AnimatePresence>
      <motion.div
        key="emergent-card"
        variants={emergenceVariants}
        initial="hidden"
        animate="visible"
        exit="exit"
        className="fixed z-50 left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[90vw] max-w-xl p-0.5 rounded-2xl pointer-events-auto"
        style={{
          background: 'linear-gradient(135deg, rgba(var(--jarvis-accent-rgb), 0.4) 0%, rgba(var(--jarvis-accent-rgb), 0.05) 50%, rgba(var(--jarvis-accent-rgb), 0.3) 100%)',
        }}
      >
        <div
          className="w-full h-full rounded-[15px] p-5 sm:p-6 flex flex-col gap-4 relative overflow-hidden backdrop-blur-xl"
          style={{
            background: 'rgba(10, 10, 10, 0.88)',
            border: '1px solid rgba(var(--jarvis-accent-rgb), 0.25)',
          }}
        >
          {/* Emergence particle ray particle effect background */}
          <div className="absolute -top-24 -left-24 w-48 h-48 rounded-full bg-[radial-gradient(circle,rgba(var(--jarvis-accent-rgb),0.35)_0%,transparent_70%)] pointer-events-none animate-pulse" />

          {/* Header bar */}
          <div className="flex items-center justify-between border-b border-[rgba(var(--jarvis-accent-rgb),0.15)] pb-3 z-10">
            <div className="flex items-center gap-2.5">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[var(--jarvis-accent)] opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[var(--jarvis-accent)]" />
              </span>
              <span
                className="text-xs font-bold uppercase tracking-[0.2em] text-[var(--jarvis-accent)]"
                style={{ fontFamily: 'Orbitron, sans-serif' }}
              >
                {isThinking ? 'NEURAL SYNTHESIS...' : 'PARTICLE RESPONSE'}
              </span>
            </div>

            <div className="flex items-center gap-2">
              {onSpeakToggle && (
                <button
                  onClick={onSpeakToggle}
                  className="p-1.5 rounded-lg border border-[var(--jarvis-accent)]/20 text-neutral-400 hover:text-[var(--jarvis-accent)] hover:bg-[var(--jarvis-accent)]/10 transition-colors"
                  title={isSpeaking ? 'Mute Speech' : 'Read Aloud'}
                >
                  {isSpeaking ? <Volume2 className="w-4 h-4 text-[var(--jarvis-accent)] animate-pulse" /> : <VolumeX className="w-4 h-4" />}
                </button>
              )}
              <button
                onClick={onClose}
                className="p-1.5 rounded-lg border border-neutral-800 text-neutral-400 hover:text-white hover:bg-neutral-800 transition-colors cursor-pointer"
                title="Collapse into Core"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Thinking Step trace list */}
          {isThinking && steps && steps.length > 0 && (
            <div className="flex flex-col gap-1.5 my-1 z-10 max-h-32 overflow-y-auto hud-scrollbar">
              {steps.slice(-3).map((step, idx) => (
                <div key={idx} className="flex items-center gap-2 text-xs text-[#e0d6c2] font-mono bg-neutral-900/60 px-3 py-1.5 rounded-md border border-neutral-800">
                  <Sparkles className="w-3 h-3 text-[var(--jarvis-accent)] shrink-0 animate-spin" />
                  <span className="truncate">{step.step || step.tool_used}</span>
                </div>
              ))}
            </div>
          )}

          {/* Content display */}
          <div className="z-10 max-h-[50vh] overflow-y-auto hud-scrollbar pr-1">
            {text ? (
              <p
                className="text-sm sm:text-base leading-relaxed text-[#e0d6c2] font-medium whitespace-pre-wrap selection:bg-[var(--jarvis-accent)] selection:text-black"
                style={{ fontFamily: 'Rajdhani, sans-serif', letterSpacing: '0.02em' }}
              >
                {text}
              </p>
            ) : isThinking ? (
              <div className="flex items-center gap-3 py-3 text-neutral-400 text-xs font-mono">
                <Bot className="w-4 h-4 text-[var(--jarvis-accent)] animate-bounce" />
                <span>Formulating response from core particles...</span>
              </div>
            ) : null}
          </div>

          {/* Footer bar */}
          <div className="flex items-center justify-between text-[10px] text-neutral-500 font-mono pt-2 border-t border-[rgba(var(--jarvis-accent-rgb),0.1)] z-10">
            <span className="flex items-center gap-1">
              <ShieldCheck className="w-3 h-3 text-[var(--jarvis-accent)]" /> DOXA SPHERE ENGINE
            </span>
            <span>AUTO-COLLAPSE IN 9S</span>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
