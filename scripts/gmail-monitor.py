#!/usr/bin/env python3
"""
gmail-monitor.py: Monitor Gmail for business leads/opportunities
"""
import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get('WORKSPACE', '/home/tomer/.openclaw/workspace'))
OPPORTUNITIES_DB = WORKSPACE / 'databases/opportunities.json'

def run_gog_search(query, max_results=10):
    """Run gog gmail search and parse results."""
    os.environ['GOG_KEYRING_PASSWORD'] = 'openclaw-test'
    cmd = ['gog', 'gmail', 'search', query, '--max', str(max_results), '--json']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"Error running gog: {e}")
    return {"threads": []}

def extract_leads(threads):
    """Extract potential leads from email threads."""
    leads = []
    keywords = ['interested', 'opportunity', 'collaboration', 'partnership', 'budget', 'rate', 'availability']
    
    for thread in threads:
        subject = thread.get('subject', '').lower()
        if any(kw in subject for kw in keywords):
            leads.append({
                'id': thread['id'],
                'from': thread.get('from', ''),
                'subject': thread.get('subject', ''),
                'date': thread.get('date', ''),
                'found_at': datetime.utcnow().isoformat() + "Z"
            })
    return leads

def save_lead(lead):
    """Save a lead to opportunities database."""
    data = json.load(open(OPPORTUNITIES_DB))
    data['leads'].append(lead)
    with open(OPPORTUNITIES_DB, 'w') as f:
        json.dump(data, f, indent=2)
    return True

if __name__ == '__main__':
    # Search for leads from last 7 days
    query = 'newer_than:7d (interested OR opportunity OR collaboration OR partnership OR budget OR rate OR availability)'
    results = run_gog_search(query, max_results=20)
    leads = extract_leads(results.get('threads', []))
    
    print(f"Found {len(leads)} potential leads")
    for lead in leads:
        save_lead(lead)
        print(f"  - {lead['subject']} from {lead['from']}")
