#!/usr/bin/env python3
"""
Scheduled Prefect flow for daily Checkmarx vulnerability detection at 8 AM.
"""
import os
import time
import json
import requests
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from prefect import flow, task, serve
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
    
    # Mock vulnerability data with repositories
    vulnerabilities = [
        {
            "id": "CX-SQL-001",
            "type": "SQL Injection",
            "severity": "High",
            "repository": "backend-api",
            "file": "/api/users.py",
            "line": 45,
            "description": "User input is not properly sanitized before being used in SQL query"
        },
        {
            "id": "CX-XSS-002", 
            "type": "Cross-Site Scripting (XSS)",
            "severity": "Medium",
            "repository": "frontend-app",
            "file": "/frontend/components/UserProfile.tsx",
            "line": 78,
            "description": "User-controlled data is rendered without proper encoding"
        },
        {
            "id": "CX-PATH-003",
            "type": "Path Traversal",
            "severity": "High",
            "repository": "backend-api",
            "file": "/api/files.py",
            "line": 23,
            "description": "File path constructed from user input without validation"
        },
        {
            "id": "CX-CRYPTO-004",
            "type": "Weak Cryptography",
            "severity": "Medium",
            "repository": "auth-service",
            "file": "/auth/password_utils.py",
            "line": 12,
            "description": "MD5 hash used for password storage"
        },
    ]
    
    print(f"✅ Found {len(vulnerabilities)} vulnerabilities")
    return vulnerabilities


