import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error(
    'NEXT_PUBLIC_API_BASE_URL is not defined. Check Vercel environment variables.'
  );
}

interface ToolFilters {
  category?: string;
  pricing?: string;
  limit?: number;
}

export async function getAllTools(filters: ToolFilters = {}) {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/tools`);
    let tools = response.data;

    // Normalize filters
    const category = filters.category?.trim();
    const pricing = filters.pricing?.trim().toLowerCase();

    // Client-side filtering
    if (category) {
      tools = tools.filter((tool: any) => tool.category === category);
    }

    if (pricing) {
      tools = tools.filter((tool: any) => 
        tool.pricing?.toLowerCase() === pricing
      );
    }

    if (filters.limit) {
      tools = tools.slice(0, filters.limit);
    }

    return tools;
  } catch (error) {
    console.error('Error fetching tools:', error);
    return [];
  }
}

export async function getTrendingTools() {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/tools/trending`
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching trending tools:', error);
    return [];
  }
}

export async function getStats() {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/stats`
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    return {
      total_tools: 0,
      new_today: 0,
      avg_hype_score: 0,
      top_category: 'N/A',
    };
  }
}

export async function getCategories() {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/categories`
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
    return [];
  }
}
