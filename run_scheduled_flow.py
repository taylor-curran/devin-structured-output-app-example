#!/usr/bin/env python3
"""
Script to run and test the scheduled vulnerability scan flow.
"""
import sys
from scheduled_prefect_flow import daily_vulnerability_scan_flow

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 RUNNING VULNERABILITY SCAN MANUALLY")
    print("="*60)
    print("This is a manual test run of the daily scheduled flow.")
    print("In production, this would run automatically at 8:00 AM daily.\n")
    
    # Disable Prefect cloud connection for local testing
    import os
    os.environ["PREFECT_API_URL"] = ""
    
    # Run the flow manually
    result = daily_vulnerability_scan_flow()
    
    print("\n" + "="*60)
    print("✅ MANUAL TEST RUN COMPLETE")
    print("="*60)
    
    if result.get("status") == "no_vulnerabilities":
        print("No vulnerabilities found in this scan.")
    else:
        print(f"Created {result['total_sessions_created']} sessions:")
        print(f"\n🎯 Orchestrator: {result['orchestrator_session']['url']}")
        print("\n🔧 Fix Sessions:")
        for session in result['fix_sessions']:
            print(f"   - {session['url']}")
    
    print("\n💡 To set up the automated daily schedule:")
    print("   1. Run: python scheduled_prefect_flow.py")
    print("   2. This will start a server that runs the flow daily at 8:00 AM")
    print("   3. Keep the server running to maintain the schedule")
    print("="*60)
