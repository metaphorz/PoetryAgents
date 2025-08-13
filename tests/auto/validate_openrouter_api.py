#!/usr/bin/env python3
"""
Simple validation script for OpenRouter API
"""

import os
import sys
import requests
sys.path.append('../..')  # Add parent directory for imports

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openrouter_api():
    """Test OpenRouter API directly."""
    print("🔑 Testing OpenRouter API Key...")
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found")
        return False
    
    print(f"✅ API Key loaded: {api_key[:15]}...")
    
    try:
        # Test API connection
        print("\n🌐 Testing API connection...")
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API connection successful")
            
            models = response.json()["data"]
            print(f"✅ Found {len(models)} total models")
            
            # Search for Baidu models
            baidu_models = [m for m in models if "baidu" in m["id"].lower()]
            print(f"\n🔍 Baidu models found: {len(baidu_models)}")
            
            for i, model in enumerate(baidu_models, 1):
                print(f"  {i}. {model['id']}")
                if model.get('name'):
                    print(f"     Name: {model['name']}")
            
            if baidu_models:
                print(f"\n✅ Ready to test with: {baidu_models[0]['id']}")
                return True, baidu_models[0]['id']
            else:
                print("❌ No Baidu models available")
                return False, None
                
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False, None

if __name__ == "__main__":
    success, baidu_model = test_openrouter_api()
    
    if success:
        print(f"\n🎉 OpenRouter API is working!")
        print(f"🚀 Ready to use Baidu model: {baidu_model}")
        print("\n📋 Next steps:")
        print("  1. Run: python main.py")
        print("  2. Choose option 2 (OpenRouter)")
        print("  3. Search for 'baidu' when prompted")
    else:
        print("\n💥 OpenRouter API test failed")