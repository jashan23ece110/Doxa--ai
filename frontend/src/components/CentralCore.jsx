import React, { useRef, useMemo, useEffect, useState } from 'react';
import { Canvas, useFrame, extend, useThree } from '@react-three/fiber';
import { Effects } from '@react-three/drei';
import { UnrealBloomPass } from 'three-stdlib';
import * as THREE from 'three';
import { motion } from 'framer-motion';

extend({ UnrealBloomPass });

function ParticleSwarm({
  isActive,
  isThinking,
  isSpeaking,
  count,
  themeName = 'ultron',
  sentiment = 'neutral',
  isDebating = false,
  steps = [],
}) {
  const meshRef = useRef();
  const lineMeshRef = useRef();
  const coreOuterRef = useRef();
  const coreInnerRef = useRef();
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

  // Precompute random offsets for node clusters in Thought Graph mode
  const nodeOffsets = useMemo(() => {
    const arr = [];
    for (let i = 0; i < count; i++) {
      const radius = Math.random() * 5.0 + 1.0;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2.0 * Math.random() - 1.0);
      arr.push(new THREE.Vector3(
        radius * Math.sin(phi) * Math.cos(theta),
        radius * Math.sin(phi) * Math.sin(theta),
        radius * Math.cos(phi)
      ));
    }
    return arr;
  }, [count]);

  const morphProgress = useRef(0);
  const debateProgress = useRef(0);

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

    // Easing breathing pattern for Idle state (hypnotic Slow Wave)
    let breathing = 1.0;
    if (!isThinking && !isSpeaking && !isActive) {
      breathing = 1.0 + Math.sin(time * 1.5) * 0.12; // slow breathing cycle ~ 4s
    }

    // Voice envelope simulation (syllable frequency ~4Hz + intonation jitter ~18Hz)
    let speechEnvelope = 0.1;
    if (isSpeaking) {
      const syllableWave = Math.sin(time * 3.8 * Math.PI * 2);
      const intonationWave = Math.sin(time * 18.0);
      speechEnvelope = (syllableWave * 0.55 + intonationWave * 0.15 + 0.45);
      speechEnvelope = Math.max(0.05, Math.min(1.0, speechEnvelope));
    }

    if (isThinking) {
      targetRadius = 42;
      targetTurbulence = 15.0;
      targetPulse = 9.5;
      targetSpeed = 1.6;
      targetSwirl = 6.5;
      targetColorIntensity = 1.0;
    } else if (isSpeaking) {
      // Dynamic voice reactive envelope
      targetRadius = 31.0 + speechEnvelope * 13.0 + Math.sin(time * 62.0) * 0.45 * speechEnvelope; // voice vibration ripple
      targetTurbulence = 9.5;
      targetPulse = 4.0 + speechEnvelope * 12.0;
      targetSpeed = 1.1;
      targetSwirl = 4.2;
      targetColorIntensity = 0.85 + speechEnvelope * 0.15;
    } else if (isActive) {
      targetRadius = 28;
      targetTurbulence = 6.5;
      targetPulse = 3.5;
      targetSpeed = 0.75;
      targetSwirl = 2.2;
      targetColorIntensity = 0.75;
    } else {
      // Idle state with breathing effect
      targetRadius = 22 * breathing;
      targetPulse = 2.5 * breathing;
      targetTurbulence = 3.5 + Math.sin(time * 1.5) * 0.8;
      targetSpeed = 0.28;
    }

    // Apply sentiment adjustments
    if (sentiment === 'serious') {
      targetSpeed *= 0.6;
      targetPulse *= 0.7;
      targetRadius *= 0.95;
      targetColorIntensity *= 0.8;
    } else if (sentiment === 'exciting') {
      targetSpeed *= 1.4;
      targetPulse *= 1.5;
      targetTurbulence *= 1.2;
      targetColorIntensity *= 1.25;
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

    // Update morphProgress for Thought Graph mode
    const targetMorph = isThinking ? 1.0 : 0.0;
    morphProgress.current = THREE.MathUtils.lerp(morphProgress.current, targetMorph, 2.5 * delta);

    // Update debateProgress for Multi-Agent Debate mode
    const targetDebate = isDebating ? 1.0 : 0.0;
    debateProgress.current = THREE.MathUtils.lerp(debateProgress.current, targetDebate, 2.5 * delta);

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

      // Morph coordinates to node centers if in Thought Graph mode
      if (morphProgress.current > 0.001) {
        const pOffset = nodeOffsets[i];
        const nodeIdx = i % 3;
        let nodeX = 0, nodeY = 0, nodeZ = 0;
        if (nodeIdx === 0) {
          nodeX = -25 + pOffset.x;
          nodeY = 12 + pOffset.y;
          nodeZ = pOffset.z;
        } else if (nodeIdx === 1) {
          nodeX = 0 + pOffset.x;
          nodeY = 0 + pOffset.y;
          nodeZ = pOffset.z;
        } else {
          nodeX = 25 + pOffset.x;
          nodeY = -12 + pOffset.y;
          nodeZ = pOffset.z;
        }
        x = THREE.MathUtils.lerp(x, nodeX, morphProgress.current);
        y = THREE.MathUtils.lerp(y, nodeY, morphProgress.current);
        z = THREE.MathUtils.lerp(z, nodeZ, morphProgress.current);
      }

      // Morph coordinates to two separate split centers if in Multi-Agent Debate mode
      if (debateProgress.current > 0.001) {
        const cx = i < count / 2 ? -18 : 18;
        const targetX = cx + x * 0.55;
        const targetY = y * 0.55;
        const targetZ = z * 0.55;
        x = THREE.MathUtils.lerp(x, targetX, debateProgress.current);
        y = THREE.MathUtils.lerp(y, targetY, debateProgress.current);
        z = THREE.MathUtils.lerp(z, targetZ, debateProgress.current);
      }

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
        let baseHue = 0.52;
        if (sentiment === 'serious') baseHue = 0.62;
        else if (sentiment === 'exciting') baseHue = 0.48;
        hue = baseHue + heat * 0.12;
        saturation = 0.90 - heat * 0.10;
        lightness = (0.35 + heat * 0.35) * intensity;
      } else {
        // ultron crimson red
        let baseHue = 0.95;
        if (sentiment === 'serious') baseHue = 0.78;
        else if (sentiment === 'exciting') baseHue = 0.02;
        hue = baseHue + heat * 0.11;
        saturation = 0.95 - heat * 0.15;
        lightness = (0.28 + heat * 0.32) * intensity + Math.abs(noise3) * 0.12 * intensity;
      }

      // Morph colors in Multi-Agent Debate mode
      if (debateProgress.current > 0.001) {
        if (i < count / 2) {
          // Left sphere: crimson red (hue ~0.95)
          hue = THREE.MathUtils.lerp(hue, 0.95, debateProgress.current);
          saturation = THREE.MathUtils.lerp(saturation, 0.95, debateProgress.current);
          lightness = THREE.MathUtils.lerp(lightness, 0.38 * intensity, debateProgress.current);
        } else {
          // Right sphere: cyan blue (hue ~0.54)
          hue = THREE.MathUtils.lerp(hue, 0.54, debateProgress.current);
          saturation = THREE.MathUtils.lerp(saturation, 0.90, debateProgress.current);
          lightness = THREE.MathUtils.lerp(lightness, 0.42 * intensity, debateProgress.current);
        }
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
        
        // Skip drawing cross-boundary lines in Multi-Agent Debate mode
        if (debateProgress.current > 0.1 && ((p1Idx < count / 2 && p2Idx >= count / 2) || (p1Idx >= count / 2 && p2Idx < count / 2))) {
          linePositions[ptr++] = 0;
          linePositions[ptr++] = 0;
          linePositions[ptr++] = 0;
          linePositions[ptr++] = 0;
          linePositions[ptr++] = 0;
          linePositions[ptr++] = 0;
          continue;
        }

        const p1 = positions[p1Idx];
        const p2 = positions[p2Idx];

        const dist = p1.distanceTo(p2);
        const maxDist = isThinking ? 75 : 35;

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

    // Project node centers to 2D screen space for Thought Graph labels
    if (typeof window !== 'undefined') {
      const nodeCenters = [
        new THREE.Vector3(-25, 12, 0),
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(25, -12, 0)
      ];

      const width = gl.domElement.clientWidth;
      const height = gl.domElement.clientHeight;

      nodeCenters.forEach((center, idx) => {
        const tempV = center.clone();
        tempV.project(camera);

        const x = (tempV.x * 0.5 + 0.5) * width;
        const y = (-(tempV.y * 0.5) + 0.5) * height;

        const el = document.getElementById(`doxa-node-label-${idx}`);
        if (el) {
          el.style.left = `${x}px`;
          el.style.top = `${y}px`;
          el.style.opacity = morphProgress.current;
          el.style.pointerEvents = morphProgress.current > 0.3 ? 'auto' : 'none';
        }
      });
      // Animate central cores
      if (coreOuterRef.current) {
        const coreScale = 1.0 + (isSpeaking ? speechEnvelope * 0.25 : (isThinking ? 0.15 + Math.sin(time * 8.0) * 0.05 : Math.sin(time * 1.5) * 0.05));
        coreOuterRef.current.scale.set(coreScale, coreScale, coreScale);
        
        // Sync color with current active theme
        const hexColor = themeName === 'aether' ? 0x00d9ff : 0xdc143c; // cyan or crimson
        coreOuterRef.current.material.color.setHex(hexColor);
        
        // Sync opacity
        coreOuterRef.current.material.opacity = isThinking
          ? 0.45 + Math.sin(time * 10) * 0.1
          : 0.28 + (isSpeaking ? speechEnvelope * 0.15 : Math.sin(time * 1.5) * 0.06);
      }
      if (coreInnerRef.current) {
        const coreScale = 1.0 + (isSpeaking ? speechEnvelope * 0.12 : (isThinking ? 0.08 : Math.sin(time * 1.5) * 0.02));
        coreInnerRef.current.scale.set(coreScale, coreScale, coreScale);
        
        coreInnerRef.current.material.opacity = isThinking
          ? 0.75 + Math.sin(time * 15) * 0.08
          : 0.65 + (isSpeaking ? speechEnvelope * 0.1 : Math.sin(time * 1.5) * 0.03);
      }
    }
  });

  return (
    <>
      <instancedMesh ref={meshRef} args={[geometry, material, count]} />
      <lineSegments ref={lineMeshRef} geometry={lineGeometry} material={lineMaterial} />
      
      {/* Dynamic central glowing cores */}
      <mesh ref={coreOuterRef}>
        <sphereGeometry args={[9.5, 32, 32]} />
        <meshBasicMaterial
          color={themeName === 'aether' ? 0x00d9ff : 0xdc143c}
          transparent
          opacity={0.3}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </mesh>
      <mesh ref={coreInnerRef}>
        <sphereGeometry args={[4.2, 32, 32]} />
        <meshBasicMaterial
          color={0xffffff}
          transparent
          opacity={0.65}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </mesh>
    </>
  );
}

