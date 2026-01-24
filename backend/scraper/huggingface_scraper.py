"""
Hugging Face Scraper
Finds new AI models and spaces
"""

import requests
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceScraper:
    """
    Scrapes Hugging Face for trending AI models
    Uses their PUBLIC API (no authentication needed for basic data)
    """
    
    def __init__(self):
        self.api_base = "https://huggingface.co/api"
        self.site_base = "https://huggingface.co"
    
    def scrape_trending_models(self, limit: int = 20) -> List[Dict]:
        """
        Get trending AI models from Hugging Face
        
        Args:
            limit: Number of models to fetch
        
        Returns:
            List of model data
        """
        logger.info("🔍 Scraping Hugging Face models...")
        
        try:
            # Hugging Face API endpoint for models
            url = f"{self.api_base}/models"
            
            params = {
                'sort': 'trending',  # Get trending models
                'limit': limit,
                'full': 'true'  # Get full model info
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            models_data = response.json()
            
            models = []
            for model in models_data:
                try:
                    model_info = self._parse_model(model)
                    models.append(model_info)
                    logger.info(f"✅ Found model: {model_info['name']}")
                
                except Exception as e:
                    logger.error(f"Error parsing model: {str(e)}")
                    continue
            
            logger.info(f"✅ Found {len(models)} trending models")
            return models
        
        except Exception as e:
            logger.error(f"❌ Error scraping Hugging Face: {str(e)}")
            return []
    
    def scrape_trending_spaces(self, limit: int = 10) -> List[Dict]:
        """
        Get trending Spaces (demo apps) from Hugging Face
        
        Args:
            limit: Number of spaces to fetch
        
        Returns:
            List of space data
        """
        logger.info("🔍 Scraping Hugging Face Spaces...")
        
        try:
            url = f"{self.api_base}/spaces"
            
            params = {
                'sort': 'trending',
                'limit': limit,
                'full': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            spaces_data = response.json()
            
            spaces = []
            for space in spaces_data:
                try:
                    space_info = self._parse_space(space)
                    spaces.append(space_info)
                    logger.info(f"✅ Found space: {space_info['name']}")
                
                except Exception as e:
                    logger.error(f"Error parsing space: {str(e)}")
                    continue
            
            logger.info(f"✅ Found {len(spaces)} trending spaces")
            return spaces
        
        except Exception as e:
            logger.error(f"❌ Error scraping Spaces: {str(e)}")
            return []
    
    def _parse_model(self, model_data: dict) -> Dict:
        """
        Parse model data from API response
        
        Args:
            model_data: Raw model data from API
        
        Returns:
            Cleaned model info
        """
        model_id = model_data.get('id', 'unknown')
        
        return {
            'name': model_id,
            'url': f"{self.site_base}/{model_id}",
            'description': self._get_description(model_data),
            'likes': model_data.get('likes', 0),
            'downloads': model_data.get('downloads', 0),
            'tags': model_data.get('tags', []),
            'pipeline_tag': model_data.get('pipeline_tag', 'unknown'),
            'source': 'huggingface'
        }
    
    def _parse_space(self, space_data: dict) -> Dict:
        """
        Parse space data from API response
        
        Args:
            space_data: Raw space data from API
        
        Returns:
            Cleaned space info
        """
        space_id = space_data.get('id', 'unknown')
        
        return {
            'name': space_id,
            'url': f"{self.site_base}/spaces/{space_id}",
            'description': self._get_description(space_data),
            'likes': space_data.get('likes', 0),
            'sdk': space_data.get('sdk', 'unknown'),
            'tags': space_data.get('tags', []),
            'source': 'huggingface-space'
        }
    
    def _get_description(self, data: dict) -> str:
        """
        Extract description from model/space data
        
        Args:
            data: Model or space data
        
        Returns:
            Description string
        """
        # Try multiple fields for description
        description = (
            data.get('description') or
            data.get('cardData', {}).get('description') or
            f"AI model from Hugging Face"
        )
        
        return description[:500]  # Limit to 500 chars

# Create scraper instance
huggingface_scraper = HuggingFaceScraper()