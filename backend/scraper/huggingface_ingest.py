"""
Hugging Face Ingestion Layer
Saves Hugging Face scraped data to database with proper logging
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.huggingface_scraper import huggingface_scraper
from database.connection import db
from database.models import AITool
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def ingest_huggingface():
    """
    Ingest Hugging Face models and spaces into the database
    
    This is the MANDATORY step that converts scraper output to database records
    
    Returns:
        dict: Ingestion statistics for models and spaces
    """
    logger.info("Starting Hugging Face ingestion")
    
    try:
        # STEP 1: Run the scrapers
        models = huggingface_scraper.scrape_trending_models(limit=20)
        spaces = huggingface_scraper.scrape_trending_spaces(limit=10)
        
        # Log raw counts BEFORE processing
        logger.info(f"HF Scraping returned {len(models)} models and {len(spaces)} spaces")
        
        # STEP 2: Track stats
        stats = {
            "models": {"scraped": len(models), "inserted": 0, "skipped": 0, "failed": 0},
            "spaces": {"scraped": len(spaces), "inserted": 0, "skipped": 0, "failed": 0}
        }
        
        # STEP 3: Ingest models
        for model in models:
            try:
                # Prevent duplicates by URL
                existing = db.client.table("ai_tools") \
                    .select("id") \
                    .eq("url", model["url"]) \
                    .execute()
                
                if existing.data:
                    stats["models"]["skipped"] += 1
                    logger.debug(f"Skipped duplicate model: {model['name']}")
                    continue
                
                # Create AITool model
                ai_tool = AITool(
                    name=model["name"],
                    description=model.get("description", "AI model from Hugging Face"),
                    url=model["url"],
                    source="huggingface",
                    category=model.get("pipeline_tag", "AI"),
                    pricing="free",  # Most HF models are free
                    hype_score=min(100, 50 + model.get("likes", 0)),  # Base 50 + likes
                    tags=model.get("tags", [])
                )
                
                # Insert to database
                result = db.insert_tool(ai_tool)
                stats["models"]["inserted"] += 1
                
                logger.info(f"✅ Inserted HF model: {ai_tool.name} | Likes: {model.get('likes', 0)}")
            
            except Exception as e:
                stats["models"]["failed"] += 1
                logger.error(f"❌ Failed to insert model {model.get('name', 'Unknown')}: {str(e)}")
                continue
        
        # STEP 4: Ingest spaces
        for space in spaces:
            try:
                # Prevent duplicates by URL
                existing = db.client.table("ai_tools") \
                    .select("id") \
                    .eq("url", space["url"]) \
                    .execute()
                
                if existing.data:
                    stats["spaces"]["skipped"] += 1
                    logger.debug(f"⏭️ Skipped duplicate space: {space['name']}")
                    continue
                
                # Create AITool model
                ai_tool = AITool(
                    name=space["name"],
                    description=space.get("description", "AI space from Hugging Face"),
                    url=space["url"],
                    source="huggingface-space",
                    category="Demo App",
                    pricing="free",  # Most HF spaces are free
                    hype_score=min(100, 50 + space.get("likes", 0)),
                    tags=space.get("tags", [])
                )
                
                # Insert to database
                result = db.insert_tool(ai_tool)
                stats["spaces"]["inserted"] += 1
                
                logger.info(f"✅ Inserted HF space: {ai_tool.name} | SDK: {space.get('sdk', 'unknown')}")
            
            except Exception as e:
                stats["spaces"]["failed"] += 1
                logger.error(f"❌ Failed to insert space {space.get('name', 'Unknown')}: {str(e)}")
                continue
        
        # STEP 5: Log final summary
        total_inserted = stats["models"]["inserted"] + stats["spaces"]["inserted"]
        total_scraped = stats["models"]["scraped"] + stats["spaces"]["scraped"]
        
        summary = f"""
🎉 Hugging Face ingest complete!
   📊 Total Scraped: {total_scraped}
   ✅ Total Inserted: {total_inserted}
   ⏭️ Total Skipped (duplicates): {stats["models"]["skipped"] + stats["spaces"]["skipped"]}
   ❌ Total Failed: {stats["models"]["failed"] + stats["spaces"]["failed"]}
   
   Models: Inserted={stats["models"]["inserted"]}, Skipped={stats["models"]["skipped"]}
   Spaces: Inserted={stats["spaces"]["inserted"]}, Skipped={stats["spaces"]["skipped"]}
        """
        logger.info(summary)
        
        return {
            "status": "success" if total_inserted > 0 or total_scraped == 0 else "warning",
            "models": stats["models"],
            "spaces": stats["spaces"],
            "total_scraped": total_scraped,
            "total_inserted": total_inserted
        }
    
    except Exception as e:
        logger.error(f"❌ Hugging Face ingest failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "models": {"scraped": 0, "inserted": 0, "skipped": 0, "failed": 0},
            "spaces": {"scraped": 0, "inserted": 0, "skipped": 0, "failed": 0}
        }


if __name__ == "__main__":
    # Test the ingestion
    result = ingest_huggingface()
    print(f"\n📋 Ingestion Result: {result}")

