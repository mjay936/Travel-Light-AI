#!/usr/bin/env python3
"""
Travel Light Launcher - Choose how to run the travel planning application
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import fpdf
        import langgraph
        import langchain
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def show_menu():
    """Show the main menu."""
    print("🚀 Travel Light - AI Travel Planning Assistant")
    print("=" * 50)
    print("Choose how to run the application:")
    print()
    print("1. 🌐 Web Interface (Streamlit)")
    print("2. 💻 Command Line Interface")
    print("3. 🎮 Demo Version (No API keys needed)")
    print("4. 🔧 Check Setup")
    print("5. ❌ Exit")
    print()

def run_web_interface():
    """Launch the Streamlit web interface."""
    print("🌐 Starting web interface...")
    print("💡 The app will open in your browser at http://localhost:8501")
    print("💡 Press Ctrl+C to stop the server")
    print()
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "travel_light_webpage.py"])
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped.")
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")

def run_cli():
    """Run the command line interface."""
    print("💻 Starting command line interface...")
    print()
    
    try:
        subprocess.run([sys.executable, "travel_light.py"])
    except KeyboardInterrupt:
        print("\n👋 CLI stopped.")
    except Exception as e:
        print(f"❌ Error running CLI: {e}")

def run_demo():
    """Run the demo version."""
    print("🎮 Starting demo version...")
    print()
    
    try:
        subprocess.run([sys.executable, "demo_version.py"])
    except KeyboardInterrupt:
        print("\n👋 Demo stopped.")
    except Exception as e:
        print(f"❌ Error running demo: {e}")

def check_setup():
    """Check the current setup."""
    print("🔧 Checking setup...")
    print()
    
    # Check dependencies
    if check_dependencies():
        print("✅ All dependencies installed")
    else:
        print("❌ Missing dependencies")
        return
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    amadeus_key = os.getenv("AMADEUS_API_KEY")
    aviation_key = os.getenv("AVIATIONSTACK_API_KEY")
    
    print(f"🔑 OpenAI API Key: {'✅ Set' if openai_key else '❌ Not Set'}")
    print(f"🔑 Amadeus API Key: {'✅ Set' if amadeus_key else '❌ Not Set (Optional)'}")
    print(f"🔑 AviationStack API Key: {'✅ Set' if aviation_key else '❌ Not Set (Optional)'}")
    
    if not openai_key:
        print("\n💡 To use the full AI version:")
        print("1. Get an OpenAI API key from https://platform.openai.com/api-keys")
        print("2. Create a .env file with: OPENAI_API_KEY=your_key_here")
        print("3. Restart this launcher")
    
    print("\n📁 Files found:")
    files = [
        "travel_light.py",
        "travel_light_webpage.py", 
        "demo_version.py",
        "requirements.txt"
    ]
    
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")

def main():
    """Main launcher function."""
    if not check_dependencies():
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                run_web_interface()
            elif choice == "2":
                run_cli()
            elif choice == "3":
                run_demo()
            elif choice == "4":
                check_setup()
                input("\nPress Enter to continue...")
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
