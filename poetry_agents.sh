#!/usr/bin/env zsh

# Poetry Agents - Complete Workflow Script
# This script does everything: fetches live models, generates HTML, and opens the interface

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emojis for better UX
ROCKET="🚀"
CHECK="✅"
WARNING="⚠️"
ERROR="❌"
INFO="💡"
POETRY="🎭"
COMPUTER="💻"
DOWNLOAD="📥"
BROWSER="🌐"

print_header() {
    echo "${PURPLE}=================================================================${NC}"
    echo "${POETRY} ${CYAN}Poetry Agents - Complete Workflow Script${NC} ${POETRY}"
    echo "${PURPLE}=================================================================${NC}"
    echo ""
}

print_section() {
    echo ""
    echo "${BLUE}$1${NC}"
    echo "${BLUE}$(echo "$1" | sed 's/./=/g')${NC}"
}

print_success() {
    echo "${GREEN}${CHECK} $1${NC}"
}

print_warning() {
    echo "${YELLOW}${WARNING} $1${NC}"
}

print_error() {
    echo "${RED}${ERROR} $1${NC}"
}

print_info() {
    echo "${CYAN}${INFO} $1${NC}"
}

check_requirements() {
    print_section "Checking Requirements"
    
    # Check if we're in the right directory
    if [[ ! -f "main.py" ]]; then
        print_error "main.py not found! Please run this script from the PoetryAgents directory."
        exit 1
    fi
    print_success "Found main.py - in correct directory"
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed or not in PATH"
        exit 1
    fi
    print_success "Python 3 is available"
    
    # Check if generate_html_interface.py exists
    if [[ ! -f "generate_html_interface.py" ]]; then
        print_error "generate_html_interface.py not found!"
        exit 1
    fi
    print_success "HTML generator script found"
    
    # Check if requirements.txt exists and install dependencies
    if [[ -f "requirements.txt" ]]; then
        print_info "Installing/updating Python dependencies..."
        python3 -m pip install -r requirements.txt --quiet
        print_success "Dependencies updated"
    else
        print_warning "requirements.txt not found - skipping dependency installation"
    fi
    
    # Check for API keys
    local has_api_keys=false
    if [[ -n "$ANTHROPIC_API_KEY" ]]; then
        print_success "Anthropic API key found"
        has_api_keys=true
    else
        print_warning "ANTHROPIC_API_KEY not set"
    fi
    
    if [[ -n "$OPENAI_API_KEY" ]]; then
        print_success "OpenAI API key found"
        has_api_keys=true
    else
        print_warning "OPENAI_API_KEY not set"
    fi
    
    if [[ -n "$GOOGLE_API_KEY" ]]; then
        print_success "Google API key found"
        has_api_keys=true
    else
        print_warning "GOOGLE_API_KEY not set"
    fi
    
    if [[ -n "$OPENROUTER_API_KEY" ]]; then
        print_success "OpenRouter API key found"
        has_api_keys=true
    else
        print_warning "OPENROUTER_API_KEY not set"
    fi
    
    if [[ "$has_api_keys" = false ]]; then
        print_error "No API keys found! Please set at least one API key environment variable."
        print_info "Example: export ANTHROPIC_API_KEY='your-key-here'"
        exit 1
    fi
}

generate_fresh_interface() {
    print_section "${ROCKET} Generating Fresh HTML Interface with Live Model Data"
    
    # Remove old generated file if it exists
    if [[ -f "poetry_generator_live.html" ]]; then
        rm "poetry_generator_live.html"
        print_info "Removed old interface file"
    fi
    
    # Generate new interface with live model data
    print_info "Fetching live model data from APIs..."
    python3 generate_html_interface.py
    
    if [[ -f "poetry_generator_live.html" ]]; then
        print_success "Fresh HTML interface generated successfully!"
        
        # Get file size and model count info
        local file_size=$(wc -c < "poetry_generator_live.html" | tr -d ' ')
        local model_count=$(grep -o '"[^"]*": "[^"]*claude-\|"[^"]*": "[^"]*gpt-\|"[^"]*": "[^"]*gemini-' poetry_generator_live.html | wc -l | tr -d ' ')
        
        print_info "File size: ${file_size} bytes"
        print_info "Total models embedded: ${model_count}"
    else
        print_error "Failed to generate HTML interface"
        exit 1
    fi
}

open_interface() {
    print_section "${BROWSER} Opening HTML Interface"
    
    local html_file="poetry_generator_live.html"
    
    if [[ ! -f "$html_file" ]]; then
        print_error "$html_file not found!"
        exit 1
    fi
    
    # Detect OS and open appropriate browser
    case "$(uname -s)" in
        Darwin*)
            print_info "Opening in default browser (macOS)..."
            open "$html_file"
            ;;
        Linux*)
            print_info "Opening in default browser (Linux)..."
            xdg-open "$html_file"
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)
            print_info "Opening in default browser (Windows)..."
            start "$html_file"
            ;;
        *)
            print_warning "Unknown OS - cannot auto-open browser"
            print_info "Please manually open: $html_file"
            return
            ;;
    esac
    
    print_success "Interface opened in your default browser!"
}

