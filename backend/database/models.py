"""
Database Models for AI Tool Tracker
Defines the structure of our data
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

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
    url: str = Field(default="")  # Website link (string, not HttpUrl)
    
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
    logo_url: Optional[str] = None  # Logo URL (string, not HttpUrl)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator("url", "logo_url", mode="before")
    @classmethod
    def validate_url_to_string(cls, v):
        """
        Convert any URL-type objects to strings for JSON serialization.
        
        This handles:
        - Pydantic HttpUrl/Url objects
        - httpx.URL objects
        - Any other URL-like objects
        """
        # If it's None or already a string, return as-is
        if v is None or isinstance(v, str):
            return v
        
        # If it has a __str__ method and looks like a URL object, convert to string
        if hasattr(v, '__str__'):
            try:
                str_value = str(v)
                # Verify it looks like a URL (basic check)
                if '://' in str_value:
                    return str_value
            except:
                pass
        
        # For any other type, return as-is (let the _normalize_dict handle it later)
        return v


class ToolStats(BaseModel):
    """
    Statistics about our tool collection
    For dashboard summary cards
    """
    total_tools: int
    new_today: int
    avg_hype_score: float
    top_category: str