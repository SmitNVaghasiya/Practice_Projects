from crewai import Agent, Task, Crew
import ollama

# Define an AI agent
agent = Agent(
    name="DeepSeek AI",
    role="General Assistant",
    goal="Answer user queries efficiently",
    backstory="An AI assistant trained to provide accurate and helpful responses.",
    allow_delegation=False
)

# Define a task for the agent
task = Task(
    description="Chat with the user and provide responses.",
    expected_output="A helpful AI-generated response to user queries.",
    agent=agent,
    function=lambda: ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": input('Ask something: ')}])['message']['content']
)

# Create a crew
crew = Crew(agents=[agent], tasks=[task])

# Run the AI agent
result = crew.kickoff()
print("\nAI Response:", result)
