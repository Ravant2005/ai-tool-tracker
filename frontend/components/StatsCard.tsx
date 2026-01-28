'use client';

import { LucideIcon } from 'lucide-react';
import { motion } from 'framer-motion';

interface StatsCardProps {
    icon: LucideIcon;
    label: string;
    value: number | string;
    color?: 'purple';
}

export default function StatsCard({ icon: Icon, label, value, color = "purple" }: StatsCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
            whileHover={{ scale: 1.03, y: -2 }}
            className="bg-white rounded-xl p-6 shadow-sm hover:shadow-lg transition-all duration-200 border-l-4 border-[#F4C430]"
        >
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm font-medium text-gray-600 mb-2">{label}</p>
                    <p className="text-3xl font-bold text-[#5B2D8B]">{value}</p>
                </div>
                <div className="bg-[#5B2D8B]/10 p-3 rounded-lg">
                    <Icon className="w-7 h-7 text-[#5B2D8B]" />
                </div>
            </div>
        </motion.div>
    );
}