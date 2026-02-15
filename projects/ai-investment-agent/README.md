# AI Investment Analysis Agent

Research and development for an AI agent that analyzes company reports, SEC filings, and market data to find investment opportunities and gaps.

## Research Summary (Feb 15, 2026)

### Existing Landscape

**Top Projects Found:**
| Project | Stars | Description |
|---------|-------|-------------|
| [ProsusAI/finBERT](https://github.com/ProsusAI/finBERT) | 2000 | Financial sentiment analysis with BERT |
| [virattt/ai-financial-agent](https://github.com/virattt/ai-financial-agent) | 1693 | Investment research agent with Financial Datasets API |
| [virattt/financial-agent-ui](https://github.com/virattt/financial-agent-ui) | 779 | Generative UI for financial agents |
| [virattt/financial-agent](https://github.com/virattt/financial-agent) | 242 | LangChain-based financial agent |
| [TickrAgent](https://github.com/The-Swarm-Corporation/TickrAgent) | 54 | Enterprise swarm of financial agents for stock analysis |

**Approaches in the Wild:**
1. **Sentiment Analysis** - FinBERT for analyzing earnings calls, news, filings
2. **RAG on SEC Filings** - Build retrieval-augmented generation over 10-K, 10-Q
3. **Real-time Data Agents** - APIs: Financial Datasets, yfinance, Polygon
4. **Multi-Agent Swarms** - Specialized agents analyzing different aspects simultaneously

### Gap Analysis: What's NOT Being Done Well

1. **Cross-Company Comparison Agent**
   - Existing tools analyze one company at a time
   - Opportunity: Compare filings across competitors to find hidden discrepancies
   - Example: "Company A mentions supply chain risk but competitor B doesn't — why?"

2. **Anomaly Detection in SEC Filings**
   - Most tools summarize; few detect inconsistencies or red flags
   - Opportunity: Flag sudden language changes, missing disclosures, tone shifts

3. **Earnings Call Tone vs Actual Performance**
   - Sentiment tools exist, but few correlate tone with subsequent stock performance
   - Opportunity: Predictive model using call sentiment → 90-day returns

4. **Small-Cap Undervalued Stock Finder**
   - Most agents focus on large caps (AAPL, MSFT, NVDA, TSLA)
   - Opportunity: Scan lesser-known companies (<$2B market cap) for value gaps

5. **Insider Trading Pattern Detection**
   - Form 4 filings are public but underanalyzed
   - Opportunity: Detect unusual insider buying/selling patterns before price moves

6. **Supply Chain Disruption Prediction**
   - Supplier mentions scattered across filings
   - Opportunity: Cross-reference supplier names across filings to predict disruption contagion

7. **Management Turnover Impact**
   - Track executive departures/arrivals and correlate with performance
   - Opportunity: Early warning system for leadership instability

### Recommended Approach

**Phase 1: SEC Filings Scanner (MVP)**
- Focus: 10-K and 10-Q filings
- Data source: SEC EDGAR API (free)
- Initial capability: Extract risk factors, compare YoY changes, flag anomalies
- Output: Weekly report of "interesting findings" across scanned companies

**Phase 2: Multi-Signal Correlation**
- Add earnings call transcripts (sentiment analysis)
- Add insider trading data (Form 4)
- Add price/volume data (yfinance, free)
- Correlate signals to generate investment hypotheses

**Phase 3: Backtesting & Validation**
- Historical analysis: Would past signals have predicted returns?
- Build confidence scores for each signal type
- Refine model based on results

### Data Sources (Free/Low-Cost)

| Source | Data Type | Cost |
|--------|-----------|------|
| [SEC EDGAR](https://www.sec.gov/edgar) | 10-K, 10-Q, 8-K, Form 4 | Free |
| [yfinance](https://github.com/ranaroussi/yfinance) | Price, volume, fundamentals | Free |
| [Financial Datasets API](https://financialdatasets.ai) | Comprehensive (5 free tickers) | Freemium |
| [Alpha Vantage](https://www.alphavantage.co) | Price, fundamentals | Free tier |
| [Polygon.io](https://polygon.io) | Real-time market data | Free tier |

### Technical Stack (Proposed)

```
- Python 3.11+
- LangChain or LlamaIndex for RAG
- FinBERT for sentiment
- SEC EDGAR API for filings
- yfinance for price data
- PostgreSQL or SQLite for storage
- Streamlit or Gradio for UI (optional)
```

## Next Steps

1. [ ] Set up SEC EDGAR API access and test filing retrieval
2. [ ] Build simple 10-K parser to extract risk factors section
3. [ ] Create comparison logic for YoY risk factor changes
4. [ ] Test FinBERT sentiment on sample earnings call transcript
5. [ ] Design database schema for storing analysis results
6. [ ] Build first "interesting findings" report generator

## Revenue Potential

| Offering | Price Point | Target |
|----------|-------------|--------|
| Weekly Report Subscription | $99/month | Retail investors |
| API Access to Signals | $299/month | Quant traders, small funds |
| Custom Analysis | $2,000/engagement | Family offices, advisors |
| White-label Solution | $10,000+ | Fintech platforms |

## Contact

- Email: shellyfinn9@gmail.com
- GitHub: shelly-finn

---

**Status:** Research phase
**Next Action:** Build SEC EDGAR filing retriever prototype
**Created:** Feb 15, 2026
