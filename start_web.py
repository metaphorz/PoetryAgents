#!/usr/bin/env python3
"""
Simple startup script for the Poetry Agents web interface.
Checks dependencies and starts the web server.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['flask', 'flask_cors']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install them with:")
        print("   pip install flask flask-cors")
        print("\n   Or install all requirements:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_environment():
    """Check if required environment variables are set."""
    required_vars = ['ANTHROPIC_API_KEY']
    optional_vars = ['OPENAI_API_KEY', 'GEMINI_API_KEY', 'OPENROUTER_API_KEY']
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print("❌ Missing required environment variables:")
        for var in missing_required:
            print(f"   - {var}")
        print("\n💡 Set them in your .env file or export them:")
        for var in missing_required:
            print(f"   export {var}=your_api_key_here")
        return False
    
    if missing_optional:
        print("⚠️  Optional environment variables not set:")
        for var in missing_optional:
            print(f"   - {var}")
        print("   (Some providers won't be available)")
    
    return True

def main():
    """Main startup function."""
    print("🎭 Poetry Agents Web Interface Startup")
    print("=" * 40)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ Dependencies OK")
    
    # Check environment
    print("\n🔑 Checking environment variables...")
    if not check_environment():
        sys.exit(1)
    print("✅ Environment OK")
    
    # Ensure outputs directory exists
    os.makedirs('outputs', exist_ok=True)
    
    print("\n🚀 Starting web server...")
    print("📱 Open your browser to: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    # Start the web server
    try:
        from web_server import app
        app.run(debug=True, host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Poetry Agents web server...")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()