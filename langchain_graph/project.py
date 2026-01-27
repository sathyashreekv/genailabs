import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict
from langgraph.graph import StateGraph, END

load_dotenv()
class MoodState(TypedDict):
    """A simple state object to hold user input and mood."""
    user_input: str
    mood: str
    response: str
    suggestions: str

# Initialize model with API key from environment
api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)

def classify_mood(state: MoodState) -> dict:
    try:
        response = model.invoke(f"Is the user happy or sad? User said: {state['user_input']}")
        mood_detected = response.content.lower()
        return {"mood": mood_detected}
    except Exception as e:
        return {"mood": "error"}

def respond_to_mood(state: MoodState) -> dict:
    try:
        response = model.invoke(f"Generate an empathetic response to someone who is feeling: {state['mood']}. User said: {state['user_input']}")
        return {"response": response.content}
    except Exception as e:
        return {"response": "I understand how you're feeling."}

def generate_suggestions(state: MoodState) -> dict:
    try:
        response = model.invoke(f"Provide 3-4 helpful suggestions for someone who is feeling: {state['mood']}. Format as bullet points.")
        return {"suggestions": response.content}
    except Exception as e:
        return {"suggestions": "• Take some time for self-care\n• Reach out to someone you trust"}

# Build the graph
workflow = StateGraph(MoodState)
workflow.add_node("classify", classify_mood)
workflow.add_node("respond", respond_to_mood)
workflow.add_node("suggest", generate_suggestions)

workflow.set_entry_point("classify")
workflow.add_edge("classify", "respond")
workflow.add_edge("respond", "suggest")
workflow.add_edge("suggest", END)

app = workflow.compile()

if __name__ == "__main__":
    user_input = input("How are you feeling today? ")
    result = app.invoke({"user_input": user_input, "mood": "", "response": "", "suggestions": ""})
    print(f"\nMood detected: {result['mood']}")
    print(f"Response: {result['response']}")
    print(f"\nSuggestions:\n{result['suggestions']}")



