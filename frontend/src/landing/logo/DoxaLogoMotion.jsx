import React, { useEffect, useState } from 'react';
import { motion, useAnimation, useReducedMotion } from 'framer-motion';
import { logoVariants } from './logoStates';
import './logoMotion.css';

export default function DoxaLogoMotion({
  className = '',
  width,
  height,
  style,
  color = 'currentColor',
  ...props
}) {
  const controls = useAnimation();
  const prefersReducedMotion = useReducedMotion();
  const [currentState, setCurrentState] = useState('form');

  // Intelligent Interaction System
  // Sequence: form -> deform -> transform -> reform -> finalForm -> form
  const playTransformationSequence = async () => {
    if (prefersReducedMotion) return;

    setCurrentState('deform');
    await controls.start('deform');

    setCurrentState('transform');
    await controls.start('transform');

    setCurrentState('reform');
    await controls.start('reform');

    setCurrentState('finalForm');
    await controls.start('finalForm');

    // Hold final form briefly, then return to base form (resting)
    setTimeout(async () => {
      setCurrentState('form');
      await controls.start('form');
    }, 2000);
  };

  useEffect(() => {
    if (prefersReducedMotion) {
      controls.start('reduced');
    } else {
      controls.start('form');
    }
  }, [controls, prefersReducedMotion]);

  // Derive class for CSS drop-shadows
  const glowClass = `is-${currentState.replace(/([A-Z])/g, '-$1').toLowerCase()}`;

  return (
    <motion.svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 100 100"
      className={`doxa-logo-motion ${glowClass} ${className}`}
      width={width}
      height={height}
      style={style}
      fill="none"
      stroke={color}
      strokeWidth="7"
      onMouseEnter={playTransformationSequence}
      aria-label="Doxa AI Logo"
      {...props}
    >
      <motion.circle
        cx="50" cy="50" r="42"
        variants={logoVariants.outer}
        initial={prefersReducedMotion ? "reduced" : "form"}
        animate={controls}
      />
      <motion.circle
        cx="50" cy="64" r="28"
        variants={logoVariants.middle}
        initial={prefersReducedMotion ? "reduced" : "form"}
        animate={controls}
      />
      <motion.circle
        cx="50" cy="78" r="14"
        variants={logoVariants.inner}
        initial={prefersReducedMotion ? "reduced" : "form"}
        animate={controls}
      />
    </motion.svg>
  );
}
