import { OrbitControls, Text, Edges, ContactShadows, Environment, Sky } from '@react-three/drei';
import { Canvas, useFrame } from '@react-three/fiber';
import React, { useState, useRef } from 'react';

// Realistic Materials
const materials = {
  wall: <meshStandardMaterial color="#e5e0d8" roughness={0.8} />, // Lighter Beige/plaster
  glass: <meshStandardMaterial color="#2a4b6c" roughness={0.1} metalness={0.9} />, // Reflective glass
  roof: <meshStandardMaterial color="#5a5a5a" roughness={0.9} />, // Darker roof
  frame: <meshStandardMaterial color="#808080" roughness={0.5} metalness={0.5} />, // Metallic frames
  concrete: <meshStandardMaterial color="#8e8e8e" roughness={0.9} />, // Concrete base
  hvac: <meshStandardMaterial color="#b0b0b0" roughness={0.6} metalness={0.4} />, // HVAC metal
  treeTrunk: <meshStandardMaterial color="#5c4033" roughness={0.9} />, // Tree trunk
  treeLeaves: <meshStandardMaterial color="#2d5a27" roughness={0.8} />, // Tree leaves
};

// Tree Component
function Tree({ position, scale = 1 }) {
  return (
    <group position={position} scale={[scale, scale, scale]}>
      {/* Trunk */}
      <mesh position={[0, 0.5, 0]} castShadow receiveShadow>
        <cylinderGeometry args={[0.2, 0.3, 1, 8]} />
        {materials.treeTrunk}
      </mesh>
      {/* Leaves (Pine tree style) */}
      <mesh position={[0, 1.5, 0]} castShadow receiveShadow>
        <coneGeometry args={[1.2, 2, 8]} />
        {materials.treeLeaves}
      </mesh>
      <mesh position={[0, 2.2, 0]} castShadow receiveShadow>
        <coneGeometry args={[1, 1.5, 8]} />
        {materials.treeLeaves}
      </mesh>
    </group>
  );
}

// Critical Alert Badge — pulsing red orb above the building
function CriticalBadge({ yOffset = 6 }) {
  const meshRef = useRef();
  const ringRef = useRef();

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    if (meshRef.current) {
      meshRef.current.position.y = yOffset + Math.sin(t * 2) * 0.15;
    }
    if (ringRef.current) {
      const pulse = 1 + Math.abs(Math.sin(t * 2)) * 0.5;
      ringRef.current.scale.set(pulse, pulse, pulse);
      ringRef.current.material.opacity = 1 - Math.abs(Math.sin(t * 2)) * 0.6;
    }
  });

  return (
    <group>
      <mesh ref={ringRef} position={[0, yOffset, 0]}>
        <torusGeometry args={[0.35, 0.05, 8, 24]} />
        <meshStandardMaterial color="#ef4444" emissive="#ef4444" emissiveIntensity={2} transparent opacity={0.7} />
      </mesh>
      <mesh ref={meshRef} position={[0, yOffset, 0]}>
        <sphereGeometry args={[0.22, 16, 16]} />
        <meshStandardMaterial color="#ef4444" emissive="#ef4444" emissiveIntensity={3} roughness={0.1} />
      </mesh>
      <Text position={[0.5, yOffset + 0.05, 0]} fontSize={0.35} color="#ef4444" anchorX="left" anchorY="middle" outlineWidth={0.04} outlineColor="#ffffff">
        ! KRİTİK
      </Text>
    </group>
  );
}

// Window Grid Component
function RealisticWindows({ width, height, rows, cols, position, rotation = [0, 0, 0] }) {
  const w = width / cols;
  const h = height / rows;
  const gap = 0.05;
  const windows = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x = -width / 2 + w / 2 + c * w;
      const y = -height / 2 + h / 2 + r * h;
      windows.push(
        <mesh key={`${r}-${c}`} position={[x, y, 0]} castShadow>
          <boxGeometry args={[w - gap, h - gap, 0.1]} />
          {materials.glass}
        </mesh>
      );
    }
  }
  return (
    <group position={position} rotation={rotation}>
      <mesh position={[0, 0, -0.05]}>
        <boxGeometry args={[width, height, 0.05]} />
        <meshStandardMaterial color="#222" />
      </mesh>
      {windows}
    </group>
  );
}

