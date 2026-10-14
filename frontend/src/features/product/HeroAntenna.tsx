import { OrbitControls } from '@react-three/drei';
import { Canvas, useFrame } from '@react-three/fiber';
import { useMemo, useRef, useState } from 'react';
import type { Group } from 'three';

const elements = [
  { z: -1.55, length: 2.55, accent: false },
  { z: -0.72, length: 2.28, accent: true },
  { z: 0.02, length: 2.04, accent: false },
  { z: 0.67, length: 1.83, accent: false },
  { z: 1.24, length: 1.66, accent: false },
  { z: 1.72, length: 1.52, accent: false },
] as const;

function AntennaAssembly({ reducedMotion, interacting }: { reducedMotion: boolean; interacting: boolean }) {
  const assembly = useRef<Group>(null);
  const material = useMemo(() => ({ color: '#d7e0dc', metalness: 0.8, roughness: 0.27 }), []);

  useFrame((_, delta) => {
    if (assembly.current && !reducedMotion && !interacting) assembly.current.rotation.y += delta * 0.16;
  });

  return <group ref={assembly} rotation={[0.14, -0.72, 0.05]}>
    <mesh rotation={[Math.PI / 2, 0, 0]}>
      <cylinderGeometry args={[0.055, 0.055, 3.9, 12]} />
      <meshStandardMaterial color="#26332e" metalness={0.65} roughness={0.34} />
    </mesh>
    {elements.map((element) => <group key={element.z} position={[0, 0, element.z]}>
      <mesh rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.032, 0.032, element.length, 12]} />
        <meshStandardMaterial {...material} color={element.accent ? '#3bb88a' : material.color} />
      </mesh>
      <mesh position={[0, 0.035, 0]}>
        <boxGeometry args={[0.15, 0.1, 0.15]} />
        <meshStandardMaterial color="#34443c" metalness={0.42} roughness={0.45} />
      </mesh>
    </group>)}
  </group>;
}

export default function HeroAntenna() {
  const [interacting, setInteracting] = useState(false);
  const reducedMotion = typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

  if (typeof ResizeObserver === 'undefined') return <div className="hero-antenna-fallback" aria-label="Parametric Yagi-Uda antenna visualization">3D antenna visual</div>;

  return <div className="hero-antenna" aria-label="Interactive parametric Yagi-Uda antenna visualization">
    <Canvas camera={{ position: [4.5, 2.9, 5.4], fov: 40 }} dpr={[1, 1.5]} gl={{ antialias: true, alpha: true }}>
      <ambientLight intensity={1.4} />
      <directionalLight position={[4, 5, 3]} intensity={2.7} color="#f8fff9" />
      <directionalLight position={[-3, 1, -2]} intensity={0.8} color="#71d8af" />
      <AntennaAssembly reducedMotion={reducedMotion} interacting={interacting} />
      <gridHelper args={[8, 16, '#426256', '#22392f']} position={[0, -1.34, 0]} />
      <OrbitControls
        enablePan
        enableZoom
        minDistance={4.2}
        maxDistance={8}
        onStart={() => setInteracting(true)}
        onEnd={() => window.setTimeout(() => setInteracting(false), 1600)}
      />
    </Canvas>
    <div className="hero-annotation annotation-top">PARAMETRIC YAGI-UDA</div>
    <div className="hero-annotation annotation-side">FREQUENCY · INPUT-DRIVEN</div>
    <div className="hero-annotation annotation-bottom">INTERACTIVE GEOMETRY VIEW</div>
  </div>;
}
