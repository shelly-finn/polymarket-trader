#!/usr/bin/env python3
"""
heartbeat-monitor.py: Revenue loop automation
Runs every heartbeat to scan for leads, generate ideas, and track progress
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get('WORKSPACE', '/home/tomer/.openclaw/workspace'))
OPPORTUNITIES_DB = WORKSPACE / 'databases/opportunities.json'
IDEAS_LOG = WORKSPACE / 'revenue-ideas.md'

def load_opportunities():
    """Load opportunities from JSON database."""
    if OPPORTUNITIES_DB.exists():
        with open(OPPORTUNITIES_DB) as f:
            return json.load(f)
    return {"opportunities": [], "leads": [], "completed": [], "metadata": {}}

def save_opportunities(data):
    """Save opportunities to JSON database."""
    data["metadata"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(OPPORTUNITIES_DB, 'w') as f:
        json.dump(data, f, indent=2)

def get_status_summary():
    """Get current status of all opportunities."""
    data = load_opportunities()
    ideas = len(data.get('opportunities', []))
    leads = len(data.get('leads', []))
    completed = len(data.get('completed', []))
    return {
        'ideas': ideas,
        'leads': leads,
        'completed': completed,
        'total_active': ideas + leads
    }

def log_activity(action, details=""):
    """Log activity to a simple activity log."""
    log_file = WORKSPACE / 'databases/activity.log'
    timestamp = datetime.utcnow().isoformat() + "Z"
    entry = f"{timestamp} | {action} | {details}\n"
    with open(log_file, 'a') as f:
        f.write(entry)

if __name__ == '__main__':
    summary = get_status_summary()
    print(json.dumps(summary))
    log_activity("heartbeat-check", f"ideas={summary['ideas']}, leads={summary['leads']}")
