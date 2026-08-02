import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, ChevronDown, ChevronUp, Cpu } from 'lucide-react';
import ToolCallCard from './ToolCallCard';

export default function ReasoningViewCard({ steps = [], selfCheck = null }) {
  const [isOpen, setIsOpen] = useState(false); // Default collapsed as per spec

  const validSteps = (steps || []).filter(s => s && s.step);
  if (validSteps.length === 0 && !selfCheck) return null;

  return (
    <div className="w-full my-2.5 border border-[var(--jarvis-accent)]/15 rounded-xl overflow-hidden bg-neutral-950/40 backdrop-blur-md font-mono text-xs transition-all duration-300">
      {/* Collapsible Header (Default Collapsed) */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-3.5 py-2 flex items-center justify-between bg-neutral-900/40 hover:bg-neutral-900/80 transition-colors border-b border-[var(--jarvis-accent)]/5 text-left select-none"
      >
        <div className="flex items-center gap-2">
          <Sparkles className="w-3.5 h-3.5 text-[var(--jarvis-accent)]" />
          <span className="text-neutral-400 font-semibold tracking-wider text-[11px]">
            Thought Process
          </span>
          <span className="px-1.5 py-0.5 rounded bg-neutral-800 text-[10px] text-neutral-400 border border-neutral-700">
            {validSteps.length} steps
          </span>
        </div>

        <div className="flex items-center gap-2 text-neutral-500 text-[10px]">
          <span>{isOpen ? 'Hide reasoning' : 'Show reasoning'}</span>
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </button>

      {/* Reasoning Steps & Tool Traces (Collapsible) */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="p-3 bg-black/60 flex flex-col gap-2 border-t border-[var(--jarvis-accent)]/5"
          >
            {validSteps.map((step, idx) => (
              <div key={idx} className="flex flex-col gap-1">
                <div className="flex items-center gap-2 text-[10px] text-neutral-400">
                  <span className="text-[var(--jarvis-accent)] font-bold">[{idx + 1}]</span>
                  <span className="text-white font-medium">{step.step}</span>
                </div>

                {/* Render Tool Call Card if tool was invoked */}
                {step.tool_used && step.tool_used !== 'None' && (
                  <div className="pl-4">
                    <ToolCallCard step={step} />
                  </div>
                )}
              </div>
            ))}

            {/* Evaluation Self-Check Critique */}
            {selfCheck && (
              <div className="mt-2 p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 text-[10px] flex flex-col gap-1">
                <span className="font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1">
                  <Cpu className="w-3 h-3" /> Evaluator Self-Check:
                </span>
                <p className="font-sans leading-relaxed text-amber-200/90">{selfCheck}</p>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