// Engineering Buildings
function EngineeringBuilding({ position, name, onClick, isActive, hasCritical, variant = 1 }) {
  const [hovered, setHovered] = useState(false);
  const width = variant === 1 ? 4 : 5;
  const depth = variant === 1 ? 2 : 2.5;
  const totalHeight = variant === 1 ? 4 : 3.5;
  const cols = variant === 1 ? 6 : 8;
  const winWidth = variant === 1 ? 3.6 : 4.6;

  const handlePointerOver = (e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = 'pointer'; };
  const handlePointerOut = (e) => { e.stopPropagation(); setHovered(false); document.body.style.cursor = 'auto'; };
  const handleClick = (e) => { e.stopPropagation(); if (onClick) onClick(name); };

  return (
    <group position={position} onClick={handleClick} onPointerOver={handlePointerOver} onPointerOut={handlePointerOut}>
      <mesh position={[0, 0.1, 0]} receiveShadow castShadow>
        <boxGeometry args={[width + 0.4, 0.2, depth + 0.4]} />
        <meshStandardMaterial color={hovered || isActive ? "#a0a0a0" : "#8e8e8e"} roughness={0.9} />
      </mesh>
      <mesh position={[0, totalHeight / 2, 0]} castShadow receiveShadow>
        <boxGeometry args={[width, totalHeight, depth]} />
        <meshStandardMaterial color={hovered || isActive ? "#f5f0e8" : "#e5e0d8"} roughness={0.8} />
        <Edges scale={1} threshold={15} color={hovered || isActive ? "#3b82f6" : "#c0b9b0"} />
      </mesh>
      <RealisticWindows width={winWidth} height={1.2} rows={1} cols={cols} position={[0, 1.2, depth / 2]} />
      {variant === 1 && <RealisticWindows width={winWidth} height={1.2} rows={1} cols={cols} position={[0, 2.8, depth / 2]} />}
      <RealisticWindows width={winWidth} height={1.2} rows={1} cols={cols} position={[0, 1.2, -depth / 2]} rotation={[0, Math.PI, 0]} />
      {variant === 1 && <RealisticWindows width={winWidth} height={1.2} rows={1} cols={cols} position={[0, 2.8, -depth / 2]} rotation={[0, Math.PI, 0]} />}
      <mesh position={[0, totalHeight + 0.1, 0]} castShadow receiveShadow>
        <boxGeometry args={[width + 0.2, 0.2, depth + 0.2]} />
        {materials.roof}
      </mesh>
      <group position={[0, totalHeight + 0.4, 0]}>
         <mesh position={[-1, 0, 0]} castShadow><boxGeometry args={[0.6, 0.4, 0.6]} />{materials.hvac}</mesh>
         <mesh position={[1, 0, 0]} castShadow><boxGeometry args={[0.4, 0.5, 0.8]} />{materials.hvac}</mesh>
      </group>
      {hasCritical && <CriticalBadge yOffset={totalHeight + 1.8} />}
      <Text position={[0, totalHeight + 1.2, 0]} fontSize={0.4} color={hasCritical ? '#ef4444' : '#1b1b23'} anchorX="center" anchorY="middle" outlineWidth={0.03} outlineColor="#ffffff">
        {name}
      </Text>
    </group>
  );
}

