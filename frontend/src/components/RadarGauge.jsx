import React from 'react';

const RADIUS = 50;
const CENTER = 60;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;
const MAX_QUERIES = 100;

// Fixed dot positions (angles in degrees) on the outer health ring
const HEALTH_DOTS = [0, 45, 90, 135, 180, 225, 270, 315];

const RadarGauge = ({ queriesCount = 0 }) => {
  const clampedCount = Math.min(queriesCount, MAX_QUERIES);
  const queryOffset =
    CIRCUMFERENCE - (clampedCount / MAX_QUERIES) * CIRCUMFERENCE;

  return (
    <div className="hud-panel">
      <h3
        style={{
          fontFamily: "'Orbitron', sans-serif",
          fontSize: '0.7rem',
          color: '#dc143c',
          textTransform: 'uppercase',
          letterSpacing: '0.25em',
          marginBottom: '1rem',
        }}
      >
        Diagnostics
      </h3>

      <div
        style={{
          display: 'flex',
          flexDirection: 'row',
          gap: '1.5rem',
          justifyContent: 'center',
          alignItems: 'flex-start',
        }}
      >
        {/* ── Queries Processed Gauge ── */}
        <div style={{ textAlign: 'center' }}>
          <svg viewBox="0 0 120 120" width="120" height="120">
            {/* Background circle */}
            <circle
              cx={CENTER}
              cy={CENTER}
              r={RADIUS}
              fill="none"
              stroke="rgba(220, 20, 60,0.08)"
              strokeWidth="6"
            />

            {/* Animated arc */}
            <circle
              cx={CENTER}
              cy={CENTER}
              r={RADIUS}
              fill="none"
              stroke="#dc143c"
              strokeWidth="6"
              strokeLinecap="round"
              strokeDasharray={CIRCUMFERENCE}
              strokeDashoffset={queryOffset}
              style={{
                transition: 'stroke-dashoffset 0.8s ease-in-out',
                transform: 'rotate(-90deg)',
                transformOrigin: '50% 50%',
                filter: 'drop-shadow(0 0 6px rgba(220, 20, 60,0.7))',
              }}
            />

            {/* Center value */}
            <text
              x={CENTER}
              y={CENTER + 1}
              textAnchor="middle"
              dominantBaseline="central"
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: '1.4rem',
                fill: '#dc143c',
              }}
            >
              {clampedCount}
            </text>
          </svg>

          <p
            style={{
              fontFamily: "'Orbitron', sans-serif",
              fontSize: '0.6rem',
              color: '#dc143c',
              textTransform: 'uppercase',
              letterSpacing: '0.2em',
              marginTop: '0.35rem',
            }}
          >
            Queries
          </p>
        </div>

        {/* ── System Health Gauge ── */}
        <div style={{ textAlign: 'center' }}>
          <svg viewBox="0 0 120 120" width="120" height="120">
            {/* Outer decorative ring */}
            <circle
              cx={CENTER}
              cy={CENTER}
              r={RADIUS}
              fill="none"
              stroke="rgba(220, 20, 60,0.08)"
              strokeWidth="1.5"
            />

            {/* Middle decorative ring */}
            <circle
              cx={CENTER}
              cy={CENTER}
              r={RADIUS - 10}
              fill="none"
              stroke="rgba(220, 20, 60,0.06)"
              strokeWidth="1"
            />

            {/* Inner decorative ring */}
            <circle
              cx={CENTER}
              cy={CENTER}
              r={RADIUS - 20}
              fill="none"
              stroke="rgba(220, 20, 60,0.04)"
              strokeWidth="1"
            />

            {/* Dots on the outer ring */}
            {HEALTH_DOTS.map((deg) => {
              const rad = (deg * Math.PI) / 180;
              const x = CENTER + RADIUS * Math.cos(rad);
              const y = CENTER + RADIUS * Math.sin(rad);
              return (
                <circle
                  key={deg}
                  cx={x}
                  cy={y}
                  r="2"
                  fill="#dc143c"
                  opacity="0.6"
                />
              );
            })}

            {/* Rotating sweep line */}
            <line
              x1={CENTER}
              y1={CENTER}
              x2={CENTER}
              y2={CENTER - RADIUS + 4}
              stroke="#dc143c"
              strokeWidth="1.5"
              strokeLinecap="round"
              opacity="0.7"
              className="animate-scan-sweep"
              style={{ transformOrigin: `${CENTER}px ${CENTER}px` }}
            />

            {/* Center value */}
            <text
              x={CENTER}
              y={CENTER + 1}
              textAnchor="middle"
              dominantBaseline="central"
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: '1.2rem',
                fill: '#dc143c',
              }}
            >
              98%
            </text>
          </svg>

          <p
            style={{
              fontFamily: "'Orbitron', sans-serif",
              fontSize: '0.6rem',
              color: '#dc143c',
              textTransform: 'uppercase',
              letterSpacing: '0.2em',
              marginTop: '0.35rem',
            }}
          >
            Health
          </p>
        </div>
      </div>
    </div>
  );
};

export default RadarGauge;
