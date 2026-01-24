"""
Product Hunt Scraper
Finds new AI product launches
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductHuntScraper:
    """
    Scrapes Product Hunt for AI product launches
    """
    
    def __init__(self):
        self.base_url = "https://www.producthunt.com"
        self.headers = {
            'User-Agent': os.getenv('USER_AGENT',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        }
    
    def scrape_ai_products(self) -> List[Dict]:
        """
        Scrape today's AI product launches from Product Hunt
        
        Returns:
            List of AI products with their data
        """
        logger.info("🔍 Scraping Product Hunt for AI products...")
        
        try:
            # Product Hunt homepage shows today's launches
            url = f"{self.base_url}/topics/artificial-intelligence"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            products = []
            
            # Find product cards (Note: PH structure changes often)
            # This is a simplified scraper - real implementation might need updates
            product_links = soup.find_all('a', href=True)
            
            visited_urls = set()
            
            for link in product_links[:30]:  # Check first 30 links
                href = link.get('href', '')
                
                # Product Hunt URLs look like: /posts/product-name
                if '/posts/' in href and href not in visited_urls:
                    visited_urls.add(href)
                    
                    try:
                        product_data = self._scrape_product_page(href)
                        if product_data and self._is_ai_related(product_data):
                            products.append(product_data)
                            logger.info(f"✅ Found AI product: {product_data['name']}")
                    
                    except Exception as e:
                        logger.error(f"Error scraping product: {str(e)}")
                        continue
                    
                    # Be polite
                    time.sleep(1)
                    
                    # Limit to 10 products per run
                    if len(products) >= 10:
                        break
            
            logger.info(f"✅ Found {len(products)} AI products")
            return products
        
        except Exception as e:
            logger.error(f"❌ Error scraping Product Hunt: {str(e)}")
            return []
    
    def _scrape_product_page(self, product_url: str) -> Dict:
        """
        Scrape individual product page
        
        Args:
            product_url: Relative URL of product page
        
        Returns:
            Product data dictionary
        """
        full_url = f"{self.base_url}{product_url}"
        
        response = requests.get(full_url, headers=self.headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract product name from URL
        product_name = product_url.split('/posts/')[1] if '/posts/' in product_url else "Unknown"
        product_name = product_name.replace('-', ' ').title()
        
        # Try to find description (meta tag)
        description = ""
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '')
        
        # Try to find tagline
        if not description:
            # Look for h1 or main heading
            h1 = soup.find('h1')
            if h1:
                description = h1.get_text(strip=True)
        
        return {
            'name': product_name,
            'url': full_url,
            'description': description or "AI product from Product Hunt",
            'source': 'producthunt',
            'upvotes': 0  # Would need more complex scraping for real upvotes
        }
    
    def _is_ai_related(self, product_data: Dict) -> bool:
        """
        Check if product is AI-related
        
        Args:
            product_data: Product data dictionary
        
        Returns:
            True if AI-related, False otherwise
        """
        ai_keywords = [
            'ai', 'artificial intelligence', 'ml', 'machine learning',
            'chatbot', 'gpt', 'llm', 'neural', 'deep learning',
            'automation', 'smart', 'intelligent', 'assistant',
            'generative', 'model', 'nlp', 'computer vision'
        ]
        
        text = f"{product_data['name']} {product_data['description']}".lower()
        
        return any(keyword in text for keyword in ai_keywords)

# Create scraper instance
producthunt_scraper = ProductHuntScraper()