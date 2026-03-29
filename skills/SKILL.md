---
name: quantbrief_portfolio_analysis
description: >
  Analyze an Indian equity portfolio using the QuantBrief AI engine.
  Use this skill when the user asks about their portfolio, stock performance,
  market event impact, or wants investment recommendations.
  Supports queries like "How does the RBI rate cut affect me?", "Show my portfolio",
  "What should I buy?", and "Analyze HDFCBANK".
user-invocable: true
---

# QuantBrief Portfolio Analysis Skill

## Overview
This skill connects to the QuantBrief backend API to provide real-time portfolio analysis,
market event impact assessment, and AI-driven investment recommendations for Indian retail investors.

## Prerequisites
The QuantBrief backend should be running for the web UI. Start it with:
```bash
cd "C:\Users\ASHWIN GOYAL\Downloads\QuantBrief-v3"
python backend.py
```

The MCP server can also answer directly through `mcp_server.py`, because it now shares the same
analysis engine as the backend.

## Available Commands

### 1. Full Portfolio Analysis
When the user asks about their portfolio or wants a general overview:
```bash
curl -s http://localhost:8000/api/analyze -X POST -H "Content-Type: application/json" -d '{"stocks":[{"ticker":"RELIANCE","weight":0.20},{"ticker":"HDFCBANK","weight":0.18},{"ticker":"TCS","weight":0.15},{"ticker":"INFY","weight":0.12},{"ticker":"ICICIBANK","weight":0.10},{"ticker":"BAJFINANCE","weight":0.08},{"ticker":"MARUTI","weight":0.06},{"ticker":"DLF","weight":0.04},{"ticker":"SUNPHARMA","weight":0.04},{"ticker":"LT","weight":0.03}],"period":"3y"}'
```

### 2. Health Check
To verify the backend is running:
```bash
curl -s http://localhost:8000/api/health
```

### 3. List Available Stocks
When the user asks what stocks they can add:
```bash
curl -s http://localhost:8000/api/stocks
```

## Response Formatting
When presenting results to the user:

1. **Portfolio Overview**: Show stocks sorted by weight with their AI signals (BUY/HOLD/SELL)
2. **Key Metrics**: Present CAGR, Sharpe Ratio, Volatility, Max Drawdown in a clean format
3. **Market Events**: Explain how current events affect the user's specific portfolio
4. **Recommendation**: Give clear ACCUMULATE / HOLD / REDUCE / EXIT advice
5. **Risk Warning**: Always include: "This is AI-generated analysis, not financial advice. Consult a SEBI-registered advisor."

## Example Interactions

**User**: "How does my portfolio look?"
**Action**: Run the full analysis endpoint, then summarize:
- Portfolio CAGR and Sharpe Ratio
- Top performers and underperformers
- Stocks with BUY vs HOLD signals
- Overall recommendation

**User**: "Should I buy more HDFCBANK?"
**Action**: Run analysis, focus on HDFCBANK metrics:
- Current AI signal and confidence
- CAGR and volatility relative to portfolio
- Sector correlation with other holdings
- Impact of current rate-sensitive events

**User**: "What market events should I worry about?"
**Action**: Pull from the event data and explain impact in plain language with portfolio-specific exposure percentages.

## Important Notes
- All monetary values should be shown in Rs (Indian Rupees)
- Use IST timezone for timestamps
- If backend is offline, explain what data would be available and suggest starting it
- Keep language simple and avoid excessive jargon
- This is for EDUCATIONAL purposes - always include proper risk disclaimers
