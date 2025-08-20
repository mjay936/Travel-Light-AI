import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for OpenAI API key early
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  Warning: OPENAI_API_KEY not found. Running in demo mode.")
    print("💡 To use the full AI version, set OPENAI_API_KEY in your .env file")
    
    # Demo mode - create simple functions that return demo data
    def build_conversation_graph():
        """Demo version of the conversation graph."""
        class DemoGraph:
            def invoke(self, state):
                user_msg = state.get("messages", [])[-1] if state.get("messages") else {"content": ""}
                content = user_msg.get("content", "").lower()
                
                if "bali" in content:
                    return {
                        "messages": [
                            {"role": "assistant", "content": "🌴 Here's a 3-day budget trip to Bali:\n\nDay 1: Arrive in Bali, check into budget hostel in Kuta, explore Kuta Beach\nDay 2: Visit Sacred Monkey Forest in Ubud, explore Ubud Palace\nDay 3: Sunrise at Mount Batur, visit Tanah Lot Temple\n\nDoes this look good to you?"}
                        ]
                    }
                else:
                    return {
                        "messages": [
                            {"role": "assistant", "content": "🎯 I can help you plan trips! Try asking for a specific destination, like 'Plan a 3-day budget trip to Bali'"}
                        ]
                    }
        
        return DemoGraph()
    
    # Export the demo function
    __all__ = ['build_conversation_graph']
    
else:
    # Full AI mode - import the real components
    from llm_provider import ACTIVE_LLM
    from langgraph.prebuilt import create_react_agent

    AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
    AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")
    AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

    def get_amadeus_access_token():
        """Obtain Amadeus API OAuth2 Access Token."""
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': AMADEUS_API_KEY,
            'client_secret': AMADEUS_API_SECRET
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception(f"Failed to retrieve Amadeus token: {response.text}")

    def search_hotels(city_code: str, check_in: str, check_out: str, adults: int = 1) -> str:
        """Search hotels using Amadeus API based on city, dates, and number of adults."""
        if not AMADEUS_API_KEY or not AMADEUS_API_SECRET:
            return "Amadeus API credentials not configured. Please set AMADEUS_API_KEY and AMADEUS_API_SECRET in your .env file."
        
        try:
            token = get_amadeus_access_token()
            url = f"https://test.api.amadeus.com/v2/shopping/hotel-offers?cityCode={city_code}&checkInDate={check_in}&checkOutDate={check_out}&adults={adults}"
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return f"Failed to retrieve hotels: {response.text}"
            hotels = response.json().get("data", [])
            if not hotels:
                return "No hotels found."
            return "\n".join([
                f"{h['hotel']['name']} - ${h['offers'][0]['price']['total']}"
                for h in hotels[:3]
            ])
        except Exception as e:
            return f"Error searching hotels: {str(e)}"

    def hotel_search_tool(city_code: str, check_in: str, check_out: str, adults: int = 1) -> str:
        """Retrieve hotel options for specified city and dates using Amadeus API."""
        return search_hotels(city_code, check_in, check_out, adults)

    def flight_search_tool(query: str) -> str:
        """Search for flights using AviationStack API (static example)."""
        if not AVIATIONSTACK_API_KEY:
            return "AviationStack API key not configured. Please set AVIATIONSTACK_API_KEY in your .env file."
        
        try:
            source = "JFK"
            destination = "LHR"
            date = "2025-06-01"
            url = f"http://api.aviationstack.com/v1/flights?access_key={AVIATIONSTACK_API_KEY}&dep_iata={source}&arr_iata={destination}&flight_date={date}"
            response = requests.get(url)
            if response.status_code != 200:
                return f"Failed to fetch flight data: {response.text}"
            flights = response.json().get('data', [])
            if not flights:
                return "No flights found."
            return "\n".join([
                f"{f['airline']['name']} flight {f['flight']['iata']} at {f['departure']['scheduled']}"
                for f in flights[:3]
            ])
        except Exception as e:
            return f"Error searching flights: {str(e)}"

    # Create a simple travel planning agent with all tools
    travel_agent_prompt = """
    You are a world-class travel planning assistant.

    You can help users with:
    1. Creating detailed day-by-day itineraries
    2. Searching for hotels (use hotel_search_tool)
    3. Searching for flights (use flight_search_tool)

    When creating itineraries, include:
    - Key activities for each day
    - Recommended dining options
    - Cultural highlights
    - Local tips
    - Budget estimates

    Always be helpful, detailed, and provide practical travel advice.
    """

    # Create the main travel agent with all tools
    travel_agent = create_react_agent(
        model=ACTIVE_LLM,
        tools=[hotel_search_tool, flight_search_tool],
        prompt=travel_agent_prompt,
        name="travel_agent"
    )

    def build_conversation_graph():
        """Build a simple conversation graph with the travel agent."""
        return travel_agent

    # Export the function
    __all__ = ['build_conversation_graph']

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        print("\n💡 Running demo mode instead...")
        
        # Run demo
        graph = build_conversation_graph()
        test_state = {"messages": [{"role": "user", "content": "Plan a 3-day solo budget trip to Bali"}]}
        
        try:
            result = graph.invoke(test_state)
            print("\n📋 Demo Response:")
            print("=" * 50)
            for msg in result.get("messages", []):
                print(f"{msg['role'].capitalize()}: {msg['content']}")
        except Exception as e:
            print(f"❌ Demo error: {str(e)}")
        
        exit(0)
    
    print("🚀 Starting Travel Light - AI Travel Planning Assistant")
    print("=" * 50)
    
    graph = build_conversation_graph()
    test_state = {"messages": [{"role": "user", "content": "Plan a 3-day solo budget trip to Bali"}]}
    
    try:
        result = graph.invoke(test_state)
        print("\n📋 Conversation History:")
        print("=" * 50)
        for msg in result.get("messages", []):
            print(f"{msg['role'].capitalize()}: {msg['content']}")
    except Exception as e:
        print(f"❌ Error running the application: {str(e)}")
        print("\n💡 Make sure you have:")
        print("1. Set OPENAI_API_KEY in your .env file")
        print("2. Have an active internet connection")
        print("3. Have sufficient OpenAI API credits")
