#!/usr/bin/env python3
"""
Demo script to show the Poetry Agents web interface in action.
Opens the web server and provides example usage instructions.
"""

import os
import sys
import time
import webbrowser
import threading
from web_server import app

def show_demo_instructions():
    """Show demo instructions after a short delay."""
    time.sleep(2)  # Wait for server to start
    
    print("\n" + "="*60)
    print("🎭 POETRY AGENTS WEB INTERFACE DEMO")
    print("="*60)
    print()
    print("🌐 Web interface is now running at: http://localhost:5000")
    print()
    print("💡 QUICK DEMO STEPS:")
    print("   1. The page should open automatically in your browser")
    print("   2. Select providers for both poets (e.g., Claude + OpenAI)")
    print("   3. Choose specific models from the dropdowns")
    print("   4. Enter a theme like: 'walking in autumn rain'")
    print("   5. Select poetry form (try Haiku for quick results)")
    print("   6. Choose 2 rounds of conversation")
    print("   7. Click 'Generate Poetry Dialogue'")
    print()
    print("📝 EXAMPLE THEMES TO TRY:")
    print("   • 'a cat watching snow fall'")
    print("   • 'the last bookstore on earth'")
    print("   • 'dancing with shadows at midnight'")
    print("   • 'finding a message in a bottle'")
    print("   • 'the sound of wind through trees'")
    print()
    print("🎨 POETRY FORMS TO EXPLORE:")
    print("   • Haiku (3 lines, 5-7-5 syllables) - Quick to generate")
    print("   • Prose (paragraph form) - Expressive and flowing")
    print("   • Sonnet (14 lines) - Classic and structured")
    print("   • Limerick (5 lines) - Humorous and playful")
    print()
    print("🛑 Press Ctrl+C here to stop the demo server")
    print("="*60)

def main():
    """Run the demo."""
    print("🚀 Starting Poetry Agents Web Interface Demo...")
    
    # Check if we have at least one API key
    api_keys = {
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'OPENROUTER_API_KEY': os.getenv('OPENROUTER_API_KEY')
    }
    
    available_keys = [name for name, key in api_keys.items() if key]
    
    if not available_keys:
        print("\n❌ No API keys found!")
        print("💡 Set at least one API key in your environment:")
        print("   export ANTHROPIC_API_KEY=your_key_here")
        print("   export OPENAI_API_KEY=your_key_here")
        print("   export GEMINI_API_KEY=your_key_here")
        print("   export OPENROUTER_API_KEY=your_key_here")
        sys.exit(1)
    
    print(f"✅ Found API keys: {', '.join(available_keys)}")
    
    # Ensure outputs directory exists
    os.makedirs('outputs', exist_ok=True)
    
    # Start instruction thread
    instruction_thread = threading.Thread(target=show_demo_instructions)
    instruction_thread.daemon = True
    instruction_thread.start()
    
    # Try to open browser automatically
    try:
        threading.Timer(1.0, lambda: webbrowser.open('http://localhost:5000')).start()
    except:
        pass  # Browser opening is optional
    
    # Start the Flask server
    try:
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Demo completed! Thanks for trying Poetry Agents!")
        print("📁 Check the 'outputs' folder for any generated poetry files.")

if __name__ == '__main__':
    main()