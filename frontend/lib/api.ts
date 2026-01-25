import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

if (!API_BASE_URL) {
    throw new Error('NEXT_PUBLIC_API_BASE_URL environment variable is required');
}

// Log the resolved API base URL for debugging
console.log('🔗 API Base URL:', API_BASE_URL);

interface ToolFilters {
    category?: string;
    pricing?: string;
    limit?: number;
}

export async function getAllTools(filters: ToolFilters = {}) {
    try {
        const params = new URLSearchParams();
        if (filters.category) params.append('category', filters.category);
        if (filters.pricing) params.append('pricing', filters.pricing);
        if (filters.limit) params.append('limit', filters.limit.toString());
        
        const response = await axios.get(`${API_BASE_URL}/api/tools?${params}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching tools:', error);
        return [];
    }
}

export async function getTrendingTools() {
    try {
        const response = await axios.get(`${API_BASE_URL}/api/tools/trending`);
        return response.data;
    } catch (error) {
        console.error('Error fetching trending tools:', error);
        return [];
    }
}

export async function getStats() {
    try {
        const response = await axios.get(`${API_BASE_URL}/api/stats`);
        return response.data;
    } catch (error) {
        console.error('Error fetching stats:', error);
        return { total_tools: 0, new_today: 0, avg_hype_score: 0, top_category: 'N/A' };
    }
}

export async function getCategories() {
    try {
        const response = await axios.get(`${API_BASE_URL}/api/categories`);
        return response.data;
    } catch (error) {
        console.error('Error fetching categories:', error);
        return [];
    }
}