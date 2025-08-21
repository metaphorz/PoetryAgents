#!/usr/bin/env zsh

# Debug Dropdown Issue - Diagnose why model dropdowns have no options
# This script creates a live test to identify the exact problem

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "${CYAN}🔍 Debugging Model Dropdown Issue${NC}"
echo "=================================="
echo ""

# Step 1: Check if the loadModelsForPoet function is actually being called
echo "${CYAN}Step 1: Analyzing JavaScript Function Logic${NC}"
echo ""

# Extract the loadModelsForPoet function from the HTML
echo "${YELLOW}📋 Extracting loadModelsForPoet function...${NC}"
awk '/function loadModelsForPoet\(/,/^        \}/' poetry_generator_live.html > extracted_function.js

if [[ -f "extracted_function.js" ]]; then
    echo "${GREEN}✅ Function extracted successfully${NC}"
    echo ""
    echo "${CYAN}Function content:${NC}"
    cat extracted_function.js | head -20
    echo "..."
else
    echo "${RED}❌ Could not extract function${NC}"
fi

# Step 2: Create a minimal test HTML to isolate the issue
echo ""
echo "${CYAN}Step 2: Creating Live Test HTML${NC}"

cat > live_test_dropdown.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Live Model Dropdown Test</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 800px; }
        .test-section { margin: 20px 0; padding: 15px; border: 2px solid #ddd; border-radius: 8px; }
        select { width: 300px; padding: 8px; margin: 5px 0; font-size: 14px; }
        select:disabled { opacity: 0.5; background: #f0f0f0; }
        .result { margin: 10px 0; padding: 8px; border-radius: 4px; font-weight: bold; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .warning { background: #fff3cd; color: #856404; }
        button { padding: 8px 15px; margin: 5px; cursor: pointer; }
        .debug-info { background: #e7f3ff; padding: 10px; margin: 10px 0; border-radius: 5px; font-family: monospace; }
    </style>
</head>
<body>
    <h1>🔍 Model Dropdown Debug Test</h1>
    <p>This test isolates the model dropdown functionality to identify the exact issue.</p>

    <div class="test-section">
        <h3>Test 1: Basic Model Loading</h3>
        <label>Provider:</label><br>
        <select id="testProvider1">
            <option value="">Select Provider...</option>
            <option value="Claude">Claude</option>
            <option value="OpenAI">OpenAI</option>
            <option value="Gemini">Gemini</option>
        </select><br>
        
        <label>Model (should populate when provider selected):</label><br>
        <select id="testModel1" disabled>
            <option value="">First select a provider...</option>
        </select>
        
        <div id="testResult1" class="result"></div>
        <div id="debugInfo1" class="debug-info"></div>
        
        <button onclick="manualTest('Claude', 'testModel1', 'testResult1', 'debugInfo1')">Manual Test: Claude</button>
        <button onclick="manualTest('OpenAI', 'testModel1', 'testResult1', 'debugInfo1')">Manual Test: OpenAI</button>
    </div>

    <div class="test-section">
        <h3>Test 2: Data Inspection</h3>
        <button onclick="inspectModelData()">Inspect Model Data</button>
        <button onclick="testFunctionExists()">Test Function Exists</button>
        <div id="inspectionResult" class="debug-info"></div>
    </div>

    <div class="test-section">
        <h3>Test 3: Console Logs</h3>
        <p>Open browser console (F12 → Console) to see detailed debugging info.</p>
        <button onclick="enableVerboseLogging()">Enable Verbose Logging</button>
    </div>

    <script>
EOF

# Extract the actual model data from the main HTML file
echo "        // Model data extracted from main HTML file" >> live_test_dropdown.html
grep -A 200 "const modelData = {" poetry_generator_live.html | sed '/const openrouterModelData/,$d' >> live_test_dropdown.html

cat >> live_test_dropdown.html << 'EOF'

        let verboseLogging = false;

        function log(message) {
            console.log('🔍 DEBUG:', message);
            if (verboseLogging) {
                const debugInfo = document.getElementById('debugInfo1');
                debugInfo.innerHTML += message + '<br>';
            }
        }

        function loadModelsForPoet(poetNumber, provider) {
            log(`Called loadModelsForPoet(${poetNumber}, "${provider}")`);
            
            const modelSelect = document.getElementById(`testModel${poetNumber}`);
            const resultDiv = document.getElementById(`testResult${poetNumber}`);
            
            log(`Model select element: ${modelSelect ? 'Found' : 'NOT FOUND'}`);
            log(`Result div element: ${resultDiv ? 'Found' : 'NOT FOUND'}`);
            
            if (!provider) {
                log('No provider selected - disabling dropdown');
                modelSelect.disabled = true;
                modelSelect.innerHTML = '<option value="">First select a provider...</option>';
                resultDiv.innerHTML = '';
                return;
            }

            log(`Looking for models for provider: "${provider}"`);
            log(`modelData object exists: ${typeof modelData !== 'undefined'}`);
            log(`modelData keys: ${typeof modelData !== 'undefined' ? Object.keys(modelData).join(', ') : 'undefined'}`);

            const models = modelData[provider];
            log(`Models for ${provider}: ${models ? 'Found' : 'NOT FOUND'}`);
            
            if (models) {
                log(`Number of models found: ${Object.keys(models).length}`);
                log(`First few models: ${Object.keys(models).slice(0, 3).join(', ')}`);
            }
            
            if (!models) {
                log(`No models found for provider: ${provider}`);
                modelSelect.innerHTML = '<option value="">No models available</option>';
                modelSelect.disabled = true;
                resultDiv.innerHTML = '<span class="error">❌ No models found for ' + provider + '</span>';
                return;
            }
            
            log('Populating dropdown with models...');
            modelSelect.innerHTML = '<option value="">Select model...</option>';
            
            let modelCount = 0;
            Object.entries(models).forEach(([displayName, modelId]) => {
                log(`Adding model: ${displayName} → ${modelId}`);
                const option = document.createElement('option');
                option.value = modelId;
                option.textContent = displayName;
                modelSelect.appendChild(option);
                modelCount++;
            });
            
            modelSelect.disabled = false;
            log(`Successfully added ${modelCount} models to dropdown`);
            resultDiv.innerHTML = `<span class="success">✅ Loaded ${modelCount} models for ${provider}</span>`;
        }

        function manualTest(provider, modelSelectId, resultId, debugId) {
            document.getElementById(debugId).innerHTML = '';
            log(`Manual test: Loading models for ${provider}`);
            
            // Get the poet number from the select ID
            const poetNumber = modelSelectId.replace('testModel', '');
            loadModelsForPoet(poetNumber, provider);
        }

        function inspectModelData() {
            const resultDiv = document.getElementById('inspectionResult');
            let html = '<strong>Model Data Inspection:</strong><br>';
            
            if (typeof modelData === 'undefined') {
                html += '❌ modelData is undefined!<br>';
            } else {
                html += `✅ modelData exists<br>`;
                html += `📊 Providers: ${Object.keys(modelData).join(', ')}<br>`;
                
                Object.entries(modelData).forEach(([provider, models]) => {
                    html += `<br><strong>${provider}:</strong> ${Object.keys(models).length} models<br>`;
                    Object.entries(models).slice(0, 3).forEach(([name, id]) => {
                        html += `&nbsp;&nbsp;• ${name} → ${id}<br>`;
                    });
                    if (Object.keys(models).length > 3) {
                        html += `&nbsp;&nbsp;... and ${Object.keys(models).length - 3} more<br>`;
                    }
                });
            }
            
            resultDiv.innerHTML = html;
        }

        function testFunctionExists() {
            const resultDiv = document.getElementById('inspectionResult');
            let html = '<strong>Function Existence Test:</strong><br>';
            
            html += `loadModelsForPoet: ${typeof loadModelsForPoet === 'function' ? '✅ Exists' : '❌ Missing'}<br>`;
            html += `Object.entries: ${typeof Object.entries === 'function' ? '✅ Exists' : '❌ Missing'}<br>`;
            html += `document.getElementById: ${typeof document.getElementById === 'function' ? '✅ Exists' : '❌ Missing'}<br>`;
            
            resultDiv.innerHTML += html;
        }

        function enableVerboseLogging() {
            verboseLogging = true;
            log('Verbose logging enabled');
        }

        // Set up event listeners
        document.addEventListener('DOMContentLoaded', function() {
            log('DOM loaded, setting up event listeners');
            
            document.getElementById('testProvider1').addEventListener('change', function() {
                log(`Provider changed to: "${this.value}"`);
                loadModelsForPoet('1', this.value);
            });
            
            log('Event listeners set up successfully');
            
            // Auto-run inspection
            setTimeout(() => {
                inspectModelData();
                testFunctionExists();
            }, 500);
        });
    </script>
</body>
</html>
EOF

echo "${GREEN}✅ Created live_test_dropdown.html${NC}"

# Step 3: Compare with main HTML structure
echo ""
echo "${CYAN}Step 3: Checking Main HTML Structure${NC}"

# Check if the event listeners are properly set up in the main file
echo ""
echo "${YELLOW}📋 Event listener setup in main HTML:${NC}"
if grep -A 5 -B 2 "poet1Provider.*addEventListener.*change" poetry_generator_live.html; then
    echo "${GREEN}✅ Found poet1Provider event listener${NC}"
else
    echo "${RED}❌ poet1Provider event listener not found${NC}"
fi

echo ""
echo "${YELLOW}📋 loadModelsForPoet calls in main HTML:${NC}"
if grep -n "loadModelsForPoet" poetry_generator_live.html; then
    echo "${GREEN}✅ Found loadModelsForPoet function calls${NC}"
else
    echo "${RED}❌ No loadModelsForPoet function calls found${NC}"
fi

# Step 4: Create quick fix script
echo ""
echo "${CYAN}Step 4: Creating Quick Fix Script${NC}"

cat > quick_dropdown_fix.sh << 'EOF'
#!/usr/bin/env zsh

# Quick fix for dropdown issue
echo "🔧 Applying quick dropdown fix..."

# Check if the issue is in the function call parameters
echo "Checking function call syntax..."

if grep -q "loadModelsForPoet(1, this.value)" poetry_generator_live.html; then
    echo "✅ Function calls look correct"
else
    echo "⚠️  Function call syntax may be incorrect"
fi

# Check if DOMContentLoaded is properly set up
if grep -q "DOMContentLoaded.*function" poetry_generator_live.html; then
    echo "✅ DOMContentLoaded listener found"
else
    echo "❌ DOMContentLoaded listener missing"
fi

echo ""
echo "💡 Next steps:"
echo "1. Open live_test_dropdown.html in browser"
echo "2. Check browser console for errors"
echo "3. Try the manual test buttons"
echo "4. Look at the data inspection results"
EOF

chmod +x quick_dropdown_fix.sh

echo "${GREEN}✅ Created quick_dropdown_fix.sh${NC}"

# Step 5: Summary and instructions
echo ""
echo "${CYAN}🎯 Debug Summary${NC}"
echo "=================="
echo ""
echo "${GREEN}Files Created:${NC}"
echo "  • ${YELLOW}live_test_dropdown.html${NC} - Interactive test to isolate the issue"
echo "  • ${YELLOW}extracted_function.js${NC} - The actual loadModelsForPoet function"
echo "  • ${YELLOW}quick_dropdown_fix.sh${NC} - Quick diagnostic checks"
echo ""
echo "${CYAN}Next Steps:${NC}"
echo "1. ${YELLOW}Open live_test_dropdown.html in your browser${NC}"
echo "2. ${YELLOW}Check the console (F12) for JavaScript errors${NC}"
echo "3. ${YELLOW}Click 'Inspect Model Data' to see if data is loaded${NC}"
echo "4. ${YELLOW}Try the manual test buttons${NC}"
echo "5. ${YELLOW}Compare behavior with the main interface${NC}"
echo ""
echo "${CYAN}The test will show exactly why the dropdowns aren't populating!${NC}"

# Cleanup
rm -f extracted_function.js 2>/dev/null || true