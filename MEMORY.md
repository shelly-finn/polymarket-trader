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

## Current Status
- 1 active idea: "OpenClaw Automation Consulting" (service offering, high revenue potential)
- 0 leads found (inbox is new)
- 0 completed tasks
- All automation scripts tested and working
- Git initialized and first commit done

