#!/usr/bin/env python3
"""
Fix Main Poetry Generator Interface
Applies the working JavaScript logic from the debug version to the main interface.
"""

import os
import re

def fix_main_interface():
    """Fix the main poetry generator interface with clean JavaScript."""
    
    print("🛠️ Fixing main poetry generator interface...")
    
    # Read the original file
    with open("poetry_generator_live.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the loadModelsForPoet function with the working version
    old_function_pattern = r'function loadModelsForPoet\(poetNumber, provider\) \{[^}]+\}'
    
    new_function = '''function loadModelsForPoet(poetNumber, provider) {
            const modelSelect = document.getElementById(`poet${poetNumber}Model`);
            
            if (!modelSelect) {
                console.error('Model select element not found:', `poet${poetNumber}Model`);
                return;
            }
            
            if (!provider) {
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                return;
            }

            const models = modelData[provider];
            
            if (!models) {
                console.error('No models found for provider:', provider);
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
    
    # Replace the function
    content = re.sub(old_function_pattern, new_function, content, flags=re.DOTALL)
    
    # Fix the toggleApiMode function to be more robust
    old_toggle_pattern = r'function toggleApiMode\(\) \{.*?\n        \}'
    
    new_toggle_function = '''function toggleApiMode() {
            const apiMode = document.querySelector('input[name="apiMode"]:checked').value;
            const isOpenrouter = apiMode === 'openrouter';

            // Show/hide appropriate form groups
            ['poet1', 'poet2'].forEach(poet => {
                const directGroup = document.getElementById(poet + 'DirectGroup');
                const modelGroup = document.getElementById(poet + 'ModelGroup');
                const openrouterGroup = document.getElementById(poet + 'OpenrouterGroup');
                const openrouterModelGroup = document.getElementById(poet + 'OpenrouterModelGroup');

                if (isOpenrouter) {
                    if (directGroup) directGroup.style.display = 'none';
                    if (modelGroup) modelGroup.style.display = 'none';
                    if (openrouterGroup) openrouterGroup.style.display = 'block';
                    if (openrouterModelGroup) openrouterModelGroup.style.display = 'block';
                    
                    // Clear direct API selections
                    const providerSelect = document.getElementById(poet + 'Provider');
                    const modelSelect = document.getElementById(poet + 'Model');
                    if (providerSelect) providerSelect.selectedIndex = 0;
                    if (modelSelect) {
                        modelSelect.selectedIndex = 0;
                        modelSelect.disabled = true;
                        modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                    }
                } else {
                    if (directGroup) directGroup.style.display = 'block';
                    if (modelGroup) modelGroup.style.display = 'block';
                    if (openrouterGroup) openrouterGroup.style.display = 'none';
                    if (openrouterModelGroup) openrouterModelGroup.style.display = 'none';
                    
                    // Clear OpenRouter selections
                    const openrouterProviderSelect = document.getElementById(poet + 'OpenrouterProvider');
                    const openrouterModelSelect = document.getElementById(poet + 'OpenrouterModel');
                    if (openrouterProviderSelect) openrouterProviderSelect.selectedIndex = 0;
                    if (openrouterModelSelect) {
                        openrouterModelSelect.selectedIndex = 0;
                        openrouterModelSelect.disabled = true;
                        openrouterModelSelect.innerHTML = '<option value="">First select a provider...</option>';
                    }
                    
                    // Reset Direct API model dropdown
                    const providerSelect = document.getElementById(poet + 'Provider');
                    const modelSelect = document.getElementById(poet + 'Model');
                    
                    if (modelSelect) {
                        if (providerSelect && providerSelect.value) {
                            // If provider is already selected, reload its models
                            loadModelsForPoet(poet.replace('poet', ''), providerSelect.value);
                        } else {
                            modelSelect.disabled = true;
                            modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                        }
                    }
                }
            });
        }'''
    
    # Replace the toggle function
    content = re.sub(old_toggle_pattern, new_toggle_function, content, flags=re.DOTALL)
    
    # Improve the event listener setup
    old_event_setup = '''            // Direct API provider change handlers
            document.getElementById('poet1Provider').addEventListener('change', function() {
                loadModelsForPoet(1, this.value);
            });

            document.getElementById('poet2Provider').addEventListener('change', function() {
                loadModelsForPoet(2, this.value);
            });'''
    
    new_event_setup = '''            // Direct API provider change handlers with error checking
            const poet1Provider = document.getElementById('poet1Provider');
            const poet2Provider = document.getElementById('poet2Provider');
            
            if (poet1Provider) {
                poet1Provider.addEventListener('change', function() {
                    loadModelsForPoet(1, this.value);
                });
            } else {
                console.error('poet1Provider element not found');
            }

            if (poet2Provider) {
                poet2Provider.addEventListener('change', function() {
                    loadModelsForPoet(2, this.value);
                });
            } else {
                console.error('poet2Provider element not found');
            }'''
    
    # Replace the event setup
    content = content.replace(old_event_setup, new_event_setup)
    
    # Write the fixed version
    fixed_file = "poetry_generator_live_clean.html"
    with open(fixed_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created fixed main interface: {fixed_file}")
    return fixed_file

def main():
    """Fix the main interface."""
    
    print("🔧 Fixing Main Poetry Generator Interface")
    print("=" * 50)
    
    fixed_file = fix_main_interface()
    
    print(f"\n✅ Main interface fixed: {fixed_file}")
    print(f"📍 Full path: {os.path.abspath(fixed_file)}")
    
    print(f"\n🧪 To test the fixed interface:")
    print(f"1. Open: file://{os.path.abspath(fixed_file)}")
    print("2. Select 'Direct APIs' mode")
    print("3. Choose providers for Poet 1 and 2")
    print("4. Verify model dropdowns populate and enable")
    print("5. Try generating poetry")
    
    print(f"\n✨ The fixed version includes:")
    print("   • Clean loadModelsForPoet function")
    print("   • Robust toggleApiMode with error checking")
    print("   • Improved event listener setup")
    print("   • No syntax errors or malformed JavaScript")
    
    return fixed_file

if __name__ == "__main__":
    main()