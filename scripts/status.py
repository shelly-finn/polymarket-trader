#!/usr/bin/env python3
"""
status.py: Show revenue system status dashboard
"""
import json
from pathlib import Path
from datetime import datetime
import os

WORKSPACE = Path(os.environ.get('WORKSPACE', '/home/tomer/.openclaw/workspace'))
OPPORTUNITIES_DB = WORKSPACE / 'databases/opportunities.json'

def print_dashboard():
    """Print a formatted status dashboard."""
    if not OPPORTUNITIES_DB.exists():
        print("No opportunities database found.")
        return
    
    with open(OPPORTUNITIES_DB) as f:
        data = json.load(f)
    
    opps = data.get('opportunities', [])
    leads = data.get('leads', [])
    completed = data.get('completed', [])
    
    print("\n" + "="*60)
    print("REVENUE SYSTEM STATUS")
    print("="*60)
    
    print(f"\n📊 SUMMARY")
    print(f"  Active Ideas:      {len(opps)}")
    print(f"  Incoming Leads:    {len(leads)}")
    print(f"  Completed Tasks:   {len(completed)}")
    print(f"  Total Active:      {len(opps) + len(leads)}")
    
    if opps:
        print(f"\n💡 ACTIVE IDEAS")
        for i, opp in enumerate(opps, 1):
            print(f"  {i}. {opp['title']}")
            print(f"     Status: {opp['status']} | Effort: {opp['effort']} | Revenue: {opp['potential_revenue']}")
            print(f"     Next: {opp['next_steps'][0] if opp['next_steps'] else 'None'}")
    
    if leads:
        print(f"\n🔥 NEW LEADS")
        for i, lead in enumerate(leads, 1):
            print(f"  {i}. {lead['subject']}")
            print(f"     From: {lead['from']}")
            print(f"     Date: {lead['date']}")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    print_dashboard()
