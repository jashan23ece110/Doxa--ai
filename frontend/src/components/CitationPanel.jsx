import React from 'react';
import { ExternalLink, Globe, FileText } from 'lucide-react';

export default function CitationPanel({ text = '', steps = [] }) {
  const sources = [];
  const seenUrls = new Set();

  // 1. Extract markdown links [Title](http...) from text
  const linkRegex = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g;
  let match;
  while ((match = linkRegex.exec(text)) !== null) {
    const title = match[1].trim();
    const url = match[2].trim();
    if (!seenUrls.has(url)) {
      seenUrls.add(url);
      try {
        const domain = new URL(url).hostname.replace('www.', '');
        sources.push({ title: title || domain, url, domain, type: 'web' });
      } catch {
        sources.push({ title: title || url, url, domain: 'web', type: 'web' });
      }
    }
  }

  // 2. Extract plain URLs if not already caught
  const plainUrlRegex = /(https?:\/\/[^\s\)\>\]]+)/g;
  while ((match = plainUrlRegex.exec(text)) !== null) {
    const url = match[1].trim().replace(/[.,;]$/, '');
    if (!seenUrls.has(url)) {
      seenUrls.add(url);
      try {
        const domain = new URL(url).hostname.replace('www.', '');
        sources.push({ title: domain, url, domain, type: 'web' });
      } catch {
        sources.push({ title: url, url, domain: 'web', type: 'web' });
      }
    }
  }

  // 3. Extract document RAG sources from steps output
  (steps || []).forEach(s => {
    if (s.tool_used === 'search_documents' && s.output) {
      const docMatches = s.output.matchAll(/Document:\s*([^\n]+)/g);
      for (const dm of docMatches) {
        const docName = dm[1].trim();
        if (!seenUrls.has(docName)) {
          seenUrls.add(docName);
          sources.push({ title: docName, domain: 'Knowledge Base', type: 'doc' });
        }
      }
    }
  });

  if (sources.length === 0) return null;

  return (
    <div className="w-full mt-3 pt-2.5 border-t border-[var(--jarvis-accent)]/10 font-mono text-xs">
      <div className="text-[10px] text-[#7a7060] uppercase tracking-wider mb-2 font-bold flex items-center gap-1.5 select-none">
        <Globe className="w-3 h-3 text-[var(--jarvis-accent)]" />
        <span>Sources & Citations ({sources.length}):</span>
      </div>

      <div className="flex flex-wrap gap-2">
        {sources.map((src, idx) => (
          <a
            key={idx}
            href={src.url || '#'}
            target={src.url ? '_blank' : '_self'}
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-neutral-900/80 border border-[var(--jarvis-accent)]/15 text-[#e0d6c2] hover:text-[var(--jarvis-accent)] hover:border-[var(--jarvis-accent)]/40 hover:bg-neutral-850 transition-all duration-150 text-[10px] font-sans group shadow-sm"
          >
            {src.type === 'doc' ? (
              <FileText className="w-3 h-3 text-emerald-400 shrink-0" />
            ) : (
              <Globe className="w-3 h-3 text-[var(--jarvis-accent)] shrink-0" />
            )}

            <span className="font-medium truncate max-w-[140px]" title={src.title}>
              {src.title}
            </span>

            {src.url && (
              <ExternalLink className="w-2.5 h-2.5 text-neutral-500 group-hover:text-[var(--jarvis-accent)] transition-colors shrink-0" />
            )}
          </a>
        ))}
      </div>
    </div>
  );
}
