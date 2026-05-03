import { OrbitControls, Text, Edges, Environment, Sky } from '@react-three/drei';
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

// Bush Component
function Bush({ position, scale = 1 }) {
  return (
    <group position={position} scale={[scale, scale, scale]}>
      <mesh position={[0, 0.25, 0]} castShadow receiveShadow>
        <sphereGeometry args={[0.4, 12, 12]} />
        {materials.treeLeaves}
      </mesh>
      <mesh position={[0.3, 0.2, 0.1]} castShadow receiveShadow>
        <sphereGeometry args={[0.28, 8, 8]} />
        {materials.treeLeaves}
      </mesh>
      <mesh position={[-0.25, 0.18, 0.05]} castShadow receiveShadow>
        <sphereGeometry args={[0.22, 8, 8]} />
        {materials.treeLeaves}
      </mesh>
    </group>
  );
}

// Round Tree (wider canopy variety)
function RoundTree({ position, scale = 1 }) {
  return (
    <group position={position} scale={[scale, scale, scale]}>
      <mesh position={[0, 0.6, 0]} castShadow receiveShadow>
        <cylinderGeometry args={[0.18, 0.25, 1.2, 8]} />
        {materials.treeTrunk}
      </mesh>
      <mesh position={[0, 2.0, 0]} castShadow receiveShadow>
        <sphereGeometry args={[1.1, 12, 12]} />
        <meshStandardMaterial color="#3a7d35" roughness={0.8} />
      </mesh>
    </group>
  );
}

// Bench Component
function Bench({ position, rotation = [0, 0, 0], scale = 1 }) {
  return (
    <group position={position} rotation={rotation} scale={[scale, scale, scale]}>
      <mesh position={[0, 0.25, 0]} castShadow receiveShadow>
        <boxGeometry args={[1.2, 0.05, 0.4]} />
        <meshStandardMaterial color="#8b5a2b" roughness={0.9} />
      </mesh>
      <mesh position={[0, 0.5, -0.15]} rotation={[-0.1, 0, 0]} castShadow receiveShadow>
        <boxGeometry args={[1.2, 0.3, 0.05]} />
        <meshStandardMaterial color="#8b5a2b" roughness={0.9} />
      </mesh>
      <mesh position={[-0.5, 0.125, 0]} castShadow receiveShadow>
        <boxGeometry args={[0.1, 0.25, 0.3]} />
        <meshStandardMaterial color="#2d2d2d" roughness={0.8} />
      </mesh>
      <mesh position={[0.5, 0.125, 0]} castShadow receiveShadow>
        <boxGeometry args={[0.1, 0.25, 0.3]} />
        <meshStandardMaterial color="#2d2d2d" roughness={0.8} />
      </mesh>
    </group>
  );
}

// Street Lamp
function StreetLamp({ position }) {
  return (
    <group position={position}>
      <mesh position={[0, 1.5, 0]} castShadow>
        <cylinderGeometry args={[0.06, 0.09, 3, 8]} />
        <meshStandardMaterial color="#444444" roughness={0.5} metalness={0.6} />
      </mesh>
      <mesh position={[0.35, 3.1, 0]} castShadow>
        <cylinderGeometry args={[0.05, 0.05, 0.7, 8]} />
        <meshStandardMaterial color="#444444" roughness={0.5} metalness={0.6} />
      </mesh>
      <mesh position={[0.7, 3.1, 0]} castShadow>
        <sphereGeometry args={[0.18, 10, 10]} />
        <meshStandardMaterial color="#fffde7" emissive="#fffacd" emissiveIntensity={1.5} roughness={0.2} />
      </mesh>
    </group>
  );
}


