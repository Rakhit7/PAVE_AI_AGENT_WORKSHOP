"""
MY FIRST MULTI-AGENT TEAM (Google ADK)

Three specialist agents work one after another.
Each agent does ONE job and saves its answer under a name (output_key).
The next agents can then use that answer by writing {name} in their instruction.

Setup:  pip install google-adk python-dotenv
        make a file called .env containing:  GEMINI_API_KEY=your_key_here
Run:    python lesson_team.py
"""

import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import InMemoryRunner

load_dotenv()

MODEL = "gemini-3.5-flash-lite"

# AGENT 1: reads the topic, writes the explanation
explainer = Agent(
    name="explainer",
    model=MODEL,
    instruction=(
        "You are a teacher. The user gives you a topic. "
        "Explain it to Grade 9 students in short paragraphs with one everyday example."
    ),
    output_key="explanation",   # saves this agent's answer under the name 'explanation'
)

# AGENT 2: uses {explanation} written by agent 1
activity_designer = Agent(
    name="activity_designer",
    model=MODEL,
    instruction=(
        "Design one 15-minute classroom activity for this lesson.\n"
        "EXPLANATION WRITTEN BY THE PREVIOUS AGENT:\n{explanation}\n\n"
        "Write: a goal, materials, and numbered steps."
    ),
    output_key="activity",
)

# AGENT 3: also uses {explanation}
quiz_writer = Agent(
    name="quiz_writer",
    model=MODEL,
    instruction=(
        "Write a 5-question quiz with an answer key, based on this explanation:\n"
        "{explanation}"
    ),
    output_key="quiz",
)

# THE TEAM: run the three agents in this order
root_agent = SequentialAgent(
    name="lesson_team",
    sub_agents=[explainer, activity_designer, quiz_writer],
)


async def main():
    runner = InMemoryRunner(agent=root_agent, app_name="lesson_app")
    await runner.run_debug("Python for-loops")   # <- change the topic here

asyncio.run(main())