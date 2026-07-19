import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Cpu, HardDrive, Zap, Wifi, Thermometer, ArrowUpDown } from 'lucide-react';

const METRICS = [
  { key: 'neural',    label: 'Neural Core', icon: Cpu,         initial: 78 },
  { key: 'memory',    label: 'Memory',      icon: HardDrive,   initial: 45 },
  { key: 'latency',   label: 'Latency',     icon: Zap,         initial: 23 },
  { key: 'signal',    label: 'Signal',       icon: Wifi,        initial: 92 },
  { key: 'thermal',   label: 'Thermal',     icon: Thermometer, initial: 34 },
  { key: 'bandwidth', label: 'Bandwidth',   icon: ArrowUpDown, initial: 67 },
];

const AnimatedNumber = ({ value }) => {
  const [displayValue, setDisplayValue] = useState(value);
  const prevValue = useRef(value);

  useEffect(() => {
    if (prevValue.current === value) return;
    
    const start = prevValue.current;
    const end = value;
    const duration = 200; // ms
    let startTime;
    let animFrame;

    const tick = (now) => {
      if (!startTime) startTime = now;
      const progress = Math.min((now - startTime) / duration, 1);
      
      const current = Math.round(start + (end - start) * progress);
      setDisplayValue(current);
      
      if (progress < 1) {
        animFrame = requestAnimationFrame(tick);
      } else {
        prevValue.current = end;
      }
    };
    
    animFrame = requestAnimationFrame(tick);
    
    return () => cancelAnimationFrame(animFrame);
  }, [value]);

  return <>{displayValue}</>;
};

const StatsPanel = () => {
  const [values, setValues] = useState(() =>
    Object.fromEntries(METRICS.map((m) => [m.key, m.initial]))
  );

  useEffect(() => {
    const interval = setInterval(() => {
      setValues((prev) => {
        const next = { ...prev };
        METRICS.forEach(({ key, initial }) => {
          const drift = (Math.random() * 10 - 5); // ±5
          next[key] = Math.min(100, Math.max(0, Math.round(initial + drift)));
        });
        return next;
      });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="hud-panel hud-panel-scan">
      <h3
        style={{
          fontFamily: "'Orbitron', sans-serif",
          fontSize: '0.7rem',
          color: '#ffd60a',
          textTransform: 'uppercase',
          letterSpacing: '0.25em',
          marginBottom: '1rem',
        }}
      >
        System Status
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {METRICS.map((metric, i) => {
          const Icon = metric.icon;
          const value = values[metric.key];

          return (
            <motion.div
              key={metric.key}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1, duration: 0.4, ease: 'easeOut' }}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.6rem',
              }}
            >
              <Icon
                size={16}
                style={{ color: '#ffd60a', flexShrink: 0 }}
              />

              <span
                style={{
                  fontFamily: "'Rajdhani', sans-serif",
                  fontSize: '0.8rem',
                  color: '#e0d6c2',
                  width: '5.5rem',
                  flexShrink: 0,
                }}
              >
                {metric.label}
              </span>

              <div className="hud-progress" style={{ flex: 1 }}>
                <div
                  className="hud-progress-fill"
                  style={{
                    width: `${value}%`,
                    transition: 'width 1s ease-in-out',
                  }}
                />
              </div>

              <span
                style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: '0.75rem',
                  color: '#ffd60a',
                  width: '2.5rem',
                  textAlign: 'right',
                  flexShrink: 0,
                }}
              >
                <AnimatedNumber value={value} />%
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

export default StatsPanel;
