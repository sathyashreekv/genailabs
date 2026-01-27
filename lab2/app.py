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

def test_google_genai():
    """Test Google Generative AI directly."""
    try:
        import google.generativeai as genai
        
        # Configure API key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("No API key found in environment")
            return None
            
        genai.configure(api_key=api_key)
        
        # List available models
        print("Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
        
        # Try to use a model
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say hello")
        print(f"Success: {response.text}")
        return True
        
    except ImportError:
        print("google-generativeai not installed. Installing...")
        os.system("pip install google-generativeai")
        return test_google_genai()
    except Exception as e:
        print(f"API test failed: {e}")
        return False

def weather_agent_with_genai(user_input: str, user_id: str = "1"):
    """Weather agent using Google Generative AI directly."""
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
        prompt = f"""You are an expert weather forecaster who speaks in puns.

User location: {location}
Current weather: {weather}
User question: {user_input}

Provide a punny weather response with lots of weather-related puns:"""
        
        # Get response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"API call failed: {e}")
        return weather_agent_mock(user_input, user_id)

def weather_agent_mock(user_input: str, user_id: str = "1"):
    """Mock weather agent with puns (fallback)."""
    location = get_user_location(user_id)
    weather = get_weather_for_location(location)
    
    if "weather" in user_input.lower():
        return f"Well, well, well! The weather in {location} is absolutely 'sun-sational'! {weather} I'd say it's a 'ray-diant' day for some outdoor fun!"
    elif "thank" in user_input.lower():
        return f"You're 'thunder-fully' welcome! It's always a 'breeze' to help you stay 'current' with the weather in {location}!"
    else:
        return f"I'm here to help with weather forecasts for {location}! Ask me about the weather!"

# Test the agent
if __name__ == "__main__":
    print("Weather Agent - Testing Google Generative AI")
    print("=" * 50)
    
    # Test API connection
    api_works = test_google_genai()
    
    print("\n" + "=" * 50)
    
    if api_works:
        print("Using Google Generative AI")
        print("=" * 50)
        
        response1 = weather_agent_with_genai("what is the weather outside?", "1")
        print("Q: What is the weather outside?")
        print(f"A: {response1}")
        print()
        
        response2 = weather_agent_with_genai("thank you!", "1")
        print("Q: Thank you!")
        print(f"A: {response2}")
        
    else:
        print("Using Mock Version (API not available)")
        print("=" * 50)
        
        response1 = weather_agent_mock("what is the weather outside?", "1")
        print("Q: What is the weather outside?")
        print(f"A: {response1}")
        print()
        
        response2 = weather_agent_mock("thank you!", "1")
        print("Q: Thank you!")
        print(f"A: {response2}")