@task(name="Create Orchestrator Session", log_prints=True, retries=2)
def create_orchestrator_session(vulnerabilities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create the main orchestrator Devin session."""
    
    # Group vulnerabilities by repository
    repos = {}
    for v in vulnerabilities:
        repo = v.get('repository', 'unknown')
        if repo not in repos:
            repos[repo] = []
        repos[repo].append(v)
    
    vulnerability_summary = ""
    for repo, vulns in repos.items():
        vulnerability_summary += f"\n**Repository: {repo}**\n"
        for v in vulns:
            vulnerability_summary += f"  - {v['id']}: {v['type']} ({v['severity']})\n"
    
    prompt = f"""
    Daily vulnerability scan orchestrator for {datetime.now().strftime('%Y-%m-%d')}.
    
    Orchestrate vulnerability remediation across multiple repositories:
    {vulnerability_summary}
    
    Track progress with this structured output:
    {{
      "scan_date": "{datetime.now().strftime('%Y-%m-%d')}",
      "scan_time": "{datetime.now().strftime('%H:%M')}",
      "status": "initializing",
      "total_vulnerabilities": {len(vulnerabilities)},
      "high_severity": {len([v for v in vulnerabilities if v['severity'] == 'High'])},
      "medium_severity": {len([v for v in vulnerabilities if v['severity'] == 'Medium'])},
      "remediation_progress": 0
    }}
    """
    
    print("Creating orchestrator session...")
    response = requests.post(
        "https://api.devin.ai/v1/sessions",
        json={
            "prompt": prompt, 
            "title": f"Daily Vulnerability Scan - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "tags": ["daily-scan", "automated", "checkmarx"]
        },
        headers=headers
    )
    response.raise_for_status()
    result = response.json()
    
    print(f"✅ Orchestrator session created: {result['url']}")
    return result


@task(name="Create Fix Session", log_prints=True, retries=2)
def create_vulnerability_fix_session(vulnerability: Dict[str, Any], scan_date: str) -> Dict[str, Any]:
    """Create a Devin session to fix a specific vulnerability."""
    
    repository = vulnerability.get('repository', 'unknown')
    
    prompt = f"""
    Fix this security vulnerability found in daily scan on {scan_date}:
    
    **Repository**: {repository}
    **ID**: {vulnerability['id']}
    **Type**: {vulnerability['type']} 
    **Severity**: {vulnerability['severity']}
    **File**: {vulnerability['file']}
    **Line**: {vulnerability['line']}
    
    {vulnerability['description']}
    
    Update this structured output:
    {{
      "scan_date": "{scan_date}",
      "repository": "{repository}",
      "vulnerability_id": "{vulnerability['id']}",
      "status": "fixing",
      "fixed": false,
      "fix_timestamp": null
    }}
    """
    
    print(f"Creating fix session for {vulnerability['id']}...")
    response = requests.post(
        "https://api.devin.ai/v1/sessions",
        json={
            "prompt": prompt, 
            "title": f"[{scan_date}] Fix {vulnerability['id']}",
            "tags": ["vulnerability-fix", "automated", vulnerability['severity'].lower()]
        },
        headers=headers
    )
    response.raise_for_status()
    result = response.json()
    
    print(f"✅ Fix session created for {vulnerability['id']}: {result['url']}")
    return result


@task(name="Send Notification", log_prints=True)
def send_notification(summary: Dict[str, Any]):
    """Send notification about the daily scan results."""
    print("\n" + "="*60)
    print("📧 DAILY VULNERABILITY SCAN NOTIFICATION")
    print("="*60)
    print(f"Date: {summary['scan_date']}")
    print(f"Time: {summary['scan_time']}")
    print(f"Total Sessions Created: {summary['total_sessions_created']}")
    print(f"Vulnerabilities Found: {summary['total_vulnerabilities']}")
    print(f"  - High Severity: {summary['high_severity']}")
    print(f"  - Medium Severity: {summary['medium_severity']}")
    print(f"  - Low Severity: {summary['low_severity']}")
    print("\nSessions have been created and are being processed.")
    print("="*60)
    
    # In production, this could send an email, Slack message, etc.
    # For now, just log the notification


@flow(name="Daily Checkmarx Vulnerability Scan", log_prints=True)
def daily_vulnerability_scan_flow():
    """
    Scheduled Prefect flow that runs daily at 8 AM to check for vulnerabilities.
    """
    scan_date = datetime.now().strftime('%Y-%m-%d')
    print(f"🚀 Starting daily vulnerability scan for {scan_date}")
    
    # Step 1: Check for vulnerabilities
    vulnerabilities = check_checkmarx_api()
    
    if not vulnerabilities:
        print("✨ No vulnerabilities found in today's scan!")
        send_notification({
            "scan_date": scan_date,
            "scan_time": datetime.now().strftime('%H:%M'),
            "total_sessions_created": 0,
            "total_vulnerabilities": 0,
            "high_severity": 0,
            "medium_severity": 0,
            "low_severity": 0
        })
        return {"status": "no_vulnerabilities", "sessions_created": 0}
    
    # Step 2: Create orchestrator session
    orchestrator = create_orchestrator_session(vulnerabilities)
    
    # Step 3: Create fix sessions for each vulnerability
    fix_session_results = []
    for vuln in vulnerabilities:
        session = create_vulnerability_fix_session(vuln, scan_date)
        fix_session_results.append(session)
    
    # Step 4: Generate summary
    summary = {
        "scan_date": scan_date,
        "scan_time": datetime.now().strftime('%H:%M'),
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
        "total_vulnerabilities": len(vulnerabilities),
        "high_severity": len([v for v in vulnerabilities if v['severity'] == 'High']),
        "medium_severity": len([v for v in vulnerabilities if v['severity'] == 'Medium']),
        "low_severity": len([v for v in vulnerabilities if v['severity'] == 'Low']),
        "timestamp": datetime.now().isoformat()
    }
    
    # Step 5: Send notification
    send_notification(summary)
    
    print("✅ Daily vulnerability scan completed successfully!")
    print(f"📋 Full Summary: {json.dumps(summary, indent=2)}")
    
    return summary


if __name__ == "__main__":
    # Two options for running the scheduled flow:
    
    # OPTION 1: Create a deployment that can be scheduled (recommended for production)
    print("\n" + "="*60)
    print("📅 SCHEDULING DAILY VULNERABILITY SCAN")
    print("="*60)
    
    # Create deployment with cron schedule for 8 AM daily
    deployment = daily_vulnerability_scan_flow.to_deployment(
        name="daily-8am-vulnerability-scan",
        description="Runs Checkmarx vulnerability scan every day at 8:00 AM",
        cron="0 8 * * *",  # Cron expression for 8:00 AM every day
        tags=["checkmarx", "daily", "automated"],
        parameters={},  # Can add default parameters if needed
        work_pool_name=None  # Uses default work pool
    )
    
    print("\n✅ Deployment configured with the following schedule:")
    print("   - Runs every day at 8:00 AM")
    print("   - Cron expression: 0 8 * * *")
    print("\nTo start the scheduled deployment, run:")
    print("   prefect deployment run 'Daily Checkmarx Vulnerability Scan/daily-8am-vulnerability-scan'")
    
    # OPTION 2: Serve the deployment (starts a long-running process)
    print("\n" + "="*60)
    print("🚀 STARTING SCHEDULED FLOW SERVER")
    print("="*60)
    print("The flow will run automatically every day at 8:00 AM")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # This will start a server that runs the flow on schedule
    serve(
        daily_vulnerability_scan_flow.to_deployment(
            name="daily-8am-vulnerability-scan",
            cron="0 8 * * *"  # 8:00 AM every day
        ),
        daily_vulnerability_scan_flow.to_deployment(
            name="test-immediate",
            description="Test deployment that runs immediately for testing",
            tags=["test"]
            # No schedule - can be triggered manually
        )
    )
