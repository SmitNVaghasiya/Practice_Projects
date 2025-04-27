import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# api_key = os.getenv("GROQ_API_KEY"),
api_key = os.environ.get('API_KEY')

print(api_key)
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

stream = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a highly experienced car expert with a lifetime of hands-on work in the automotive industry. You possess in-depth knowledge of every type of car, from classic vintage models to the latest high-performance supercars and electric vehicles. Your expertise extends to all aspects of automobiles, including engines, transmissions, suspension systems, electronics, aerodynamics, and cutting-edge automotive technologies. You can provide precise technical insights, expert recommendations, and troubleshooting advice on any car-related topic with absolute accuracy."
        },
        {
            "role": "user",
            "content": "what types of cars are best at aerodynamics.",
        }
    ],

    # The language model which will generate the completion.
    model="llama-3.3-70b-versatile",

    temperature=0.5,

    max_completion_tokens=1024,

    top_p=1,

    stop=None,

    # If set, partial message deltas will be sent.
    stream=True,
)

# Print the incremental deltas returned by the LLM.
for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
