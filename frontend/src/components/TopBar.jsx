import React, { useState, useEffect } from 'react';
import { Shield, User } from 'lucide-react';

const TopBar = ({ user }) => {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (date) =>
    date.toLocaleTimeString('en-GB', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });

  const formatDate = (date) =>
    date.toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });

  const truncatedEmail = user && user.length > 20 ? user.slice(0, 20) + '…' : user;

  return (
    <div
      className="flex items-center justify-between px-5 w-full"
      style={{
        height: 48,
        background: 'transparent',
        borderBottom: '1px solid rgba(255,214,10,0.15)',
      }}
    >
      {/* Left — Branding */}
      <div className="flex items-center gap-2">
        <span
          className="font-bold text-lg tracking-widest"
          style={{ fontFamily: "'Orbitron', sans-serif", color: '#ffffff' }}
        >
          DOXA
        </span>
        <span className="text-[10px]" style={{ color: '#3a4a5c' }}>
          v2.0
        </span>
      </div>

      {/* Center — Live Clock */}
      <div className="flex flex-col items-center leading-tight">
        <span
          className="text-base tracking-wider"
          style={{ fontFamily: "'JetBrains Mono', monospace", color: '#ffd60a' }}
        >
          {formatTime(now)}
        </span>
        <span className="text-[10px]" style={{ color: '#7a7060' }}>
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
          <span className="text-[10px] uppercase tracking-wider" style={{ color: '#7a7060' }}>
            Online
          </span>
        </div>

        {/* Encrypted */}
        <div className="flex items-center gap-1">
          <Shield size={11} color="#7a7060" />
          <span className="text-[10px] uppercase tracking-wider" style={{ color: '#7a7060' }}>
            Encrypted
          </span>
        </div>

        {/* User */}
        <div className="flex items-center gap-1">
          <User size={11} color="#7a7060" />
          <span className="text-[10px] tracking-wider" style={{ color: '#7a7060' }}>
            {truncatedEmail || '—'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default TopBar;
