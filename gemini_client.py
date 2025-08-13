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
    """Client for interacting with Google's Gemini models."""
    
    @classmethod
    def get_available_models(cls, limit_recent=6):
        """Dynamically fetch available Gemini models from the API.
        
        Args:
            limit_recent: If specified, return only the N most relevant/recent models
        """
        try:
            # Initialize temporary client to fetch models
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable is required")
            
            genai.configure(api_key=api_key)
            models = genai.list_models()
            
            # Build models list with display names, filter for text generation models
            model_list = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    # Clean up model name (remove 'models/' prefix)
                    model_id = model.name.replace('models/', '')
                    model_list.append((model.display_name, model_id))
            
            # Smart sorting for Gemini (since no timestamps)
            # Priority: 2.5 > 2.0 > 1.5 > 1.0, then Pro > Flash > others
            def model_priority(item):
                display_name = item[0].lower()
                score = 0
                
                # Version priority (higher is better)
                if '2.5' in display_name: score += 1000
                elif '2.0' in display_name: score += 800
                elif '1.5' in display_name: score += 600
                elif '1.0' in display_name: score += 400
                
                # Type priority
                if 'pro' in display_name: score += 100
                elif 'flash' in display_name: score += 80
                
                # Prefer non-experimental/preview
                if 'preview' not in display_name and 'experimental' not in display_name:
                    score += 50
                
                return score
            
            # Sort by priority (highest first)
            model_list.sort(key=model_priority, reverse=True)
            
            # Limit to most relevant if specified
            if limit_recent:
                model_list = model_list[:limit_recent]
            
            # Convert back to dict
            available_models = {}
            for display_name, model_id in model_list:
                available_models[display_name] = model_id
            
            return available_models
        except Exception as e:
            # Fallback to known models if API fails
            return {
                "Gemini 2.5 Pro": "gemini-2.5-pro",
                "Gemini 2.5 Flash": "gemini-2.5-flash",
                "Gemini 2.0 Flash": "gemini-2.0-flash",
                "Gemini 1.5 Pro": "gemini-1.5-pro",
                "Gemini 1.5 Flash": "gemini-1.5-flash",
                "Gemini 1.0 Pro": "gemini-1.0-pro"
            }
    
    def __init__(self, model: str = None):
        """Initialize the Gemini client.
        
        Args:
            model: Model display name from get_available_models()
        """
        if not genai:
            raise ImportError("Google Generative AI library is required")
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
            
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Get available models dynamically
        available_models = self.get_available_models()
        
        # Use default if no model specified
        if model is None:
            model = list(available_models.keys())[0]  # Use first available model
        
        # Set model based on selection
        if model not in available_models:
            raise ValueError(f"Model '{model}' not available. Choose from: {list(available_models.keys())}")
        
        # Initialize the model
        self.model = genai.GenerativeModel(available_models[model])
        self.model_name = model
    
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
            
            # Configure safety settings to be less restrictive for creative poetry
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Check if response was blocked by safety filters
            if not response.candidates:
                return "Unable to generate content. Here's a gentle poem instead:\n\nWords dance on the page\nLike butterflies in spring air\nPoetry takes flight"
            
            candidate = response.candidates[0]
            
            # Check if content was blocked
            if not candidate.content or not candidate.content.parts:
                # Check safety ratings to understand why it was blocked
                safety_issues = []
                if candidate.safety_ratings:
                    for rating in candidate.safety_ratings:
                        if rating.probability not in ["NEGLIGIBLE", "LOW"]:
                            safety_issues.append(f"{rating.category}: {rating.probability}")
                
                if safety_issues:
                    print(f"Content blocked by safety filters: {', '.join(safety_issues)}")
                    # Try a more neutral version of the prompt
                    neutral_prompt = f"Write a creative and family-friendly poem about: {prompt.split('about')[-1] if 'about' in prompt else 'nature and beauty'}"
                    
                    try:
                        response = self.model.generate_content(
                            neutral_prompt,
                            generation_config=generation_config,
                            safety_settings=safety_settings
                        )
                        
                        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                            return response.text.strip()
                    except:
                        pass
                
                return "The gentle breeze whispers\nThrough leaves of emerald green\nNature's poetry flows"
            
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