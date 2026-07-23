import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Zap, Bot, Clock, Target } from 'lucide-react';

const MetricItem = ({ icon: Icon, label, value, target, showBar }) => {
  const progress = target ? Math.min((parseFloat(value) / target) * 100, 100) : 0;

  return (
    <div className="flex flex-col gap-1 min-w-[140px]">
      <div className="flex items-center gap-1.5">
        <Icon size={12} color="var(--jarvis-text-dim)" />
        <span
          className="text-xs uppercase tracking-wider"
          style={{ fontFamily: "'Rajdhani', sans-serif", color: 'var(--jarvis-text-dim)' }}
        >
          {label}
        </span>
      </div>
      <span
        className="text-lg"
        style={{ fontFamily: "'JetBrains Mono', monospace", color: 'var(--jarvis-accent)' }}
      >
        {value}
        {target != null && (
          <span className="text-[10px]" style={{ color: 'rgba(var(--jarvis-accent-rgb), 0.35)' }}>
            {' '}
            / {target}
          </span>
        )}
      </span>
      {showBar && (
        <div
          className="w-full h-[3px] rounded-full overflow-hidden"
          style={{ background: 'rgba(var(--jarvis-accent-rgb),0.08)' }}
        >
          <div
            className="h-full rounded-full transition-all duration-700 ease-out"
            style={{
              width: `${progress}%`,
              background: 'linear-gradient(90deg, var(--jarvis-accent), #00ff88)',
              boxShadow: '0 0 8px rgba(var(--jarvis-accent-rgb),0.4)',
            }}
          />
        </div>
      )}
    </div>
  );
};

const ObjectivesCard = ({ queriesCount = 0, sessionStart }) => {
  const [uptime, setUptime] = useState('00:00:00');

  useEffect(() => {
    if (!sessionStart) return;

    const tick = () => {
      const diff = Math.max(0, Math.floor((Date.now() - sessionStart.getTime()) / 1000));
      const h = String(Math.floor(diff / 3600)).padStart(2, '0');
      const m = String(Math.floor((diff % 3600) / 60)).padStart(2, '0');
      const s = String(diff % 60).padStart(2, '0');
      setUptime(`${h}:${m}:${s}`);
    };

    tick();
    const timer = setInterval(tick, 1000);
    return () => clearInterval(timer);
  }, [sessionStart]);

  return (
    <motion.div
      className="hud-panel"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
    >
      <h3
        className="text-[10px] uppercase tracking-[0.2em] mb-4"
        style={{ fontFamily: "'Orbitron', sans-serif", color: 'var(--jarvis-accent)' }}
      >
        Objectives
      </h3>

      <div className="flex flex-col gap-4">
        <MetricItem
          icon={Zap}
          label="Queries Handled"
          value={queriesCount}
          target={50}
          showBar
        />
        <MetricItem
          icon={Bot}
          label="Automations Run"
          value={12}
          target={25}
          showBar
        />
        <MetricItem
          icon={Clock}
          label="Uptime"
          value={uptime}
          target={null}
          showBar={false}
        />
        <MetricItem
          icon={Target}
          label="Accuracy"
          value="94.2%"
          target={null}
          showBar={false}
        />
      </div>
    </motion.div>
  );
};

export default ObjectivesCard;
