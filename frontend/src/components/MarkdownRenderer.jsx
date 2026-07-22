import React from 'react';

export default function MarkdownRenderer({ content = '' }) {
  if (!content) return null;

  // Split content by triple backticks to identify code blocks
  const parts = content.split(/```/);

  return (
    <div className="flex flex-col gap-1.5 leading-relaxed text-sm select-text">
      {parts.map((part, index) => {
        // Odd indices are code blocks
        if (index % 2 === 1) {
          const lines = part.split('\n');
          // Check if first line specifies language
          const firstLine = lines[0].trim();
          const hasLang = /^[a-zA-Z0-9_\-+]+$/.test(firstLine);
          const codeLines = hasLang ? lines.slice(1) : lines;
          const codeText = codeLines.join('\n').replace(/^\n+|\n+$/g, '');
          
          return (
            <div key={index} className="my-2 border border-[#dc143c]/15 rounded-xl overflow-hidden shadow-inner bg-neutral-950/90 font-mono text-[12px]">
              {hasLang && (
                <div className="bg-neutral-900 border-b border-[#dc143c]/10 px-4 py-1.5 text-[10px] text-neutral-400 font-bold uppercase tracking-wider flex justify-between items-center" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                  <span>{firstLine}</span>
                  <button 
                    onClick={() => navigator.clipboard.writeText(codeText)}
                    className="hover:text-white transition-colors cursor-pointer"
                  >
                    COPY
                  </button>
                </div>
              )}
              <pre className="p-4 overflow-x-auto hud-scrollbar max-h-96 text-[#ff4500]">
                <code>{codeText}</code>
              </pre>
            </div>
          );
        }

        // Even indices are regular markdown text
        return (
          <div key={index} className="markdown-inline flex flex-col gap-1 text-[#e0d6c2]">
            {part.split('\n').map((line, lIdx) => {
              const trimmed = line.trim();
              if (!trimmed) return <div key={lIdx} className="h-2" />;

              // Headers
              if (trimmed.startsWith('### ')) {
                return (
                  <h3 key={lIdx} className="text-sm font-bold text-neutral-100 uppercase tracking-wide mt-3 mb-1 font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                    {parseInline(trimmed.substring(4))}
                  </h3>
                );
              }
              if (trimmed.startsWith('## ')) {
                return (
                  <h2 key={lIdx} className="text-md font-bold text-[#dc143c] uppercase tracking-wider mt-4 mb-1 font-orbitron" style={{ fontFamily: 'Orbitron, sans-serif' }}>
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

              // Bullet lists
              if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
                return (
                  <ul key={lIdx} className="list-disc list-inside ml-2.5 my-0.5 text-neutral-300">
                    <li className="list-item">{parseInline(trimmed.substring(2))}</li>
                  </ul>
                );
              }

              // Normal paragraph line
              return (
                <p key={lIdx} className="my-0.5">
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
  // Regex splitting on **bold** and `code`
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
        <code key={index} className="px-1.5 py-0.5 bg-neutral-900 border border-[#dc143c]/15 text-[#ff4500] rounded font-mono text-xs mx-0.5">
          {token.slice(1, -1)}
        </code>
      );
    }
    return token;
  });
}
