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

prompt = "How many data types are there in DSA?"

message = {
    "role": role,
    "content": prompt
}
messages = [message]

# Create the completion request
response = client.chat.completions.create(model=model, messages=messages)

# Cleaned up the print statement to output only the model's text response
print("\n--- LLM Response ---")
print(response.choices[0].message.content)
