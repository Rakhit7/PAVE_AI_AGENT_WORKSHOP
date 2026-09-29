"""
Multi-Agent Syllabus Workflow — improved version
Planner -> Worker -> Supervisor pipeline using the Gemini API (google-genai SDK).

Improvements over the original workshop skeleton:
- Retry with exponential backoff around every API call
- Typed, named wrapper functions per agent (run_planner / run_worker / run_supervisor)
- Supervisor output is typed structured output (Pydantic model + response_schema)
  instead of free-text string matching on "DECISION: APPROVED"
"""

from __future__ import annotations

import time
from enum import Enum

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

load_dotenv()  # reads GEMINI_API_KEY from a local .env file, if present

client = genai.Client()  # picks up GEMINI_API_KEY from the environment
MODEL = "gemini-3.8-flash"
MAX_RETRIES = 3


# ---------------------------------------------------------------------------
# Typed structured output for the supervisor's decision
# ---------------------------------------------------------------------------

class Decision(str, Enum):
    APPROVED = "APPROVED"
    REVISE = "REVISE"


class SupervisorReview(BaseModel):
    comments: str
    decision: Decision


# ---------------------------------------------------------------------------
# Low-level call helpers (retry + backoff)
# ---------------------------------------------------------------------------

def call_agent(system_prompt: str, user_input: str, max_retries: int = MAX_RETRIES) -> str:
    pass


def call_supervisor(system_prompt: str, user_input: str, max_retries: int = MAX_RETRIES) -> SupervisorReview:
    pass


# ---------------------------------------------------------------------------
# Agent prompts
# ---------------------------------------------------------------------------

PLANNER_PROMPT = """You are a planning agent. Given a workshop topic,
produce a 3-day outline only: day titles and 3-4 bullet topics per day.
Do not write full content. Output as plain structured text."""

WORKER_PROMPT = """You are a content-writing agent. Given a workshop
outline, write full session content for each day: objectives, a short
explanation for each bullet topic, and one activity per day. Follow the
outline exactly — do not add or remove topics."""

SUPERVISOR_PROMPT = """You are a supervisor agent. Compare the DRAFT
against the OUTLINE it was supposed to follow. Check: does every outline
topic appear in the draft? Is each day's content substantive enough for
a real session? Write your findings as the 'comments' field, and set
'decision' to APPROVED if the draft is ready to send to a manager, or
REVISE if it needs another pass."""


# ---------------------------------------------------------------------------
# Typed per-agent wrapper functions
# ---------------------------------------------------------------------------

def run_planner(topic: str) -> str:
    pass

def run_worker(outline: str) -> str:
    pass


def run_supervisor(outline: str, draft: str) -> SupervisorReview:
    pass


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    topic = "Generative AI for Classroom Teachers"

    outline = run_planner(topic)
    print("=== PLANNER OUTPUT ===\n", outline)

    draft = run_worker(outline)
    print("\n=== WORKER OUTPUT ===\n", draft)

    review = run_supervisor(outline, draft)
    print("\n=== SUPERVISOR OUTPUT ===")
    print(review.comments)

    match review.decision:
        case Decision.APPROVED:
            print("\n>> Ready to email to manager.")
        case Decision.REVISE:
            print("\n>> Sent back for revision.")
            print("   (Extension: loop the worker again with the supervisor's comments as new input.)")


if __name__ == "__main__":
    main()