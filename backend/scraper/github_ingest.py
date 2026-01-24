"""
GitHub Trending Ingestion Layer
Saves GitHub scraped data to database with proper logging
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.github_scraper import github_scraper
from database.connection import db
from database.models import AITool
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def ingest_github():
    """
    Ingest GitHub trending AI repositories into the database
    
    This is the MANDATORY step that converts scraper output to database records
    
    Returns:
        dict: Ingestion statistics for repos
    """
    logger.info("🚀 Starting GitHub ingestion")
    
    try:
        # STEP 1: Run the scraper (Python repos with AI filter)
        repos = github_scraper.scrape_trending_ai_repos(language="python")
        
        logger.info(f"🧪 GitHub Scraping returned {len(repos)} repos")
        
        # STEP 2: Track stats
        stats = {
            "scraped": len(repos),
            "inserted": 0,
            "skipped": 0,
            "failed": 0
        }
        
        # STEP 3: Ingest each repo
        for repo in repos:
            try:
                # Prevent duplicates by URL
                existing = db.client.table("ai_tools") \
                    .select("id") \
                    .eq("url", repo["url"]) \
                    .execute()
                
                if existing.data:
                    stats["skipped"] += 1
                    logger.debug(f"⏭️ Skipped duplicate repo: {repo['name']}")
                    continue
                
                # Create AITool model
                ai_tool = AITool(
                    name=repo["name"],
                    description=repo.get("description", "AI repository from GitHub"),
                    url=repo["url"],
                    source="github",
                    category="AI",
                    pricing="free",  # Open source repos are free
                    hype_score=min(100, 50 + min(repo.get("today_stars", 0), 50)),  # Base 50 + today's stars
                    github_stars=repo.get("stars", 0),
                    tags=[repo.get("language", "python"), "ai", "github"]
                )
                
                # Insert to database
                result = db.insert_tool(ai_tool)
                stats["inserted"] += 1
                
                logger.info(f"✅ Inserted GitHub repo: {ai_tool.name} | Stars: {repo.get('stars', 0)} | Today: {repo.get('today_stars', 0)}")
            
            except Exception as e:
                stats["failed"] += 1
                logger.error(f"❌ Failed to insert repo {repo.get('name', 'Unknown')}: {str(e)}")
                continue
        
        # STEP 4: Log final summary
        summary = f"""
🎉 GitHub ingest complete!
   📊 Total Scraped: {stats['scraped']}
   ✅ Total Inserted: {stats['inserted']}
   ⏭️ Total Skipped (duplicates): {stats['skipped']}
   ❌ Total Failed: {stats['failed']}
        """
        logger.info(summary)
        
        return {
            "status": "success" if stats["inserted"] > 0 or stats["scraped"] == 0 else "warning",
            "repos": stats,
            "total_scraped": stats["scraped"],
            "total_inserted": stats["inserted"]
        }
    
    except Exception as e:
        logger.error(f"❌ GitHub ingest failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "repos": {"scraped": 0, "inserted": 0, "skipped": 0, "failed": 0},
            "total_scraped": 0,
            "total_inserted": 0
        }


if __name__ == "__main__":
    # Test the ingestion
    result = ingest_github()
    print(f"\n📋 Ingestion Result: {result}")

