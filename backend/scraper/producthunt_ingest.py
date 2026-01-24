"""
Product Hunt Ingestion Layer
Saves Product Hunt scraped data to database with proper logging
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.producthunt_scraper import producthunt_scraper
from database.connection import db
from database.models import AITool
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def ingest_producthunt():
    """
    Ingest Product Hunt AI products into the database
    
    This is the MANDATORY step that converts scraper output to database records
    
    Returns:
        dict: Ingestion statistics
    """
    logger.info("Starting Product Hunt ingestion")
    
    try:
        # STEP 1: Run the scraper
        products = producthunt_scraper.scrape_ai_products()
        
        # Log raw count BEFORE processing
        logger.info(f"PH Scraping returned {len(products)} products")
        
        # STEP 2: Track stats
        scraped = len(products)
        inserted = 0
        skipped = 0
        failed = 0
        
        # STEP 3: Ingest each product
        for product in products:
            try:
                # Prevent duplicates by URL
                existing = db.client.table("ai_tools") \
                    .select("id") \
                    .eq("url", product["url"]) \
                    .execute()
                
                if existing.data:
                    skipped += 1
                    logger.info(f"Skipped duplicate: {product['name']}")
                    continue
                
                # Create AITool model
                ai_tool = AITool(
                    name=product["name"],
                    description=product.get("description", "AI product from Product Hunt"),
                    url=product["url"],
                    source="producthunt",
                    category="AI",
                    pricing="unknown",
                    hype_score=50  # Default score for PH products
                )
                
                # Insert to database
                result = db.insert_tool(ai_tool)
                inserted += 1
                
                logger.info(f"✅ Inserted PH tool: {ai_tool.name} | ID: {result.get('id', 'unknown')}")
            
            except Exception as e:
                failed += 1
                logger.error(f"❌ Failed to insert {product.get('name', 'Unknown')}: {str(e)}")
                continue
        
        # STEP 4: Log final summary
        summary = f"""
🎉 Product Hunt ingest complete!
   📊 Scraped: {scraped}
   ✅ Inserted: {inserted}
   ⏭️ Skipped (duplicates): {skipped}
   ❌ Failed: {failed}
        """
        logger.info(summary)
        
        return {
            "scraped": scraped,
            "inserted": inserted,
            "skipped": skipped,
            "failed": failed,
            "status": "success" if inserted > 0 or scraped == 0 else "warning"
        }
    
    except Exception as e:
        logger.error(f"❌ Product Hunt ingest failed: {str(e)}")
        return {
            "scraped": 0,
            "inserted": 0,
            "skipped": 0,
            "failed": 0,
            "status": "error",
            "error": str(e)
        }


if __name__ == "__main__":
    # Test the ingestion
    result = ingest_producthunt()
    print(f"\n📋 Ingestion Result: {result}")

