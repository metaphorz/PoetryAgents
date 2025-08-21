#!/usr/bin/env zsh

# Poetry Agents Web Server Stop Script
# Stops the web server running on port 8080

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print header
echo "${BLUE}🎭 Poetry Agents Web Server - Stop${NC}"
echo "${BLUE}=====================================${NC}"
echo ""

# Find processes running on port 8080
echo "${BLUE}🔍 Looking for web server processes...${NC}"

# Kill processes using port 8080
if command -v lsof > /dev/null; then
    PIDS=$(lsof -ti:8080 2>/dev/null || true)
    if [[ -n "$PIDS" ]]; then
        echo "${BLUE}📋 Found processes: $PIDS${NC}"
        echo "${BLUE}🛑 Stopping web server...${NC}"
        
        # Kill the processes
        for pid in $PIDS; do
            if kill -TERM $pid 2>/dev/null; then
                echo "   Stopped PID $pid"
            fi
        done
        
        # Wait and force kill if needed
        sleep 2
        for pid in $PIDS; do
            if ps -p $pid > /dev/null 2>&1; then
                kill -KILL $pid 2>/dev/null || true
                echo "   Force killed PID $pid"
            fi
        done
        
        echo "${GREEN}✅ Web server stopped successfully!${NC}"
    else
        echo "${YELLOW}⚠️  No web server found running on port 8080${NC}"
        echo "${GREEN}✅ Server is already stopped${NC}"
    fi
else
    # Fallback method using ps and grep
    echo "${BLUE}🛑 Stopping Python web server processes...${NC}"
    pkill -f "python.*start_web.py" 2>/dev/null && echo "${GREEN}✅ Stopped start_web.py${NC}" || true
    pkill -f "python.*web_server.py" 2>/dev/null && echo "${GREEN}✅ Stopped web_server.py${NC}" || true
    pkill -f "Flask" 2>/dev/null && echo "${GREEN}✅ Stopped Flask processes${NC}" || true
    echo "${GREEN}✅ Stop commands completed${NC}"
fi

echo ""
echo "${BLUE}💡 To start the server again, run: ./start_web_server.sh${NC}"