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

      {/* ── main layout: full-screen central sphere ── */}
      <div className="flex-1 flex min-h-0 relative z-10 items-center justify-center p-2 min-w-0 pointer-events-none">
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          className="w-full h-full flex items-center justify-center relative pointer-events-auto"
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
    </div>
  );
}
