"""
OpenRouter Client for unified LLM API access
Handles communication with multiple LLM providers through OpenRouter.
"""

import os
import requests
import time
from typing import Optional, Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    import openai
except ImportError:
    print("OpenAI library not found. Install with: pip install openai")
    openai = None

class OpenRouterClient:
    """Client for interacting with multiple LLMs through OpenRouter."""
    
    def __init__(self, model_identifier: str):
        """Initialize the OpenRouter client.
        
        Args:
            model_identifier: Either a search term (e.g., "Claude") or exact model ID (e.g., "anthropic/claude-3.5-sonnet")
        """
        if not openai:
            raise ImportError("OpenAI library is required for OpenRouter")
        
        # Get API key from environment
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        self.api_key = api_key
        self.model_identifier = model_identifier
        
        # Check if it's already a model ID (contains "/") or needs to be found
        if "/" in model_identifier:
            self.model_id = model_identifier
            self.model_name = f"OpenRouter ({model_identifier})"
        else:
            self.model_id = self._find_model(model_identifier)
            self.model_name = f"OpenRouter ({model_identifier})"
        
        # Initialize OpenAI client pointing to OpenRouter
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # Check account status and warn about potential issues
        self._check_account_status()
    
    def _check_account_status(self):
        """Check account status and warn about potential rate limit issues."""
        try:
            response = requests.get(
                "https://openrouter.ai/api/v1/auth/key",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if using free model
                is_free_model = ":free" in self.model_id
                
                # Get account info
                usage = data.get("usage", 0)
                limit = data.get("limit")
                is_free_tier = data.get("is_free_tier", True)
                
                # Calculate credits remaining
                credits_remaining = None
                if limit is not None:
                    credits_remaining = limit - usage
                
                # Warn about potential issues
                warnings = []
                
                if is_free_model:
                    if is_free_tier:
                        warnings.append("⚠️  Using free model with free tier account - daily limit: 50 requests")
                        warnings.append("💡 Consider purchasing 10+ credits to unlock 1000 daily requests")
                    else:
                        warnings.append("ℹ️  Using free model - daily limit: 1000 requests (20/minute)")
                    warnings.append("⚠️  Free models may have upstream rate limits from providers")
                
                if credits_remaining is not None and credits_remaining < 1:
                    warnings.append("⚠️  Low credits remaining - consider adding more credits")
                
                if warnings:
                    print("\n" + "\n".join(warnings))
                    print(f"📊 Account: {usage} credits used" + 
                          (f" / {limit} limit" if limit else " (unlimited)"))
                    print(f"🤖 Model: {self.model_id}")
                    print()
                    
        except Exception as e:
            # Don't fail initialization if status check fails
            print(f"Note: Unable to check account status: {e}")
    
    def _get_available_models(self) -> List[Dict]:
        """Fetch available models from OpenRouter API."""
        try:
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                }
            )
            response.raise_for_status()
            return response.json()["data"]
        except Exception as e:
            print(f"Error fetching OpenRouter models: {e}")
            return []
    
    def _find_model(self, search_term: str) -> str:
        """Find the best matching model ID for the search term.
        
        Args:
            search_term: Search term like "Claude", "GPT-4", "Baidu"
            
        Returns:
            Model ID string for OpenRouter API
        """
        models = self._get_available_models()
        search_lower = search_term.lower()
        
        # Try exact matches first
        for model in models:
            model_id = model["id"]
            if search_lower in model_id.lower():
                print(f"Found model: {model_id}")
                return model_id
        
        # Try partial matches in name/description
        for model in models:
            model_id = model["id"]
            model_name = model.get("name", "").lower()
            
            if (search_lower in model_name or 
                search_lower in model_id.lower() or
                any(search_lower in part for part in model_id.split("/"))):
                print(f"Found model: {model_id}")
                return model_id
        
        # Fallback options based on common searches - prefer paid models
        fallback_models = {
            "claude": "anthropic/claude-3.5-sonnet",
            "gpt": "openai/gpt-4o",
            "gpt-4": "openai/gpt-4o", 
            "gemini": "google/gemini-pro",
            "llama": "meta-llama/llama-3.2-90b-vision-instruct",  # Paid model
            "baidu": "baidu/ernie-4.5-300b-a47b",
            "cohere": "cohere/command-r-plus",
            "mistral": "mistralai/mistral-large",
            "anthropic": "anthropic/claude-3.5-sonnet"
        }
        
        for key, model_id in fallback_models.items():
            if key in search_lower:
                print(f"Using fallback model: {model_id}")
                return model_id
        
        # Ultimate fallback
        print(f"No match found for '{search_term}', using default GPT-4o")
        return "openai/gpt-4o"
    
    @classmethod
    def search_models(cls, search_term: str = "") -> List[Dict]:
        """Search for available models matching the term.
        
        Args:
            search_term: Optional search term to filter models
            
        Returns:
            List of matching model dictionaries
        """
        try:
            api_key = os.getenv('OPENROUTER_API_KEY')
            if not api_key:
                return []
            
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            response.raise_for_status()
            models = response.json()["data"]
            
            if not search_term:
                return models[:20]  # Return first 20 if no search
            
            search_lower = search_term.lower()
            matches = []
            
            for model in models:
                model_id = model["id"]
                model_name = model.get("name", "")
                
                if (search_lower in model_id.lower() or 
                    search_lower in model_name.lower()):
                    matches.append({
                        "id": model_id,
                        "name": model_name,
                        "description": model.get("description", "")
                    })
            
            # Sort by relevance (exact matches first, then partial)
            def relevance_score(match):
                model_id = match["id"].lower()
                if model_id.startswith(search_lower):
                    return 0  # Highest priority for prefix matches
                elif search_lower in model_id.split("/")[0]:
                    return 1  # High priority for provider matches
                elif search_lower in model_id:
                    return 2  # Medium priority for partial ID matches
                else:
                    return 3  # Lowest priority for name/description matches
            
            matches.sort(key=relevance_score)
            return matches[:15]  # Return top 15 matches
            
        except Exception as e:
            print(f"Error searching models: {e}")
            return []
    
    def check_model_status(self, model_id: str) -> Dict:
        """Check if a specific model is available and any known issues.
        
        Args:
            model_id: The model ID to check
            
        Returns:
            Dict with status information
        """
        try:
            # Get model info
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            
            if response.status_code == 200:
                models = response.json()["data"]
                
                # Find the specific model
                model_info = None
                for model in models:
                    if model["id"] == model_id:
                        model_info = model
                        break
                
                if model_info:
                    is_free = ":free" in model_id
                    
                    return {
                        "available": True,
                        "is_free_model": is_free,
                        "pricing": model_info.get("pricing", {}),
                        "context_length": model_info.get("context_length", 0),
                        "warnings": [
                            "Free model - may have upstream rate limits"
                        ] if is_free else []
                    }
                else:
                    return {
                        "available": False,
                        "error": f"Model {model_id} not found"
                    }
            else:
                return {
                    "available": False,
                    "error": f"API error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "available": False,
                "error": f"Error checking model status: {str(e)}"
            }
    
    def _get_paid_alternatives(self, free_model_id: str) -> List[str]:
        """Get paid alternatives for a free model.
        
        Args:
            free_model_id: The free model ID (with :free suffix)
            
        Returns:
            List of paid model alternatives
        """
        # Remove :free suffix to get base model
        base_model = free_model_id.replace(":free", "")
        
        # Common paid alternatives for popular free models
        alternatives = {
            "meta-llama/llama-3.2-11b-vision-instruct": [
                "meta-llama/llama-3.2-90b-vision-instruct",
                "meta-llama/llama-3.1-70b-instruct",
                "anthropic/claude-3.5-sonnet"
            ],
            "meta-llama/llama-3.2-3b-instruct": [
                "meta-llama/llama-3.2-90b-vision-instruct",
                "meta-llama/llama-3.1-70b-instruct"
            ],
            "meta-llama/llama-3.1-8b-instruct": [
                "meta-llama/llama-3.1-70b-instruct",
                "meta-llama/llama-3.2-90b-vision-instruct"
            ],
            "mistralai/mistral-7b-instruct": [
                "mistralai/mistral-large",
                "mistralai/mixtral-8x7b-instruct"
            ],
            "google/gemma-7b-it": [
                "google/gemini-pro",
                "google/gemma-2-27b-it"
            ]
        }
        
        # Try to find exact match first
        if base_model in alternatives:
            return alternatives[base_model]
        
        # Otherwise suggest general high-quality paid models
        return [
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o",
            "meta-llama/llama-3.2-90b-vision-instruct"
        ]
    
    def generate_poetry(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate poetry using OpenRouter with retry logic for rate limits.
        
        Args:
            prompt: The prompt for poetry generation
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated poetry text
        """
        max_retries = 3
        base_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_id,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7,
                    extra_headers={
                        "HTTP-Referer": "https://github.com/anthropics/claude-code",
                        "X-Title": "Poetry Agents",
                    }
                )
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                error_str = str(e)
                
                # Check for rate limit errors
                if "429" in error_str and "rate-limited" in error_str:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)  # Exponential backoff
                        print(f"Rate limit hit for {self.model_id}. Retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(delay)
                        continue
                    else:
                        # Extract helpful information from the error
                        if "temporarily rate-limited upstream" in error_str:
                            model_name = self.model_id.split("/")[-1] if "/" in self.model_id else self.model_id
                            is_free_model = ":free" in self.model_id
                            
                            # Suggest paid alternatives for free models
                            paid_alternatives = self._get_paid_alternatives(self.model_id)
                            
                            suggestions = [
                                "1. Use a paid model (not ending in ':free') - your credits will work normally",
                                "2. Wait a few minutes and try again",
                                "3. Use direct API mode instead of OpenRouter (option 1 in main menu)"
                            ]
                            
                            if is_free_model and paid_alternatives:
                                suggestions.insert(1, f"   💡 Try these paid alternatives: {', '.join(paid_alternatives)}")
                                suggestions.append("4. Free models have upstream rate limits regardless of your credits")
                                suggestions.append("5. Add your own API key at https://openrouter.ai/settings/integrations")
                            elif is_free_model:
                                suggestions.append("4. Free models have strict rate limits - consider using paid models")
                                suggestions.append("5. Add your own API key at https://openrouter.ai/settings/integrations")
                            
                            raise Exception(f"The model '{model_name}' is temporarily rate-limited. Please try:\n" + 
                                          "\n".join(suggestions))
                        else:
                            raise Exception(f"Rate limit exceeded after {max_retries} attempts: {error_str}")
                
                # Check for other common errors
                elif "401" in error_str or "unauthorized" in error_str.lower():
                    raise Exception(f"OpenRouter API authentication failed. Please check your OPENROUTER_API_KEY in .env file")
                elif "404" in error_str:
                    raise Exception(f"Model '{self.model_id}' not found. Please check the model name or try a different model")
                else:
                    # For other errors, don't retry
                    raise Exception(f"Error generating poetry with OpenRouter: {error_str}")
        
        # This should never be reached, but just in case
        raise Exception("Maximum retry attempts exceeded")
    
    def test_connection(self) -> bool:
        """Test the connection to OpenRouter.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            test_response = self.generate_poetry("Write a simple two-word poem.", max_tokens=10)
            return len(test_response.strip()) > 0
        except Exception as e:
            print(f"Connection test error: {str(e)}")
            return False