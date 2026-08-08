import React from 'react';

/**
 * SvgLogo — Reusable, accessible, scalable 2D vector logo for Doxa.
 *
 * Renders Doxa's signature 3 nested offset rings mark.
 * Uses `currentColor` for effortless theme adaptation (light/dark/gradients).
 * Target individual rings via data-ring / id for future animation/morphing.
 */
export default function SvgLogo({
  size,
  width = 36,
  height = 36,
  className = '',
  color = 'currentColor',
  ariaLabel = 'Doxa Logo',
  style = {},
  ...props
}) {
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
      style={style}
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
        className="transition-colors duration-300"
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
        className="transition-colors duration-300"
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
        className="transition-colors duration-300"
      />
    </svg>
  );
}
