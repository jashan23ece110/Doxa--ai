import React from 'react';
import SvgLogo from './logo/SvgLogo';

export default function Footer({ onLaunchApp }) {
  const scrollToSection = (id) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <footer className="w-full bg-black border-t border-white/[0.06] py-12 px-4 sm:px-6 lg:px-8 z-10 relative">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-8 select-none">
        
        {/* Left Side: Logo mark + Wordmark */}
        <div 
          className="flex items-center gap-2.5 cursor-pointer"
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          title="Scroll to Top"
        >
          {/* Plain icon — SVG component */}
          <SvgLogo size={32} className="w-8 h-8" />
          <span className="text-lg font-semibold tracking-tight text-white">
            Doxa
          </span>
        </div>

        {/* Center/Right: Simple Navigation/Reference Links */}
        <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-4 text-[13px] font-medium text-neutral-400 font-sans">
          <button 
            type="button" 
            onClick={() => scrollToSection('features')} 
            className="hover:text-white transition-colors duration-200 cursor-pointer"
          >
            Features
          </button>
          <button 
            type="button" 
            onClick={() => scrollToSection('how-it-works')} 
            className="hover:text-white transition-colors duration-200 cursor-pointer"
          >
            How It Works
          </button>
          <button 
            type="button" 
            onClick={onLaunchApp} 
            className="hover:text-violet-400 font-semibold transition-colors duration-200 cursor-pointer"
          >
            Try Doxa
          </button>
          <span className="text-neutral-800 hidden sm:inline">|</span>
          <span className="hover:text-neutral-300 transition-colors duration-200 cursor-default">
            Privacy
          </span>
          <span className="hover:text-neutral-300 transition-colors duration-200 cursor-default">
            Terms
          </span>
        </div>

        {/* Right/Bottom Copyright Line */}
        <div className="text-[10px] text-neutral-600 font-mono tracking-wider uppercase">
          © 2026 Doxa. All rights reserved.
        </div>

      </div>
    </footer>
  );
}
