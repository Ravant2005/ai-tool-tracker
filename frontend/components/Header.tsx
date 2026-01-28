'use client';

import { Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Header() {
    return (
        <header className="relative bg-gradient-to-r from-[#5B2D8B] to-[#3A1C6B] text-white shadow-lg overflow-hidden">
            <motion.div
                className="absolute inset-0 bg-gradient-to-r from-[#5B2D8B]/20 to-[#3A1C6B]/20"
                animate={{
                    backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
                }}
                transition={{
                    duration: 10,
                    repeat: Infinity,
                    ease: 'linear',
                }}
                style={{ backgroundSize: '200% 200%' }}
            />
            <div className="container mx-auto px-4 py-6 relative z-10">
                <motion.div
                    className="flex items-center justify-between"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <div className="flex items-center space-x-3">
                        <motion.div
                            className="bg-white p-2 rounded-lg shadow-lg"
                            whileHover={{ scale: 1.1, rotate: 5 }}
                            transition={{ type: 'spring', stiffness: 300 }}
                        >
                            <Sparkles className="w-6 h-6 text-[#F4C430]" />
                        </motion.div>
                        <div>
                            <h1 className="text-2xl font-bold">AI Tool Tracker</h1>
                            <p className="text-sm text-white/80">
                                Discover trending AI tools daily
                            </p>
                        </div>
                    </div>
                </motion.div>
            </div>
        </header>
    );
}