#!/usr/bin/env python3
"""
Test version of Travel Light - demonstrates the structure without requiring API keys
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_setup():
    """Test the setup and show what's needed to run the full application."""
    print("🚀 Travel Light - AI Travel Planning Assistant")
    print("=" * 50)
    
    # Check environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    amadeus_key = os.getenv("AMADEUS_API_KEY")
    aviation_key = os.getenv("AVIATIONSTACK_API_KEY")
    
    print("📋 Environment Check:")
    print(f"✅ OpenAI API Key: {'Set' if openai_key else '❌ Not Set'}")
    print(f"✅ Amadeus API Key: {'Set' if amadeus_key else '❌ Not Set (Optional)'}")
    print(f"✅ AviationStack API Key: {'Set' if aviation_key else '❌ Not Set (Optional)'}")
    
    print("\n🔧 Setup Instructions:")
    print("1. Create a .env file in this directory")
    print("2. Add your API keys:")
    print("   OPENAI_API_KEY=your_openai_api_key_here")
    print("   AMADEUS_API_KEY=your_amadeus_api_key_here (optional)")
    print("   AMADEUS_API_SECRET=your_amadeus_secret_here (optional)")
    print("   AVIATIONSTACK_API_KEY=your_aviationstack_key_here (optional)")
    
    print("\n🌐 Get API Keys:")
    print("- OpenAI: https://platform.openai.com/api-keys")
    print("- Amadeus: https://developers.amadeus.com/")
    print("- AviationStack: https://aviationstack.com/")
    
    print("\n🎯 To run the full application:")
    print("python travel_light.py")
    
    print("\n📝 Example .env file content:")
    print("OPENAI_API_KEY=sk-your-openai-key-here")
    print("AMADEUS_API_KEY=your-amadeus-key")
    print("AMADEUS_API_SECRET=your-amadeus-secret")
    print("AVIATIONSTACK_API_KEY=your-aviationstack-key")

if __name__ == "__main__":
    test_setup()
