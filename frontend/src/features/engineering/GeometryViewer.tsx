import { OrbitControls } from '@react-three/drei';
import { Canvas } from '@react-three/fiber';

import type { GeometryElement, GeometryModel } from '../../types';

interface GeometryViewerProps {
  geometry: GeometryModel | null;
}

function WireElement({ element }: { element: GeometryElement }) {
  const length = element.length_m ?? 0.05;
  const radius = Math.max(element.radius_m ?? length / 90, length / 180);
  const [x, y, z] = element.position_m;
  const vertical = element.orientation_deg === 90;

  return (
    <mesh position={[x, y, z]} rotation={vertical ? [0, 0, Math.PI / 2] : [0, 0, 0]}>
      <cylinderGeometry args={[radius, radius, length, 12]} />
      <meshStandardMaterial color="#71d3b3" metalness={0.65} roughness={0.28} />
    </mesh>
  );
}

export default function GeometryViewer({ geometry }: GeometryViewerProps) {
  if (!geometry) {
    return <div className="viewer-empty">Generate a canonical design to inspect its engineering geometry.</div>;
  }

  // Keep the workspace testable in DOM-only environments; production browsers
  // receive the interactive renderer below.
  if (typeof ResizeObserver === 'undefined') {
    return <div className="viewer-empty">Interactive geometry rendering is available in a browser with canvas support.</div>;
  }

  return (
    <div className="geometry-viewer" aria-label="Interactive engineering geometry viewer">
      <Canvas camera={{ position: [0.35, 0.3, 0.45], fov: 42 }}>
        <color attach="background" args={['#101816']} />
        <ambientLight intensity={1.1} />
        <directionalLight position={[1, 1, 1]} intensity={2.2} />
        <gridHelper args={[1, 12, '#456157', '#253a33']} />
        {geometry.elements.map((element) => <WireElement key={element.name} element={element} />)}
        <OrbitControls enablePan enableZoom enableRotate />
      </Canvas>
      <p>Canonical geometry only. Rotate, pan, and zoom are viewer controls; dimensions originate in the engineering engine.</p>
    </div>
  );
}
