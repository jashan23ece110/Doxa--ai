import React from 'react';
import DoxaLogoMotion from './DoxaLogoMotion';

/**
 * SvgLogo — Canonical 2D Logo entry point for Doxa.
 *
 * Automatically wraps `DoxaLogoMotion` for interactive 5-state micro-animations
 * (FORM → DEFORM → TRANSFORM → REFORM → FINAL FORM).
 * Set `animated={false}` for static vector rendering where micro-interaction is unnecessary.
 */
export default function SvgLogo({
  size,
  width = 36,
  height = 36,
  className = '',
  color = 'currentColor',
  ariaLabel = 'Doxa Logo',
  animated = true,
  interactive = true,
  style = {},
  ...props
}) {
  if (animated) {
    return (
      <DoxaLogoMotion
        size={size}
        width={width}
        height={height}
        className={className}
        color={color}
        ariaLabel={ariaLabel}
        interactive={interactive}
        style={style}
        {...props}
      />
    );
  }

  const w = size || width;
  const h = size || height;

  return (
    <svg
      width={w}
      height={h}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label={ariaLabel}
      className={`shrink-0 ${className}`}
      style={{
        ...style,
        filter: 'drop-shadow(0 0 3px rgba(168, 85, 247, 0.25))',
      }}
      {...props}
    >
      {/* Outer Ring */}
      <circle
        id="doxa-ring-outer"
        data-ring="outer"
        cx="50"
        cy="40"
        r="32"
        stroke={color}
        strokeWidth="3.6"
        strokeLinecap="round"
      />

      {/* Middle Ring */}
      <circle
        id="doxa-ring-middle"
        data-ring="middle"
        cx="45"
        cy="53"
        r="22"
        stroke={color}
        strokeWidth="3.4"
        strokeLinecap="round"
      />

      {/* Inner Ring */}
      <circle
        id="doxa-ring-inner"
        data-ring="inner"
        cx="42"
        cy="64"
        r="13"
        stroke={color}
        strokeWidth="3.2"
        strokeLinecap="round"
      />
    </svg>
  );
}

export { DoxaLogoMotion };
