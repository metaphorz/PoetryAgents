#!/usr/bin/env python3
"""
Simple test to verify the generated HTML interface works correctly.
"""

import re
import os

def test_html_interface():
    """Test the generated HTML interface."""
    print("🧪 Testing Poetry Agents HTML Interface")
    print("=" * 50)
    
    # Check if the HTML file exists
    html_file = "poetry_generator_live.html"
    if not os.path.exists(html_file):
        print(f"❌ Error: {html_file} not found!")
        return False
    
    print(f"✅ Found: {html_file}")
    
    # Read the HTML content
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test 1: Check if model data is embedded
    if 'const modelData =' in content:
        print("✅ Model data properly embedded")
    else:
        print("❌ Model data not found!")
        return False
    
    # Test 2: Check if OpenRouter data is embedded
    if 'const openrouterModelData =' in content:
        print("✅ OpenRouter model data properly embedded")
    else:
        print("❌ OpenRouter model data not found!")
        return False
    
    # Test 3: Check for Claude models
    claude_pattern = r'"Claude":\s*{[^}]*"Claude Sonnet 4"'
    if re.search(claude_pattern, content):
        print("✅ Claude models found (including Claude Sonnet 4)")
    else:
        print("⚠️  Claude models might not be current")
    
    # Test 4: Check for OpenAI models
    openai_pattern = r'"OpenAI":\s*{[^}]*"GPT-4o"'
    if re.search(openai_pattern, content):
        print("✅ OpenAI models found")
    else:
        print("⚠️  OpenAI models might not be current")
    
    # Test 5: Check for Gemini models
    gemini_pattern = r'"Gemini":\s*{[^}]*"Gemini"'
    if re.search(gemini_pattern, content):
        print("✅ Gemini models found")
    else:
        print("⚠️  Gemini models might not be current")
    
    # Test 6: Check for proper HTML structure
    required_elements = [
        '<form id="poetryForm">',
        'name="apiMode"',
        'name="poet1Provider"',
        'name="poet2Provider"',
        'name="theme"',
        'name="form"',
        'name="conversationLength"',
        'name="emojis"'
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in content:
            missing_elements.append(element)
    
    if not missing_elements:
        print("✅ All required HTML form elements present")
    else:
        print(f"❌ Missing HTML elements: {missing_elements}")
        return False
    
    # Test 7: Check JavaScript functions
    required_functions = [
        'function toggleApiMode()',
        'function loadModelsForPoet(',
        'function loadOpenrouterModelsForPoet(',
        'function generatePythonScript('
    ]
    
    missing_functions = []
    for func in required_functions:
        if func not in content:
            missing_functions.append(func)
    
    if not missing_functions:
        print("✅ All required JavaScript functions present")
    else:
        print(f"❌ Missing JavaScript functions: {missing_functions}")
        return False
    
    # Test 8: Check file size (should be substantial)
    file_size = len(content)
    if file_size > 30000:  # Should be at least 30KB with embedded data
        print(f"✅ File size appropriate: {file_size} bytes")
    else:
        print(f"⚠️  File size seems small: {file_size} bytes")
    
    # Test 9: Count models
    claude_models = len(re.findall(r'"[^"]*":\s*"claude-[^"]*"', content))
    openai_models = len(re.findall(r'"[^"]*":\s*"gpt-[^"]*"', content))
    gemini_models = len(re.findall(r'"[^"]*":\s*"gemini-[^"]*"', content))
    
    total_models = claude_models + openai_models + gemini_models
    print(f"📊 Model count: {total_models} total ({claude_models} Claude, {openai_models} OpenAI, {gemini_models} Gemini)")
    
    if total_models > 15:  # Should have a good number of models
        print("✅ Good model coverage")
    else:
        print("⚠️  Model count seems low")
    
    print(f"\n🎉 HTML interface test completed successfully!")
    print(f"💡 Open {html_file} in your browser to use the interface")
    return True

if __name__ == '__main__':
    test_html_interface()