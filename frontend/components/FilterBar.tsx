import { Filter } from 'lucide-react';

interface Category {
    name: string;
    count: number;
}

interface FilterBarProps {
    categories: Category[];
    selectedCategory: string;
    onCategoryChange: (category: string) => void;
    selectedPricing: string;
    onPricingChange: (pricing: string) => void;
}

export default function FilterBar({ 
    categories, 
    selectedCategory, 
    onCategoryChange,
    selectedPricing,
    onPricingChange 
}: FilterBarProps) {
    const pricingOptions = ['all', 'free', 'freemium', 'paid'];
    
    return (
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
            <div className="flex items-center mb-4">
                <Filter className="w-5 h-5 text-purple-600 mr-2" />
                <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
            </div>
            
            <div className="grid md:grid-cols-2 gap-6">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Category
                    </label>
                    <select
                        value={selectedCategory}
                        onChange={(e) => onCategoryChange(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    >
                        <option value="">All Categories</option>
                        {categories.map((cat) => (
                            <option key={cat.name} value={cat.name}>
                                {cat.name} ({cat.count})
                            </option>
                        ))}
                    </select>
                </div>
                
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Pricing
                    </label>
                    <div className="flex gap-2">
                        {pricingOptions.map((option) => (
                            <button
                                key={option}
                                onClick={() => onPricingChange(option === 'all' ? '' : option)}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                                    (option === 'all' && !selectedPricing) || selectedPricing === option
                                        ? 'bg-purple-600 text-white'
                                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                            >
                                {option.charAt(0).toUpperCase() + option.slice(1)}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}