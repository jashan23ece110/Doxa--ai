import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

/**
 * HeroStarfield — 360k GPU-rendered particles forming the Doxa nested-rings logo.
 *
 * All per-particle computation lives in custom vertex/fragment shaders.
 * The JS animation loop only updates ~15 uniforms per frame — zero per-particle work.
 *
 * Features:
 *   • 360k particles desktop (30k mobile), ring-only, pure black bg
 *   • Click-and-drag rotation with momentum + idle auto-rotation
 *   • Global color cycling through 5 palettes (~1.5s each)
 *   • Localized hover color inversion (complement of current cycle color)
 *   • Click/tap ripple color pulse
 *   • Mouse + touch repulsion (coexists with drag — reduced during drag)
 *   • Bloom halo via second render pass with larger/softer point size
 */
export default function HeroStarfield() {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let width = window.innerWidth;
    let height = window.innerHeight;
    const isMobile = width < 768;

    // ── Scene ──
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 500);
    camera.position.z = 100;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    renderer.setClearColor(0x000000, 0);
    renderer.domElement.style.cursor = 'default';
    container.appendChild(renderer.domElement);

    // ── Logo ring geometry (exact Doxa mark — 3 offset circles) ──
    const S = 2.0;
    const rings = [
      { cx:  0 * S, cy:  4 * S, r: 28 * S, stroke: 2.8 * S },   // outer
      { cx: -3 * S, cy: -5 * S, r: 19 * S, stroke: 2.6 * S },   // middle
      { cx: -5 * S, cy: -12 * S, r: 12 * S, stroke: 2.4 * S },  // inner
    ];

    // ── Particle counts ──
    const PPR = isMobile ? 10000 : 120000;
    const count = PPR * 3; // 360k desktop, 30k mobile

    // ── Generate attribute data (set once, never modified in JS) ──
    const homeData      = new Float32Array(count * 3);
    const scatterData   = new Float32Array(count * 3);
    const phaseData     = new Float32Array(count);
    const ringIdxData   = new Float32Array(count);
    const brightnessData = new Float32Array(count);
    const angleData      = new Float32Array(count);
    const radiusData     = new Float32Array(count);
    const centerData     = new Float32Array(count * 2);

    let idx = 0;
    for (let ri = 0; ri < 3; ri++) {
      const ring = rings[ri];
      for (let p = 0; p < PPR; p++) {
        const angle = (p / PPR) * Math.PI * 2 + (Math.random() - 0.5) * 0.02;
        const t = (Math.random() + Math.random() + Math.random()) / 3; // gaussian-ish
        const r = ring.r + (t - 0.5) * ring.stroke;
        const x = ring.cx + Math.cos(angle) * r;
        const y = ring.cy + Math.sin(angle) * r;
        const z = (Math.random() - 0.5) * 3;

        const i3 = idx * 3;
        const i2 = idx * 2;
        homeData[i3]     = x;
        homeData[i3 + 1] = y;
        homeData[i3 + 2] = z;
        scatterData[i3]     = (Math.random() - 0.5) * 280;
        scatterData[i3 + 1] = (Math.random() - 0.5) * 280;
        scatterData[i3 + 2] = (Math.random() - 0.5) * 100;
        phaseData[idx]       = Math.random() * Math.PI * 2;
        ringIdxData[idx]     = ri;
        brightnessData[idx]  = 0.55 + Math.random() * 0.55;
        
        angleData[idx]       = angle;
        radiusData[idx]      = r;
        centerData[i2]       = ring.cx;
        centerData[i2 + 1]   = ring.cy;
        idx++;
      }
    }

    // ── Geometry ──
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position',    new THREE.BufferAttribute(homeData, 3));
    geometry.setAttribute('aScatter',    new THREE.BufferAttribute(scatterData, 3));
    geometry.setAttribute('aPhase',      new THREE.BufferAttribute(phaseData, 1));
    geometry.setAttribute('aRingIndex',  new THREE.BufferAttribute(ringIdxData, 1));
    geometry.setAttribute('aBrightness', new THREE.BufferAttribute(brightnessData, 1));
    geometry.setAttribute('aAngle',      new THREE.BufferAttribute(angleData, 1));
    geometry.setAttribute('aRadius',     new THREE.BufferAttribute(radiusData, 1));
    geometry.setAttribute('aCenter',     new THREE.BufferAttribute(centerData, 2));

    // ══════════════════════════════════════════════════════════════════════
    //  GLSL SHADERS — all per-particle logic runs on GPU
    // ══════════════════════════════════════════════════════════════════════

    const vertexShader = /* glsl */ `
      attribute vec3 aScatter;
      attribute float aPhase;
      attribute float aRingIndex;
      attribute float aBrightness;
      attribute float aAngle;
      attribute float aRadius;
      attribute vec2 aCenter;

      uniform float uTime;
      uniform float uFormation;
      uniform vec2  uPointer;
      uniform float uPointerActive;
      uniform float uDragging;
      uniform float uRepelRadius;
      uniform float uRepelStrength;
      uniform float uColorPhase;
      uniform float uClickPulseTime;
      uniform vec2  uClickOrigin;
      uniform float uPointSize;
      uniform float uPixelRatio;
      uniform float uDeform;
      uniform float uDeformMode;
      uniform float uFlowOffset;
      uniform float uModeProgress;

      varying vec3 vColor;

      // ── 5 palette modes × 3 rings ──
      vec3 palette(float m, float r) {
        // Palette 0 — Cyan
        if (m < 0.5) {
          return r < 0.5 ? vec3(0.024, 0.714, 0.831) :
                 r < 1.5 ? vec3(0.133, 0.827, 0.933) :
                           vec3(0.404, 0.910, 0.976);
        }
        // Palette 1 — Violet
        if (m < 1.5) {
          return r < 0.5 ? vec3(0.545, 0.361, 0.965) :
                 r < 1.5 ? vec3(0.659, 0.333, 0.969) :
                           vec3(0.753, 0.518, 0.988);
        }
        // Palette 2 — Indigo
        if (m < 2.5) {
          return r < 0.5 ? vec3(0.388, 0.400, 0.945) :
                 r < 1.5 ? vec3(0.506, 0.549, 0.973) :
                           vec3(0.647, 0.706, 0.988);
        }
        // Palette 3 — Sky Blue
        if (m < 3.5) {
          return r < 0.5 ? vec3(0.220, 0.741, 0.973) :
                 r < 1.5 ? vec3(0.490, 0.827, 0.988) :
                           vec3(0.729, 0.902, 0.992);
        }
        // Palette 4 — Magenta
        return r < 0.5 ? vec3(0.851, 0.275, 0.937) :
               r < 1.5 ? vec3(0.910, 0.475, 0.976) :
                         vec3(0.941, 0.671, 0.988);
      }

      void main() {
        // Compute base ring position dynamically using the flowing angle
        float currentAngle = aAngle + uFlowOffset;
        vec3 baseRingPos = vec3(aCenter.x + cos(currentAngle) * aRadius, aCenter.y + sin(currentAngle) * aRadius, position.z);

        // 1 ── Breathing animation
        float bx = sin(uTime * 0.5 + aPhase) * 0.8
                  + sin(uTime * 0.23 + aPhase * 2.3) * 0.32;
        float by = cos(uTime * 0.4 + aPhase * 1.7) * 0.8
                  + cos(uTime * 0.19 + aPhase * 3.1) * 0.32;
        float bz = sin(uTime * 0.35 + aPhase * 0.8) * 0.4;
        vec3 breathPos = baseRingPos + vec3(bx, by, bz);

        // 2 ── Formation convergence (scattered → formed)
        //      Stagger: inner ring forms first, outer last
        float ringDelay = (2.0 - aRingIndex) * 0.12;
        float f = smoothstep(ringDelay, ringDelay + 0.7, uFormation);
        vec3 localPos = mix(position + aScatter, breathPos, f);

        // 2.5 ── 5-Mode Intelligence Cycle (FORM → DEFORM → TRANSFORM → RETRIEVE → REFORM)
        vec3 p1 = breathPos;

        // Mode 2: DEFORM (Organic triangular wave shield)
        float triMod = 1.0 + 0.35 * cos(3.0 * currentAngle - 1.5708) + 0.08 * sin(6.0 * currentAngle);
        vec3 p2 = vec3(aCenter.x + cos(currentAngle) * aRadius * triMod, (aCenter.y + 3.0) + sin(currentAngle) * aRadius * triMod, position.z + sin(currentAngle * 4.0) * 4.0);

        // Mode 3: TRANSFORM (Intertwined swirl vortex)
        float swirlA = currentAngle + aRingIndex * 2.094;
        float rMod = aRadius * (1.0 + 0.38 * sin(2.0 * currentAngle + aRingIndex));
        vec3 p3 = vec3(cos(swirlA + 0.45 * sin(3.0 * currentAngle)) * rMod * 1.15, sin(swirlA + 0.45 * cos(3.0 * currentAngle)) * rMod * 1.15, position.z + sin(swirlA * 3.0) * 8.0);

        // Mode 4: RETRIEVE (Particle spiral galaxy / information stream)
        float normR = aRadius / 60.0;
        float spiralAngle = currentAngle * 2.8 + aRingIndex * 2.094 + (1.0 - normR) * 4.0 + uTime * 3.0;
        float spirR = 6.0 + normR * 38.0;
        vec3 p4 = vec3(cos(spiralAngle) * spirR, sin(spiralAngle) * spirR, (fract(aPhase * 10.0) - 0.5) * 20.0);

        // Mode 5: REFORM (Snap convergence)
        vec3 p5 = mix(p4, p1, 0.85);

        vec3 modePos = p1;
        if (uModeProgress > 0.001) {
          if (uModeProgress <= 0.20) {
            float t = smoothstep(0.0, 1.0, uModeProgress / 0.20);
            modePos = mix(p1, p2, t);
          } else if (uModeProgress <= 0.45) {
            float t = smoothstep(0.0, 1.0, (uModeProgress - 0.20) / 0.25);
            modePos = mix(p2, p3, t);
          } else if (uModeProgress <= 0.70) {
            float t = smoothstep(0.0, 1.0, (uModeProgress - 0.45) / 0.25);
            modePos = mix(p3, p4, t);
          } else if (uModeProgress <= 0.90) {
            float t = smoothstep(0.0, 1.0, (uModeProgress - 0.70) / 0.20);
            modePos = mix(p4, p5, t);
          } else {
            float t = smoothstep(0.0, 1.0, (uModeProgress - 0.90) / 0.10);
            modePos = mix(p5, p1, t);
          }
        }

        // Deform effect (Forward or Backward depending on uDeformMode)
        vec3 deformOffset;
        if (uDeformMode < 0.5) {
          deformOffset = aScatter * 0.55;
        } else {
          vec3 tangent = vec3(-sin(currentAngle), cos(currentAngle), 0.0);
          deformOffset = -tangent * aRadius * 0.35 + aScatter * 0.25;
        }
        
        vec3 targetPos = mix(modePos, breathPos + deformOffset, uDeform * f);
        localPos = mix(position + aScatter, targetPos, f);

        // 3 ── World transform (includes group rotation via modelMatrix)
        vec4 worldPos = modelMatrix * vec4(localPos, 1.0);

        // 4 ── Pointer repulsion (reduced during drag)
        float repelMix = uPointerActive * max(1.0 - uDragging * 0.9, 0.0);
        if (repelMix > 0.01) {
          vec2 diff = worldPos.xy - uPointer;
          float dist = length(diff);
          if (dist < uRepelRadius && dist > 0.01) {
            float force = 1.0 - dist / uRepelRadius;
            float strength = force * force * force * uRepelStrength * repelMix;
            worldPos.xy += (diff / dist) * strength;
          }
        }

        // 5 ── Project
        vec4 viewPos = viewMatrix * worldPos;
        gl_Position = projectionMatrix * viewPos;
        float cameraDist = max(-viewPos.z, 10.0);
        gl_PointSize = uPointSize * uPixelRatio * (100.0 / cameraDist);

        // 6 ── Color cycling (lerp between adjacent palette modes)
        float cp = mod(uColorPhase, 5.0);
        float modeA = floor(cp);
        float modeB = mod(modeA + 1.0, 5.0);
        float blendT = fract(cp);
        vec3 baseColor = mix(palette(modeA, aRingIndex),
                             palette(modeB, aRingIndex), blendT);

        // 7 ── Localized hover color inversion
        float hoverDist   = length(worldPos.xy - uPointer);
        float hoverRadius = uRepelRadius * 1.3;
        float hoverFactor = smoothstep(hoverRadius, hoverRadius * 0.15, hoverDist)
                          * uPointerActive
                          * max(1.0 - uDragging * 0.8, 0.0);
        vec3 invertedColor = vec3(1.0) - baseColor;
        vec3 finalColor = mix(baseColor, invertedColor, hoverFactor);

        // 8 ── Click ripple pulse
        float clickAge = uTime - uClickPulseTime;
        if (clickAge > 0.0 && clickAge < 2.0) {
          float clickDist = length(worldPos.xy - uClickOrigin);
          float ripplePos = clickAge * 70.0;
          float ripple = 1.0 - smoothstep(0.0, 18.0, abs(clickDist - ripplePos));
          float fade   = 1.0 - smoothstep(0.0, 2.0, clickAge);
          finalColor = mix(finalColor, vec3(1.0), ripple * fade * 0.65);
        }

        // 9 ── Per-particle brightness variation
        vColor = finalColor * aBrightness;
      }
    `;

    const fragmentShader = /* glsl */ `
      varying vec3 vColor;
      uniform float uGlowExp;
      uniform float uAlphaScale;

      void main() {
        vec2 c = 2.0 * gl_PointCoord - 1.0;
        float r2 = dot(c, c);
        if (r2 > 1.0) discard;
        float glow = exp(-r2 * uGlowExp);
        gl_FragColor = vec4(vColor * glow, glow * uAlphaScale);
      }
    `;

    // ── Shared uniforms (both materials reference the same objects) ──
    const shared = {
      uTime:           { value: 0 },
      uFormation:      { value: 0 },
      uDeform:         { value: 0 },
      uDeformMode:     { value: 0 },
      uFlowOffset:     { value: 0 },
      uPointer:        { value: new THREE.Vector2(99999, 99999) },
      uPointerActive:  { value: 0 },
      uDragging:       { value: 0 },
      uRepelRadius:    { value: isMobile ? 22 : 30 },
      uRepelStrength:  { value: isMobile ? 16 : 24 },
      uColorPhase:     { value: 0 },
      uClickPulseTime: { value: -100 },
      uClickOrigin:    { value: new THREE.Vector2(0, 0) },
      uPixelRatio:     { value: renderer.getPixelRatio() },
      uModeProgress:   { value: 0 },
    };

    // Main pass — sharp, full brightness
    const mainMaterial = new THREE.ShaderMaterial({
      uniforms: {
        ...shared,
        uPointSize:  { value: isMobile ? 1.5 : 1.8 },
        uGlowExp:    { value: 3.5 },
        uAlphaScale: { value: 0.85 },
      },
      vertexShader,
      fragmentShader,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    // Bloom pass — large, soft, dim (luminous halo)
    const bloomMaterial = new THREE.ShaderMaterial({
      uniforms: {
        ...shared,
        uPointSize:  { value: isMobile ? 5.0 : 7.0 },
        uGlowExp:    { value: 1.2 },
        uAlphaScale: { value: 0.09 },
      },
      vertexShader,
      fragmentShader,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    // ── Scene graph — parent group handles rotation ──
    const group = new THREE.Group();
    scene.add(group);

    const mainPoints = new THREE.Points(geometry, mainMaterial);
    mainPoints.frustumCulled = false;
    group.add(mainPoints);

    const bloomPoints = new THREE.Points(geometry, bloomMaterial);
    bloomPoints.frustumCulled = false;
    group.add(bloomPoints);

    // ══════════════════════════════════════════════════════════════════════
    //  INTERACTION STATE
    // ══════════════════════════════════════════════════════════════════════

    const clock = new THREE.Clock();

    let pointerX = 99999, pointerY = 99999;
    let pointerActive = false;

    // Drag rotation
    let isDragging = false;
    let maybeClick = false;
    let dragStartX = 0, dragStartY = 0;
    let dragPrevX = 0, dragPrevY = 0;
    let dragStartTime = 0;

    // Momentum after drag release
    let momentumX = 0, momentumY = 0;

    // Idle auto-rotation blend
    let lastInteractionTime = 0;
    let autoRotBlend = 0;

    // State machine cycle constants
    const STATE_FORMED = 0;
    const STATE_DEFORMING_FORWARD = 1;
    const STATE_HELD_FORWARD = 2;
    const STATE_REFORMING_FORWARD = 3;
    const STATE_REVERSE_FLOW = 4;
    const STATE_RESETTING = 5;
    const STATE_DEFORMING_BACKWARD = 6;
    const STATE_HELD_BACKWARD = 7;
    const STATE_REFORMING_BACKWARD = 8;

    let cycleState = STATE_FORMED;
    let cycleStateTimer = 0.0;

    let uDeformVal = 0.0;
    let uDeformModeVal = 0.0; // 0 = forward, 1 = backward

    // Flow path offset variables
    let flowSpeed = 0.05;
    let flowOffset = 0.0;
    let startFlowOffset = 0.0;

    // Reset rotation tracking
    let resetStartRotX = 0.0;
    let resetStartRotY = 0.0;
    let resetTargetRotY = 0.0;

    // Camera parallax
    let camTargetX = 0, camTargetY = 0;
    let camX = 0, camY = 0;
    let scrollY = 0;

    // ── Raycaster for screen → world conversion ──
    const raycaster = new THREE.Raycaster();
    const ndcVec = new THREE.Vector2();
    const worldPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    const worldIntersect = new THREE.Vector3();

    const updatePointerWorld = (clientX, clientY) => {
      const rect = renderer.domElement.getBoundingClientRect();
      ndcVec.x = ((clientX - rect.left) / rect.width) * 2 - 1;
      ndcVec.y = -((clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(ndcVec, camera);
      if (raycaster.ray.intersectPlane(worldPlane, worldIntersect)) {
        pointerX = worldIntersect.x;
        pointerY = worldIntersect.y;
      }
    };

    // Skip drag-start if clicking on a button/link
    const isInteractive = (e) =>
      e.target && e.target.closest && e.target.closest('button, a, input, [role=button]');

    // ══════════════════════════════════════════════════════════════════════
    //  MOUSE EVENTS
    // ══════════════════════════════════════════════════════════════════════

    const onMouseDown = (e) => {
      if (isInteractive(e)) return;
      maybeClick = true;
      isDragging = false;
      dragStartX = dragPrevX = e.clientX;
      dragStartY = dragPrevY = e.clientY;
      dragStartTime = performance.now();
      triggerHeroModeCycle();
    };

    const onMouseMove = (e) => {
      updatePointerWorld(e.clientX, e.clientY);
      pointerActive = true;
      camTargetX = (e.clientX / width - 0.5) * 2;
      camTargetY = -(e.clientY / height - 0.5) * 2;
      lastInteractionTime = clock.getElapsedTime();

      // Detect drag threshold
      if (maybeClick) {
        if (Math.abs(e.clientX - dragStartX) > 4 || Math.abs(e.clientY - dragStartY) > 4) {
          maybeClick = false;
          isDragging = true;
        }
      }

      // Apply rotation during drag
      if (isDragging) {
        const dx = e.clientX - dragPrevX;
        const dy = e.clientY - dragPrevY;
        const sens = 0.004;
        group.rotation.y += dx * sens;
        group.rotation.x = Math.max(-1, Math.min(1, group.rotation.x + dy * sens));
        momentumY = momentumY * 0.5 + dx * sens * 0.5; // smooth
        momentumX = momentumX * 0.5 + dy * sens * 0.5;
        dragPrevX = e.clientX;
        dragPrevY = e.clientY;
      }
    };

    const onMouseUp = (e) => {
      if (maybeClick && performance.now() - dragStartTime < 250) {
        // Short click → trigger color pulse
        updatePointerWorld(e.clientX, e.clientY);
        shared.uClickPulseTime.value = clock.getElapsedTime();
        shared.uClickOrigin.value.set(pointerX, pointerY);
      }
      maybeClick = false;
      isDragging = false;
      lastInteractionTime = clock.getElapsedTime();
    };

    const onMouseLeave = () => {
      pointerActive = false;
      pointerX = pointerY = 99999;
      maybeClick = false;
      isDragging = false;
    };

    // ══════════════════════════════════════════════════════════════════════
    //  TOUCH EVENTS
    // ══════════════════════════════════════════════════════════════════════

    let touchId = null;

    const onTouchStart = (e) => {
      if (isInteractive(e) || e.touches.length !== 1) return;
      const t = e.touches[0];
      touchId = t.identifier;
      maybeClick = true;
      isDragging = false;
      dragStartX = dragPrevX = t.clientX;
      dragStartY = dragPrevY = t.clientY;
      dragStartTime = performance.now();
      updatePointerWorld(t.clientX, t.clientY);
      pointerActive = true;
    };

    const onTouchMove = (e) => {
      const t = Array.from(e.touches).find(tt => tt.identifier === touchId);
      if (!t) return;
      updatePointerWorld(t.clientX, t.clientY);
      pointerActive = true;
      lastInteractionTime = clock.getElapsedTime();

      if (maybeClick) {
        if (Math.abs(t.clientX - dragStartX) > 6 || Math.abs(t.clientY - dragStartY) > 6) {
          maybeClick = false;
          isDragging = true;
        }
      }

      if (isDragging) {
        const dx = t.clientX - dragPrevX;
        const dy = t.clientY - dragPrevY;
        const sens = 0.004;
        group.rotation.y += dx * sens;
        group.rotation.x = Math.max(-1, Math.min(1, group.rotation.x + dy * sens));
        momentumY = momentumY * 0.5 + dx * sens * 0.5;
        momentumX = momentumX * 0.5 + dy * sens * 0.5;
        dragPrevX = t.clientX;
        dragPrevY = t.clientY;
      }
    };

    const onTouchEnd = (e) => {
      if (!Array.from(e.touches).find(tt => tt.identifier === touchId)) {
        if (maybeClick && performance.now() - dragStartTime < 300) {
          shared.uClickPulseTime.value = clock.getElapsedTime();
          shared.uClickOrigin.value.set(pointerX, pointerY);
        }
        maybeClick = false;
        isDragging = false;
        pointerActive = false;
        pointerX = pointerY = 99999;
        touchId = null;
        lastInteractionTime = clock.getElapsedTime();
      }
    };

    const onScroll = () => { scrollY = window.scrollY; };

    // All listeners on window (hero section z-10 blocks canvas events)
    window.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    window.addEventListener('touchstart', onTouchStart, { passive: true });
    window.addEventListener('touchmove', onTouchMove, { passive: true });
    window.addEventListener('touchend', onTouchEnd);
    window.addEventListener('scroll', onScroll);

    const onResize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
      shared.uPixelRatio.value = renderer.getPixelRatio();
    };
    window.addEventListener('resize', onResize);

    // ══════════════════════════════════════════════════════════════════════
    //  ANIMATION LOOP — only uniform updates, no per-particle JS work
    // ══════════════════════════════════════════════════════════════════════
    // ── Animation loop ──
    let animId;
    // ── 5-Mode Intelligence Cycle Triggering ──
    let modeCycleActive = false;
    let modeCycleStartTime = 0;

    const triggerHeroModeCycle = () => {
      if (modeCycleActive) return;
      modeCycleActive = true;
      modeCycleStartTime = clock.getElapsedTime();
    };

    const handleInteractionTrigger = (e) => {
      if (!modeCycleActive && !isDragging) {
        triggerHeroModeCycle();
      }
    };

    window.addEventListener('doxa-trigger-logo-motion', triggerHeroModeCycle);

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const time = clock.getElapsedTime();
      const delta = Math.min(0.1, time - lastTime); // clamp delta to avoid huge jumps on tab background
      lastTime = time;

      // ── Drive 5-Mode Intelligence Cycle Uniform ──
      if (modeCycleActive) {
        const modeElapsed = time - modeCycleStartTime;
        const p = Math.min(modeElapsed / 2.2, 1.0);
        shared.uModeProgress.value = p;
        if (p >= 1.0) {
          modeCycleActive = false;
          shared.uModeProgress.value = 0.0;
        }
      } else {
        shared.uModeProgress.value = 0.0;
      }

      // ── Formation convergence ──
      if (shared.uFormation.value < 1) {
        shared.uFormation.value = Math.min(1, shared.uFormation.value + 0.006);
      }

      // ── Deform / reform / reverse / reset cycle logic (State Machine) ──
      const isResetting = (shared.uFormation.value > 0.95 && !isDragging && cycleState === STATE_RESETTING);

      if (shared.uFormation.value > 0.95) {
        if (isDragging) {
          // Reset to baseline and pause cycles while user is manually drag-rotating
          uDeformVal += (0.0 - uDeformVal) * 0.08;
          flowSpeed += (0.05 - flowSpeed) * 0.08;
          uDeformModeVal += (0.0 - uDeformModeVal) * 0.08;
          cycleState = STATE_FORMED;
          cycleStateTimer = 0.0;
        } else {
          // Advance state timer
          cycleStateTimer += delta;

          // Process state transitions and set uniforms/speeds
          switch (cycleState) {
            case STATE_FORMED:
              uDeformVal = 0.0;
              uDeformModeVal = 0.0;
              flowSpeed = 0.05;
              if (cycleStateTimer >= 3.0) {
                cycleState = STATE_DEFORMING_FORWARD;
                cycleStateTimer = 0.0;
              }
              break;

            case STATE_DEFORMING_FORWARD:
              uDeformModeVal = 0.0;
              flowSpeed = 0.05;
              {
                const t = Math.min(1.0, cycleStateTimer / 1.0);
                uDeformVal = t * t * (3.0 - 2.0 * t); // cubic ease-in-out
                if (cycleStateTimer >= 1.0) {
                  cycleState = STATE_HELD_FORWARD;
                  cycleStateTimer = 0.0;
                }
              }
              break;

            case STATE_HELD_FORWARD:
              uDeformVal = 1.0;
              uDeformModeVal = 0.0;
              flowSpeed = 0.05;
              if (cycleStateTimer >= 0.6) {
                cycleState = STATE_REFORMING_FORWARD;
                cycleStateTimer = 0.0;
              }
              break;

            case STATE_REFORMING_FORWARD:
              uDeformModeVal = 0.0;
              flowSpeed = 0.05;
              {
                const t = Math.min(1.0, cycleStateTimer / 1.0);
                uDeformVal = 1.0 - (t * t * (3.0 - 2.0 * t)); // cubic ease-in-out
                if (cycleStateTimer >= 1.0) {
                  cycleState = STATE_REVERSE_FLOW;
                  cycleStateTimer = 0.0;
                  startFlowOffset = flowOffset;
                }
              }
              break;

            case STATE_REVERSE_FLOW:
              uDeformVal = 0.0;
              uDeformModeVal = 0.0;
              // Reverse speed: -2.5 rad/s
              flowSpeed = -2.5;
              // Wait until flow offset completes exactly one full loop (2*PI radians) backward
              if (flowOffset <= startFlowOffset - 2.0 * Math.PI) {
                cycleState = STATE_RESETTING;
                cycleStateTimer = 0.0;
                // Capture current rotation states for fixed-duration eased reset
                resetStartRotX = group.rotation.x;
                resetStartRotY = group.rotation.y;
                // Target Y rotation is the nearest multiple of 2*PI (keeps front-facing)
                resetTargetRotY = Math.round(group.rotation.y / (Math.PI * 2)) * Math.PI * 2;
              }
              break;

            case STATE_RESETTING:
              uDeformVal = 0.0;
              uDeformModeVal = 0.0;
              flowSpeed = 0.05;
              {
                // Fixed duration reset: 2.0 seconds (visibly slower/smoother)
                const duration = 2.0;
                const t = Math.min(1.0, cycleStateTimer / duration);
                const ease = t * t * (3.0 - 2.0 * t); // cubic ease-in-out
                
                group.rotation.x = THREE.MathUtils.lerp(resetStartRotX, 0.0, ease);
                group.rotation.y = THREE.MathUtils.lerp(resetStartRotY, resetTargetRotY, ease);
                momentumX = 0;
                momentumY = 0;

                if (cycleStateTimer >= duration) {
                  // Normalize rotation to exactly 0 to avoid numeric drift
                  group.rotation.x = 0.0;
                  group.rotation.y = 0.0;
                  cycleState = STATE_DEFORMING_BACKWARD;
                  cycleStateTimer = 0.0;
                }
              }
              break;

            case STATE_DEFORMING_BACKWARD:
              uDeformModeVal = 1.0; // backward scatter mode
              flowSpeed = 0.05;
              {
                const t = Math.min(1.0, cycleStateTimer / 1.0);
                uDeformVal = t * t * (3.0 - 2.0 * t); // cubic ease-in-out
                if (cycleStateTimer >= 1.0) {
                  cycleState = STATE_HELD_BACKWARD;
                  cycleStateTimer = 0.0;
                }
              }
              break;

            case STATE_HELD_BACKWARD:
              uDeformVal = 1.0;
              uDeformModeVal = 1.0;
              flowSpeed = 0.05;
              if (cycleStateTimer >= 4.0) { // hold for 4 seconds as requested
                cycleState = STATE_REFORMING_BACKWARD;
                cycleStateTimer = 0.0;
              }
              break;

            case STATE_REFORMING_BACKWARD:
              uDeformModeVal = 1.0;
              flowSpeed = 0.05;
              {
                const t = Math.min(1.0, cycleStateTimer / 1.0);
                uDeformVal = 1.0 - (t * t * (3.0 - 2.0 * t)); // cubic ease-in-out
                if (cycleStateTimer >= 1.0) {
                  cycleState = STATE_FORMED;
                  cycleStateTimer = 0.0;
                  uDeformModeVal = 0.0;
                }
              }
              break;
          }
        }
      } else {
        uDeformVal = 0.0;
        flowSpeed = 0.05;
      }

      // Smoothly increment flow offset based on integrated flowSpeed
      flowOffset += flowSpeed * delta;
      shared.uFlowOffset.value = flowOffset;
      shared.uDeform.value = uDeformVal;
      shared.uDeformMode.value = uDeformModeVal;

      // ── Rotation: momentum + auto-rotation ──
      const timeSinceInteraction = time - lastInteractionTime;

      if (isDragging) {
        autoRotBlend = Math.max(0, autoRotBlend - 0.03);
      } else if (isResetting) {
        autoRotBlend = 0.0;
        momentumX = 0;
        momentumY = 0;
        // Smoothly straighten/reset rotation to original position/orientation
        group.rotation.x += (0.0 - group.rotation.x) * 0.06;
        group.rotation.y += (0.0 - group.rotation.y) * 0.06;
      } else {
        // Decay momentum
        momentumX *= 0.965;
        momentumY *= 0.965;
        if (Math.abs(momentumX) < 0.00001) momentumX = 0;
        if (Math.abs(momentumY) < 0.00001) momentumY = 0;
        group.rotation.y += momentumY;
        group.rotation.x += momentumX;
        group.rotation.x = Math.max(-1, Math.min(1, group.rotation.x));

        // Auto-rotation: fade in after 2.5s idle + near-zero momentum
        if (Math.abs(momentumY) < 0.0002 && Math.abs(momentumX) < 0.0002 && timeSinceInteraction > 2.5) {
          autoRotBlend = Math.min(1, autoRotBlend + 0.004);
        } else {
          autoRotBlend = Math.max(0, autoRotBlend - 0.01);
        }
      }
      // Gentle idle sway (rock back and forth gently, no continuous 360 spin)
      if (!isDragging && !isResetting) {
        const swayY = Math.sin(time * 0.25) * 0.1; // +/- 6 degrees
        const swayX = Math.cos(time * 0.2) * 0.05;  // +/- 3 degrees
        if (autoRotBlend > 0.001) {
          group.rotation.y = THREE.MathUtils.lerp(group.rotation.y, swayY, autoRotBlend * 0.03);
          group.rotation.x = THREE.MathUtils.lerp(group.rotation.x, swayX, autoRotBlend * 0.03);
        }
      }

      // ── Camera parallax (reduced during drag) ──
      if (!isDragging) {
        camX += (camTargetX - camX) * 0.03;
        camY += (camTargetY - camY) * 0.03;
      } else {
        camX += (0 - camX) * 0.05;
        camY += (0 - camY) * 0.05;
      }
      camera.position.x = camX * 8;
      camera.position.y = camY * 6 - scrollY * 0.02;
      camera.lookAt(0, 0, 0);

      // ── Update shared uniforms (both materials receive these) ──
      shared.uTime.value          = time;
      shared.uPointer.value.set(pointerX, pointerY);
      shared.uPointerActive.value = pointerActive ? 1 : 0;
      shared.uDragging.value      = isDragging ? 1 : 0;
      shared.uColorPhase.value    = (time * 0.667) % 5; // ~1.5s per palette

      // Fade out canvas opacity dynamically based on scroll position (fully transparent past hero height)
      const fadeOpacity = Math.max(0, Math.min(1, 1 - scrollY / (height * 0.85)));
      if (containerRef.current) {
        containerRef.current.style.opacity = fadeOpacity;
        // Turn off pointer events completely when faded out
        containerRef.current.style.pointerEvents = fadeOpacity > 0.05 ? 'auto' : 'none';
      }

      renderer.render(scene, camera);
    };

    animate();

    // ── Cleanup ──
    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      window.removeEventListener('touchstart', onTouchStart);
      window.removeEventListener('touchmove', onTouchMove);
      window.removeEventListener('touchend', onTouchEnd);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onResize);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      geometry.dispose();
      mainMaterial.dispose();
      bloomMaterial.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 z-0 overflow-hidden"
      style={{ pointerEvents: 'none' }}
      aria-hidden="true"
    />
  );
}
