import React, { Suspense, lazy } from 'react';
import HeroStarfield from '../animations/HeroStarfield';
import Navbar from './Navbar';
import Footer from './Footer';
import HeroSection from '../sections/HeroSection';
import CapabilityStrip from '../sections/CapabilityStrip';

const FeatureShowcase = lazy(() => import('../sections/FeatureShowcase'));
const HowItWorks = lazy(() => import('../sections/HowItWorks'));
const FinalCTA = lazy(() => import('../sections/FinalCTA'));

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

        <Suspense fallback={<div className="h-96 flex items-center justify-center text-neutral-400">Loading...</div>}>
          {/* 11 Full Feature Showcase Blocks */}
          <FeatureShowcase onLaunchApp={onLaunchApp} />

          {/* How It Works Flow */}
          <HowItWorks />

          {/* Closing CTA */}
          <FinalCTA onLaunchApp={onLaunchApp} />
        </Suspense>
      </div>

      {/* Footer */}
      <Footer onLaunchApp={onLaunchApp} />
    </div>
  );
}
