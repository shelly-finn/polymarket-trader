# Heartbeat - Polymarket Intelligence System

**Goal:** Build a profitable Polymarket trading system through research, analysis, and systematic strategy testing.

**Every heartbeat MUST produce work.** No empty heartbeats. Each run should result in:
- New research (1 deep dive per heartbeat minimum)
- New paper bets placed (documented reasoning)
- Updated market intelligence
- Commit to GitHub with timestamp and changes

## Each Heartbeat Does

### 1. Market Intelligence (3 min)
- Scan active markets for new opportunities
- Track price movements on watched markets
- Identify unusual volume or price swings
- Log market state changes to `data/market_history.json`
- **OUTPUT:** Updated cache + signals file

### 2. Research & Analysis (10 min)
Pick ONE market and do deep research:
- **News correlation**: What events could move this market?
- **Resolution criteria**: How exactly does this resolve? Edge cases?
- **Market structure**: Who's trading? Liquidity depth? Spread?
- **Historical patterns**: Similar past markets? How did they resolve?
- **Contrarian check**: Why might the crowd be wrong?
- **Price analysis**: Why is it priced where it is? Mispriced?

Save research to `research/MARKET_ID.md`
**OUTPUT:** Markdown file with timestamp, sources, analysis

### 3. Paper Trading + Bet Placement (5 min)
- Scan open bets: price changes, P&L, resolve if done
- Find ONE trading signal from market intelligence
- Place documented paper bet with:
  - Specific entry reason (edge identified)
  - Price target (where/why to exit)
  - Position size
- **OUTPUT:** New line in paper_bets.json + updated performance.json

### 4. Commit & Push (2 min)
- Stage all changes: research/, data/, strategies/
- Commit: `git commit -m "heartbeat: TIMESTAMP — SUMMARY"`
  - Example: `heartbeat: 2026-02-15T06:35Z — Russia/Ukraine research, placed BTC bet at $68k`
- Push: `git push origin main`
- **OUTPUT:** GitHub shows commit activity every heartbeat

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
