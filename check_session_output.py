#!/usr/bin/env python3
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# The session ID from the previous run
SESSION_ID = "a5b0e4d8a71743269ef635c733a130d1"

api_key = os.getenv("DEVIN_API_KEY")
if not api_key:
    raise ValueError("DEVIN_API_KEY not found in .env file")

headers = {"Authorization": f"Bearer {api_key}"}

print(f"Checking session: {SESSION_ID}")
print(f"URL: https://app.devin.ai/sessions/{SESSION_ID}\n")

try:
    response = requests.get(
        f"https://api.devin.ai/v1/sessions/{SESSION_ID}",
        headers=headers,
        timeout=10
    )
    response.raise_for_status()
    data = response.json()
    
    print(f"Session Status: {data.get('status', 'unknown')}")
    print(f"Session State: {data.get('state', 'unknown')}\n")
    
    if data.get("structured_output"):
        print("✅ Structured Output Found!")
        print("-" * 50)
        output = data["structured_output"]
        # Handle both string and dict responses
        if isinstance(output, str):
            try:
                output = json.loads(output)
            except json.JSONDecodeError:
                print("Raw output (not valid JSON):")
                print(output)
        
        if isinstance(output, dict):
            print(json.dumps(output, indent=2))
        else:
            print(output)
    else:
        print("❌ No structured output available yet")
        print("The session might still be processing the task")
        
except requests.exceptions.RequestException as e:
    print(f"Error checking session: {e}")
