import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

export default function VoiceTelemetry({ isSpeaking = false }) {
  const [amplitude, setAmplitude] = useState(0.1);
  const barsRef = useRef([]);
  const animRef = useRef(null);

  useEffect(() => {
    if (!isSpeaking) {
      setAmplitude(0.0);
      return;
    }

    const startTime = Date.now();
    const updateWave = () => {
      const elapsed = (Date.now() - startTime) / 1000;
      
      // Replicate the central core's voice-reactive envelope formula
      const syllableWave = Math.sin(elapsed * 3.8 * Math.PI * 2);
      const intonationWave = Math.sin(elapsed * 18.0);
      let envelope = (syllableWave * 0.55 + intonationWave * 0.15 + 0.45);
      envelope = Math.max(0.05, Math.min(1.0, envelope));
      
      setAmplitude(envelope);

      // Animate each vertical bar in the waveform
      if (barsRef.current) {
        barsRef.current.forEach((bar, idx) => {
          if (!bar) return;
          // Stagger each bar slightly using the index
          const barPhase = idx * 0.18;
          const individualSyllable = Math.sin((elapsed * 3.8 * Math.PI * 2) - barPhase);
          const individualIntonation = Math.sin((elapsed * 18.0) - barPhase);
          let val = (individualSyllable * 0.55 + individualIntonation * 0.15 + 0.45);
          val = Math.max(0.05, Math.min(1.0, val)) * envelope;
          
          const targetHeight = 8 + val * 38; // height between 8px and 46px
          bar.style.height = `${targetHeight}px`;
        });
      }

      animRef.current = requestAnimationFrame(updateWave);
    };

    animRef.current = requestAnimationFrame(updateWave);
    return () => {
      if (animRef.current) cancelAnimationFrame(animRef.current);
    };
  }, [isSpeaking]);

  if (!isSpeaking) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 15 }}
      transition={{ duration: 0.3 }}
      className="hud-panel hud-panel-bright p-3.5 flex flex-col gap-2.5 w-full bg-neutral-950/80 backdrop-blur-md border border-[var(--jarvis-accent)]/30 rounded-xl shadow-[0_0_20px_rgba(var(--jarvis-accent-rgb),0.15)]"
      style={{ fontFamily: 'Rajdhani, sans-serif' }}
    >
      {/* Header */}
      <div className="flex items-center justify-between text-[10px] tracking-wider font-semibold" style={{ fontFamily: 'Orbitron, sans-serif' }}>
        <span className="text-[var(--jarvis-accent)] flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-[var(--jarvis-accent)] animate-ping" />
          CORE TELEMETRY // VOICE ENVELOPE
        </span>
        <span className="text-[#00ff88] flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-[#00ff88]" />
          SPEAKING // BROADCAST ACTIVE
        </span>
      </div>

      {/* Waveform Visualization Bars */}
      <div className="h-12 flex items-center justify-center gap-1 bg-neutral-950/60 border border-[var(--jarvis-border)] rounded-lg px-4 overflow-hidden relative">
        <div className="absolute inset-0 opacity-10 bg-[linear-gradient(rgba(var(--jarvis-accent-rgb),0.1)_50%,transparent_50%)] bg-[length:100%_4px]" />
        {Array.from({ length: 32 }).map((_, idx) => (
          <div
            key={idx}
            ref={(el) => (barsRef.current[idx] = el)}
            className="w-1 rounded-full bg-gradient-to-t from-[var(--jarvis-accent)] to-[var(--jarvis-accent-hover)] transition-all duration-75"
            style={{ height: '8px', minWidth: '3px' }}
          />
        ))}
      </div>

      {/* Technical metrics */}
      <div className="grid grid-cols-3 gap-2 text-[10px] font-semibold text-[var(--jarvis-text-dim)] uppercase tracking-wider text-center" style={{ fontFamily: 'Orbitron, sans-serif' }}>
        <div className="bg-neutral-900/40 py-1 rounded border border-[var(--jarvis-border)] truncate">
          CHANNEL: <span className="text-white font-mono text-[9px]">DOXA_CORE_01 // SECURE</span>
        </div>
        <div className="bg-neutral-900/40 py-1 rounded border border-[var(--jarvis-border)] truncate">
          ROTATION: <span className="text-white font-mono text-[9px]">{(0.04 + amplitude * 0.08).toFixed(3)} RAD/S</span>
        </div>
        <div className="bg-neutral-900/40 py-1 rounded border border-[var(--jarvis-border)] truncate">
          LATENCY: <span className="text-white font-mono text-[9px]">{(1.8 + amplitude * 1.2).toFixed(2)} MS</span>
        </div>
      </div>
    </motion.div>
  );
}
