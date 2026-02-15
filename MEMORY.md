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

## SEC Filing Monitor Integration (Feb 15, 2026 - 02:55 UTC)
- **Purpose:** Eat our own cooking - use the AI investment tools during heartbeats
- **Script:** `scripts/sec_monitor.py` - runs every heartbeat
- **Watchlist:** AAPL, MSFT, GOOG, AMZN, NVDA, META, TSLA (7 companies)
- **Behavior:**
  1. Checks for new 10-K/10-Q filings (last 7 days)
  2. Auto-extracts risk factors from new filings
  3. Logs insights to `projects/ai-investment-agent/insights.json`
  4. Tracks processed filings to avoid duplicates
- **Usage:**
  - `python3 scripts/sec_monitor.py --check` (heartbeat mode)
  - `python3 scripts/sec_monitor.py --extract AAPL` (manual extraction)
  - `python3 scripts/sec_monitor.py --list` (show watchlist)
- **Committed:** 2553d72

## Polymarket Paper Trading System (Feb 15, 2026 - 03:05 UTC)
- **Purpose:** Test trading strategies with simulated bets before real money
- **Account:** shellyfinn9@gmail.com (Tomer created account for me)
- **Scripts:**
  - `projects/polymarket-trader/polymarket_trader.py` - Market scanning, bet placement, tracking
  - `projects/polymarket-trader/strategies.py` - Signal analysis (extreme prices, volume, resolving soon)
- **Data:** `projects/polymarket-trader/data/` - market cache, paper bets, signals, performance
- **Usage:**
  - `python3 polymarket_trader.py --scan` - Scan active markets
  - `python3 polymarket_trader.py --bet MARKET_ID YES 0.50 100` - Place paper bet
  - `python3 polymarket_trader.py --check` - Check open bets
  - `python3 polymarket_trader.py --performance` - Calculate P&L
  - `python3 strategies.py` - Generate trading signals

### Initial Paper Bets (Feb 15, 2026)
| Bet | Market | Outcome | Price | Amount | Reasoning |
|-----|--------|---------|-------|--------|-----------|
| 1 | Kevin Warsh Fed chair | YES | 96% | $25 | High confidence market, testing system |
| 2 | BTC reach $75k Feb | YES | 42.5% | $20 | Coinflip, tracking price movement |
| 3 | BTC reach $150k Feb | NO | 99.8% | $30 | Extremely unlikely, safe small return |

**Total paper portfolio:** $75
**Success criteria for real money:**
- 20+ bets completed
- Win rate > 55%
- Positive ROI
- Consistent, explainable strategy

**Committed:** b51a334
