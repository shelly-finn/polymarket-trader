#!/usr/bin/env python3
"""
heartbeat-execute.py: Main execution engine for heartbeat revenue loop
Combines: lead scanning, idea advancement, implementation
"""
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(os.environ.get('WORKSPACE', '/home/tomer/.openclaw/workspace'))
OPPORTUNITIES_DB = WORKSPACE / 'databases/opportunities.json'
ACTIVITY_LOG = WORKSPACE / 'databases/activity.log'

def log_activity(action, details=""):
    """Log activity with timestamp."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    with open(ACTIVITY_LOG, 'a') as f:
        f.write(f"{timestamp} | {action} | {details}\n")

def load_opportunities():
    with open(OPPORTUNITIES_DB) as f:
        return json.load(f)

def save_opportunities(data):
    data["metadata"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(OPPORTUNITIES_DB, 'w') as f:
        json.dump(data, f, indent=2)

def scan_gmail_leads():
    """Scan Gmail for new leads."""
    try:
        os.environ['GOG_KEYRING_PASSWORD'] = 'openclaw-test'
        cmd = ['gog', 'gmail', 'search', 
               'newer_than:7d (interested OR opportunity OR collaboration OR partnership OR budget OR rate OR availability)',
               '--max', '20', '--json']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            leads_found = len(data.get('threads', []))
            log_activity("scan_gmail", f"found {leads_found} threads")
            return data.get('threads', [])
    except Exception as e:
        log_activity("scan_gmail_error", str(e))
    return []

def advance_highest_priority_idea():
    """Find and advance the next idea in the pipeline."""
    data = load_opportunities()
    opps = data.get('opportunities', [])
    
    # Find next idea needing work
    for opp in opps:
        if opp['status'] == 'idea':
            # Move to spec stage
            opp['status'] = 'spec'
            action = f"Advanced '{opp['title']}' to spec stage"
            log_activity("advance_idea", action)
            save_opportunities(data)
            return {'status': 'spec', 'idea': opp['title'], 'action': action}
        
        elif opp['status'] == 'spec':
            # Would normally run implementation, but require explicit trigger
            action = f"'{opp['title']}' ready for prototype - requires implementation trigger"
            log_activity("idea_ready", action)
            return {'status': 'spec', 'idea': opp['title'], 'action': action}
        
        elif opp['status'] == 'prototype':
            # Continue with next steps
            action = f"'{opp['title']}' in prototype stage - next: {opp['next_steps'][0] if opp['next_steps'] else 'none'}"
            log_activity("prototype_progress", action)
            return {'status': 'prototype', 'idea': opp['title'], 'action': action}
    
    return None

def generate_new_idea():
    """Generate a new revenue idea."""
    ideas_templates = [
        {
            "title": "LinkedIn Content Marketing for OpenClaw",
            "description": "Create a content series showing automation wins + tutorials",
            "category": "content",
            "potential_revenue": "medium",
            "effort": "low",
            "market": ["solopreneurs", "agencies", "ops-people"]
        },
        {
            "title": "OpenClaw Automation Templates Marketplace",
            "description": "Sell pre-built automation scripts/templates on Gumroad or similar",
            "category": "product",
            "potential_revenue": "medium",
            "effort": "high"
        },
        {
            "title": "Email Automation Agency",
            "description": "Specialize in email sequence automation for SaaS/e-commerce",
            "category": "service",
            "potential_revenue": "high",
            "effort": "high"
        },
        {
            "title": "Free OpenClaw Automation Audit Tool",
            "description": "SaaS tool that analyzes Gmail/Calendar usage and suggests automations",
            "category": "product",
            "potential_revenue": "high",
            "effort": "high"
        },
        {
            "title": "Automation Consulting for Non-Profits",
            "description": "Offer discounted automation services to non-profits (mission + revenue)",
            "category": "service",
            "potential_revenue": "low",
            "effort": "low"
        }
    ]
    
    import random
    new_idea = random.choice(ideas_templates)
    new_idea['id'] = f"idea_{datetime.utcnow().timestamp()}"
    new_idea['status'] = 'idea'
    new_idea['next_steps'] = ["Define target market", "Create value proposition", "Build prototype"]
    
    data = load_opportunities()
    data['opportunities'].append(new_idea)
    save_opportunities(data)
    
    log_activity("generate_idea", f"new idea: {new_idea['title']}")
    return new_idea

def main():
    """Run the complete heartbeat execution."""
    print("\n" + "="*60)
    print("HEARTBEAT EXECUTION - Revenue Loop")
    print("="*60)
    
    # 1. Scan for leads
    print("\n[1/4] Scanning Gmail for leads...")
    leads = scan_gmail_leads()
    if leads:
        print(f"  ✓ Found {len(leads)} potential leads")
    else:
        print("  • No new leads found")
    
    # 2. Advance active ideas
    print("\n[2/4] Advancing active ideas...")
    idea_status = advance_highest_priority_idea()
    if idea_status:
        print(f"  ✓ {idea_status['action']}")
    else:
        print("  • No ideas to advance")
    
    # 3. Generate new idea if needed
    print("\n[3/4] Checking for new idea generation...")
    data = load_opportunities()
    if len(data['opportunities']) < 3:
        new_idea = generate_new_idea()
        print(f"  ✓ Generated new idea: {new_idea['title']}")
    else:
        print(f"  • Already have {len(data['opportunities'])} active ideas")
    
    # 4. Summary
    print("\n[4/4] Status Summary")
    data = load_opportunities()
    opps = data['opportunities']
    print(f"  Active ideas: {len(opps)}")
    print(f"  Incoming leads: {len(data['leads'])}")
    print(f"  Ideas by stage:")
    for stage in ['idea', 'spec', 'prototype', 'testing', 'launched']:
        count = sum(1 for o in opps if o['status'] == stage)
        if count > 0:
            print(f"    - {stage}: {count}")
    
    print("\n" + "="*60)
    print("Heartbeat complete!")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
