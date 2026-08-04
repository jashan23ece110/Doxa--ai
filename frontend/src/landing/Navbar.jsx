import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, ChevronDown, Bot, ArrowRight, Cpu, Database, Globe, Mic, GitBranch, ShieldCheck } from 'lucide-react';
import doxaLogo from '../assets/logo.png';

const CAPABILITIES = [
  { label: 'Autonomous Reasoning', desc: 'Multi-step planning & tool execution', icon: Cpu },
  { label: 'RAG Knowledge Base', desc: 'Vector document search over your data', icon: Database },
  { label: 'Live Web Search', desc: 'Real-time Tavily web citations', icon: Globe },
  { label: 'Native Voice Mode', desc: 'Conversational voice synthesis', icon: Mic },
  { label: 'Timeline Branching', desc: 'Non-linear thread exploration', icon: GitBranch },
  { label: 'Dual Model Debate', desc: 'Optimist vs Skeptic consensus engine', icon: ShieldCheck }
];

export default function Navbar({ onLaunchApp }) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const scrollToSection = (id) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? 'bg-black/70 backdrop-blur-xl border-b border-white/10 shadow-[0_10px_30px_rgba(0,0,0,0.8)] py-3'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        {/* Brand Logo */}
        <div className="flex items-center gap-3 cursor-pointer select-none" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 via-indigo-600 to-cyan-500 p-0.5 shadow-[0_0_20px_rgba(139,92,246,0.4)]">
            <div className="w-full h-full bg-black rounded-[10px] flex items-center justify-center p-1.5 overflow-hidden">
              <img
                src={doxaLogo}
                alt="Doxa Logo"
                className="w-full h-full object-contain filter invert brightness-200"
              />
            </div>
          </div>
          <div className="flex flex-col">
            <span className="text-xl font-bold tracking-widest text-white font-orbitron uppercase bg-clip-text text-transparent bg-gradient-to-r from-white via-neutral-200 to-violet-400" style={{ fontFamily: 'Orbitron, sans-serif' }}>
              DOXA
            </span>
            <span className="text-[9px] font-mono tracking-wider text-violet-400 font-semibold uppercase leading-none">
              AUTONOMOUS AI v2.0
            </span>
          </div>
        </div>

        {/* Center Nav Links */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-sans text-neutral-300 font-medium">
          {/* Capabilities Dropdown */}
          <div className="relative" ref={dropdownRef}>
            <button
              type="button"
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center gap-1.5 hover:text-white transition-colors cursor-pointer py-1"
            >
              <span>What Doxa Can Do</span>
              <ChevronDown className={`w-4 h-4 text-violet-400 transition-transform duration-200 ${dropdownOpen ? 'rotate-180' : ''}`} />
            </button>

            <AnimatePresence>
              {dropdownOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 10, scale: 0.96 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 10, scale: 0.96 }}
                  transition={{ duration: 0.15 }}
                  className="absolute left-1/2 -translate-x-1/2 mt-3 w-80 p-2 rounded-2xl bg-neutral-950/95 backdrop-blur-2xl border border-violet-500/20 shadow-[0_20px_50px_rgba(0,0,0,0.9)] grid grid-cols-1 gap-1 z-50 font-sans"
                >
                  <div className="px-3 py-1.5 text-[10px] font-mono font-bold uppercase tracking-wider text-violet-400 border-b border-neutral-800">
                    Platform Capabilities
                  </div>
                  {CAPABILITIES.map((cap, idx) => {
                    const Icon = cap.icon;
                    return (
                      <div
                        key={idx}
                        onClick={() => {
                          setDropdownOpen(false);
                          scrollToSection('features');
                        }}
                        className="flex items-start gap-3 p-2.5 rounded-xl hover:bg-neutral-900/80 cursor-pointer transition-colors group"
                      >
                        <div className="p-2 rounded-lg bg-violet-500/10 border border-violet-500/20 text-violet-400 group-hover:bg-violet-500/20 group-hover:text-cyan-300 transition-colors shrink-0">
                          <Icon className="w-4 h-4" />
                        </div>
                        <div className="flex flex-col">
                          <span className="text-xs font-semibold text-white group-hover:text-violet-300 transition-colors">
                            {cap.label}
                          </span>
                          <span className="text-[10px] text-neutral-400 leading-tight mt-0.5">
                            {cap.desc}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <button
            type="button"
            onClick={() => scrollToSection('features')}
            className="hover:text-white transition-colors cursor-pointer"
          >
            Features
          </button>

          <button
            type="button"
            onClick={() => scrollToSection('how-it-works')}
            className="hover:text-white transition-colors cursor-pointer"
          >
            How It Works
          </button>
        </nav>

        {/* Right CTA Button */}
        <div className="flex items-center gap-4">
          <motion.button
            type="button"
            onClick={onLaunchApp}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.96 }}
            className="relative px-5 py-2.5 rounded-full font-bold text-xs uppercase tracking-wider text-white shadow-[0_0_25px_rgba(139,92,246,0.5)] overflow-hidden group cursor-pointer"
            style={{ fontFamily: 'Orbitron, sans-serif' }}
          >
            {/* Animated Gradient Background */}
            <span className="absolute inset-0 bg-gradient-to-r from-violet-600 via-indigo-600 to-cyan-500 group-hover:brightness-125 transition-all duration-300" />
            <span className="relative z-10 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-300 animate-pulse" />
              <span>Try Doxa</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </span>
          </motion.button>
        </div>
      </div>
    </header>
  );
}
