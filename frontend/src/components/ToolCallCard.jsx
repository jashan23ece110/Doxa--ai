import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Globe, 
  Calculator, 
  Calendar, 
  Terminal, 
  FileText, 
  Cpu, 
  ChevronDown, 
  ChevronUp, 
  Check, 
  Loader2 
} from 'lucide-react';

function getToolIcon(toolName) {
  const name = (toolName || '').toLowerCase();
  if (name.includes('search') || name.includes('brave')) return Globe;
  if (name.includes('calc') || name.includes('math')) return Calculator;
  if (name.includes('calendar') || name.includes('event')) return Calendar;
  if (name.includes('python') || name.includes('code')) return Terminal;
  if (name.includes('doc') || name.includes('rag')) return FileText;
  return Cpu;
}

export default function ToolCallCard({ step }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!step || !step.tool_used || step.tool_used === 'None') return null;

  const Icon = getToolIcon(step.tool_used);
  const isRunning = step.output === 'Running...';
  const hasOutput = step.output && step.output !== 'Running...';

  // Format arguments object
  const formattedArgs = typeof step.input === 'object' 
    ? JSON.stringify(step.input, null, 2) 
    : String(step.input || '');

  return (
    <div className="w-full my-2 border border-[var(--jarvis-accent)]/15 rounded-xl overflow-hidden bg-neutral-950/70 backdrop-blur-md shadow-md text-xs font-mono transition-all duration-200">
      {/* Header Bar */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        className="px-3.5 py-2 flex items-center justify-between cursor-pointer select-none bg-neutral-900/60 hover:bg-neutral-900/90 transition-colors border-b border-[var(--jarvis-accent)]/5"
      >
        <div className="flex items-center gap-2 min-w-0">
          <div className={`p-1.5 rounded-lg border ${
            isRunning 
              ? 'bg-amber-500/10 border-amber-500/30 text-amber-400 animate-pulse' 
              : 'bg-[var(--jarvis-accent)]/10 border-[var(--jarvis-accent)]/20 text-[var(--jarvis-accent)]'
          }`}>
            <Icon className="w-3.5 h-3.5" />
          </div>

          <div className="flex items-center gap-2 truncate">
            <span className="font-semibold text-white tracking-wider">
              {step.tool_used}
            </span>
            <span className="text-[10px] text-neutral-500 hidden sm:inline">
              ({step.step || 'Executing tool'})
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          {isRunning ? (
            <span className="flex items-center gap-1 text-[10px] text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
              <Loader2 className="w-3 h-3 animate-spin" />
              RUNNING
            </span>
          ) : (
            <span className="flex items-center gap-1 text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              <Check className="w-3 h-3" />
              DONE
            </span>
          )}

          <button type="button" className="text-neutral-500 hover:text-white transition-colors">
            {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Expandable Parameters & Output View */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="p-3 bg-neutral-950/80 border-t border-[var(--jarvis-accent)]/5 flex flex-col gap-2.5 text-[11px]"
          >
            {/* Input Arguments */}
            {step.input && (
              <div>
                <div className="text-[9px] text-[#7a7060] uppercase tracking-wider mb-1 font-bold">
                  Input Arguments:
                </div>
                <pre className="p-2 rounded-lg bg-black/60 border border-neutral-800 text-cyan-300/90 overflow-x-auto whitespace-pre-wrap leading-relaxed font-mono">
                  {formattedArgs}
                </pre>
              </div>
            )}

            {/* Output Result */}
            {hasOutput && (
              <div>
                <div className="text-[9px] text-[#7a7060] uppercase tracking-wider mb-1 font-bold">
                  Execution Output:
                </div>
                <pre className="p-2 rounded-lg bg-black/80 border border-emerald-500/20 text-emerald-300/90 max-h-40 overflow-y-auto hud-scrollbar whitespace-pre-wrap leading-relaxed font-mono">
                  {step.output}
                </pre>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
