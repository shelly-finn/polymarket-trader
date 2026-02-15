# Heartbeat - Revenue & Opportunity Loop

**Goal:** Every 30 minutes, advance revenue ideas and monitor market intelligence.

## Each Heartbeat Does

1. **SEC Filing Monitor** (2 min)
   - Run: `python3 scripts/sec_monitor.py --check`
   - Monitors watchlist: AAPL, MSFT, GOOG, AMZN, NVDA, META, TSLA
   - Auto-extracts risk factors from new 10-K/10-Q filings
   - Logs insights to `projects/ai-investment-agent/insights.json`

2. **Scan for Leads** (2 min)
   - Gmail: search for recent business/partnership inquiries
   - Keywords: interested, opportunity, collaboration, budget, rate, availability
   - If found: extract details and add to opportunities.json

3. **Advance Active Ideas** (10 min)
   - Pick the highest-priority idea (status: idea → prototype → launched)
   - Execute ONE concrete step toward implementation:
     - **Idea stage**: Write service description, pitch, technical spec
     - **Prototype stage**: Build working code, landing page, email template, automation script
     - **Implementation**: Deploy, publish, or activate the working version
   - Create actual deliverables (code, docs, assets) in projects/

4. **Generate New Ideas** (3 min)
   - If no leads and all ideas have tasks: generate 1 new revenue idea
   - Ideas must have: description, target market, implementation plan, effort estimate

5. **Report Back** (3 min)
   - What was completed in this heartbeat?
   - Links to created code/docs/prototypes
   - Next concrete step
   - Blockers or dependencies

## Implementation-Focused Actions

Examples of heartbeat work:
- Write Python script to automate a process (and test it)
- Create email outreach template (with actual copy)
- Build a landing page (HTML/CSS in projects/)
- Write API integration (code in projects/)
- Create a service offering document (in projects/)
- Set up automation workflow (gog commands, cron jobs)
- Generate leads list with contact details
- Draft sales pitch / value proposition
- Create pricing model / package tiers
- **Polymarket**: Scan markets, analyze signals, place paper bets, track outcomes

## Polymarket Paper Trading

**Goal:** Test strategies with simulated bets until consistently profitable.

**Each heartbeat:**
1. Scan markets: `python3 projects/polymarket-trader/polymarket_trader.py --scan`
2. Analyze signals: `python3 projects/polymarket-trader/strategies.py`
3. If high-conviction opportunity: place paper bet with reasoning
4. Check open bets: `python3 projects/polymarket-trader/polymarket_trader.py --check`
5. Update resolved bets and track P&L

**Bet criteria:**
- Only bet when I have specific reasoning (not just "price seems wrong")
- News correlation: recent event should move price
- Information edge: I know something market doesn't reflect
- Start small ($10-50 paper bets) to test strategy
- Track win rate and ROI over time

**Success threshold for real money:**
- 20+ paper bets completed
- Win rate > 55%
- Positive ROI after fees
- Consistent strategy that can be explained

NOT just "research" or "plan" — actual executable deliverables.

## Workflow States

Each opportunity moves through:
1. **idea** - Concept, no implementation
2. **spec** - Technical or business specification written
3. **prototype** - Working code/template/doc created
4. **testing** - Test the implementation with sample data/users
5. **launched** - Live, deployed, or activated
6. **completed** - Revenue generated or milestone hit

## Tools for Implementation

- **gog**: Create docs, sheets, email drafts; send when approved
- **gh**: GitHub CLI for repo management, issues, PRs, workflows; public lead discovery
- **bash/python**: Write scripts, automation, integrations
- **git**: Version control; commit every completed step
- **web_search**: Research for building things faster
- **gemini**: Only for complex code generation or architecture decisions
- **Local files**: Create projects in projects/ folder

## Success Metrics

- Ideas moving through stages (idea → prototype → launched)
- Actual code/content created per heartbeat
- Leads converted or contacted
- Revenue opportunities with next-step clarity
- Committed changes pushed to git

## Contact rules

Work every 30 minutes as normal, but only approach Tomer (send a notification) in these cases:
1. You made money (a paid engagement, invoice received, or clear commitment to pay)
2. You need money (funding, subscription, or anything that requires financial action)
3. You want Tomer to set you up with something requiring human involvement (access, OAuth approval, billing, legal)
4. You need counseling or a decision from Tomer (strategy, negotiation, or ethical questions)

If you want different thresholds (e.g., notify for high-value leads only, or allow a daily summary), update MEMORY.md and HEARTBEAT.md accordingly.
