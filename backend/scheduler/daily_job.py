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
        logger.info("=" * 70)
        logger.info("🚀 STARTING DAILY AI TOOL SCAN")
        logger.info(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)
        
        all_tools = []
        
        # Step 1: Scrape all sources
        logger.info("\n" + "=" * 70)
        logger.info("📡 PHASE 1: WEB SCRAPING")
        logger.info("=" * 70)
        
        try:
            # GitHub
            logger.info("\n[1/4] 🔍 Scraping GitHub Trending...")
            github_tools = github_scraper.scrape_trending_ai_repos()
            all_tools.extend(github_tools)
            logger.info(f"✅ GitHub: {len(github_tools)} repos found")
            
            # Product Hunt
            logger.info("\n[2/4] 🔍 Scraping Product Hunt...")
            ph_tools = producthunt_scraper.scrape_ai_products()
            all_tools.extend(ph_tools)
            logger.info(f"✅ Product Hunt: {len(ph_tools)} products found")
            
            # Hugging Face Models
            logger.info("\n[3/4] 🔍 Scraping Hugging Face Models...")
            hf_models = huggingface_scraper.scrape_trending_models(limit=15)
            all_tools.extend(hf_models)
            logger.info(f"✅ HF Models: {len(hf_models)} models found")
            
            # Hugging Face Spaces
            logger.info("\n[4/4] 🔍 Scraping Hugging Face Spaces...")
            hf_spaces = huggingface_scraper.scrape_trending_spaces(limit=10)
            all_tools.extend(hf_spaces)
            logger.info(f"✅ HF Spaces: {len(hf_spaces)} spaces found")
        
        except Exception as e:
            logger.error(f"❌ Error during scraping phase: {type(e).__name__}: {str(e)}", exc_info=True)
        
        logger.info(f"\n📊 SCRAPING SUMMARY:")
        logger.info(f"   Total tools collected: {len(all_tools)}")
        
        if len(all_tools) == 0:
            logger.warning("⚠️  WARNING: No tools were scraped! Check scraper logs above.")
            return
        
        # Step 2: AI Analysis
        logger.info("\n" + "=" * 70)
        logger.info("🤖 PHASE 2: AI ANALYSIS & ENRICHMENT")
        logger.info("=" * 70)
        
        analyzed_tools = []
        failed_analysis = 0
        
        for i, tool_data in enumerate(all_tools, 1):
            try:
                tool_name = tool_data.get('name', f'Tool#{i}')
                logger.info(f"\n[{i}/{len(all_tools)}] 🤖 Analyzing: {tool_name}")
                
                # Run AI analysis
                analyzed = ai_analyzer.analyze_tool(tool_data)
                analyzed_tools.append(analyzed)
                
                logger.info(f"   ✅ Hype Score: {analyzed.get('hype_score', 0)}/100")
                logger.info(f"   📂 Category: {analyzed.get('category', 'Unknown')}")
                logger.info(f"   💰 Pricing: {analyzed.get('pricing', 'unknown')}")
                logger.info(f"   🏷️  Use Cases: {', '.join(analyzed.get('use_cases', [])[:2])}")
            
            except Exception as e:
                logger.error(f"   ❌ Analysis failed: {type(e).__name__}: {str(e)}")
                failed_analysis += 1
                continue
        
        logger.info(f"\n📊 ANALYSIS SUMMARY:")
        logger.info(f"   Successfully analyzed: {len(analyzed_tools)}/{len(all_tools)}")
        logger.info(f"   Failed: {failed_analysis}")
        
        if len(analyzed_tools) == 0:
            logger.error("❌ No tools were successfully analyzed. Aborting database insert.")
            return
        
        # Step 3: Save to Database
        logger.info("\n" + "=" * 70)
        logger.info("💾 PHASE 3: DATABASE STORAGE")
        logger.info("=" * 70)
        
        saved_count = 0
        updated_count = 0
        duplicate_count = 0
        insert_failed = 0
        
        for tool_data in analyzed_tools:
            tool_name = tool_data.get('name', 'Unknown')
            
            try:
                # Check if tool already exists (duplicate detection)
                existing = await db.get_tool_by_name(tool_name)
                
                if existing:
                    # Update existing tool
                    try:
                        await db.update_tool(
                            existing['id'],
                            {
                                'hype_score': tool_data.get('hype_score'),
                                'description': tool_data.get('description'),
                                'updated_at': datetime.now().isoformat()
                            }
                        )
                        updated_count += 1
                        logger.info(f"🔄 Updated (ID:{existing['id']}): {tool_name}")
                    except Exception as e:
                        logger.error(f"❌ Update failed: {tool_name}: {str(e)}")
                        insert_failed += 1
                else:
                    # Create new tool (with validation)
                    try:
                        url = tool_data.get('url', '')
                        # Basic URL validation
                        if not url or (not url.startswith('http://') and not url.startswith('https://')):
                            logger.warning(f"   ⚠️  Invalid URL for {tool_name}: '{url}'")
                            url = f"https://example.com/ai/{tool_name.lower().replace(' ', '-')}"
                            logger.info(f"   → Using placeholder: {url}")
                        
                        ai_tool = AITool(
                            name=tool_name,
                            description=tool_data.get('description', ''),
                            url=url,
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
                        logger.info(f"✅ Saved (NEW): {tool_name}")
                    except Exception as e:
                        logger.error(f"❌ Insert failed: {tool_name}: {type(e).__name__}: {str(e)}")
                        insert_failed += 1
                        continue
            
            except Exception as e:
                logger.error(f"❌ Database lookup error for {tool_name}: {str(e)}")
                duplicate_count += 1
                continue
        
        # Final summary
        logger.info("\n" + "=" * 70)
        logger.info("🎉 DAILY SCAN COMPLETE!")
        logger.info("=" * 70)
        logger.info(f"\n📊 FINAL SUMMARY:")
        logger.info(f"   Phase 1 (Scraping):")
        logger.info(f"      • Total tools collected: {len(all_tools)}")
        logger.info(f"   Phase 2 (Analysis):")
        logger.info(f"      • Successfully analyzed: {len(analyzed_tools)}")
        logger.info(f"      • Failed: {failed_analysis}")
        logger.info(f"   Phase 3 (Database):")
        logger.info(f"      • ✅ New tools saved: {saved_count}")
        logger.info(f"      • 🔄 Existing tools updated: {updated_count}")
        logger.info(f"      • ⏭️  Duplicates skipped: {duplicate_count}")
        logger.info(f"      • ❌ Insert/Update failed: {insert_failed}")
        logger.info(f"\n📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70 + "\n")
    
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