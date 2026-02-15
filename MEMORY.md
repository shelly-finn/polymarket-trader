# MEMORY.md - Long-Term Memory

## Identity
- **Name:** Shelly Finn
- **Google Account:** shellyfinn9@gmail.com (password: 123Shelly!@#)
- **Setup Date:** February 14, 2026
- **Primary Goal:** Revenue generation via heartbeat-driven automation loop

## System Setup (Feb 14, 2026 - 19:44 UTC)

### Google Workspace Integration (gog)
- **Status:** Active and configured
- **Connected Services:** Gmail, Calendar, Drive, People/Contacts, Sheets, Slides, Tasks
- **Environment:** GOG_KEYRING_PASSWORD="openclaw-test" (set in .bashrc for seamless auth)
- **Keyring Setup:** Automatic authentication enabled for headless operation

### Revenue System Architecture
- **Heartbeat Interval:** 30 minutes (every heartbeat, revenue loop executes)
- **Database:** `databases/opportunities.json` - JSON schema for tracking ideas, leads, completed tasks
- **Scripts:**
  - `scripts/heartbeat-monitor.py` - Status check and opportunity counter
  - `scripts/gmail-monitor.py` - Scans Gmail for business leads using keywords
  - `scripts/status.py` - Displays current dashboard (ideas, leads, completed)
- **Workspace Folders:**
  - `projects/` - Active revenue projects
  - `drafts/` - Email templates, pitch decks (created but NOT sent without approval)
  - `research/` - Market analysis and competitive research
  - `assets/` - Templates, images, media

### Key Instructions from Tomer
- **Autonomy:** Full autonomy on Google account and system (has root access)
- **Safe Actions:** Create drafts, documents, scripts, organize files, scan emails
- **Restricted:** Cannot send emails/publish without explicit approval
- **Gemini:** Use sparingly, only for complex reasoning/programming tasks
- **Git:** All changes committed; databases/ and drafts/ excluded from version control

## Heartbeat Loop Behavior (Every 30 minutes)
1. Search Gmail for business keywords: interested, opportunity, partnership, budget, rate, availability
2. Check status of active ideas and leads
3. If no new leads: generate 1 new micro-revenue idea
4. Log findings to opportunities.json
5. Report: ideas found, leads discovered, progress made

## Heartbeat contact rules
- Work every 30 minutes as normal, but only approach Tomer (send a notification) in these cases:
  1. You made money (a paid engagement, invoice received, or clear commitment to pay)
  2. You need money (funding, subscription, or anything that requires financial action)
  3. You want Tomer to set you up with something requiring human involvement (access, OAuth approval, billing, legal)
  4. You need counseling or a decision from Tomer (strategy, negotiation, or ethical questions)

## GitHub Integration (Feb 15, 2026 - 02:25 UTC)
- **Account:** shelly-finn (authenticated via Google OAuth)
- **CLI:** gh (GitHub CLI) fully functional
- **Active Repos:**
  - https://github.com/shelly-finn/openclaw-automation-consulting (service offering, lead magnet)
  - https://github.com/shelly-finn/heartbeat-automation (framework and workflow)
  - https://github.com/shelly-finn/openclaw-tools (templates, drafts, assets)
  - https://github.com/shelly-finn/ai-investment-agent (SEC filings analysis, investment research - PRIVATE)
- **Capability:** Can now create issues, PRs, search repos, manage workflows, use for public-facing lead discovery

## Current Status
- 2 active ideas:
  1. "OpenClaw Automation Consulting" (status: prototype, high revenue potential)
  2. "AI Investment Analysis Agent" (status: spec, research complete, higher revenue ceiling)
- 4 GitHub repos created and maintained
- 0 leads found (inbox is new, outreach starting)
- 0 completed tasks (revenue not yet generated)
- All automation scripts tested and working
- Git + GitHub fully integrated into the workflow

## AI Investment Agent Research (Feb 15, 2026)
- Scanned GitHub for existing financial agent projects (FinBERT, virattt/ai-financial-agent, TickrAgent)
- Created SEC EDGAR fetcher and risk comparator tools
- Identified gap opportunities: cross-company comparison, anomaly detection, small-cap scanner
- Revenue potential: $99-299/mo subscriptions, $2k+ custom analysis

## SEC EDGAR Parser Fix (Feb 15, 2026 - 02:45 UTC)
- **Issue:** Risk factor extraction regex was failing on XBRL inline format (only ~10 chars extracted)
- **Root cause:** Complex nested HTML tags and entities weren't being cleaned before pattern matching
- **Solution:** Improved extraction function with:
  1. Multiple regex patterns (specific to general fallback)
  2. Proper HTML entity decoding (including numeric &#8217; style)
  3. Safe character code conversion with bounds checking (<1114112 codepoints)
  4. Better tag stripping (comments, styles, all tags)
  5. Increased char limit to 150K for verbose XBRL filings
- **Status:** ✅ FIXED - Tested on Apple 10-K (Sept 2025): Successfully extracted 68,022 chars of risk factors
- **Files:** sec_edgar_fetcher.py, risk_comparator.py, data/AAPL_2025-10-31_risks.txt
- **Committed:** 8c8d53b
