#!/usr/bin/env python3
"""
Create Simple Fix for Dropdown Issue
Creates a clean, working version without syntax errors.
"""

import os
import re

def create_simple_fixed_version():
    """Create a simple, clean fixed version."""
    
    print("🛠️ Creating simple, clean fix...")
    
    # Read the original file
    with open("poetry_generator_live.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the loadModelsForPoet function and add simple debug
    pattern = r'(function loadModelsForPoet\(poetNumber, provider\) \{[^}]+\})'
    
    simple_load_function = '''function loadModelsForPoet(poetNumber, provider) {
            console.log('Loading models for poet', poetNumber, 'provider:', provider);
            const modelSelect = document.getElementById(`poet${poetNumber}Model`);
            
            if (!modelSelect) {
                console.error('Model select not found:', `poet${poetNumber}Model`);
                return;
            }
            
            if (!provider) {
                console.log('No provider - disabling dropdown');
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                return;
            }

            const models = modelData[provider];
            console.log('Models found:', models ? Object.keys(models).length : 0);
            
            if (!models) {
                console.log('No models available for provider:', provider);
                modelSelect.innerHTML = '<option value="">No models available</option>';
                modelSelect.disabled = true;
                return;
            }
            
            console.log('Populating dropdown with models...');
            modelSelect.innerHTML = '<option value="">Select model...</option>';
            
            Object.entries(models).forEach(([displayName, modelId]) => {
                const option = document.createElement('option');
                option.value = modelId;
                option.textContent = displayName;
                modelSelect.appendChild(option);
            });
            
            modelSelect.disabled = false;
            console.log('Dropdown enabled with', Object.keys(models).length, 'models');
        }'''
    
    # Replace the function
    content = re.sub(pattern, simple_load_function, content, flags=re.DOTALL)
    
    # Add simple initialization after DOMContentLoaded
    init_code = '''
            console.log('Page loaded - checking dropdown states...');
            
            // Check if dropdowns exist
            const poet1Provider = document.getElementById('poet1Provider');
            const poet1Model = document.getElementById('poet1Model');
            const poet2Provider = document.getElementById('poet2Provider');
            const poet2Model = document.getElementById('poet2Model');
            
            console.log('Elements found:', {
                poet1Provider: !!poet1Provider,
                poet1Model: !!poet1Model,
                poet2Provider: !!poet2Provider,
                poet2Model: !!poet2Model
            });
            
            // Initialize model dropdowns as disabled
            if (poet1Model) {
                poet1Model.disabled = true;
                poet1Model.innerHTML = '<option value="">First select a provider...</option>';
            }
            if (poet2Model) {
                poet2Model.disabled = true;
                poet2Model.innerHTML = '<option value="">First select a provider...</option>';
            }'''
    
    # Find the end of the DOMContentLoaded listener and add our init code
    content = content.replace(
        '        });',
        init_code + '\n        });'
    )
    
    # Write the simple fixed version
    fixed_file = "poetry_generator_simple_fix.html"
    with open(fixed_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created simple fix: {fixed_file}")
    return fixed_file

def main():
    """Create a simple, working fix."""
    
    print("🔧 Creating Simple Dropdown Fix")
    print("=" * 40)
    
    fixed_file = create_simple_fixed_version()
    
    print(f"\n✅ Simple fix created: {fixed_file}")
    print(f"📍 Full path: {os.path.abspath(fixed_file)}")
    
    print(f"\n🧪 To test:")
    print(f"1. Open: file://{os.path.abspath(fixed_file)}")
    print("2. Open browser console (F12)")
    print("3. Try selecting providers for Poet 1 or 2")
    print("4. Check console for debug messages")
    print("5. Model dropdowns should now work")
    
    return fixed_file

if __name__ == "__main__":
    main()