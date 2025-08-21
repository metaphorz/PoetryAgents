#!/usr/bin/env zsh

# Poetry Agents Web Server Startup Script
# Loads environment variables from .env and starts the web server

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print header
echo "${BLUE}🎭 Poetry Agents Web Server${NC}"
echo "${BLUE}================================${NC}"
echo ""

# Check if .env file exists
if [[ ! -f ".env" ]]; then
    echo "${RED}❌ .env file not found!${NC}"
    echo "${YELLOW}💡 Please create a .env file with your API keys${NC}"
    exit 1
fi

echo "${GREEN}✅ Found .env file${NC}"

# Load environment variables from .env file
# Remove any quotes and export each line
while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip empty lines and comments
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    
    # Remove quotes and export the variable
    key=$(echo "$line" | cut -d'=' -f1)
    value=$(echo "$line" | cut -d'=' -f2- | sed 's/^["'\'']\|["'\'']$//g')
    
    if [[ -n "$key" && -n "$value" ]]; then
        export "$key"="$value"
        echo "${GREEN}✅ Loaded: $key${NC}"
    fi
done < .env

echo ""

# Check for required dependencies
echo "${BLUE}🔍 Checking dependencies...${NC}"
if ! python -c "import flask, flask_cors" 2>/dev/null; then
    echo "${YELLOW}⚠️  Installing Flask dependencies...${NC}"
    pip install flask flask-cors
fi
echo "${GREEN}✅ Dependencies OK${NC}"

echo ""

# Start the web server
echo "${BLUE}🚀 Starting Poetry Agents Web Server...${NC}"
echo "${GREEN}📱 Open your browser to: http://localhost:8080${NC}"
echo "${YELLOW}🛑 Press Ctrl+C to stop the server${NC}"
echo ""

# Start the server
python start_web.py