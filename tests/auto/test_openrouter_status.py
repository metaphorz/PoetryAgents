#!/usr/bin/env python3
"""
Test script to demonstrate OpenRouter status checking capabilities.
"""

import os
from dotenv import load_dotenv
from openrouter_client import OpenRouterClient

load_dotenv()

def test_status_checking():
    """Test the new status checking features."""
    
    # Check if OpenRouter API key is available
    if not os.getenv('OPENROUTER_API_KEY'):
        print("⚠️  OPENROUTER_API_KEY not found in environment")
        return
    
    print("🧪 Testing OpenRouter Status Checking\n")
    
    # Test 1: Check account status with a free model
    print("📋 Test 1: Free model status check")
    print("-" * 40)
    try:
        client = OpenRouterClient("meta-llama/llama-3.2-11b-vision-instruct:free")
        print("✅ Free model client initialized successfully")
    except Exception as e:
        print(f"❌ Free model client failed: {e}")
    
    print("\n" + "=" * 50 + "\n")
    
    # Test 2: Check account status with a paid model
    print("📋 Test 2: Paid model status check")
    print("-" * 40)
    try:
        client = OpenRouterClient("anthropic/claude-3.5-sonnet")
        print("✅ Paid model client initialized successfully")
    except Exception as e:
        print(f"❌ Paid model client failed: {e}")
    
    print("\n" + "=" * 50 + "\n")
    
    # Test 3: Check specific model status
    print("📋 Test 3: Model-specific status check")
    print("-" * 40)
    try:
        client = OpenRouterClient("claude")  # Will find Claude model
        
        # Check status of a free model
        free_status = client.check_model_status("meta-llama/llama-3.2-11b-vision-instruct:free")
        print(f"Free model status: {free_status}")
        
        # Check status of a paid model
        paid_status = client.check_model_status("anthropic/claude-3.5-sonnet")
        print(f"Paid model status: {paid_status}")
        
    except Exception as e:
        print(f"❌ Model status check failed: {e}")

if __name__ == "__main__":
    test_status_checking()