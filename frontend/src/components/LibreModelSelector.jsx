import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Bot, MessageSquare, ChevronDown, Check, Sparkles } from 'lucide-react';

const MODES = [
  {
    id: 'ask',
    label: 'Fast Direct',
    sub: 'Moonshot Kimi-K3 Free Model',
    icon: Zap,
    color: 'text-amber-400',
    badge: 'FAST'
  },
  {
    id: 'agent',
    label: 'Agentic Plan & Execute',
    sub: 'Full Multi-Step RAG & Tools',
    icon: Bot,
    color: 'text-[var(--jarvis-accent)]',
    badge: 'REASONING'
  },
  {
    id: 'debate',
    label: 'Parallel Debate',
    sub: 'Dual Optimist vs Skeptic Engine',
    icon: MessageSquare,
    color: 'text-emerald-400',
    badge: 'DEBATE'
  }
];

export default function LibreModelSelector({ chatMode = 'ask', setChatMode }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const currentMode = MODES.find(m => m.id === chatMode) || MODES[0];
  const CurrentIcon = currentMode.icon;

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div ref={dropdownRef} className="relative inline-block text-xs font-mono z-30 select-none">
      {/* Selector Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-neutral-900/80 border border-[var(--jarvis-accent)]/20 text-[#e0d6c2] hover:text-white hover:border-[var(--jarvis-accent)]/40 hover:bg-neutral-850 transition-all shadow-md cursor-pointer"
      >
        <CurrentIcon className={`w-3.5 h-3.5 ${currentMode.color}`} />
        <span className="font-semibold font-sans">{currentMode.label}</span>
        <span className="px-1.5 py-0.5 rounded bg-[var(--jarvis-accent)]/10 text-[9px] text-[var(--jarvis-accent)] border border-[var(--jarvis-accent)]/20 font-mono">
          {currentMode.badge}
        </span>
        <ChevronDown className={`w-3.5 h-3.5 text-neutral-400 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Dropdown Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.96 }}
            transition={{ duration: 0.15 }}
            className="absolute left-0 mt-1.5 w-64 max-h-[320px] overflow-y-auto hud-scrollbar p-1.5 rounded-2xl bg-neutral-950/95 backdrop-blur-2xl border border-[var(--jarvis-accent)]/25 shadow-[0_15px_35px_rgba(0,0,0,0.8)] flex flex-col gap-1 z-50"
          >
            <div className="px-2 py-1 text-[9px] font-bold uppercase tracking-wider text-[#7a7060] border-b border-neutral-800 mb-1">
              Select Processing Engine
            </div>

            {MODES.map((mode) => {
              const Icon = mode.icon;
              const isSelected = mode.id === chatMode;

              return (
                <button
                  key={mode.id}
                  type="button"
                  onClick={() => {
                    setChatMode(mode.id);
                    setIsOpen(false);
                  }}
                  className={`flex items-start gap-2.5 p-2 rounded-xl text-left transition-all ${
                    isSelected
                      ? 'bg-[var(--jarvis-accent)]/15 border border-[var(--jarvis-accent)]/30 text-white'
                      : 'hover:bg-neutral-900 text-neutral-300 border border-transparent'
                  }`}
                >
                  <div className={`p-1.5 rounded-lg bg-neutral-900 border border-neutral-800 shrink-0 ${mode.color}`}>
                    <Icon className="w-4 h-4" />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold font-sans text-xs text-white">
                        {mode.label}
                      </span>
                      {isSelected && <Check className="w-3.5 h-3.5 text-[var(--jarvis-accent)]" />}
                    </div>
                    <p className="text-[10px] text-neutral-400 font-sans truncate mt-0.5">
                      {mode.sub}
                    </p>
                  </div>
                </button>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
