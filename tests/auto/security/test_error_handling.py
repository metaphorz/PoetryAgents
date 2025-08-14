#!/usr/bin/env python3
"""
Error Handling Security Tests
Tests for secure error handling and information disclosure prevention.
"""

import sys
import os
import unittest
import tempfile
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from security_utils import SecureErrorHandler
from exceptions import APIError

class TestErrorHandlingSecurity(unittest.TestCase):
    """Test secure error handling implementation."""
    
    def test_error_message_sanitization(self):
        """Test that error messages don't leak sensitive information."""
        sensitive_data_tests = [
            # API endpoints and URLs
            (ConnectionError("Failed to connect to https://api.secret-service.com/v1/admin"), 
             ["api.secret-service.com", "/v1/admin"]),
            
            # File paths
            (FileNotFoundError("No such file: /home/user/.secrets/api_keys.txt"),
             ["/home/user/.secrets", "api_keys.txt"]),
            
            # API keys and tokens
            (ValueError("Invalid API key: sk-1234567890abcdef"),
             ["sk-1234567890abcdef"]),
            
            # Database connection strings
            (Exception("Database error: postgres://user:pass@localhost:5432/secret_db"),
             ["postgres://", "user:pass", "secret_db"]),
            
            # Internal server details
            (Exception("Internal server error on server-internal-01.company.com:8080"),
             ["server-internal-01.company.com:8080"]),
        ]
        
        for error, sensitive_items in sensitive_data_tests:
            with self.subTest(error=str(error)):
                safe_message = SecureErrorHandler.sanitize_error_message(error, "test_context")
                
                # Should not contain any sensitive information
                for item in sensitive_items:
                    self.assertNotIn(item, safe_message, 
                                   f"Sensitive data '{item}' found in: {safe_message}")
                
                # Should contain context
                self.assertIn("test_context", safe_message)
                
                # Should be user-friendly
                self.assertGreater(len(safe_message), 20)
                self.assertNotIn("Traceback", safe_message)
                self.assertNotIn("Exception", safe_message)
    
    def test_error_type_mapping(self):
        """Test that different error types map to appropriate user messages."""
        error_mappings = [
            (ConnectionError("Network error"), "connect"),
            (TimeoutError("Request timeout"), "timed out"),
            (PermissionError("Access denied"), "permission"),
            (ValueError("Invalid input"), "Invalid input"),
        ]
        
        for error, expected_keyword in error_mappings:
            with self.subTest(error=type(error).__name__):
                safe_message = SecureErrorHandler.sanitize_error_message(error)
                self.assertIn(expected_keyword.lower(), safe_message.lower())
    
    def test_secure_logging_redaction(self):
        """Test that logging properly redacts sensitive information."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as log_file:
            # Set up logging
            logger = logging.getLogger('security_utils')
            handler = logging.FileHandler(log_file.name)
            logger.addHandler(handler)
            logger.setLevel(logging.ERROR)
            
            try:
                # Test cases with sensitive data
                sensitive_inputs = [
                    "My API key is sk-1234567890abcdef and token is pk-9876543210fedcba",
                    "Password is secret123 and the token is bearer_abc123def456",
                    "Database connection: postgres://admin:supersecret@db.example.com",
                    "API key: anthropic_sk_1234567890abcdef1234567890abcdef",
                    "OpenAI key: sk-proj-1234567890abcdef and secret is mysecret",
                ]
                
                for user_input in sensitive_inputs:
                    with self.subTest(input=user_input[:50] + "..."):
                        error = Exception("Test error")
                        SecureErrorHandler.log_error_securely(error, "test_context", user_input)
                
                # Read and check log content
                log_file.seek(0)
                log_content = log_file.read()
                
                # Should not contain any API keys or secrets
                sensitive_patterns = [
                    "sk-1234567890abcdef",
                    "pk-9876543210fedcba", 
                    "secret123",
                    "supersecret",
                    "mysecret",
                    "bearer_abc123def456",
                    "anthropic_sk_1234567890abcdef1234567890abcdef",
                    "sk-proj-1234567890abcdef",
                ]
                
                for pattern in sensitive_patterns:
                    self.assertNotIn(pattern, log_content, 
                                   f"Sensitive pattern '{pattern}' found in logs")
                
                # Should contain redaction markers
                self.assertIn("[REDACTED]", log_content)
                self.assertIn("test_context", log_content)
                
            finally:
                logger.removeHandler(handler)
                os.unlink(log_file.name)
    
    def test_api_error_creation(self):
        """Test that APIError creation doesn't leak information."""
        original_errors = [
            Exception("Internal error: Failed to connect to database at secret-db.internal:5432"),
            ConnectionError("Network error: Could not reach https://internal-api.company.com/secret"),
            ValueError("Validation failed: Invalid API key sk-1234567890abcdef"),
        ]
        
        for original_error in original_errors:
            with self.subTest(error=str(original_error)):
                # Create APIError with secure message
                safe_message = SecureErrorHandler.sanitize_error_message(original_error)
                api_error = APIError("TestProvider", safe_message, original_error)
                
                # Public message should be safe
                self.assertNotIn("secret-db.internal", str(api_error))
                self.assertNotIn("internal-api.company.com", str(api_error))
                self.assertNotIn("sk-1234567890abcdef", str(api_error))
                
                # Should contain provider and safe message
                self.assertIn("TestProvider", str(api_error))
    
    def test_context_preservation(self):
        """Test that important context is preserved while removing sensitive data."""
        test_cases = [
            ("claude_auth", "Authentication failed", "authentication"),
            ("openai_rate_limit", "Rate limit exceeded", "rate limit"),
            ("gemini_generation", "Generation failed", "failed"),
            ("model_validation", "Invalid model", "model"),
        ]
        
        for context, message, expected_keyword in test_cases:
            with self.subTest(context=context):
                error = Exception(f"Detailed error: {message} due to internal reasons")
                safe_message = SecureErrorHandler.sanitize_error_message(error, context)
                
                # Should contain context and expected keyword
                self.assertIn(context, safe_message)
                self.assertIn(expected_keyword.lower(), safe_message.lower())
                
                # Should not contain internal details
                self.assertNotIn("internal reasons", safe_message)
                self.assertNotIn("Detailed error", safe_message)

def run_error_handling_tests():
    """Run error handling security tests with detailed reporting."""
    print("🛡️ ERROR HANDLING SECURITY TESTS")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestErrorHandlingSecurity)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total - failures - errors
    
    print(f"\n{'='*50}")
    print(f"ERROR HANDLING TEST RESULTS")
    print(f"{'='*50}")
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}") 
    print(f"Errors: {errors}")
    print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "0%")
    
    if failures > 0:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}")
    
    if errors > 0:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_error_handling_tests()
    sys.exit(0 if success else 1)