export default function CentralCore({
  isActive = false,
  isThinking = false,
  isSpeaking = false,
  themeName = 'ultron',
  sentiment = 'neutral',
  isDebating = false,
  steps = [],
}) {
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
        <ParticleSwarm
          isActive={isActive}
          isThinking={isThinking}
          isSpeaking={isSpeaking}
          count={count}
          themeName={themeName}
          sentiment={sentiment}
          isDebating={isDebating}
          steps={steps}
        />
        <Effects disableGamma>
          <unrealBloomPass threshold={0.04} strength={1.35} radius={0.55} />
        </Effects>
      </Canvas>

      {/* Thought Graph Floating Labels */}
      {!isMobile && (
        <>
          <div
            id="doxa-node-label-0"
            className="absolute transform -translate-x-1/2 -translate-y-1/2 opacity-0 z-30 pointer-events-none transition-all duration-150"
          >
            <div className="bg-black/85 backdrop-blur-md border border-[rgba(var(--jarvis-accent-rgb),0.35)] px-3 py-1.5 rounded-lg flex items-center gap-2 shadow-2xl">
              <span className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]" />
              <span className="text-[10px] tracking-wider uppercase font-semibold text-[#e0d6c2] font-mono">
                PLANNING CORE
              </span>
            </div>
          </div>
          <div
            id="doxa-node-label-1"
            className="absolute transform -translate-x-1/2 -translate-y-1/2 opacity-0 z-30 pointer-events-none transition-all duration-150"
          >
            <div className="bg-black/85 backdrop-blur-md border border-[rgba(var(--jarvis-accent-rgb),0.35)] px-3 py-1.5 rounded-lg flex items-center gap-2 shadow-2xl">
              <span className={`w-2 h-2 rounded-full ${steps.some(s => s.step.toLowerCase().includes('execut')) ? 'bg-amber-500 animate-pulse shadow-[0_0_8px_#f59e0b]' : steps.length > 2 ? 'bg-emerald-500 shadow-[0_0_8px_#10b981]' : 'bg-neutral-600'}`} />
              <span className="text-[10px] tracking-wider uppercase font-semibold text-[#e0d6c2] font-mono">
                RUNTIME EXECUTOR
              </span>
            </div>
          </div>
          <div
            id="doxa-node-label-2"
            className="absolute transform -translate-x-1/2 -translate-y-1/2 opacity-0 z-30 pointer-events-none transition-all duration-150"
          >
            <div className="bg-black/85 backdrop-blur-md border border-[rgba(var(--jarvis-accent-rgb),0.35)] px-3 py-1.5 rounded-lg flex items-center gap-2 shadow-2xl">
              <span className={`w-2 h-2 rounded-full ${steps.some(s => s.step.toLowerCase().includes('final')) ? 'bg-amber-500 animate-pulse shadow-[0_0_8px_#f59e0b]' : steps.some(s => s.step.toLowerCase().includes('finaliz')) ? 'bg-emerald-500 shadow-[0_0_8px_#10b981]' : 'bg-neutral-600'}`} />
              <span className="text-[10px] tracking-wider uppercase font-semibold text-[#e0d6c2] font-mono">
                SYNTHESIS ENGINE
              </span>
            </div>
          </div>
        </>
      )}
    </motion.div>
  );
}
