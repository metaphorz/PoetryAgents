"""
OpenRouter Client for unified LLM API access
Handles communication with multiple LLM providers through OpenRouter.
"""

import os
import requests
import time
from typing import Optional, Dict, List, Any
from dotenv import load_dotenv
from base_llm_client import BaseLLMClient

# Load environment variables from .env file
load_dotenv()

try:
    import openai
except ImportError:
    print("OpenAI library not found. Install with: pip install openai")
    openai = None

class OpenRouterClient(BaseLLMClient):
    """Client for interacting with multiple LLMs through OpenRouter."""
    
    @classmethod
    def get_available_models(cls, limit_recent=6):
        """Fetch available OpenRouter models and return as display_name: model_id dict."""
        try:
            api_key = os.getenv('OPENROUTER_API_KEY')
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY environment variable is required")
            
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={
                    "Authorization": f"Bearer {api_key}",
                }
            )
            response.raise_for_status()
            models = response.json()["data"]
            
            # Build models dict with provider/model format for display
            # Filter out models that require additional API keys (BYOK models)
            available_models = {}
            for model in models[:limit_recent] if limit_recent else models:
                model_id = model["id"]
                description = model.get("description", "")
                
                # Skip models that require "Bring Your Own Key" (BYOK)
                if ("BYOK is required" in description or 
                    "bring your own key" in description.lower()):
                    continue
                    
                # Create a readable display name
                if "/" in model_id:
                    provider, model_name = model_id.split("/", 1)
                    display_name = f"{provider.title()} {model_name.replace('-', ' ').title()}"
                else:
                    display_name = model_id.replace('-', ' ').title()
                
                available_models[display_name] = model_id
            
            return available_models
            
        except Exception as e:
            raise Exception(f"Failed to fetch OpenRouter models: {str(e)}")
    
    def __init__(self, model: str = None):
        """Initialize the OpenRouter client.
        
        Args:
            model: Model display name from get_available_models(), or model identifier like 'Claude' for search
        """
        # Store the original model for potential search functionality
        self.model_identifier = model if model else "anthropic/claude-3.5-sonnet"
        
        # For OpenRouter, we handle model validation differently since the available models
        # can be a very large list and we want to allow any valid OpenRouter model ID
        self.api_key_env = 'OPENROUTER_API_KEY'
        self.api_key = self._get_api_key()
        
        # Set model directly without base class validation for OpenRouter
        # since we validate through the OpenRouter API directly
        if model:
            self.model = model
            self.model_name = model
        else:
            self.model = "anthropic/claude-3.5-sonnet"
            self.model_name = "Claude 3.5 Sonnet"
        
        # Initialize the client
        self._initialize_client()
        
        # Check account status and warn about potential issues
        self._check_account_status()
    
    def _get_api_key(self) -> str:
        """Get API key from environment variables."""
        if not self.api_key_env:
            raise ValueError("API key environment variable name not specified")
        
        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise ValueError(f"{self.api_key_env} environment variable is required")
        
        return api_key
    
    def test_connection(self) -> bool:
        """
        Test the connection to the API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            test_response = self.generate_poetry("Write a simple two-word poem.", max_tokens=10)
            return len(test_response.strip()) > 0
        except Exception:
            return False
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the current model."""
        return {
            'provider': 'OpenRouter',
            'model_name': self.model_name,
            'model_id': self.model
        }
    
    def _initialize_client(self):
        """Initialize the OpenAI client pointing to OpenRouter."""
        if not openai:
            raise ImportError("OpenAI library is required for OpenRouter")
            
        # Initialize OpenAI client pointing to OpenRouter
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
    
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
                is_free_model = ":free" in self.model
                
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
                    print(f"🤖 Model: {self.model}")
                    print()
                    
        except Exception as e:
            # Don't fail initialization if status check fails
            pass
    
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
                # Filter out BYOK models and return first 20
                filtered_models = []
                for model in models:
                    model_id = model["id"]
                    description = model.get("description", "")
                    # Skip BYOK models only
                    if not ("BYOK is required" in description or 
                            "bring your own key" in description.lower()):
                        filtered_models.append(model)
                return filtered_models[:20]
            
            search_lower = search_term.lower()
            matches = []
            
            for model in models:
                model_id = model["id"]
                model_name = model.get("name", "")
                description = model.get("description", "")
                
                # Skip models that require "Bring Your Own Key" (BYOK)
                if ("BYOK is required" in description or 
                    "bring your own key" in description.lower()):
                    continue
                
                if (search_lower in model_id.lower() or 
                    search_lower in model_name.lower()):
                    matches.append({
                        "id": model_id,
                        "name": model_name,
                        "description": description
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
    
    def check_model_status(self, model_id: str) -> Dict[str, Any]:
        """Check if a model is available and get its status.
        
        Args:
            model_id: The model ID to check
            
        Returns:
            Dict containing availability and metadata about the model
        """
        try:
            # Fetch all available models
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            models = response.json()["data"]
            
            # Find the specific model
            model_found = None
            for model in models:
                if model["id"] == model_id:
                    model_found = model
                    break
            
            if not model_found:
                return {
                    "available": False,
                    "is_free_model": False,
                    "error": f"Model {model_id} not found in available models"
                }
            
            # Check if it's a free model (ends with :free)
            is_free_model = model_id.endswith(":free")
            
            return {
                "available": True,
                "is_free_model": is_free_model,
                "model_data": model_found,
                "pricing": model_found.get("pricing", {}),
                "context_length": model_found.get("context_length", 0)
            }
            
        except Exception as e:
            return {
                "available": False,
                "is_free_model": False,
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
                    model=self.model,
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
                        print(f"Rate limit hit for {self.model}. Retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(delay)
                        continue
                    else:
                        # Extract helpful information from the error
                        if "temporarily rate-limited upstream" in error_str:
                            model_name = self.model.split("/")[-1] if "/" in self.model else self.model
                            is_free_model = ":free" in self.model
                            
                            # Suggest paid alternatives for free models
                            paid_alternatives = self._get_paid_alternatives(self.model)
                            
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
                    raise Exception(f"Model '{self.model}' not found. Please check the model name or try a different model")
                else:
                    # For other errors, don't retry
                    raise Exception(f"Error generating poetry with OpenRouter: {error_str}")
        
        # This should never be reached, but just in case
        raise Exception("Maximum retry attempts exceeded")