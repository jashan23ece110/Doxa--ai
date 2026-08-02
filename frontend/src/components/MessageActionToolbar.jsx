import React, { useState } from 'react';
import { Copy, Check, ThumbsUp, ThumbsDown, RotateCcw, GitBranch } from 'lucide-react';

export default function MessageActionToolbar({ msgText = '', onRegenerate, onBranch, showToast }) {
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState(null); // 'up' | 'down' | null

  const handleCopy = () => {
    navigator.clipboard.writeText(msgText);
    setCopied(true);
    showToast?.('Copied message to clipboard', 'info');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleFeedback = (type) => {
    const nextVal = feedback === type ? null : type;
    setFeedback(nextVal);
    if (nextVal) {
      showToast?.(type === 'up' ? 'Feedback recorded! (Helpful)' : 'Feedback recorded! (Needs improvement)', 'success');
    }
  };

  return (
    <div className="flex items-center gap-3 mt-2.5 pt-2 border-t border-[var(--jarvis-accent)]/10 text-neutral-400 font-mono text-[10px] select-none">
      {/* Copy Button */}
      <button
        type="button"
        onClick={handleCopy}
        className="flex items-center gap-1 hover:text-white transition-colors cursor-pointer"
        title="Copy response"
      >
        {copied ? (
          <>
            <Check className="w-3 h-3 text-emerald-400" />
            <span className="text-emerald-400 font-bold">COPIED</span>
          </>
        ) : (
          <>
            <Copy className="w-3 h-3" />
            <span>COPY</span>
          </>
        )}
      </button>

      {/* Thumbs Up */}
      <button
        type="button"
        onClick={() => handleFeedback('up')}
        className={`hover:text-emerald-400 transition-colors cursor-pointer ${feedback === 'up' ? 'text-emerald-400 font-bold' : ''}`}
        title="Helpful response"
      >
        <ThumbsUp className="w-3 h-3" />
      </button>

      {/* Thumbs Down */}
      <button
        type="button"
        onClick={() => handleFeedback('down')}
        className={`hover:text-red-400 transition-colors cursor-pointer ${feedback === 'down' ? 'text-red-400 font-bold' : ''}`}
        title="Needs improvement"
      >
        <ThumbsDown className="w-3 h-3" />
      </button>

      {/* Regenerate Button */}
      {onRegenerate && (
        <button
          type="button"
          onClick={onRegenerate}
          className="flex items-center gap-1 hover:text-amber-400 transition-colors cursor-pointer ml-auto sm:ml-0"
          title="Regenerate response"
        >
          <RotateCcw className="w-3 h-3" />
          <span>REGENERATE</span>
        </button>
      )}

      {/* Branch Button */}
      {onBranch && (
        <button
          type="button"
          onClick={onBranch}
          className="flex items-center gap-1 hover:text-[var(--jarvis-accent)] transition-colors cursor-pointer ml-auto"
          title="Branch conversation timeline from here"
        >
          <GitBranch className="w-3 h-3" />
          <span>BRANCH</span>
        </button>
      )}
    </div>
  );
}
