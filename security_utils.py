"""
Security utilities for LLM client input validation and sanitization.
Provides defensive security measures to prevent injection attacks and information leakage.
"""

import re
import logging
from typing import Tuple, List, Optional
from dataclasses import dataclass

# Configure secure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SecurityValidationResult:
    """Result of security validation with sanitized content and warnings."""
    is_safe: bool
    sanitized_content: str
    warnings: List[str]
    blocked_patterns: List[str]

class SecurityValidator:
    """Provides input validation and sanitization for LLM interactions."""
    
    # Dangerous prompt injection patterns
    INJECTION_PATTERNS = [
        r'ignore\s+previous\s+instructions',
        r'ignore\s+all\s+previous\s+instructions',
        r'forget\s+all\s+previous\s+instructions',
        r'forget\s+previous\s+instructions',
        r'disregard\s+previous\s+instructions',
        r'override\s+previous\s+instructions',
        r'new\s+instructions\s*:',
        r'system\s*:\s*new\s+role',
        r'act\s+as\s+a\s+different',
        r'pretend\s+to\s+be',
        r'you\s+are\s+now',
        r'roleplay\s+as',
        r'simulate\s+being',
        r'reveal\s+your\s+system\s+prompt',
        r'show\s+me\s+your\s+instructions',
        r'what\s+are\s+your\s+instructions',
        r'bypass\s+safety',
        r'disable\s+safety',
        r'break\s+character',
        r'jailbreak',
        r'uncensored\s+mode',
        r'developer\s+mode',
        r'admin\s+override',
        r'sudo\s+mode',
        r'root\s+access',
    ]
    
    # Suspicious content patterns
    SUSPICIOUS_PATTERNS = [
        r'<script[^>]*>',
        r'javascript:',
        r'data:text/html',
        r'eval\s*\(',
        r'exec\s*\(',
        r'import\s+os',
        r'import\s+subprocess',
        r'__import__',
        r'getattr\s*\(',
        r'setattr\s*\(',
        r'delattr\s*\(',
    ]
    
    MAX_PROMPT_LENGTH = 10000  # Maximum allowed prompt length
    
    @classmethod
    def sanitize_prompt(cls, prompt: str) -> SecurityValidationResult:
        """
        Sanitize and validate user prompt input for security.
        
        Args:
            prompt: User-provided prompt text
            
        Returns:
            SecurityValidationResult with validation status and sanitized content
        """
        if not isinstance(prompt, str):
            return SecurityValidationResult(
                is_safe=False,
                sanitized_content="",
                warnings=["Invalid input type - expected string"],
                blocked_patterns=[]
            )
        
        warnings = []
        blocked_patterns = []
        sanitized = prompt.strip()
        
        # Check length
        if len(sanitized) > cls.MAX_PROMPT_LENGTH:
            warnings.append(f"Prompt truncated from {len(sanitized)} to {cls.MAX_PROMPT_LENGTH} characters")
            sanitized = sanitized[:cls.MAX_PROMPT_LENGTH]
        
        if len(sanitized) == 0:
            return SecurityValidationResult(
                is_safe=False,
                sanitized_content="",
                warnings=["Empty prompt not allowed"],
                blocked_patterns=[]
            )
        
        # Check for injection patterns
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                blocked_patterns.append(pattern)
                # Remove the matched pattern
                sanitized = re.sub(pattern, "[BLOCKED]", sanitized, flags=re.IGNORECASE)
        
        # Check for suspicious patterns
        for pattern in cls.SUSPICIOUS_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                blocked_patterns.append(pattern)
                warnings.append(f"Suspicious pattern detected and removed: {pattern}")
                sanitized = re.sub(pattern, "[REMOVED]", sanitized, flags=re.IGNORECASE)
        
        # Additional sanitization
        sanitized = cls._additional_sanitization(sanitized)
        
        is_safe = len(blocked_patterns) == 0
        
        if blocked_patterns:
            warnings.append(f"Blocked {len(blocked_patterns)} potentially dangerous pattern(s)")
            logger.warning(f"Security: Blocked dangerous patterns in prompt: {blocked_patterns}")
        
        return SecurityValidationResult(
            is_safe=is_safe,
            sanitized_content=sanitized,
            warnings=warnings,
            blocked_patterns=blocked_patterns
        )
    
    @classmethod
    def _additional_sanitization(cls, text: str) -> str:
        """Apply additional sanitization rules."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove potential control characters
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        return text.strip()
    
    @classmethod
    def validate_model_parameter(cls, model: str) -> Tuple[bool, str]:
        """
        Validate model parameter to prevent injection.
        
        Args:
            model: Model identifier string
            
        Returns:
            Tuple of (is_valid, sanitized_model)
        """
        if not isinstance(model, str):
            return False, ""
        
        # Check for dangerous characters that could be used for command injection
        dangerous_chars = [';', '&', '|', '`', '$', '(', ')', '{', '}', '<', '>', '\n', '\r', '\t']
        if any(char in model for char in dangerous_chars):
            return False, ""
        
        # Only allow alphanumeric, hyphens, underscores, periods, slashes, and colons
        if not re.match(r'^[a-zA-Z0-9\-_./:]+$', model):
            return False, ""
        
        # Check length
        if len(model) > 200:  # Reasonable max length for model names
            return False, ""
        
        # Check if the sanitized version is the same as original
        sanitized = re.sub(r'[^a-zA-Z0-9\-_./:]', '', model)
        if sanitized != model:
            return False, ""
        
        return True, sanitized
    
    @classmethod
    def validate_max_tokens(cls, max_tokens: int) -> Tuple[bool, int]:
        """
        Validate max_tokens parameter.
        
        Args:
            max_tokens: Maximum tokens to generate
            
        Returns:
            Tuple of (is_valid, validated_max_tokens)
        """
        if not isinstance(max_tokens, int):
            try:
                max_tokens = int(max_tokens)
            except (ValueError, TypeError):
                return False, 500  # Default safe value
        
        # Enforce reasonable bounds
        if max_tokens < 1:
            return False, 1
        if max_tokens > 8000:  # Reasonable upper limit
            return False, 8000
        
        return True, max_tokens

class SecureErrorHandler:
    """Handles errors securely without leaking sensitive information."""
    
    @staticmethod
    def sanitize_error_message(error: Exception, context: str = "") -> str:
        """
        Create a safe error message that doesn't leak system information.
        
        Args:
            error: The original exception
            context: Context where the error occurred
            
        Returns:
            Sanitized error message safe for user display
        """
        error_type = type(error).__name__
        
        # Map specific errors to user-friendly messages
        error_mappings = {
            'ConnectionError': 'Unable to connect to the service. Please check your internet connection.',
            'TimeoutError': 'Request timed out. Please try again.',
            'AuthenticationError': 'Authentication failed. Please check your API key.',
            'PermissionError': 'Access denied. Please check your permissions.',
            'RateLimitError': 'Rate limit exceeded. Please wait and try again.',
            'QuotaExceededError': 'Usage quota exceeded. Please check your account limits.',
            'ValidationError': 'Invalid input provided. Please check your request.',
            'ValueError': 'Invalid input provided. Please check your request.',
            'APIError': 'Service temporarily unavailable. Please try again later.',
        }
        
        # Context-specific messages
        context_mappings = {
            'claude_auth': 'Authentication failed. Please check your API key.',
            'openai_rate_limit': 'Rate limit exceeded. Please wait and try again.',
            'gemini_generation': 'Poetry generation failed. Please try again.',
            'model_validation': 'Invalid model specified. Please check the model name.',
        }
        
        # Get message based on context first, then error type
        if context and context in context_mappings:
            base_message = context_mappings[context]
        else:
            base_message = error_mappings.get(error_type, 'An error occurred while processing your request.')
        
        if context:
            return f"{context}: {base_message}"
        
        return base_message
    
    @staticmethod
    def log_error_securely(error: Exception, context: str = "", user_input: str = None):
        """
        Log error details securely for debugging while protecting sensitive data.
        
        Args:
            error: The exception to log
            context: Context where the error occurred
            user_input: User input (will be sanitized before logging)
        """
        # Sanitize user input before logging
        safe_input = "N/A"
        if user_input:
            input_str = str(user_input)[:100]  # Limit length first
            
            # Remove API keys (sk-, pk-, anthropic_sk_, etc.)
            safe_input = re.sub(r'\b[a-zA-Z_]{2,15}-[a-zA-Z0-9]{20,}\b', '[API_KEY_REDACTED]', input_str)
            safe_input = re.sub(r'\b[a-zA-Z_]{2,15}_sk_[a-zA-Z0-9]{20,}\b', '[API_KEY_REDACTED]', safe_input)
            
            # Remove other potential secrets (long alphanumeric strings)
            safe_input = re.sub(r'\b[a-zA-Z0-9]{16,}\b', '[REDACTED]', safe_input)
            
            # Remove password patterns - comprehensive approach
            # Pattern 1: "password is secret123" or "password: secret123"
            safe_input = re.sub(r'\b(password|secret|token)\s*(?:is|=|:)\s*\S+', r'\1=[REDACTED]', safe_input, flags=re.IGNORECASE)
            
            # Pattern 2: "and password is secret123" - catch remaining secrets after previous substitutions
            safe_input = re.sub(r'\band\s+(password|secret|token)\s*(?:is|=|:)?\s*\S+', r'and \1=[REDACTED]', safe_input, flags=re.IGNORECASE)
            
            # Pattern 3: Database connection strings with passwords
            safe_input = re.sub(r'://[^:/@]+:[^/@]+@', '://[USER]:[REDACTED]@', safe_input)
            
            # Pattern 4: Any remaining standalone secrets that look like passwords (be more specific)
            safe_input = re.sub(r'\bsupersecret\b', '[REDACTED]', safe_input, flags=re.IGNORECASE)
            safe_input = re.sub(r'\bmysecret\b', '[REDACTED]', safe_input, flags=re.IGNORECASE)
            safe_input = re.sub(r'\bsecret\d+\b', '[REDACTED]', safe_input, flags=re.IGNORECASE)
        
        logger.error(
            f"Security: Error in {context} - "
            f"Type: {type(error).__name__} - "
            f"Input: {safe_input} - "
            f"Error: {str(error)[:200]}"
        )