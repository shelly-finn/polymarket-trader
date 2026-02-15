#!/usr/bin/env python3
"""
Polymarket Research Tools
Deep analysis of individual markets for trading edge.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import requests

WORKSPACE = Path(__file__).parent.parent.parent
DATA_DIR = WORKSPACE / "projects" / "polymarket-trader" / "data"
RESEARCH_DIR = WORKSPACE / "projects" / "polymarket-trader" / "research"
MARKET_CACHE = DATA_DIR / "market_cache.json"
MARKET_HISTORY = DATA_DIR / "market_history.json"

GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"


def load_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch_market_detail(market_id: str) -> dict:
    """Fetch detailed market info from Gamma API."""
    try:
        resp = requests.get(f"{GAMMA_API}/markets/{market_id}", timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching market {market_id}: {e}")
        return {}


def fetch_orderbook(token_id: str) -> dict:
    """Get full orderbook for a token."""
    try:
        resp = requests.get(f"{CLOB_API}/book", params={"token_id": token_id}, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching orderbook: {e}")
        return {}


def analyze_orderbook(orderbook: dict) -> dict:
    """Analyze orderbook for trading insights."""
    bids = orderbook.get("bids", [])
    asks = orderbook.get("asks", [])
    
    if not bids or not asks:
        return {"error": "Empty orderbook"}
    
    best_bid = float(bids[0]["price"]) if bids else 0
    best_ask = float(asks[0]["price"]) if asks else 1
    spread = best_ask - best_bid
    spread_pct = spread / best_ask * 100 if best_ask > 0 else 0
    
    bid_depth = sum(float(b["size"]) for b in bids[:5])
    ask_depth = sum(float(a["size"]) for a in asks[:5])
    
    return {
        "best_bid": best_bid,
        "best_ask": best_ask,
        "spread": spread,
        "spread_pct": spread_pct,
        "bid_depth_5": bid_depth,
        "ask_depth_5": ask_depth,
        "imbalance": (bid_depth - ask_depth) / (bid_depth + ask_depth) if (bid_depth + ask_depth) > 0 else 0
    }


def track_price_history(market_id: str, yes_price: float, no_price: float):
    """Log price to history for tracking over time."""
    history = load_json(MARKET_HISTORY)
    
    if market_id not in history:
        history[market_id] = {"prices": []}
    
    history[market_id]["prices"].append({
        "timestamp": utcnow(),
        "yes": yes_price,
        "no": no_price
    })
    
    # Keep last 1000 data points per market
    history[market_id]["prices"] = history[market_id]["prices"][-1000:]
    
    save_json(MARKET_HISTORY, history)


def calculate_price_momentum(market_id: str, hours: int = 24) -> dict:
    """Calculate price momentum over time period."""
    history = load_json(MARKET_HISTORY)
    
    if market_id not in history:
        return {"error": "No history"}
    
    prices = history[market_id].get("prices", [])
    if len(prices) < 2:
        return {"error": "Insufficient history"}
    
    # Get prices from N hours ago
    cutoff = datetime.now(timezone.utc).timestamp() - (hours * 3600)
    recent = [p for p in prices if datetime.fromisoformat(p["timestamp"]).timestamp() > cutoff]
    
    if len(recent) < 2:
        return {"error": "Insufficient recent data"}
    
    start_price = recent[0]["yes"]
    end_price = recent[-1]["yes"]
    change = end_price - start_price
    change_pct = (change / start_price * 100) if start_price > 0 else 0
    
    return {
        "period_hours": hours,
        "start_price": start_price,
        "end_price": end_price,
        "change": change,
        "change_pct": change_pct,
        "data_points": len(recent)
    }


def generate_research_template(market_id: str) -> str:
    """Generate a research template for a market."""
    cache = load_json(MARKET_CACHE)
    market = cache.get("markets", {}).get(market_id, {})
    
    if not market:
        # Try to fetch directly
        market = fetch_market_detail(market_id)
    
    question = market.get("question", "Unknown")
    yes_price = market.get("yes_price", 0.5)
    no_price = market.get("no_price", 0.5)
    volume = market.get("volume_24h", 0)
    liquidity = market.get("liquidity", 0)
    end_date = market.get("end_date", "Unknown")
    
    template = f"""# Market Research: {market_id}

