#!/usr/bin/env python3
"""
Test script to verify model selection fixes for OpenAI, Claude, and Gemini clients.
Verifies that display names properly map to model IDs and clients can be initialized.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_openai_model_selection():
    """Test OpenAI model selection and client initialization."""
    print("🧪 Testing OpenAI Model Selection")
    print("-" * 40)
    
    try:
        from openai_client import OpenAIClient
        
        # Get available models
        models_dict = OpenAIClient.get_available_models()
        print(f"✓ Available models: {len(models_dict)} models")
        
        # Test with display name
        if models_dict:
            display_name = list(models_dict.keys())[0]
            model_id = models_dict[display_name]
            print(f"✓ Testing with display name: '{display_name}' → '{model_id}'")
            
            # Test client creation with model ID (what main.py now passes)
            client = OpenAIClient(model_id)
            print(f"✓ Client created successfully with model ID")
            print(f"✓ Client model: {client.model}")
            print(f"✓ Client model name: {client.model_name}")
            
        print("✅ OpenAI model selection test PASSED\n")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI model selection test FAILED: {e}\n")
        return False

def test_claude_model_selection():
    """Test Claude model selection and client initialization."""
    print("🧪 Testing Claude Model Selection")
    print("-" * 40)
    
    try:
        from llm_client import LLMClient
        
        # Get available models
        models_dict = LLMClient.get_available_models()
        print(f"✓ Available models: {len(models_dict)} models")
        
        # Test with display name
        if models_dict:
            display_name = list(models_dict.keys())[0]
            model_id = models_dict[display_name]
            print(f"✓ Testing with display name: '{display_name}' → '{model_id}'")
            
            # Test client creation with model ID (what main.py now passes)
            client = LLMClient(model_id)
            print(f"✓ Client created successfully with model ID")
            print(f"✓ Client model: {client.model}")
            print(f"✓ Client model name: {client.model_name}")
            
        print("✅ Claude model selection test PASSED\n")
        return True
        
    except Exception as e:
        print(f"❌ Claude model selection test FAILED: {e}\n")
        return False

def test_gemini_model_selection():
    """Test Gemini model selection and client initialization."""
    print("🧪 Testing Gemini Model Selection")
    print("-" * 40)
    
    try:
        from gemini_client import GeminiClient
        
        # Get available models
        models_dict = GeminiClient.get_available_models()
        print(f"✓ Available models: {len(models_dict)} models")
        
        # Test with display name
        if models_dict:
            display_name = list(models_dict.keys())[0]
            model_id = models_dict[display_name]
            print(f"✓ Testing with display name: '{display_name}' → '{model_id}'")
            
            # Test client creation with model ID (what main.py now passes)
            client = GeminiClient(model_id)
            print(f"✓ Client created successfully with model ID")
            print(f"✓ Client model: {client.model}")
            print(f"✓ Client model name: {client.model_name}")
            
        print("✅ Gemini model selection test PASSED\n")
        return True
        
    except Exception as e:
        print(f"❌ Gemini model selection test FAILED: {e}\n")
        return False

def test_openrouter_validation():
    """Test OpenRouter model validation."""
    print("🧪 Testing OpenRouter Model Validation")
    print("-" * 40)
    
    try:
        from openrouter_client import OpenRouterClient
        
        # Get available models first
        models_dict = OpenRouterClient.get_available_models()
        print(f"✓ Available models: {len(models_dict)} models")
        
        if models_dict:
            # Test with the first available model
            model_id = list(models_dict.values())[0]
            print(f"✓ Testing with model: {model_id}")
            
            # Create client with an available model
            client = OpenRouterClient(model_id)
            
            # Test the new check_model_status method
            status = client.check_model_status(model_id)
            
            print(f"✓ Model status check returned: {status.get('available', False)}")
            print(f"✓ Is free model: {status.get('is_free_model', False)}")
        
        print("✅ OpenRouter validation test PASSED\n")
        return True
        
    except Exception as e:
        print(f"❌ OpenRouter validation test FAILED: {e}\n")
        return False

if __name__ == "__main__":
    print("🧪 Model Selection Fix Verification\n")
    print("=" * 50)
    
    results = []
    results.append(test_openai_model_selection())
    results.append(test_claude_model_selection())
    results.append(test_gemini_model_selection())
    results.append(test_openrouter_validation())
    
    print("=" * 50)
    print("📊 Test Results Summary:")
    print(f"✅ Passed: {sum(results)}/{len(results)} tests")
    
    if all(results):
        print("🎉 All model selection fixes are working correctly!")
    else:
        print("⚠️  Some tests failed - review the error messages above")