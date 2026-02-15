#!/usr/bin/env python3
"""
Risk Factor Comparator
Compares risk factors between two SEC 10-K filings to identify changes.

Usage:
    python risk_comparator.py AAPL --years 2024,2025
"""

import argparse
import difflib
import gzip
import json
import re
import sys
from pathlib import Path
from typing import Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

HEADERS = {
    "User-Agent": "Shelly Finn shellyfinn9@gmail.com",
    "Accept-Encoding": "gzip, deflate",
}


def fetch_url(url: str, timeout: int = 60) -> Optional[str]:
    """Fetch URL with gzip handling."""
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=timeout) as response:
            data = response.read()
            if response.info().get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
            return data.decode("utf-8", errors="ignore")
    except (HTTPError, URLError) as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
    return None


def get_company_info(ticker: str) -> Tuple[Optional[str], str]:
    """Get CIK and company name for ticker."""
    url = "https://www.sec.gov/files/company_tickers.json"
    data = fetch_url(url, timeout=30)
    
    if data:
        try:
            tickers = json.loads(data)
            for entry in tickers.values():
                if entry.get("ticker", "").upper() == ticker.upper():
                    cik = str(entry.get("cik_str", "")).zfill(10)
                    name = entry.get("title", "Unknown")
                    return cik, name
        except json.JSONDecodeError:
            pass
    
    return None, "Unknown"


def get_10k_filings(cik: str, count: int = 5) -> list:
    """Get recent 10-K filings for a company."""
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    data = fetch_url(url)
    
    if not data:
        return []
    
    try:
        filings_data = json.loads(data)
        recent = filings_data.get("filings", {}).get("recent", {})
        
        forms = recent.get("form", [])
        accession_numbers = recent.get("accessionNumber", [])
        filing_dates = recent.get("filingDate", [])
        primary_docs = recent.get("primaryDocument", [])
        
        results = []
        for i, form in enumerate(forms):
            if form == "10-K" and len(results) < count:
                year = filing_dates[i][:4]
                results.append({
                    "year": year,
                    "filing_date": filing_dates[i],
                    "accession_number": accession_numbers[i],
                    "primary_document": primary_docs[i],
                    "cik": cik.lstrip("0"),
                })
        
        return results
    except (json.JSONDecodeError, KeyError):
        return []


def get_filing_url(filing: dict) -> str:
    """Construct URL to filing document."""
    acc = filing["accession_number"].replace("-", "")
    return f"https://www.sec.gov/Archives/edgar/data/{filing['cik']}/{acc}/{filing['primary_document']}"


def extract_risk_factors_html(html: str) -> str:
    """Extract risk factors from 10-K HTML filing with robust XBRL handling."""
    
    # Step 1: Strip script and style tags first
    html_cleaned = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    html_cleaned = re.sub(r'<style[^>]*>.*?</style>', ' ', html_cleaned, flags=re.DOTALL | re.IGNORECASE)
    
    # Step 2: Find Risk Factors section with flexible patterns
    patterns = [
        # XBRL format: Item 1A with flexible spacing/tags + Risk Factors
        r'(?i)Item\s+1A[.\s]*(?:<[^>]*>)?(?:&#160;)*\s*Risk\s+Factors\s*(?:<[^>]*>)?\s*(.*?)(?:Item\s+1B|Item\s+2[^0-9])',
        # Simpler: just Risk Factors section
        r'(?i)Risk\s+Factors\s*(?:<[^>]*>)?\s*(.*?)(?:Item\s+1B|Item\s+2[^0-9])',
        # Very broad fallback
        r'(?i)Risk\s+Factors(.*?)Item\s+1B',
    ]
    
    text = None
    for pattern in patterns:
        match = re.search(pattern, html_cleaned, re.DOTALL | re.IGNORECASE)
        if match:
            # Get the captured group
            if match.lastindex and match.lastindex > 0:
                text = match.group(match.lastindex)
            else:
                text = match.group(0)
            
            # Verify meaningful content
            if text and len(text.strip()) > 300:
                break
            text = None
    
    if not text:
        return ""
    
    # Step 3: Clean up HTML/XBRL tags
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)  # HTML comments
    text = re.sub(r'<[^>]+>', ' ', text)  # All tags
    
    # Step 4: Decode HTML entities
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&apos;', "'", text)
    # Handle numeric entities carefully
    try:
        text = re.sub(r'&#x([0-9a-fA-F]+);', lambda m: chr(int(m.group(1), 16)) if int(m.group(1), 16) < 1114112 else '?', text)
        text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))) if int(m.group(1)) < 1114112 else '?', text)
    except (ValueError, OverflowError):
        pass
    text = re.sub(r'&[a-z]+;', ' ', text)  # Remaining entities
    
    # Step 5: Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Return if substantial content found
    if len(text) > 500:
        return text[:150000]  # Increased limit for XBRL filings
    
    return ""


