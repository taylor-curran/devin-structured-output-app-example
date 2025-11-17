#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_devin_session(prompt, **kwargs):
    api_key = os.getenv('DEVIN_API_KEY')
    if not api_key:
        raise ValueError("DEVIN_API_KEY not found in .env file")
    
    body = {"prompt": prompt, **kwargs}
    
    response = requests.post(
        "https://api.devin.ai/v1/sessions",
        json=body,
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    result = create_devin_session(
        "Review the pull request at https://github.com/example/repo/pull/123",
        idempotent=True
    )
    print(f"Session: {result['url']}")
