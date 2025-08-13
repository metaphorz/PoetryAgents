"""
Gemini Client for Google Generative AI integration.
Refactored to use BaseLLMClient for consistency and reduced duplication.
"""

from typing import Dict
from base_llm_client import BaseLLMClient
from exceptions import APIError, ModelNotAvailableError

try:
    import google.generativeai as genai
except ImportError:
    print("Google Generative AI library not found. Install with: pip install google-generativeai")
    genai = None

class GeminiClient(BaseLLMClient):
    """Client for interacting with Google's Gemini models."""
    
    def __init__(self, model: str = None):
        """Initialize the Gemini client."""
        if not genai:
            raise ImportError("Google Generative AI library is required")
        
        super().__init__(model, 'GEMINI_API_KEY')
    
    def get_available_models(self, limit_recent: int = 6) -> Dict[str, str]:
        """Get available Gemini models from the API."""
        try:
            genai.configure(api_key=self.api_key)
            models = genai.list_models()
            
            # Build models list with display names, filter for text generation models
            model_list = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    model_id = model.name.replace('models/', '')
                    model_list.append((model.display_name, model_id))
            
            # Smart sorting for Gemini
            def model_priority(item):
                display_name = item[0].lower()
                score = 0
                
                if '2.5' in display_name: score += 1000
                elif '2.0' in display_name: score += 800
                elif '1.5' in display_name: score += 600
                elif '1.0' in display_name: score += 400
                
                if 'pro' in display_name: score += 100
                elif 'flash' in display_name: score += 80
                
                if 'preview' not in display_name and 'experimental' not in display_name:
                    score += 50
                
                return score
            
            model_list.sort(key=model_priority, reverse=True)
            
            if limit_recent:
                model_list = model_list[:limit_recent]
            
            available_models = {}
            for display_name, model_id in model_list:
                available_models[display_name] = model_id
            
            return available_models
        except Exception as e:
            return {
                "Gemini 2.5 Pro": "gemini-2.5-pro",
                "Gemini 2.5 Flash": "gemini-2.5-flash",
                "Gemini 2.0 Flash": "gemini-2.0-flash",
                "Gemini 1.5 Pro": "gemini-1.5-pro",
                "Gemini 1.5 Flash": "gemini-1.5-flash",
                "Gemini 1.0 Pro": "gemini-1.0-pro"
            }
    
    def _initialize_client(self):
        """Initialize the Gemini client."""
        genai.configure(api_key=self.api_key)
        self.model_client = genai.GenerativeModel(self.model)
    
    def generate_poetry(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate poetry using Gemini."""
        try:
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.7,
                top_p=0.8,
                top_k=40
            )
            
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
            ]
            
            response = self.model_client.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Handle safety filtering
            if not response.candidates or not response.candidates[0].content:
                return "Words dance on the page\nLike butterflies in spring air\nPoetry takes flight"
            
            return response.text.strip()
            
        except Exception as e:
            raise APIError("Gemini", f"Poetry generation failed: {str(e)}", e)
    
