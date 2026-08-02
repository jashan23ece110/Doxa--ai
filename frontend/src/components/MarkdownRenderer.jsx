import React, { useState } from 'react';
import { Copy, Check, Code2 } from 'lucide-react';

export default function MarkdownRenderer({ content = '' }) {
  const [copiedIdx, setCopiedIdx] = useState(null);

  if (!content) return null;

  const handleCopyCode = (codeText, index) => {
    navigator.clipboard.writeText(codeText);
    setCopiedIdx(index);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  // Split content by triple backticks to identify code blocks
  const parts = content.split(/```/);

  return (
    <div className="flex flex-col gap-2 leading-relaxed text-sm select-text font-sans">
      {parts.map((part, index) => {
        // Odd indices are code blocks
        if (index % 2 === 1) {
          const lines = part.split('\n');
          const firstLine = lines[0].trim();
          const hasLang = /^[a-zA-Z0-9_\-+]+$/.test(firstLine);
          const langName = hasLang ? firstLine : 'code';
          const codeLines = hasLang ? lines.slice(1) : lines;
          const codeText = codeLines.join('\n').replace(/^\n+|\n+$/g, '');
          
          return (
            <div key={index} className="my-2.5 border border-neutral-800 rounded-xl overflow-hidden shadow-xl bg-neutral-950/95 font-mono text-[12px]">
              {/* Code Block Header */}
              <div className="bg-neutral-900/90 border-b border-neutral-800 px-4 py-2 text-[10px] text-neutral-400 font-bold uppercase tracking-wider flex justify-between items-center select-none font-mono">
                <div className="flex items-center gap-1.5 text-[var(--jarvis-accent)]">
                  <Code2 className="w-3.5 h-3.5" />
                  <span>{langName}</span>
                </div>
                <button 
                  onClick={() => handleCopyCode(codeText, index)}
                  className="flex items-center gap-1 hover:text-white text-neutral-400 transition-colors cursor-pointer px-2 py-0.5 rounded bg-neutral-800/60 border border-neutral-700/50"
                  title="Copy code to clipboard"
                >
                  {copiedIdx === index ? (
                    <>
                      <Check className="w-3 h-3 text-emerald-400" />
                      <span className="text-emerald-400 text-[9px]">COPIED</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3 h-3" />
                      <span className="text-[9px]">COPY</span>
                    </>
                  )}
                </button>
              </div>

              {/* Code Block Body */}
              <pre className="p-4 overflow-x-auto hud-scrollbar max-h-96 text-cyan-200/90 leading-relaxed font-mono">
                <code>{codeText}</code>
              </pre>
            </div>
          );
        }

        // Even indices are regular markdown text
        return (
          <div key={index} className="markdown-inline flex flex-col gap-2 text-[#e0d6c2]">
            {part.split('\n').map((line, lIdx) => {
              const trimmed = line.trim();
              if (!trimmed) return <div key={lIdx} className="h-1" />;

              // Headers
              if (trimmed.startsWith('### ')) {
                return (
                  <h3 key={lIdx} className="text-sm font-bold text-white uppercase tracking-wider mt-3 mb-1 font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                    {parseInline(trimmed.substring(4))}
                  </h3>
                );
              }
              if (trimmed.startsWith('## ')) {
                return (
                  <h2 key={lIdx} className="text-base font-bold text-[var(--jarvis-accent)] uppercase tracking-wider mt-3.5 mb-1 font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                    {parseInline(trimmed.substring(3))}
                  </h2>
                );
              }
              if (trimmed.startsWith('# ')) {
                return (
                  <h1 key={lIdx} className="text-lg font-bold text-white uppercase tracking-widest mt-4 mb-2 font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                    {parseInline(trimmed.substring(2))}
                  </h1>
                );
              }

              // Blockquotes
              if (trimmed.startsWith('> ')) {
                return (
                  <blockquote key={lIdx} className="pl-3.5 py-1.5 my-1.5 border-l-2 border-[var(--jarvis-accent)]/50 bg-[var(--jarvis-accent)]/5 rounded-r-lg text-neutral-300 italic text-xs">
                    {parseInline(trimmed.substring(2))}
                  </blockquote>
                );
              }

              // Bullet lists
              if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
                return (
                  <div key={lIdx} className="flex items-start gap-2 ml-2 my-0.5 text-neutral-200">
                    <span className="text-[var(--jarvis-accent)] select-none shrink-0 mt-1.5 text-xs">•</span>
                    <span className="flex-1 leading-relaxed">{parseInline(trimmed.substring(2))}</span>
                  </div>
                );
              }

              // Numbered lists (e.g. 1. , 2. )
              if (/^\d+\.\s/.test(trimmed)) {
                const match = trimmed.match(/^(\d+)\.\s(.*)/);
                if (match) {
                  return (
                    <div key={lIdx} className="flex items-start gap-2 ml-2 my-0.5 text-neutral-200">
                      <span className="text-[var(--jarvis-accent)] font-mono font-bold select-none shrink-0 text-xs">{match[1]}.</span>
                      <span className="flex-1 leading-relaxed">{parseInline(match[2])}</span>
                    </div>
                  );
                }
              }

              // Normal paragraph line
              return (
                <p key={lIdx} className="my-0.5 leading-relaxed">
                  {parseInline(line)}
                </p>
              );
            })}
          </div>
        );
      })}
    </div>
  );
}

// Simple inline parser for bold and inline code
function parseInline(text) {
  const tokens = text.split(/(\*\*.*?\*\*|`.*?`)/g);
  
  return tokens.map((token, index) => {
    if (token.startsWith('**') && token.endsWith('**')) {
      return (
        <strong key={index} className="font-bold text-white tracking-wide">
          {token.slice(2, -2)}
        </strong>
      );
    }
    if (token.startsWith('`') && token.endsWith('`')) {
      return (
        <code key={index} className="px-1.5 py-0.5 bg-neutral-900 border border-[var(--jarvis-accent)]/20 text-[var(--jarvis-accent)] rounded font-mono text-xs mx-0.5">
          {token.slice(1, -1)}
        </code>
      );
    }
    return token;
  });
}
