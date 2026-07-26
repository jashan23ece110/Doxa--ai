import React, { useState, useEffect } from 'react';
import { Shield, User, Menu } from 'lucide-react';

const TopBar = ({ user, toggleSidebar, sidebarOpen }) => {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (date) =>
    date.toLocaleTimeString('en-GB', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });

  const formatDate = (date) =>
    date.toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: '2-digit' });

  const truncatedEmail = user && user.includes('@')
    ? user.split('@')[0]
    : user;

  return (
    <div
      className="flex items-center justify-between px-5 w-full"
      style={{
        height: 48,
        background: 'transparent',
        borderBottom: '1px solid rgba(var(--jarvis-accent-rgb),0.15)',
      }}
    >
      {/* Left — Branding */}
      <div className="flex items-center gap-2">
        <button
          onClick={toggleSidebar}
          className="mr-1 p-1 rounded-lg border border-[var(--jarvis-accent)]/15 text-neutral-400 hover:text-[var(--jarvis-accent)] hover:bg-[var(--jarvis-accent)]/5 hover:border-[var(--jarvis-accent)]/30 transition-all cursor-pointer z-30 flex items-center justify-center"
          title={sidebarOpen ? "Collapse Sidebar" : "Expand Sidebar"}
        >
          <Menu className="w-4 h-4" />
        </button>
        <span
          className="font-bold text-lg tracking-widest"
          style={{ fontFamily: "'Orbitron', sans-serif", color: '#ffffff' }}
        >
          DOXA
        </span>
        <span className="text-[10px]" style={{ color: 'var(--jarvis-text-dim)' }}>
          v2.0
        </span>
      </div>

      {/* Center — Live Clock */}
      <div className="flex flex-col items-center leading-tight">
        <span
          className="text-base tracking-wider"
          style={{ fontFamily: "'JetBrains Mono', monospace", color: 'var(--jarvis-accent)' }}
        >
          {formatTime(now)}
        </span>
        <span className="text-[10px]" style={{ color: 'var(--jarvis-text-dim)' }}>
          {formatDate(now)}
        </span>
      </div>

      {/* Right — Status Badges */}
      <div className="flex items-center gap-3">
        {/* Online */}
        <div className="flex items-center gap-1">
          <span
            className="inline-block w-[6px] h-[6px] rounded-full"
            style={{ background: '#00ff88', boxShadow: '0 0 6px rgba(0,255,136,0.6)' }}
          />
          <span className="text-[10px] uppercase tracking-wider" style={{ color: 'var(--jarvis-text-dim)' }}>
            Online
          </span>
        </div>

        {/* Encrypted */}
        <div className="flex items-center gap-1">
          <Shield size={11} color="var(--jarvis-text-dim)" />
          <span className="text-[10px] uppercase tracking-wider" style={{ color: 'var(--jarvis-text-dim)' }}>
            Encrypted
          </span>
        </div>

        {/* User */}
        <div className="flex items-center gap-1">
          <User size={11} color="var(--jarvis-text-dim)" />
          <span className="text-[10px] tracking-wider" style={{ color: 'var(--jarvis-text-dim)' }}>
            {truncatedEmail || '—'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default TopBar;
