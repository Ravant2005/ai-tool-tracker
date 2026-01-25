"""
Daily Automation Job
Runs scraping and analysis automatically
"""

import logging
import asyncio
from datetime import datetime
from typing import List, Dict

# Import our modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.github_scraper import github_scraper
from scraper.producthunt_ingest import ingest_producthunt
from scraper.huggingface_ingest import ingest_huggingface
from scraper.github_ingest import ingest_github
from database.connection import db
from database.models import AITool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DailyJob:
    """
    Orchestrates the daily scraping and analysis process
    """
    
    def __init__(self):
        # Use ingestion layers instead of direct scrapers
        self.ingestion_sources = {
            'producthunt': ingest_producthunt,
            'huggingface': ingest_huggingface,
            'github': ingest_github
        }
    
    async def run_daily_scan(self):
        """
        Main daily job - runs ingestion and analyzes tools
        """
        logger.info("=" * 60)
        logger.info("STARTING DAILY AI TOOL SCAN")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        all_ingestion_results = {}
        
        # Step 1: Run ingestion for each source
        logger.info("\nPHASE 1: INGESTION (Scraping + DB Storage)")
        
        try:
            # Product Hunt - DISABLED (blocks bots, requires login)
            # logger.info("\nRunning Product Hunt ingestion...")
            # ph_result = ingest_producthunt()
            # all_ingestion_results['producthunt'] = ph_result
            # logger.info(f"   PH Result: inserted={ph_result.get('inserted', 0)}, scraped={ph_result.get('scraped', 0)}")
            
            # Hugging Face
            logger.info("\nRunning Hugging Face ingestion...")
            hf_result = ingest_huggingface()
            all_ingestion_results['huggingface'] = hf_result
            logger.info(f"   HF Result: inserted={hf_result.get('total_inserted', 0)}, scraped={hf_result.get('total_scraped', 0)}")
            
            # GitHub
            logger.info("\nRunning GitHub ingestion...")
            gh_result = ingest_github()
            all_ingestion_results['github'] = gh_result
            logger.info(f"   GH Result: inserted={gh_result.get('total_inserted', 0)}, scraped={gh_result.get('total_scraped', 0)}")
            
        except Exception as e:
            logger.error(f"Error during ingestion: {str(e)}")
        
        # Step 2: Get newly inserted tools from database
        logger.info("\nPHASE 2: SUMMARY")
        
        try:
            # Get tools discovered today
            new_tools = db.get_trending_today()
            logger.info(f"Found {len(new_tools)} tools discovered today")
            
        except Exception as e:
            logger.error(f"Error during summary: {str(e)}")
        
        # Step 3: Final summary
        total_inserted = sum(
            r.get('inserted', 0) if isinstance(r, dict) else r.get('total_inserted', 0) 
            for r in all_ingestion_results.values()
        )
        total_scraped = sum(
            r.get('scraped', 0) if isinstance(r, dict) else r.get('total_scraped', 0) 
            for r in all_ingestion_results.values()
        )
        
        logger.info("\n" + "=" * 60)
        logger.info("DAILY SCAN COMPLETE!")
        logger.info(f"Summary:")
        logger.info(f"   Sources processed: {len(all_ingestion_results)}")
        logger.info(f"   Total tools scraped: {total_scraped}")
        logger.info(f"   New tools inserted: {total_inserted}")
        logger.info(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
    
    def test_run(self):
        """
        Test run with limited scraping (for development)
        """
        logger.info("TEST RUN - Limited ingestion")
        
        try:
            # Hugging Face ingestion  
            hf_result = ingest_huggingface()
            
            # GitHub ingestion
            gh_result = ingest_github()
            
            logger.info(f"Test results: HF={hf_result}, GH={gh_result}")
            
            return {
                "huggingface": hf_result,
                "github": gh_result
            }
        except Exception as e:
            logger.error(f"Test run failed: {str(e)}")
            return {"error": str(e)}

# Create job instance
daily_job = DailyJob()

# Main execution
if __name__ == "__main__":
    # Run the daily job
    asyncio.run(daily_job.run_daily_scan())