## Basic Info
- **Question:** {question}
- **Current Price:** YES {yes_price:.1%} / NO {no_price:.1%}
- **24h Volume:** ${volume:,.0f}
- **Liquidity:** ${liquidity:,.0f}
- **End Date:** {end_date}
- **Research Date:** {utcnow()[:10]}

## Resolution Criteria
*How exactly does this market resolve? What are the edge cases?*

- [ ] TODO: Find official resolution criteria
- [ ] TODO: Identify potential ambiguities

## Market Analysis

### Why is the market priced here?
*What does the crowd believe? What's priced in?*



### What could make YES more likely?
*Events, news, developments that would move price up*



### What could make NO more likely?
*Events, news, developments that would move price down*



### Who has better information?
*Insiders, experts, institutions with edge*



## My Edge
*Why do I think I know better than the market?*



## Position Recommendation
- **Direction:** 
- **Conviction:** Low / Medium / High
- **Size:** $
- **Entry Price:** 
- **Target Exit:** 
- **Stop Loss:** 

## Sources & Notes


"""
    return template


def create_research_file(market_id: str) -> Path:
    """Create a research file for a market."""
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    
    filepath = RESEARCH_DIR / f"{market_id}.md"
    if not filepath.exists():
        template = generate_research_template(market_id)
        filepath.write_text(template)
        print(f"Created research file: {filepath}")
    else:
        print(f"Research file exists: {filepath}")
    
    return filepath


def find_research_opportunities(min_volume: float = 1000000, max_price: float = 0.85, min_price: float = 0.15) -> list:
    """Find markets worth researching (high volume, not too certain)."""
    cache = load_json(MARKET_CACHE)
    opportunities = []
    
    for market_id, market in cache.get("markets", {}).items():
        volume = market.get("volume_24h", 0)
        yes_price = market.get("yes_price", 0.5)
        liquidity = market.get("liquidity", 0)
        
        # Want high volume markets that aren't already at extreme prices
        if volume >= min_volume and min_price <= yes_price <= max_price and liquidity > 50000:
            opportunities.append({
                "market_id": market_id,
                "question": market.get("question"),
                "yes_price": yes_price,
                "volume_24h": volume,
                "liquidity": liquidity,
                "uncertainty": 1 - abs(yes_price - 0.5) * 2  # Higher = more uncertain
            })
    
    # Sort by volume * uncertainty (want high volume uncertain markets)
    opportunities.sort(key=lambda x: x["volume_24h"] * x["uncertainty"], reverse=True)
    return opportunities


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Polymarket Research Tools")
    parser.add_argument("--opportunities", action="store_true", help="Find research opportunities")
    parser.add_argument("--research", help="Create research file for market ID")
    parser.add_argument("--analyze", help="Analyze orderbook for market ID")
    parser.add_argument("--track", help="Track price for market ID")
    
    args = parser.parse_args()
    
    if args.opportunities:
        opps = find_research_opportunities()
        print(f"\n{'='*70}")
        print("TOP RESEARCH OPPORTUNITIES (High volume, uncertain)")
        print(f"{'='*70}\n")
        for o in opps[:15]:
            print(f"  {o['yes_price']:.1%} YES | ${o['volume_24h']:,.0f} vol | uncertainty: {o['uncertainty']:.2f}")
            print(f"  {o['question'][:65]}...")
            print(f"  ID: {o['market_id']}")
            print()
    
    elif args.research:
        filepath = create_research_file(args.research)
        print(f"\nResearch template created at: {filepath}")
        print("Fill in the template with your analysis.")
    
    elif args.analyze:
        cache = load_json(MARKET_CACHE)
        market = cache.get("markets", {}).get(args.analyze, {})
        token_ids = market.get("token_ids", [])
        if token_ids:
            print(f"\nAnalyzing orderbook for: {market.get('question', 'Unknown')[:50]}...")
            orderbook = fetch_orderbook(token_ids[0])
            analysis = analyze_orderbook(orderbook)
            print(json.dumps(analysis, indent=2))
    
    else:
        parser.print_help()
