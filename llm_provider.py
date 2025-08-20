import os
from langchain_openai import ChatOpenAI

# Initialize the LLM provider with error handling
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    ACTIVE_LLM = ChatOpenAI(
        model="gpt-4o-mini",  # You can change this to gpt-4 or other models
        temperature=0.7,
        api_key=api_key
    )
except Exception as e:
    # Create a dummy LLM for demo purposes
    class DummyLLM:
        def __init__(self):
            self.model = "demo-mode"
            self.temperature = 0.7
        
        def invoke(self, *args, **kwargs):
            return "Demo mode: This would be an AI response in the full version."
    
    ACTIVE_LLM = DummyLLM()
