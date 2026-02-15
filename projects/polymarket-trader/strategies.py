#!/usr/bin/env python3
"""
Polymarket Trading Strategies
Identifies potential mispriced markets using various signals.
"""

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
import requests

WORKSPACE = Path(__file__).parent.parent.parent
DATA_DIR = WORKSPACE / "projects" / "polymarket-trader" / "data"
SIGNALS_FILE = DATA_DIR / "signals.json"
MARKET_CACHE_FILE = DATA_DIR / "market_cache.json"


def load_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class MarketAnalyzer:
    """Analyzes markets for trading opportunities."""
    
    def __init__(self):
        self.cache = load_json(MARKET_CACHE_FILE)
        self.markets = self.cache.get("markets", {})
    
    def find_extreme_prices(self, min_liquidity: float = 10000) -> list:
        """
        Find markets with extreme prices (1-10% or 90-99%) that might be mispriced.
        Extreme prices are where edge is highest if you're right.
        
        Strategy: If a market is priced at 5% YES, and you think it's actually 15%,
        you can 3x your money if right.
        """
        opportunities = []
        
        for market_id, market in self.markets.items():
            if market.get("liquidity", 0) < min_liquidity:
                continue
            
            yes_price = market.get("yes_price", 0.5)
            no_price = market.get("no_price", 0.5)
            
            # Look for extreme YES prices (undervalued YES)
            if 0.01 <= yes_price <= 0.15:
                opportunities.append({
                    "market_id": market_id,
                    "question": market.get("question"),
                    "signal": "EXTREME_LOW_YES",
                    "current_price": yes_price,
                    "potential_return": (1 / yes_price) - 1,  # If wins at $1
                    "liquidity": market.get("liquidity"),
                    "volume_24h": market.get("volume_24h"),
                    "reasoning": f"YES priced at {yes_price:.1%}. If actually >50% likely, massive upside."
                })
            
            # Look for extreme NO prices (undervalued NO) 
            if 0.01 <= no_price <= 0.15:
                opportunities.append({
                    "market_id": market_id,
                    "question": market.get("question"),
                    "signal": "EXTREME_LOW_NO",
                    "current_price": no_price,
                    "potential_return": (1 / no_price) - 1,
                    "liquidity": market.get("liquidity"),
                    "volume_24h": market.get("volume_24h"),
                    "reasoning": f"NO priced at {no_price:.1%}. If outcome unlikely, easy profit."
                })
        
        return sorted(opportunities, key=lambda x: x["potential_return"], reverse=True)
    
    def find_high_volume_movers(self, volume_threshold: float = 1000000) -> list:
        """
        Find markets with unusually high volume (potential information asymmetry).
        """
        movers = []
        
        for market_id, market in self.markets.items():
            volume = market.get("volume_24h", 0)
            liquidity = market.get("liquidity", 1)
            
            if volume >= volume_threshold:
                vol_to_liq = volume / liquidity if liquidity > 0 else 0
                
                movers.append({
                    "market_id": market_id,
                    "question": market.get("question"),
                    "signal": "HIGH_VOLUME",
                    "volume_24h": volume,
                    "liquidity": liquidity,
                    "vol_to_liq_ratio": vol_to_liq,
                    "yes_price": market.get("yes_price"),
                    "reasoning": f"${volume:,.0f} volume (ratio: {vol_to_liq:.1f}x). Smart money moving?"
                })
        
        return sorted(movers, key=lambda x: x["volume_24h"], reverse=True)
    
    def find_time_sensitive(self, hours_until_resolve: int = 48) -> list:
        """
        Find markets resolving soon where information edge matters most.
        """
        soon = []
        now = datetime.now(timezone.utc)
        
        for market_id, market in self.markets.items():
            end_date_str = market.get("end_date")
            if not end_date_str:
                continue
            
            try:
                # Parse end date
                end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
                time_left = end_date - now
                hours_left = time_left.total_seconds() / 3600
                
                if 0 < hours_left <= hours_until_resolve:
                    soon.append({
                        "market_id": market_id,
                        "question": market.get("question"),
                        "signal": "RESOLVING_SOON",
                        "hours_left": hours_left,
                        "end_date": end_date_str,
                        "yes_price": market.get("yes_price"),
                        "liquidity": market.get("liquidity"),
                        "reasoning": f"Resolves in {hours_left:.1f}h. Last chance for edge."
                    })
            except (ValueError, TypeError):
                continue
        
        return sorted(soon, key=lambda x: x["hours_left"])
    
    def find_political_opportunities(self) -> list:
        """
        Find political markets where news might create edge.
        """
        political = []
        political_keywords = [
            "trump", "biden", "election", "congress", "senate", 
            "president", "democrat", "republican", "nomination",
            "fed", "tariff", "ukraine", "china", "iran"
        ]
        
        for market_id, market in self.markets.items():
            question = market.get("question", "").lower()
            
            if any(kw in question for kw in political_keywords):
                political.append({
                    "market_id": market_id,
                    "question": market.get("question"),
                    "signal": "POLITICAL",
                    "yes_price": market.get("yes_price"),
                    "volume_24h": market.get("volume_24h"),
                    "liquidity": market.get("liquidity"),
                    "keywords": [kw for kw in political_keywords if kw in question]
                })
        
        return sorted(political, key=lambda x: x["volume_24h"], reverse=True)


