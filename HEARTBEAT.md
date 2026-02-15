# Heartbeat - Polymarket Intelligence System

**Goal:** Build a profitable Polymarket trading system through research, analysis, and systematic strategy testing.

## Each Heartbeat Does

### 1. Market Intelligence (5 min)
- Scan active markets for new opportunities
- Track price movements on watched markets
- Identify unusual volume or price swings
- Log market state changes to `data/market_history.json`

### 2. Research & Analysis (10 min)
Pick ONE market and do deep research:
- **News correlation**: What events could move this market?
- **Resolution criteria**: How exactly does this resolve? Edge cases?
- **Market structure**: Who's trading? Liquidity depth? Spread?
- **Historical patterns**: Similar past markets? How did they resolve?
- **Contrarian check**: Why might the crowd be wrong?

Save research to `research/MARKET_ID.md`

### 3. Strategy Development (10 min)
Build and test trading strategies:
- **Event-driven**: News breaks → market should move
- **Arbitrage**: Price inconsistencies across related markets
- **Time decay**: Markets mispriced as resolution approaches
- **Sentiment**: Crowd psychology creates mispricings
- **Information edge**: I know something market doesn't reflect

Document strategies in `strategies/` with:
- Entry criteria
- Exit criteria
- Position sizing
- Expected edge
- Backtest results (if possible)

### 4. Paper Trading (5 min)
- Check open bets: price changes, P&L
- Resolve completed bets (won/lost)
- Place new bets ONLY with documented reasoning
- Update performance metrics

### 5. System Building (ongoing)
Build tools that give edge:
- [ ] News scraper for market-relevant events
- [ ] Price alert system for watched markets
- [ ] Resolution tracker (when markets resolve, log outcomes)
- [ ] Smart money tracker (large position changes)
- [ ] Cross-market correlator (related markets moving together)

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

**Entry criteria:**
- Written reasoning required (no "gut feel" bets)
- Must identify specific edge (why am I smarter than market?)
- Must have exit plan (take profit / stop loss levels)

**Tracking:**
- Log every bet with reasoning
- Track which strategies win/lose
- Calculate ROI by strategy type
- Review and iterate weekly

## Success Metrics

**Phase 1: Learning (current)**
- 20+ paper bets with documented reasoning
- Research notes on 10+ markets
- 2-3 defined strategies with entry/exit rules

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

**Notify Tomer only when:**
1. **Made money** — A real bet resolved profitably or a deal closed
2. **Need money** — Funding, subscription, or payment required
3. **Need human setup** — API access, account creation, legal/billing action
4. **Stuck** — Hit a blocker that requires human input to unblock
5. **Exceptional opportunity** — Time-sensitive edge that needs quick decision

**Work silently on:**
- Paper trading (iterate, place bets, track performance)
- Research and analysis (deep dives, strategy docs)
- System building (code, tooling, automation)
- Learning and strategy testing
- Market monitoring and signal generation

**Cadence:** Heartbeat runs every 30 minutes. Most cycles will complete silently. Only interrupt when above conditions are met.

## File Structure

```
projects/polymarket-trader/
├── data/
│   ├── market_cache.json      # Current market state
│   ├── market_history.json    # Price history over time
│   ├── paper_bets.json        # All paper bets
│   ├── signals.json           # Generated signals
│   └── performance.json       # P&L tracking
├── research/
│   └── {market_id}.md         # Deep dive research per market
├── strategies/
│   └── {strategy_name}.md     # Documented strategies
├── polymarket_trader.py       # Main trading CLI
└── strategies.py              # Signal analysis
```
