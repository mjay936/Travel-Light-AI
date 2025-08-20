#!/usr/bin/env python3
"""
Demo version of Travel Light - shows the functionality without requiring API keys
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TravelLightDemo:
    def __init__(self):
        self.conversation_history = []
        
    def add_message(self, role, content):
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})
        
    def generate_itinerary(self, destination, days, budget):
        """Generate a sample itinerary."""
        itineraries = {
            "bali": {
                "budget": f"""
🌴 {days}-Day Budget Trip to Bali

Day 1: Arrival & Kuta Beach
- Arrive at Ngurah Rai International Airport
- Check into budget hostel in Kuta (IDR 200,000/night)
- Explore Kuta Beach and watch sunset
- Dinner at local warung (IDR 50,000)
- Optional: Beach party at night

Day 2: Cultural Ubud
- Morning: Visit Sacred Monkey Forest (IDR 80,000)
- Afternoon: Explore Ubud Palace and Market
- Evening: Traditional dance performance (IDR 150,000)
- Dinner at local restaurant (IDR 75,000)

Day 3: Adventure & Departure
- Morning: Sunrise at Mount Batur (IDR 300,000 with guide)
- Afternoon: Visit Tanah Lot Temple (IDR 60,000)
- Evening: Last-minute shopping at Kuta
- Departure

💰 Total Budget: ~IDR 1,000,000 (≈ $70 USD)
🏨 Accommodation: Budget hostels
🍽️ Food: Local warungs and street food
🚗 Transport: Local buses and shared taxis
""",
                "mid-range": f"""
🌴 {days}-Day Mid-Range Trip to Bali

Day 1: Arrival & Seminyak
- Arrive at Ngurah Rai International Airport
- Check into boutique hotel in Seminyak (IDR 800,000/night)
- Relax at Seminyak Beach
- Sunset cocktails at beach club
- Dinner at upscale restaurant (IDR 300,000)

Day 2: Cultural & Nature
- Morning: Private tour to Tegalalang Rice Terraces
- Afternoon: Visit Ubud Palace and Sacred Monkey Forest
- Evening: Traditional dance at Ubud Palace
- Dinner at organic farm restaurant (IDR 400,000)

Day 3: Luxury & Departure
- Morning: Private sunrise tour to Mount Batur
- Afternoon: Spa treatment at luxury resort
- Evening: Fine dining experience
- Departure

💰 Total Budget: ~IDR 4,000,000 (≈ $280 USD)
🏨 Accommodation: Boutique hotels
🍽️ Food: Mid-range restaurants
🚗 Transport: Private driver
""",
                "luxury": f"""
🌴 {days}-Day Luxury Trip to Bali

Day 1: Arrival & Luxury Resort
- Private airport transfer to luxury resort
- Check into 5-star resort in Nusa Dua (IDR 3,000,000/night)
- Private beach access and infinity pool
- Sunset dinner at resort's fine dining restaurant
- Optional: Private beach bonfire

Day 2: Exclusive Experiences
- Private helicopter tour over Bali
- Exclusive access to hidden waterfalls
- Private cooking class with master chef
- Sunset yacht cruise with champagne
- Michelin-starred dinner experience

Day 3: Ultimate Luxury & Departure
- Private sunrise yoga session
- Exclusive spa treatment package
- Private island lunch experience
- Luxury shopping with personal stylist
- Private jet departure

💰 Total Budget: ~IDR 15,000,000 (≈ $1,000 USD)
🏨 Accommodation: 5-star luxury resorts
🍽️ Food: Fine dining and exclusive experiences
🚗 Transport: Private helicopter and luxury vehicles
"""
            }
        }
        
        return itineraries.get(destination.lower(), itineraries["bali"])[budget]
    
    def search_hotels(self, city, check_in, check_out, adults):
        """Simulate hotel search."""
        hotels = {
            "bali": [
                "🏨 Budget: Kuta Beach Hostel - $25/night",
                "🏨 Mid-Range: Seminyak Boutique Hotel - $120/night", 
                "🏨 Luxury: Nusa Dua Resort & Spa - $350/night"
            ],
            "tokyo": [
                "🏨 Budget: Asakusa Capsule Hotel - $30/night",
                "🏨 Mid-Range: Shibuya Business Hotel - $150/night",
                "🏨 Luxury: Ritz-Carlton Tokyo - $500/night"
            ]
        }
        return "\n".join(hotels.get(city.lower(), hotels["bali"]))
    
    def search_flights(self, from_city, to_city, date):
        """Simulate flight search."""
        flights = [
            "✈️ Economy: AirAsia - $450 (12h 30m)",
            "✈️ Business: Singapore Airlines - $1,200 (11h 45m)",
            "✈️ First Class: Emirates - $3,500 (10h 15m)"
        ]
        return "\n".join(flights)
    
    def run_demo(self):
        """Run the interactive demo."""
        print("🚀 Travel Light - AI Travel Planning Assistant (Demo Mode)")
        print("=" * 60)
        print("This is a demo version that simulates the AI travel planning experience.")
        print("In the full version, this would be powered by OpenAI's GPT models.\n")
        
        # Simulate user input
        destination = "Bali"
        days = 3
        budget = "budget"
        
        print(f"🎯 Planning a {days}-day {budget} trip to {destination}...")
        print("=" * 60)
        
        # Generate itinerary
        itinerary = self.generate_itinerary(destination, days, budget)
        self.add_message("assistant", f"I'll create a {days}-day {budget} itinerary for {destination}.")
        self.add_message("assistant", itinerary)
        
        print("📋 Generated Itinerary:")
        print(itinerary)
        
        # Simulate user confirmation
        print("\n" + "=" * 60)
        print("User: This looks great! Can you help me find hotels and flights?")
        self.add_message("user", "This looks great! Can you help me find hotels and flights?")
        
        # Search hotels
        hotels = self.search_hotels("bali", "2025-06-01", "2025-06-04", 1)
        self.add_message("assistant", "Here are some hotel options for Bali:")
        self.add_message("assistant", hotels)
        
        print("\n🏨 Hotel Options:")
        print(hotels)
        
        # Search flights
        flights = self.search_flights("New York", "Bali", "2025-06-01")
        self.add_message("assistant", "Here are some flight options:")
        self.add_message("assistant", flights)
        
        print("\n✈️ Flight Options:")
        print(flights)
        
        print("\n" + "=" * 60)
        print("🎉 Demo completed! This shows how the AI travel planning system works.")
        print("\nTo run the full AI-powered version:")
        print("1. Get an OpenAI API key from https://platform.openai.com/api-keys")
        print("2. Create a .env file with: OPENAI_API_KEY=your_key_here")
        print("3. Run: python travel_light.py")

if __name__ == "__main__":
    demo = TravelLightDemo()
    demo.run_demo()
