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
async def get_all_tools(
    limit: int = 100,
    category: Optional[str] = None,
    pricing: Optional[str] = None
):
    """
    Get all AI tools
    
    Query Parameters:
    - limit: Maximum number of tools (default: 100)
    - category: Filter by category (e.g., "NLP", "Computer Vision")
    - pricing: Filter by pricing ("free", "freemium", "paid")
    
    Returns:
        List of AI tools sorted by hype score
    """
    try:
        logger.info(f"Fetching tools (limit: {limit}, category: {category}, pricing: {pricing})")
        
        # Get all tools from database
        tools = await db.get_all_tools(limit=limit)
        
        # Apply filters
        if category:
            tools = [t for t in tools if t.get('category') == category]
        
        if pricing:
            tools = [t for t in tools if t.get('pricing') == pricing]
        
        logger.info(f"Returning {len(tools)} tools")
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
        # For now, get all tools and find by ID
        # (In production, would query database directly)
        tools = await db.get_all_tools(limit=1000)
        tool = next((t for t in tools if t.get('id') == tool_id), None)
        
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        
        return tool
    
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
        tools = await db.get_all_tools(limit=1000)
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
        tools = await db.get_all_tools(limit=1000)
        
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
    Manually trigger the daily scan
    (For testing - in production would be scheduled)
    
    Returns:
        Scan results
    """
    try:
        logger.info("Manual scan triggered")
        await daily_job.run_daily_scan()
        return {
            "status": "success",
            "message": "Manual scan completed",
            "timestamp": datetime.now().isoformat()
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

# ============== STARTUP/SHUTDOWN EVENTS ==============

@app.on_event("startup")
async def startup_event():
    """
    Runs when server starts
    """
    logger.info("🚀 AI Tool Tracker API Starting...")
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
    logger.info("👋 AI Tool Tracker API Shutting down...")

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