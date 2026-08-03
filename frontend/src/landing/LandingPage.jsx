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

      {/* Capability Numbers & Stats Strip */}
      <CapabilityStrip />

      {/* 12 Feature Showcase Blocks */}
      <FeatureShowcase />

      {/* How It Works Flow */}
      <HowItWorks />

      {/* Closing CTA */}
      <FinalCTA onLaunchApp={onLaunchApp} />

      {/* Footer */}
      <Footer onLaunchApp={onLaunchApp} />
    </div>
  );
}
