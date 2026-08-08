import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ArrowRight, Cpu, Database, ShieldAlert, GitBranch, Sparkles, Zap, Menu, X, Layers } from 'lucide-react';
import SvgLogo from './logo/SvgLogo';

const STAGE_NAV_ITEMS = [
  { label: 'Stages 1–5: Core AI OS', desc: 'Foundation, RAG & reasoning loops', id: 'stage-explorer', icon: Cpu },
  { label: 'Stages 6–7: Security & Risk', desc: 'Threat intelligence & human risk', id: 'security-human-intelligence', icon: ShieldAlert },
  { label: 'Stage 8: Data Intelligence', desc: 'Heterogeneous data & knowledge graphs', id: 'massive-data-intelligence', icon: Database },
  { label: 'Stage 9: Autonomous Agents', desc: 'Multi-agent swarms & tool execution', id: 'autonomous-software-agents', icon: GitBranch },
  { label: 'Stage 10: Decision Platform', desc: 'Executive decision support & scenarios', id: 'enterprise-decision-intelligence', icon: Sparkles },
  { label: 'Complete Feature Showcase', desc: 'Explore all 11 product capabilities', id: 'features', icon: Layers }
];

const WHATS_NEW = [
  { label: 'Stage 10 Decision Support', desc: 'Executive scenario analysis & feedback loops' },
  { label: 'Multi-Agent Swarms', desc: 'Delegated tool execution & human checkpoints' },
  { label: 'Native Voice Mode 2.0', desc: 'Natural conversation with streaming TTS' },
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
          ? 'bg-black/90 backdrop-blur-2xl border-b border-white/[0.08] shadow-lg py-3.5'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-14">

        {/* ── Left: Logo mark + wordmark ── */}
        <div
          className="flex items-center gap-2.5 cursor-pointer select-none shrink-0"
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => e.key === 'Enter' && window.scrollTo({ top: 0, behavior: 'smooth' })}
          aria-label="Scroll to top of Doxa Landing Page"
        >
          <SvgLogo size={36} className="w-9 h-9" />
          <span className="text-[21px] font-semibold tracking-tight text-white font-sans">
            Doxa
          </span>
        </div>

        {/* ── Center: Nav links (desktop) ── */}
        <nav className="hidden md:flex items-center gap-1.5 text-[15px] text-neutral-400 font-medium font-sans">

          {/* Architecture Stages dropdown */}
          <div className="relative" ref={capRef}>
            <button
              type="button"
              onClick={() => {
                setCapabilitiesOpen(!capabilitiesOpen);
                setWhatsNewOpen(false);
              }}
              className="flex items-center gap-1 px-3 py-2 rounded-lg hover:text-white hover:bg-white/[0.04] transition-colors cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400"
              aria-expanded={capabilitiesOpen}
              aria-label="Toggle Architecture Stages Menu"
            >
              <span>Capabilities & Stages</span>
              <ChevronDown className={`w-3.5 h-3.5 opacity-50 transition-transform duration-200 ${capabilitiesOpen ? 'rotate-180' : ''}`} />
            </button>

            <AnimatePresence>
              {capabilitiesOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 8 }}
                  transition={{ duration: 0.15, ease: 'easeOut' }}
                  className="absolute left-1/2 -translate-x-1/2 mt-2 w-[340px] p-1.5 rounded-2xl bg-neutral-950/95 backdrop-blur-2xl border border-white/[0.08] shadow-2xl z-50"
                >
                  {STAGE_NAV_ITEMS.map((item, idx) => {
                    const Icon = item.icon;
                    return (
                      <div
                        key={idx}
                        onClick={() => scrollToSection(item.id)}
                        className="flex items-start gap-3 px-3 py-2.5 rounded-xl hover:bg-white/[0.04] cursor-pointer transition-colors group"
                        role="button"
                        tabIndex={0}
                        onKeyDown={(e) => e.key === 'Enter' && scrollToSection(item.id)}
                      >
                        <div className="mt-0.5 p-1.5 rounded-lg bg-white/[0.04] text-neutral-400 group-hover:text-cyan-400 transition-colors shrink-0">
                          <Icon className="w-4 h-4" />
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
                    );
                  })}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* How It Works link */}
          <button
            type="button"
            onClick={() => scrollToSection('how-it-works')}
            className="px-3 py-2 rounded-lg hover:text-white hover:bg-white/[0.04] transition-colors cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400"
          >
            How It Works
          </button>

          {/* What's New dropdown */}
          <div className="relative" ref={newRef}>
            <button
              type="button"
              onClick={() => {
                setWhatsNewOpen(!whatsNewOpen);
                setCapabilitiesOpen(false);
              }}
              className="flex items-center gap-1 px-3 py-2 rounded-lg hover:text-white hover:bg-white/[0.04] transition-colors cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400"
              aria-expanded={whatsNewOpen}
              aria-label="Toggle What's New Menu"
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
                  className="absolute left-1/2 -translate-x-1/2 mt-2 w-[310px] p-1.5 rounded-2xl bg-neutral-950/95 backdrop-blur-2xl border border-white/[0.08] shadow-2xl z-50"
                >
                  {WHATS_NEW.map((item, idx) => (
                    <div
                      key={idx}
                      className="flex items-start gap-3 px-3 py-2.5 rounded-xl hover:bg-white/[0.04] cursor-pointer transition-colors group"
                    >
                      <div className="mt-0.5 p-1.5 rounded-lg bg-white/[0.04] text-neutral-400 group-hover:text-cyan-400 transition-colors shrink-0">
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
          <motion.button
            type="button"
            onClick={onLaunchApp}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            className="hidden sm:flex items-center gap-2 px-5 py-2 rounded-full text-[14px] font-semibold text-white cursor-pointer overflow-hidden shadow-[0_0_20px_rgba(124,58,237,0.3)] transition-all duration-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400"
            style={{
              background: 'linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #06b6d4 100%)',
            }}
            aria-label="Try Doxa AI Operating System"
          >
            <SvgLogo size={18} className="w-[18px] h-[18px]" />
            <span>Try Doxa</span>
            <ArrowRight className="w-3.5 h-3.5 opacity-70" />
          </motion.button>

          {/* Mobile menu toggle */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg text-neutral-400 hover:text-white hover:bg-white/[0.06] transition-colors cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400"
            aria-label="Toggle Mobile Menu"
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
            className="md:hidden overflow-hidden bg-black/95 backdrop-blur-2xl border-t border-white/[0.06]"
          >
            <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col gap-1">
              {STAGE_NAV_ITEMS.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => scrollToSection(item.id)}
                  className="text-left px-3 py-2.5 rounded-lg text-neutral-300 hover:text-white hover:bg-white/[0.04] transition-colors text-[14px] font-medium"
                >
                  {item.label}
                </button>
              ))}
              <div className="pt-3 border-t border-white/[0.06] mt-2">
                <button
                  onClick={() => { setMobileMenuOpen(false); onLaunchApp(); }}
                  className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-full text-[13px] font-semibold text-white cursor-pointer"
                  style={{
                    background: 'linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #06b6d4 100%)',
                  }}
                >
                  <SvgLogo size={16} className="w-4 h-4" />
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
