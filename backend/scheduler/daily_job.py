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
sys.path.append('..')

from scraper.github_scraper import github_scraper
from scraper.producthunt_scraper import producthunt_scraper
from scraper.huggingface_scraper import huggingface_scraper
from ai_engine.analyzer import ai_analyzer
from database.connection import db
from database.models import AITool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DailyJob:
    """
    Orchestrates the daily scraping and analysis process
    """
    
    def __init__(self):
        self.sources = {
            'github': github_scraper,
            'producthunt': producthunt_scraper,
            'huggingface': huggingface_scraper
        }
    
    async def run_daily_scan(self):
        """
        Main daily job - scrapes all sources and analyzes tools
        """
        logger.info("=" * 60)
        logger.info("🚀 STARTING DAILY AI TOOL SCAN")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        all_tools = []
        
        # Step 1: Scrape all sources
        logger.info("\n📡 PHASE 1: WEB SCRAPING")
        
        try:
            # GitHub
            logger.info("\n🔍 Scraping GitHub Trending...")
            github_tools = github_scraper.scrape_trending_ai_repos()
            all_tools.extend(github_tools)
            logger.info(f"Found {len(github_tools)} GitHub repos")
            
            # Product Hunt
            logger.info("\n🔍 Scraping Product Hunt...")
            ph_tools = producthunt_scraper.scrape_ai_products()
            all_tools.extend(ph_tools)
            logger.info(f"Found {len(ph_tools)} Product Hunt launches")
            
            # Hugging Face Models
            logger.info("\n🔍 Scraping Hugging Face Models...")
            hf_models = huggingface_scraper.scrape_trending_models(limit=15)
            all_tools.extend(hf_models)
            logger.info(f"Found {len(hf_models)} HF models")
            
            # Hugging Face Spaces
            logger.info("\n🔍 Scraping Hugging Face Spaces...")
            hf_spaces = huggingface_scraper.scrape_trending_spaces(limit=10)
            all_tools.extend(hf_spaces)
            logger.info(f"Found {len(hf_spaces)} HF spaces")
        
        except Exception as e:
            logger.error(f"❌ Error during scraping: {str(e)}")
        
        logger.info(f"\n✅ Total tools collected: {len(all_tools)}")
        
        # Step 2: AI Analysis
        logger.info("\n🤖 PHASE 2: AI ANALYSIS")
        
        analyzed_tools = []
        for i, tool_data in enumerate(all_tools, 1):
            try:
                logger.info(f"\nAnalyzing {i}/{len(all_tools)}: {tool_data.get('name', 'Unknown')}")
                
                # Run AI analysis
                analyzed = ai_analyzer.analyze_tool(tool_data)
                analyzed_tools.append(analyzed)
                
                logger.info(f"  ✅ Hype Score: {analyzed.get('hype_score', 0)}/100")
                logger.info(f"  📊 Category: {analyzed.get('category', 'Unknown')}")
                logger.info(f"  💰 Pricing: {analyzed.get('pricing', 'Unknown')}")
            
            except Exception as e:
                logger.error(f"  ❌ Analysis failed: {str(e)}")
                continue
        
        logger.info(f"\n✅ Analyzed {len(analyzed_tools)} tools")
        
        # Step 3: Save to Database
        logger.info("\n💾 PHASE 3: DATABASE STORAGE")
        
        saved_count = 0
        updated_count = 0
        
        for tool_data in analyzed_tools:
            try:
                # Check if tool already exists
                existing = await db.get_tool_by_name(tool_data.get('name', ''))
                
                if existing:
                    # Update existing tool
                    await db.update_tool(
                        existing['id'],
                        {
                            'hype_score': tool_data.get('hype_score'),
                            'description': tool_data.get('description'),
                            'updated_at': datetime.now().isoformat()
                        }
                    )
                    updated_count += 1
                    logger.info(f"  🔄 Updated: {tool_data.get('name')}")
                else:
                    # Create new tool
                    ai_tool = AITool(
                        name=tool_data.get('name', 'Unknown'),
                        description=tool_data.get('description', ''),
                        url=tool_data.get('url', 'https://example.com'),
                        source=tool_data.get('source', 'unknown'),
                        summary=tool_data.get('summary'),
                        use_cases=tool_data.get('use_cases', []),
                        category=tool_data.get('category'),
                        hype_score=tool_data.get('hype_score', 0),
                        github_stars=tool_data.get('stars', 0),
                        pricing=tool_data.get('pricing', 'unknown'),
                        tags=tool_data.get('tags', [])
                    )
                    
                    await db.insert_tool(ai_tool)
                    saved_count += 1
                    logger.info(f"  ✅ Saved: {tool_data.get('name')}")
            
            except Exception as e:
                logger.error(f"  ❌ Database error: {str(e)}")
                continue
        
        # Final summary
        logger.info("\n" + "=" * 60)
        logger.info("🎉 DAILY SCAN COMPLETE!")
        logger.info(f"📊 Summary:")
        logger.info(f"   • Tools scraped: {len(all_tools)}")
        logger.info(f"   • Tools analyzed: {len(analyzed_tools)}")
        logger.info(f"   • New tools saved: {saved_count}")
        logger.info(f"   • Existing tools updated: {updated_count}")
        logger.info(f"   • Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
    
    async def test_run(self):
        """
        Test run with limited scraping (for development)
        """
        logger.info("🧪 TEST RUN - Limited scraping")
        
        # Just scrape 2-3 items from each source
        all_tools = []
        
        # GitHub (top 3)
        github_tools = github_scraper.scrape_trending_ai_repos()[:3]
        all_tools.extend(github_tools)
        
        # Hugging Face models (top 3)
        hf_models = huggingface_scraper.scrape_trending_models(limit=3)
        all_tools.extend(hf_models)
        
        logger.info(f"Test scraped {len(all_tools)} tools")
        
        # Analyze first tool only
        if all_tools:
            test_tool = all_tools[0]
            analyzed = ai_analyzer.analyze_tool(test_tool)
            logger.info(f"Test analysis: {analyzed}")
        
        return all_tools

# Create job instance
daily_job = DailyJob()

# Main execution
if __name__ == "__main__":
    # Run the daily job
    asyncio.run(daily_job.run_daily_scan())