// AKM Building
function AKMBuilding({ position, name, onClick, isActive, hasCritical }) {
  const [hovered, setHovered] = useState(false);

  const handlePointerOver = (e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = 'pointer'; };
  const handlePointerOut = (e) => { e.stopPropagation(); setHovered(false); document.body.style.cursor = 'auto'; };
  const handleClick = (e) => { e.stopPropagation(); if (onClick) onClick(name); };

  return (
    <group position={position} scale={[0.6, 0.6, 0.6]} onClick={handleClick} onPointerOver={handlePointerOver} onPointerOut={handlePointerOut}>
      <mesh position={[0, 0.1, -1]} receiveShadow castShadow>
        <boxGeometry args={[14, 0.2, 9]} />
        <meshStandardMaterial color={hovered || isActive ? "#a0a0a0" : "#8e8e8e"} roughness={0.9} />
      </mesh>
      <group position={[-4, 0, -2]}>
        <mesh position={[0, 1.5, 0]} castShadow receiveShadow>
          <boxGeometry args={[6, 3, 2.5]} />
          <meshStandardMaterial color={hovered || isActive ? "#f5f0e8" : "#e5e0d8"} roughness={0.8} />
          <Edges color={hovered || isActive ? "#3b82f6" : "#c0b9b0"} />
        </mesh>
        <RealisticWindows width={5.6} height={0.8} rows={1} cols={8} position={[0, 1, 1.25]} />
        <RealisticWindows width={5.6} height={0.8} rows={1} cols={8} position={[0, 2.2, 1.25]} />
        <mesh position={[0, 3.1, 0]} castShadow receiveShadow><boxGeometry args={[6.2, 0.2, 2.7]} />{materials.roof}</mesh>
      </group>
      <group position={[-0.5, 0, -1.5]} rotation={[0, -Math.PI / 12, 0]}>
        <mesh position={[0, 1.5, 0]} castShadow receiveShadow>
          <boxGeometry args={[4, 3, 2.5]} />
          <meshStandardMaterial color={hovered || isActive ? "#f5f0e8" : "#e5e0d8"} roughness={0.8} />
        </mesh>
        <RealisticWindows width={3.8} height={2.8} rows={3} cols={4} position={[0, 1.5, 1.25]} />
        <mesh position={[0, 3.1, 0]} castShadow receiveShadow><boxGeometry args={[4.2, 0.2, 2.7]} />{materials.roof}</mesh>
      </group>
      <group position={[3, 0, -3]} rotation={[0, Math.PI / 8, 0]}>
        <mesh position={[0, 1.5, 0]} castShadow receiveShadow>
          <boxGeometry args={[3.5, 3, 2.5]} />
          <meshStandardMaterial color={hovered || isActive ? "#f5f0e8" : "#e5e0d8"} roughness={0.8} />
          <Edges color={hovered || isActive ? "#3b82f6" : "#c0b9b0"} />
        </mesh>
        <RealisticWindows width={3.1} height={0.8} rows={1} cols={4} position={[0, 1, 1.25]} />
        <RealisticWindows width={3.1} height={0.8} rows={1} cols={4} position={[0, 2.2, 1.25]} />
        <mesh position={[0, 3.1, 0]} castShadow receiveShadow><boxGeometry args={[3.7, 0.2, 2.7]} />{materials.roof}</mesh>
      </group>
      <group position={[3.5, 0, 1]}>
        <mesh position={[0, 1.5, 0]} castShadow receiveShadow><cylinderGeometry args={[3.4, 3.4, 3, 32]} />{materials.glass}</mesh>
        <mesh position={[0, 0.1, 0]} receiveShadow><cylinderGeometry args={[3.6, 3.6, 0.2, 32]} /><meshStandardMaterial color={hovered || isActive ? "#a0a0a0" : "#8e8e8e"} roughness={0.9} /></mesh>
        {Array.from({ length: 24 }).map((_, i) => (
          <mesh key={`rot-mullion-${i}`} position={[0, 1.5, 0]} rotation={[0, (i * Math.PI) / 12, 0]} castShadow>
            <boxGeometry args={[7.0, 3, 0.15]} />{materials.wall}
          </mesh>
        ))}
        {[1, 2].map(y => (
          <mesh key={`ring-${y}`} position={[0, y, 0]} castShadow><cylinderGeometry args={[3.55, 3.55, 0.1, 32]} />{materials.frame}</mesh>
        ))}
        <mesh position={[0, 3.1, 0]} castShadow receiveShadow><cylinderGeometry args={[3.7, 3.7, 0.2, 32]} />{materials.roof}</mesh>
      </group>
      {hasCritical && <CriticalBadge yOffset={6} />}
      <Text position={[0, 4.8, 0]} fontSize={0.8} color={hasCritical ? '#ef4444' : '#1b1b23'} anchorX="center" anchorY="middle" outlineWidth={0.05} outlineColor="#ffffff">
        {name}
      </Text>
    </group>
  );
}

