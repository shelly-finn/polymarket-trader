#!/usr/bin/env python3
"""
SEC Filing Monitor - Heartbeat Integration
Checks watchlist companies for new filings and extracts risk factors.

Usage (from heartbeat):
    python scripts/sec_monitor.py --check
    python scripts/sec_monitor.py --extract AAPL
    python scripts/sec_monitor.py --compare AAPL --years 2024,2025
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "projects" / "ai-investment-agent"))

from sec_edgar_fetcher import (
    get_company_filings, filter_filings,
    get_filing_url, fetch_filing_content, extract_risk_factors, fetch_url
)
import json as json_lib

def get_cik_from_ticker(ticker: str) -> str:
    """Look up CIK from ticker using company_tickers.json (more reliable)."""
    url = "https://www.sec.gov/files/company_tickers.json"
    data = fetch_url(url, timeout=30)
    if data:
        try:
            tickers = json_lib.loads(data)
            for entry in tickers.values():
                if entry.get("ticker", "").upper() == ticker.upper():
                    return str(entry.get("cik_str", "")).zfill(10)
        except:
            pass
    return None

WORKSPACE = Path(__file__).parent.parent
WATCHLIST_FILE = WORKSPACE / "projects" / "ai-investment-agent" / "watchlist.json"
DATA_DIR = WORKSPACE / "projects" / "ai-investment-agent" / "data"
INSIGHTS_FILE = WORKSPACE / "projects" / "ai-investment-agent" / "insights.json"


def load_watchlist() -> dict:
    """Load the company watchlist."""
    if WATCHLIST_FILE.exists():
        return json.loads(WATCHLIST_FILE.read_text())
    return {"companies": []}


def save_watchlist(watchlist: dict):
    """Save the watchlist with updates."""
    watchlist["updated"] = datetime.utcnow().strftime("%Y-%m-%d")
    WATCHLIST_FILE.write_text(json.dumps(watchlist, indent=2))


def load_insights() -> dict:
    """Load existing insights."""
    if INSIGHTS_FILE.exists():
        return json.loads(INSIGHTS_FILE.read_text())
    return {"insights": [], "last_scan": None}


def save_insights(insights: dict):
    """Save insights."""
    INSIGHTS_FILE.write_text(json.dumps(insights, indent=2))


def check_new_filings(days_back: int = 7) -> list:
    """Check watchlist for new filings in the last N days."""
    watchlist = load_watchlist()
    new_filings = []
    cutoff = datetime.utcnow() - timedelta(days=days_back)
    
    print(f"Checking {len(watchlist['companies'])} companies for filings since {cutoff.date()}...")
    
    for company in watchlist["companies"]:
        ticker = company["ticker"]
        try:
            cik = get_cik_from_ticker(ticker)
            if not cik:
                print(f"  {ticker}: Could not find CIK")
                continue
            
            filings_data = get_company_filings(cik)
            if not filings_data:
                continue
            
            # Check for recent 10-K or 10-Q
            for filing_type in ["10-K", "10-Q"]:
                filings = filter_filings(filings_data, filing_type, count=1)
                for filing in filings:
                    filing_date = datetime.strptime(filing["filing_date"], "%Y-%m-%d")
                    if filing_date >= cutoff:
                        # Check if we've already processed this
                        filing_id = f"{ticker}_{filing['filing_date']}_{filing_type}"
                        tracked = watchlist.get("filings_tracked", [])
                        
                        if filing_id not in tracked:
                            new_filings.append({
                                "ticker": ticker,
                                "name": company["name"],
                                "type": filing_type,
                                "date": filing["filing_date"],
                                "accession": filing["accession_number"],
                                "cik": cik,
                                "filing_id": filing_id
                            })
                            print(f"  {ticker}: NEW {filing_type} filed {filing['filing_date']}")
                        else:
                            print(f"  {ticker}: {filing_type} already processed")
        except Exception as e:
            print(f"  {ticker}: Error - {e}")
    
    watchlist["last_checked"] = datetime.utcnow().isoformat()
    save_watchlist(watchlist)
    
    return new_filings


def extract_and_save(ticker: str, filing_type: str = "10-K") -> dict:
    """Extract risk factors from a company's latest filing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    cik = get_cik_from_ticker(ticker)
    if not cik:
        return {"error": f"Could not find CIK for {ticker}"}
    
    filings_data = get_company_filings(cik)
    if not filings_data:
        return {"error": "Could not fetch filings data"}
    
    filings = filter_filings(filings_data, filing_type, count=1)
    if not filings:
        return {"error": f"No {filing_type} filings found"}
    
    filing = filings[0]
    url = get_filing_url(cik.lstrip("0"), filing["accession_number"], filing["primary_document"])
    
    print(f"Fetching {ticker} {filing_type} from {filing['filing_date']}...")
    content = fetch_filing_content(url)
    
    if not content:
        return {"error": "Could not fetch filing content"}
    
    risks = extract_risk_factors(content)
    if not risks:
        return {"error": "Could not extract risk factors"}
    
    # Save to file
    output_file = DATA_DIR / f"{ticker}_{filing['filing_date']}_risks.txt"
    output_file.write_text(risks)
    
    result = {
        "ticker": ticker,
        "filing_type": filing_type,
        "filing_date": filing["filing_date"],
        "chars_extracted": len(risks),
        "output_file": str(output_file),
        "preview": risks[:500] + "..."
    }
    
    print(f"Extracted {len(risks):,} chars -> {output_file}")
    return result


