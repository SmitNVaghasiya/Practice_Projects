import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key = GROQ_API_KEY)

def prompt_starter(start_prompt):
    first_response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": start_prompt
            }
        ],
        model = "llama-3.1-8b-instant"
    )
    return first_response.choices[0].message.content

def helper(query):
    response = client.chat.completions.create(
        messages=[
            {
                'role': "user",
                'content' : query,
            }
        ],
        model = "deepseek-r1-distill-llama-70b"
    )
    return response.choices[0].message.content

start_prompt = "You are user friendly ai agent so greet user wormly and how can i help or in similar manner in half line or less content."
first_response = prompt_starter(start_prompt)
print(first_response)

while True:
    query = str(input(""))
    if query == "exit":
        break
    response = helper(query)
    print(response)