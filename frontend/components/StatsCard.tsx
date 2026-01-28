import { LucideIcon } from 'lucide-react';

interface StatsCardProps {
    icon: LucideIcon;
    label: string;
    value: number | string;
    color?: 'blue' | 'purple' | 'green' | 'orange';
}

export default function StatsCard({ icon: Icon, label, value, color = "blue" }: StatsCardProps) {
    const colorClasses = {
        blue: "from-blue-500 to-blue-600",
        purple: "from-purple-500 to-purple-600",
        green: "from-green-500 to-green-600",
        orange: "from-orange-500 to-orange-600"
    };
    
    return (
        <div className={`bg-gradient-to-br ${colorClasses[color]} rounded-xl p-6 text-white shadow-md hover:shadow-lg transition-shadow duration-200`}>
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm font-medium opacity-90 mb-2">{label}</p>
                    <p className="text-3xl font-bold">{value}</p>
                </div>
                <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                    <Icon className="w-7 h-7" />
                </div>
            </div>
        </div>
    );
}