def process_new_filings(new_filings: list) -> list:
    """Process new filings: extract risks and generate insights."""
    insights = load_insights()
    watchlist = load_watchlist()
    results = []
    
    for filing in new_filings:
        ticker = filing["ticker"]
        filing_type = filing["type"]
        
        print(f"\nProcessing {ticker} {filing_type}...")
        result = extract_and_save(ticker, filing_type)
        
        if "error" not in result:
            # Mark as processed
            tracked = watchlist.get("filings_tracked", [])
            tracked.append(filing["filing_id"])
            watchlist["filings_tracked"] = tracked[-100:]  # Keep last 100
            
            # Add insight
            insight = {
                "date": datetime.utcnow().isoformat(),
                "ticker": ticker,
                "type": filing_type,
                "filing_date": result["filing_date"],
                "chars": result["chars_extracted"],
                "summary": f"New {filing_type} from {ticker} ({result['filing_date']}): {result['chars_extracted']:,} chars of risk factors extracted"
            }
            insights["insights"].append(insight)
            results.append(result)
        else:
            print(f"  Error: {result['error']}")
    
    insights["last_scan"] = datetime.utcnow().isoformat()
    save_insights(insights)
    save_watchlist(watchlist)
    
    return results


def heartbeat_check() -> str:
    """Run a heartbeat check - returns summary for the agent."""
    new_filings = check_new_filings(days_back=7)
    
    if not new_filings:
        return "SEC Monitor: No new filings in watchlist (last 7 days)"
    
    results = process_new_filings(new_filings)
    
    summary = f"SEC Monitor: Found {len(new_filings)} new filings\n"
    for r in results:
        summary += f"  - {r['ticker']}: {r['chars_extracted']:,} chars extracted\n"
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="SEC Filing Monitor")
    parser.add_argument("--check", action="store_true", help="Check for new filings (heartbeat mode)")
    parser.add_argument("--extract", help="Extract risk factors for a ticker")
    parser.add_argument("--list", action="store_true", help="List watchlist companies")
    parser.add_argument("--add", help="Add ticker to watchlist")
    
    args = parser.parse_args()
    
    if args.check:
        result = heartbeat_check()
        print(f"\n{result}")
    elif args.extract:
        result = extract_and_save(args.extract)
        print(json.dumps(result, indent=2))
    elif args.list:
        watchlist = load_watchlist()
        print("Watchlist:")
        for c in watchlist["companies"]:
            print(f"  {c['ticker']}: {c['name']} ({c['sector']})")
    elif args.add:
        watchlist = load_watchlist()
        # Would need to look up company name
        watchlist["companies"].append({"ticker": args.add.upper(), "name": "TBD", "sector": "TBD"})
        save_watchlist(watchlist)
        print(f"Added {args.add.upper()} to watchlist")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
