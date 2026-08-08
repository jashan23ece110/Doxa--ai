import React from 'react';

export default function SvgLogo({ className = '', width, height, style, ...props }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 100 100"
      className={className}
      width={width}
      height={height}
      style={style}
      fill="none"
      stroke="currentColor"
      strokeWidth="7"
      {...props}
    >
      <circle cx="50" cy="50" r="42" />
      <circle cx="50" cy="64" r="28" />
      <circle cx="50" cy="78" r="14" />
    </svg>
  );
}
