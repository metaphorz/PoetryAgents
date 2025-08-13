#!/usr/bin/env python3
"""
Simple test to verify OpenRouter client can be imported
"""

import sys
import os
# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from openrouter_client import OpenRouterClient
    print("✅ OpenRouterClient imported successfully")
    
    # Test without API key - should fail gracefully
    try:
        client = OpenRouterClient("test")
        print("❌ Should have failed without API key")
    except ValueError as e:
        if "OPENROUTER_API_KEY" in str(e):
            print("✅ Correctly requires API key")
        else:
            print(f"❌ Unexpected error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")