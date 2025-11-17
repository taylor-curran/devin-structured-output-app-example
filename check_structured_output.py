#!/usr/bin/env python3
import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def check_structured_output(session_id):
    """Check if a session has structured output"""
    api_key = os.getenv("DEVIN_API_KEY")
    if not api_key:
        raise ValueError("DEVIN_API_KEY not found in .env file")
    
    # Handle full URL or just ID
    if "devin.ai/sessions/" in session_id:
        session_id = session_id.split("/")[-1]
    
    # Add devin- prefix if missing
    if not session_id.startswith("devin-"):
        session_id = f"devin-{session_id}"
    
    response = requests.get(
        f"https://api.devin.ai/v1/sessions/{session_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    data = response.json()
    
    print(f"Session: {session_id}")
    print(f"Status: {data.get('status', 'unknown')}")
    print("-" * 50)
    
    if 'structured_output' in data and data['structured_output']:
        print("✅ Has structured output:")
        try:
            parsed = json.loads(data['structured_output'])
            print(json.dumps(parsed, indent=2))
        except:
            print(data['structured_output'])
    else:
        print("❌ No structured output found")
    

if __name__ == "__main__":
    # Default to the session you provided
    session = sys.argv[1] if len(sys.argv) > 1 else "https://app.devin.ai/sessions/f06264f43bb94899942e3cf931b5ceae"
    check_structured_output(session)
