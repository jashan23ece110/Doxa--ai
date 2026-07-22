import React, { useRef, useMemo, useEffect, useState } from 'react';
import { Canvas, useFrame, extend, useThree } from '@react-three/fiber';
import { Effects } from '@react-three/drei';
import { UnrealBloomPass } from 'three-stdlib';
import * as THREE from 'three';
import { motion } from 'framer-motion';

extend({ UnrealBloomPass });

function ParticleSwarm({ isActive, isThinking, isSpeaking, count }) {
  const meshRef = useRef();
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
    const cursorWorld = new THREE.Vector3();
    raycaster.ray.intersectPlane(plane, cursorWorld);
    
    // Map cursor to local space
    const cursorLocal = cursorWorld.clone();
    const invMatrix = new THREE.Matrix4().copy(meshRef.current.matrixWorld).invert();
    cursorLocal.applyMatrix4(invMatrix);

    const pushRadius = 30.0;

    // Shockwave timeline handler
    if (shockwave.current.active) {
      shockwave.current.time += delta;
      if (shockwave.current.time > 1.5) {
        shockwave.current.active = false;
      }
    }

    for (let i = 0; i < count; i++) {
      const f = i / count;
      const phi = phiTheta[i * 2];
      const theta = phiTheta[i * 2 + 1];

      const noise1 = Math.sin(theta * 3.0 + t * 2.0);
      const noise2 = Math.cos(phi * 5.0 - t * 1.5);
      const noise3 = Math.sin((theta + phi) * swirl + t * 3.0);

      const flame = radius + noise1 * turbulence + noise2 * turbulence * 0.5 + noise3 * pulse;
      const stretch = 1.0 + 0.4 * Math.abs(Math.sin(t + f * tau * 6.0));

      let x = Math.sin(phi) * Math.cos(theta + t * 0.2) * flame;
      let y = Math.cos(phi) * flame * stretch;
      let z = Math.sin(phi) * Math.sin(theta + t * 0.2) * flame;

      const flicker = 1.0 + 0.08 * Math.sin(i * 0.15 + t * 12.0);
      x *= flicker;
      y *= flicker;
      z *= flicker;

      // Cursor attract/repel force displacement (Noticeable response)
      const dx = x - cursorLocal.x;
      const dy = y - cursorLocal.y;
      const dz = z - cursorLocal.z;
      const distSq = dx * dx + dy * dy + dz * dz;

      if (distSq < pushRadius * pushRadius && distSq > 0.01) {
        const dist = Math.sqrt(distSq);
        const force = (1.0 - dist / pushRadius) * 20.0; // Strengthened displacement push
        x += (dx / dist) * force;
        y += (dy / dist) * force;
        z += (dz / dist) * force;
      }

      // Dynamic shockwave calculation (radial burst)
      if (shockwave.current.active) {
        const waveRadius = shockwave.current.time * 65.0; // propagation speed
        const waveWidth = 7.0;
        const pDist = Math.sqrt(x * x + y * y + z * z);
        const distToWave = Math.abs(pDist - waveRadius);
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

      // Smooth color states morphing
      const heat = Math.abs(noise1 * 0.5 + noise2 * 0.5);
      const hue = 0.95 + heat * 0.11; // crimson-red to orange-red range
      const saturation = 0.95 - heat * 0.15;
      const lightness = (0.28 + heat * 0.32) * intensity + Math.abs(noise3) * 0.12 * intensity;

      pColor.setHSL(hue, saturation, lightness);
      meshRef.current.setColorAt(i, pColor);
    }

    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) {
      meshRef.current.instanceColor.needsUpdate = true;
    }
  });

  return (
    <instancedMesh ref={meshRef} args={[geometry, material, count]} />
  );
}

export default function CentralCore({ isActive = false, isThinking = false, isSpeaking = false }) {
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
        <fog attach="fog" args={['#0a0a0a', 0.005]} />
        <ambientLight intensity={0.4} />
        <ParticleSwarm isActive={isActive} isThinking={isThinking} isSpeaking={isSpeaking} count={count} />
        <Effects disableGamma>
          <unrealBloomPass threshold={0.04} strength={1.35} radius={0.55} />
        </Effects>
      </Canvas>
    </motion.div>
  );
}
