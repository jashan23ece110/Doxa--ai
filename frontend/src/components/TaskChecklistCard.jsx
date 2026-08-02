import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, Circle, Loader2, ListTodo, ChevronDown, ChevronUp } from 'lucide-react';

export default function TaskChecklistCard({ plan = [], steps = [], isCompleted = false }) {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!plan || plan.length === 0) return null;

  // Calculate current active step index based on executed tool steps
  const executedCount = steps.filter(s => s.tool_used && s.tool_used !== 'None').length;
  const currentStepIdx = isCompleted ? plan.length : Math.min(executedCount, plan.length - 1);
  const completedCount = isCompleted ? plan.length : currentStepIdx;
  const progressPercent = Math.round((completedCount / plan.length) * 100);

  return (
    <div className="w-full my-3 backdrop-blur-xl bg-neutral-950/60 border border-[var(--jarvis-accent)]/20 rounded-xl overflow-hidden shadow-[0_10px_25px_rgba(0,0,0,0.5)] font-mono text-xs transition-all duration-300">
      {/* Header Bar */}
      <div 
        onClick={() => setIsExpanded(!isExpanded)}
        className="px-3.5 py-2.5 bg-neutral-900/80 border-b border-[var(--jarvis-accent)]/10 flex items-center justify-between cursor-pointer select-none hover:bg-neutral-900 transition-colors"
      >
        <div className="flex items-center gap-2">
          <ListTodo className="w-4 h-4 text-[var(--jarvis-accent)] animate-pulse" />
          <span className="font-semibold tracking-wider uppercase text-[#e0d6c2]">
            Execution Plan
          </span>
          <span className="px-2 py-0.5 rounded-full bg-[var(--jarvis-accent)]/10 text-[var(--jarvis-accent)] text-[10px] font-bold border border-[var(--jarvis-accent)]/20">
            {completedCount}/{plan.length} DONE
          </span>
        </div>

        <div className="flex items-center gap-3">
          {/* Miniature Progress Bar */}
          <div className="w-24 h-1.5 bg-neutral-800 rounded-full overflow-hidden hidden sm:block border border-neutral-700/50">
            <div 
              className="h-full bg-[var(--jarvis-accent)] transition-all duration-500"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <button type="button" className="text-[#7a7060] hover:text-[#e0d6c2] transition-colors">
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Task Items List */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="p-3 flex flex-col gap-2 bg-neutral-950/40"
          >
            {plan.map((taskText, idx) => {
              const itemDone = isCompleted || idx < currentStepIdx;
              const itemActive = !isCompleted && idx === currentStepIdx;

              return (
                <div 
                  key={idx}
                  className={`flex items-center gap-2.5 p-2 rounded-lg border transition-all duration-200 ${
                    itemDone
                      ? 'bg-emerald-950/20 border-emerald-500/20 text-neutral-400'
                      : itemActive
                        ? 'bg-[var(--jarvis-accent)]/10 border-[var(--jarvis-accent)]/30 text-[var(--jarvis-accent)] shadow-[0_0_12px_rgba(var(--jarvis-accent-rgb),0.1)]'
                        : 'bg-neutral-900/40 border-neutral-800/60 text-neutral-500'
                  }`}
                >
                  {/* Status Icon */}
                  {itemDone ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  ) : itemActive ? (
                    <Loader2 className="w-4 h-4 text-[var(--jarvis-accent)] animate-spin shrink-0" />
                  ) : (
                    <Circle className="w-4 h-4 text-neutral-600 shrink-0" />
                  )}

                  {/* Task Text */}
                  <span className={`text-[11px] font-sans leading-tight ${itemDone ? 'line-through opacity-75' : itemActive ? 'font-medium text-white' : ''}`}>
                    {taskText}
                  </span>
                </div>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
