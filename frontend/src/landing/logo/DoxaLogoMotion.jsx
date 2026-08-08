import React, { useState, useCallback } from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import {
  MOTION_TIMINGS,
  OUTER_RING_KEYFRAMES,
  MIDDLE_RING_KEYFRAMES,
  INNER_RING_KEYFRAMES,
  GLOW_KEYFRAMES,
} from './logoStates';

/**
 * DoxaLogoMotion — Canonical 2D UI Logo Micro-Motion System
 *
 * Implements the 5-State Doxa Motion Lifecycle:
 * FORM → DEFORM → TRANSFORM → REFORM → FINAL FORM → FORM (Rest)
 *
 * Triggers on desktop hover (mouseenter) and mobile tap (click/touchstart).
 * Respects `prefers-reduced-motion` for accessibility.
 */
export default function DoxaLogoMotion({
  size,
  width = 36,
  height = 36,
  className = '',
  color = 'currentColor',
  ariaLabel = 'Doxa Logo',
  interactive = true,
  style = {},
  ...props
}) {
  const w = size || width;
  const h = size || height;
  const shouldReduceMotion = useReducedMotion();
  const [isAnimating, setIsAnimating] = useState(false);

  const triggerAnimation = useCallback(() => {
    if (!interactive || shouldReduceMotion || isAnimating) return;
    setIsAnimating(true);
  }, [interactive, shouldReduceMotion, isAnimating]);

  const handleAnimationComplete = useCallback(() => {
    setIsAnimating(false);
  }, []);

  // Static / Rest variants (Form State)
  const restVariant = {
    x: 0,
    y: 0,
    scale: 1,
    rotate: 0,
    opacity: 0.95,
    transition: { duration: 0.3, ease: 'easeOut' },
  };

  return (
    <motion.svg
      width={w}
      height={h}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label={ariaLabel}
      className={`shrink-0 cursor-pointer select-none ${className}`}
      style={{
        ...style,
        willChange: isAnimating ? 'filter, transform' : 'auto',
      }}
      onMouseEnter={triggerAnimation}
      onClick={triggerAnimation}
      onTouchStart={triggerAnimation}
      animate={
        isAnimating && !shouldReduceMotion
          ? GLOW_KEYFRAMES
          : { filter: 'drop-shadow(0 0 3px rgba(168, 85, 247, 0.25))' }
      }
      transition={
        isAnimating
          ? {
              duration: MOTION_TIMINGS.totalDuration,
              times: MOTION_TIMINGS.times,
              ease: 'easeInOut',
            }
          : { duration: 0.3 }
      }
      {...props}
    >
      {/* Outer Ring */}
      <motion.circle
        id="doxa-ring-outer"
        data-ring="outer"
        cx="50"
        cy="40"
        r="32"
        stroke={color}
        strokeWidth="3.6"
        strokeLinecap="round"
        style={{ transformOrigin: '50px 40px' }}
        animate={
          isAnimating && !shouldReduceMotion
            ? OUTER_RING_KEYFRAMES
            : restVariant
        }
        transition={
          isAnimating
            ? {
                duration: MOTION_TIMINGS.totalDuration,
                times: MOTION_TIMINGS.times,
                ease: 'easeInOut',
              }
            : { duration: 0.3 }
        }
        onAnimationComplete={handleAnimationComplete}
      />

      {/* Middle Ring */}
      <motion.circle
        id="doxa-ring-middle"
        data-ring="middle"
        cx="45"
        cy="53"
        r="22"
        stroke={color}
        strokeWidth="3.4"
        strokeLinecap="round"
        style={{ transformOrigin: '45px 53px' }}
        animate={
          isAnimating && !shouldReduceMotion
            ? MIDDLE_RING_KEYFRAMES
            : restVariant
        }
        transition={
          isAnimating
            ? {
                duration: MOTION_TIMINGS.totalDuration,
                times: MOTION_TIMINGS.times,
                ease: 'easeInOut',
              }
            : { duration: 0.3 }
        }
      />

      {/* Inner Ring */}
      <motion.circle
        id="doxa-ring-inner"
        data-ring="inner"
        cx="42"
        cy="64"
        r="13"
        stroke={color}
        strokeWidth="3.2"
        strokeLinecap="round"
        style={{ transformOrigin: '42px 64px' }}
        animate={
          isAnimating && !shouldReduceMotion
            ? INNER_RING_KEYFRAMES
            : restVariant
        }
        transition={
          isAnimating
            ? {
                duration: MOTION_TIMINGS.totalDuration,
                times: MOTION_TIMINGS.times,
                ease: 'easeInOut',
              }
            : { duration: 0.3 }
        }
      />
    </motion.svg>
  );
}
