import os 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

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

# DEFINNIG SCHEMA FOR JSON OUTPUT
class TicketInfo(BaseModel):
    name: str
    product: str
    issue: str
    contact_number: int
    email_id: str

Schema = TicketInfo.model_json_schema()
response_format = {
    'type': 'json_object',
    'schema': Schema
}
system_prompt = f"""
You are a helpful assistant that extracts information from customer complaint emails and provides it in this {Schema} JSON format.
"""

message_system = {
    "role": "system",
    "content": system_prompt
}


text = "Hello My name is Akshit Jain and I Recently Purchased an Iphone from your store in Delhi and I am facing some issues with the device. The screen flickers and the battery drains quickly. I would like to request a replacement or a refund for the product. Please let me know the process for returning the device and getting a new one or a refund. Thank you. My contact numbetr is 9350558221 and my email id is akshitjain@gmail.com "
prompt = f"""
This is a customer complaint email: "{text}". Please extract the following information from the email and provide it in JSON format:
"""

message = {
    "role": role,
    "content": prompt
}
messages = [message_system, message]

# Create the completion request
response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

# Cleaned up the print statement to output only the model's text response
print("\n--- LLM Response ---")
print(response.choices[0].message.content)
answer = response.choices[0].message.content




#How to Read Json

import json

raw_json = answer
data_file = json.loads(raw_json)
ticket_info = TicketInfo(**data_file)
print("\n--- Parsed Ticket Info ---\n")
print(ticket_info.name)
print(ticket_info.product)
print(ticket_info.issue)
print(ticket_info.contact_number)
print(ticket_info.email_id)
