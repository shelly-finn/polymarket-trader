#!/usr/bin/env bash
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
