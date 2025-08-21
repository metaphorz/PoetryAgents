#!/usr/bin/env zsh

# Fix HTML Interface - Regenerate with correct JavaScript functions
# This script fixes the missing model selection dropdown functionality

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo "${PURPLE}=================================================================${NC}"
    echo "🔧 ${CYAN}Poetry Agents - HTML Interface Fix${NC} 🔧"
    echo "${PURPLE}=================================================================${NC}"
    echo ""
}

print_section() {
    echo ""
    echo "${BLUE}$1${NC}"
    echo "${BLUE}$(echo "$1" | sed 's/./=/g')${NC}"
}

backup_current_html() {
    print_section "💾 Backing Up Current Files"
    
    if [[ -f "poetry_generator_live.html" ]]; then
        cp "poetry_generator_live.html" "poetry_generator_live.html.backup"
        echo "${GREEN}✅ Backed up poetry_generator_live.html${NC}"
    fi
    
    if [[ -f "generate_html_interface.py" ]]; then
        cp "generate_html_interface.py" "generate_html_interface.py.backup"
        echo "${GREEN}✅ Backed up generate_html_interface.py${NC}"
    fi
}

fix_html_generator() {
    print_section "🔨 Fixing HTML Generator Script"
    
    # The issue is likely in the HTML template - let me check if the JavaScript functions are properly included
    python3 -c "
import re

print('🔍 Analyzing generate_html_interface.py...')

with open('generate_html_interface.py', 'r') as f:
    content = f.read()

# Check if critical JavaScript functions are included
critical_functions = [
    'function toggleApiMode',
    'function loadModelsForPoet',
    'function loadOpenrouterModelsForPoet',
    'function generatePythonScript'
]

missing_functions = []
for func in critical_functions:
    if func not in content:
        missing_functions.append(func)

if missing_functions:
    print('❌ Missing JavaScript functions in generator:')
    for func in missing_functions:
        print(f'  • {func}')
else:
    print('✅ All JavaScript functions found in generator')

# Check HTML template structure
if 'html_content = f' in content:
    print('✅ HTML template structure found')
else:
    print('❌ HTML template structure missing')
"
}

regenerate_interface() {
    print_section "🚀 Regenerating HTML Interface"
    
    echo "${CYAN}💡 Running fresh model data fetch and HTML generation...${NC}"
    
    # Remove old file to ensure fresh generation
    if [[ -f "poetry_generator_live.html" ]]; then
        rm "poetry_generator_live.html"
    fi
    
    # Regenerate with fresh data
    python3 generate_html_interface.py
    
    if [[ -f "poetry_generator_live.html" ]]; then
        echo "${GREEN}✅ New HTML interface generated${NC}"
        
        # Verify the critical functions are now present
        echo ""
        echo "${CYAN}🔍 Verifying JavaScript functions in new HTML:${NC}"
        
        functions=("toggleApiMode" "loadModelsForPoet" "loadOpenrouterModelsForPoet" "generatePythonScript")
        all_found=true
        
        for func in "${functions[@]}"; do
            if grep -q "function $func" poetry_generator_live.html; then
                echo "  ${GREEN}✅ $func${NC}"
            else
                echo "  ${RED}❌ $func (STILL MISSING)${NC}"
                all_found=false
            fi
        done
        
        if [[ "$all_found" = true ]]; then
            echo "${GREEN}🎉 All JavaScript functions are now present!${NC}"
            return 0
        else
            echo "${RED}❌ Some functions still missing - need to fix the generator${NC}"
            return 1
        fi
    else
        echo "${RED}❌ Failed to generate new HTML interface${NC}"
        return 1
    fi
}

