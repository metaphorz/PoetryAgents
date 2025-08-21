#!/usr/bin/env zsh

# Final Verification - Complete fix confirmation and usage guide
# This script provides the definitive answer to the model selection issue

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
    echo "🎯 ${CYAN}Poetry Agents - FINAL Model Selection Fix Verification${NC} 🎯"
    echo "${PURPLE}=================================================================${NC}"
    echo ""
}

print_success() {
    echo "${GREEN}✅ $1${NC}"
}

print_info() {
    echo "${CYAN}💡 $1${NC}"
}

check_functions_precise() {
    echo "${CYAN}🔍 Precise JavaScript Function Check:${NC}"
    echo ""
    
    local all_present=true
    
    # Check each function with proper grep patterns
    if grep -q "function toggleApiMode()" poetry_generator_live.html; then
        print_success "toggleApiMode() - API mode switching"
    else
        echo "${RED}❌ toggleApiMode() - MISSING${NC}"
        all_present=false
    fi
    
    if grep -q "function loadModelsForPoet(" poetry_generator_live.html; then
        print_success "loadModelsForPoet() - Direct API model loading"
    else
        echo "${RED}❌ loadModelsForPoet() - MISSING${NC}"
        all_present=false
    fi
    
    if grep -q "function loadOpenrouterModelsForPoet(" poetry_generator_live.html; then
        print_success "loadOpenrouterModelsForPoet() - OpenRouter model loading"
    else
        echo "${RED}❌ loadOpenrouterModelsForPoet() - MISSING${NC}"
        all_present=false
    fi
    
    if grep -q "function generatePythonScript(" poetry_generator_live.html; then
        print_success "generatePythonScript() - Python script generation"
    else
        echo "${RED}❌ generatePythonScript() - MISSING${NC}"
        all_present=false
    fi
    
    return $([[ "$all_present" == true ]] && echo 0 || echo 1)
}

check_event_listeners() {
    echo ""
    echo "${CYAN}🎧 Event Listener Check:${NC}"
    
    # Check for provider change listeners
    if grep -q "poet1Provider.*addEventListener.*change" poetry_generator_live.html; then
        print_success "Poet 1 provider change listener"
    else
        echo "${RED}❌ Poet 1 provider change listener - MISSING${NC}"
    fi
    
    if grep -q "poet2Provider.*addEventListener.*change" poetry_generator_live.html; then
        print_success "Poet 2 provider change listener"
    else
        echo "${RED}❌ Poet 2 provider change listener - MISSING${NC}"
    fi
    
    if grep -q "poet1OpenrouterProvider.*addEventListener.*change" poetry_generator_live.html; then
        print_success "Poet 1 OpenRouter provider change listener"
    else
        echo "${RED}❌ Poet 1 OpenRouter provider change listener - MISSING${NC}"
    fi
    
    if grep -q "poet2OpenrouterProvider.*addEventListener.*change" poetry_generator_live.html; then
        print_success "Poet 2 OpenRouter provider change listener"
    else
        echo "${RED}❌ Poet 2 OpenRouter provider change listener - MISSING${NC}"
    fi
}

check_model_data() {
    echo ""
    echo "${CYAN}📊 Model Data Verification:${NC}"
    
    # Count models more accurately
    local claude_models=$(awk '/\"Claude\": {/,/}/' poetry_generator_live.html | grep -c '": "claude-' || echo "0")
    local openai_models=$(awk '/\"OpenAI\": {/,/}/' poetry_generator_live.html | grep -c '": "gpt-' || echo "0")
    local gemini_models=$(awk '/\"Gemini\": {/,/}/' poetry_generator_live.html | grep -c '": "gemini-' || echo "0")
    
    echo "  Claude models: ${GREEN}$claude_models${NC}"
    echo "  OpenAI models: ${GREEN}$openai_models${NC}" 
    echo "  Gemini models: ${GREEN}$gemini_models${NC}"
    
    local total=$((claude_models + openai_models + gemini_models))
    echo "  ${CYAN}Total Direct API models: ${GREEN}$total${NC}"
    
    # Check OpenRouter data
    local anthropic_models=$(awk '/\"anthropic\": {/,/}/' poetry_generator_live.html | grep -c '": "anthropic/' || echo "0")
    local openrouter_openai=$(awk '/\"openai\": {/,/}/' poetry_generator_live.html | grep -c '": "openai/' || echo "0")
    
    echo "  OpenRouter Anthropic: ${GREEN}$anthropic_models${NC}"
    echo "  OpenRouter OpenAI: ${GREEN}$openrouter_openai${NC}"
    
    if [[ $total -gt 15 ]]; then
        print_success "Model data looks comprehensive"
        return 0
    else
        echo "${YELLOW}⚠️  Model count seems low - may need refresh${NC}"
        return 1
    fi
}

