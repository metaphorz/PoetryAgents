#!/usr/bin/env python3
"""
Fix Web Interface Dropdown Issue
Identifies and fixes the problem where model dropdowns are greyed out.
"""

import os
import sys
from datetime import datetime

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def analyze_issue():
    """Analyze the dropdown issue in the main HTML file."""
    
    print("🔍 Analyzing the dropdown issue...")
    
    # Read the main HTML file
    main_html_file = "poetry_generator_live.html"
    
    with open(main_html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues_found = []
    
    # Check for common issues
    if 'modelSelect.disabled = true' in content:
        issues_found.append("Found disabled statements in JavaScript")
    
    if 'toggleApiMode()' in content:
        issues_found.append("Found toggleApiMode function that may interfere")
    
    if 'addEventListener' in content:
        issues_found.append("Found event listeners - check if they're set up correctly")
    
    print(f"📊 Issues found: {len(issues_found)}")
    for issue in issues_found:
        print(f"   ⚠️ {issue}")
    
    return issues_found

def create_fixed_html():
    """Create a fixed version of the HTML with improved dropdown functionality."""
    
    print("🛠️ Creating fixed version of the HTML...")
    
    # Read the original file
    with open("poetry_generator_live.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Improve the toggleApiMode function
    old_toggle_function = '''        function toggleApiMode() {
            const apiMode = document.querySelector('input[name="apiMode"]:checked').value;
            const isOpenrouter = apiMode === 'openrouter';

            // Show/hide appropriate form groups
            ['poet1', 'poet2'].forEach(poet => {
                const directGroup = document.getElementById(poet + 'DirectGroup');
                const modelGroup = document.getElementById(poet + 'ModelGroup');
                const openrouterGroup = document.getElementById(poet + 'OpenrouterGroup');
                const openrouterModelGroup = document.getElementById(poet + 'OpenrouterModelGroup');

                if (isOpenrouter) {
                    directGroup.style.display = 'none';
                    modelGroup.style.display = 'none';
                    openrouterGroup.style.display = 'block';
                    openrouterModelGroup.style.display = 'block';
                    
                    // Clear direct API selections
                    document.getElementById(poet + 'Provider').selectedIndex = 0;
                    document.getElementById(poet + 'Model').selectedIndex = 0;
                    document.getElementById(poet + 'Model').disabled = true;
                } else {
                    directGroup.style.display = 'block';
                    modelGroup.style.display = 'block';
                    openrouterGroup.style.display = 'none';
                    openrouterModelGroup.style.display = 'none';
                    
                    // Clear OpenRouter selections
                    document.getElementById(poet + 'OpenrouterProvider').selectedIndex = 0;
                    document.getElementById(poet + 'OpenrouterModel').selectedIndex = 0;
                    document.getElementById(poet + 'OpenrouterModel').disabled = true;
                }
            });
        }'''
    
    new_toggle_function = '''        function toggleApiMode() {
            const apiMode = document.querySelector('input[name="apiMode"]:checked').value;
            const isOpenrouter = apiMode === 'openrouter';

            console.log('🔄 Toggling API mode to:', apiMode);

            // Show/hide appropriate form groups
            ['poet1', 'poet2'].forEach(poet => {
                const directGroup = document.getElementById(poet + 'DirectGroup');
                const modelGroup = document.getElementById(poet + 'ModelGroup');
                const openrouterGroup = document.getElementById(poet + 'OpenrouterGroup');
                const openrouterModelGroup = document.getElementById(poet + 'OpenrouterModelGroup');

                if (isOpenrouter) {
                    console.log(`📱 Showing OpenRouter mode for ${poet}`);
                    directGroup.style.display = 'none';
                    modelGroup.style.display = 'none';
                    openrouterGroup.style.display = 'block';
                    openrouterModelGroup.style.display = 'block';
                    
                    // Clear direct API selections
                    const providerSelect = document.getElementById(poet + 'Provider');
                    const modelSelect = document.getElementById(poet + 'Model');
                    providerSelect.selectedIndex = 0;
                    modelSelect.selectedIndex = 0;
                    modelSelect.disabled = true;
                    modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                } else {
                    console.log(`🖥️ Showing Direct API mode for ${poet}`);
                    directGroup.style.display = 'block';
                    modelGroup.style.display = 'block';
                    openrouterGroup.style.display = 'none';
                    openrouterModelGroup.style.display = 'none';
                    
                    // Clear OpenRouter selections
                    const openrouterProviderSelect = document.getElementById(poet + 'OpenrouterProvider');
                    const openrouterModelSelect = document.getElementById(poet + 'OpenrouterModel');
                    openrouterProviderSelect.selectedIndex = 0;
                    openrouterModelSelect.selectedIndex = 0;
                    openrouterModelSelect.disabled = true;
                    openrouterModelSelect.innerHTML = '<option value="">First select a provider...</option>';
                    
                    // Reset Direct API model dropdown to proper state
                    const providerSelect = document.getElementById(poet + 'Provider');
                    const modelSelect = document.getElementById(poet + 'Model');
                    
                    // If provider is already selected, reload its models
                    if (providerSelect.value) {
                        console.log(`🔄 Reloading models for ${poet} provider: ${providerSelect.value}`);
                        loadModelsForPoet(poet.replace('poet', ''), providerSelect.value);
                    } else {
                        modelSelect.disabled = true;
                        modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                    }
                }
            });
        }'''
    
    # Replace the function
    content = content.replace(old_toggle_function, new_toggle_function)
    
    # Fix 2: Improve the loadModelsForPoet function with better debugging
    old_load_function = '''        function loadModelsForPoet(poetNumber, provider) {
            const modelSelect = document.getElementById(`poet${poetNumber}Model`);
            
            if (!provider) {
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                return;
            }

            const models = modelData[provider];
            
            if (!models) {
                modelSelect.innerHTML = '<option value="">No models available</option>';
                modelSelect.disabled = true;
                return;
            }
            
            modelSelect.innerHTML = '<option value="">Select model...</option>';
            
            Object.entries(models).forEach(([displayName, modelId]) => {
                const option = document.createElement('option');
                option.value = modelId;
                option.textContent = displayName;
                modelSelect.appendChild(option);
            });
            
            modelSelect.disabled = false;
        }'''
    
    new_load_function = '''        function loadModelsForPoet(poetNumber, provider) {
            console.log(`📋 Loading models for Poet ${poetNumber}, Provider: "${provider}"`);
            
            const modelSelect = document.getElementById(`poet${poetNumber}Model`);
            
            if (!modelSelect) {
                console.error(`❌ Model select element not found: poet${poetNumber}Model`);
                return;
            }
            
            console.log(`✅ Found model select element: poet${poetNumber}Model`);
            
            if (!provider) {
                console.log('ℹ️ No provider selected - disabling model dropdown');
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                return;
            }

            console.log(`🔍 Looking for models for provider: "${provider}"`);
            console.log(`📊 Available providers: ${Object.keys(modelData).join(', ')}`);
            
            const models = modelData[provider];
            
            if (!models) {
                console.error(`❌ No models found for provider: ${provider}`);
                modelSelect.innerHTML = '<option value="">No models available</option>';
                modelSelect.disabled = true;
                return;
            }
            
            console.log(`✅ Found ${Object.keys(models).length} models for ${provider}`);
            
            // Clear and populate dropdown
            modelSelect.innerHTML = '<option value="">Select model...</option>';
            
            let addedModels = 0;
            Object.entries(models).forEach(([displayName, modelId]) => {
                console.log(`➕ Adding model: "${displayName}" → "${modelId}"`);
                const option = document.createElement('option');
                option.value = modelId;
                option.textContent = displayName;
                modelSelect.appendChild(option);
                addedModels++;
            });
            
            // Enable the dropdown
            modelSelect.disabled = false;
            console.log(`🎉 Successfully enabled dropdown with ${addedModels} models`);
            
            // Verify it's actually enabled
            setTimeout(() => {
                if (modelSelect.disabled) {
                    console.error('⚠️ WARNING: Dropdown is still disabled after enabling!');
                } else {
                    console.log('✅ Dropdown is properly enabled');
                }
            }, 100);
        }'''
    
    # Replace the function
    content = content.replace(old_load_function, new_load_function)
    
    # Fix 3: Add debugging to the event listeners
    old_event_setup = '''            document.getElementById('poet1Provider').addEventListener('change', function() {
                loadModelsForPoet(1, this.value);
            });

            document.getElementById('poet2Provider').addEventListener('change', function() {
                loadModelsForPoet(2, this.value);
            });'''
    
    new_event_setup = '''            // Provider change event listeners with debugging
            const poet1Provider = document.getElementById('poet1Provider');
            const poet2Provider = document.getElementById('poet2Provider');
            
            if (poet1Provider) {
                poet1Provider.addEventListener('change', function() {
                    console.log(`🔄 Poet 1 provider changed to: "${this.value}"`);
                    loadModelsForPoet(1, this.value);
                });
                console.log('✅ Poet 1 provider event listener set up');
            } else {
                console.error('❌ Poet 1 provider element not found');
            }

            if (poet2Provider) {
                poet2Provider.addEventListener('change', function() {
                    console.log(`🔄 Poet 2 provider changed to: "${this.value}"`);
                    loadModelsForPoet(2, this.value);
                });
                console.log('✅ Poet 2 provider event listener set up');
            } else {
                console.error('❌ Poet 2 provider element not found');
            }'''
    
    # Replace the event setup
    content = content.replace(old_event_setup, new_event_setup)
    
    # Fix 4: Add initialization check on page load
    init_check = '''
            // Initialize dropdowns on page load
            console.log('🚀 Initializing dropdowns on page load...');
            
            ['poet1', 'poet2'].forEach(poet => {
                const providerSelect = document.getElementById(poet + 'Provider');
                const modelSelect = document.getElementById(poet + 'Model');
                
                if (providerSelect && modelSelect) {
                    console.log(`✅ Found elements for ${poet}`);
                    // Ensure model dropdown starts disabled
                    modelSelect.disabled = true;
                    modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                } else {
                    console.error(`❌ Missing elements for ${poet}: provider=${!!providerSelect}, model=${!!modelSelect}`);
                }
            });
            
            // Set initial API mode
            const initialApiMode = document.querySelector('input[name="apiMode"]:checked');
            if (initialApiMode) {
                console.log(`📱 Initial API mode: ${initialApiMode.value}`);
                toggleApiMode();
            } else {
                console.log('📱 No initial API mode selected, defaulting to direct');
            }'''
    
    # Add the initialization check before the closing of the DOMContentLoaded event
    content = content.replace('        });', init_check + '\n        });')
    
    # Write the fixed version
    fixed_file = "poetry_generator_live_fixed.html"
    with open(fixed_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created fixed version: {fixed_file}")
    return fixed_file

def main():
    """Main function to analyze and fix the dropdown issue."""
    
    print("🛠️ Web Interface Dropdown Fix")
    print("=" * 50)
    
    # Analyze the issue
    issues = analyze_issue()
    
    if issues:
        print(f"\n🔧 Creating fixes for {len(issues)} identified issues...")
        
        # Create fixed version
        fixed_file = create_fixed_html()
        
        print(f"\n✅ Fixed version created: {fixed_file}")
        print(f"📍 Full path: {os.path.abspath(fixed_file)}")
        
        print("\n📋 Fixes applied:")
        print("   1. Enhanced toggleApiMode with better state management")
        print("   2. Added extensive debugging to loadModelsForPoet function")
        print("   3. Improved event listener setup with error checking")
        print("   4. Added proper initialization on page load")
        
        print(f"\n🧪 To test the fix:")
        print(f"1. Open the fixed file in your browser:")
        print(f"   file://{os.path.abspath(fixed_file)}")
        print("2. Open browser console (F12) to see debug messages")
        print("3. Try selecting providers and watch the console output")
        print("4. The dropdowns should now work properly")
        
        return fixed_file
    else:
        print("ℹ️ No obvious issues found in the HTML structure")
        return None

if __name__ == "__main__":
    main()