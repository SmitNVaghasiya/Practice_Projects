from crewai import Agent, Task, Crew
from langchain_community.llms.ollama import Ollama  # Correct import for Ollama
from langchain.memory import ConversationBufferMemory

# Initialize LLM (local instance) using Ollama for local models
llm = Ollama(model="llama3")

# Memory to retain conversation history (optional)
memory = ConversationBufferMemory(memory_key="chat_history")

# Primary Information Agent
info_agent = Agent(
    role="Information Agent",
    goal="Provide rich, structured, and engaging information.",
    backstory="""
        You are an AI librarian with a vast knowledge of the world. 
        You structure information concisely but with depth, making it engaging and easy to understand.
    """,
    llm=llm,
    memory=memory,
    allow_delegation=False,  # Ensures the agent itself completes the task
    verbose=True  # Enables detailed logging
)

# Additional Agents for Multiple Perspectives
scientist_agent = Agent(
    role="Marine Biologist",
    goal="Provide scientific insights about marine life.",
    backstory="You have studied marine creatures for decades and love explaining their biology.",
    llm=llm
)

historian_agent = Agent(
    role="History Expert",
    goal="Provide historical records and interesting facts about topics.",
    backstory="You are a history buff who enjoys uncovering the past.",
    llm=llm
)

# Task Definition with Detailed Expectations
task1 = Task(
    description="Tell me all about the box jellyfish, including its habitat, venom, and interactions with humans.",
    expected_output="""
        - A short but detailed summary (3-4 sentences)
        - 7 bullet points covering:
          1. Scientific classification
          2. Habitat & distribution
          3. Physical characteristics
          4. Venom effects & dangers
          5. Human interactions & cases
          6. Prevention & first aid measures
          7. Interesting trivia
    """,
    agent=info_agent
)

# Crew Definition with Multiple Agents
crew = Crew(
    agents=[info_agent, scientist_agent, historian_agent],
    tasks=[task1],
    verbose=2
)

# Execute Task
result = crew.kickoff()

# Output Results
print("############")
print(result)
