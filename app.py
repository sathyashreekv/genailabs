import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY environment variable not found.")
    print("Please make sure you have a .env file with:")
    print("GEMINI_API_KEY=your_actual_api_key_here")
    exit(1)

# Initialize the new Gemini client
client = genai.Client(api_key=api_key)

def main():
    print("Welcome to the Simple Gemini Application!")
    print("Type 'quit' to exit.")
    print("-" * 40)
    
    # Start a chat session using the new SDK
    chat = client.chats.create(model='gemini-2.5-flash')
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        try:
            # Send message and get response
            response = chat.send_message(user_input)
            print(f"Gemini: {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
