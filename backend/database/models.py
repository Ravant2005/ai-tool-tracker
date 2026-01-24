"""
Database Models for AI Tool Tracker
Defines the structure of our data
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field

class AITool(BaseModel):
    """
    Represents a single AI tool in our database
    
    Think of this like a form with fields:
    - Tool name
    - Description
    - Website link
    - etc.
    """
    
    # Basic Information
    id: Optional[int] = None
    name: str  # e.g., "ChatGPT"
    description: str  # What the tool does
    url: str = Field(..., description="Website link (auto-converted to HttpUrl)")  # Website link
    
    # Discovery Information
    source: str  # Where we found it: "github", "producthunt", etc.
    discovered_date: datetime = Field(default_factory=datetime.now)

    
    # AI Analysis Results
    summary: Optional[str] = None  # AI-generated summary
    use_cases: Optional[List[str]] = None  # List of use cases
    category: Optional[str] = None  # e.g., "NLP", "Computer Vision"
    
    # Metrics
    hype_score: Optional[int] = None  # 0-100, how trending it is
    github_stars: Optional[int] = None
    pricing: Optional[str] = None  # "free", "freemium", "paid"
    
    # Metadata
    tags: Optional[List[str]] = None
    logo_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ToolStats(BaseModel):
    """
    Statistics about our tool collection
    For dashboard summary cards
    """
    total_tools: int
    new_today: int
    avg_hype_score: float
    top_category: str