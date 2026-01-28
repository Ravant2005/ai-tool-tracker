'use client';

import { Canvas } from '@react-three/fiber';
import { Float, Sphere } from '@react-three/drei';
import { Suspense } from 'react';

function FloatingOrbs() {
    return (
        <>
            <Float speed={1.5} rotationIntensity={0.5} floatIntensity={0.5}>
                <Sphere args={[0.5, 32, 32]} position={[-2, 1, -3]}>
                    <meshStandardMaterial color="#8b5cf6" opacity={0.3} transparent />
                </Sphere>
            </Float>
            <Float speed={2} rotationIntensity={0.3} floatIntensity={0.7}>
                <Sphere args={[0.3, 32, 32]} position={[2, -1, -2]}>
                    <meshStandardMaterial color="#3b82f6" opacity={0.3} transparent />
                </Sphere>
            </Float>
            <Float speed={1.8} rotationIntensity={0.4} floatIntensity={0.6}>
                <Sphere args={[0.4, 32, 32]} position={[0, 2, -4]}>
                    <meshStandardMaterial color="#06b6d4" opacity={0.3} transparent />
                </Sphere>
            </Float>
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} intensity={0.5} />
        </>
    );
}

export default function AnimatedBackground() {
    return (
        <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50" />
            <Suspense fallback={null}>
                <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
                    <FloatingOrbs />
                </Canvas>
            </Suspense>
        </div>
    );
}
