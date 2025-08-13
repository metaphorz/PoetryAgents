"""
Custom exceptions for the Poetry Agent system.
Provides structured error handling throughout the application.
"""

class PoetryAgentError(Exception):
    """Base exception for Poetry Agent system."""
    pass

class APIError(PoetryAgentError):
    """Raised when API calls fail."""
    
    def __init__(self, provider: str, message: str, original_error: Exception = None):
        self.provider = provider
        self.original_error = original_error
        super().__init__(f"{provider} API Error: {message}")

class ConfigurationError(PoetryAgentError):
    """Raised when configuration is invalid."""
    pass

class ModelNotAvailableError(PoetryAgentError):
    """Raised when requested model is not available."""
    
    def __init__(self, model: str, provider: str, available_models: list):
        self.model = model
        self.provider = provider
        self.available_models = available_models
        super().__init__(f"Model '{model}' not available for {provider}. Available models: {', '.join(available_models)}")

class ValidationError(PoetryAgentError):
    """Raised when input validation fails."""
    pass

class FileOperationError(PoetryAgentError):
    """Raised when file operations fail."""
    pass

class PromptGenerationError(PoetryAgentError):
    """Raised when prompt generation fails."""
    pass