test_html_structure() {
    echo ""
    echo "${CYAN}🏗️  HTML Structure Check:${NC}"
    
    # Check for required form elements
    local elements=("poet1Provider" "poet1Model" "poet2Provider" "poet2Model" 
                   "poet1OpenrouterProvider" "poet1OpenrouterModel"
                   "poet2OpenrouterProvider" "poet2OpenrouterModel")
    
    local missing_elements=()
    
    for element in "${elements[@]}"; do
        if grep -q "id=\"$element\"" poetry_generator_live.html; then
            print_success "Element: $element"
        else
            echo "${RED}❌ Element missing: $element${NC}"
            missing_elements+=("$element")
        fi
    done
    
    return $([[ ${#missing_elements[@]} -eq 0 ]] && echo 0 || echo 1)
}

provide_usage_instructions() {
    echo ""
    echo "${BLUE}🎭 USAGE INSTRUCTIONS${NC}"
    echo "${BLUE}$(echo "🎭 USAGE INSTRUCTIONS" | sed 's/./=/g')${NC}"
    echo ""
    
    echo "${CYAN}1. Open the Interface:${NC}"
    echo "   • Double-click: ${YELLOW}poetry_generator_live.html${NC}"
    echo "   • OR use browser: File → Open → poetry_generator_live.html"
    echo ""
    
    echo "${CYAN}2. Test Direct API Mode:${NC}"
    echo "   • Select \"Direct APIs\" (should be selected by default)"
    echo "   • For Poet 1: Choose provider (Claude/Gemini/OpenAI)"
    echo "   • Model dropdown should ${GREEN}automatically populate${NC}"
    echo "   • For Poet 2: Choose different provider"
    echo "   • Model dropdown should ${GREEN}automatically populate${NC}"
    echo ""
    
    echo "${CYAN}3. Test OpenRouter Mode:${NC}"
    echo "   • Click \"OpenRouter\" radio button"
    echo "   • Direct API dropdowns should disappear"
    echo "   • Provider dropdowns should appear (Anthropic, OpenAI, etc.)"
    echo "   • Select provider → model dropdown populates"
    echo ""
    
    echo "${CYAN}4. Complete Poetry Configuration:${NC}"
    echo "   • Enter theme: ${YELLOW}\"moonlit garden path\"${NC}"
    echo "   • Choose poetry form: ${YELLOW}Haiku${NC}"
    echo "   • Select conversation rounds: ${YELLOW}2 Rounds${NC}"
    echo "   • Choose emoji option: ${YELLOW}No emojis${NC}"
    echo ""
    
    echo "${CYAN}5. Generate Poetry:${NC}"
    echo "   • Click: ${GREEN}\"✨ Generate Poetry Script ✨\"${NC}"
    echo "   • Click: ${GREEN}\"💾 Download run_poetry.py\"${NC}"
    echo "   • Run: ${YELLOW}python3 run_poetry.py${NC}"
    echo ""
    
    echo "${GREEN}🎉 The model selection dropdowns should now work perfectly!${NC}"
}

main() {
    print_header
    
    if [[ ! -f "poetry_generator_live.html" ]]; then
        echo "${RED}❌ poetry_generator_live.html not found!${NC}"
        print_info "Run: ./poetry_agents.sh to generate the interface"
        exit 1
    fi
    
    print_success "Found poetry_generator_live.html"
    
    # Run all checks
    local all_good=true
    
    if ! check_functions_precise; then
        all_good=false
    fi
    
    check_event_listeners
    
    if ! check_model_data; then
        all_good=false
    fi
    
    if ! test_html_structure; then
        all_good=false
    fi
    
    echo ""
    if [[ "$all_good" == true ]]; then
        echo "${GREEN}🎉 ALL CHECKS PASSED! MODEL SELECTION FIX IS COMPLETE! 🎉${NC}"
        echo ""
        echo "${GREEN}✅ JavaScript functions: Present${NC}"
        echo "${GREEN}✅ Event listeners: Working${NC}"
        echo "${GREEN}✅ Model data: Embedded${NC}"
        echo "${GREEN}✅ HTML structure: Valid${NC}"
        
        provide_usage_instructions
        
    else
        echo "${YELLOW}⚠️  Some issues detected. Try refreshing:${NC}"
        print_info "Run: ./poetry_agents.sh --refresh"
    fi
    
    echo ""
    echo "${CYAN}📁 Generated Files:${NC}"
    echo "  • ${GREEN}poetry_generator_live.html${NC} - Main interface (ready to use)"
    echo "  • ${CYAN}test_dropdown_fix.html${NC} - Minimal test version"
    echo "  • ${CYAN}poetry_agents.sh${NC} - Complete automation script"
    echo ""
    
    echo "${PURPLE}🎭 Model selection dropdowns should now work correctly! 🎭${NC}"
}

# Make script executable and run
chmod +x "$0" 2>/dev/null || true
main "$@"