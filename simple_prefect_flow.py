#!/usr/bin/env python3
"""
Simple local Prefect flow for Checkmarx vulnerability detection and Devin session creation.
"""
import os
import time
import json
import requests
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from prefect import flow, task
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

api_key = os.getenv("DEVIN_API_KEY")
if not api_key:
    raise ValueError("DEVIN_API_KEY not found in .env file")

headers = {"Authorization": f"Bearer {api_key}"}


@task(name="Check Checkmarx API", log_prints=True)
def check_checkmarx_api() -> List[Dict[str, Any]]:
    """Mock the Checkmarx API to return vulnerabilities."""
    print("🔍 Checking Checkmarx API for vulnerabilities...")
    
    # Simulate API delay
    time.sleep(2)
    
    # Mock vulnerability data (simplified)
    vulnerabilities = [
        {
            "id": "CX-SQL-001",
            "type": "SQL Injection",
            "severity": "High",
            "file": "/api/users.py",
            "line": 45,
            "description": "User input is not properly sanitized before being used in SQL query"
        },
        {
            "id": "CX-XSS-002", 
            "type": "Cross-Site Scripting (XSS)",
            "severity": "Medium",
            "file": "/frontend/components/UserProfile.tsx",
            "line": 78,
            "description": "User-controlled data is rendered without proper encoding"
        },
        {
            "id": "CX-PATH-003",
            "type": "Path Traversal",
            "severity": "High",
            "file": "/api/files.py",
            "line": 23,
            "description": "File path constructed from user input without validation"
        },
    ]
    
    print(f"✅ Found {len(vulnerabilities)} vulnerabilities")
    return vulnerabilities


@task(name="Create Orchestrator Session", log_prints=True)
def create_orchestrator_session(vulnerabilities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create the main orchestrator Devin session."""
    
    vulnerability_summary = "\n".join([
        f"- {v['id']}: {v['type']} ({v['severity']})"
        for v in vulnerabilities
    ])
    
    prompt = f"""
    Orchestrate vulnerability remediation for these issues:
    
    {vulnerability_summary}
    
    Track progress with this structured output:
    {{
      "status": "initializing",
      "total_vulnerabilities": {len(vulnerabilities)},
      "high_severity": {len([v for v in vulnerabilities if v['severity'] == 'High'])},
      "remediation_progress": 0
    }}
    """
    
    print("Creating orchestrator session...")
    response = requests.post(
        "https://api.devin.ai/v1/sessions",
        json={"prompt": prompt, "title": f"Vulnerability Orchestrator - {datetime.now().strftime('%H:%M')}"},
        headers=headers
    )
    response.raise_for_status()
    result = response.json()
    
    print(f"✅ Orchestrator session created: {result['url']}")
    return result


@task(name="Create Fix Session", log_prints=True)
def create_vulnerability_fix_session(vulnerability: Dict[str, Any]) -> Dict[str, Any]:
    """Create a Devin session to fix a specific vulnerability."""
    
    prompt = f"""
    Fix this security vulnerability:
    
    **ID**: {vulnerability['id']}
    **Type**: {vulnerability['type']} 
    **Severity**: {vulnerability['severity']}
    **File**: {vulnerability['file']}
    **Line**: {vulnerability['line']}
    
    {vulnerability['description']}
    
    Update this structured output:
    {{
      "vulnerability_id": "{vulnerability['id']}",
      "status": "fixing",
      "fixed": false
    }}
    """
    
    print(f"Creating fix session for {vulnerability['id']}...")
    response = requests.post(
        "https://api.devin.ai/v1/sessions",
        json={"prompt": prompt, "title": f"Fix {vulnerability['id']}"},
        headers=headers
    )
    response.raise_for_status()
    result = response.json()
    
    print(f"✅ Fix session created for {vulnerability['id']}: {result['url']}")
    return result


@flow(name="Checkmarx Vulnerability Remediation", log_prints=True)
def vulnerability_remediation_flow():
    """
    Main Prefect flow to check for vulnerabilities and create Devin sessions.
    Running in local mode without Prefect server.
    """
    print("🚀 Starting Checkmarx vulnerability remediation flow")
    
    # Step 1: Check for vulnerabilities
    vulnerabilities = check_checkmarx_api()
    
    if not vulnerabilities:
        print("✨ No vulnerabilities found!")
        return {"status": "no_vulnerabilities", "sessions_created": 0}
    
    # Step 2: Create orchestrator session
    orchestrator = create_orchestrator_session(vulnerabilities)
    
    # Step 3: Create fix sessions for each vulnerability
    fix_session_results = []
    for vuln in vulnerabilities:
        session = create_vulnerability_fix_session(vuln)
        fix_session_results.append(session)
    
    # Step 4: Generate summary
    summary = {
        "orchestrator_session": {
            "id": orchestrator["session_id"],
            "url": orchestrator["url"]
        },
        "fix_sessions": [
            {
                "id": session["session_id"],
                "url": session["url"]
            }
            for session in fix_session_results
        ],
        "total_sessions_created": len(fix_session_results) + 1,
        "timestamp": datetime.now().isoformat()
    }
    
    print("✅ Flow completed successfully!")
    print(f"📋 Summary: {json.dumps(summary, indent=2)}")
    
    return summary


if __name__ == "__main__":
    # Disable Prefect's attempt to connect to cloud/server
    os.environ["PREFECT_API_URL"] = ""
    
    # Run the flow directly
    print("\n" + "="*60)
    print("🎉 RUNNING PREFECT FLOW LOCALLY")
    print("="*60 + "\n")
    
    result = vulnerability_remediation_flow()
    
    print("\n" + "="*60)
    print("🎉 VULNERABILITY REMEDIATION FLOW COMPLETE")
    print("="*60)
    
    if result.get("status") == "no_vulnerabilities":
        print("No vulnerabilities found - nothing to fix!")
    else:
        print(f"\n📊 Sessions Created: {result.get('total_sessions_created', 0)}")
        print(f"\n🎯 Orchestrator Session:")
        print(f"   {result['orchestrator_session']['url']}")
        
        print(f"\n🔧 Fix Sessions:")
        for session in result['fix_sessions']:
            print(f"   {session['url']}")
