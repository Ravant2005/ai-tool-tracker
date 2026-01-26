"""
Database Connection Handler
Connects to Supabase (our free database)
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import List, Optional, Any, Dict, Union
from .models import AITool
from datetime import datetime, date
import logging

# Setup logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _normalize_dict(data: Dict) -> Dict:
    """
    Recursively convert all non-JSON-serializable types to serializable equivalents.
    
    This fixes the "Object of type Url is not JSON serializable" error by converting:
    - Pydantic Url/HttpUrl objects to strings
    - httpx.URL objects to strings
    - datetime objects to ISO format strings
    - date objects to ISO format strings
    - Any other non-serializable objects to strings
    
    Args:
        data: Dictionary to normalize
        
    Returns:
        Clean dictionary with only JSON-serializable values
    """
    if not isinstance(data, dict):
        return data
    
    normalized = {}
    for key, value in data.items():
        normalized[key] = _normalize_value(value)
    
    return normalized


def _normalize_value(value: Any) -> Any:
    """
    Convert a single value to its JSON-serializable equivalent.
    
    Args:
        value: Any value that might not be JSON serializable
        
    Returns:
        JSON-serializable version of the value
    """
    # Handle None
    if value is None:
        return None
    
    # Handle strings, ints, floats, bools (already JSON serializable)
    if isinstance(value, (str, int, float, bool)):
        return value
    
    # Handle datetime objects
    if isinstance(value, datetime):
        return value.isoformat()
    
    # Handle date objects
    if isinstance(value, date):
        return value.isoformat()
    
    # Handle lists
    if isinstance(value, list):
        return [_normalize_value(item) for item in value]
    
    # Handle dicts
    if isinstance(value, dict):
        return _normalize_dict(value)
    
    # Handle Pydantic Url/HttpUrl objects
    # Check for pydantic URL types by looking for common attributes/methods
    if hasattr(value, '__str__') and hasattr(value, 'host'):
        # Likely a URL object - convert to string
        try:
            str_value = str(value)
            # Verify it looks like a URL
            if str_value.startswith('http://') or str_value.startswith('https://'):
                return str_value
        except:
            pass
    
    # Handle any other object by converting to string
    try:
        return str(value)
    except:
        return None

class Database:
    """
    This class handles all database operations
    Think of it as your database assistant
    """
    
    def __init__(self):
        """
        Initialize connection to Supabase
        Gets URL and KEY from .env file
        """
        load_dotenv()  # Load environment variables from .env file
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and/or SUPABASE_SERVICE_ROLE_KEY not found in environment!")
        
        # Create connection to database
        self.client: Client = create_client(supabase_url, supabase_key)
        logger.info("Database connection established")
    
    def insert_tool(self, tool: AITool) -> dict:
        """
        Save a new AI tool to database
        
        Args:
            tool: AITool object with all the data
        
        Returns:
            The saved tool with its ID, or None if insert failed
        """
        try:
            # Convert Pydantic model to a dict, which handles most serialization
            tool_data = tool.model_dump(exclude={'id'})
            
            # Use our robust normalizer for any tricky types
            normalized_data = _normalize_dict(tool_data)
            
            # Log the data being inserted (for debugging)
            logger.info(f"DB INSERT: {tool.name} | {normalized_data.get('url', 'N/A')} | source={tool.source}")
            
            # Insert into 'ai_tools' table
            response = self.client.table('ai_tools').insert(normalized_data).execute()
            
            # Check if insert actually succeeded
            if response.data:
                logger.info(f"Tool saved: {tool.name} (ID: {response.data[0].get('id')})")
                return response.data[0]
            else:
                logger.error(f"DB insert returned no data for: {tool.name}")
                return None
        
        except Exception as e:
            logger.error(f"Error saving tool '{tool.name}': {str(e)}")
            return None
    
    def get_all_tools(self, limit: int = 100) -> List[dict]:
        """
        Get all AI tools from database
        
        Args:
            limit: Maximum number of tools to return
        
        Returns:
            List of all tools
        """
        try:
            response = self.client.table('ai_tools')\
                .select("*")\
                .order('hype_score', desc=True)\
                .limit(limit)\
                .execute()
            
            logger.info(f"Retrieved {len(response.data)} tools")
            return response.data
        
        except Exception as e:
            logger.error(f"Error fetching tools: {str(e)}")
            return []
    
    def get_tool_by_name(self, name: str) -> Optional[dict]:
        """
        Search for a specific tool by name
        
        Args:
            name: Tool name to search for
        
        Returns:
            Tool data if found, None otherwise
        """
        try:
            response = self.client.table('ai_tools')\
                .select("*")\
                .eq('name', name)\
                .execute()
            
            if response.data:
                return response.data[0]
            return None
        
        except Exception as e:
            logger.error(f"Error searching tool: {str(e)}")
            return None
    
    def update_tool(self, tool_id: int, updates: dict) -> dict:
        """
        Update an existing tool
        
        Args:
            tool_id: ID of the tool to update
            updates: Dictionary of fields to update
        
        Returns:
            Updated tool data
        """
        try:
            # Normalize updates to be JSON serializable
            updates = _normalize_dict(updates)
            
            response = self.client.table('ai_tools')\
                .update(updates)\
                .eq('id', tool_id)\
                .execute()
            
            logger.info(f"Tool {tool_id} updated")
            return response.data[0]
        
        except Exception as e:
            logger.error(f"Error updating tool: {str(e)}")
            raise
    
    def get_trending_today(self) -> List[dict]:
        """
        Get tools discovered today, sorted by hype score
        
        Returns:
            List of today's trending tools
        """
        try:
            from datetime import datetime, timedelta
            today = datetime.now().date()
            
            response = self.client.table('ai_tools')\
                .select("*")\
                .gte('discovered_date', today.isoformat())\
                .order('hype_score', desc=True)\
                .execute()
            
            return response.data
        
        except Exception as e:
            logger.error(f"Error fetching trending tools: {str(e)}")
            return []

# Create a global database instance
db = Database()