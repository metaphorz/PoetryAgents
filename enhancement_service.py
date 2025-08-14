"""
Enhancement service for poetry post-processing.
Handles ASCII art generation and emoji enhancement.
"""

from typing import Optional
from base_llm_client import BaseLLMClient
from llm_client import LLMClient
from exceptions import APIError

class EnhancementService:
    """Service for enhancing poetry with ASCII art and emojis."""
    
    def __init__(self, client: Optional[BaseLLMClient] = None):
        """
        Initialize the enhancement service.
        
        Args:
            client: Optional LLM client to use. If None, creates default Claude client.
        """
        self.client = client or LLMClient()
    
    def generate_ascii_art(self, theme: str) -> str:
        """
        Generate ASCII art based on the theme.
        
        Args:
            theme: The theme to create ASCII art for
            
        Returns:
            ASCII art as a string
        """
        prompt = f"""Create simple ASCII art (text art) that represents the poetic theme: "{theme}". 

Guidelines:
- Use only basic ASCII characters: - | / \\ * + = ~ ^ v < > . : ; ' " ( ) [ ] {{ }} @ # $ % & 
- Keep it small but impactful (4-8 lines maximum)
- Make it visually appealing and thematically appropriate
- Consider the poetic and artistic nature of the theme
- Create something that would complement poetry about this theme

Examples of good ASCII art themes:
- Snow/winter: snowflakes, bare trees, mountains
- Ocean/water: waves, boats, fish
- Night/stars: moon, stars, constellation patterns  
- Love/romance: hearts, flowers, intertwined elements
- Archery: bows, arrows, targets
- Games: board patterns, pieces
- Nature: trees, animals, landscapes

Return ONLY the ASCII art with no explanatory text or comments."""
        
        try:
            ascii_art = self.client.generate_poetry(prompt, max_tokens=250)
            return ascii_art.strip()
        except Exception as e:
            # If ASCII art generation fails, proceed without it
            print(f"Warning: ASCII art generation failed ({str(e)}), proceeding without ASCII art")
            return ""
    
    def add_emojis_to_poetry(self, poetry: str, theme: str) -> str:
        """
        Add emojis to poetry by enhancing words with relevant emojis.
        
        Args:
            poetry: The original poetry text
            theme: The theme to help context for emoji selection
            
        Returns:
            Poetry enhanced with emojis placed after relevant words
        """
        prompt = f"""Add emojis to enhance this poetry about "{theme}". 

Instructions:
- Place emojis immediately AFTER words they represent (word🌟 not 🌟word)
- Only add emojis to nouns, nature words, emotions, and vivid imagery words
- Don't add emojis to articles, prepositions, or common words like "the", "and", "in"
- Use 2-4 emojis per line maximum to avoid overwhelming the poetry
- Choose emojis that enhance the poetic imagery and theme
- Preserve the exact line structure and spacing of the original
- Return ONLY the enhanced poetry with no explanatory text or comments

Original poetry:
{poetry}

Return the poetry with emojis added, maintaining the same line breaks and structure."""
        
        try:
            enhanced_poetry = self.client.generate_poetry(prompt, max_tokens=400)
            return enhanced_poetry.strip()
        except Exception as e:
            # Return original poetry if enhancement fails
            return poetry