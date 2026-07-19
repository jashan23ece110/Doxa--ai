import React, { useRef, useMemo, useEffect, useCallback, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import * as THREE from 'three';
import { motion } from 'framer-motion';

// ─── Constants ──────────────────────────────────────────────────────────────────
const MAX_PARTICLES = 2500;
const MAX_LINE_SEGMENTS = 4000;
const CONNECTION_DIST = 0.55;
const CONNECTION_DIST_SQ = CONNECTION_DIST * CONNECTION_DIST;
const RIPPLE_DURATION = 1.0;
const CURSOR_PUSH_RADIUS = 0.6;
const CURSOR_PUSH_STRENGTH = 0.3;

// Spatial Partitioning Grid
const GRID_SIZE = 12; 
const CELL_SIZE = 0.55;
const OFFSET = 3.0; // shifts space from [-3, 3] to [0, 6]
const GRID_CELLS = GRID_SIZE * GRID_SIZE * GRID_SIZE;

// Multi-color palette
const COLORS = [
  { hex: '#ffd60a', weight: 70 }, // Gold dominant
  { hex: '#ff9500', weight: 15 }, // Amber
  { hex: '#fff4d6', weight: 10 }, // Warm white
  { hex: '#4dd0c4', weight: 5 },  // Teal accent
];

// ─── Helpers ────────────────────────────────────────────────────────────────────

function getRandomColor() {
  const rand = Math.random() * 100;
  let sum = 0;
  for (const c of COLORS) {
    sum += c.weight;
    if (rand <= sum) return new THREE.Color(c.hex);
  }
  return new THREE.Color(COLORS[0].hex);
}

/** Build explosion distribution */
function buildExplosionData(count) {
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const isDrifter = new Uint8Array(count);

  for (let i = 0; i < count; i++) {
    const u = Math.random();
    const v = Math.random();
    const theta = u * 2.0 * Math.PI;
    const phi = Math.acos(2.0 * v - 1.0);
    const r = Math.pow(Math.random(), 1.5) * 1.8; 

    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = r * Math.cos(phi);

    const color = getRandomColor();
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;

    isDrifter[i] = Math.random() < 0.25 ? 1 : 0;
  }
  return { positions, colors, isDrifter };
}

function createGlowTexture(color1, color2, color3) {
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(
    size / 2, size / 2, 0,
    size / 2, size / 2, size / 2,
  );
  gradient.addColorStop(0, color1);
  gradient.addColorStop(0.3, color2);
  gradient.addColorStop(0.7, color3);
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, size);
  const texture = new THREE.CanvasTexture(canvas);
  texture.needsUpdate = true;
  return texture;
}

