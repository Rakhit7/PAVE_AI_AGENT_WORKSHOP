import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Check that a .env file exists in this "
        "folder and contains a line like: GEMINI_API_KEY=your-key-here"
    )
 
client = genai.Client(api_key=api_key)
MODEL = "gemini-3.8-flash"

response = client.models.generate_content(
    model=MODEL,
    contents="Say hello in one sentence."
)
print(response.text)

def call_agent(system_prompt: str, user_input: str) -> str:
    """One call = one agent 'turn'. Each agent has its own system prompt,
    which is what makes it behave like a distinct role rather than one
    generic assistant."""
    response = client.models.generate_content(
        model=MODEL,
        contents=f"{system_prompt}\n\n---\n\n{user_input}",
    )
    return response.text

def run_pipeline(topic: str):
    # ---- 1. Planner agent ----
    planner_prompt = """You are a planning agent. Given a workshop topic,
produce a 3-day outline only: day titles and 3-4 bullet topics per day.
Do not write full content. Output as plain structured text."""
 
    outline = call_agent(planner_prompt, f"Workshop topic: {topic}")
    print("=== PLANNER OUTPUT ===\n", outline, "\n")
 
    # ---- 2. Worker agent ----
    worker_prompt = """You are a content-writing agent. Given a workshop
outline, write full session content for each day: objectives, a short
explanation for each bullet topic, and one activity per day. Follow the
outline exactly -- do not add or remove topics."""
 
    draft = call_agent(worker_prompt, f"Outline:\n{outline}")
    print("=== WORKER OUTPUT ===\n", draft, "\n")
 
    # ---- 3. Supervisor agent ----
    supervisor_prompt = """You are a supervisor agent. Compare the DRAFT
against the OUTLINE it was supposed to follow. Check: does every outline
topic appear in the draft? Is each day's content substantive enough for
a real session? Write your comments, then end with exactly one line:
'DECISION: APPROVED' or 'DECISION: REVISE'."""
 
    review_input = f"OUTLINE:\n{outline}\n\nDRAFT:\n{draft}"
    review = call_agent(supervisor_prompt, review_input)
    print("=== SUPERVISOR OUTPUT ===\n", review, "\n")
 
    # ---- Decision handling ----
    if "DECISION: APPROVED" in review:
        print(">> Ready to email to manager.")
    else:
        print(">> Sent back for revision.")
        print("   (Extension: loop the worker again with the supervisor's")
        print("   comments as new input -- see Section 5.5 of the guide.)")
 
    return outline, draft, review
 
 
if __name__ == "__main__":
    workshop_topic = "Generative AI for Classroom Teachers"
    run_pipeline(workshop_topic)