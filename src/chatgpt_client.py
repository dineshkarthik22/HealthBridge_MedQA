import os
from openai import OpenAI
from typing import List, Dict, Optional

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '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')  # Set this via environment variable for security

# System prompt that can be modified as needed
SYSTEM_PROMPT = """
You are a helpful medical assistant that provides accurate and informative responses to medical questions.
You always cite your sources and maintain a professional tone.
"""

class ChatGPTClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialize the ChatGPT client.
        
        Args:
            api_key: OpenAI API key. If not provided, will use OPENAI_API_KEY environment variable
            model: The GPT model to use (default: gpt-4)
        """
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided either through initialization or environment variable")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.system_prompt = SYSTEM_PROMPT

    def set_system_prompt(self, new_prompt: str) -> None:
        """
        Update the system prompt used for conversations.
        
        Args:
            new_prompt: The new system prompt to use
        """
        self.system_prompt = new_prompt

    def get_response(self, user_message: str, temperature: float = 0.7) -> str:
        """
        Get a response from ChatGPT for a given user message.
        
        Args:
            user_message: The user's input message
            temperature: Controls randomness in the response (0.0 to 1.0)
            
        Returns:
            str: The model's response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error getting response from ChatGPT: {str(e)}")

    def get_conversation_response(self, conversation_history: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        Get a response from ChatGPT given a conversation history.
        
        Args:
            conversation_history: List of message dictionaries with 'role' and 'content' keys
            temperature: Controls randomness in the response (0.0 to 1.0)
            
        Returns:
            str: The model's response
        """
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(conversation_history)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error getting response from ChatGPT: {str(e)}")

# Example usage:
if __name__ == "__main__":
    # Initialize the client
    chatgpt = ChatGPTClient()  # Make sure OPENAI_API_KEY environment variable is set
    
    # Get a simple response
    response = chatgpt.get_response("What are the common symptoms of the flu?")
    print(response)
    
    # Update system prompt if needed
    chatgpt.set_system_prompt("You are a medical expert specializing in infectious diseases.")
    
    # Use conversation history
    conversation = [
        {"role": "user", "content": "What are the risk factors for diabetes?"},
        {"role": "assistant", "content": "The main risk factors include obesity, family history..."},
        {"role": "user", "content": "How can these risks be mitigated?"}
    ]
    response = chatgpt.get_conversation_response(conversation)
    print(response)
