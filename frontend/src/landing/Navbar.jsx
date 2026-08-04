import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ArrowRight, Cpu, Database, Globe, Mic, GitBranch, ShieldCheck, Zap, Bell, Menu, X } from 'lucide-react';
import doxaLogo from '../assets/logo.png';

const CAPABILITIES = [
  { label: 'Autonomous Reasoning', desc: 'Multi-step planning & tool execution', icon: Cpu },
  { label: 'RAG Knowledge Base', desc: 'Vector document search over your data', icon: Database },
  { label: 'Live Web Search', desc: 'Real-time Tavily web citations', icon: Globe },
  { label: 'Native Voice Mode', desc: 'Conversational voice synthesis', icon: Mic },
  { label: 'Timeline Branching', desc: 'Non-linear thread exploration', icon: GitBranch },
  { label: 'Dual Model Debate', desc: 'Optimist vs Skeptic consensus engine', icon: ShieldCheck }
];

const WHATS_NEW = [
  { label: 'Voice Mode 2.0', desc: 'Natural conversation with streaming TTS' },
  { label: 'Timeline Branching', desc: 'Explore alternative reasoning paths' },
  { label: 'Processing Engine Selector', desc: 'Choose your AI model on-the-fly' },
];

export default function Navbar({ onLaunchApp }) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [capabilitiesOpen, setCapabilitiesOpen] = useState(false);
  const [whatsNewOpen, setWhatsNewOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const capRef = useRef(null);
  const newRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (capRef.current && !capRef.current.contains(e.target)) {
        setCapabilitiesOpen(false);
      }
      if (newRef.current && !newRef.current.contains(e.target)) {
        setWhatsNewOpen(false);
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
    setCapabilitiesOpen(false);
    setWhatsNewOpen(false);
    setMobileMenuOpen(false);
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? 'bg-black/60 backdrop-blur-2xl border-b border-white/[0.06] shadow-lg py-3.5'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-14">

        {/* ── Left: Logo mark + wordmark ── */}
        <div
          className="flex items-center gap-2.5 cursor-pointer select-none shrink-0"
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        >
          {/* Plain icon — no container, no border, no glow */}
          <img
            src={doxaLogo}
            alt="Doxa"
            className="w-9 h-9 object-contain"
            style={{ filter: 'invert(1) brightness(2)' }}
          />
          <span className="text-[21px] font-semibold tracking-tight text-white">
            Doxa
          </span>
        </div>

        {/* ── Center: Nav links (desktop) ── */}
        <nav className="hidden md:flex items-center gap-1.5 text-[15px] text-neutral-400 font-medium">

          {/* What Doxa Can Do — dropdown */}
          <div className="relative" ref={capRef}>
            <button
              type="button"
              onClick={() => {
                setCapabilitiesOpen(!capabilitiesOpen);
                setWhatsNewOpen(false);
              }}
              className="flex items-center gap-1 px-3 py-2 rounded-lg hover:text-white hover:bg-white/[0.04] transition-colors cursor-pointer"
            >
              <span>What Doxa Can Do</span>
              <ChevronDown className={`w-3.5 h-3.5 opacity-50 transition-transform duration-200 ${capabilitiesOpen ? 'rotate-180' : ''}`} />
            </button>

            <AnimatePresence>
              {capabilitiesOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 8 }}
                  transition={{ duration: 0.15, ease: 'easeOut' }}
                  className="absolute left-1/2 -translate-x-1/2 mt-2 w-[320px] p-1.5 rounded-xl bg-neutral-950/95 backdrop-blur-2xl border border-white/[0.08] shadow-2xl z-50"
                >
                  {CAPABILITIES.map((cap, idx) => {
                    const Icon = cap.icon;
                    return (
                      <div
                        key={idx}
                        onClick={() => {
                          setCapabilitiesOpen(false);
                          scrollToSection('features');
                        }}
                        className="flex items-start gap-3 px-3 py-2.5 rounded-lg hover:bg-white/[0.04] cursor-pointer transition-colors group"
                      >
                        <div className="mt-0.5 p-1.5 rounded-md bg-white/[0.04] text-neutral-400 group-hover:text-violet-400 transition-colors shrink-0">
                          <Icon className="w-4 h-4" />
                        </div>
                        <div className="flex flex-col">
                          <span className="text-[13px] font-medium text-neutral-200 group-hover:text-white transition-colors">
                            {cap.label}
                          </span>
                          <span className="text-[11px] text-neutral-500 leading-snug mt-0.5">
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

          {/* Subscriptions — static link */}
          <button
            type="button"
            onClick={() => scrollToSection('pricing')}
            className="px-3 py-2 rounded-lg hover:text-white hover:bg-white/[0.04] transition-colors cursor-pointer"
          >
            Subscriptions
          </button>

          {/* What's New — dropdown */}
          <div className="relative" ref={newRef}>
            <button
              type="button"
              onClick={() => {
                setWhatsNewOpen(!whatsNewOpen);
                setCapabilitiesOpen(false);
              }}
              className="flex items-center gap-1 px-3 py-2 rounded-lg hover:text-white hover:bg-white/[0.04] transition-colors cursor-pointer"
            >
              <span>What's New</span>
              <ChevronDown className={`w-3.5 h-3.5 opacity-50 transition-transform duration-200 ${whatsNewOpen ? 'rotate-180' : ''}`} />
            </button>

            <AnimatePresence>
              {whatsNewOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 8 }}
                  transition={{ duration: 0.15, ease: 'easeOut' }}
                  className="absolute left-1/2 -translate-x-1/2 mt-2 w-[300px] p-1.5 rounded-xl bg-neutral-950/95 backdrop-blur-2xl border border-white/[0.08] shadow-2xl z-50"
                >
                  {WHATS_NEW.map((item, idx) => (
                    <div
                      key={idx}
                      className="flex items-start gap-3 px-3 py-2.5 rounded-lg hover:bg-white/[0.04] cursor-pointer transition-colors group"
                    >
                      <div className="mt-0.5 p-1.5 rounded-md bg-white/[0.04] text-neutral-400 group-hover:text-cyan-400 transition-colors shrink-0">
                        <Zap className="w-4 h-4" />
                      </div>
                      <div className="flex flex-col">
                        <span className="text-[13px] font-medium text-neutral-200 group-hover:text-white transition-colors">
                          {item.label}
                        </span>
                        <span className="text-[11px] text-neutral-500 leading-snug mt-0.5">
                          {item.desc}
                        </span>
                      </div>
                    </div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </nav>

        {/* ── Right: Try Doxa CTA ── */}
        <div className="flex items-center gap-3">
          {/* Try Doxa — simple solid gradient pill */}
          <motion.button
            type="button"
            onClick={onLaunchApp}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            className="hidden sm:flex items-center gap-2 px-5 py-2.5 rounded-full text-[14px] font-semibold text-white cursor-pointer overflow-hidden"
            style={{
              background: 'linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #06b6d4 100%)',
            }}
          >
            <img
              src={doxaLogo}
              alt=""
              className="w-[18px] h-[18px] object-contain"
              style={{ filter: 'invert(1) brightness(2)' }}
            />
            <span>Try Doxa</span>
            <ArrowRight className="w-3.5 h-3.5 opacity-70" />
          </motion.button>

          {/* Mobile menu toggle */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg text-neutral-400 hover:text-white hover:bg-white/[0.06] transition-colors cursor-pointer"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* ── Mobile Menu ── */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2, ease: 'easeOut' }}
            className="md:hidden overflow-hidden bg-black/90 backdrop-blur-2xl border-t border-white/[0.06]"
          >
            <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col gap-1">
              <button
                onClick={() => scrollToSection('features')}
                className="text-left px-3 py-2.5 rounded-lg text-neutral-300 hover:text-white hover:bg-white/[0.04] transition-colors text-[14px] font-medium"
              >
                What Doxa Can Do
              </button>
              <button
                onClick={() => scrollToSection('pricing')}
                className="text-left px-3 py-2.5 rounded-lg text-neutral-300 hover:text-white hover:bg-white/[0.04] transition-colors text-[14px] font-medium"
              >
                Subscriptions
              </button>
              <button
                onClick={() => scrollToSection('how-it-works')}
                className="text-left px-3 py-2.5 rounded-lg text-neutral-300 hover:text-white hover:bg-white/[0.04] transition-colors text-[14px] font-medium"
              >
                What's New
              </button>
              <div className="pt-2 border-t border-white/[0.06] mt-1">
                <button
                  onClick={() => { setMobileMenuOpen(false); onLaunchApp(); }}
                  className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-full text-[13px] font-semibold text-white cursor-pointer"
                  style={{
                    background: 'linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #06b6d4 100%)',
                  }}
                >
                  <img
                    src={doxaLogo}
                    alt=""
                    className="w-4 h-4 object-contain"
                    style={{ filter: 'invert(1) brightness(2)' }}
                  />
                  <span>Try Doxa</span>
                  <ArrowRight className="w-3.5 h-3.5 opacity-70" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
