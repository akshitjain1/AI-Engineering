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

model = "openai/gpt-oss-20b"
role = "user"

prompt1 = "Hii"
prompt2 = "Expalain Time Travel in Detail"
prompt3 = "Write a 1000 word essay on machinne learning"

#Convert into a list of prompts
prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
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
    response = client.chat.completions.create(model=model, messages=messages, temperature=1, max_tokens=500)
    usage = response.usage
    print(f"Prompt: {prompt} --> Tokens Used: {usage.total_tokens}, Prompt Tokens: {usage.prompt_tokens}, Completion Tokens: {usage.completion_tokens}, Finish Reason: {response.choices[0].finish_reason}")


