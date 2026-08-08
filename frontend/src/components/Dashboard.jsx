import React from 'react';
import { motion } from 'framer-motion';
import CentralCore from './CentralCore';
import TopBar from './TopBar';

const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.6, ease: 'easeOut' } },
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
    <div className={`w-full flex flex-col relative overflow-hidden scan-lines grid-bg ${isSphereMode ? 'h-full flex-1' : 'shrink-0 z-30'}`}>
      {/* ── ambient glow blobs ── */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <div
          className={`absolute -top-[15%] -right-[10%] w-[700px] h-[700px] rounded-full bg-[radial-gradient(circle,rgba(var(--jarvis-accent-rgb),0.08)_0%,transparent_60%)] transition-opacity duration-700 ${
            isSphereMode ? 'opacity-30' : 'opacity-10'
          }`}
        />
      </div>

      {/* ── top bar ── */}
      <div className="w-full z-30">
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

      {/* ── full-screen central sphere (Exclusive to Sphere Mode) ── */}
      {isSphereMode && (
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
      )}
    </div>
  );
}
