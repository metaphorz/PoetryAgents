#!/usr/bin/env zsh

# Debug Models - Investigate model selection issues
# This script diagnoses why model dropdowns aren't populated correctly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo "${PURPLE}=================================================================${NC}"
    echo "🔍 ${CYAN}Poetry Agents - Model Selection Debug Tool${NC} 🔍"
    echo "${PURPLE}=================================================================${NC}"
    echo ""
}

print_section() {
    echo ""
    echo "${BLUE}$1${NC}"
    echo "${BLUE}$(echo "$1" | sed 's/./=/g')${NC}"
}

debug_html_model_data() {
    print_section "🌐 Analyzing HTML Model Data"
    
    if [[ ! -f "poetry_generator_live.html" ]]; then
        echo "${RED}❌ poetry_generator_live.html not found!${NC}"
        echo "${CYAN}💡 Run: ./poetry_agents.sh --refresh${NC}"
        return 1
    fi
    
    echo "${GREEN}✅ HTML file found${NC}"
    
    # Extract and analyze modelData
    echo ""
    echo "${CYAN}📊 Direct API Model Data:${NC}"
    grep -A 50 "const modelData =" poetry_generator_live.html | grep -E "\"[^\"]*\":\s*{" | while read line; do
        provider=$(echo "$line" | sed -E 's/.*"([^"]*)":.*/\1/')
        echo "  📦 Provider: ${YELLOW}$provider${NC}"
    done
    
    # Count models per provider
    echo ""
    echo "${CYAN}🔢 Model Counts per Provider:${NC}"
    for provider in "Claude" "Gemini" "OpenAI"; do
        count=$(grep -A 100 "\"$provider\":" poetry_generator_live.html | grep -E "\"[^\"]*\":\s*\"[^\"]*\"" | wc -l | tr -d ' ')
        echo "  $provider: ${GREEN}$count models${NC}"
    done
    
    # Extract and analyze OpenRouter data
    echo ""
    echo "${CYAN}📊 OpenRouter Model Data:${NC}"
    grep -A 50 "const openrouterModelData =" poetry_generator_live.html | grep -E "\"[^\"]*\":\s*{" | while read line; do
        provider=$(echo "$line" | sed -E 's/.*"([^"]*)":.*/\1/')
        echo "  🌍 OpenRouter Provider: ${YELLOW}$provider${NC}"
    done
    
    # Count OpenRouter models per provider
    echo ""
    echo "${CYAN}🔢 OpenRouter Model Counts:${NC}"
    for provider in "anthropic" "openai" "google" "meta-llama" "mistralai" "qwen"; do
        # Look for the provider section and count models in it
        count=$(awk "/\"$provider\": {/,/}/" poetry_generator_live.html | grep -E "\"[^\"]*\":\s*\"[^\"]*\"" | wc -l | tr -d ' ')
        if [[ $count -gt 0 ]]; then
            echo "  $provider: ${GREEN}$count models${NC}"
        fi
    done
}

debug_javascript_functions() {
    print_section "⚙️ Analyzing JavaScript Functions"
    
    # Check if key functions exist
    functions=("toggleApiMode" "loadModelsForPoet" "loadOpenrouterModelsForPoet" "generatePythonScript")
    
    for func in "${functions[@]}"; do
        if grep -q "function $func" poetry_generator_live.html; then
            echo "${GREEN}✅ Function found: $func${NC}"
        else
            echo "${RED}❌ Missing function: $func${NC}"
        fi
    done
    
    # Check for event listeners
    echo ""
    echo "${CYAN}🎧 Event Listeners:${NC}"
    if grep -q "addEventListener('change', function()" poetry_generator_live.html; then
        echo "${GREEN}✅ Provider change listeners found${NC}"
    else
        echo "${RED}❌ Provider change listeners missing${NC}"
    fi
    
    if grep -q "DOMContentLoaded" poetry_generator_live.html; then
        echo "${GREEN}✅ DOMContentLoaded listener found${NC}"
    else
        echo "${RED}❌ DOMContentLoaded listener missing${NC}"
    fi
}

debug_html_structure() {
    print_section "🏗️ Analyzing HTML Structure"
    
    # Check for required form elements
    elements=(
        "poet1Provider"
        "poet1Model" 
        "poet2Provider"
        "poet2Model"
        "poet1OpenrouterProvider"
        "poet1OpenrouterModel"
        "poet2OpenrouterProvider"
        "poet2OpenrouterModel"
    )
    
    for element in "${elements[@]}"; do
        if grep -q "id=\"$element\"" poetry_generator_live.html; then
            echo "${GREEN}✅ Element found: $element${NC}"
        else
            echo "${RED}❌ Missing element: $element${NC}"
        fi
    done
    
    # Check for proper select options structure
    echo ""
    echo "${CYAN}🔍 Dropdown Structure:${NC}"
    direct_options=$(grep -c "Select Provider..." poetry_generator_live.html)
    echo "  Direct API dropdowns: ${GREEN}$direct_options${NC}"
    
    openrouter_options=$(grep -c "value=\"anthropic\"" poetry_generator_live.html)
    echo "  OpenRouter provider options: ${GREEN}$openrouter_options${NC}"
}

