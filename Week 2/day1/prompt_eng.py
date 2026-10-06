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

def llm_ans(prompt):
    message = {
        'role' : "user",
        'content' : prompt
    }
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

Bad_prompt = """This is a user complaint:
My laptop is not working and my Girl Friend left me
Classify this"""

def main():
    while(True):
        user_complaint = input("Enter the user complaint: ")
        if user_complaint.lower() == "exit":
            print("Exiting the program.")
            break
        prompt = f""" You are a support assistant at a WholeSale Grocery Store.
        # CONSTRAINTS and TASKS
        You have to classify the Following user complain {user_complaint} into one of the following categories:
        1. Product Quality
        2. Customer Service
        3. Delivery Issues
        4. Billing Disputes
        5. Other
        # OUTPUT FORMAT
        Category: <category_name>
        # EXAMPLES
        User Complaint: "The milk I bought was spoiled."
        Category: Product Quality
        User Complaint: "I was charged twice for my order."
        Category: Billing Disputes
        #FALLBACK
        If the issue is unrelated to the above categories, classify it as "OTHER".

        """
        classification = llm_ans(prompt)
        print(classification)
        break
main()