def analyze_all() -> dict:
    """Run all analysis strategies and compile signals."""
    analyzer = MarketAnalyzer()
    
    signals = {
        "generated_at": utcnow(),
        "total_markets": len(analyzer.markets),
        "extreme_prices": analyzer.find_extreme_prices()[:20],
        "high_volume": analyzer.find_high_volume_movers()[:15],
        "resolving_soon": analyzer.find_time_sensitive()[:10],
        "political": analyzer.find_political_opportunities()[:15]
    }
    
    save_json(SIGNALS_FILE, signals)
    return signals


def print_signals(signals: dict):
    """Pretty print trading signals."""
    print(f"\n{'='*80}")
    print(f"POLYMARKET TRADING SIGNALS - {signals['generated_at'][:19]}")
    print(f"Analyzed {signals['total_markets']} markets")
    print(f"{'='*80}\n")
    
    print("🎯 EXTREME PRICES (high potential return):")
    print("-" * 60)
    for s in signals.get("extreme_prices", [])[:5]:
        print(f"  {s['signal']}: {s['question'][:50]}...")
        print(f"    Price: {s['current_price']:.1%} | Potential: {s['potential_return']:.0%} return")
        print(f"    Liquidity: ${s['liquidity']:,.0f}")
        print()
    
    print("\n📈 HIGH VOLUME (smart money?):")
    print("-" * 60)
    for s in signals.get("high_volume", [])[:5]:
        print(f"  {s['question'][:50]}...")
        print(f"    Volume: ${s['volume_24h']:,.0f} | YES: {s['yes_price']:.1%}")
        print()
    
    print("\n⏰ RESOLVING SOON:")
    print("-" * 60)
    for s in signals.get("resolving_soon", [])[:5]:
        print(f"  {s['question'][:50]}...")
        print(f"    {s['hours_left']:.1f}h left | YES: {s['yes_price']:.1%}")
        print()
    
    print("\n🏛️ POLITICAL MARKETS:")
    print("-" * 60)
    for s in signals.get("political", [])[:5]:
        print(f"  {s['question'][:50]}...")
        print(f"    YES: {s['yes_price']:.1%} | Volume: ${s['volume_24h']:,.0f}")
        print()


if __name__ == "__main__":
    print("Analyzing markets...")
    signals = analyze_all()
    print_signals(signals)
    print(f"\nSignals saved to {SIGNALS_FILE}")