def compare_risks(old_text: str, new_text: str) -> dict:
    """Compare two risk factor texts and identify changes."""
    # Split into paragraphs/sentences for comparison
    old_lines = [s.strip() for s in re.split(r'[.!?]\s+', old_text) if len(s.strip()) > 50]
    new_lines = [s.strip() for s in re.split(r'[.!?]\s+', new_text) if len(s.strip()) > 50]
    
    # Find new risks (in new but not in old)
    old_set = set(old_lines)
    new_set = set(new_lines)
    
    added = new_set - old_set
    removed = old_set - new_set
    
    # Calculate similarity
    matcher = difflib.SequenceMatcher(None, old_text[:50000], new_text[:50000])
    similarity = matcher.ratio()
    
    return {
        "similarity": round(similarity * 100, 1),
        "added_statements": len(added),
        "removed_statements": len(removed),
        "sample_added": list(added)[:5],
        "sample_removed": list(removed)[:5],
    }


def main():
    parser = argparse.ArgumentParser(description="Compare 10-K risk factors year over year")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--years", default="2024,2025", help="Years to compare (comma-separated)")
    parser.add_argument("--output", help="Output file for comparison report")
    
    args = parser.parse_args()
    years = [y.strip() for y in args.years.split(",")]
    
    if len(years) != 2:
        print("Please specify exactly two years to compare", file=sys.stderr)
        sys.exit(1)
    
    print(f"Looking up {args.ticker}...")
    cik, company_name = get_company_info(args.ticker)
    
    if not cik:
        print(f"Could not find CIK for {args.ticker}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Company: {company_name} (CIK: {cik})")
    print(f"Fetching 10-K filings...")
    
    filings = get_10k_filings(cik, count=10)
    
    # Find filings for requested years
    year_filings = {}
    for f in filings:
        if f["year"] in years:
            year_filings[f["year"]] = f
    
    if len(year_filings) != 2:
        available = [f["year"] for f in filings]
        print(f"Could not find filings for both years. Available: {available}", file=sys.stderr)
        sys.exit(1)
    
    # Fetch and extract risk factors
    risks = {}
    for year in years:
        filing = year_filings[year]
        url = get_filing_url(filing)
        print(f"  Fetching {year} filing from {url[:60]}...")
        
        html = fetch_url(url, timeout=120)
        if not html:
            print(f"  Could not fetch {year} filing", file=sys.stderr)
            continue
        
        risk_text = extract_risk_factors_html(html)
        if risk_text:
            risks[year] = risk_text
            print(f"  Extracted {len(risk_text):,} chars of risk factors")
        else:
            print(f"  Could not extract risk factors from {year} filing")
    
    if len(risks) != 2:
        print("Could not extract risk factors from both filings", file=sys.stderr)
        sys.exit(1)
    
    # Compare
    print(f"\nComparing {years[0]} vs {years[1]}...\n")
    comparison = compare_risks(risks[years[0]], risks[years[1]])
    
    print("=" * 60)
    print(f"RISK FACTOR COMPARISON: {args.ticker}")
    print(f"Company: {company_name}")
    print(f"Comparing: {years[0]} → {years[1]}")
    print("=" * 60)
    print(f"\nOverall similarity: {comparison['similarity']}%")
    print(f"New risk statements: {comparison['added_statements']}")
    print(f"Removed risk statements: {comparison['removed_statements']}")
    
    if comparison['sample_added']:
        print(f"\n--- Sample NEW risks in {years[1]} ---")
        for i, stmt in enumerate(comparison['sample_added'][:3], 1):
            print(f"\n{i}. {stmt[:300]}...")
    
    if comparison['sample_removed']:
        print(f"\n--- Sample REMOVED risks from {years[0]} ---")
        for i, stmt in enumerate(comparison['sample_removed'][:3], 1):
            print(f"\n{i}. {stmt[:300]}...")
    
    # Save report
    if args.output:
        report = {
            "ticker": args.ticker,
            "company": company_name,
            "years": years,
            "comparison": comparison,
            "risk_text": {y: risks[y][:10000] for y in years},
        }
        Path(args.output).write_text(json.dumps(report, indent=2))
        print(f"\nFull report saved to {args.output}")
    
    print("\nDone.")


if __name__ == "__main__":
    main()
