import { OrbitControls, Text } from '@react-three/drei';
import { Canvas } from '@react-three/fiber';
import React from 'react';

// Shared transparent material for architectural massing look
function GlassMaterial({ color = '#ffffff' }) {
  return (
    <meshPhysicalMaterial
      color={color}
      transparent
      opacity={0.75}
      roughness={0.2}
      transmission={0.5}
      thickness={1}
      envMapIntensity={1}
    />
  );
}

// Engineering Buildings (Mühendislik 1 & 2): Long rectangular blocks
function EngineeringBuilding({ position, name, color = '#c0c1ff' }) {
  const width = 3.5;
  const depth = 1.5;
  const heightPerFloor = 1;
  const floors = 4;
  const totalHeight = heightPerFloor * floors;

  return (
    <group position={position}>
      {/* Main Building Body */}
      <mesh position={[0, totalHeight / 2, 0]} castShadow receiveShadow>
        <boxGeometry args={[width, totalHeight, depth]} />
        <GlassMaterial color={color} />
      </mesh>

      {/* Roof detail */}
      <mesh position={[0, totalHeight + 0.1, 0]} castShadow receiveShadow>
        <boxGeometry args={[width - 0.2, 0.2, depth - 0.2]} />
        <meshStandardMaterial color="#ffffff" roughness={0.9} />
      </mesh>

      {/* Building Label */}
      <Text
        position={[0, totalHeight + 1.0, 0]}
        fontSize={0.4}
        color="#1b1b23"
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.03}
        outlineColor="#ffffff"
      >
        {name}
      </Text>
    </group>
  );
}

// AKM Building: Based on the provided architectural photo
function AKMBuilding({ position, name, color = '#c0c1ff' }) {
  return (
    <group position={position} scale={[0.6, 0.6, 0.6]}>
      {/* Left Wing */}
      <mesh position={[-4, 1.5, -2]} castShadow receiveShadow>
        <boxGeometry args={[6, 3, 2.5]} />
        <GlassMaterial color={color} />
      </mesh>
      
      {/* Center Connecting Hall (angled to create the curved facade illusion) */}
      <mesh position={[-0.5, 1.5, -1.5]} castShadow receiveShadow rotation={[0, -Math.PI / 12, 0]}>
        <boxGeometry args={[4, 3, 2.5]} />
        <GlassMaterial color={color} />
      </mesh>

      {/* Back Right Wing */}
      <mesh position={[3, 1.5, -3]} castShadow receiveShadow rotation={[0, Math.PI / 8, 0]}>
        <boxGeometry args={[3.5, 3, 2.5]} />
        <GlassMaterial color={color} />
      </mesh>

      {/* Prominent Front Right Rotunda */}
      <mesh position={[3.5, 1.5, 1]} castShadow receiveShadow>
        <cylinderGeometry args={[3.5, 3.5, 3, 64]} />
        <GlassMaterial color={color} />
      </mesh>
      
      {/* Rotunda Roof Detail */}
      <mesh position={[3.5, 3.1, 1]} castShadow receiveShadow>
        <cylinderGeometry args={[3.4, 3.4, 0.2, 64]} />
        <meshStandardMaterial color="#ffffff" roughness={0.9} />
      </mesh>

      {/* Left Wing Roof Detail */}
      <mesh position={[-4, 3.1, -2]} castShadow receiveShadow>
        <boxGeometry args={[5.8, 0.2, 2.3]} />
        <meshStandardMaterial color="#ffffff" roughness={0.9} />
      </mesh>

      {/* Back Right Wing Roof Detail */}
      <mesh position={[3, 3.1, -3]} castShadow receiveShadow rotation={[0, Math.PI / 8, 0]}>
        <boxGeometry args={[3.3, 0.2, 2.3]} />
        <meshStandardMaterial color="#ffffff" roughness={0.9} />
      </mesh>

      {/* Center Roof Detail */}
      <mesh position={[-0.5, 3.1, -1.5]} castShadow receiveShadow rotation={[0, -Math.PI / 12, 0]}>
        <boxGeometry args={[3.8, 0.2, 2.3]} />
        <meshStandardMaterial color="#ffffff" roughness={0.9} />
      </mesh>

      {/* Building Label */}
      <Text
        position={[0, 4.5, 0]}
        fontSize={0.8}
        color="#1b1b23"
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.05}
        outlineColor="#ffffff"
      >
        {name}
      </Text>
    </group>
  );
}

export default function ThreeDMap() {
  return (
    <div className="absolute inset-0">
      <Canvas shadows camera={{ position: [0, 6, 10], fov: 50 }}>
        <color attach="background" args={['#f5f2fe']} />
        
        {/* Lighting */}
        <ambientLight intensity={0.6} />
        <directionalLight
          position={[10, 15, 10]}
          intensity={1.5}
          castShadow
          shadow-mapSize={[1024, 1024]}
        />

        {/* Buildings */}
        {/* Mühendislik 1 */}
        <EngineeringBuilding position={[-4.5, 0, -2]} name="Mühendislik 1" color="#c0c1ff" />
        
        {/* Mühendislik 2 */}
        <EngineeringBuilding position={[0, 0, 1]} name="Mühendislik 2" color="#c0c1ff" />
        
        {/* AKM */}
        <AKMBuilding position={[5, 0, -1]} name="AKM" color="#ffb783" />

        {/* Ground */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]} receiveShadow>
          <planeGeometry args={[50, 50]} />
          <meshStandardMaterial color="#e4e1ed" />
        </mesh>

        {/* Controls */}
        <OrbitControls makeDefault minPolarAngle={0} maxPolarAngle={Math.PI / 2 - 0.05} />
      </Canvas>
    </div>
  );
}