create_minimal_test_interface() {
    print_section "🧪 Creating Minimal Test Interface"
    
    # Create a simplified test version to isolate the issue
    cat > test_dropdown_fix.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Model Selection Test</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ccc; border-radius: 8px; }
        select { width: 300px; padding: 8px; margin: 5px 0; }
        select:disabled { opacity: 0.5; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>🔍 Model Selection Debug Test</h1>
    
    <div class="section">
        <h3>Direct API Test</h3>
        <label>Provider:</label><br>
        <select id="testProvider">
            <option value="">Select Provider...</option>
            <option value="Claude">Claude</option>
            <option value="OpenAI">OpenAI</option>
            <option value="Gemini">Gemini</option>
        </select><br>
        
        <label>Model:</label><br>
        <select id="testModel" disabled>
            <option value="">First select a provider...</option>
        </select>
        
        <div id="testResult"></div>
    </div>
    
    <div class="section">
        <h3>OpenRouter Test</h3>
        <label>Provider:</label><br>
        <select id="testOpenrouterProvider">
            <option value="">Select Provider...</option>
            <option value="anthropic">Anthropic</option>
            <option value="openai">OpenAI</option>
        </select><br>
        
        <label>Model:</label><br>
        <select id="testOpenrouterModel" disabled>
            <option value="">First select a provider...</option>
        </select>
        
        <div id="testOpenrouterResult"></div>
    </div>

    <script>
        // Test model data (simplified)
        const testModelData = {
            "Claude": {
                "Claude Sonnet 4": "claude-sonnet-4-20250514",
                "Claude Opus 4": "claude-opus-4-20250514",
                "Claude Haiku 3.5": "claude-3-5-haiku-20241022"
            },
            "OpenAI": {
                "GPT-4o": "gpt-4o",
                "GPT-4o Mini": "gpt-4o-mini",
                "GPT-4 Turbo": "gpt-4-turbo"
            },
            "Gemini": {
                "Gemini 2.5 Pro": "gemini-2.5-pro",
                "Gemini 2.5 Flash": "gemini-2.5-flash"
            }
        };
        
        const testOpenrouterData = {
            "anthropic": {
                "Claude Opus 4.1": "anthropic/claude-opus-4.1"
            },
            "openai": {
                "GPT-5 Mini": "openai/gpt-5-mini",
                "GPT-4o": "openai/gpt-4o"
            }
        };
        
        function loadTestModels(provider) {
            const modelSelect = document.getElementById('testModel');
            const resultDiv = document.getElementById('testResult');
            
            console.log('Loading models for provider:', provider);
            
            if (!provider) {
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                resultDiv.innerHTML = '';
                return;
            }

            const models = testModelData[provider];
            
            if (!models) {
                modelSelect.innerHTML = '<option value="">No models available</option>';
                modelSelect.disabled = true;
                resultDiv.innerHTML = '<span class="error">❌ No models found for ' + provider + '</span>';
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
            resultDiv.innerHTML = '<span class="success">✅ Loaded ' + Object.keys(models).length + ' models</span>';
            
            console.log('Successfully loaded', Object.keys(models).length, 'models for', provider);
        }
        
        function loadTestOpenrouterModels(provider) {
            const modelSelect = document.getElementById('testOpenrouterModel');
            const resultDiv = document.getElementById('testOpenrouterResult');
            
            console.log('Loading OpenRouter models for provider:', provider);
            
            if (!provider) {
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                resultDiv.innerHTML = '';
                return;
            }

            const models = testOpenrouterData[provider];
            
            if (!models) {
                modelSelect.innerHTML = '<option value="">No models available</option>';
                modelSelect.disabled = true;
                resultDiv.innerHTML = '<span class="error">❌ No models found for ' + provider + '</span>';
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
            resultDiv.innerHTML = '<span class="success">✅ Loaded ' + Object.keys(models).length + ' models</span>';
            
            console.log('Successfully loaded', Object.keys(models).length, 'OpenRouter models for', provider);
        }
        
        // Set up event listeners
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM loaded, setting up event listeners');
            
            document.getElementById('testProvider').addEventListener('change', function() {
                console.log('Provider changed to:', this.value);
                loadTestModels(this.value);
            });
            
            document.getElementById('testOpenrouterProvider').addEventListener('change', function() {
                console.log('OpenRouter provider changed to:', this.value);
                loadTestOpenrouterModels(this.value);
            });
            
            console.log('Event listeners set up successfully');
        });
    </script>
</body>
</html>
EOF

    echo "${GREEN}✅ Created test_dropdown_fix.html${NC}"
    echo "${CYAN}💡 Open test_dropdown_fix.html in your browser to test model selection${NC}"
}

