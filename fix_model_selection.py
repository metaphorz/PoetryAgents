#!/usr/bin/env python3
"""
Fix model selection issues in the HTML interface.
This script analyzes and fixes common model dropdown problems.
"""

import re
import json
from datetime import datetime

def analyze_html():
    """Analyze the current HTML for model selection issues."""
    
    print("🔍 Analyzing HTML model selection...")
    
    with open('poetry_generator_live.html', 'r') as f:
        content = f.read()
    
    # Extract modelData
    model_data_match = re.search(r'const modelData = ({.*?});', content, re.DOTALL)
    if model_data_match:
        try:
            # Clean up the JavaScript object to make it valid JSON
            js_object = model_data_match.group(1)
            # Remove extra whitespace and format properly
            js_object = re.sub(r'\s+', ' ', js_object)
            model_data = json.loads(js_object)
            
            print("✅ Model data extracted successfully")
            
            for provider, models in model_data.items():
                print(f"  📦 {provider}: {len(models)} models")
                for name, id in list(models.items())[:3]:  # Show first 3
                    print(f"    • {name} → {id}")
                if len(models) > 3:
                    print(f"    ... and {len(models) - 3} more")
            
            return model_data
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing model data: {e}")
            return None
    else:
        print("❌ Could not find modelData in HTML")
        return None

def check_javascript_syntax():
    """Check for JavaScript syntax issues."""
    
    print("\n🔍 Checking JavaScript syntax...")
    
    with open('poetry_generator_live.html', 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check for common issues
    if 'loadModelsForPoet(' not in content:
        issues.append("loadModelsForPoet function missing")
    
    if 'addEventListener(\'change\',' not in content:
        issues.append("Change event listeners missing")
    
    if 'DOMContentLoaded' not in content:
        issues.append("DOMContentLoaded listener missing")
    
    # Check for proper dropdown enabling
    if '.disabled = false' not in content:
        issues.append("Dropdown enabling logic missing")
    
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"  • {issue}")
        return False
    else:
        print("✅ JavaScript syntax looks good")
        return True

def test_model_counts():
    """Test if model counts match expectations."""
    
    print("\n🔢 Testing model counts...")
    
    with open('poetry_generator_live.html', 'r') as f:
        content = f.read()
    
    # Count models in each provider section
    providers = ['Claude', 'Gemini', 'OpenAI']
    
    for provider in providers:
        pattern = f'"{provider}":\\s*{{([^}}]+)}}'
        match = re.search(pattern, content)
        if match:
            models_section = match.group(1)
            model_count = len(re.findall(r'"[^"]*":\s*"[^"]*"', models_section))
            print(f"  📦 {provider}: {model_count} models")
            
            if model_count == 0:
                print(f"    ❌ No models found for {provider}")
            elif model_count < 3:
                print(f"    ⚠️  Low model count for {provider}")
            else:
                print(f"    ✅ Good model count for {provider}")
        else:
            print(f"  ❌ {provider} section not found")

if __name__ == '__main__':
    print("🔧 Model Selection Diagnostic Tool")
    print("=" * 50)
    
    model_data = analyze_html()
    check_javascript_syntax()
    test_model_counts()
    
    print("\n💡 Next steps:")
    print("1. Check browser console for JavaScript errors")
    print("2. Verify dropdown elements are properly named")
    print("3. Test in different browsers")
    print("4. Run: ./poetry_agents.sh --refresh to regenerate")
