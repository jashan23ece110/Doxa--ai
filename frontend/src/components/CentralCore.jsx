import React, { useRef, useMemo, useEffect, useState } from 'react';
import { Canvas, useFrame, extend, useThree } from '@react-three/fiber';
import { Effects } from '@react-three/drei';
import { UnrealBloomPass } from 'three-stdlib';
import * as THREE from 'three';
import { motion } from 'framer-motion';

extend({ UnrealBloomPass });

function ParticleSwarm({ isActive, isThinking, isSpeaking, count, themeName = 'ultron' }) {
  const meshRef = useRef();
  const lineMeshRef = useRef();
  const { camera, pointer, raycaster, gl } = useThree();
  
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const target = useMemo(() => new THREE.Vector3(), []);
  const pColor = useMemo(() => new THREE.Color(), []);
  
  // Shockwave tracking ref
  const shockwave = useRef({ active: false, time: 0 });

  // Add direct canvas click listener to trigger shockwave
  useEffect(() => {
    const handleCanvasClick = () => {
      shockwave.current.active = true;
      shockwave.current.time = 0;
    };
    const canvasEl = gl.domElement;
    canvasEl.addEventListener('pointerdown', handleCanvasClick);
    return () => canvasEl.removeEventListener('pointerdown', handleCanvasClick);
  }, [gl]);

  // Precomputed positions list for lerping
  const positions = useMemo(() => {
    const pos = [];
    for (let i = 0; i < count; i++) {
      pos.push(new THREE.Vector3(
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10
      ));
    }
    return pos;
  }, [count]);

  // Precompute phi and theta values (Fibonacci spiral distribution)
  const phiTheta = useMemo(() => {
    const arr = new Float32Array(count * 2);
    const tau = 6.28318530718;
    for (let i = 0; i < count; i++) {
      const f = i / count;
      arr[i * 2] = Math.acos(1.0 - 2.0 * f); // phi
      arr[i * 2 + 1] = tau * f * 89.0; // theta
    }
    return arr;
  }, [count]);

  // Occasional constellation connections (select first 120 nodes)
  const connectionPairs = useMemo(() => {
    const pairs = [];
    const maxParticles = Math.min(count, 120);
    for (let i = 0; i < maxParticles; i++) {
      const numConns = Math.floor(Math.random() * 2) + 1; // 1 or 2 connections per node
      for (let c = 0; c < numConns; c++) {
        const targetIdx = Math.floor(Math.random() * maxParticles);
        if (targetIdx !== i && !pairs.some(p => (p[0] === i && p[1] === targetIdx) || (p[0] === targetIdx && p[1] === i))) {
          pairs.push([i, targetIdx]);
        }
      }
    }
    return pairs;
  }, [count]);

  // Vertex array for drawing lines
  const linePositions = useMemo(() => {
    return new Float32Array(connectionPairs.length * 2 * 3);
  }, [connectionPairs]);

  const lineGeometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    return geo;
  }, [linePositions]);

  const lineMaterial = useMemo(() => {
    const accentColor = themeName === 'aether' ? '#00d9ff' : 'var(--jarvis-accent)';
    return new THREE.LineBasicMaterial({
      color: new THREE.Color(accentColor),
      transparent: true,
      opacity: 0.1,
      blending: THREE.AdditiveBlending,
      linewidth: 1
    });
  }, [themeName]);

  const geometry = useMemo(() => new THREE.TetrahedronGeometry(0.24), []);
  const material = useMemo(() => new THREE.MeshBasicMaterial({ color: 0xffffff }), []);

  // Morphable simulation parameters
  const currentParams = useRef({
    radius: 22,
    turbulence: 3.5,
    pulse: 2.5,
    speed: 0.3,
    swirl: 1.5,
    colorIntensity: 0.5
  });

  useFrame((state, delta) => {
    if (!meshRef.current) return;
    const time = state.clock.getElapsedTime();

    // Rotate the whole mesh slowly for ambient rotation
    meshRef.current.rotation.y = time * 0.04;
    meshRef.current.rotation.x = Math.sin(time * 0.015) * 0.08;

    // Define target parameters based on active state
    let targetRadius = 22;
    let targetTurbulence = 3.5;
    let targetPulse = 2.5;
    let targetSpeed = 0.3;
    let targetSwirl = 1.5;
    let targetColorIntensity = 0.55;

    // Voice envelope simulation (syllable frequency ~4Hz + intonation jitter ~18Hz)
    let speechEnvelope = 0.1;
    if (isSpeaking) {
      const syllableWave = Math.sin(time * 3.8 * Math.PI * 2);
      const intonationWave = Math.sin(time * 18.0);
      speechEnvelope = (syllableWave * 0.55 + intonationWave * 0.15 + 0.45);
      speechEnvelope = Math.max(0.05, Math.min(1.0, speechEnvelope));
    }

    if (isThinking) {
      targetRadius = 45;
      targetTurbulence = 16.5;
      targetPulse = 11;
      targetSpeed = 1.7;
      targetSwirl = 7.0;
      targetColorIntensity = 1.0;
    } else if (isSpeaking) {
      // Dynamic voice reactive envelope
      targetRadius = 32.5 + speechEnvelope * 10.0;
      targetTurbulence = 9.0;
      targetPulse = 4.0 + speechEnvelope * 11.0;
      targetSpeed = 1.05;
      targetSwirl = 4.5;
      targetColorIntensity = 0.85 + speechEnvelope * 0.15;
    } else if (isActive) {
      targetRadius = 30;
      targetTurbulence = 7;
      targetPulse = 4;
      targetSpeed = 0.8;
      targetSwirl = 2.5;
      targetColorIntensity = 0.75;
    }

    // Smooth transition between parameters (easing/lerp took ~0.8s)
    const lerpFactor = 1 - Math.exp(-2.8 * delta);
    currentParams.current.radius = THREE.MathUtils.lerp(currentParams.current.radius, targetRadius, lerpFactor);
    currentParams.current.turbulence = THREE.MathUtils.lerp(currentParams.current.turbulence, targetTurbulence, lerpFactor);
    currentParams.current.pulse = THREE.MathUtils.lerp(currentParams.current.pulse, targetPulse, lerpFactor);
    currentParams.current.speed = THREE.MathUtils.lerp(currentParams.current.speed, targetSpeed, lerpFactor);
    currentParams.current.swirl = THREE.MathUtils.lerp(currentParams.current.swirl, targetSwirl, lerpFactor);
    currentParams.current.colorIntensity = THREE.MathUtils.lerp(currentParams.current.colorIntensity, targetColorIntensity, lerpFactor);

    const radius = currentParams.current.radius;
    const turbulence = currentParams.current.turbulence;
    const pulse = currentParams.current.pulse;
    const speed = currentParams.current.speed;
    const swirl = currentParams.current.swirl;
    const intensity = currentParams.current.colorIntensity;

    const t = time * speed;
    const tau = 6.28318530718;

    // Cursor interaction: project cursor in XY plane at z=0
    raycaster.setFromCamera(pointer, camera);
    const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    const cursor = new THREE.Vector3();
    raycaster.ray.intersectPlane(plane, cursor);

    // Update shockwave time progress
    if (shockwave.current.active) {
      shockwave.current.time += delta * 45.0; // speed of shockwave propagation
      if (shockwave.current.time > 95.0) {
        shockwave.current.active = false;
      }
    }

    for (let i = 0; i < count; i++) {
      const phi = phiTheta[i * 2];
      const theta = phiTheta[i * 2 + 1];

      // Organic noises mapping using trigonometric wave sums
      const noise1 = Math.sin(phi * 3.5 + t) * Math.cos(theta * 2.2 + t);
      const noise2 = Math.cos(phi * 1.5 - t) * Math.sin(theta * 4.4 + t);
      const noise3 = Math.sin(phi * 8.0 + t * 2) * Math.cos(theta * 5.0 - t);

      // Distortions: pull coordinates from fibonacci grid
      const dRadius = radius + noise1 * turbulence + Math.sin(time * 2.5 + phi * 10.0) * pulse;
      const dTheta = theta + noise2 * swirl;

      let x = dRadius * Math.sin(phi) * Math.cos(dTheta);
      let y = dRadius * Math.sin(phi) * Math.sin(dTheta);
      let z = dRadius * Math.cos(phi);

      // Cursor hover repulsion effect (within threshold ~22px)
      const pPos = positions[i];
      const distToCursor = cursor.distanceTo(pPos);
      if (distToCursor < 22.0) {
        const force = (1.0 - distToCursor / 22.0) * 8.0;
        const dir = new THREE.Vector3().subVectors(pPos, cursor).normalize();
        x += dir.x * force;
        y += dir.y * force;
        z += dir.z * force;
      }

      // Dynamic shockwave ring expansion on click
      if (shockwave.current.active) {
        const waveRadius = shockwave.current.time;
        const pDist = pPos.length();
        const distToWave = Math.abs(pDist - waveRadius);
        const waveWidth = 5.5;

        if (distToWave < waveWidth && pDist > 0.1) {
          const strength = (1.0 - distToWave / waveWidth) * 22.0 * Math.max(0, 1 - waveRadius / 95.0);
          x += (x / pDist) * strength;
          y += (y / pDist) * strength;
          z += (z / pDist) * strength;
        }
      }

      target.set(x, y, z);
      positions[i].lerp(target, 0.14);

      dummy.position.copy(positions[i]);
      dummy.updateMatrix();
      meshRef.current.setMatrixAt(i, dummy.matrix);

      // Smooth color states morphing based on active theme
      const heat = Math.abs(noise1 * 0.5 + noise2 * 0.5);
      let hue, saturation, lightness;
      
      if (themeName === 'aether') {
        hue = 0.52 + heat * 0.12; // cyan-blue holographic
        saturation = 0.90 - heat * 0.10;
        lightness = (0.35 + heat * 0.35) * intensity;
      } else {
        // ultron crimson red
        hue = 0.95 + heat * 0.11; // crimson-red to orange-red
        saturation = 0.95 - heat * 0.15;
        lightness = (0.28 + heat * 0.32) * intensity + Math.abs(noise3) * 0.12 * intensity;
      }

      pColor.setHSL(hue, saturation, lightness);
      meshRef.current.setColorAt(i, pColor);
    }

    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) {
      meshRef.current.instanceColor.needsUpdate = true;
    }

    // Update constellation connecting lines
    if (lineMeshRef.current) {
      const posAttr = lineMeshRef.current.geometry.attributes.position;
      let ptr = 0;

      let targetOpacity = 0.08;
      if (isThinking) targetOpacity = 0.45;
      else if (isActive) targetOpacity = 0.20;

      lineMeshRef.current.material.opacity = THREE.MathUtils.lerp(
        lineMeshRef.current.material.opacity,
        targetOpacity,
        lerpFactor
      );

      for (let i = 0; i < connectionPairs.length; i++) {
        const [p1Idx, p2Idx] = connectionPairs[i];
        const p1 = positions[p1Idx];
        const p2 = positions[p2Idx];

        const dist = p1.distanceTo(p2);
        const maxDist = isThinking ? 60 : 35;

        if (dist < maxDist) {
          linePositions[ptr++] = p1.x;
          linePositions[ptr++] = p1.y;
          linePositions[ptr++] = p1.z;
          
          linePositions[ptr++] = p2.x;
          linePositions[ptr++] = p2.y;
          linePositions[ptr++] = p2.z;
        } else {
          linePositions[ptr++] = 0;
          linePositions[ptr++] = 0;
          linePositions[ptr++] = 0;
          linePositions[ptr++] = 0;
          linePositions[ptr++] = 0;
          linePositions[ptr++] = 0;
        }
      }
      posAttr.needsUpdate = true;
      lineMeshRef.current.rotation.copy(meshRef.current.rotation);
    }
  });

  return (
    <>
      <instancedMesh ref={meshRef} args={[geometry, material, count]} />
      <lineSegments ref={lineMeshRef} geometry={lineGeometry} material={lineMaterial} />
    </>
  );
}

export default function CentralCore({ isActive = false, isThinking = false, isSpeaking = false, themeName = 'ultron' }) {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      setIsMobile(window.innerWidth < 768);
    }
  }, []);

  const count = isMobile ? 1200 : 5000;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8, ease: 'easeOut' }}
      style={{ width: '100%', height: '100%', position: 'relative' }}
    >
      <Canvas
        camera={{ position: [0, 0, 95], fov: 60 }}
        gl={{ alpha: true }}
        style={{ background: 'transparent' }}
      >
        <fog attach="fog" args={[themeName === 'aether' ? '#050b14' : '#0a0a0a', 0.005]} />
        <ambientLight intensity={0.4} />
        <ParticleSwarm isActive={isActive} isThinking={isThinking} isSpeaking={isSpeaking} count={count} themeName={themeName} />
        <Effects disableGamma>
          <unrealBloomPass threshold={0.04} strength={1.35} radius={0.55} />
        </Effects>
      </Canvas>
    </motion.div>
  );
}
