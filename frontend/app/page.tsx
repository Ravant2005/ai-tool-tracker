'use client';

import { useState, useEffect } from 'react';
import { Loader2, Sparkles, TrendingUp, Package, Target } from 'lucide-react';
import { motion } from 'framer-motion';
import dynamic from 'next/dynamic';

// Import components
import Header from '@/components/Header';
import StatsCard from '@/components/StatsCard';
import FilterBar from '@/components/FilterBar';
import ToolCard from '@/components/ToolCard';

// Lazy load 3D background
const AnimatedBackground = dynamic(() => import('@/components/AnimatedBackground'), {
    ssr: false,
    loading: () => null,
});

// Import API functions
import { getAllTools, getTrendingTools, getStats, getCategories } from '@/lib/api';

// Force dynamic rendering - prevent static generation
export const dynamic = 'force-dynamic';

export default function Home() {
    const [tools, setTools] = useState<any[]>([]);
    const [trendingTools, setTrendingTools] = useState<any[]>([]);
    const [stats, setStats] = useState({
        total_tools: 0,
        new_today: 0,
        avg_hype_score: 0,
        top_category: 'N/A'
    });
    const [categories, setCategories] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedPricing, setSelectedPricing] = useState('');
    
    useEffect(() => {
        fetchAllData();
    }, []);
    
    useEffect(() => {
        fetchTools();
    }, [selectedCategory, selectedPricing]);
    
    const fetchAllData = async () => {
        setLoading(true);
        try {
            const [toolsData, trendingData, statsData, categoriesData] = await Promise.all([
                getAllTools(),
                getTrendingTools(),
                getStats(),
                getCategories()
            ]);
            setTools(toolsData);
            setTrendingTools(trendingData);
            setStats(statsData);
            setCategories(categoriesData);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };
    
    const fetchTools = async () => {
        const toolsData = await getAllTools({
            category: selectedCategory,
            pricing: selectedPricing
        });
        setTools(toolsData);
    };
    
    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center">
                <div className="text-center">
                    <Loader2 className="w-12 h-12 text-purple-600 animate-spin mx-auto mb-4" />
                    <p className="text-gray-600">Loading AI tools...</p>
                </div>
            </div>
        );
    }
    
    return (
        <div className="min-h-screen relative">
            <AnimatedBackground />
            <Header />
            
            <main className="container mx-auto px-4 py-10">
                <section className="mb-16">
                    <h2 className="text-3xl font-bold text-gray-900 mb-8">Dashboard Overview</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                        <StatsCard icon={Package} label="Total AI Tools" value={stats.total_tools} color="blue" />
                        <StatsCard icon={Sparkles} label="New Today" value={stats.new_today} color="purple" />
                        <StatsCard icon={TrendingUp} label="Avg Hype Score" value={stats.avg_hype_score} color="green" />
                        <StatsCard icon={Target} label="Top Category" value={stats.top_category} color="orange" />
                    </div>
                </section>
                
                {trendingTools.length > 0 && (
                    <section className="mb-16">
                        <motion.div
                            className="flex items-center mb-8"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5 }}
                        >
                            <TrendingUp className="w-7 h-7 text-purple-600 mr-3" />
                            <h2 className="text-3xl font-bold text-gray-900">Trending Today</h2>
                        </motion.div>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                            {trendingTools.slice(0, 6).map((tool, index) => (
                                <motion.div
                                    key={tool.id}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.4, delay: index * 0.1 }}
                                >
                                    <ToolCard tool={tool} />
                                </motion.div>
                            ))}
                        </div>
                    </section>
                )}
                
                <FilterBar
                    categories={categories}
                    selectedCategory={selectedCategory}
                    onCategoryChange={setSelectedCategory}
                    selectedPricing={selectedPricing}
                    onPricingChange={setSelectedPricing}
                />
                
                <section>
                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-3xl font-bold text-gray-900">All AI Tools</h2>
                        <span className="text-gray-600 font-medium">{tools.length} tools found</span>
                    </div>
                    
                    {tools.length === 0 ? (
                        <div className="bg-white rounded-xl shadow-sm p-12 text-center border border-gray-200">
                            <p className="text-gray-600 mb-4 text-lg">No tools found</p>
                            <button
                                onClick={() => { setSelectedCategory(''); setSelectedPricing(''); }}
                                className="px-6 py-2.5 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium"
                            >
                                Clear Filters
                            </button>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                            {tools.map((tool) => <ToolCard key={tool.id} tool={tool} />)}
                        </div>
                    )}
                </section>
            </main>
            
            <footer className="bg-gray-900 text-white py-12 mt-20 relative z-10">
                <div className="container mx-auto px-4">
                    <motion.div
                        className="flex flex-col items-center justify-center space-y-4"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                    >
                        <p className="text-gray-300 text-lg font-medium text-center">
                            One platform. Always updated. Discover the AI tools that matter.
                        </p>
                        <motion.a
                            href="https://www.linkedin.com/in/s-ravant-vignesh-384b01373/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-gray-800 hover:bg-blue-600 transition-colors duration-200"
                            aria-label="LinkedIn Profile"
                            whileHover={{ scale: 1.15, rotate: 5 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                            </svg>
                        </motion.a>
                    </motion.div>
                </div>
            </footer>
        </div>
    );
}