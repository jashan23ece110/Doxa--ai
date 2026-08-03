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
    const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.z = 120;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    // Particle Count based on device
    const isMobile = width < 768;
    const count = isMobile ? 600 : 1800;

    // Positions, Colors, Sizes
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const scales = new Float32Array(count);
    const initialPositions = new Float32Array(count * 3);

    // Palette: Violet (#8b5cf6), Indigo (#6366f1), Cyan (#06b6d4), Soft White (#e2e8f0)
    const colorPalette = [
      new THREE.Color('#8b5cf6'),
      new THREE.Color('#6366f1'),
      new THREE.Color('#06b6d4'),
      new THREE.Color('#a855f7'),
      new THREE.Color('#38bdf8'),
    ];

    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      // Cylinder / stream distribution
      const radius = 20 + Math.random() * 140;
      const theta = Math.random() * Math.PI * 2;
      const z = (Math.random() - 0.5) * 300;

      const x = Math.cos(theta) * radius;
      const y = Math.sin(theta) * radius;

      positions[i3] = x;
      positions[i3 + 1] = y;
      positions[i3 + 2] = z;

      initialPositions[i3] = x;
      initialPositions[i3 + 1] = y;
      initialPositions[i3 + 2] = z;

      const color = colorPalette[Math.floor(Math.random() * colorPalette.length)];
      colors[i3] = color.r;
      colors[i3 + 1] = color.g;
      colors[i3 + 2] = color.b;

      scales[i] = Math.random() * 2.5 + 0.8;
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('scale', new THREE.BufferAttribute(scales, 1));

    // Particle Canvas Texture
    const particleCanvas = document.createElement('canvas');
    particleCanvas.width = 64;
    particleCanvas.height = 64;
    const ctx = particleCanvas.getContext('2d');
    const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
    grad.addColorStop(0.3, 'rgba(255, 255, 255, 0.8)');
    grad.addColorStop(0.6, 'rgba(255, 255, 255, 0.2)');
    grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 64, 64);
    const texture = new THREE.CanvasTexture(particleCanvas);

    const material = new THREE.PointsMaterial({
      size: 3.5,
      vertexColors: true,
      map: texture,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      opacity: 0.85
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Subtle ambient background ring mesh
    const ringGeo = new THREE.TorusGeometry(80, 0.4, 16, 100);
    const ringMat = new THREE.MeshBasicMaterial({
      color: new THREE.Color('#8b5cf6'),
      transparent: true,
      opacity: 0.15,
      wireframe: true
    });
    const torusRing = new THREE.Mesh(ringGeo, ringMat);
    torusRing.rotation.x = Math.PI / 3;
    scene.add(torusRing);

    // Mouse & Scroll Parallax
    let mouseX = 0;
    let mouseY = 0;
    let targetMouseX = 0;
    let targetMouseY = 0;
    let scrollY = 0;

    const handleMouseMove = (e) => {
      targetMouseX = (e.clientX / window.innerWidth - 0.5) * 2;
      targetMouseY = (e.clientY / window.innerHeight - 0.5) * 2;
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
    let clock = new THREE.Clock();
    let animId;

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Smooth mouse interpolation
      mouseX += (targetMouseX - mouseX) * 0.05;
      mouseY += (targetMouseY - mouseY) * 0.05;

      // Particle rotation & wobble
      particles.rotation.y = elapsedTime * 0.04 + mouseX * 0.2;
      particles.rotation.x = elapsedTime * 0.02 + mouseY * 0.15 + scrollY * 0.0003;

      torusRing.rotation.z = elapsedTime * 0.03;
      torusRing.rotation.y = mouseX * 0.3;

      const pos = geometry.attributes.position.array;
      for (let i = 0; i < count; i++) {
        const i3 = i * 3;
        // Subtle vertical oscillation
        pos[i3 + 1] = initialPositions[i3 + 1] + Math.sin(elapsedTime * 1.5 + i) * 3;
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
      className="fixed inset-0 pointer-events-none z-0 overflow-hidden opacity-90"
      aria-hidden="true"
    />
  );
}
