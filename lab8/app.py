import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY environment variable not found.")
    print("Please make sure you have a .env file with:")
    print("GROQ_API_KEY=your_actual_api_key_here")
    print("Note: You can get a free API key from https://console.groq.com/")
    exit(1)

# Initialize the Groq client
client = Groq(api_key=api_key)

def main():
    print("Welcome to the Llama 3 Chat Application!")
    print("Powered by Groq's super-fast infrastructure.")
    print("Type 'quit' to exit.")
    print("-" * 50)
    
    # Store chat history locally to give the AI memory of the conversation
    chat_history = [
        {
            "role": "system",
            "content": "You are a helpful, smart, and concise assistant."
        }
    ]
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        # Add user message to history
        chat_history.append({"role": "user", "content": user_input})
        
        try:
            # Send message and get response using Llama 3 8B model
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant", # You can also change this to "llama3-70b-8192"
                messages=chat_history,
                temperature=0.7,
                max_tokens=1024,
            )
            
            response_text = completion.choices[0].message.content
            print(f"\nLlama 3: {response_text}")
            
            # Add assistant response to history so it Remembers context
            chat_history.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
