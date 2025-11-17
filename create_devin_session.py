#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def create_devin_session(prompt, **kwargs):
    api_key = os.getenv("DEVIN_API_KEY")
    if not api_key:
        raise ValueError("DEVIN_API_KEY not found in .env file")

    body = {"prompt": prompt, **kwargs}

    response = requests.post(
        "https://api.devin.ai/v1/sessions",
        json=body,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Simple prompt with 2-field structured output
    prompt_with_output = """
    Print hello world in Python. Update this structured output:
    {
      "status": "not started",
      "code_written": false
    }
    """
    
    result = create_devin_session(
        prompt_with_output,
        idempotent=False,
    )
    print(f"Session: {result['url']}")
