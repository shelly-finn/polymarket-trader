# Heartbeat - Polymarket Paper Trading (Rapid Iteration)

**Goal:** Find a repeatable, profitable trading strategy by testing on short-resolution markets.

**Philosophy:** 
- Fast feedback loops (1-7 days per bet)
- Rapid iteration (adjust strategy based on results)
- Data-driven edge discovery (test, measure, improve, repeat)
- Build systematic approach vs. one-off bets

**Every heartbeat MUST produce work:** Place 2-3 bets on markets resolving within 7 days, document strategy, commit results.

## Each Heartbeat (30 min cycle)

### 1. Short-Resolution Market Scan (3 min)
- Identify markets resolving in next **1-7 days ONLY**
- Categories: Crypto prices (daily), sports (same day), economic data (scheduled), event timing
- Filter for liquid markets (high volume, tight spreads)
- **OUTPUT:** 2-3 candidate markets

### 2. Quick Research + Bet (8 min)
For EACH market:
- **Edge identified?** Why do I think market is mispriced RIGHT NOW?
- **Base rate check:** Similar past events — what actually happened?
- **Price analysis:** Is this a volatility bet, contrarian bet, or information edge?
- **Entry/exit:** Specific price/outcome targets and stop-loss levels

Write ONE-PAGE research to `research/SHORT_MARKET_ID_DATE.md`

**OUTPUT:** Quick analysis doc (1-3 paragraphs, not long essays)

### 3. Bet Placement (5 min)
- Place 2-3 paper bets per heartbeat on short-resolution markets
- Size: $5-15 each (smaller, more frequent bets)
- Track in `data/paper_bets.json` with:
  - Market ID, question, direction
  - Entry price, amount, resolution date
  - Strategy name (e.g., "crypto volatility", "sports contrarian", "data edge")
  - Reasoning (one line: why mispriced?)

**OUTPUT:** New bets logged with strategy labels

### 4. Weekly Performance Review (Sunday)
- Resolve all closed bets from past week
- Calculate win rate, ROI by strategy
- Document what worked/failed in `data/strategy_performance.json`
- Update HEARTBEAT.md strategy list based on results
- Commit: "weekly: TIMESTAMP — X% win rate, Y strategies tested, adjust Z"

**OUTPUT:** Data-driven feedback on strategy effectiveness

### 5. Commit & Push (2 min)
- Stage: research/, data/
- Commit: `git commit -m "heartbeat: TIMESTAMP — STRATEGY_NAME bets (resolves DATE)"`
- Push to GitHub

**OUTPUT:** Every heartbeat visible on GitHub



## Strategies to Test

### Active Strategies (Current Iteration)

1. **Crypto Volatility Underpricing**
   - Hypothesis: Daily crypto price moves are often underpriced (markets conservative on volatility)
   - Test: Place bets on BTC/ETH daily moves >2%, <1% based on historical frequency
   - Resolution: 1-7 days
   - Status: Testing

2. **Sports Contrarian (Schedule TBD)**
   - Hypothesis: Crowd overreacts to recent performance; early-week odds vs late-week adjustments
   - Test: Place opposite-consensus bets on games resolving same day
   - Resolution: 1 day (game time)
   - Status: Pending sports calendar

3. **Economic Data Edge**
   - Hypothesis: Market prices in consensus forecasts; actual data often surprises both ways
   - Test: Bet on jobless claims, CPI, PMI above/below consensus on release day
   - Resolution: Same day as data release (Thursdays typically)
   - Status: Testing on next scheduled releases

### Past Strategies (Long-dated, removed from active rotation)
- Ukraine ceasefire (44 days) — too slow feedback
- Iran strikes (44 days) — too slow feedback
- JD Vance 2028 (1046 days) — too slow feedback
- Fed Q1 cuts (42 days) — too slow feedback

## File Structure

```
projects/polymarket-trader/
├── data/
│   ├── paper_bets.json                 # All paper bets (cumulative)
│   ├── strategy_performance.json       # Win rates by strategy (weekly updates)
│   └── weekly_summary.json             # Performance summaries per week
├── research/
│   └── SHORT_MARKETID_DATE.md          # Quick 1-pagers (resolves soon)
├── scripts/
│   └── resolve_bets.py                 # Mark bets as won/lost weekly
└── polymarket_trader.py                # Main CLI
```

## Success Criteria

**Phase 1: Edge Discovery (Weeks 1-4)**
- Test 3+ strategies
- 20+ paper bets completed
- Win rate >52% on any strategy
- Identify 1 repeatable edge

**Phase 2: Optimization (Weeks 5-8)**
- Scale winning strategy
- 50+ bets per week on best strategy
- Win rate >55%
- ROI >10% per week
- Report to Tomer

**Phase 3: Real Money (TBD)**
- Deploy capital on proven strategy
- Live trading with position sizing
- Continuous monitoring
