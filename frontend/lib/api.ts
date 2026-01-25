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
  const params = new URLSearchParams();

  if (filters.category) params.append('category', filters.category);
  if (filters.pricing) params.append('pricing', filters.pricing);
  if (filters.limit) params.append('limit', filters.limit.toString());

  const response = await axios.get(
    `${API_BASE_URL}/api/tools?${params.toString()}`
  );
  return response.data;
}

export async function getTrendingTools() {
  const response = await axios.get(
    `${API_BASE_URL}/api/tools/trending`
  );
  return response.data;
}

export async function getStats() {
  const response = await axios.get(
    `${API_BASE_URL}/api/stats`
  );
  return response.data;
}

export async function getCategories() {
  const response = await axios.get(
    `${API_BASE_URL}/api/categories`
  );
  return response.data;
}
