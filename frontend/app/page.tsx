'use client';

import { useState, useEffect } from 'react';
import { Loader2, Sparkles, TrendingUp, Package, Target } from 'lucide-react';

// Import components
import Header from '@/components/Header';
import StatsCard from '@/components/StatsCard';
import FilterBar from '@/components/FilterBar';
import ToolCard from '@/components/ToolCard';

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
        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
            <Header />
            
            <main className="container mx-auto px-4 py-8">
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-gray-900 mb-6">Dashboard Overview</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <StatsCard icon={Package} label="Total AI Tools" value={stats.total_tools} color="blue" />
                        <StatsCard icon={Sparkles} label="New Today" value={stats.new_today} color="purple" />
                        <StatsCard icon={TrendingUp} label="Avg Hype Score" value={stats.avg_hype_score} color="green" />
                        <StatsCard icon={Target} label="Top Category" value={stats.top_category} color="orange" />
                    </div>
                </section>
                
                {trendingTools.length > 0 && (
                    <section className="mb-12">
                        <div className="flex items-center mb-6">
                            <TrendingUp className="w-6 h-6 text-purple-600 mr-2" />
                            <h2 className="text-2xl font-bold text-gray-900">Trending Today</h2>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {trendingTools.slice(0, 6).map((tool) => (
                                <ToolCard key={tool.id} tool={tool} />
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
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-2xl font-bold text-gray-900">All AI Tools</h2>
                        <span className="text-gray-600">{tools.length} tools found</span>
                    </div>
                    
                    {tools.length === 0 ? (
                        <div className="bg-white rounded-xl shadow-md p-12 text-center">
                            <p className="text-gray-600 mb-4">No tools found</p>
                            <button
                                onClick={() => { setSelectedCategory(''); setSelectedPricing(''); }}
                                className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
                            >
                                Clear Filters
                            </button>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {tools.map((tool) => <ToolCard key={tool.id} tool={tool} />)}
                        </div>
                    )}
                </section>
            </main>
            
            <footer className="bg-gray-900 text-white py-8 mt-16">
                <div className="container mx-auto px-4 text-center">
                    <p className="text-gray-400">For feedback or contributions, mail us at:messiahravant@gmail.com</p>
                </div>
            </footer>
        </div>
    );
}