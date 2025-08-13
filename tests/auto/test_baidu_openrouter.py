#!/usr/bin/env python3
"""
Test OpenRouter integration with Baidu model
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_baidu_openrouter():
    """Test OpenRouter with Baidu model specifically."""
    print("🧪 Testing OpenRouter with Baidu Model")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return False
    
    print(f"✅ OpenRouter API key found: {api_key[:10]}...")
    
    try:
        from openrouter_client import OpenRouterClient
        
        # Test 1: Search for Baidu models
        print("\n🔍 Step 1: Searching for Baidu models...")
        matches = OpenRouterClient.search_models("baidu")
        if matches:
            print(f"✅ Found {len(matches)} Baidu model(s):")
            for i, match in enumerate(matches, 1):
                print(f"  {i}. {match['id']}")
                if match.get('description'):
                    print(f"     {match['description'][:100]}...")
        else:
            print("❌ No Baidu models found")
            return False
        
        # Test 2: Initialize client with Baidu model
        baidu_model = matches[0]['id']  # Use first Baidu model found
        print(f"\n🤖 Step 2: Initializing client with {baidu_model}...")
        client = OpenRouterClient(baidu_model)
        print(f"✅ Client initialized with model: {client.model_id}")
        
        # Test 3: Test connection
        print("\n🔗 Step 3: Testing connection...")
        if client.test_connection():
            print("✅ Connection test successful")
        else:
            print("❌ Connection test failed")
            return False
        
        # Test 4: Generate a simple haiku
        print("\n📝 Step 4: Testing poetry generation...")
        prompt = "Write a haiku about testing software"
        try:
            result = client.generate_poetry(prompt, max_tokens=100)
            print("✅ Poetry generation successful:")
            print("=" * 30)
            print(result)
            print("=" * 30)
        except Exception as e:
            print(f"❌ Poetry generation failed: {e}")
            return False
        
        print("\n🎉 All Baidu OpenRouter tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Baidu OpenRouter: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_baidu_openrouter()
    
    print("\n" + "=" * 50)
    print("🏁 TEST RESULTS")
    print("=" * 50)
    
    if success:
        print("🎉 OpenRouter integration with Baidu model working perfectly!")
        print("\n📋 Ready for production use:")
        print("  ✅ API authentication")
        print("  ✅ Model discovery")
        print("  ✅ Client initialization") 
        print("  ✅ Poetry generation")
    else:
        print("💥 Some tests failed. Check the output above for details.")