import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function HeroStarfield() {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let width = window.innerWidth;
    let height = window.innerHeight;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    camera.position.z = 110;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    const isMobile = width < 768;
    const count = isMobile ? 1200 : 3200;

    // Attribute buffers
    const positions = new Float32Array(count * 3);
    const initialPositions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const scales = new Float32Array(count);
    const speeds = new Float32Array(count);
    const angles = new Float32Array(count);
    const radii = new Float32Array(count);
    const layerTypes = new Float32Array(count); // 0 = orbital ring, 1 = logarithmic spiral, 2 = ambient halo

    // Doxa Color Palette: Violet (#8b5cf6), Indigo (#6366f1), Cyan (#06b6d4), Neon Magenta (#d946ef), Soft White (#f8fafc)
    const palette = [
      new THREE.Color('#8b5cf6'),
      new THREE.Color('#6366f1'),
      new THREE.Color('#06b6d4'),
      new THREE.Color('#38bdf8'),
      new THREE.Color('#d946ef'),
      new THREE.Color('#a855f7'),
    ];

    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      const layer = i % 3; // 0, 1, or 2
      layerTypes[i] = layer;

      let x = 0, y = 0, z = 0;
      let r = 0, angle = 0;

      if (layer === 0) {
        // Concentric Orbital Ring / Nested Arc Formation
        r = 25 + Math.random() * 85;
        angle = Math.random() * Math.PI * 2;
        x = Math.cos(angle) * r;
        y = Math.sin(angle) * r * 0.65; // Elliptical arc
        z = (Math.random() - 0.5) * 60;
      } else if (layer === 1) {
        // Logarithmic Energy Wave Arc
        angle = Math.random() * Math.PI * 3;
        r = 15 + Math.pow(angle, 1.4) * 8;
        x = Math.cos(angle) * r - 20;
        y = Math.sin(angle) * r * 0.8;
        z = (Math.random() - 0.5) * 100;
      } else {
        // Deep 3D Ambient Energy Field
        r = 30 + Math.random() * 160;
        angle = Math.random() * Math.PI * 2;
        x = (Math.random() - 0.5) * 280;
        y = (Math.random() - 0.5) * 200;
        z = (Math.random() - 0.5) * 220;
      }

      positions[i3] = x;
      positions[i3 + 1] = y;
      positions[i3 + 2] = z;

      initialPositions[i3] = x;
      initialPositions[i3 + 1] = y;
      initialPositions[i3 + 2] = z;

      radii[i] = r;
      angles[i] = angle;
      speeds[i] = 0.003 + Math.random() * 0.008;

      // Color mapping
      const color = palette[Math.floor(Math.random() * palette.length)];
      colors[i3] = color.r;
      colors[i3 + 1] = color.g;
      colors[i3 + 2] = color.b;

      // Particle scale (layered depth)
      scales[i] = layer === 0 ? (Math.random() * 2.5 + 1.2) : (Math.random() * 1.8 + 0.8);
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('scale', new THREE.BufferAttribute(scales, 1));

    // Glow Canvas Texture
    const particleCanvas = document.createElement('canvas');
    particleCanvas.width = 64;
    particleCanvas.height = 64;
    const ctx = particleCanvas.getContext('2d');
    const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
    grad.addColorStop(0.25, 'rgba(255, 255, 255, 0.85)');
    grad.addColorStop(0.5, 'rgba(255, 255, 255, 0.3)');
    grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 64, 64);
    const texture = new THREE.CanvasTexture(particleCanvas);

    const material = new THREE.PointsMaterial({
      size: 4.2,
      vertexColors: true,
      map: texture,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      opacity: 0.9
    });

    const particleSystem = new THREE.Points(geometry, material);
    scene.add(particleSystem);

    // Decorative Geometric Orbital Arc Rings
    const ringGeo1 = new THREE.TorusGeometry(55, 0.3, 16, 120);
    const ringMat1 = new THREE.MeshBasicMaterial({
      color: new THREE.Color('#8b5cf6'),
      transparent: true,
      opacity: 0.22,
      wireframe: true
    });
    const ring1 = new THREE.Mesh(ringGeo1, ringMat1);
    ring1.rotation.x = Math.PI / 2.8;
    scene.add(ring1);

    const ringGeo2 = new THREE.TorusGeometry(85, 0.2, 16, 140);
    const ringMat2 = new THREE.MeshBasicMaterial({
      color: new THREE.Color('#06b6d4'),
      transparent: true,
      opacity: 0.15,
      wireframe: true
    });
    const ring2 = new THREE.Mesh(ringGeo2, ringMat2);
    ring2.rotation.y = Math.PI / 3.5;
    scene.add(ring2);

    // Interaction State
    let targetMouseX = 0;
    let targetMouseY = 0;
    let mouseX = 0;
    let mouseY = 0;
    let scrollY = 0;

    const handleMouseMove = (e) => {
      targetMouseX = (e.clientX / window.innerWidth - 0.5) * 2;
      targetMouseY = -(e.clientY / window.innerHeight - 0.5) * 2;
    };

    const handleScroll = () => {
      scrollY = window.scrollY;
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('scroll', handleScroll);

    const handleResize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    window.addEventListener('resize', handleResize);

    // Animation Loop
    const clock = new THREE.Clock();
    let animId;

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const time = clock.getElapsedTime();

      // Smooth mouse lerp
      mouseX += (targetMouseX - mouseX) * 0.06;
      mouseY += (targetMouseY - mouseY) * 0.06;

      // Camera parallax
      camera.position.x = mouseX * 15;
      camera.position.y = mouseY * 15 + scrollY * -0.04;
      camera.lookAt(0, 0, 0);

      // Ring rotations
      ring1.rotation.z = time * 0.05;
      ring1.rotation.y = mouseX * 0.3;
      ring2.rotation.x = time * 0.03 + mouseY * 0.2;

      // Particle Flow Field & Mouse Repulsion
      const pos = geometry.attributes.position.array;

      for (let i = 0; i < count; i++) {
        const i3 = i * 3;
        const layer = layerTypes[i];
        const spd = speeds[i];

        angles[i] += spd;
        const ang = angles[i];

        if (layer === 0) {
          // Orbital Ellipse Flow
          const r = radii[i] + Math.sin(time * 1.2 + i) * 3;
          const currX = Math.cos(ang) * r;
          const currY = Math.sin(ang) * r * 0.65;
          const currZ = initialPositions[i3 + 2] + Math.sin(time * 0.8 + ang) * 5;

          // Mouse Repulsion deflection
          const dx = currX - (mouseX * 50);
          const dy = currY - (mouseY * 50);
          const dist = Math.sqrt(dx * dx + dy * dy);

          let pushX = 0, pushY = 0;
          if (dist < 45) {
            const force = (45 - dist) / 45;
            pushX = (dx / dist) * force * 15;
            pushY = (dy / dist) * force * 15;
          }

          pos[i3] = currX + pushX;
          pos[i3 + 1] = currY + pushY;
          pos[i3 + 2] = currZ;
        } else if (layer === 1) {
          // Logarithmic Energy Spiral Wave
          const r = radii[i] + Math.cos(time * 1.5 + ang) * 6;
          const currX = Math.cos(ang) * r - 20;
          const currY = Math.sin(ang) * r * 0.8;
          const currZ = initialPositions[i3 + 2] + Math.cos(time + i) * 8;

          pos[i3] = currX;
          pos[i3 + 1] = currY;
          pos[i3 + 2] = currZ;
        } else {
          // Ambient Particle Oscillation & Scroll Drift
          pos[i3 + 1] = initialPositions[i3 + 1] + Math.sin(time * 1.2 + i) * 4;
          pos[i3] = initialPositions[i3] + Math.cos(time * 0.8 + i) * 4;
        }
      }

      geometry.attributes.position.needsUpdate = true;

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleResize);
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
      className="fixed inset-0 pointer-events-none z-0 overflow-hidden opacity-95"
      aria-hidden="true"
    />
  );
}
