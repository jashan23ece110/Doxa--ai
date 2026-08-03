import React from 'react';
import { Bot, Globe, ExternalLink, Code2 } from 'lucide-react';

export default function Footer({ onLaunchApp }) {
  return (
    <footer className="py-12 px-4 sm:px-6 lg:px-8 bg-black border-t border-white/10 text-neutral-400 font-mono text-xs z-10 relative">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-violet-600/20 border border-violet-500/30 flex items-center justify-center text-violet-400">
            <Bot className="w-4 h-4" />
          </div>
          <span className="font-bold text-white tracking-widest uppercase font-orbitron text-sm" style={{ fontFamily: 'Orbitron, sans-serif' }}>
            DOXA AI
          </span>
          <span className="text-[10px] text-neutral-500">© 2026 DOXA AI Platform Inc.</span>
        </div>

        <div className="flex items-center gap-6 text-xs text-neutral-300 font-sans">
          <button type="button" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} className="hover:text-white transition-colors cursor-pointer">
            Overview
          </button>
          <button type="button" onClick={onLaunchApp} className="hover:text-violet-400 transition-colors cursor-pointer font-semibold">
            Try Doxa
          </button>
          <a href="https://doxas.app" target="_blank" rel="noreferrer" className="hover:text-white transition-colors flex items-center gap-1">
            <Globe className="w-3.5 h-3.5 text-cyan-400" /> doxas.app <ExternalLink className="w-2.5 h-2.5" />
          </a>
        </div>
      </div>
    </footer>
  );
}
