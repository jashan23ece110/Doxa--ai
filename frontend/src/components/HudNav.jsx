import React from 'react';
import { motion } from 'framer-motion';
import { Code2, FileText, History, Settings } from 'lucide-react';

const NAV_ITEMS = [
  { id: 'eval', icon: Code2, label: 'EVAL' },
  { id: 'documents', icon: FileText, label: 'DOCS' },
  { id: 'history', icon: History, label: 'HISTORY' },
  { id: 'settings', icon: Settings, label: 'CONFIG' },
];

export default function HudNav({ activeOverlay, onNavigate }) {
  return (
    <div
      style={{
        position: 'fixed',
        left: 0,
        top: '50%',
        transform: 'translateY(-50%)',
        zIndex: 20,
        display: 'flex',
        flexDirection: 'column',
        gap: '4px',
        padding: '10px 6px',
        borderRadius: '0 12px 12px 0',
        background: 'rgba(6, 12, 28, 0.82)',
        backdropFilter: 'blur(12px)',
        border: '1px solid rgba(220, 20, 60, 0.08)',
        borderLeft: 'none',
        boxShadow: '4px 0 24px rgba(0, 0, 0, 0.3)',
      }}
    >
      {NAV_ITEMS.map((item) => {
        const isActive = activeOverlay === item.id;
        const Icon = item.icon;

        return (
          <motion.button
            key={item.id}
            onClick={() => onNavigate?.(item.id)}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            title={item.label}
            style={{
              position: 'relative',
              width: '40px',
              height: '40px',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '2px',
              background: isActive
                ? 'rgba(220, 20, 60, 0.08)'
                : 'transparent',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              padding: 0,
              transition: 'background 0.2s ease',
              borderLeft: isActive
                ? '2px solid #dc143c'
                : '2px solid transparent',
            }}
          >
            <Icon
              size={17}
              color={isActive ? '#dc143c' : '#7a7060'}
              style={{
                transition: 'color 0.2s ease',
                filter: isActive
                  ? 'drop-shadow(0 0 4px rgba(220, 20, 60, 0.5))'
                  : 'none',
              }}
            />
            <span
              style={{
                fontFamily: "'Orbitron', sans-serif",
                fontSize: '6px',
                fontWeight: 600,
                letterSpacing: '0.08em',
                color: isActive ? '#dc143c' : '#3a4d62',
                textTransform: 'uppercase',
                lineHeight: 1,
                transition: 'color 0.2s ease',
              }}
            >
              {item.label}
            </span>
          </motion.button>
        );
      })}
    </div>
  );
}
