#!/usr/bin/env bash
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
