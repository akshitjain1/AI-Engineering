import os 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# Initialize the Groq client
client = Groq(api_key=my_api_key)

# FIXED: Updated to an active production model ID
model = "openai/gpt-oss-20b"

role = "user"

prompt = "Hii, Suggest me a name for my food company, Name should be in one word"

#SYSTEM
message_system = {
    "role": "system",
    "content": "You are a brand manager who suggest name for my food company, Name should be in one word"
}
message = {
    
    "role": role,
    "content": prompt
}
messages = [message_system, message]

# Create the completion request
#TEMPERATURE by default is 0.7, you can change it to any value between 0 and 2
response = client.chat.completions.create(model=model, messages=messages, temperature=1)

# Cleaned up the print statement to output only the model's text response
print("\n--- LLM Response ---")
print(response.choices[0].message.content)
