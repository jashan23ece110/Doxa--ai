import React from 'react';
import { motion } from 'framer-motion';
import CentralCore from './CentralCore';
import StatsPanel from './StatsPanel';
import RadarGauge from './RadarGauge';
import ObjectivesCard from './ObjectivesCard';
import TelemetryLog from './TelemetryLog';
import TopBar from './TopBar';

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
  morphText = '',
  toggleSidebar,
  sidebarOpen,
  isSphereMode = false,
  onToggleSphereMode,
}) {
  const isAgentActive = agentLoading || agentStatus?.status === 'running' || isDebating;
  const isAgentThinking = (agentStatus?.status === 'running' && (agentStatus?.steps?.length || 0) < 5) || isDebating;

  return (
    <div className="h-full w-full flex flex-col relative overflow-hidden scan-lines grid-bg">
      {/* ── ambient glow blobs (dynamic variables mapped to current theme) ── */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <div
          className={`absolute -top-[15%] -right-[10%] w-[700px] h-[700px] rounded-full bg-[radial-gradient(circle,rgba(var(--jarvis-accent-rgb),0.08)_0%,transparent_60%)] transition-opacity duration-700 ${
            isSphereMode ? 'opacity-30' : 'opacity-100'
          }`}
        />
        <div
          className={`absolute top-[50%] -left-[15%] w-[500px] h-[500px] rounded-full bg-[radial-gradient(circle,rgba(var(--jarvis-accent-rgb),0.05)_0%,transparent_55%)] transition-opacity duration-700 ${
            isSphereMode ? 'opacity-20' : 'opacity-100'
          }`}
        />
        <div
          className={`absolute bottom-[5%] right-[20%] w-[400px] h-[400px] rounded-full bg-[radial-gradient(circle,rgba(var(--jarvis-accent-rgb),0.04)_0%,transparent_50%)] transition-opacity duration-700 ${
            isSphereMode ? 'opacity-20' : 'opacity-100'
          }`}
        />
      </div>

      {/* ── top bar ── */}
      <div
        className={`transition-all duration-500 ease-out z-30 ${
          isSphereMode ? 'opacity-0 -translate-y-6 pointer-events-none' : 'opacity-100 translate-y-0 pointer-events-auto'
        }`}
      >
        <TopBar
          user={user}
          toggleSidebar={toggleSidebar}
          sidebarOpen={sidebarOpen}
          onNavigate={onNavigate}
          activeOverlay={activeOverlay}
          isSphereMode={isSphereMode}
          onToggleSphereMode={onToggleSphereMode}
        />
      </div>

      {/* ── main grid ── */}
      <div className="flex-1 flex min-h-0 relative z-10">
        {/* left column: stats */}
        <motion.div
          variants={slideUp}
          initial="initial"
          animate="animate"
          className={`hidden lg:flex flex-col w-64 xl:w-72 p-4 gap-4 shrink-0 z-20 transition-all duration-500 ease-out ${
            isSphereMode ? 'opacity-0 -translate-x-12 pointer-events-none' : 'opacity-100 translate-x-0 pointer-events-auto'
          }`}
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
            className={`flex-1 w-full max-w-[800px] xl:max-w-[1000px] flex items-center justify-center relative pointer-events-auto transition-all duration-700 ease-out ${
              isSphereMode ? 'scale-110 sm:scale-125 md:scale-130 -translate-y-2' : 'scale-100 translate-y-0'
            }`}
          >
            <CentralCore
              isActive={isAgentActive}
              isThinking={isAgentThinking}
              isSpeaking={isSpeaking}
              themeName={themeName}
              sentiment={sentiment}
              isDebating={isDebating}
              steps={steps}
              morphText={morphText}
            />
          </motion.div>
        </div>

        {/* right column: gauges + telemetry */}
        <motion.div
          variants={slideUp}
          initial="initial"
          animate="animate"
          transition={{ delay: 0.15 }}
          className={`hidden lg:flex flex-col w-64 xl:w-72 p-4 gap-4 shrink-0 transition-all duration-500 ease-out ${
            isSphereMode ? 'opacity-0 translate-x-12 pointer-events-none' : 'opacity-100 translate-x-0 pointer-events-auto'
          }`}
        >
          <RadarGauge queriesCount={queriesCount} />
          <div className="flex-1 min-h-0">
            <TelemetryLog agentSteps={agentStatus?.steps} />
          </div>
        </motion.div>
      </div>

      {/* ── mobile: stats + telemetry ── */}
      <div
        className={`lg:hidden px-4 pb-4 flex gap-4 overflow-x-auto hud-scrollbar shrink-0 select-none pb-5 border-t border-[rgba(var(--jarvis-accent-rgb),0.05)] bg-neutral-950/20 backdrop-blur-sm z-20 transition-all duration-500 ease-out ${
          isSphereMode ? 'opacity-0 translate-y-12 pointer-events-none' : 'opacity-100 translate-y-0 pointer-events-auto'
        }`}
      >
        <div className="min-w-[280px] shrink-0">
          <StatsPanel />
        </div>
        <div className="min-w-[280px] shrink-0">
          <ObjectivesCard queriesCount={queriesCount} sessionStart={sessionStart} />
        </div>
        <div className="min-w-[280px] shrink-0">
          <RadarGauge queriesCount={queriesCount} />
        </div>
        <div className="min-w-[280px] shrink-0 h-[220px]">
          <TelemetryLog agentSteps={agentStatus?.steps} />
        </div>
      </div>
    </div>
  );
}
