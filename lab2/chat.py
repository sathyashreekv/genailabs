import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

def get_user_location(user_id: str) -> str:
    """Retrieve user location based on user ID."""
    return "Florida" if user_id == "1" else "SF"

def weather_agent_chat(user_input: str, user_id: str = "1"):
    """Interactive weather agent using Google Generative AI."""
    try:
        import google.generativeai as genai
        
        # Configure API
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        
        # Get user location and weather
        location = get_user_location(user_id)
        weather = get_weather_for_location(location)
        
        # Create model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create prompt
        prompt = f"""You are an expert weather forecaster who speaks in puns and loves to chat!

User location: {location}
Current weather: {weather}
User message: {user_input}

Respond with weather-related puns and be conversational. If they ask about weather, give a punny forecast. If they chat about other things, still work in weather puns when possible:"""
        
        # Get response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Oops! Looks like there's a 'storm' in my system: {e}"

def chat_loop():
    """Interactive chat loop with the weather agent."""
    print("🌤️  Weather Agent Chat - Powered by Gemini 2.5 Flash")
    print("=" * 60)
    print("Ask me about the weather or just chat! Type 'quit' to exit.")
    print("=" * 60)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nWeather Agent: Have a 'sun-sational' day! Don't let any storms cloud your mood! ☀️")
            break
        
        if not user_input:
            continue
            
        print("\nWeather Agent: ", end="")
        response = weather_agent_chat(user_input)
        print(response)

if __name__ == "__main__":
    chat_loop()