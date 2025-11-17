#!/usr/bin/env python3
import os
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DEVIN_API_KEY")
if not api_key:
    raise ValueError("DEVIN_API_KEY not found in .env file")

headers = {"Authorization": f"Bearer {api_key}"}


def create_session():
    """Create a session with structured output"""
    prompt = """
    Create a detailed plan for building a simple todo list web application.
    Break it down into clear steps and update this structured output as you develop the plan:
    {
      "project": "Todo List Web App",
      "overview": "Brief description of the project",
      "phases": [
        {
          "phase": "Planning",
          "tasks": ["Define requirements", "Choose tech stack"],
          "duration": "1-2 days"
        }
      ],
      "tech_stack": {
        "frontend": "",
        "backend": "",
        "database": ""
      },
      "milestones": [],
      "risks": [],
      "status": "in_progress"
    }
    """
    
    response = requests.post(
        "https://api.devin.ai/v1/sessions",
        json={"prompt": prompt},
        headers=headers
    )
    response.raise_for_status()
    return response.json()


def wait_for_structured_output(session_id, timeout=1800):
    """Wait for structured output to appear (max 30 minutes)"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(
                f"https://api.devin.ai/v1/sessions/{session_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("structured_output"):
                output = data["structured_output"]
                # Handle both string and dict responses
                if isinstance(output, str):
                    output = json.loads(output)
                return output, data.get("status")
            
            print(".", end="", flush=True)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 504:
                print("T", end="", flush=True)  # Timeout, keep trying
            else:
                raise
        
        time.sleep(5)
    
    return None, "timeout"


if __name__ == "__main__":
    # Create session
    print("Creating session...")
    session = create_session()
    session_id = session["session_id"]
    print(f"Session created: {session['url']}")
    
    # Wait for structured output
    print("Waiting for structured output", end="")
    output, status = wait_for_structured_output(session_id)
    
    if output:
        print(f"\n✅ Got structured output! (status: {status})")
        print(json.dumps(output, indent=2))
    else:
        print(f"\n❌ Timeout waiting for structured output")