show_usage_instructions() {
    print_section "${COMPUTER} How to Use the Interface"
    
    cat << 'EOF'
🎯 Quick Start Guide:

1️⃣  CONFIGURE YOUR POETRY:
   • Choose "Direct APIs" or "OpenRouter" mode
   • Select LLM providers and specific models for both poets
   • Enter a creative theme (e.g., "moonlit garden path")
   • Pick poetry form (Haiku, Sonnet, Prose, etc.)
   • Set conversation rounds (1-4)
   • Choose emoji enhancement (yes/no)

2️⃣  GENERATE SCRIPT:
   • Click "✨ Generate Poetry Script ✨"
   • Click "💾 Download run_poetry.py"
   • Save the file to this directory

3️⃣  RUN YOUR POETRY:
   • In terminal: python3 run_poetry.py
   • Your custom poetry will be generated automatically
   • File opens in markdown viewer when complete

🎨 Theme Ideas:
   • "first snow of winter"
   • "robot learning to love"  
   • "ancient library at midnight"
   • "the last tree on earth"
   • "neon lights reflecting in puddles"

💫 Popular Combinations:
   • Claude + OpenAI, Haiku, 2 rounds (fast & beautiful)
   • Gemini + Claude, Sonnet, 1 round (sophisticated)
   • OpenRouter models, Prose, 3 rounds (experimental)
EOF
}

show_files_created() {
    print_section "${DOWNLOAD} Files Available"
    
    echo "📁 Current directory contents:"
    echo ""
    
    if [[ -f "poetry_generator_live.html" ]]; then
        local size=$(wc -c < "poetry_generator_live.html" | tr -d ' ')
        printf "   ${GREEN}${CHECK} poetry_generator_live.html${NC} (%'d bytes)\n" "$size"
        echo "      → Fresh HTML interface with live model data"
    fi
    
    if [[ -f "poetry_generator.html" ]]; then
        printf "   ${YELLOW}${WARNING} poetry_generator.html${NC} (older version)\n"
        echo "      → Static version - use poetry_generator_live.html instead"
    fi
    
    if [[ -f "generate_html_interface.py" ]]; then
        printf "   ${GREEN}${CHECK} generate_html_interface.py${NC}\n"
        echo "      → Script to refresh HTML interface with latest models"
    fi
    
    if [[ -d "outputs" ]]; then
        local poetry_count=$(find outputs -name "poetry_dialogue_*.md" | wc -l | tr -d ' ')
        printf "   ${GREEN}${CHECK} outputs/${NC} (%d poetry files)\n" "$poetry_count"
        echo "      → Your generated poetry dialogues"
    fi
    
    echo ""
    print_info "To refresh models: ./poetry_agents.sh --refresh"
    print_info "To open interface: ./poetry_agents.sh --open"
}

cleanup_old_files() {
    print_section "🧹 Cleaning Up Old Files"
    
    # Remove old test files
    if [[ -f "test_html_interface.py" ]]; then
        rm "test_html_interface.py"
        print_info "Removed test file"
    fi
    
    # Clean up any temporary files
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    print_success "Cleanup complete"
}

show_help() {
    cat << 'EOF'
🎭 Poetry Agents - Complete Workflow Script

USAGE:
    ./poetry_agents.sh [OPTIONS]

OPTIONS:
    (no args)        Run complete workflow: check requirements, generate interface, open browser
    --help, -h       Show this help message
    --refresh, -r    Regenerate HTML interface with latest model data
    --open, -o       Open existing HTML interface in browser
    --check, -c      Check requirements only
    --clean          Clean up temporary files and regenerate everything

EXAMPLES:
    ./poetry_agents.sh              # Complete workflow
    ./poetry_agents.sh --refresh    # Update models and regenerate interface
    ./poetry_agents.sh --open       # Just open the interface
    ./poetry_agents.sh --clean      # Clean and regenerate everything

REQUIREMENTS:
    • Python 3 with required packages (pip install -r requirements.txt)
    • At least one API key: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY, or OPENROUTER_API_KEY
    • Internet connection for fetching live model data

The script fetches live model data from all available APIs and creates a standalone
HTML interface that works without any server. Just open the HTML file in your browser!
EOF
}

main() {
    # Parse command line arguments
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --refresh|-r)
            print_header
            check_requirements
            generate_fresh_interface
            print_success "Interface refreshed with latest model data!"
            exit 0
            ;;
        --open|-o)
            print_header
            open_interface
            exit 0
            ;;
        --check|-c)
            print_header
            check_requirements
            print_success "All requirements satisfied!"
            exit 0
            ;;
        --clean)
            print_header
            cleanup_old_files
            check_requirements
            generate_fresh_interface
            open_interface
            show_usage_instructions
            show_files_created
            exit 0
            ;;
        "")
            # Default: full workflow
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
    
    # Main workflow
    print_header
    
    print_info "Starting complete Poetry Agents workflow..."
    print_info "This will: check requirements → generate fresh interface → open browser"
    echo ""
    
    # Step 1: Check requirements
    check_requirements
    
    # Step 2: Generate fresh interface with live model data
    generate_fresh_interface
    
    # Step 3: Open in browser
    open_interface
    
    # Step 4: Show usage instructions
    show_usage_instructions
    
    # Step 5: Show what files are available
    show_files_created
    
    print_section "${POETRY} Workflow Complete!"
    print_success "Poetry Agents is ready to use!"
    print_info "The HTML interface should now be open in your browser."
    print_info "Configure your poets, enter a theme, and generate beautiful poetry!"
    
    echo ""
    print_info "Need help? Run: ./poetry_agents.sh --help"
    print_info "Refresh models: ./poetry_agents.sh --refresh"
}

# Make sure we're executable
chmod +x "$0" 2>/dev/null || true

# Run main function with all arguments
main "$@"