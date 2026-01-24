"""
GitHub Trending Scraper
Finds trending AI repositories on GitHub
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubScraper:
    """
    Scrapes GitHub Trending page for AI projects
    """
    
    def __init__(self):
        self.base_url = "https://github.com/trending"
        self.headers = {
            'User-Agent': os.getenv('USER_AGENT', 
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        }
    
    def scrape_trending_ai_repos(self, language: str = "python") -> List[Dict]:
        """
        Scrape GitHub trending repos
        
        Args:
            language: Programming language filter (default: python)
        
        Returns:
            List of trending repositories with their data
        """
        logger.info(f"🔍 Scraping GitHub Trending ({language})...")
        
        try:
            # Build URL with language and "ai" topic filter
            url = f"{self.base_url}/{language}?since=daily"
            logger.debug(f"GitHub URL: {url}")
            
            # Make request
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            logger.info(f"✅ GitHub HTTP {response.status_code}")
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all repository cards
            repos = []
            repo_articles = soup.find_all('article', class_='Box-row')
            
            logger.info(f"📊 Found {len(repo_articles)} total trending repos on page")
            
            if len(repo_articles) == 0:
                logger.warning("⚠️  No articles found - GitHub page structure may have changed")
            
            for idx, article in enumerate(repo_articles[:20], 1):  # Get top 20
                try:
                    repo_data = self._parse_repo_card(article)
                    
                    # Filter for AI-related repos
                    if self._is_ai_related(repo_data):
                        repos.append(repo_data)
                        logger.info(f"✅ [{idx}] AI repo: {repo_data['name']} | ⭐ {repo_data.get('stars', 0)}")
                    else:
                        logger.debug(f"[{idx}] Skipped (not AI): {repo_data['name']}")
                
                except Exception as e:
                    logger.error(f"❌ Error parsing repo #{idx}: {str(e)}")
                    continue
                
                # Be polite - small delay between processing
                time.sleep(0.5)
            
            logger.info(f"🎯 Found {len(repos)} AI-related repos out of {len(repo_articles)} total")
            return repos
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ HTTP Error scraping GitHub: {type(e).__name__}: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"❌ Error scraping GitHub: {type(e).__name__}: {str(e)}", exc_info=True)
            return []
    
    def _parse_repo_card(self, article) -> Dict:
        """
        Extract data from a single repository card
        
        Args:
            article: BeautifulSoup article element
        
        Returns:
            Dictionary with repo data
        """
        # Get repo name and URL
        h2 = article.find('h2', class_='h3')
        repo_link = h2.find('a')['href'] if h2 and h2.find('a') else ""
        repo_name = repo_link.strip('/').replace('/', '-') if repo_link else "Unknown"
        
        # Get description
        description_elem = article.find('p', class_='col-9')
        description = description_elem.get_text(strip=True) if description_elem else "No description"
        
        # Get stars
        stars_elem = article.find('svg', {'aria-label': 'star'})
        stars = 0
        if stars_elem and stars_elem.parent:
            stars_text = stars_elem.parent.get_text(strip=True)
            stars = self._parse_star_count(stars_text)
        
        # Get language
        language_elem = article.find('span', {'itemprop': 'programmingLanguage'})
        language = language_elem.get_text(strip=True) if language_elem else "Unknown"
        
        # Get today's stars
        today_stars_elem = article.find('span', class_='float-sm-right')
        today_stars = 0
        if today_stars_elem:
            today_text = today_stars_elem.get_text(strip=True)
            today_stars = self._parse_star_count(today_text.split()[0])
        
        return {
            'name': repo_name,
            'url': f"https://github.com{repo_link}",
            'description': description,
            'stars': stars,
            'language': language,
            'today_stars': today_stars,
            'source': 'github'
        }
    
    def _parse_star_count(self, text: str) -> int:
        """
        Convert star count text to integer
        Examples: "1.2k" -> 1200, "523" -> 523
        
        Args:
            text: Star count as string
        
        Returns:
            Integer star count
        """
        try:
            text = text.strip().replace(',', '')
            if 'k' in text.lower():
                return int(float(text.lower().replace('k', '')) * 1000)
            return int(text)
        except:
            return 0
    
    def _is_ai_related(self, repo_data: Dict) -> bool:
        """
        Check if repository is AI/ML related
        
        Args:
            repo_data: Repository data dictionary
        
        Returns:
            True if AI-related, False otherwise
        """
        # AI-related keywords
        ai_keywords = [
            'ai', 'ml', 'machine learning', 'deep learning',
            'neural', 'llm', 'gpt', 'chatbot', 'transformer',
            'nlp', 'computer vision', 'opencv', 'tensorflow',
            'pytorch', 'model', 'diffusion', 'stable diffusion',
            'huggingface', 'langchain', 'agent', 'rag'
        ]
        
        # Check in name and description
        text = f"{repo_data['name']} {repo_data['description']}".lower()
        
        return any(keyword in text for keyword in ai_keywords)

# Create scraper instance
github_scraper = GitHubScraper()