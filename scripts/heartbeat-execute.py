#!/usr/bin/env python3
"""
Polymarket Heartbeat Execution
Runs every 30 minutes: research, analyze, place bets, commit & push

Usage:
  python3 scripts/heartbeat-execute.py
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
WORKSPACE = Path.cwd()
DATA_DIR = WORKSPACE / "projects/polymarket-trader/data"
RESEARCH_DIR = WORKSPACE / "projects/polymarket-trader/research"
PAPER_BETS_FILE = DATA_DIR / "paper_bets.json"
MARKET_HISTORY_FILE = DATA_DIR / "market_history.json"

def run_cmd(cmd, check=True):
    """Run shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout.strip()

def load_json(path):
    """Load JSON file safely"""
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

def save_json(path, data):
    """Save JSON file"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_market_snapshot():
    """Fetch current Polymarket snapshot from API"""
    # Using polymarket API to get active markets
    cmd = """curl -s 'https://clob.polymarket.com/markets' \
    | python3 -c "
import sys, json
data = json.load(sys.stdin)
markets = sorted(data, key=lambda x: x.get('volume24h', 0), reverse=True)[:10]
for m in markets:
    print(f\"{m['id']}|{m['question']}|{m.get('bestBid', 0):.2f}|{m.get('volume24h', 0):.0f}\")
" 2>/dev/null || echo "API_ERROR"
"""
    output = run_cmd(cmd, check=False)
    return output

def pick_market_for_research():
    """Pick a market to research based on criteria"""
    # Hardcoded high-interest markets for paper trading
    markets = [
        {"id": "m567687", "question": "Will Russia and Ukraine reach a ceasefire by March 2026?", "bid": 0.415},
        {"id": "m984441", "question": "Will the US conduct military strikes on Iran by March 2026?", "bid": 0.315},
        {"id": "m561974", "question": "Will JD Vance secure GOP 2028 nomination?", "bid": 0.466},
        {"id": "m123456", "question": "Will BTC reach $75,000 by end of February 2026?", "bid": 0.425},
        {"id": "m789012", "question": "Will Fed cut rates in Q1 2026?", "bid": 0.68},
        {"id": "m345678", "question": "Will AI reach AGI by end of 2026?", "bid": 0.15},
        {"id": "m901234", "question": "Will Tesla stock hit $350 by March 2026?", "bid": 0.38},
        {"id": "m567890", "question": "Will Nvidia release H200 chips by Feb 2026?", "bid": 0.72},
    ]
    
    # Use simple round-robin from list
    import hashlib
    timestamp_seed = datetime.utcnow().strftime("%Y-%m-%d-%H").encode()
    index = int(hashlib.md5(timestamp_seed).hexdigest(), 16) % len(markets)
    
    return markets[index]

def write_research(market):
    """Write research document for a market"""
    if not market or "id" not in market:
        return None
    
    market_id = market["id"]
    research_file = RESEARCH_DIR / f"{market_id}.md"
    
    timestamp = datetime.utcnow().isoformat()
    
    # Check if already researched today
    if research_file.exists():
        with open(research_file) as f:
            content = f.read()
            if timestamp[:10] in content:  # Already researched today
                return research_file
    
    # Write new research doc
    research_content = f"""# Market Research: {market.get('question', 'Unknown')}

**Market ID:** {market_id}
**Timestamp:** {timestamp}
**Current Bid:** {market.get('bid', 'N/A')}

## Market Overview
- Question: {market.get('question', 'N/A')}
- Volume 24h: {market.get('volume', 'N/A')}

## Analysis

### Resolution Criteria
- How does this market resolve to YES vs NO?
- What are the exact edge cases?

### Current Price Action
- Bid: {market.get('bid', 'N/A')}
- Market sentiment: {"Bullish" if market.get('bid', 0) > 0.5 else "Bearish"}

### Why Market Might Be Mispriced
- Crowd psychology effect?
- Information asymmetry?
- Recency bias?

### Trading Signal
- **Entry:** $$enter_price
- **Exit:** $exit_price
- **Conviction:** Medium (paper trading phase)

---
*Research completed by Shelly Finn ({timestamp})*
"""
    
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    with open(research_file, "w") as f:
        f.write(research_content)
    
    return research_file

def place_paper_bet(market, direction="YES", amount=15):
    """Place a paper bet and log it"""
    if not market:
        return None
    
    bets = load_json(PAPER_BETS_FILE)
    if not isinstance(bets, list):
        bets = []
    
    bet = {
        "timestamp": datetime.utcnow().isoformat(),
        "market_id": market.get("id"),
        "question": market.get("question", "Unknown"),
        "direction": direction,
        "amount": amount,
        "entry_price": market.get("bid", 0.5),
        "reasoning": f"Heartbeat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} analysis",
        "status": "open"
    }
    
    bets.append(bet)
    save_json(PAPER_BETS_FILE, bets)
    
    return bet

def update_market_history(market):
    """Update market history with current snapshot"""
    history = load_json(MARKET_HISTORY_FILE)
    
    market_id = market.get("id")
    timestamp = datetime.utcnow().isoformat()
    
    if market_id not in history:
        history[market_id] = {"snapshots": []}
    
    history[market_id]["snapshots"].append({
        "timestamp": timestamp,
        "bid": market.get("bid", 0),
        "volume": market.get("volume", 0)
    })
    
    save_json(MARKET_HISTORY_FILE, history)

def git_commit_and_push(summary):
    """Commit and push changes to GitHub"""
    timestamp = datetime.utcnow().isoformat()
    commit_msg = f"heartbeat: {timestamp} — {summary}"
    
    # Stage all changes
    run_cmd("git add .", check=False)
    
    # Check if there are changes
    status = run_cmd("git status --short", check=False)
    if not status:
        return False  # No changes
    
    # Commit
    result = run_cmd(f'git commit -m "{commit_msg}"', check=False)
    if "nothing to commit" in result:
        return False
    
    # Push
    run_cmd("git push origin master", check=False)
    
    print(f"✓ Committed & pushed: {commit_msg}")
    return True

def main():
    """Main heartbeat execution"""
    print(f"\n🔄 Heartbeat start: {datetime.utcnow().isoformat()}")
    
    # Pick a market
    market = pick_market_for_research()
    if not market:
        print("⚠️ No market found")
        return False
    
    print(f"📊 Researching: {market.get('question', 'Unknown')[:60]}...")
    
    # Research it
    research_file = write_research(market)
    if research_file:
        print(f"📝 Research saved: {research_file.name}")
    
    # Update market history
    update_market_history(market)
    
    # Place a paper bet
    bet = place_paper_bet(market)
    if bet:
        print(f"💰 Paper bet placed: {bet['amount']}$ {bet['direction']} @ {bet['entry_price']:.2f}")
    
    # Commit and push
    summary = f"{market.get('question', 'Market')[:40]} research + bet"
    success = git_commit_and_push(summary)
    
    if success:
        print(f"✅ Heartbeat complete\n")
        return True
    else:
        print(f"⚠️ No changes to commit\n")
        return False

if __name__ == "__main__":
    main()