function createParticleTexture() {
  return createGlowTexture(
    'rgba(255,255,255,1)',
    'rgba(255,255,255,0.6)',
    'rgba(255,255,255,0.1)'
  );
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

// ─── Inner Scene Component ──────────────────────────────────────────────────────

function NeuralExplosion({ isActive, isThinking, isSpeaking, particleCount }) {
  const { camera, pointer, gl } = useThree();

  const groupRef = useRef();
  const pointsRef = useRef();
  const linesRef = useRef();
  const glowRef = useRef();
  const rippleGroupRef = useRef();
  const ripplesRef = useRef([]);

  // Spatial Partitioning zero-allocation buffers
  const gridHeadRef = useRef(new Int32Array(GRID_CELLS));
  const gridNextRef = useRef(new Int32Array(MAX_PARTICLES));

  const animRef = useRef({
    rotationSpeed: 0.0015,
    alpha: 0.7,
    glowOpacity: 0.8,
    glowScale: 2.5,
    time: 0,
  });

  const driftRef = useRef(new Float32Array(MAX_PARTICLES));
  const basePositionsRef = useRef(null);
  
  const raycasterRef = useRef(new THREE.Raycaster());
  const cursorWorldRef = useRef(new THREE.Vector3());

  const [labels, setLabels] = useState([]);
  
  const { basePositions, baseColors, isDrifter } = useMemo(() => {
    const { positions, colors, isDrifter } = buildExplosionData(particleCount);
    return { basePositions: positions, baseColors: colors, isDrifter };
  }, [particleCount]);

  useEffect(() => {
    basePositionsRef.current = new Float32Array(basePositions);
    
    // Add floating labels
    const newLabels = [];
    const texts = ['SYS.OK', 'NET_SYNC', 'DATA_STREAM', 'MEM_OK', 'CORE_ACT', 'UPLINK'];
    const minRadius = 1.0;
    const maxRadius = 1.6;
    const minLabelDistSq = 0.8 * 0.8; // minimum distance between labels

    for(let i = 0; i < 6; i++) {
      let candidatePos = null;
      for (let attempt = 0; attempt < 100; attempt++) {
        const pIdx = Math.floor(Math.random() * particleCount) * 3;
        const px = basePositions[pIdx];
        const py = basePositions[pIdx+1];
        const pz = basePositions[pIdx+2];
        const distToCenter = Math.sqrt(px*px + py*py + pz*pz);
        
        if (distToCenter >= minRadius && distToCenter <= maxRadius) {
          // Check collision with other labels
          let tooClose = false;
          for (const lbl of newLabels) {
            const dx = lbl.pos[0] - px;
            const dy = lbl.pos[1] - py;
            const dz = lbl.pos[2] - pz;
            if (dx*dx + dy*dy + dz*dz < minLabelDistSq) {
              tooClose = true;
              break;
            }
          }
          if (!tooClose) {
            candidatePos = [px, py, pz];
            break;
          }
        }
      }
      
      // If we failed after 100 attempts, just take a random outer point (fallback)
      if (!candidatePos) {
        for (let attempt = 0; attempt < 100; attempt++) {
           const pIdx = Math.floor(Math.random() * particleCount) * 3;
           const px = basePositions[pIdx];
           const py = basePositions[pIdx+1];
           const pz = basePositions[pIdx+2];
           const distToCenter = Math.sqrt(px*px + py*py + pz*pz);
           if (distToCenter >= minRadius) {
             candidatePos = [px, py, pz];
             break;
           }
        }
      }
      if (!candidatePos) candidatePos = [1.5, 0, 0]; // hard fallback

      newLabels.push({
        id: i,
        pos: candidatePos,
        text: texts[i]
      });
    }
    setLabels(newLabels);
  }, [basePositions, particleCount]);

  const particleTexture = useMemo(() => createParticleTexture(), []);
  
  const glowTexture = useMemo(() => createGlowTexture(
    'rgba(255,214,10,0.6)',
    'rgba(255,214,10,0.2)',
    'rgba(255,214,10,0.02)'
  ), []);

  const coreTexture = useMemo(() => createGlowTexture(
    'rgba(255,255,255,1)',
    'rgba(255,244,214,0.8)',
    'rgba(255,214,10,0.1)'
  ), []);

  const pointsGeometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(basePositions);
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(baseColors, 3));
    return geo;
  }, [basePositions, baseColors]);

  const pointsMaterial = useMemo(
    () =>
      new THREE.PointsMaterial({
        size: 0.1,
        sizeAttenuation: true,
        transparent: true,
        opacity: 0.8,
        vertexColors: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        map: particleTexture,
      }),
    [particleTexture],
  );

  const linesGeometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    const posBuf = new Float32Array(MAX_LINE_SEGMENTS * 2 * 3);
    const colorBuf = new Float32Array(MAX_LINE_SEGMENTS * 2 * 3);
    geo.setAttribute('position', new THREE.BufferAttribute(posBuf, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(colorBuf, 3));
    geo.setDrawRange(0, 0);
    return geo;
  }, []);

  const linesMaterial = useMemo(
    () =>
      new THREE.LineBasicMaterial({
        vertexColors: true,
        transparent: true,
        opacity: 0.25, 
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      }),
    [],
  );

  const handleClick = useCallback(() => {
    const ringGeo = new THREE.RingGeometry(0.05, 0.2, 64);
    const ringMat = new THREE.MeshBasicMaterial({
      color: new THREE.Color('#fff4d6'),
      transparent: true,
      opacity: 0.8,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI / 2;
    if (rippleGroupRef.current) {
      rippleGroupRef.current.add(ring);
      ripplesRef.current.push({ mesh: ring, age: 0 });
    }
  }, []);

  useEffect(() => {
    const domElement = gl.domElement;
    domElement.addEventListener('click', handleClick);
    return () => domElement.removeEventListener('click', handleClick);
  }, [gl.domElement, handleClick]);

  useFrame((state, delta) => {
    const anim = animRef.current;
    anim.time += delta;

    let targetSpeed, targetAlpha, targetGlowOpacity;
    let isThinkingState = isThinking;
    let isActiveState = isActive;

    if (isThinkingState) {
      targetSpeed = 0.008;
      targetAlpha = 0.9;
      targetGlowOpacity = 1.0;
    } else if (isSpeaking) {
      // Speaking state: rhythmic pulse — sphere breathes in/out
      const pulse = Math.sin(anim.time * 4) * 0.5 + 0.5; // 0..1 at ~0.6Hz
      targetSpeed = 0.003 + pulse * 0.004;
      targetAlpha = 0.75 + pulse * 0.2;
      targetGlowOpacity = 0.7 + pulse * 0.3;
    } else if (isActiveState) {
      targetSpeed = 0.004;
      targetAlpha = 0.85;
      targetGlowOpacity = 0.8;
    } else {
      targetSpeed = 0.0015;
      targetAlpha = 0.7;
      targetGlowOpacity = 0.6;
    }

    const lerpFactor = 1 - Math.exp(-3 * delta);
    anim.rotationSpeed = lerp(anim.rotationSpeed, targetSpeed, lerpFactor);
    anim.alpha = lerp(anim.alpha, targetAlpha, lerpFactor);
    anim.glowOpacity = lerp(anim.glowOpacity, targetGlowOpacity, lerpFactor);

    if (groupRef.current) {
      groupRef.current.rotation.y += anim.rotationSpeed;
      groupRef.current.rotation.z += anim.rotationSpeed * 0.5;
    }

    const posAttr = pointsGeometry.getAttribute('position');
    const posArr = posAttr.array;
    const drift = driftRef.current;
    const base = basePositionsRef.current;

    const head = gridHeadRef.current;
    const next = gridNextRef.current;
    head.fill(-1);

    if (base) {
      for (let i = 0; i < particleCount; i++) {
        let driftTarget = 0;
        if (isThinkingState) {
          driftTarget = -0.15;
        } else if (isSpeaking) {
          // Speaking pulse: particles gently expand/contract
          const pulse = Math.sin(anim.time * 4 + i * 0.01) * 0.08;
          driftTarget = pulse;
        } else if (isActiveState && isDrifter[i]) {
          driftTarget = 0.4 + Math.sin(anim.time * 2 + i) * 0.1;
        } else if (isDrifter[i]) {
          driftTarget = Math.sin(anim.time + i) * 0.05;
        }
        
        drift[i] = lerp(drift[i], driftTarget, 0.02);
        const scale = 1 + drift[i];
        
        const px = base[i * 3] * scale;
        const py = base[i * 3 + 1] * scale;
        const pz = base[i * 3 + 2] * scale;
        
        posArr[i * 3] = px;
        posArr[i * 3 + 1] = py;
        posArr[i * 3 + 2] = pz;

        // Spatial grid insertion
        let cx = Math.floor((px + OFFSET) / CELL_SIZE);
        let cy = Math.floor((py + OFFSET) / CELL_SIZE);
        let cz = Math.floor((pz + OFFSET) / CELL_SIZE);
        
        if (cx < 0) cx = 0; if (cx >= GRID_SIZE) cx = GRID_SIZE - 1;
        if (cy < 0) cy = 0; if (cy >= GRID_SIZE) cy = GRID_SIZE - 1;
        if (cz < 0) cz = 0; if (cz >= GRID_SIZE) cz = GRID_SIZE - 1;

        const cellIdx = cx + cy * GRID_SIZE + cz * GRID_SIZE * GRID_SIZE;
        next[i] = head[cellIdx];
        head[cellIdx] = i;
      }
    }

    // Cursor interaction
    raycasterRef.current.setFromCamera(pointer, camera);
    const ray = raycasterRef.current.ray;
    const tClosest = ray.direction.dot(cursorWorldRef.current.copy(ray.origin).negate());
    if (tClosest > 0) {
      ray.at(tClosest, cursorWorldRef.current);
    } else {
      cursorWorldRef.current.set(999, 999, 999);
    }

    if (groupRef.current) {
      const invMatrix = new THREE.Matrix4().copy(groupRef.current.matrixWorld).invert();
      cursorWorldRef.current.applyMatrix4(invMatrix);
    }

    const cursorLocal = cursorWorldRef.current;
    for (let i = 0; i < particleCount; i++) {
      const ix = i * 3;
      const dx = posArr[ix] - cursorLocal.x;
      const dy = posArr[ix + 1] - cursorLocal.y;
      const dz = posArr[ix + 2] - cursorLocal.z;
      const distSq = dx * dx + dy * dy + dz * dz;

      if (distSq < CURSOR_PUSH_RADIUS * CURSOR_PUSH_RADIUS && distSq > 0.001) {
        const dist = Math.sqrt(distSq);
        const pushFactor = (1 - dist / CURSOR_PUSH_RADIUS) * CURSOR_PUSH_STRENGTH;
        posArr[ix] += (dx / dist) * pushFactor;
        posArr[ix + 1] += (dy / dist) * pushFactor;
        posArr[ix + 2] += (dz / dist) * pushFactor;
      }
    }

    posAttr.needsUpdate = true;
    pointsMaterial.opacity = anim.alpha;

    // Line connections using spatial grid
    const linePos = linesGeometry.getAttribute('position').array;
    const lineColor = linesGeometry.getAttribute('color').array;
    let lineIndex = 0;
    let lineCount = 0;

    for (let i = 0; i < particleCount && lineCount < MAX_LINE_SEGMENTS; i++) {
      const ix = i * 3;
      const px = posArr[ix];
      const py = posArr[ix + 1];
      const pz = posArr[ix + 2];

      let cx = Math.floor((px + OFFSET) / CELL_SIZE);
      let cy = Math.floor((py + OFFSET) / CELL_SIZE);
      let cz = Math.floor((pz + OFFSET) / CELL_SIZE);
      
      if (cx < 0) cx = 0; if (cx >= GRID_SIZE) cx = GRID_SIZE - 1;
      if (cy < 0) cy = 0; if (cy >= GRID_SIZE) cy = GRID_SIZE - 1;
      if (cz < 0) cz = 0; if (cz >= GRID_SIZE) cz = GRID_SIZE - 1;

      for (let x = cx - 1; x <= cx + 1; x++) {
        for (let y = cy - 1; y <= cy + 1; y++) {
          for (let z = cz - 1; z <= cz + 1; z++) {
            if (x < 0 || x >= GRID_SIZE || y < 0 || y >= GRID_SIZE || z < 0 || z >= GRID_SIZE) continue;
            
            const cellIdx = x + y * GRID_SIZE + z * GRID_SIZE * GRID_SIZE;
            let j = head[cellIdx];
            
            while (j !== -1 && lineCount < MAX_LINE_SEGMENTS) {
              if (j > i) {
                const jx = j * 3;
                const dx = px - posArr[jx];
                const dy = py - posArr[jx + 1];
                const dz = pz - posArr[jx + 2];
                const distSq = dx * dx + dy * dy + dz * dz;

                if (distSq < CONNECTION_DIST_SQ) {
                  linePos[lineIndex] = px;
                  linePos[lineIndex + 1] = py;
                  linePos[lineIndex + 2] = pz;
                  lineColor[lineIndex] = baseColors[ix];
                  lineColor[lineIndex + 1] = baseColors[ix + 1];
                  lineColor[lineIndex + 2] = baseColors[ix + 2];

                  linePos[lineIndex + 3] = posArr[jx];
                  linePos[lineIndex + 4] = posArr[jx + 1];
                  linePos[lineIndex + 5] = posArr[jx + 2];
                  lineColor[lineIndex + 3] = baseColors[jx];
                  lineColor[lineIndex + 4] = baseColors[jx + 1];
                  lineColor[lineIndex + 5] = baseColors[jx + 2];
                  
                  lineIndex += 6;
                  lineCount++;
                }
              }
              j = next[j];
            }
          }
        }
      }

      // Add rare random long cross-connections
      if (isDrifter[i] && Math.random() < 0.005 && lineCount < MAX_LINE_SEGMENTS) {
        const j = Math.floor(Math.random() * particleCount);
        if (j > i) {
          const jx = j * 3;
          linePos[lineIndex] = px;
          linePos[lineIndex + 1] = py;
          linePos[lineIndex + 2] = pz;
          lineColor[lineIndex] = baseColors[ix];
          lineColor[lineIndex + 1] = baseColors[ix + 1];
          lineColor[lineIndex + 2] = baseColors[ix + 2];

          linePos[lineIndex + 3] = posArr[jx];
          linePos[lineIndex + 4] = posArr[jx + 1];
          linePos[lineIndex + 5] = posArr[jx + 2];
          lineColor[lineIndex + 3] = baseColors[jx];
          lineColor[lineIndex + 4] = baseColors[jx + 1];
          lineColor[lineIndex + 5] = baseColors[jx + 2];
          
          lineIndex += 6;
          lineCount++;
        }
      }
    }

    linesGeometry.setDrawRange(0, lineCount * 2);
    linesGeometry.getAttribute('position').needsUpdate = true;
    linesGeometry.getAttribute('color').needsUpdate = true;

    if (glowRef.current) {
      const pulseVal = Math.sin(anim.time * 2) * 0.05 + 1;
      const glowScale = 3.5 * pulseVal;
      glowRef.current.scale.set(glowScale, glowScale, 1);
      glowRef.current.material.opacity = anim.glowOpacity + Math.sin(anim.time * 2.5) * 0.05;
    }

    const ripples = ripplesRef.current;
    for (let i = ripples.length - 1; i >= 0; i--) {
      const ripple = ripples[i];
      ripple.age += delta;
      const t = ripple.age / RIPPLE_DURATION;

      if (t >= 1) {
        if (rippleGroupRef.current) {
          rippleGroupRef.current.remove(ripple.mesh);
        }
        ripple.mesh.geometry.dispose();
        ripple.mesh.material.dispose();
        ripples.splice(i, 1);
      } else {
        const s = t * 5; 
        ripple.mesh.scale.set(s, s, s);
        ripple.mesh.material.opacity = 0.6 * (1 - t);
      }
    }
  });

  return (
    <>
      <group ref={groupRef}>
        <points ref={pointsRef} geometry={pointsGeometry} material={pointsMaterial} />
        <lineSegments ref={linesRef} geometry={linesGeometry} material={linesMaterial} />
        
        {/* Floating Data Labels */}
        {labels.map((lbl, idx) => (
          <Html 
            key={lbl.id} 
            position={lbl.pos}
            center
            style={{ pointerEvents: 'none' }}
          >
            <div style={{
              color: '#ffd60a',
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: '8px',
              opacity: 0.8,
              textShadow: '0 0 5px rgba(255,214,10,0.5)',
              border: '1px solid rgba(255,214,10,0.4)',
              padding: '2px 5px',
              backgroundColor: 'rgba(10,14,23,0.4)',
              backdropFilter: 'blur(4px)',
              borderRadius: '3px',
              whiteSpace: 'nowrap',
              animation: `centralCorePulse ${2 + idx}s infinite alternate`
            }}>
              {lbl.text}
            </div>
          </Html>
        ))}
      </group>

      {/* Center Singularity */}
      <sprite material={new THREE.SpriteMaterial({
        map: coreTexture,
        color: new THREE.Color('#ffffff'),
        transparent: true,
        opacity: 1,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      })} position={[0, 0, 0]} scale={[1.2, 1.2, 1]} />
      
      {/* Ambient Halo */}
      <sprite ref={glowRef} material={new THREE.SpriteMaterial({
        map: glowTexture,
        color: new THREE.Color('#ffd60a'),
        transparent: true,
        opacity: 0.5,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      })} position={[0, 0, 0]} />

      <group ref={rippleGroupRef} />
    </>
  );
}

// ─── Outer Component ────────────────────────────────────────────────────────────

export default function CentralCore({ isActive = false, isThinking = false, isSpeaking = false }) {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const low = window.innerWidth < 768; // Removed hardware concurrency check so mobile uses WebGL too
      setIsMobile(low);
    }
  }, []);

  // Removed CSS fallback. Both desktop and mobile render the WebGL neural explosion.
  // Mobile just renders with a lower particle count.
  const particleCount = isMobile ? 600 : 2200; 

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8, ease: 'easeOut' }}
      style={{ width: '100%', height: '100%', position: 'relative' }}
    >
      <Canvas
        dpr={[1, 2]}
        camera={{ position: [0, 0, 2.7], fov: 60 }}
        gl={{ alpha: true }}
        style={{ background: 'transparent' }}
      >
        <NeuralExplosion isActive={isActive} isThinking={isThinking} isSpeaking={isSpeaking} particleCount={particleCount} />
      </Canvas>
    </motion.div>
  );
}
