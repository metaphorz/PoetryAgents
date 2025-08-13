import os
import sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

print("Testing OpenRouter API Key...")
api_key = os.getenv('OPENROUTER_API_KEY')
if api_key:
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        from openrouter_client import OpenRouterClient
        print("✅ OpenRouterClient imported successfully")
        
        # Test search for Baidu
        print("🔍 Searching for Baidu models...")
        matches = OpenRouterClient.search_models("baidu")
        print(f"Found {len(matches)} matches:")
        for match in matches:
            print(f"  - {match['id']}")
        
        if matches:
            print("✅ Baidu model search successful!")
        else:
            print("❌ No Baidu models found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ No API key found")