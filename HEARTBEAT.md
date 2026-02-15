# Heartbeat - Polymarket Intelligence System

**Goal:** Build a profitable Polymarket trading system through research, analysis, and systematic strategy testing.

**Every heartbeat MUST produce work.** No empty heartbeats. Each run should result in:
- New research (1 deep dive per heartbeat minimum)
- New paper bets placed (documented reasoning)
- Updated market intelligence
- Commit to GitHub with timestamp and changes

## Each Heartbeat (My Direct Work)

### 1. Market Scan (5 min)
- What markets are moving right now?
- What's happening with watched markets (Ukraine/Russia, BTC, Fed, AI)?
- Any news that changes probabilities?
- **OUTPUT:** Market selection for deep dive

### 2. Deep Research (10 min)
I analyze ONE market thoroughly:
- **News & events**: What actually moves this market? Current news?
- **Resolution mechanics**: How does this resolve YES vs NO? Edge cases?
- **Base rates**: Similar past events — how often did they happen?
- **Price analysis**: Why is market at this bid? Is it mispriced?
- **My edge**: Why do I think I'm right and market is wrong?
- **Contrarian view**: What would prove me wrong?

Write analysis to `research/MARKET_ID.md` with:
- Timestamp, sources, my reasoning
- Entry logic (why BET on this now)
- Exit plan (profit/stop loss targets)
- Conviction level (high/medium/low)

**OUTPUT:** Research doc with my thesis

### 3. Bet Placement (3 min)
- Place ONE paper bet based on research
- Entry: My identified edge
- Amount: $10-30 (betting pool ~$100)
- Direction: YES or NO with reasoning
- Track in `data/paper_bets.json`

**OUTPUT:** New bet logged + documented reasoning

### 4. Commit & Push (2 min)
- Stage changes: research/, data/
- Commit: `git commit -m "heartbeat: TIMESTAMP — SUMMARY"`
  - Example: `heartbeat: 2026-02-15T06:35Z — Russia/Ukraine escalation risk, placed NO bet at 58%`
- Push: `git push origin master`

**OUTPUT:** GitHub commit visible to you instantly

## Research Priorities

### High-Value Market Types
1. **Near-term political**: Fed decisions, nominations, policy
2. **Crypto price targets**: BTC/ETH milestones
3. **Tech/AI releases**: Product launches, model releases
4. **Sports with edge**: Stats-heavy, model-able
5. **Binary events**: Clear resolution, datable outcomes

### Research Questions for Each Market
1. What exactly triggers YES vs NO?
2. What's the base rate for this type of event?
3. What information would change my view?
4. Who has better information than me?
5. Why is the market priced where it is?

## Paper Trading Rules

**Bet sizing:**
- Max 10% of portfolio on single bet
- Start small ($10-25) until strategy proves out
- Scale up only with documented edge
- **Every heartbeat:** Place at least 1 new bet if signal exists

**Entry criteria:**
- Written reasoning required (no "gut feel" bets)
- Must identify specific edge (why am I smarter than market?)
- Must have exit plan (take profit / stop loss levels)

**Tracking:**
- Log every bet with reasoning, market ID, timestamp
- Track which strategies win/lose
- Calculate ROI by strategy type
- Review performance weekly

## Success Metrics

**Phase 1: Learning (current)**
- 50+ paper bets placed (from daily heartbeats)
- 10+ researched markets with deep-dive docs
- 3-5 defined strategies with entry/exit rules
- Consistent commits to GitHub

**Phase 2: Proving**
- Win rate > 55%
- Positive ROI after simulated fees
- Consistent strategy that can be explained
- Report to Tomer for real money allocation

**Phase 3: Scaling**
- Real money deployment
- Position sizing optimization
- Portfolio diversification
- Automated alerts/execution

## Contact Rules

Only notify Tomer when:
1. **Made money** — A real bet resolved profitably or a deal closed
2. **Need human setup** — API access, account creation, legal/billing action
3. **Stuck** — Hit a blocker that requires human input to unblock
4. **Exceptional opportunity** — Time-sensitive edge that needs quick decision

**Work silently on everything else** — Research, paper trading, commits, monitoring, analysis.

## Heartbeat Cadence

- **Runs:** Every 30 minutes (non-blocking)
- **Work per run:** ~20 minutes of actual analysis/research/trading
- **Output per run:** Git commit pushed to GitHub
- **Visibility:** Tomer sees progress via GitHub activity feed
- **Interruptions:** Only on money-made / need-human-help conditions

## File Structure

```
projects/polymarket-trader/
├── data/
│   ├── market_cache.json      # Current market state
│   ├── market_history.json    # Price history over time
│   ├── paper_bets.json        # All paper bets (cumulative)
│   ├── signals.json           # Generated signals
│   └── performance.json       # P&L tracking
├── research/
│   └── {market_id}.md         # Deep dive research per market
├── strategies/
│   └── {strategy_name}.md     # Documented strategies
├── polymarket_trader.py       # Main trading CLI
└── strategies.py              # Signal analysis
```