test_model_loading_logic() {
    print_section "🧪 Testing Model Loading Logic"
    
    # Create a simple test HTML to verify the logic
    cat > test_model_loading.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Model Loading Test</title></head>
<body>
    <select id="testProvider">
        <option value="">Select Provider...</option>
        <option value="Claude">Claude</option>
        <option value="OpenAI">OpenAI</option>
    </select>
    <select id="testModel" disabled>
        <option value="">First select a provider...</option>
    </select>
    
    <script>
        // Extract model data from main HTML file
EOF
    
    # Extract just the modelData from the main file
    grep -A 100 "const modelData =" poetry_generator_live.html | sed '/const openrouterModelData/,$d' >> test_model_loading.html
    
    cat >> test_model_loading.html << 'EOF'
        
        function loadTestModels(provider) {
            const modelSelect = document.getElementById('testModel');
            
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
            console.log(`Loaded ${Object.keys(models).length} models for ${provider}`);
        }
        
        document.getElementById('testProvider').addEventListener('change', function() {
            loadTestModels(this.value);
        });
        
        // Auto-test
        setTimeout(() => {
            console.log('Testing Claude models...');
            loadTestModels('Claude');
            console.log('Claude model count:', document.getElementById('testModel').options.length - 1);
            
            console.log('Testing OpenAI models...');  
            loadTestModels('OpenAI');
            console.log('OpenAI model count:', document.getElementById('testModel').options.length - 1);
        }, 100);
    </script>
</body>
</html>
EOF

    echo "${GREEN}✅ Created test_model_loading.html${NC}"
    echo "${CYAN}💡 Open test_model_loading.html in browser and check console for model loading test results${NC}"
}

show_raw_model_data() {
    print_section "📋 Raw Model Data Extracted"
    
    echo "${CYAN}🤖 Claude Models:${NC}"
    grep -A 20 '"Claude":' poetry_generator_live.html | grep -E "\"[^\"]*\":\s*\"claude-[^\"]*\"" | while read line; do
        model=$(echo "$line" | sed -E 's/.*"([^"]*)":\s*"([^"]*)".*/ \1 → \2/')
        echo "  ${GREEN}$model${NC}"
    done
    
    echo ""
    echo "${CYAN}🤖 OpenAI Models:${NC}"
    grep -A 20 '"OpenAI":' poetry_generator_live.html | grep -E "\"[^\"]*\":\s*\"gpt-[^\"]*\"" | while read line; do
        model=$(echo "$line" | sed -E 's/.*"([^"]*)":\s*"([^"]*)".*/ \1 → \2/')
        echo "  ${GREEN}$model${NC}"
    done
    
    echo ""
    echo "${CYAN}🤖 Gemini Models:${NC}"
    grep -A 20 '"Gemini":' poetry_generator_live.html | grep -E "\"[^\"]*\":\s*\"gemini-[^\"]*\"" | while read line; do
        model=$(echo "$line" | sed -E 's/.*"([^"]*)":\s*"([^"]*)".*/ \1 → \2/')
        echo "  ${GREEN}$model${NC}"
    done
    
    echo ""
    echo "${CYAN}🌍 OpenRouter - Anthropic Models:${NC}"
    awk '/\"anthropic\": {/,/}/' poetry_generator_live.html | grep -E "\"[^\"]*\":\s*\"anthropic\/[^\"]*\"" | while read line; do
        model=$(echo "$line" | sed -E 's/.*"([^"]*)":\s*"([^"]*)".*/ \1 → \2/')
        echo "  ${GREEN}$model${NC}"
    done
    
    echo ""
    echo "${CYAN}🌍 OpenRouter - OpenAI Models:${NC}"
    awk '/\"openai\": {/,/}/' poetry_generator_live.html | grep -E "\"[^\"]*\":\s*\"openai\/[^\"]*\"" | while read line; do
        model=$(echo "$line" | sed -E 's/.*"([^"]*)":\s*"([^"]*)".*/ \1 → \2/')
        echo "  ${GREEN}$model${NC}"
    done
}

generate_fix_script() {
    print_section "🔧 Generating Model Selection Fix"
    
    cat > fix_model_selection.py << 'EOF'
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
EOF

    chmod +x fix_model_selection.py
    echo "${GREEN}✅ Created fix_model_selection.py${NC}"
    echo "${CYAN}💡 Run: python3 fix_model_selection.py${NC}"
}

main() {
    print_header
    
    echo "${CYAN}💡 This script analyzes why model dropdowns aren't populated correctly${NC}"
    echo ""
    
    debug_html_model_data
    debug_javascript_functions
    debug_html_structure
    test_model_loading_logic
    show_raw_model_data
    generate_fix_script
    
    print_section "🎯 Diagnosis Complete"
    
    echo "${GREEN}✅ Debug analysis complete${NC}"
    echo ""
    echo "${CYAN}📋 Files created:${NC}"
    echo "  • test_model_loading.html - Test model loading in isolation"
    echo "  • fix_model_selection.py - Advanced diagnostic tool"
    echo ""
    echo "${CYAN}🔍 Recommended next steps:${NC}"
    echo "  1. Open test_model_loading.html in browser and check console"
    echo "  2. Run: python3 fix_model_selection.py"
    echo "  3. Check browser console on main interface for errors"
    echo "  4. Try: ./poetry_agents.sh --refresh to regenerate interface"
    
    echo ""
    echo "${YELLOW}🤔 Common causes of missing models:${NC}"
    echo "  • JavaScript errors preventing dropdown population"
    echo "  • Event listeners not firing on provider selection"  
    echo "  • Model data not properly embedded in HTML"
    echo "  • Browser caching old version of interface"
}

# Make script executable and run
chmod +x "$0" 2>/dev/null || true
main "$@"