// Sports Field (basketball court / multipurpose)
function SportsField({ position, rotation = [0, 0, 0] }) {
  return (
    <group position={position} rotation={rotation}>
      {/* Court surface */}
      <mesh position={[0, 0.02, 0]} receiveShadow>
        <boxGeometry args={[8, 0.04, 14]} />
        <meshStandardMaterial color="#c0392b" roughness={0.9} />
      </mesh>
      {/* Court lines */}
      <mesh position={[0, 0.05, 0]} receiveShadow>
        <boxGeometry args={[8.2, 0.01, 0.1]} />
        <meshStandardMaterial color="#ffffff" roughness={1} />
      </mesh>
      <mesh position={[0, 0.05, 0]} rotation={[0, Math.PI / 2, 0]} receiveShadow>
        <boxGeometry args={[14.2, 0.01, 0.1]} />
        <meshStandardMaterial color="#ffffff" roughness={1} />
      </mesh>
      {/* Hoops */}
      {[-6.5, 6.5].map((z, i) => (
        <group key={i} position={[0, 0, z]}>
          <mesh position={[0, 1.5, 0]} castShadow>
            <cylinderGeometry args={[0.06, 0.06, 3, 8]} />
            <meshStandardMaterial color="#555555" metalness={0.6} roughness={0.4} />
          </mesh>
          <mesh position={[0, 3.1, 0.45]} castShadow>
            <torusGeometry args={[0.23, 0.035, 8, 24]} />
            <meshStandardMaterial color="#e65100" roughness={0.4} metalness={0.3} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

// Parking Lot
function ParkingLot({ position, rotation = [0, 0, 0] }) {
  const spots = [];
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 5; col++) {
      spots.push([col * 2.2 - 4.4, row]);
    }
  }
  return (
    <group position={position} rotation={rotation}>
      {/* Asphalt */}
      <mesh position={[0, 0.01, 0]} receiveShadow>
        <boxGeometry args={[13, 0.02, 10]} />
        <meshStandardMaterial color="#4a4a4a" roughness={0.95} />
      </mesh>
      {/* Parking lines */}
      {spots.map(([x, row], i) => (
        <mesh key={i} position={[x, 0.03, (row - 0.5) * 4]} receiveShadow>
          <boxGeometry args={[1.8, 0.01, 0.08]} />
          <meshStandardMaterial color="#ffffff" roughness={1} />
        </mesh>
      ))}
      {/* A few car silhouettes */}
      {[[-4.4, 0, -2], [-2.2, 0, -2], [0, 0, -2], [2.2, 0, 2], [-2.2, 0, 2]].map(([x, y, z], i) => (
        <group key={`car-${i}`} position={[x, 0.2, z]}>
          <mesh castShadow>
            <boxGeometry args={[1.6, 0.4, 3.2]} />
            <meshStandardMaterial color={['#1a237e', '#4e342e', '#1b5e20', '#37474f', '#880e4f'][i]} roughness={0.3} metalness={0.5} />
          </mesh>
          <mesh position={[0, 0.32, 0]} castShadow>
            <boxGeometry args={[1.4, 0.3, 1.8]} />
            <meshStandardMaterial color={['#1a237e', '#4e342e', '#1b5e20', '#37474f', '#880e4f'][i]} roughness={0.3} metalness={0.5} />
          </mesh>
        </group>
      ))}
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
      <Canvas camera={{ position: [0, 18, 28], fov: 48 }}>
        <Sky sunPosition={[10, 20, 10]} turbidity={0.3} rayleigh={0.5} />
        <Environment preset="city" />
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 20, 10]} intensity={1.3} castShadow />
        <directionalLight position={[-15, 12, -10]} intensity={0.4} />

        {/* ── Ana binalar ─────────────────────── */}
        <EngineeringBuilding position={[-10, 0, -4]} name="Mühendislik 1" onClick={onBuildingClick} isActive={activeBuilding === "Mühendislik 1"} hasCritical={criticalBuildings.includes("Mühendislik 1")} variant={1} />
        <EngineeringBuilding position={[0, 0, 5]} name="Mühendislik 2" onClick={onBuildingClick} isActive={activeBuilding === "Mühendislik 2"} hasCritical={criticalBuildings.includes("Mühendislik 2")} variant={2} />
        <AKMBuilding position={[12, 0, -2]} name="AKM" onClick={onBuildingClick} isActive={activeBuilding === "AKM"} hasCritical={criticalBuildings.includes("AKM")} />



        {/* ── Zemin ───────────────────────────── */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
          <planeGeometry args={[140, 140]} />
          <meshStandardMaterial color="#7a9265" roughness={1} />
        </mesh>

        {/* ── Yollar ──────────────────────────── */}
        {/* Ana yatay cadde */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]}>
          <planeGeometry args={[80, 3.5]} />
          <meshStandardMaterial color="#5a5a5a" roughness={0.9} />
        </mesh>
        {/* Dikey cadde */}
        <mesh rotation={[-Math.PI/2, 0, Math.PI/2]} position={[0, 0.01, 0]}>
          <planeGeometry args={[60, 3.5]} />
          <meshStandardMaterial color="#5a5a5a" roughness={0.9} />
        </mesh>
        {/* Yan yol - sol */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[-10, 0.01, -2]}>
          <planeGeometry args={[3, 6]} />
          <meshStandardMaterial color="#666666" roughness={0.9} />
        </mesh>
        {/* Yan yol - orta */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 3]}>
          <planeGeometry args={[3, 5]} />
          <meshStandardMaterial color="#666666" roughness={0.9} />
        </mesh>
        {/* Yan yol - sağ */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[12, 0.01, -1]}>
          <planeGeometry args={[3, 5]} />
          <meshStandardMaterial color="#666666" roughness={0.9} />
        </mesh>

        {/* ── Sokak lambaları (yol boyunca) ───── */}
        <StreetLamp position={[-18, 0, 1.5]} />
        <StreetLamp position={[-12, 0, 1.5]} />
        <StreetLamp position={[ -6, 0, 1.5]} />
        <StreetLamp position={[  0, 0, 1.5]} />
        <StreetLamp position={[  6, 0, 1.5]} />
        <StreetLamp position={[ 12, 0, 1.5]} />
        <StreetLamp position={[ 18, 0, 1.5]} />
        <StreetLamp position={[-18, 0,-1.5]} />
        <StreetLamp position={[-12, 0,-1.5]} />
        <StreetLamp position={[  6, 0,-1.5]} />
        <StreetLamp position={[ 18, 0,-1.5]} />
        {/* Dikey yol lambaları */}
        <StreetLamp position={[ 1.5, 0,-8]} />
        <StreetLamp position={[ 1.5, 0,-14]} />
        <StreetLamp position={[ 1.5, 0, 10]} />
        <StreetLamp position={[ 1.5, 0, 16]} />

        {/* ── Çam ağaçları (kampüs genelinde) ── */}
        {/* Mühendislik 1 çevresi */}
        <Tree position={[-5, 0, 2]}   scale={1.2} />
        <Tree position={[-6, 0, -1]}  scale={0.9} />
        <Tree position={[-13, 0, -1]} scale={1.1} />
        <Tree position={[-8, 0, 3]}   scale={0.8} />
        {/* Mühendislik 2 çevresi */}
        <Tree position={[4, 0, 2]}    scale={1.3} />
        <Tree position={[6, 0, -3]}   scale={1.0} />
        <Tree position={[8, 0, 4]}    scale={1.2} />
        {/* AKM çevresi */}
        <Tree position={[15, 0, 2]}   scale={0.9} />
        <Tree position={[14, 0, -6]}  scale={1.1} />
        {/* Genel kampüs - uzak köşeler */}
        <Tree position={[-2, 0, -4]}  scale={1.0} />
        <Tree position={[2, 0, -2]}   scale={0.8} />
        <Tree position={[-12, 0, -6]} scale={1.3} />
        <Tree position={[-20, 0,  5]} scale={1.1} />
        <Tree position={[-25, 0,  0]} scale={1.3} />
        <Tree position={[-25, 0, -5]} scale={0.9} />
        <Tree position={[-20, 0, 15]} scale={1.2} />
        <Tree position={[-15, 0, 22]} scale={1.0} />
        <Tree position={[ -5, 0, 22]} scale={1.4} />
        <Tree position={[  5, 0, 20]} scale={0.8} />
        <Tree position={[ 15, 0, 18]} scale={1.1} />
        <Tree position={[ 25, 0, 10]} scale={1.3} />
        <Tree position={[ 28, 0,  0]} scale={0.9} />
        <Tree position={[ 28, 0,-10]} scale={1.2} />
        <Tree position={[ 20, 0,-18]} scale={1.0} />
        <Tree position={[ 10, 0,-20]} scale={1.3} />
        <Tree position={[  0, 0,-22]} scale={1.1} />
        <Tree position={[-10, 0,-20]} scale={0.9} />
        <Tree position={[-20, 0,-16]} scale={1.2} />
        <Tree position={[-28, 0,-10]} scale={1.0} />
        <Tree position={[-28, 0,  8]} scale={1.3} />
        {/* Spor alanı çevresi */}
        <Tree position={[-30, 0,-18]} scale={1.1} />
        <Tree position={[-26, 0,-30]} scale={1.2} />
        <Tree position={[-18, 0,-30]} scale={0.9} />

        {/* ── Geniş yapraklı ağaçlar ──────────── */}
        <RoundTree position={[-3, 0, -12]}  scale={1.2} />
        <RoundTree position={[ 4, 0, -12]}  scale={1.0} />
        <RoundTree position={[-16, 0,  2]}  scale={1.1} />
        <RoundTree position={[ 18, 0, -5]}  scale={1.3} />
        <RoundTree position={[-7, 0, 12]}   scale={0.9} />
        <RoundTree position={[ 8, 0, 12]}   scale={1.2} />
        <RoundTree position={[-20, 0, -2]}  scale={1.0} />
        <RoundTree position={[ 22, 0, -8]}  scale={1.1} />
        <RoundTree position={[ 0,  0,  17]} scale={1.3} />
        <RoundTree position={[-13, 0, -15]} scale={1.0} />
        <RoundTree position={[ 12, 0, -14]} scale={1.2} />

        {/* ── Çalılar ─────────────────────────── */}
        <Bush position={[-2, 0, 1]}   scale={0.8} />
        <Bush position={[-1, 0, 1.2]} scale={1.2} />
        <Bush position={[4, 0, -1]}   scale={0.9} />
        <Bush position={[4.5, 0, -1.2]} scale={0.7} />
        <Bush position={[-8, 0, -2]}  scale={1.1} />
        <Bush position={[10, 0, 1]}   scale={1.3} />
        <Bush position={[-3, 0, -9]}  scale={1.0} />
        <Bush position={[3, 0, -9]}   scale={0.8} />
        <Bush position={[-6, 0, -11]} scale={1.2} />
        <Bush position={[6, 0, -11]}  scale={0.9} />
        <Bush position={[-18, 0,  4]} scale={1.0} />
        <Bush position={[-18, 0, -4]} scale={1.1} />
        <Bush position={[ 18, 0,  4]} scale={0.8} />
        <Bush position={[ 18, 0, -8]} scale={1.2} />
        <Bush position={[-10, 0, 14]} scale={1.0} />
        <Bush position={[ 10, 0, 14]} scale={0.9} />
        <Bush position={[ 0, 0, -16]} scale={1.1} />
        <Bush position={[-5, 0, 18]}  scale={1.3} />
        <Bush position={[ 5, 0, 18]}  scale={0.8} />
        <Bush position={[ 26, 0, 5]}  scale={1.0} />
        <Bush position={[ 26, 0,-5]}  scale={1.2} />
        <Bush position={[-26, 0, 5]}  scale={0.9} />

        {/* ── Banklar ─────────────────────────── */}
        {/* Plaza çevresi */}
        <Bench position={[-3.5, 0, -9]} rotation={[0, 0, 0]} />
        <Bench position={[1.5, 0, -9]}  rotation={[0, Math.PI, 0]} />
        <Bench position={[-1, 0, -4.5]} rotation={[0, Math.PI / 2, 0]} />
        {/* Yol kenarları */}
        <Bench position={[-3, 0, 2]}    rotation={[0, Math.PI / 4, 0]} />
        <Bench position={[3, 0, 2]}     rotation={[0, -Math.PI / 6, 0]} />
        <Bench position={[8, 0, 2]}     rotation={[0, 0, 0]} />
        <Bench position={[-8, 0, 2]}    rotation={[0, Math.PI, 0]} />
        <Bench position={[8, 0, -2]}    rotation={[0, Math.PI / 2, 0]} />
        {/* Kantin önü */}
        <Bench position={[-20, 0, -4]}  rotation={[0, Math.PI / 3, 0]} />
        <Bench position={[-20, 0, -2]}  rotation={[0, -Math.PI / 4, 0]} />
        {/* Spor alanı yanı */}
        <Bench position={[-28, 0, -20]} rotation={[0, Math.PI / 2, 0]} />
        <Bench position={[-28, 0, -24]} rotation={[0, Math.PI / 2, 0]} />

        <OrbitControls makeDefault minPolarAngle={0} maxPolarAngle={Math.PI / 2 - 0.05} minDistance={5} maxDistance={55} />
      </Canvas>
    </div>
  );
}

