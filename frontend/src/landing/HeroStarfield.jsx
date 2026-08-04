import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

/**
 * HeroStarfield — dense, glowing particles forming the exact Doxa nested-rings
 * logo mark on a pure black background.
 *
 * Logo geometry (from the actual asset):
 *   • Outer ring  — large circle, centered at (0, +4)
 *   • Middle ring — medium circle, centered at (-3, -4)
 *   • Inner ring  — small circle, centered at (-5, -10)
 * All overlapping to create the cascading-orbit mark.
 *
 * No ambient/scatter particles. Pure black bg + logo rings only.
 * Dense, fine-grained, soft glow — Gemini-level visual quality.
 * Mouse + touch reactivity with proper z-index / pointer-events fix.
 */
export default function HeroStarfield() {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let width = window.innerWidth;
    let height = window.innerHeight;

    // ── Scene ──
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 500);
    camera.position.z = 100;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    renderer.setClearColor(0x000000, 0); // transparent — page bg is already black
    container.appendChild(renderer.domElement);

    const isMobile = width < 768;

    // ── Exact Doxa logo ring definitions ──
    // Measured from the logo.png asset — three circles, each offset
    // Coordinates in a normalized space; we'll scale to world units.
    // The logo mark spans roughly -60 to +60 world units in the viewport.
    const SCALE = 2.0; // world-unit multiplier

    const rings = [
      { cx:  0 * SCALE, cy:  4 * SCALE, r: 28 * SCALE, stroke: 2.8 * SCALE }, // outer
      { cx: -3 * SCALE, cy: -5 * SCALE, r: 19 * SCALE, stroke: 2.6 * SCALE }, // middle
      { cx: -5 * SCALE, cy: -12 * SCALE, r: 12 * SCALE, stroke: 2.4 * SCALE }, // inner
    ];

    // Ring colors: outer = cyan, middle = indigo, inner = violet (gradient across rings)
    const ringColorSets = [
      // outer ring: cyan → sky blue
      [new THREE.Color('#06b6d4'), new THREE.Color('#22d3ee'), new THREE.Color('#38bdf8')],
      // middle ring: indigo → violet
      [new THREE.Color('#6366f1'), new THREE.Color('#818cf8'), new THREE.Color('#8b5cf6')],
      // inner ring: violet → magenta
      [new THREE.Color('#8b5cf6'), new THREE.Color('#a855f7'), new THREE.Color('#c084fc')],
    ];

    // ── Particle generation ──
    // Dense: many particles per ring, distributed along the stroke width
    const PARTICLES_PER_RING = isMobile ? 1800 : 5000;
    const count = PARTICLES_PER_RING * rings.length;

    const positions    = new Float32Array(count * 3);
    const homePositions = new Float32Array(count * 3);
    const colors       = new Float32Array(count * 3);
    const phases       = new Float32Array(count); // per-particle noise phase
    const depthLayers  = new Float32Array(count); // z-depth randomization

    let idx = 0;

    for (let ri = 0; ri < rings.length; ri++) {
      const ring = rings[ri];
      const colorSet = ringColorSets[ri];

      for (let p = 0; p < PARTICLES_PER_RING; p++) {
        const angle = (p / PARTICLES_PER_RING) * Math.PI * 2 + (Math.random() - 0.5) * 0.015;

        // Distribute across the stroke width with gaussian-ish falloff
        // (more particles near center of stroke, fewer at edges → natural density)
        const strokeOffset = (Math.random() + Math.random() + Math.random()) / 3; // central tendency
        const r = ring.r + (strokeOffset - 0.5) * ring.stroke;

        const x = ring.cx + Math.cos(angle) * r;
        const y = ring.cy + Math.sin(angle) * r;
        const z = (Math.random() - 0.5) * 3;

        const i3 = idx * 3;
        homePositions[i3]     = x;
        homePositions[i3 + 1] = y;
        homePositions[i3 + 2] = z;

        // Start scattered, will converge
        positions[i3]     = x + (Math.random() - 0.5) * 250;
        positions[i3 + 1] = y + (Math.random() - 0.5) * 250;
        positions[i3 + 2] = z + (Math.random() - 0.5) * 80;

        // Color: pick from the ring's color set with slight variation
        const baseColor = colorSet[Math.floor(Math.random() * colorSet.length)].clone();
        // Add subtle brightness variation for organic feel
        const brightness = 0.65 + Math.random() * 0.5;
        baseColor.multiplyScalar(brightness);
        colors[i3]     = baseColor.r;
        colors[i3 + 1] = baseColor.g;
        colors[i3 + 2] = baseColor.b;

        phases[idx] = Math.random() * Math.PI * 2;
        depthLayers[idx] = z;

        idx++;
      }
    }

    // ── Geometry ──
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // ── Soft glow texture (higher res for smoother look) ──
    const texSize = 128;
    const glowCanvas = document.createElement('canvas');
    glowCanvas.width = texSize;
    glowCanvas.height = texSize;
    const gctx = glowCanvas.getContext('2d');
    const half = texSize / 2;
    const grad = gctx.createRadialGradient(half, half, 0, half, half, half);
    grad.addColorStop(0, 'rgba(255,255,255,1)');
    grad.addColorStop(0.12, 'rgba(255,255,255,0.9)');
    grad.addColorStop(0.3, 'rgba(255,255,255,0.45)');
    grad.addColorStop(0.55, 'rgba(255,255,255,0.12)');
    grad.addColorStop(1, 'rgba(255,255,255,0)');
    gctx.fillStyle = grad;
    gctx.fillRect(0, 0, texSize, texSize);
    const texture = new THREE.CanvasTexture(glowCanvas);

    const material = new THREE.PointsMaterial({
      size: isMobile ? 2.2 : 2.8,
      vertexColors: true,
      map: texture,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      opacity: 0.88,
    });

    const points = new THREE.Points(geometry, material);
    scene.add(points);

    // ── Bloom/glow post-processing layer ──
    // We add a second, larger, dimmer copy of the same particles for bloom halo
    const bloomMaterial = new THREE.PointsMaterial({
      size: isMobile ? 6.0 : 8.0,
      vertexColors: true,
      map: texture,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      opacity: 0.12,
    });
    const bloomPoints = new THREE.Points(geometry, bloomMaterial); // shares same geometry
    scene.add(bloomPoints);

    // ── Pointer / interaction state ──
    let pointerX = 99999;
    let pointerY = 99999;
    let pointerActive = false;

    // Camera parallax targets
    let camTargetX = 0;
    let camTargetY = 0;
    let camX = 0;
    let camY = 0;
    let scrollY = 0;

    const REPEL_RADIUS = isMobile ? 22 : 30;
    const REPEL_STRENGTH = isMobile ? 16 : 24;

    // Accurate screen → world conversion using the actual camera
    const raycaster = new THREE.Raycaster();
    const ndcVec = new THREE.Vector2();
    const worldPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0); // z=0 plane
    const worldIntersect = new THREE.Vector3();

    const updatePointerWorld = (clientX, clientY) => {
      // Use canvas bounding rect for correct coords (not window.innerWidth)
      const rect = renderer.domElement.getBoundingClientRect();
      ndcVec.x = ((clientX - rect.left) / rect.width) * 2 - 1;
      ndcVec.y = -((clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(ndcVec, camera);
      raycaster.ray.intersectPlane(worldPlane, worldIntersect);
      if (worldIntersect) {
        pointerX = worldIntersect.x;
        pointerY = worldIntersect.y;
      }
    };

    // ── Mouse events ──
    const onMouseMove = (e) => {
      updatePointerWorld(e.clientX, e.clientY);
      pointerActive = true;
      camTargetX = (e.clientX / width - 0.5) * 2;
      camTargetY = -(e.clientY / height - 0.5) * 2;
    };
    const onMouseLeave = () => {
      pointerActive = false;
      pointerX = 99999;
      pointerY = 99999;
    };

    // ── Touch events ──
    const onTouchStart = (e) => {
      if (e.touches.length > 0) {
        const t = e.touches[0];
        updatePointerWorld(t.clientX, t.clientY);
        pointerActive = true;
      }
    };
    const onTouchMove = (e) => {
      if (e.touches.length > 0) {
        const t = e.touches[0];
        updatePointerWorld(t.clientX, t.clientY);
        pointerActive = true;
        camTargetX = (t.clientX / width - 0.5) * 2;
        camTargetY = -(t.clientY / height - 0.5) * 2;
      }
    };
    const onTouchEnd = () => {
      pointerActive = false;
      pointerX = 99999;
      pointerY = 99999;
    };

    const onScroll = () => { scrollY = window.scrollY; };

    // ── Attach events to WINDOW (not canvas) to avoid z-index blocking ──
    // The hero section's z-10 div sits above the canvas, so canvas mouse events
    // never fire. Using window-level listeners ensures we always capture pointer.
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('scroll', onScroll);

    // Touch listeners on the container (these work because touch events
    // fire on the element under the finger, and bubbling handles the rest)
    // But for safety, also on window
    window.addEventListener('touchstart', onTouchStart, { passive: true });
    window.addEventListener('touchmove', onTouchMove, { passive: true });
    window.addEventListener('touchend', onTouchEnd);

    // ── Resize ──
    const onResize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    window.addEventListener('resize', onResize);

    // ── Formation convergence ──
    let formationT = 0;
    const FORMATION_SPEED = 0.008;

    // ── Animation loop ──
    const clock = new THREE.Clock();
    let animId;

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const time = clock.getElapsedTime();

      // Formation convergence (smoothstep)
      if (formationT < 1) {
        formationT = Math.min(1, formationT + FORMATION_SPEED);
      }
      const ease = formationT * formationT * (3 - 2 * formationT);

      // Smooth camera parallax
      camX += (camTargetX - camX) * 0.03;
      camY += (camTargetY - camY) * 0.03;
      camera.position.x = camX * 8;
      camera.position.y = camY * 6 - scrollY * 0.025;
      camera.lookAt(0, 0, 0);

      const pos = geometry.attributes.position.array;

      for (let i = 0; i < count; i++) {
        const i3 = i * 3;
        const phase = phases[i];

        // Gentle breathing noise around home position
        const breathAmp = 0.8;
        const breathX = Math.sin(time * 0.5 + phase) * breathAmp
                      + Math.sin(time * 0.23 + phase * 2.3) * breathAmp * 0.4;
        const breathY = Math.cos(time * 0.4 + phase * 1.7) * breathAmp
                      + Math.cos(time * 0.19 + phase * 3.1) * breathAmp * 0.4;
        const breathZ = Math.sin(time * 0.35 + phase * 0.8) * 0.4;

        let targetX = homePositions[i3]     + breathX;
        let targetY = homePositions[i3 + 1] + breathY;
        let targetZ = homePositions[i3 + 2] + breathZ;

        // ── Pointer repulsion ──
        if (pointerActive) {
          const dx = targetX - pointerX;
          const dy = targetY - pointerY;
          const distSq = dx * dx + dy * dy;
          const rr = REPEL_RADIUS * REPEL_RADIUS;
          if (distSq < rr && distSq > 0.01) {
            const dist = Math.sqrt(distSq);
            const force = 1 - dist / REPEL_RADIUS;
            const strength = force * force * force * REPEL_STRENGTH;
            targetX += (dx / dist) * strength;
            targetY += (dy / dist) * strength;
          }
        }

        // Lerp toward target
        const lerpRate = 0.04 + ease * 0.04;
        const formBlend = ease * 0.5 + 0.5; // at least 0.5 speed even at start

        pos[i3]     += (targetX - pos[i3])     * lerpRate * formBlend;
        pos[i3 + 1] += (targetY - pos[i3 + 1]) * lerpRate * formBlend;
        pos[i3 + 2] += (targetZ - pos[i3 + 2]) * lerpRate * formBlend;
      }

      geometry.attributes.position.needsUpdate = true;
      renderer.render(scene, camera);
    };

    animate();

    // ── Cleanup ──
    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('touchstart', onTouchStart);
      window.removeEventListener('touchmove', onTouchMove);
      window.removeEventListener('touchend', onTouchEnd);
      window.removeEventListener('resize', onResize);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      geometry.dispose();
      material.dispose();
      bloomMaterial.dispose();
      texture.dispose();
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
