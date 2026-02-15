#!/usr/bin/env python3
"""
SEC EDGAR Filing Retriever
Fetches 10-K and 10-Q filings from SEC EDGAR API

Usage:
    python sec_edgar_fetcher.py AAPL --filing-type 10-K --count 5
"""

import argparse
import gzip
import json
import re
import sys
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# SEC EDGAR API base URLs
EDGAR_COMPANY_SEARCH = "https://data.sec.gov/submissions/CIK{cik}.json"
EDGAR_FILING_BASE = "https://www.sec.gov/Archives/edgar/data"

# Required headers for SEC API
HEADERS = {
    "User-Agent": "Shelly Finn shellyfinn9@gmail.com",
    "Accept-Encoding": "gzip, deflate",
}


def fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch URL with gzip handling."""
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=timeout) as response:
            data = response.read()
            # Handle gzip encoding
            if response.info().get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
            return data.decode("utf-8", errors="ignore")
    except (HTTPError, URLError) as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
    return None


def get_cik_from_ticker(ticker: str) -> Optional[str]:
    """Look up CIK number from ticker symbol."""
    # SEC maintains a ticker-to-CIK mapping
    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=&dateb=&owner=include&count=1&output=json".format(ticker)
    
    data = fetch_url(url)
    if data:
        try:
            parsed = json.loads(data)
            if "results" in parsed and len(parsed["results"]) > 0:
                cik = parsed["results"][0].get("cik")
                return cik.zfill(10) if cik else None
        except json.JSONDecodeError:
            pass
    
    return None


def get_company_filings(cik: str) -> Optional[dict]:
    """Fetch company filing metadata from SEC EDGAR."""
    url = EDGAR_COMPANY_SEARCH.format(cik=cik)
    
    data = fetch_url(url)
    if data:
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            pass
    
    return None


def filter_filings(filings_data: dict, filing_type: str, count: int) -> list:
    """Filter filings by type and return most recent."""
    if "filings" not in filings_data or "recent" not in filings_data["filings"]:
        return []
    
    recent = filings_data["filings"]["recent"]
    forms = recent.get("form", [])
    accession_numbers = recent.get("accessionNumber", [])
    filing_dates = recent.get("filingDate", [])
    primary_documents = recent.get("primaryDocument", [])
    
    results = []
    for i, form in enumerate(forms):
        if form == filing_type and len(results) < count:
            results.append({
                "form": form,
                "accession_number": accession_numbers[i],
                "filing_date": filing_dates[i],
                "primary_document": primary_documents[i],
            })
    
    return results


def get_filing_url(cik: str, accession_number: str, primary_document: str) -> str:
    """Construct URL to the filing document."""
    accession_clean = accession_number.replace("-", "")
    return f"{EDGAR_FILING_BASE}/{cik}/{accession_clean}/{primary_document}"


def fetch_filing_content(url: str) -> Optional[str]:
    """Fetch the raw filing content."""
    return fetch_url(url, timeout=60)


def extract_risk_factors(content: str) -> Optional[str]:
    """Extract Risk Factors section from 10-K filing with robust XBRL/HTML handling."""
    
    # Step 1: Strip script and style tags first (they contain non-content)
    content_cleaned = re.sub(r'<script[^>]*>.*?</script>', ' ', content, flags=re.DOTALL | re.IGNORECASE)
    content_cleaned = re.sub(r'<style[^>]*>.*?</style>', ' ', content_cleaned, flags=re.DOTALL | re.IGNORECASE)
    
    # Step 2: Find the Risk Factors section - be flexible with HTML tags/spacing
    # These patterns are ordered from most to least specific
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
        match = re.search(pattern, content_cleaned, re.DOTALL | re.IGNORECASE)
        if match:
            # Get the captured group (content between markers)
            if match.lastindex and match.lastindex > 0:
                text = match.group(match.lastindex)
            else:
                text = match.group(0)
            
            # Verify we got meaningful content
            if text and len(text.strip()) > 300:
                break
            text = None
    
    if not text:
        return None
    
    # Step 3: Clean up HTML/XBRL tags comprehensively
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    # Remove all HTML/XML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Step 4: Decode HTML entities (both named and numeric)
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
        pass  # Skip invalid numeric entities
    text = re.sub(r'&[a-z]+;', ' ', text)  # Catch any remaining named entities
    
    # Step 5: Clean up whitespace and normalize
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Step 6: Remove control characters
    text = ''.join(c for c in text if ord(c) >= 32 or c in '\n\t\r')
    
    # Return if substantial content found
    if len(text) > 500:
        return text[:150000]  # Increased limit to 150K for XBRL filings
    
    return None


def main():
    parser = argparse.ArgumentParser(description="Fetch SEC EDGAR filings")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL)")
    parser.add_argument("--filing-type", default="10-K", help="Filing type (10-K, 10-Q, 8-K)")
    parser.add_argument("--count", type=int, default=3, help="Number of filings to fetch")
    parser.add_argument("--extract-risks", action="store_true", help="Extract risk factors section")
    parser.add_argument("--output", help="Output directory for filings")
    
    args = parser.parse_args()
    
    print(f"Looking up CIK for {args.ticker}...")
    
    # Try direct CIK lookup using company tickers endpoint
    ticker_url = "https://www.sec.gov/files/company_tickers.json"
    tickers_data_raw = fetch_url(ticker_url)
    
    cik = None
    company_name = "Unknown"
    
    if tickers_data_raw:
        try:
            tickers_data = json.loads(tickers_data_raw)
            for entry in tickers_data.values():
                if entry.get("ticker", "").upper() == args.ticker.upper():
                    cik = str(entry.get("cik_str", "")).zfill(10)
                    company_name = entry.get("title", "Unknown")
                    break
        except json.JSONDecodeError as e:
            print(f"Error parsing tickers data: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Could not fetch company tickers list", file=sys.stderr)
        sys.exit(1)
    
    if not cik:
        print(f"Could not find CIK for ticker {args.ticker}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found: {company_name} (CIK: {cik})")
    
    # Get company filings
    print(f"Fetching {args.filing_type} filings...")
    filings_data = get_company_filings(cik)
    
    if not filings_data:
        print("Could not retrieve filings data", file=sys.stderr)
        sys.exit(1)
    
    # Filter to requested filing type
    filings = filter_filings(filings_data, args.filing_type, args.count)
    
    if not filings:
        print(f"No {args.filing_type} filings found", file=sys.stderr)
        sys.exit(1)
    
    print(f"\nFound {len(filings)} {args.filing_type} filings:\n")
    
    # Output directory
    output_dir = Path(args.output) if args.output else Path(".")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for filing in filings:
        url = get_filing_url(cik.lstrip("0"), filing["accession_number"], filing["primary_document"])
        print(f"  {filing['filing_date']}: {filing['accession_number']}")
        print(f"    URL: {url}")
        
        if args.extract_risks and args.filing_type == "10-K":
            print("    Extracting risk factors...")
            content = fetch_filing_content(url)
            if content:
                risks = extract_risk_factors(content)
                if risks:
                    risk_file = output_dir / f"{args.ticker}_{filing['filing_date']}_risks.txt"
                    risk_file.write_text(risks)
                    print(f"    Saved: {risk_file} ({len(risks)} chars)")
                else:
                    print("    Could not extract risk factors section")
        print()
    
    print("Done.")


if __name__ == "__main__":
    main()
