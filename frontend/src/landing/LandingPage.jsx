import React from 'react';
import HeroStarfield from './HeroStarfield';
import Navbar from './Navbar';
import HeroSection from './HeroSection';
import CapabilityStrip from './CapabilityStrip';
import StageExplorer from './StageExplorer';
import SecurityHumanExplorer from './SecurityHumanExplorer';
import MassiveDataIntelligence from './MassiveDataIntelligence';
import AutonomousSoftwareAgents from './AutonomousSoftwareAgents';
import EnterpriseDecisionIntelligence from './EnterpriseDecisionIntelligence';
import FeatureShowcase from './FeatureShowcase';
import HowItWorks from './HowItWorks';
import FinalCTA from './FinalCTA';
import Footer from './Footer';

export default function LandingPage({ onLaunchApp }) {
  return (
    <div className="min-h-screen bg-black text-white relative overflow-x-hidden selection:bg-violet-500/30 selection:text-white font-sans">
      {/* Three.js GPU Motion Background */}
      <HeroStarfield />

      {/* Navbar */}
      <Navbar onLaunchApp={onLaunchApp} />

      {/* Hero Section */}
      <HeroSection onLaunchApp={onLaunchApp} />

      {/* Main Dark Content Wrapper */}
      <div className="bg-black text-white z-10 relative selection:bg-violet-500/30 selection:text-white">
        {/* Capability Indicators Strip */}
        <CapabilityStrip />

        {/* Interactive Stages 1–5 Intelligence Explorer */}
        <StageExplorer />

        {/* Stage 6 & Stage 7 Security & Human Intelligence Showcase */}
        <SecurityHumanExplorer />

        {/* Stage 8 Massive-Scale Data Intelligence Showcase */}
        <MassiveDataIntelligence />

        {/* Stage 9 Autonomous Software Agents Showcase */}
        <AutonomousSoftwareAgents />

        {/* Stage 10 Enterprise Decision Intelligence Showcase */}
        <EnterpriseDecisionIntelligence />

        {/* 11 Full Product Capability Showcase Blocks */}
        <FeatureShowcase onLaunchApp={onLaunchApp} />

        {/* 6-Stage Intelligence Lifecycle Flow */}
        <HowItWorks />

        {/* Closing CTA */}
        <FinalCTA onLaunchApp={onLaunchApp} />
      </div>

      {/* Footer */}
      <Footer onLaunchApp={onLaunchApp} />
    </div>
  );
}
