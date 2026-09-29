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
    pass

def run_pipeline(topic: str):
    pass
 
 
if __name__ == "__main__":
    workshop_topic = "Generative AI for Classroom Teachers"
    run_pipeline(workshop_topic)