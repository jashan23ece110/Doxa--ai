import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

/**
 * HeroStarfield — particles form the Doxa nested-rings logo mark.
 *
 * The logo is 3 concentric rings (radii ~18, 32, 48 in world units)
 * plus a bright core dot cluster at center.
 * Particles drift/breathe gently around the formation and react to
 * mouse (desktop) and touch (mobile) via repulsion.
 */
export default function HeroStarfield() {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let width = window.innerWidth;
    let height = window.innerHeight;

    // ── Scene setup ──
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    camera.position.z = 120;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    // ── Performance-adaptive particle counts ──
    const isMobile = width < 768;
    const LOGO_COUNT = isMobile ? 600 : 1600;     // particles on logo rings
    const AMBIENT_COUNT = isMobile ? 300 : 800;    // scattered ambient particles
    const CORE_COUNT = isMobile ? 40 : 100;        // bright center cluster
    const count = LOGO_COUNT + AMBIENT_COUNT + CORE_COUNT;

    // ── Logo ring geometry ──
    // 3 concentric rings at these radii in world units
    const RING_RADII = [18, 32, 48];
    const RING_THICKNESS = 1.2; // how much jitter off the ring path

    // ── Doxa color palette ──
    const violet = new THREE.Color('#8b5cf6');
    const indigo = new THREE.Color('#6366f1');
    const cyan   = new THREE.Color('#06b6d4');
    const skyBlue = new THREE.Color('#38bdf8');
    const magenta = new THREE.Color('#a855f7');
    const coreWhite = new THREE.Color('#e0e7ff');

    // ── Buffers ──
    const positions   = new Float32Array(count * 3);
    const homePositions = new Float32Array(count * 3); // where particles want to be
    const colors      = new Float32Array(count * 3);
    const sizes       = new Float32Array(count);
    const phaseOffsets = new Float32Array(count); // per-particle animation phase

    // Ring color mapping: inner ring = violet, middle = indigo, outer = cyan
    const ringColors = [
      [violet, magenta],    // inner ring
      [indigo, violet],     // middle ring
      [cyan, skyBlue],      // outer ring
    ];

    let idx = 0;

    // ── 1. Logo ring particles ──
    const particlesPerRing = Math.floor(LOGO_COUNT / RING_RADII.length);
    for (let ring = 0; ring < RING_RADII.length; ring++) {
      const r = RING_RADII[ring];
      const colorPair = ringColors[ring];
      for (let p = 0; p < particlesPerRing; p++) {
        const angle = (p / particlesPerRing) * Math.PI * 2 + (Math.random() - 0.5) * 0.04;
        const jitterR = r + (Math.random() - 0.5) * RING_THICKNESS;
        const x = Math.cos(angle) * jitterR;
        const y = Math.sin(angle) * jitterR;
        const z = (Math.random() - 0.5) * 4; // slight depth

        const i3 = idx * 3;
        homePositions[i3]     = x;
        homePositions[i3 + 1] = y;
        homePositions[i3 + 2] = z;
        positions[i3]     = x + (Math.random() - 0.5) * 200; // start scattered
        positions[i3 + 1] = y + (Math.random() - 0.5) * 200;
        positions[i3 + 2] = z + (Math.random() - 0.5) * 100;

        const color = colorPair[Math.random() > 0.5 ? 0 : 1].clone();
        // Slight brightness variation
        color.multiplyScalar(0.7 + Math.random() * 0.5);
        colors[i3]     = color.r;
        colors[i3 + 1] = color.g;
        colors[i3 + 2] = color.b;

        sizes[idx] = ring === 0 ? 3.0 + Math.random() * 1.5
                   : ring === 1 ? 2.5 + Math.random() * 1.2
                   : 2.0 + Math.random() * 1.0;
        phaseOffsets[idx] = Math.random() * Math.PI * 2;
        idx++;
      }
    }

    // ── 2. Ambient scattered particles ──
    const ambientColors = [violet, indigo, cyan, skyBlue, magenta];
    for (let p = 0; p < AMBIENT_COUNT; p++) {
      const x = (Math.random() - 0.5) * 280;
      const y = (Math.random() - 0.5) * 200;
      const z = (Math.random() - 0.5) * 160;

      const i3 = idx * 3;
      homePositions[i3]     = x;
      homePositions[i3 + 1] = y;
      homePositions[i3 + 2] = z;
      positions[i3]     = x;
      positions[i3 + 1] = y;
      positions[i3 + 2] = z;

      const color = ambientColors[Math.floor(Math.random() * ambientColors.length)].clone();
      color.multiplyScalar(0.3 + Math.random() * 0.4);
      colors[i3]     = color.r;
      colors[i3 + 1] = color.g;
      colors[i3 + 2] = color.b;

      sizes[idx] = 1.0 + Math.random() * 1.5;
      phaseOffsets[idx] = Math.random() * Math.PI * 2;
      idx++;
    }

    // ── 3. Bright core cluster ──
    for (let p = 0; p < CORE_COUNT; p++) {
      const angle = Math.random() * Math.PI * 2;
      const r = Math.random() * 6;
      const x = Math.cos(angle) * r;
      const y = Math.sin(angle) * r;
      const z = (Math.random() - 0.5) * 3;

      const i3 = idx * 3;
      homePositions[i3]     = x;
      homePositions[i3 + 1] = y;
      homePositions[i3 + 2] = z;
      positions[i3]     = x + (Math.random() - 0.5) * 150;
      positions[i3 + 1] = y + (Math.random() - 0.5) * 150;
      positions[i3 + 2] = z + (Math.random() - 0.5) * 80;

      const color = coreWhite.clone().lerp(violet, Math.random() * 0.3);
      colors[i3]     = color.r;
      colors[i3 + 1] = color.g;
      colors[i3 + 2] = color.b;

      sizes[idx] = 3.5 + Math.random() * 2.5;
      phaseOffsets[idx] = Math.random() * Math.PI * 2;
      idx++;
    }

    // ── Geometry ──
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // ── Glow texture ──
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');
    const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    grad.addColorStop(0, 'rgba(255,255,255,1)');
    grad.addColorStop(0.2, 'rgba(255,255,255,0.85)');
    grad.addColorStop(0.5, 'rgba(255,255,255,0.3)');
    grad.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 64, 64);
    const texture = new THREE.CanvasTexture(canvas);

    const material = new THREE.PointsMaterial({
      size: isMobile ? 3.0 : 3.8,
      vertexColors: true,
      map: texture,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      opacity: 0.92,
    });

    const points = new THREE.Points(geometry, material);
    scene.add(points);

    // ── Interaction state ──
    // Pointer position in normalized world-ish coordinates for repulsion calc
    let pointerWorldX = 9999; // off-screen initially
    let pointerWorldY = 9999;
    let pointerActive = false;
    let scrollY = 0;

    // Smooth camera parallax targets
    let camTargetX = 0;
    let camTargetY = 0;
    let camX = 0;
    let camY = 0;

    const REPEL_RADIUS = isMobile ? 28 : 35;   // world units
    const REPEL_STRENGTH = isMobile ? 18 : 22;  // max push distance

    // Convert screen coords to approximate world coords at z=0
    const screenToWorld = (clientX, clientY) => {
      const ndcX = (clientX / width) * 2 - 1;
      const ndcY = -(clientY / height) * 2 + 1;
      // At camera.position.z=120, fov=55, approximate world coords:
      const halfH = Math.tan(THREE.MathUtils.degToRad(55 / 2)) * 120;
      const halfW = halfH * (width / height);
      return {
        x: ndcX * halfW,
        y: ndcY * halfH,
      };
    };

    // ── Mouse events (desktop) ──
    const onMouseMove = (e) => {
      const w = screenToWorld(e.clientX, e.clientY);
      pointerWorldX = w.x;
      pointerWorldY = w.y;
      pointerActive = true;
      camTargetX = (e.clientX / width - 0.5) * 2;
      camTargetY = -(e.clientY / height - 0.5) * 2;
    };
    const onMouseLeave = () => {
      pointerActive = false;
      pointerWorldX = 9999;
      pointerWorldY = 9999;
    };

    // ── Touch events (mobile) ──
    const onTouchMove = (e) => {
      if (e.touches.length > 0) {
        const t = e.touches[0];
        const w = screenToWorld(t.clientX, t.clientY);
        pointerWorldX = w.x;
        pointerWorldY = w.y;
        pointerActive = true;
        camTargetX = (t.clientX / width - 0.5) * 2;
        camTargetY = -(t.clientY / height - 0.5) * 2;
      }
    };
    const onTouchStart = (e) => {
      onTouchMove(e); // activate on first touch
    };
    const onTouchEnd = () => {
      pointerActive = false;
      pointerWorldX = 9999;
      pointerWorldY = 9999;
    };

    const onScroll = () => { scrollY = window.scrollY; };

    // Attach to the renderer's canvas so pointer-events work
    const domEl = renderer.domElement;
    domEl.style.pointerEvents = 'auto';
    domEl.style.touchAction = 'pan-y'; // allow page scroll but capture touch-move

    domEl.addEventListener('mousemove', onMouseMove);
    domEl.addEventListener('mouseleave', onMouseLeave);
    domEl.addEventListener('touchstart', onTouchStart, { passive: true });
    domEl.addEventListener('touchmove', onTouchMove, { passive: true });
    domEl.addEventListener('touchend', onTouchEnd);
    window.addEventListener('scroll', onScroll);

    // ── Resize ──
    const onResize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    window.addEventListener('resize', onResize);

    // ── Formation lerp progress (0 = scattered, 1 = formed) ──
    let formationProgress = 0;
    const FORMATION_SPEED = 0.012; // how fast particles converge on mount

    // ── Animation loop ──
    const clock = new THREE.Clock();
    let animId;

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const time = clock.getElapsedTime();

      // Converge toward formation over time
      if (formationProgress < 1) {
        formationProgress = Math.min(1, formationProgress + FORMATION_SPEED);
      }
      const ease = formationProgress * formationProgress * (3 - 2 * formationProgress); // smoothstep

      // Smooth camera parallax
      camX += (camTargetX - camX) * 0.04;
      camY += (camTargetY - camY) * 0.04;
      camera.position.x = camX * 10;
      camera.position.y = camY * 8 - scrollY * 0.03;
      camera.lookAt(0, 0, 0);

      const pos = geometry.attributes.position.array;

      for (let i = 0; i < count; i++) {
        const i3 = i * 3;
        const phase = phaseOffsets[i];

        // Target position = home + gentle breathing noise
        const breathX = Math.sin(time * 0.6 + phase) * 1.2
                      + Math.sin(time * 0.3 + phase * 2.7) * 0.6;
        const breathY = Math.cos(time * 0.5 + phase * 1.3) * 1.2
                      + Math.cos(time * 0.25 + phase * 3.1) * 0.6;
        const breathZ = Math.sin(time * 0.4 + phase * 0.9) * 0.8;

        let targetX = homePositions[i3]     + breathX;
        let targetY = homePositions[i3 + 1] + breathY;
        let targetZ = homePositions[i3 + 2] + breathZ;

        // ── Pointer repulsion ──
        if (pointerActive) {
          const dx = targetX - pointerWorldX;
          const dy = targetY - pointerWorldY;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < REPEL_RADIUS && dist > 0.1) {
            const force = 1 - dist / REPEL_RADIUS;
            // Cubic falloff for smoother feel
            const strength = force * force * force * REPEL_STRENGTH;
            targetX += (dx / dist) * strength;
            targetY += (dy / dist) * strength;
          }
        }

        // Lerp current position toward target
        // Logo/core particles lerp faster when forming, ambient always at home
        const isLogo = i < LOGO_COUNT + CORE_COUNT;
        const lerpSpeed = isLogo ? 0.03 + ease * 0.05 : 0.02;

        // During formation, blend between scattered start and target
        const formTarget = ease;
        pos[i3]     += (targetX - pos[i3])     * lerpSpeed * (isLogo ? formTarget + 0.5 : 1);
        pos[i3 + 1] += (targetY - pos[i3 + 1]) * lerpSpeed * (isLogo ? formTarget + 0.5 : 1);
        pos[i3 + 2] += (targetZ - pos[i3 + 2]) * lerpSpeed * (isLogo ? formTarget + 0.5 : 1);
      }

      geometry.attributes.position.needsUpdate = true;
      renderer.render(scene, camera);
    };

    animate();

    // ── Cleanup ──
    return () => {
      cancelAnimationFrame(animId);
      domEl.removeEventListener('mousemove', onMouseMove);
      domEl.removeEventListener('mouseleave', onMouseLeave);
      domEl.removeEventListener('touchstart', onTouchStart);
      domEl.removeEventListener('touchmove', onTouchMove);
      domEl.removeEventListener('touchend', onTouchEnd);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onResize);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      geometry.dispose();
      material.dispose();
      texture.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 z-0 overflow-hidden opacity-95"
      aria-hidden="true"
    />
  );
}