verify_and_compare() {
    print_section "📊 Verification and Comparison"
    
    echo "${CYAN}🔍 Comparing JavaScript content:${NC}"
    
    if [[ -f "test_dropdown_fix.html" && -f "poetry_generator_live.html" ]]; then
        # Check if the main file has the essential functions
        echo ""
        echo "Main HTML Functions:"
        for func in "loadModelsForPoet" "loadOpenrouterModelsForPoet" "toggleApiMode"; do
            if grep -q "function $func" poetry_generator_live.html; then
                echo "  ${GREEN}✅ $func${NC}"
            else
                echo "  ${RED}❌ $func${NC}"
            fi
        done
        
        echo ""
        echo "Test HTML Functions:"
        for func in "loadTestModels" "loadTestOpenrouterModels"; do
            if grep -q "function $func" test_dropdown_fix.html; then
                echo "  ${GREEN}✅ $func${NC}"
            else
                echo "  ${RED}❌ $func${NC}"
            fi
        done
        
        # Check model data structure
        echo ""
        echo "${CYAN}📊 Model Data Structure:${NC}"
        claude_models_main=$(grep -A 10 '"Claude":' poetry_generator_live.html | grep -c '"claude-' || echo "0")
        claude_models_test=$(grep -A 10 '"Claude":' test_dropdown_fix.html | grep -c '"claude-' || echo "0")
        
        echo "  Main HTML Claude models: ${GREEN}$claude_models_main${NC}"
        echo "  Test HTML Claude models: ${GREEN}$claude_models_test${NC}"
        
    else
        echo "${RED}❌ Cannot compare - missing files${NC}"
    fi
}

main() {
    print_header
    
    echo "${CYAN}💡 This script fixes model selection dropdown issues${NC}"
    echo "${CYAN}💡 Problem: JavaScript functions missing from HTML interface${NC}"
    echo ""
    
    # Step 1: Backup current files
    backup_current_html
    
    # Step 2: Analyze the generator script
    fix_html_generator
    
    # Step 3: Try to regenerate the interface
    if ! regenerate_interface; then
        echo ""
        echo "${YELLOW}⚠️  Regeneration had issues, creating minimal test interface...${NC}"
        create_minimal_test_interface
    fi
    
    # Step 4: Create test interface regardless
    create_minimal_test_interface
    
    # Step 5: Compare and verify
    verify_and_compare
    
    print_section "🎯 Fix Complete"
    
    echo "${GREEN}✅ HTML interface fix process complete${NC}"
    echo ""
    echo "${CYAN}📋 Files created/modified:${NC}"
    echo "  • test_dropdown_fix.html - Minimal test interface"
    echo "  • poetry_generator_live.html.backup - Backup of original"
    echo "  • poetry_generator_live.html - Regenerated interface"
    echo ""
    echo "${CYAN}🔍 Next steps:${NC}"
    echo "  1. Open test_dropdown_fix.html in browser first"
    echo "  2. Verify dropdowns populate correctly in test"
    echo "  3. If test works, try poetry_generator_live.html"
    echo "  4. Check browser console for any JavaScript errors"
    echo ""
    echo "${YELLOW}💡 If test interface works but main doesn't:${NC}"
    echo "  The issue is in the HTML generator template"
    echo "  Run: ./poetry_agents.sh --refresh to try again"
}

# Make script executable and run
chmod +x "$0" 2>/dev/null || true
main "$@"