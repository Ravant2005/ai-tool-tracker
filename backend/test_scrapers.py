"""
Test Script for AI Tool Tracker Scrapers
Run this to verify each scraper is working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.huggingface_scraper import huggingface_scraper
from scraper.github_scraper import github_scraper
from scraper.producthunt_scraper import producthunt_scraper

import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_huggingface():
    """Test Hugging Face scraper"""
    logger.info("=" * 60)
    logger.info("TESTING HUGGING FACE SCRAPER")
    logger.info("=" * 60)
    
    # Test models
    logger.info("\nScraping trending models (limit=5)...")
    models = huggingface_scraper.scrape_trending_models(limit=5)
    logger.info(f"Models found: {len(models)}")
    
    if models:
        for m in models[:3]:
            logger.info(f"  - {m['name']} (likes: {m.get('likes', 0)})")
    
    # Test spaces
    logger.info("\nScraping trending spaces (limit=3)...")
    spaces = huggingface_scraper.scrape_trending_spaces(limit=3)
    logger.info(f"Spaces found: {len(spaces)}")
    
    if spaces:
        for s in spaces[:3]:
            logger.info(f"  - {s['name']} (likes: {s.get('likes', 0)})")
    
    return len(models) > 0 or len(spaces) > 0


def test_github():
    """Test GitHub scraper"""
    logger.info("\n" + "=" * 60)
    logger.info("TESTING GITHUB SCRAPER")
    logger.info("=" * 60)
    
    logger.info("\nScraping trending AI repos (Python, limit=10)...")
    repos = github_scraper.scrape_trending_ai_repos(language="python")
    logger.info(f"AI repos found: {len(repos)}")
    
    if repos:
        for r in repos[:5]:
            logger.info(f"  - {r['name']} (stars: {r.get('stars', 0)}, today: {r.get('today_stars', 0)})")
    
    return len(repos) > 0


def test_producthunt():
    """Test Product Hunt scraper"""
    logger.info("\n" + "=" * 60)
    logger.info("TESTING PRODUCT HUNT SCRAPER")
    logger.info("=" * 60)
    
    logger.info("\nScraping AI products from Product Hunt...")
    products = producthunt_scraper.scrape_ai_products()
    logger.info(f"AI products found: {len(products)}")
    
    if products:
        for p in products[:5]:
            logger.info(f"  - {p['name']} ({p['url']})")
    
    return len(products) > 0


def main():
    """Run all scraper tests"""
    logger.info("\n" + "#" * 60)
    logger.info("# AI TOOL TRACKER - SCRAPER TEST SUITE")
    logger.info("#" * 60)
    
    results = {}
    
    # Test each scraper
    results['huggingface'] = test_huggingface()
    results['github'] = test_github()
    results['producthunt'] = test_producthunt()
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    
    for scraper, passed in results.items():
        status = "PASS" if passed else "FAIL"
        logger.info(f"{scraper.upper()}: {status}")
    
    all_passed = all(results.values())
    logger.info(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

