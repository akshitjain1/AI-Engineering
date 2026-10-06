import os
import re
from time import sleep
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# Initialize the Groq client
client = Groq(api_key=my_api_key)

# gpt-oss models emit native tool calls (400 tool_use_failed) instead of text Actions,
# so use a model that follows text-based ReAct instructions
model = "qwen/qwen3.8-27b"


# TOOLS or APIs Functions

def get_product_price(product_name):
    # Simulated function to get product price
    prices = {
        "apple": 150,
        "banana": 80,
        "orange": 130
    }
    return prices.get(product_name.lower(), "Product not found")

def calculator(expression):
    try:
        return eval(expression)
    except:
        return "Calculation error"

tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}

system_prompt = """You are a support assistant at a WholeSale Grocery Store.

You have these tools:

get_product_price(product_name)
calculator(expression)

IMPORTANT:
Call tools exactly like these examples:

Action: get_product_price("apple")
Action: calculator("2 + 2")

Never write:
get_product_price(product_name="apple")

Never write:
calculator(expression="2 + 2")

Follow these rules:
1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer and do not call any more tools.

Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer
"""

def run_agent(question):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    for step in range(5):  # Limit the number of steps to avoid infinite loops
        print("\n------------------")
        print("STEP", step + 1)
        print("------------------")

        response = client.chat.completions.create(model=model, messages=messages, temperature=0)
        answer = response.choices[0].message.content
        print(answer)

        # Find the Action (tolerates leading spaces and markdown like **Action:**)
        match = re.search(r"Action:\**\s*(\w+)\((.*?)\)", answer)

        if match:
            tool_name = match.group(1)
            # Remove surrounding whitespace and quotes so 'apple' becomes apple
            tool_input = match.group(2).strip().strip("'\"")

            # Run the tool
            if tool_name in tools:
                observation = tools[tool_name](tool_input)
            else:
                observation = "Tool not found"

            print("Observation:", observation)

            # Add LLM response to memory, then give the tool result back to the LLM
            messages.append({"role": "assistant", "content": answer})
            messages.append({"role": "user", "content": "Observation: " + str(observation)})
            sleep(5)  # Stay under Groq rate limits

        elif "Final Answer:" in answer:
            # Agent has finished and provided a final answer
            break

        else:
            print("No action found in the model's response.")
            break


prompt = """I have 500 Rupees. What is the price of 3 apples and 2 bananas?
Can you calculate the total cost and tell me how much money I will have left after buying them?"""

run_agent(prompt)
