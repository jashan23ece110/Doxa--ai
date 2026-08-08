import React from 'react';
import { Shield, User, Settings as SettingsIcon, Radio, PanelLeftOpen, PanelLeftClose, Cpu } from 'lucide-react';
import SvgLogo from '../landing/logo/SvgLogo';

export default function TopBar({
  user,
  toggleSidebar,
  sidebarOpen,
  onNavigate,
  activeOverlay,
  isSphereMode,
  onToggleSphereMode,
  rightPanelOpen = true,
  onToggleRightPanel,
}) {
  const truncatedEmail = user && user.includes('@') ? user.split('@')[0] : user;

  return (
    <header
      className="w-full h-14 md:h-16 px-4 sm:px-6 flex items-center justify-between select-none z-30 bg-neutral-950/80 backdrop-blur-xl border-b border-white/[0.08] shadow-[0_4px_30px_rgba(0,0,0,0.4)] relative"
      aria-label="Application Top Header"
    >
      {/* ── Left Section: Sidebar Toggle & Canonical Doxa Branding ── */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={toggleSidebar}
          className="p-2 rounded-xl bg-white/[0.03] hover:bg-white/[0.08] border border-white/[0.1] text-neutral-300 hover:text-white transition-all cursor-pointer flex items-center justify-center focus:outline-none focus-visible:ring-2 focus-visible:ring-violet-400"
          title={sidebarOpen ? 'Collapse Sidebar' : 'Expand Sidebar'}
          aria-label={sidebarOpen ? 'Collapse Sidebar' : 'Expand Sidebar'}
        >
          {sidebarOpen ? (
            <PanelLeftClose className="w-4 h-4 text-neutral-400 group-hover:text-white" />
          ) : (
            <PanelLeftOpen className="w-4 h-4 text-cyan-400" />
          )}
        </button>

        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-xl bg-white/[0.04] border border-white/[0.1] flex items-center justify-center shadow-inner">
            <SvgLogo size={20} className="w-5 h-5" />
          </div>
          <div className="flex items-center gap-2">
            <span
              className="font-extrabold text-base md:text-lg tracking-wider text-white uppercase font-mono"
              style={{ fontFamily: 'Orbitron, sans-serif' }}
            >
              DOXA
            </span>
            <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded-full bg-white/[0.04] border border-white/[0.12] text-[10px] font-mono tracking-wider text-neutral-300 font-semibold uppercase">
              ENTERPRISE OS
            </span>
          </div>
        </div>
      </div>

      {/* ── Center Section: Active Workspace Label (Subtle, Non-obtrusive) ── */}
      <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-full bg-white/[0.02] border border-white/[0.06] text-xs font-mono text-neutral-400">
        <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
        <span className="tracking-wide">AUTONOMOUS REASONING CORE</span>
      </div>

      {/* ── Right Section: Status Badges & Action Controls ── */}
      <div className="flex items-center gap-2.5 sm:gap-3">
        {/* Status Indicators */}
        <div className="hidden sm:flex items-center gap-3 px-3 py-1.5 rounded-xl bg-white/[0.02] border border-white/[0.06] text-xs font-mono">
          {/* Online Badge */}
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]" />
            <span className="text-[11px] font-medium text-neutral-300">ONLINE</span>
          </div>

          <span className="text-neutral-700">|</span>

          {/* Encrypted Badge */}
          <div className="flex items-center gap-1.5">
            <Shield className="w-3.5 h-3.5 text-violet-400" />
            <span className="text-[11px] font-medium text-neutral-400">ENCRYPTED</span>
          </div>

          <span className="text-neutral-700">|</span>

          {/* User Account */}
          <div className="flex items-center gap-1.5">
            <User className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-[11px] text-neutral-300 font-semibold truncate max-w-[120px]">
              {truncatedEmail || 'Enterprise User'}
            </span>
          </div>
        </div>

        {/* Intelligence Context Panel Toggle */}
        {onToggleRightPanel && (
          <button
            type="button"
            onClick={onToggleRightPanel}
            className={`p-2 rounded-xl border transition-all duration-200 cursor-pointer flex items-center justify-center ${
              rightPanelOpen
                ? 'bg-cyan-500/15 border-cyan-400 text-cyan-300 shadow-[0_0_12px_rgba(6,182,212,0.3)]'
                : 'bg-white/[0.03] hover:bg-white/[0.08] border-white/[0.1] text-neutral-400 hover:text-white'
            }`}
            title={rightPanelOpen ? 'Hide Intelligence Panel' : 'Show Intelligence Panel'}
            aria-label="Toggle Intelligence Panel"
          >
            <Cpu className="w-4 h-4" />
          </button>
        )}

        {/* Sphere Mode Toggle */}
        <button
          type="button"
          onClick={onToggleSphereMode}
          className={`px-3 py-1.5 rounded-xl border transition-all duration-200 cursor-pointer flex items-center gap-2 text-xs font-medium font-mono ${
            isSphereMode
              ? 'bg-cyan-500/15 border-cyan-400 text-cyan-200 shadow-[0_0_15px_rgba(6,182,212,0.3)] font-semibold'
              : 'bg-white/[0.03] hover:bg-white/[0.08] border-white/[0.1] text-neutral-300 hover:text-white'
          }`}
          title="Toggle Voice Assistant Mode"
          aria-label="Toggle Voice Assistant Mode"
        >
          <Radio className={`w-3.5 h-3.5 ${isSphereMode ? 'animate-pulse text-cyan-400' : 'text-neutral-400'}`} />
          <span className="hidden md:inline uppercase text-[11px] tracking-wider">Voice Mode</span>
        </button>

        {/* System Settings Modal Trigger */}
        <button
          type="button"
          onClick={() => {
            if (activeOverlay) {
              onNavigate?.(null);
            } else {
              onNavigate?.('settings');
            }
          }}
          className={`p-2 rounded-xl border transition-all duration-200 cursor-pointer flex items-center justify-center ${
            activeOverlay
              ? 'bg-violet-500/20 border-violet-400 text-white shadow-[0_0_15px_rgba(124,58,237,0.3)]'
              : 'bg-white/[0.03] hover:bg-white/[0.08] border-white/[0.1] text-neutral-300 hover:text-white'
          }`}
          title="System Settings"
          aria-label="System Settings"
        >
          <SettingsIcon
            className={`w-4 h-4 ${activeOverlay ? 'animate-spin text-violet-300' : 'text-neutral-400'}`}
            style={{ animationDuration: '8s' }}
          />
        </button>
      </div>
    </header>
  );
}
