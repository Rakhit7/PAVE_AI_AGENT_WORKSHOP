"""
An agent is 3 things:  a MODEL (the brain) + INSTRUCTIONS (its job) + TOOLS (what it can do).
A tool is just a normal Python function.

TRY THESE QUESTIONS (and watch which tools the agent calls):

  1. What did Bikash score?
       -> one tool call, then an answer
  2. Who scored higher, Asha or Chandra?
       -> two tool calls. How did the agent know to call the tool twice?
  3. What did Zara score?
       -> the tool returns an error. How does the agent react?
  4. What is the capital of Nepal?
       -> no tool call at all. Why not?
  5. What is the average of Asha, Bikash and Chandra?
       -> three tool calls, but the maths is done by the model.
          Is it always right? (Later lesson: give it a calculator tool.)

EXPERIMENTS WITH THE CODE:

  A. Delete  tools=[get_marks]  and ask question 1 again. What changes?
  B. Change the instruction to "Answer in one word" and ask question 1.
  C. Add a new tool  get_grade(marks: int)  that returns "Pass" if marks >= 40,
     else "Fail". Add it to the tools list, then ask: "Did Bikash pass?"
"""
# Extra set up: pip install google-adk

import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner

load_dotenv()  # reads your API key from the .env file
# change the model name here
MODEL = "model-of-your-choice"

# 1. THE TOOL: a normal Python function.
#    The model can't know our students' marks, so it needs this tool to look them up.
#    The docstring is important: the model reads it to decide when to use the tool.
def get_marks(student_name: str) -> dict:
    """Looks up the marks of one student.

    Args:
        student_name: The student's first name, for example 'Asha'.
    """
    pass


# 2. THE AGENT: model + instructions + tools
# create the root here


# 3. RUN IT
# paste the main method here