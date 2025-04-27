import os
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-proj-1111"

llm = ChatOpenAI(
    model="llama3.1:8b",
    base_url="http://localhost:11434/llama3.1:8b"
)

info_agent = Agent(
    role="Information Agent",
    goal="Give compelling information about a certain topic",
    backstory="""
        You love to know information.  People love and hate you for it.  You win most of the
        quizzes at your local pub.
    """,
    llm=llm
)

task1 = Task(
    description="Tell me all about the box jellyfish.",
    expected_output="Give me a quick summary and then also give me 7 bullet points describing it.",
    agent=info_agent
)

crew = Crew(
    agents=[info_agent],
    tasks=[task1],
    verbose=True
)

result = crew.kickoff()

print("############")
print(result)


# import os
# import ollama
# from crewai import Agent, Task, Crew
# from langchain_core.language_models import LLM
# from langchain_core.callbacks.manager import CallbackManagerForLLMRun

# # Custom wrapper for Ollama to make it compatible with CrewAI
# class OllamaLLM(LLM):
#     model: str = "deepseek-r1:8b"

#     def _call(self, prompt: str, stop=None, run_manager: CallbackManagerForLLMRun = None):
#         response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
#         return response['message']['content']

#     @property
#     def _llm_type(self) -> str:
#         return "ollama"

# # Create an instance of the custom Ollama LLM
# llm = OllamaLLM()

# # Define an AI agent
# info_agent = Agent(
#     role="Information Agent",
#     goal="Give compelling information about a certain topic",
#     backstory="""
#         You love to know information. People love and hate you for it. 
#         You win most of the quizzes at your local pub.
#     """,
#     llm=llm  # Pass the LangChain-compatible wrapper
# )

# # Define a task for the agent
# task1 = Task(
#     description="Tell me all about the box jellyfish.",
#     expected_output="Give me a quick summary and then also give me 7 bullet points describing it.",
#     agent=info_agent
# )

# # Create a crew
# crew = Crew(
#     agents=[info_agent],
#     tasks=[task1],
#     verbose=True  # Boolean instead of integer
# )

# # Run the AI agent
# result = crew.kickoff()

# print("############")
# print(result)
