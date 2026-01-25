"""
FastAPI Main Server
The backend API that frontend talks to
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import logging
from datetime import datetime

# Import our modules
from database.connection import db
from database.models import AITool, ToolStats
from scheduler.daily_job import daily_job
from scraper.producthunt_ingest import ingest_producthunt
from scraper.huggingface_ingest import ingest_huggingface
from scraper.github_ingest import ingest_github

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Tool Tracker API",
    description="Discover trending AI tools daily",
    version="1.0.0"
)

# Enable CORS (allows frontend to talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== API ENDPOINTS ==============

@app.get("/")
async def root():
    """
    Home endpoint - API health check
    """
    return {
        "message": "AI Tool Tracker API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/tools", response_model=List[dict])
async def get_all_tools():
    """
    Get ALL AI tools from database without any filters
    Returns all tools sorted by created_at descending
    """
    try:
        # Direct query to return ALL tools without filters
        response = db.client.table('ai_tools').select("*").order('created_at', desc=True).execute()
        tools = response.data
        
        logger.info(f"TOOLS COUNT: {len(tools)}")
        logger.info(f"Sources found: {set(t.get('source') for t in tools)}")
        
        return tools
    
    except Exception as e:
        logger.error(f"Error fetching tools: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch tools")

@app.get("/api/tools/trending", response_model=List[dict])
async def get_trending_tools():
    """
    Get today's trending AI tools
    
    Returns:
        List of tools discovered today, sorted by hype score
    """
    try:
        logger.info("Fetching trending tools")
        tools = await db.get_trending_today()
        logger.info(f"Found {len(tools)} trending tools")
        return tools
    
    except Exception as e:
        logger.error(f"Error fetching trending tools: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch trending tools")

@app.get("/api/tools/{tool_id}")
async def get_tool_by_id(tool_id: int):
    """
    Get a specific tool by ID
    
    Args:
        tool_id: Tool ID
    
    Returns:
        Tool details
    """
    try:
        # Direct query by ID
        response = db.client.table('ai_tools').select("*").eq('id', tool_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Tool not found")
        
        return response.data[0]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching tool: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch tool")

@app.get("/api/stats", response_model=dict)
async def get_stats():
    """
    Get overall statistics
    
    Returns:
        Dashboard statistics
    """
    try:
        # Direct query for all tools
        response = db.client.table('ai_tools').select("*").execute()
        tools = response.data
        
        trending = await db.get_trending_today()
        
        # Calculate stats
        total_tools = len(tools)
        new_today = len(trending)
        
        # Average hype score
        hype_scores = [t.get('hype_score', 0) for t in tools if t.get('hype_score')]
        avg_hype = sum(hype_scores) / len(hype_scores) if hype_scores else 0
        
        # Top category
        categories = [t.get('category') for t in tools if t.get('category')]
        top_category = max(set(categories), key=categories.count) if categories else "N/A"
        
        return {
            "total_tools": total_tools,
            "new_today": new_today,
            "avg_hype_score": round(avg_hype, 1),
            "top_category": top_category
        }
    
    except Exception as e:
        logger.error(f"Error calculating stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")

@app.get("/api/categories")
async def get_categories():
    """
    Get list of all categories
    
    Returns:
        List of unique categories with counts
    """
    try:
        # Direct query for all tools
        response = db.client.table('ai_tools').select("*").execute()
        tools = response.data
        
        # Count categories
        category_counts = {}
        for tool in tools:
            cat = tool.get('category', 'Uncategorized')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Sort by count
        categories = [
            {"name": cat, "count": count}
            for cat, count in sorted(
                category_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]
        
        return categories
    
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch categories")

@app.post("/api/scan/manual")
async def trigger_manual_scan():
    """
    Manually trigger the daily scan with detailed results
    (For testing - in production would be scheduled)
    
    Returns:
        Scan results with ingestion stats for each source
    """
    try:
        logger.info("Manual scan triggered")
        
        # Run ingestion for each source
        hf_result = ingest_huggingface()
        gh_result = ingest_github()
        # Product Hunt - DISABLED (blocks bots, requires login)
        # ph_result = ingest_producthunt()
        
        return {
            "status": "success",
            "message": "Manual scan completed",
            "timestamp": datetime.now().isoformat(),
            "results": {
                "huggingface": hf_result,
                "github": gh_result
                # "producthunt": ph_result  # Disabled
            },
            "summary": {
                "total_scraped": hf_result.get("total_scraped", 0) + gh_result.get("total_scraped", 0),
                "total_inserted": hf_result.get("total_inserted", 0) + gh_result.get("total_inserted", 0)
            }
        }
    
    except Exception as e:
        logger.error(f"Manual scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@app.post("/api/scan/test")
async def trigger_test_scan():
    """
    Run a limited test scan (3-5 tools only)
    
    Returns:
        Test scan results
    """
    try:
        logger.info("Test scan triggered")
        tools = await daily_job.test_run()
        return {
            "status": "success",
            "message": "Test scan completed",
            "tools_found": len(tools),
            "sample_tools": tools[:3]
        }
    
    except Exception as e:
        logger.error(f"Test scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test scan failed: {str(e)}")

@app.get("/api/scan/logs")
async def get_scan_logs(limit: int = 10):
    """
    Get recent scan logs
    
    Query Parameters:
    - limit: Number of logs to return (default: 10)
    
    Returns:
        List of recent scan results
    """
    try:
        # For now, return a simulated log
        # In production, this would query a logs table
        return {
            "logs": [
                {
                    "id": 1,
                    "timestamp": datetime.now().isoformat(),
                    "type": "manual",
                    "status": "success",
                    "huggingface": {"inserted": 5, "scraped": 10},
                    "producthunt": {"inserted": 2, "scraped": 3}
                }
            ][:limit],
            "note": "Full scan history requires a logs table in database"
        }
    
    except Exception as e:
        logger.error(f"Error fetching scan logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch scan logs")

# ============== STARTUP/SHUTDOWN EVENTS ==============

@app.on_event("startup")
async def startup_event():
    """
    Runs when server starts
    """
    logger.info("AI Tool Tracker API Starting...")
    logger.info("=" * 60)
    logger.info("Server is ready!")
    logger.info("Visit: http://localhost:8000")
    logger.info("API Docs: http://localhost:8000/docs")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when server stops
    """
    logger.info("AI Tool Tracker API Shutting down...")

# ============== RUN SERVER ==============

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )
