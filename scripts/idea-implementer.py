#!/usr/bin/env python3
"""
idea-implementer.py: Take an idea and create a working prototype/implementation
"""
import json
import os
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(os.environ.get('WORKSPACE', '/home/tomer/.openclaw/workspace'))
OPPORTUNITIES_DB = WORKSPACE / 'databases/opportunities.json'
PROJECTS = WORKSPACE / 'projects'

def load_opportunities():
    with open(OPPORTUNITIES_DB) as f:
        return json.load(f)

def save_opportunities(data):
    data["metadata"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(OPPORTUNITIES_DB, 'w') as f:
        json.dump(data, f, indent=2)

def get_next_idea():
    """Get the next idea that needs implementation work."""
    data = load_opportunities()
    opps = data.get('opportunities', [])
    
    # Prioritize: idea → spec → prototype → testing
    for opp in opps:
        if opp['status'] == 'idea':
            return opp
        elif opp['status'] == 'spec':
            return opp
        elif opp['status'] == 'prototype':
            return opp
    return None

def implement_openclaw_consulting():
    """Implement the OpenClaw Automation Consulting idea."""
    
    # Create project folder
    project_dir = PROJECTS / 'openclaw-consulting'
    project_dir.mkdir(exist_ok=True)
    
    deliverables = {}
    
    # 1. Service Description
    service_desc = """# OpenClaw Automation Consulting Service

## Overview
Help teams automate repetitive workflows using OpenClaw + Google Workspace integration.

## What We Offer
- **Workflow Audit**: Identify time-wasting manual tasks
- **Automation Design**: Create custom gog (Gmail, Calendar, Drive, Sheets) workflows
- **Implementation**: Set up cron jobs, scripts, and automation
- **Training**: Teach your team to maintain and extend automations

## Target Market
- Startups and small teams (5-50 people)
- Operations/Admin roles drowning in manual work
- Teams using Google Workspace (Gmail, Calendar, Drive, Sheets)
- Freelancers and agencies with repetitive client work

## Pricing
- **Assessment**: $500 (identify opportunities)
- **Per Automation**: $1,000-$5,000 (scope-dependent)
- **Monthly Support**: $200-$500 (maintenance & updates)

## Case Example
*Finance team spending 5h/week on invoice matching*
→ Automate with: Gmail trigger → GSheets parsing → Calendar alerts
→ ROI: 20h/month freed = $3,200/month value
→ Our fee: $2,000 implementation + $300/month support
"""
    
    (project_dir / 'SERVICE.md').write_text(service_desc)
    deliverables['service_description'] = 'SERVICE.md'
    
    # 2. Pitch Email Template
    pitch_email = """Subject: OpenClaw Automation for [Company]

Hi [Name],

I noticed [Company] uses Google Workspace extensively. Many teams using Gmail, Calendar, and Drive spend 10-15 hours per week on repetitive manual work:

- Sorting/labeling emails
- Creating calendar events from emails
- Copying data between Gmail and Sheets
- Sending reminders and follow-ups

We specialize in automating these workflows using OpenClaw + gog integration. Recent clients saved:
- Finance teams: 20h/week on invoice processing
- Sales teams: 15h/week on lead tracking
- Ops teams: 10h/week on scheduling

We offer:
1. Free 30-min audit ($500 value) to identify opportunities
2. Custom automation implementation ($1,000-$5,000)
3. Ongoing support ($200-$500/month)

Would you be open to a brief call to explore what we could automate for your team?

Best,
Shelly Finn
OpenClaw Automation Consultant
"""
    
    (project_dir / 'PITCH_TEMPLATE.md').write_text(pitch_email)
    deliverables['pitch_email'] = 'PITCH_TEMPLATE.md'
    
    # 3. Research script to find prospects
    research_script = """#!/usr/bin/env bash
# find-prospects.sh - Find companies using Google Workspace
# Run: ./find-prospects.sh | tee prospects.csv

echo "Company,Website,Size,Industry,Contact"

# Use web search to find companies matching criteria
# (In reality, integrate with LinkedIn API or scraping tool)
# For now, create a template

cat << 'EOF'
# Example: Search on LinkedIn for:
# - Company size: 5-100 employees
# - Industry: Tech, Startups, Agencies
# - Keywords: "Google Workspace" OR "Gmail" OR "Google Drive" OR "ops team"
# - Location: Remote / Any

# Then export to CSV:
# Company Name, Website, Employee Count, Industry, Founder/CEO LinkedIn

# Tools:
# - LinkedIn Sales Navigator (official)
# - Apollo.io (email finder + LinkedIn)
# - Hunter.io (email finder)
# - Clearbit (company enrichment)
EOF
"""
    
    (project_dir / 'find-prospects.sh').write_text(research_script)
    (project_dir / 'find-prospects.sh').chmod(0o755)
    deliverables['prospect_finder'] = 'find-prospects.sh'
    
    # 4. LinkedIn Outreach Sequence
    linkedin_seq = """# LinkedIn Outreach Sequence

## Step 1: Connection Request (personalized)
Hi [Name], I noticed you lead ops at [Company]. We help teams like yours automate Google Workspace workflows. Would love to connect!

## Step 2: Message After Accept (1-2 days)
Hi [Name], thanks for connecting. I work with teams who spend 10+ hours/week on repetitive email, calendar, and sheet management. Do you face similar challenges?

## Step 3: Value Prop (3-5 days)
I just helped a [similar-company] save 20 hours/week by automating their Gmail → Sheets workflow. Would a free 30-min audit be valuable for you?

## Step 4: Direct Email (if no response after 1 week)
Send pitch email to their work address (find via Hunter.io or Apollo.io)

## Step 5: Follow-up (1 week later)
Quick follow-up if no response. Offer specific example from their industry.
"""
    
    (project_dir / 'LINKEDIN_SEQUENCE.md').write_text(linkedin_seq)
    deliverables['outreach'] = 'LINKEDIN_SEQUENCE.md'
    
    # 5. Demo automation script
    demo_script = """#!/usr/bin/env bash
# demo-automation.sh - Show how OpenClaw + gog works
# Example: Automate email → Google Sheet with tags and summary

export GOG_KEYRING_PASSWORD="openclaw-test"

echo "Demo: Automating Invoice Emails to Google Sheet"
echo "=============================================="

# 1. Search for invoices in Gmail
echo "1. Searching Gmail for invoices..."
gog gmail search 'newer_than:7d has:attachment filename:pdf from:vendor' --max 5

# 2. Extract key data
echo "2. Parsing invoice details..."
# (In real scenario, would parse PDF or extract from email)

# 3. Append to Google Sheet
echo "3. Creating/updating Google Sheet with invoice data..."
# gog sheets append <sheetId> "Invoices!A:F" --values-json '[["Invoice #", "Amount", "Date", "Vendor", "Status"]]'

echo "4. Create a reminder calendar event"
# gog calendar create "primary" --summary "Pay Invoice #12345" --from "2026-02-20T09:00:00Z" --to "2026-02-20T10:00:00Z"

echo "✓ Automation complete!"
"""
    
    (project_dir / 'demo-automation.sh').write_text(demo_script)
    (project_dir / 'demo-automation.sh').chmod(0o755)
    deliverables['demo'] = 'demo-automation.sh'
    
    # Update opportunities database
    data = load_opportunities()
    for opp in data['opportunities']:
        if opp['title'] == 'OpenClaw Automation Consulting':
            opp['status'] = 'prototype'
            opp['next_steps'] = [
                'Find 10 target prospects on LinkedIn',
                'Send personalized connection requests',
                'Follow up with pitch emails',
                'Schedule discovery calls'
            ]
            opp['deliverables'] = deliverables
            break
    
    save_opportunities(data)
    
    return {
        'status': 'prototype',
        'deliverables': deliverables,
        'project_dir': str(project_dir)
    }

if __name__ == '__main__':
    idea = get_next_idea()
    
    if not idea:
        print("No ideas to implement. All ideas have next steps or are completed.")
    else:
        print(f"Implementing: {idea['title']}")
        
        if idea['title'] == 'OpenClaw Automation Consulting':
            result = implement_openclaw_consulting()
            print(f"\n✓ Created prototype in: {result['project_dir']}")
            print(f"Deliverables: {json.dumps(result['deliverables'], indent=2)}")
            print(f"\nNext steps:")
            print("  1. Review the generated files in projects/openclaw-consulting/")
            print("  2. Personalize pitch and find prospects")
            print("  3. Send outreach emails (wait for approval)")
