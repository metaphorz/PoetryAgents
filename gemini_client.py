"""
Gemini Client for Google Generative AI integration
Handles communication with Gemini for poetry generation.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    print("Google Generative AI library not found. Install with: pip install google-generativeai")
    genai = None

class GeminiClient:
    """Client for interacting with Google's Gemini model."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        if not genai:
            raise ImportError("Google Generative AI library is required")
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
            
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Initialize the model - using the correct model name for v1
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_poetry(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate poetry using Gemini.
        
        Args:
            prompt: The prompt for poetry generation
            max_tokens: Maximum number of tokens to generate (approximate)
            
        Returns:
            Generated poetry text
        """
        try:
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.7,  # Some creativity but not too random
                top_p=0.8,
                top_k=40
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text.strip()
            
        except Exception as e:
            raise Exception(f"Error generating poetry with Gemini: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test the connection to the Gemini API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            test_response = self.generate_poetry("Write a simple two-word poem.", max_tokens=10)
            return len(test_response.strip()) > 0
        except Exception as e:
            print(f"Connection test error: {str(e)}")
            return False