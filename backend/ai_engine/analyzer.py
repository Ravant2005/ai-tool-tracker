"""
AI Analysis Engine
Uses FREE Hugging Face API to analyze AI tools
"""

import os
import requests
import logging
from typing import Dict, List, Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAnalyzer:
    """
    Analyzes AI tools using Hugging Face's FREE inference API
    """
    
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.api_url = "https://api-inference.huggingface.co/models"
        
        # Using free models
        self.summarization_model = "facebook/bart-large-cnn"
        self.sentiment_model = "distilbert-base-uncased-finetuned-sst-2-english"
    
    def analyze_tool(self, tool_data: Dict) -> Dict:
        """
        Complete analysis of an AI tool
        
        Args:
            tool_data: Raw tool data from scrapers
        
        Returns:
            Enhanced tool data with AI analysis
        """
        logger.info(f"🤖 Analyzing: {tool_data.get('name', 'Unknown')}")
        
        # Get description
        description = tool_data.get('description', '')
        
        # Generate summary
        summary = self._generate_summary(description)
        
        # Extract use cases
        use_cases = self._extract_use_cases(description, tool_data)
        
        # Calculate hype score
        hype_score = self._calculate_hype_score(tool_data)
        
        # Determine pricing
        pricing = self._detect_pricing(description)
        
        # Categorize tool
        category = self._categorize_tool(description, tool_data)
        
        # Add analysis to tool data
        tool_data.update({
            'summary': summary,
            'use_cases': use_cases,
            'hype_score': hype_score,
            'pricing': pricing,
            'category': category
        })
        
        logger.info(f"✅ Analysis complete - Hype Score: {hype_score}/100")
        return tool_data
    
    def _generate_summary(self, text: str) -> str:
        """
        Generate AI summary using Hugging Face
        
        Args:
            text: Original description
        
        Returns:
            Summarized text
        """
        if not text or len(text) < 50:
            return text
        
        try:
            # If no API key, use simple truncation
            if not self.api_key:
                return text[:200] + "..." if len(text) > 200 else text
            
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            payload = {
                "inputs": text[:1000],  # Limit input size
                "parameters": {
                    "max_length": 150,
                    "min_length": 50,
                    "do_sample": False
                }
            }
            
            response = requests.post(
                f"{self.api_url}/{self.summarization_model}",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('summary_text', text[:200])
            
            # Fallback
            return text[:200] + "..."
        
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
            return text[:200] + "..." if len(text) > 200 else text
    
    def _extract_use_cases(self, description: str, tool_data: Dict) -> List[str]:
        """
        Extract potential use cases
        
        Args:
            description: Tool description
            tool_data: Raw tool data
        
        Returns:
            List of use cases
        """
        use_cases = []
        
        # Keyword-based extraction (simple but effective)
        keywords_to_cases = {
            'chat': 'Conversational AI',
            'image': 'Image Generation/Processing',
            'video': 'Video Editing/Generation',
            'code': 'Code Generation',
            'text': 'Text Generation',
            'translation': 'Language Translation',
            'speech': 'Speech Recognition/Synthesis',
            'search': 'Intelligent Search',
            'automation': 'Workflow Automation',
            'analysis': 'Data Analysis',
            'writing': 'Content Writing',
            'design': 'Design Assistance',
            'research': 'Research Assistant'
        }
        
        text = description.lower()
        
        for keyword, use_case in keywords_to_cases.items():
            if keyword in text:
                use_cases.append(use_case)
        
        # Add from tags if available
        tags = tool_data.get('tags', [])
        for tag in tags[:3]:  # Top 3 tags
            if tag not in use_cases:
                use_cases.append(tag.title())
        
        return use_cases[:5]  # Maximum 5 use cases
    
    def _calculate_hype_score(self, tool_data: Dict) -> int:
        """
        Calculate hype score (0-100) based on metrics
        
        Args:
            tool_data: Tool data with metrics
        
        Returns:
            Hype score (0-100)
        """
        score = 50  # Base score
        
        # GitHub stars contribution (max +30)
        stars = tool_data.get('stars', 0) or tool_data.get('github_stars', 0)
        if stars:
            score += min(30, stars / 1000)
        
        # Today's stars (trending indicator, max +20)
        today_stars = tool_data.get('today_stars', 0)
        if today_stars:
            score += min(20, today_stars / 100)
        
        # Hugging Face likes/downloads (max +20)
        likes = tool_data.get('likes', 0)
        downloads = tool_data.get('downloads', 0)
        if likes:
            score += min(10, likes / 100)
        if downloads:
            score += min(10, downloads / 10000)
        
        # Product Hunt upvotes (max +15)
        upvotes = tool_data.get('upvotes', 0)
        if upvotes:
            score += min(15, upvotes / 50)
        
        # Source credibility boost
        source = tool_data.get('source', '')
        if source == 'github':
            score += 5
        elif source == 'producthunt':
            score += 10
        
        # Ensure score is between 0-100
        return min(100, max(0, int(score)))
    
    def _detect_pricing(self, description: str) -> str:
        """
        Detect pricing model from description
        
        Args:
            description: Tool description
        
        Returns:
            Pricing type: 'free', 'freemium', or 'paid'
        """
        text = description.lower()
        
        if any(word in text for word in ['free', 'open source', 'open-source', 'no cost']):
            if any(word in text for word in ['premium', 'pro', 'paid', 'subscription']):
                return 'freemium'
            return 'free'
        
        if any(word in text for word in ['paid', 'subscription', 'pricing', '$']):
            return 'paid'
        
        return 'unknown'
    
    def _categorize_tool(self, description: str, tool_data: Dict) -> str:
        """
        Categorize the AI tool
        
        Args:
            description: Tool description
            tool_data: Tool data
        
        Returns:
            Category name
        """
        text = description.lower()
        
        # Category keywords
        categories = {
            'NLP': ['nlp', 'text', 'language', 'chat', 'gpt', 'translation'],
            'Computer Vision': ['vision', 'image', 'video', 'object detection', 'ocr'],
            'Audio': ['speech', 'audio', 'voice', 'music', 'sound'],
            'Code': ['code', 'programming', 'developer', 'github copilot'],
            'Generative AI': ['generate', 'creation', 'diffusion', 'stable diffusion'],
            'Data Science': ['data', 'analysis', 'ml', 'machine learning'],
            'Automation': ['automation', 'workflow', 'agent', 'autonomous']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        # Check pipeline_tag from Hugging Face
        pipeline_tag = tool_data.get('pipeline_tag', '')
        if pipeline_tag:
            return pipeline_tag.replace('-', ' ').title()
        
        return 'General AI'

# Create analyzer instance
ai_analyzer = AIAnalyzer()