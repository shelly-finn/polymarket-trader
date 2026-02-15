#!/usr/bin/env python3
"""
Polymarket Paper Trading System
Simulates trades, tracks outcomes, tests strategies.

Usage:
    python polymarket_trader.py --scan          # Scan for opportunities
    python polymarket_trader.py --bet MARKET_ID YES 0.50 100  # Paper bet
    python polymarket_trader.py --check         # Check open paper bets
    python polymarket_trader.py --history       # View bet history
    python polymarket_trader.py --performance   # Calculate P&L
"""

import argparse
import json
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# API endpoints
GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"

# Local storage
WORKSPACE = Path(__file__).parent.parent.parent
DATA_DIR = WORKSPACE / "projects" / "polymarket-trader" / "data"
PAPER_BETS_FILE = DATA_DIR / "paper_bets.json"
MARKET_CACHE_FILE = DATA_DIR / "market_cache.json"
PERFORMANCE_FILE = DATA_DIR / "performance.json"


def utcnow() -> str:
    """Get current UTC time as ISO string."""
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    """Load JSON file or return empty structure."""
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_json(path: Path, data: dict):
    """Save data to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def fetch_active_events(limit: int = 50, tag_id: Optional[int] = None) -> list:
    """Fetch active events from Polymarket."""
    params = {
        "active": "true",
        "closed": "false",
        "limit": limit,
        "order": "volume24hr",
        "ascending": "false"
    }
    if tag_id:
        params["tag_id"] = tag_id
    
    try:
        resp = requests.get(f"{GAMMA_API}/events", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []


def fetch_market_price(token_id: str, side: str = "buy") -> Optional[float]:
    """Get current price for a token."""
    try:
        resp = requests.get(
            f"{CLOB_API}/price",
            params={"token_id": token_id, "side": side},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        return float(data.get("price", 0))
    except Exception as e:
        print(f"Error fetching price for {token_id[:20]}...: {e}")
        return None


def fetch_orderbook(token_id: str) -> dict:
    """Get orderbook depth for a token."""
    try:
        resp = requests.get(
            f"{CLOB_API}/book",
            params={"token_id": token_id},
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching orderbook: {e}")
        return {}


def scan_markets(limit: int = 20) -> list:
    """Scan for interesting market opportunities."""
    events = fetch_active_events(limit=limit)
    opportunities = []
    
    for event in events:
        for market in event.get("markets", []):
            try:
                outcomes = json.loads(market.get("outcomes", "[]"))
                prices = json.loads(market.get("outcomePrices", "[]"))
                
                if len(outcomes) >= 2 and len(prices) >= 2:
                    yes_price = float(prices[0])
                    no_price = float(prices[1])
                    
                    # Get additional market info
                    volume = float(market.get("volumeNum", 0))
                    liquidity = float(market.get("liquidityNum", 0))
                    
                    opportunities.append({
                        "event_id": event.get("id"),
                        "event_title": event.get("title"),
                        "market_id": market.get("id"),
                        "question": market.get("question"),
                        "slug": market.get("slug"),
                        "yes_price": yes_price,
                        "no_price": no_price,
                        "volume_24h": volume,
                        "liquidity": liquidity,
                        "token_ids": market.get("clobTokenIds", []),
                        "end_date": market.get("endDate"),
                        "fetched_at": utcnow()
                    })
            except (json.JSONDecodeError, ValueError, TypeError) as e:
                continue
    
    # Sort by volume
    opportunities.sort(key=lambda x: x["volume_24h"], reverse=True)
    
    # Cache for later reference
    cache = load_json(MARKET_CACHE_FILE)
    cache["markets"] = {m["market_id"]: m for m in opportunities}
    cache["updated"] = utcnow()
    save_json(MARKET_CACHE_FILE, cache)
    
    return opportunities


def place_paper_bet(
    market_id: str,
    outcome: str,  # "YES" or "NO"
    price: float,
    amount: float,
    reasoning: str = ""
) -> dict:
    """Record a paper bet."""
    bets = load_json(PAPER_BETS_FILE)
    if "bets" not in bets:
        bets["bets"] = []
    
    # Get market info from cache
    cache = load_json(MARKET_CACHE_FILE)
    market = cache.get("markets", {}).get(market_id, {})
    
    bet = {
        "id": f"bet_{len(bets['bets']) + 1}_{int(datetime.now().timestamp())}",
        "market_id": market_id,
        "question": market.get("question", "Unknown"),
        "outcome": outcome.upper(),
        "entry_price": price,
        "amount": amount,  # In USDC
        "shares": amount / price if price > 0 else 0,
        "reasoning": reasoning,
        "placed_at": utcnow(),
        "status": "open",  # open, won, lost, sold
        "exit_price": None,
        "exit_at": None,
        "pnl": None
    }
    
    bets["bets"].append(bet)
    bets["updated"] = utcnow()
    save_json(PAPER_BETS_FILE, bets)
    
    return bet


def check_open_bets() -> list:
    """Check status of open paper bets and update prices."""
    bets = load_json(PAPER_BETS_FILE)
    open_bets = [b for b in bets.get("bets", []) if b["status"] == "open"]
    
    cache = load_json(MARKET_CACHE_FILE)
    
    for bet in open_bets:
        market = cache.get("markets", {}).get(bet["market_id"], {})
        if market:
            # Get current price
            idx = 0 if bet["outcome"] == "YES" else 1
            current_price = market.get("yes_price" if idx == 0 else "no_price", bet["entry_price"])
            
            bet["current_price"] = current_price
            bet["unrealized_pnl"] = (current_price - bet["entry_price"]) * bet["shares"]
            bet["unrealized_pnl_pct"] = ((current_price / bet["entry_price"]) - 1) * 100 if bet["entry_price"] > 0 else 0
    
    return open_bets


def resolve_bet(bet_id: str, outcome: str) -> dict:
    """Mark a bet as won or lost based on market resolution."""
    bets = load_json(PAPER_BETS_FILE)
    
    for bet in bets.get("bets", []):
        if bet["id"] == bet_id and bet["status"] == "open":
            bet["status"] = outcome.lower()  # "won" or "lost"
            bet["exit_at"] = utcnow()
            
            if outcome.lower() == "won":
                bet["exit_price"] = 1.0
                bet["pnl"] = bet["shares"] - bet["amount"]  # shares worth $1 each
            else:
                bet["exit_price"] = 0.0
                bet["pnl"] = -bet["amount"]  # lost entire bet
            
            save_json(PAPER_BETS_FILE, bets)
            return bet
    
    return {}


def calculate_performance() -> dict:
    """Calculate overall trading performance."""
    bets = load_json(PAPER_BETS_FILE)
    all_bets = bets.get("bets", [])
    
    if not all_bets:
        return {"error": "No bets recorded"}
    
    closed_bets = [b for b in all_bets if b["status"] in ["won", "lost", "sold"]]
    open_bets = [b for b in all_bets if b["status"] == "open"]
    
    total_invested = sum(b["amount"] for b in all_bets)
    realized_pnl = sum(b.get("pnl", 0) for b in closed_bets if b.get("pnl") is not None)
    
    wins = len([b for b in closed_bets if b["status"] == "won"])
    losses = len([b for b in closed_bets if b["status"] == "lost"])
    
    performance = {
        "total_bets": len(all_bets),
        "open_bets": len(open_bets),
        "closed_bets": len(closed_bets),
        "wins": wins,
        "losses": losses,
        "win_rate": wins / len(closed_bets) * 100 if closed_bets else 0,
        "total_invested": total_invested,
        "realized_pnl": realized_pnl,
        "roi": realized_pnl / total_invested * 100 if total_invested > 0 else 0,
        "calculated_at": utcnow()
    }
    
    save_json(PERFORMANCE_FILE, performance)
    return performance


def print_opportunities(opportunities: list, limit: int = 10):
    """Print market opportunities in a readable format."""
    print(f"\n{'='*80}")
    print(f"TOP {limit} MARKETS BY 24H VOLUME")
    print(f"{'='*80}\n")
    
    for i, m in enumerate(opportunities[:limit], 1):
        print(f"{i}. {m['question'][:70]}...")
        print(f"   YES: {m['yes_price']:.1%} | NO: {m['no_price']:.1%}")
        print(f"   Volume 24h: ${m['volume_24h']:,.0f} | Liquidity: ${m['liquidity']:,.0f}")
        print(f"   Market ID: {m['market_id']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Polymarket Paper Trader")
    parser.add_argument("--scan", action="store_true", help="Scan for market opportunities")
    parser.add_argument("--bet", nargs=4, metavar=("MARKET_ID", "OUTCOME", "PRICE", "AMOUNT"),
                       help="Place a paper bet")
    parser.add_argument("--reason", default="", help="Reasoning for the bet")
    parser.add_argument("--check", action="store_true", help="Check open bets")
    parser.add_argument("--history", action="store_true", help="View bet history")
    parser.add_argument("--performance", action="store_true", help="Calculate performance")
    parser.add_argument("--resolve", nargs=2, metavar=("BET_ID", "OUTCOME"),
                       help="Resolve a bet (won/lost)")
    parser.add_argument("--limit", type=int, default=20, help="Number of results")
    
    args = parser.parse_args()
    
    if args.scan:
        print("Scanning markets...")
        opportunities = scan_markets(limit=args.limit)
        print_opportunities(opportunities, limit=args.limit)
        print(f"Cached {len(opportunities)} markets to {MARKET_CACHE_FILE}")
        
    elif args.bet:
        market_id, outcome, price, amount = args.bet
        bet = place_paper_bet(
            market_id=market_id,
            outcome=outcome,
            price=float(price),
            amount=float(amount),
            reasoning=args.reason
        )
        print(f"\n✅ Paper bet placed!")
        print(f"   ID: {bet['id']}")
        print(f"   Market: {bet['question'][:50]}...")
        print(f"   Outcome: {bet['outcome']} @ {bet['entry_price']:.1%}")
        print(f"   Amount: ${bet['amount']:.2f} ({bet['shares']:.2f} shares)")
        print(f"   Reasoning: {bet['reasoning']}")
        
    elif args.check:
        open_bets = check_open_bets()
        if not open_bets:
            print("\nNo open bets.")
        else:
            print(f"\n{'='*60}")
            print(f"OPEN PAPER BETS ({len(open_bets)})")
            print(f"{'='*60}\n")
            for bet in open_bets:
                print(f"ID: {bet['id']}")
                print(f"   {bet['question'][:50]}...")
                print(f"   {bet['outcome']} @ {bet['entry_price']:.1%}")
                print(f"   Amount: ${bet['amount']:.2f}")
                if "current_price" in bet:
                    print(f"   Current: {bet['current_price']:.1%} | P&L: ${bet['unrealized_pnl']:.2f} ({bet['unrealized_pnl_pct']:.1f}%)")
                print()
                
    elif args.history:
        bets = load_json(PAPER_BETS_FILE)
        all_bets = bets.get("bets", [])
        if not all_bets:
            print("\nNo bets recorded.")
        else:
            print(f"\n{'='*60}")
            print(f"BET HISTORY ({len(all_bets)} total)")
            print(f"{'='*60}\n")
            for bet in all_bets[-10:]:  # Last 10
                status_emoji = {"open": "⏳", "won": "✅", "lost": "❌", "sold": "💰"}.get(bet["status"], "?")
                pnl_str = f"P&L: ${bet.get('pnl', 0):.2f}" if bet.get("pnl") is not None else ""
                print(f"{status_emoji} {bet['outcome']} @ {bet['entry_price']:.1%} - ${bet['amount']:.2f} {pnl_str}")
                print(f"   {bet['question'][:60]}...")
                print()
                
    elif args.performance:
        perf = calculate_performance()
        if "error" in perf:
            print(f"\n{perf['error']}")
        else:
            print(f"\n{'='*60}")
            print(f"PAPER TRADING PERFORMANCE")
            print(f"{'='*60}\n")
            print(f"Total Bets: {perf['total_bets']}")
            print(f"Open: {perf['open_bets']} | Closed: {perf['closed_bets']}")
            print(f"Wins: {perf['wins']} | Losses: {perf['losses']}")
            print(f"Win Rate: {perf['win_rate']:.1f}%")
            print(f"Total Invested: ${perf['total_invested']:.2f}")
            print(f"Realized P&L: ${perf['realized_pnl']:.2f}")
            print(f"ROI: {perf['roi']:.1f}%")
            
    elif args.resolve:
        bet_id, outcome = args.resolve
        bet = resolve_bet(bet_id, outcome)
        if bet:
            print(f"\n✅ Bet resolved: {bet_id} -> {outcome}")
            print(f"   P&L: ${bet.get('pnl', 0):.2f}")
        else:
            print(f"\n❌ Bet not found or already closed: {bet_id}")
            
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
