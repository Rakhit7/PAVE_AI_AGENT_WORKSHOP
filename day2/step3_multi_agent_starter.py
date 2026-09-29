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

# change the model name here
MODEL = "model-of-your-choice"

# ---------------- THE AGENTS (this is the part to study) ----------------

# AGENT 1: reads the topic, writes the explanation
# create the explainer agent here


# AGENT 2: uses {explanation} written by agent 1
# create the activity designer agent here


# AGENT 3: also uses {explanation}
# create the quiz writer agent here

# THE TEAM: run the three agents in this order
# IMPORTANT: create the root agent and run the sequential task here


# paste the main method here