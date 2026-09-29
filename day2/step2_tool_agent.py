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

MODEL = "gemini-3.5-flash-lite"

# 1. THE TOOL: a normal Python function.
#    The model can't know our students' marks, so it needs this tool to look them up.
#    The docstring is important: the model reads it to decide when to use the tool.
def get_marks(student_name: str) -> dict:
    """Looks up the marks of one student.

    Args:
        student_name: The student's first name, for example 'Asha'.
    """
    marks = {"Asha": 78, "Bikash": 64, "Chandra": 91}
    if student_name in marks:
        return {"status": "success", "marks": marks[student_name]}
    return {"status": "error", "message": "Student not found"}


# 2. THE AGENT: model + instructions + tools
root_agent = Agent(
    name="marks_agent",
    model=MODEL,
    instruction="You help teachers. Use the tool to look up marks. Never guess.",
    tools=[get_marks],
)


# 3. RUN IT
async def main():
    question = input("Ask the agent something: ")
    runner = InMemoryRunner(agent=root_agent, app_name="first_app")
    # verbose=True shows each tool call, so you can watch the agent think
    await runner.run_debug(question, verbose=True)


asyncio.run(main())