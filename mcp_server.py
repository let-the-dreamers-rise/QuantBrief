from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from analysis_engine import DEFAULT_AUM, analyze_portfolio as run_analysis, analyze_single_stock, get_engine_status, warm_engine


mcp = FastMCP("QuantBrief")
warm_engine(background=True)


def _parse_portfolio(tickers_csv: str, weights_csv: str) -> list[dict[str, float]] | None:
    tickers = [ticker.strip().upper() for ticker in tickers_csv.split(",") if ticker.strip()]
    if not tickers:
        return None

    if weights_csv.strip():
        raw_weights = [float(weight.strip()) for weight in weights_csv.split(",") if weight.strip()]
        if len(raw_weights) != len(tickers):
            raise ValueError("Weights count must match ticker count.")
        if any(weight > 1 for weight in raw_weights):
            raw_weights = [weight / 100 for weight in raw_weights]
    else:
        raw_weights = [1 / len(tickers)] * len(tickers)

    return [{"ticker": ticker, "weight": weight} for ticker, weight in zip(tickers, raw_weights)]


def _format_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


@mcp.tool()
def analyze_portfolio(tickers_csv: str = "", weights_csv: str = "", period: str = "3y", aum: float = DEFAULT_AUM) -> str:
    """Analyze a portfolio and return a compact human-readable summary."""

    portfolio = _parse_portfolio(tickers_csv, weights_csv)
    payload = run_analysis(portfolio, period=period, aum=aum)

    lines = [
        "QUANTBRIEF PORTFOLIO ANALYSIS",
        "",
        f"Decision: {payload['recommendation']['action']} ({payload['recommendation']['confidence'] * 100:.0f}% confidence)",
        f"Portfolio CAGR: {_format_pct(payload['portfolio']['cagr'])}",
        f"Portfolio Sharpe: {payload['portfolio']['sharpe']:.2f}",
        f"Volatility: {_format_pct(payload['portfolio']['volatility'])}",
        f"Max drawdown: {_format_pct(payload['portfolio']['maxDD'])}",
        "",
        "Holdings:",
    ]

    for stock in payload["stocks"]:
        lines.append(
            f"- {stock['ticker']}: {stock['mlSignal'].upper()} at {stock['mlProb'] * 100:.0f}% | "
            f"weight {stock['weight'] * 100:.0f}% | CAGR {_format_pct(stock['cagr'])}"
        )

    top_event = payload["market"]["topEvent"]
    if top_event:
        lines.extend(
            [
                "",
                f"Top event: {top_event['title']}",
                f"Impact: {_format_pct(top_event['impact'])} | Exposure: {_format_pct(top_event['exposure'])}",
            ]
        )

    lines.extend(
        [
            "",
            "Why:",
            *[f"- {driver}" for driver in payload["recommendation"]["drivers"]],
            "",
            "This is AI-generated analysis for education, not financial advice.",
        ]
    )

    return "\n".join(lines)


@mcp.tool()
def get_market_events(tickers_csv: str = "", weights_csv: str = "", period: str = "3y") -> str:
    """Return ranked portfolio-specific market events."""

    portfolio = _parse_portfolio(tickers_csv, weights_csv)
    payload = run_analysis(portfolio, period=period)
    lines = ["MARKET EVENTS RANKED BY PORTFOLIO IMPACT", ""]
    for index, event in enumerate(payload["market"]["events"], start=1):
        lines.extend(
            [
                f"{index}. {event['title']}",
                f"   Type: {event['type']} | Impact: {_format_pct(event['impact'])} | Exposure: {_format_pct(event['exposure'])}",
                f"   Affected: {', '.join(event['affectedTickers'])}",
                f"   Summary: {event['summary']}",
                "",
            ]
        )
    lines.append("This is AI-generated analysis for education, not financial advice.")
    return "\n".join(lines)


@mcp.tool()
def lookup_stock(ticker: str, period: str = "3y") -> str:
    """Look up a single stock's risk and signal profile."""

    stock = analyze_single_stock(ticker, period=period)
    lines = [
        f"{stock['ticker']} - {stock['name']}",
        f"Sector: {stock['sector']}",
        f"CAGR: {_format_pct(stock['cagr'])}",
        f"Sharpe: {stock['sharpe']:.2f}",
        f"Volatility: {_format_pct(stock['volatility'])}",
        f"Max drawdown: {_format_pct(stock['maxDD'])}",
        f"Signal: {stock['mlSignal'].upper()} ({stock['mlProb'] * 100:.0f}% confidence)",
        f"Thesis: {stock['thesis']}",
        "",
        "This is AI-generated analysis for education, not financial advice.",
    ]
    return "\n".join(lines)


@mcp.tool()
def get_recommendation(tickers_csv: str = "", weights_csv: str = "", period: str = "3y", aum: float = DEFAULT_AUM) -> str:
    """Get the action, confidence, and next steps for a portfolio."""

    portfolio = _parse_portfolio(tickers_csv, weights_csv)
    payload = run_analysis(portfolio, period=period, aum=aum)
    recommendation = payload["recommendation"]
    lines = [
        "QUANTBRIEF RECOMMENDATION",
        "",
        f"Action: {recommendation['action']}",
        f"Confidence: {recommendation['confidence'] * 100:.0f}%",
        recommendation["summary"],
        "",
        "Add:",
        *[f"- {item['ticker']}: {item['reason']}" for item in recommendation["additions"]],
        "",
        "Hold:",
        *[f"- {item['ticker']}: {item['reason']}" for item in recommendation["holds"]],
        "",
        "Trim:",
        *[f"- {item['ticker']}: {item['reason']}" for item in recommendation["trims"]],
        "",
        "This is AI-generated analysis for education, not financial advice.",
    ]
    return "\n".join(lines)


@mcp.tool()
def get_risk_scenarios(tickers_csv: str = "", weights_csv: str = "", period: str = "3y") -> str:
    """Return base, stress, drawdown, and bull scenarios for the portfolio."""

    portfolio = _parse_portfolio(tickers_csv, weights_csv)
    payload = run_analysis(portfolio, period=period)
    lines = ["RISK SCENARIOS", ""]
    for scenario in payload["recommendation"]["scenarios"]:
        lines.extend(
            [
                f"- {scenario['label']}: {_format_pct(scenario['value'])}",
                f"  {scenario['detail']}",
            ]
        )
    lines.extend(["", "This is AI-generated analysis for education, not financial advice."])
    return "\n".join(lines)


@mcp.tool()
def engine_status() -> str:
    """Report dependency and warmup status for the analysis engine."""

    status = get_engine_status()
    warmup = status["warmup"]
    return (
        "QuantBrief engine status\n"
        f"- Warmup started: {warmup['started']}\n"
        f"- Warmup completed: {warmup['completed']}\n"
        f"- QuantStats installed: {status['quantstats']}\n"
        f"- yfinance installed: {status['yfinance']}\n"
        f"- scikit-learn installed: {status['sklearn']}\n"
        f"- Timestamp: {status['timestamp']}"
    )


if __name__ == "__main__":
    print("QuantBrief MCP server starting")
    mcp.run()
