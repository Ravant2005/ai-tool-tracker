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
        <div className="bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow duration-200 overflow-hidden border border-gray-200 hover:border-purple-300 h-full flex flex-col">
            <div className="p-6 flex-1 flex flex-col">
                <div className="flex items-start justify-between mb-4">
                    <div className="flex-1 min-w-0">
                        <h3 className="text-lg font-semibold text-gray-900 mb-2 truncate">
                            {tool.name}
                        </h3>
                        <span className="inline-block px-2.5 py-1 text-xs font-medium bg-purple-50 text-purple-700 rounded-md">
                            {tool.category || 'General AI'}
                        </span>
                    </div>
                    
                    <div className="flex items-center space-x-1 ml-3 flex-shrink-0">
                        <TrendingUp className={`w-4 h-4 ${getHypeColor(tool.hype_score)}`} />
                        <span className={`text-base font-semibold ${getHypeColor(tool.hype_score)}`}>
                            {tool.hype_score || 0}
                        </span>
                    </div>
                </div>
                
                <p className="text-gray-600 text-sm mb-4 line-clamp-3 flex-1">
                    {tool.description || 'No description available'}
                </p>
                
                {tool.use_cases && tool.use_cases.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mb-4">
                        {tool.use_cases.slice(0, 3).map((useCase, index) => (
                            <span 
                                key={index}
                                className="px-2 py-0.5 text-xs bg-gray-100 text-gray-700 rounded"
                            >
                                {useCase}
                            </span>
                        ))}
                    </div>
                )}
                
                <div className="flex items-center justify-between pt-4 mt-auto border-t border-gray-100">
                    <span className={`px-2.5 py-1 text-xs font-medium rounded-md ${getPricingColor(tool.pricing)}`}>
                        {tool.pricing || 'unknown'}
                    </span>
                    
                    {tool.github_stars && tool.github_stars > 0 && (
                        <div className="flex items-center text-gray-600 text-sm">
                            <Star className="w-3.5 h-3.5 mr-1 fill-yellow-400 stroke-yellow-400" />
                            <span className="text-xs font-medium">{tool.github_stars.toLocaleString()}</span>
                        </div>
                    )}
                    
                    <a
                        href={tool.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center text-purple-600 hover:text-purple-700 text-sm font-medium transition-colors"
                    >
                        Visit
                        <ExternalLink className="w-3.5 h-3.5 ml-1" />
                    </a>
                </div>
            </div>
            
            <div className="px-6 py-2.5 bg-gray-50 border-t border-gray-100">
                <span className="text-xs text-gray-500">
                    Source: <span className="font-medium text-gray-700">{tool.source}</span>
                </span>
            </div>
        </div>
    );
}