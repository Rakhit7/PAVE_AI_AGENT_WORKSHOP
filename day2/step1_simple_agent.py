"""
STEP 1 - The simplest possible agent.

An agent needs only four things:
  1. a GOAL         (the task the user gives it)
  2. INSTRUCTIONS   (the system prompt: its job description)
  3. a MODEL        (Gemini)
  4. an OUTPUT      (the finished result)

This agent receives a task, writes out its plan (reasoning), then produces
the final output on its own. It has no tools, no memory and no loop yet 


Run:
    python step1_simple_agent.py
    python step1_simple_agent.py "Write 3 icebreaker questions for a teacher workshop"
"""

import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found. Copy .env.example to .env and add your key.")

client = genai.Client(api_key=api_key)
MODEL = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = """You are a task agent. You receive a task and complete it on your own.

Always reply in exactly this format:
REASONING: <2-4 short lines: what the task needs and your plan>
FINAL OUTPUT: <the finished result>"""


def run_agent(task):
    response = client.models.generate_content(
        model=MODEL,
        contents=task,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    text = response.text

    # Split the reply into the plan and the finished work
    if "FINAL OUTPUT:" in text:
        reasoning, output = text.split("FINAL OUTPUT:", 1)
        reasoning = reasoning.replace("REASONING:", "").strip()
    else:
        reasoning, output = "(the model did not follow the format)", text
    return reasoning, output.strip()


if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) or (
        "Write a 5-question quick quiz on Python variables for Grade 9 students."
    )
    print(f"TASK: {task}\n")
    reasoning, output = run_agent(task)
    print("--- AGENT'S PLAN ---")
    print(reasoning)
    print("\n--- AGENT'S OUTPUT ---")
    print(output)