export default function ThreeDMap({ onBuildingClick, activeBuilding, criticalBuildings = [] }) {
  return (
    <div className="absolute inset-0">
      <Canvas shadows camera={{ position: [0, 8, 12], fov: 45 }}>
        <Sky sunPosition={[10, 20, 10]} turbidity={0.3} rayleigh={0.5} />
        <Environment preset="city" />
        <ambientLight intensity={0.4} />
        <directionalLight position={[10, 20, 10]} intensity={1.2} castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-15} shadow-camera-right={15} shadow-camera-top={15} shadow-camera-bottom={-15} shadow-bias={-0.0001} />

        <EngineeringBuilding position={[-10, 0, -4]} name="Mühendislik 1" onClick={onBuildingClick} isActive={activeBuilding === "Mühendislik 1"} hasCritical={criticalBuildings.includes("Mühendislik 1")} variant={1} />
        <EngineeringBuilding position={[0, 0, 5]} name="Mühendislik 2" onClick={onBuildingClick} isActive={activeBuilding === "Mühendislik 2"} hasCritical={criticalBuildings.includes("Mühendislik 2")} variant={2} />
        <AKMBuilding position={[12, 0, -2]} name="AKM" onClick={onBuildingClick} isActive={activeBuilding === "AKM"} hasCritical={criticalBuildings.includes("AKM")} />

        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow><planeGeometry args={[100, 100]} /><meshStandardMaterial color="#8b9d77" roughness={1} /></mesh>
        
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[1, 0.01, 0]} receiveShadow><planeGeometry args={[26, 3]} /><meshStandardMaterial color="#666666" roughness={0.9} /></mesh>
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[-10, 0.01, -1.5]} receiveShadow><planeGeometry args={[3, 4]} /><meshStandardMaterial color="#666666" roughness={0.9} /></mesh>
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 2.5]} receiveShadow><planeGeometry args={[3, 4]} /><meshStandardMaterial color="#666666" roughness={0.9} /></mesh>
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[10, 0.01, -1]} receiveShadow><planeGeometry args={[3, 5]} /><meshStandardMaterial color="#666666" roughness={0.9} /></mesh>

        <Tree position={[-5, 0, 2]} scale={1.2} />
        <Tree position={[-6, 0, -1]} scale={0.9} />
        <Tree position={[-13, 0, -1]} scale={1.1} />
        <Tree position={[-8, 0, 3]} scale={0.8} />
        <Tree position={[4, 0, 2]} scale={1.3} />
        <Tree position={[6, 0, -3]} scale={1.0} />
        <Tree position={[8, 0, 4]} scale={1.2} />
        <Tree position={[15, 0, 2]} scale={0.9} />
        <Tree position={[14, 0, -6]} scale={1.1} />
        <Tree position={[-2, 0, -4]} scale={1.0} />
        <Tree position={[2, 0, -2]} scale={0.8} />
        <Tree position={[-12, 0, -6]} scale={1.3} />

        <ContactShadows resolution={1024} scale={30} blur={2} opacity={0.5} far={10} color="#1a202c" />
        <OrbitControls makeDefault minPolarAngle={0} maxPolarAngle={Math.PI / 2 - 0.05} minDistance={5} maxDistance={30} />
      </Canvas>
    </div>
  );
}
