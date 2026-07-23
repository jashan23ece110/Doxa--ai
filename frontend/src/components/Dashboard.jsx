import React from 'react';
import { motion } from 'framer-motion';
import { Mic } from 'lucide-react';
import CentralCore from './CentralCore';
import StatsPanel from './StatsPanel';
import RadarGauge from './RadarGauge';
import ObjectivesCard from './ObjectivesCard';
import TelemetryLog from './TelemetryLog';
import TopBar from './TopBar';
import HudNav from './HudNav';

const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.6, ease: 'easeOut' } },
};

const slideUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
};

export default function Dashboard({
  user,
  agentLoading,
  agentStatus,
  isSpeaking,
  queriesCount,
  sessionStart,
  activeOverlay,
  onNavigate,
  themeName = 'ultron',
  sentiment = 'neutral',
  isDebating = false,
  steps = [],
}) {
  const isAgentActive = agentLoading || agentStatus?.status === 'running' || isDebating;
  const isAgentThinking = (agentStatus?.status === 'running' && (agentStatus?.steps?.length || 0) < 5) || isDebating;

  return (
    <div className="h-full w-full flex flex-col relative overflow-hidden scan-lines grid-bg">
      {/* ── ambient glow blobs (dynamic variables mapped to current theme) ── */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <div className="absolute -top-[15%] -right-[10%] w-[700px] h-[700px] rounded-full bg-[radial-gradient(circle,rgba(var(--jarvis-accent-rgb),0.08)_0%,transparent_60%)]" />
        <div className="absolute top-[50%] -left-[15%] w-[500px] h-[500px] rounded-full bg-[radial-gradient(circle,rgba(var(--jarvis-accent-rgb),0.05)_0%,transparent_55%)]" />
        <div className="absolute bottom-[5%] right-[20%] w-[400px] h-[400px] rounded-full bg-[radial-gradient(circle,rgba(var(--jarvis-accent-rgb),0.04)_0%,transparent_50%)]" />
      </div>

      {/* ── top bar ── */}
      <TopBar user={user} />

      {/* ── HUD nav (left edge) ── */}
      <HudNav activeOverlay={activeOverlay} onNavigate={onNavigate} />

      {/* ── main grid ── */}
      <div className="flex-1 flex min-h-0 relative z-10">
        {/* left column: stats */}
        <motion.div
          variants={slideUp}
          initial="initial"
          animate="animate"
          className="hidden lg:flex flex-col w-64 xl:w-72 p-4 gap-4 shrink-0 z-20"
        >
          <StatsPanel />
          <ObjectivesCard queriesCount={queriesCount} sessionStart={sessionStart} />
        </motion.div>

        <div className="flex-1 flex flex-col items-center justify-center p-4 gap-4 min-w-0 pointer-events-none">
          {/* central core sphere */}
          <motion.div
            variants={fadeIn}
            initial="initial"
            animate="animate"
            className="flex-1 w-full max-w-[800px] xl:max-w-[1000px] flex items-center justify-center relative pointer-events-auto"
          >
            <CentralCore
              isActive={isAgentActive}
              isThinking={isAgentThinking}
              isSpeaking={isSpeaking}
              themeName={themeName}
              sentiment={sentiment}
              isDebating={isDebating}
              steps={steps}
            />
          </motion.div>
        </div>

        {/* right column: gauges + telemetry */}
        <motion.div
          variants={slideUp}
          initial="initial"
          animate="animate"
          transition={{ delay: 0.15 }}
          className="hidden lg:flex flex-col w-64 xl:w-72 p-4 gap-4 shrink-0"
        >
          <RadarGauge queriesCount={queriesCount} />
          <div className="flex-1 min-h-0">
            <TelemetryLog agentSteps={agentStatus?.steps} />
          </div>
        </motion.div>
      </div>

      {/* ── mobile: stats + telemetry (collapsed into bottom sheet) ── */}
      <div className="lg:hidden px-4 pb-4 flex gap-3 overflow-x-auto">
        <div className="min-w-[250px]">
          <RadarGauge queriesCount={queriesCount} />
        </div>
      </div>
    </div>
  );
}
