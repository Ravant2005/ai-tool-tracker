"""
Database Connection Handler
Connects to Supabase (our free database)
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import List, Optional
from .models import AITool
import logging

# Setup logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

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
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase credentials not found in .env file!")
        
        # Create connection to database
        self.client: Client = create_client(supabase_url, supabase_key)
        logger.info("✅ Database connection established")
    
    async def insert_tool(self, tool: AITool) -> dict:
        """
        Save a new AI tool to database
        
        Args:
            tool: AITool object with all the data
        
        Returns:
            The saved tool with its ID
        """
        try:
            # Convert tool to dictionary
            tool_data = tool.model_dump(exclude={'id'})
            
            # Log the data being inserted (for debugging)
            logger.info(f"DB INSERT: {tool.name} | {tool.url} | source={tool.source}")
            
            # Insert into 'ai_tools' table
            response = self.client.table('ai_tools').insert(tool_data).execute()
            
            # Check if insert actually succeeded
            if response.data:
                logger.info(f"✅ Tool '{tool.name}' saved to database (ID: {response.data[0].get('id')})")
                return response.data[0]
            else:
                logger.error(f"❌ DB insert returned no data for: {tool.name}")
                raise Exception("Insert returned empty response")
        
        except Exception as e:
            logger.error(f"❌ Error saving tool '{tool.name}': {str(e)}")
            raise
    
    async def get_all_tools(self, limit: int = 100) -> List[dict]:
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
            
            logger.info(f"✅ Retrieved {len(response.data)} tools")
            return response.data
        
        except Exception as e:
            logger.error(f"❌ Error fetching tools: {str(e)}")
            return []
    
    async def get_tool_by_name(self, name: str) -> Optional[dict]:
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
            logger.error(f"❌ Error searching tool: {str(e)}")
            return None
    
    async def update_tool(self, tool_id: int, updates: dict) -> dict:
        """
        Update an existing tool
        
        Args:
            tool_id: ID of the tool to update
            updates: Dictionary of fields to update
        
        Returns:
            Updated tool data
        """
        try:
            response = self.client.table('ai_tools')\
                .update(updates)\
                .eq('id', tool_id)\
                .execute()
            
            logger.info(f"✅ Tool {tool_id} updated")
            return response.data[0]
        
        except Exception as e:
            logger.error(f"❌ Error updating tool: {str(e)}")
            raise
    
    async def get_trending_today(self) -> List[dict]:
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
            logger.error(f"❌ Error fetching trending tools: {str(e)}")
            return []

# Create a global database instance
db = Database()