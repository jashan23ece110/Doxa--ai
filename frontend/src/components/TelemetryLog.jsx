import React, { useState, useEffect, useRef, useCallback } from 'react';

const INITIAL_ENTRIES = [
  { text: 'System initialized', type: 'success' },
  { text: 'Neural core online', type: 'success' },
  { text: 'Knowledge base connected', type: 'info' },
  { text: 'Encryption verified', type: 'success' },
  { text: 'Telemetry stream active', type: 'info' },
  { text: 'Memory allocation nominal', type: 'info' },
  { text: 'Inference engine ready', type: 'success' },
  { text: 'Watchdog heartbeat started', type: 'info' },
  { text: 'All subsystems operational', type: 'success' },
];

const SIMULATED_EVENTS = [
  { text: 'Memory optimized', type: 'info' },
  { text: 'Cache refreshed', type: 'info' },
  { text: 'Signal strength nominal', type: 'success' },
  { text: 'Heartbeat OK', type: 'success' },
  { text: 'Garbage collection complete', type: 'info' },
  { text: 'Latency check passed', type: 'success' },
  { text: 'Token buffer flushed', type: 'info' },
  { text: 'Thermal readings stable', type: 'info' },
  { text: 'Network handshake verified', type: 'success' },
  { text: 'Index rebalanced', type: 'info' },
  { text: 'Checkpoint saved', type: 'success' },
  { text: 'Bandwidth utilization 42%', type: 'info' },
];

const MAX_ENTRIES = 50;

const formatTimestamp = (date) =>
  date.toLocaleTimeString('en-GB', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });

const TelemetryLog = ({ agentSteps }) => {
  const [entries, setEntries] = useState(() => {
    const now = new Date();
    return INITIAL_ENTRIES.map((e, i) => ({
      ...e,
      timestamp: new Date(now.getTime() - (INITIAL_ENTRIES.length - i) * 800),
    }));
  });

  const scrollRef = useRef(null);
  const prevStepsLenRef = useRef(0);

  const pushEntry = useCallback((text, type = 'info') => {
    setEntries((prev) => {
      const next = [...prev, { text, type, timestamp: new Date() }];
      return next.length > MAX_ENTRIES ? next.slice(next.length - MAX_ENTRIES) : next;
    });
  }, []);

  // Simulated system events every 3-5 seconds
  useEffect(() => {
    const schedule = () => {
      const delay = 3000 + Math.random() * 2000;
      return setTimeout(() => {
        const event = SIMULATED_EVENTS[Math.floor(Math.random() * SIMULATED_EVENTS.length)];
        pushEntry(event.text, event.type);
        timerRef = schedule();
      }, delay);
    };

    let timerRef = schedule();
    return () => clearTimeout(timerRef);
  }, [pushEntry]);

  // Ingest real agent steps
  useEffect(() => {
    if (!agentSteps || agentSteps.length === 0) return;

    const newSteps = agentSteps.slice(prevStepsLenRef.current);
    prevStepsLenRef.current = agentSteps.length;

    newSteps.forEach((step) => {
      const action = step.action || step.tool || step.type || 'step';
      const label = step.status === 'error' ? 'error' : 'info';
      pushEntry(`Agent: ${action}${step.detail ? ' — ' + step.detail : ''}`, label);
    });
  }, [agentSteps, pushEntry]);

  // Auto-scroll
  useEffect(() => {
    const el = scrollRef.current;
    if (el) {
      el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
    }
  }, [entries]);

  return (
    <div className="hud-panel" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3
        className="text-[10px] uppercase tracking-[0.2em] mb-2"
        style={{ fontFamily: "'Orbitron', sans-serif", color: '#ffd60a', flexShrink: 0 }}
      >
        Telemetry
      </h3>

      <div
        ref={scrollRef}
        className="hud-scrollbar"
        style={{ flex: 1, overflowY: 'auto', minHeight: 0 }}
      >
        {entries.map((entry, i) => {
          let eventClass = 'event';
          if (entry.type === 'success') eventClass += ' event-success';
          else if (entry.type === 'error') eventClass += ' event-error';
          else if (entry.type === 'info') eventClass += ' event-info';

          return (
            <div key={i} className="telemetry-line">
              <span className="timestamp">[{formatTimestamp(entry.timestamp)}]</span>{' '}
              <span className={eventClass}>{entry.text}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TelemetryLog;
