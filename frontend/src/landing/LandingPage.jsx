import React from 'react';
import HeroStarfield from './HeroStarfield';
import Navbar from './Navbar';
import HeroSection from './HeroSection';
import FeatureShowcase from './FeatureShowcase';
import CapabilityStrip from './CapabilityStrip';
import HowItWorks from './HowItWorks';
import FinalCTA from './FinalCTA';
import Footer from './Footer';

export default function LandingPage({ onLaunchApp }) {
  return (
    <div className="min-h-screen bg-black text-white relative overflow-x-hidden selection:bg-violet-500/30 selection:text-white font-sans">
      {/* Three.js Heavy Motion Background */}
      <HeroStarfield />

      {/* Navbar */}
      <Navbar onLaunchApp={onLaunchApp} />

      {/* Hero Section */}
      <HeroSection onLaunchApp={onLaunchApp} />

      {/* Transition Seam: Black to White/Off-white */}
      <div className="relative w-full h-40 bg-gradient-to-b from-black to-[#fafafa] z-10 pointer-events-none" />

      {/* White background content wrap */}
      <div className="bg-[#fafafa] text-neutral-900 z-10 relative selection:bg-violet-100 selection:text-violet-900">
        {/* Capability Numbers & Stats Strip */}
        <CapabilityStrip />

        {/* 11 Full Feature Showcase Blocks */}
        <FeatureShowcase onLaunchApp={onLaunchApp} />

        {/* How It Works Flow */}
        <HowItWorks />

        {/* Closing CTA */}
        <FinalCTA onLaunchApp={onLaunchApp} />
      </div>

      {/* Footer */}
      <Footer onLaunchApp={onLaunchApp} />
    </div>
  );
}
