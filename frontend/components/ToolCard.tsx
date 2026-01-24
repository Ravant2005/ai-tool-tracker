import { ExternalLink, Star, TrendingUp } from 'lucide-react';

interface Tool {
    id: number;
    name: string;
    description?: string;
    url: string;
    category?: string;
    hype_score?: number;
    github_stars?: number;
    pricing?: string;
    use_cases?: string[];
    source: string;
}

interface ToolCardProps {
    tool: Tool;
}

export default function ToolCard({ tool }: ToolCardProps) {
    const getHypeColor = (score?: number) => {
        if (!score) return 'text-gray-500';
        if (score >= 80) return 'text-red-500';
        if (score >= 60) return 'text-orange-500';
        if (score >= 40) return 'text-yellow-500';
        return 'text-gray-500';
    };
    
    const getPricingColor = (pricing?: string) => {
        switch (pricing) {
            case 'free': return 'bg-green-100 text-green-800';
            case 'freemium': return 'bg-blue-100 text-blue-800';
            case 'paid': return 'bg-purple-100 text-purple-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };
    
    return (
        <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100 hover:border-purple-200">
            <div className="p-6">
                <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-900 mb-1">
                            {tool.name}
                        </h3>
                        <span className="inline-block px-3 py-1 text-xs font-medium bg-gray-100 text-gray-700 rounded-full">
                            {tool.category || 'General AI'}
                        </span>
                    </div>
                    
                    <div className="flex items-center space-x-1 ml-2">
                        <TrendingUp className={`w-5 h-5 ${getHypeColor(tool.hype_score)}`} />
                        <span className={`text-lg font-bold ${getHypeColor(tool.hype_score)}`}>
                            {tool.hype_score || 0}
                        </span>
                    </div>
                </div>
                
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {tool.description || 'No description available'}
                </p>
                
                {tool.use_cases && tool.use_cases.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-4">
                        {tool.use_cases.slice(0, 3).map((useCase, index) => (
                            <span 
                                key={index}
                                className="px-2 py-1 text-xs bg-purple-50 text-purple-700 rounded"
                            >
                                {useCase}
                            </span>
                        ))}
                    </div>
                )}
                
                <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                    <span className={`px-3 py-1 text-xs font-medium rounded-full ${getPricingColor(tool.pricing)}`}>
                        {tool.pricing || 'unknown'}
                    </span>
                    
                    {tool.github_stars && tool.github_stars > 0 && (
                        <div className="flex items-center text-gray-600 text-sm">
                            <Star className="w-4 h-4 mr-1 fill-yellow-400 stroke-yellow-400" />
                            <span>{tool.github_stars.toLocaleString()}</span>
                        </div>
                    )}
                    
                    <a
                        href={tool.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center text-purple-600 hover:text-purple-700 text-sm font-medium"
                    >
                        Visit
                        <ExternalLink className="w-4 h-4 ml-1" />
                    </a>
                </div>
            </div>
            
            <div className="px-6 py-2 bg-gray-50 border-t border-gray-100">
                <span className="text-xs text-gray-500">
                    From: <span className="font-medium">{tool.source}</span>
                </span>
            </div>
        </div>
    );
}