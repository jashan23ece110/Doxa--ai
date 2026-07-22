import React, { useRef, useMemo, useEffect, useState } from 'react';
import { Canvas, useFrame, extend, useThree } from '@react-three/fiber';
import { Effects } from '@react-three/drei';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import * as THREE from 'three';
import { motion } from 'framer-motion';

extend({ UnrealBloomPass });

function ParticleSwarm({ isActive, isThinking, isSpeaking, count }) {
  const meshRef = useRef();
  const { camera, pointer, raycaster } = useThree();
  
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const target = useMemo(() => new THREE.Vector3(), []);
  const pColor = useMemo(() => new THREE.Color(), []);
  
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
    radius: 35,
    turbulence: 5,
    pulse: 4,
    speed: 1.0,
    swirl: 2
  });

  useFrame((state, delta) => {
    if (!meshRef.current) return;
    const time = state.clock.getElapsedTime();

    // Rotate the whole mesh slowly for ambient rotation
    meshRef.current.rotation.y = time * 0.05;
    meshRef.current.rotation.x = Math.sin(time * 0.02) * 0.1;

    // Define target parameters based on state
    let targetRadius = 35;
    let targetTurbulence = 5;
    let targetPulse = 4;
    let targetSpeed = 1.0;
    let targetSwirl = 2;

    if (isThinking) {
      targetRadius = 28;
      targetTurbulence = 15;
      targetPulse = 10;
      targetSpeed = 2.6;
      targetSwirl = 7;
    } else if (isSpeaking) {
      // Breathing pulse during voice synthesis
      const speakPulse = Math.sin(time * 12) * 5;
      targetRadius = 36 + speakPulse;
      targetTurbulence = 9;
      targetPulse = 12;
      targetSpeed = 1.8;
      targetSwirl = 4;
    } else if (isActive) {
      targetRadius = 39;
      targetTurbulence = 7;
      targetPulse = 5;
      targetSpeed = 1.3;
      targetSwirl = 3;
    }

    // Smooth transition between parameter sets
    const lerpFactor = 1 - Math.exp(-4 * delta);
    currentParams.current.radius = THREE.MathUtils.lerp(currentParams.current.radius, targetRadius, lerpFactor);
    currentParams.current.turbulence = THREE.MathUtils.lerp(currentParams.current.turbulence, targetTurbulence, lerpFactor);
    currentParams.current.pulse = THREE.MathUtils.lerp(currentParams.current.pulse, targetPulse, lerpFactor);
    currentParams.current.speed = THREE.MathUtils.lerp(currentParams.current.speed, targetSpeed, lerpFactor);
    currentParams.current.swirl = THREE.MathUtils.lerp(currentParams.current.swirl, targetSwirl, lerpFactor);

    const radius = currentParams.current.radius;
    const turbulence = currentParams.current.turbulence;
    const pulse = currentParams.current.pulse;
    const speed = currentParams.current.speed;
    const swirl = currentParams.current.swirl;

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

    const pushRadius = 24.0;

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

      // Cursor repel vector math
      const dx = x - cursorLocal.x;
      const dy = y - cursorLocal.y;
      const dz = z - cursorLocal.z;
      const distSq = dx * dx + dy * dy + dz * dz;

      if (distSq < pushRadius * pushRadius && distSq > 0.01) {
        const dist = Math.sqrt(distSq);
        const force = (1.0 - dist / pushRadius) * 14.0;
        x += (dx / dist) * force;
        y += (dy / dist) * force;
        z += (dz / dist) * force;
      }

      target.set(x, y, z);
      positions[i].lerp(target, 0.12);

      dummy.position.copy(positions[i]);
      dummy.updateMatrix();
      meshRef.current.setMatrixAt(i, dummy.matrix);

      // Colors: Overriding to gold/amber spectrum (#ffd60a based)
      const heat = Math.abs(noise1 * 0.5 + noise2 * 0.5);
      const hue = 0.08 + heat * 0.06; // HSL yellow-gold range
      const saturation = 0.95 - heat * 0.15;
      const lightness = 0.38 + heat * 0.35 + Math.abs(noise3) * 0.12;

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
          <unrealBloomPass threshold={0} strength={1.5} radius={0.45} />
        </Effects>
      </Canvas>
    </motion.div>
  );
}
