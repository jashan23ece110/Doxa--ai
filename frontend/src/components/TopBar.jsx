import React from 'react';
import { Shield, User, Menu, Settings as SettingsIcon } from 'lucide-react';

const TopBar = ({ user, toggleSidebar, sidebarOpen, onNavigate, activeOverlay }) => {
  const truncatedEmail = user && user.includes('@')
    ? user.split('@')[0]
    : user;

  return (
    <div
      className="flex items-center justify-between px-5 w-full select-none"
      style={{
        height: 48,
        background: 'transparent',
        borderBottom: '1px solid rgba(var(--jarvis-accent-rgb),0.15)',
      }}
    >
      {/* Left — Sidebar toggle controls */}
      <div className="flex items-center">
        <button
          onClick={toggleSidebar}
          className="p-1 rounded-lg border border-[var(--jarvis-accent)]/15 text-neutral-400 hover:text-[var(--jarvis-accent)] hover:bg-[var(--jarvis-accent)]/5 hover:border-[var(--jarvis-accent)]/30 transition-all cursor-pointer z-30 flex items-center justify-center"
          title={sidebarOpen ? "Collapse Sidebar" : "Expand Sidebar"}
        >
          <Menu className="w-4 h-4" />
        </button>
      </div>

      {/* Center — Center-aligned DOXA title/logo */}
      <div className="flex items-center gap-2 leading-none">
        <span
          className="font-bold text-lg tracking-widest text-white uppercase font-orbitron"
          style={{ fontFamily: "'Orbitron', sans-serif" }}
        >
          DOXA
        </span>
        <span className="text-[10px] uppercase font-bold font-orbitron text-[var(--jarvis-accent)]" style={{ fontFamily: "'Orbitron', sans-serif", letterSpacing: '0.1em' }}>
          v2.0
        </span>
      </div>

      {/* Right — Status Badges & Settings Icon */}
      <div className="flex items-center gap-3.5">
        {/* Status indicator labels */}
        <div className="hidden sm:flex items-center gap-3">
          {/* Online */}
          <div className="flex items-center gap-1.5">
            <span
              className="inline-block w-[6px] h-[6px] rounded-full"
              style={{ background: '#00ff88', boxShadow: '0 0 6px rgba(0,255,136,0.6)' }}
            />
            <span className="text-[10px] uppercase tracking-wider font-semibold text-[var(--jarvis-text-dim)]">
              Online
            </span>
          </div>

          {/* Encrypted */}
          <div className="flex items-center gap-1.5">
            <Shield size={11} className="text-[var(--jarvis-text-dim)]" />
            <span className="text-[10px] uppercase tracking-wider font-semibold text-[var(--jarvis-text-dim)]">
              Encrypted
            </span>
          </div>

          {/* User */}
          <div className="flex items-center gap-1.5">
            <User size={11} className="text-[var(--jarvis-text-dim)]" />
            <span className="text-[10px] tracking-wider font-mono text-[var(--jarvis-text-dim)]">
              {truncatedEmail || '—'}
            </span>
          </div>
        </div>

        {/* System Settings gear icon (consolidated modal trigger) */}
        <button
          onClick={() => {
            if (activeOverlay) {
              onNavigate?.(null);
            } else {
              onNavigate?.('settings'); // Default to settings/config tab
            }
          }}
          className={`p-1.5 rounded-lg border transition-all cursor-pointer flex items-center justify-center ${
            activeOverlay
              ? 'bg-[rgba(var(--jarvis-accent-rgb),0.12)] border-[var(--jarvis-accent)] text-white shadow-[0_0_12px_rgba(var(--jarvis-accent-rgb),0.25)]'
              : 'border-neutral-800 text-neutral-400 hover:text-[var(--jarvis-accent)] hover:border-[var(--jarvis-accent)]/30 hover:bg-[var(--jarvis-accent)]/5'
          }`}
          title="System Settings"
        >
          <SettingsIcon 
            className={`w-4 h-4 ${activeOverlay ? 'animate-spin' : ''}`} 
            style={{ animationDuration: '8s' }} 
          />
        </button>
      </div>
    </div>
  );
};

export default TopBar;
