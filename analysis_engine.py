from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from functools import lru_cache
import hashlib
import math
import threading
from typing import Any

import numpy as np
import pandas as pd

try:
    import quantstats as qs

    QS_AVAILABLE = True
except ImportError:
    qs = None
    QS_AVAILABLE = False

try:
    import yfinance as yf

    YF_AVAILABLE = True
except ImportError:
    yf = None
    YF_AVAILABLE = False

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split

    ML_AVAILABLE = True
except ImportError:
    RandomForestClassifier = None
    train_test_split = None
    ML_AVAILABLE = False


IST = timezone(timedelta(hours=5, minutes=30))
DEFAULT_AUM = 2_500_000
PERIOD_DAYS = {"1y": 252, "3y": 756, "5y": 1260}
PRICE_LOOKBACK = 40

STOCK_META: dict[str, dict[str, str]] = {
    "RELIANCE": {"name": "Reliance Industries", "sector": "Conglomerate", "yahoo": "RELIANCE.NS"},
    "HDFCBANK": {"name": "HDFC Bank", "sector": "Banking", "yahoo": "HDFCBANK.NS"},
    "TCS": {"name": "Tata Consultancy Services", "sector": "IT", "yahoo": "TCS.NS"},
    "INFY": {"name": "Infosys", "sector": "IT", "yahoo": "INFY.NS"},
    "ICICIBANK": {"name": "ICICI Bank", "sector": "Banking", "yahoo": "ICICIBANK.NS"},
    "BAJFINANCE": {"name": "Bajaj Finance", "sector": "NBFC", "yahoo": "BAJFINANCE.NS"},
    "MARUTI": {"name": "Maruti Suzuki", "sector": "Auto", "yahoo": "MARUTI.NS"},
    "DLF": {"name": "DLF", "sector": "Real Estate", "yahoo": "DLF.NS"},
    "SUNPHARMA": {"name": "Sun Pharma", "sector": "Pharma", "yahoo": "SUNPHARMA.NS"},
    "LT": {"name": "Larsen & Toubro", "sector": "Infrastructure", "yahoo": "LT.NS"},
    "SBIN": {"name": "State Bank of India", "sector": "Banking", "yahoo": "SBIN.NS"},
    "WIPRO": {"name": "Wipro", "sector": "IT", "yahoo": "WIPRO.NS"},
    "TATAMOTORS": {"name": "Tata Motors", "sector": "Auto", "yahoo": "TATAMOTORS.NS"},
    "HCLTECH": {"name": "HCL Technologies", "sector": "IT", "yahoo": "HCLTECH.NS"},
    "ADANIENT": {"name": "Adani Enterprises", "sector": "Conglomerate", "yahoo": "ADANIENT.NS"},
    "KOTAKBANK": {"name": "Kotak Mahindra Bank", "sector": "Banking", "yahoo": "KOTAKBANK.NS"},
    "BHARTIARTL": {"name": "Bharti Airtel", "sector": "Telecom", "yahoo": "BHARTIARTL.NS"},
    "TITAN": {"name": "Titan Company", "sector": "Consumer", "yahoo": "TITAN.NS"},
    "ASIANPAINT": {"name": "Asian Paints", "sector": "Consumer", "yahoo": "ASIANPAINT.NS"},
    "ULTRACEMCO": {"name": "UltraTech Cement", "sector": "Cement", "yahoo": "ULTRACEMCO.NS"},
    "AAPL": {"name": "Apple", "sector": "Technology", "yahoo": "AAPL"},
    "MSFT": {"name": "Microsoft", "sector": "Technology", "yahoo": "MSFT"},
    "TSLA": {"name": "Tesla", "sector": "Auto", "yahoo": "TSLA"},
    "NVDA": {"name": "NVIDIA", "sector": "Semiconductors", "yahoo": "NVDA"},
    "GOOGL": {"name": "Alphabet", "sector": "Technology", "yahoo": "GOOGL"},
}

DEFAULT_PORTFOLIO = [
    {"ticker": "RELIANCE", "weight": 0.20},
    {"ticker": "HDFCBANK", "weight": 0.18},
    {"ticker": "TCS", "weight": 0.15},
    {"ticker": "INFY", "weight": 0.12},
    {"ticker": "ICICIBANK", "weight": 0.10},
    {"ticker": "BAJFINANCE", "weight": 0.08},
    {"ticker": "MARUTI", "weight": 0.06},
    {"ticker": "DLF", "weight": 0.04},
    {"ticker": "SUNPHARMA", "weight": 0.04},
    {"ticker": "LT", "weight": 0.03},
]

SECTOR_PROFILES = {
    "Banking": {"drift": 0.00040, "sector_vol": 0.0064, "beta": 1.08},
    "NBFC": {"drift": 0.00046, "sector_vol": 0.0072, "beta": 1.18},
    "IT": {"drift": 0.00034, "sector_vol": 0.0061, "beta": 0.95},
    "Auto": {"drift": 0.00031, "sector_vol": 0.0068, "beta": 1.04},
    "Real Estate": {"drift": 0.00044, "sector_vol": 0.0081, "beta": 1.16},
    "Pharma": {"drift": 0.00029, "sector_vol": 0.0054, "beta": 0.88},
    "Infrastructure": {"drift": 0.00033, "sector_vol": 0.0062, "beta": 1.03},
    "Conglomerate": {"drift": 0.00032, "sector_vol": 0.0058, "beta": 1.00},
    "Telecom": {"drift": 0.00028, "sector_vol": 0.0053, "beta": 0.84},
    "Consumer": {"drift": 0.00026, "sector_vol": 0.0048, "beta": 0.82},
    "Cement": {"drift": 0.00030, "sector_vol": 0.0057, "beta": 0.97},
    "Technology": {"drift": 0.00037, "sector_vol": 0.0060, "beta": 1.01},
    "Semiconductors": {"drift": 0.00048, "sector_vol": 0.0085, "beta": 1.22},
}

EVENT_LIBRARY = [
    {
        "title": "RBI easing bias continues to support rate-sensitive pockets",
        "type": "macro",
        "summary": "Lower funding costs usually help lenders, NBFCs, autos, real estate, and capex names first.",
        "effects": {
            "Banking": 0.022,
            "NBFC": 0.034,
            "Auto": 0.017,
            "Real Estate": 0.028,
            "Infrastructure": 0.013,
            "Conglomerate": 0.008,
        },
    },
    {
        "title": "Large-cap IT order books remain healthy despite mixed global demand",
        "type": "sector",
        "summary": "Deal wins are cushioning the IT sleeve and keeping operating leverage intact.",
        "effects": {"IT": 0.015, "Technology": 0.013, "Semiconductors": 0.018},
    },
    {
        "title": "Domestic flows are absorbing foreign selling pressure",
        "type": "flow",
        "summary": "SIP and insurance flows continue to provide support on every dip.",
        "effects": {
            "Banking": 0.006,
            "Consumer": 0.005,
            "Pharma": 0.004,
            "Conglomerate": 0.005,
            "Infrastructure": 0.004,
            "IT": 0.004,
        },
    },
    {
        "title": "Crude and global risk sentiment remain the main downside watch",
        "type": "risk",
        "summary": "An external macro shock would pressure autos, cyclicals, and margin-sensitive holdings first.",
        "effects": {"Auto": -0.018, "Conglomerate": -0.010, "Consumer": -0.007, "Infrastructure": -0.006},
    },
]

_WARMUP_LOCK = threading.Lock()
_WARMUP_STATE = {
    "started": False,
    "completed": False,
    "started_at": None,
    "completed_at": None,
    "error": None,
}


def _seed_for(*parts: str) -> int:
    joined = "::".join(parts)
    return int(hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16], 16)


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def _now_ist() -> str:
    return datetime.now(IST).isoformat(timespec="seconds")


def list_supported_stocks() -> list[dict[str, str]]:
    return [
        {"ticker": ticker, "name": meta["name"], "sector": meta["sector"]}
        for ticker, meta in sorted(STOCK_META.items())
    ]


def normalize_portfolio(stocks: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    raw_items = stocks or DEFAULT_PORTFOLIO
    aggregate: dict[str, float] = defaultdict(float)

    for item in raw_items:
        ticker = str(item.get("ticker", "")).upper().strip()
        if not ticker:
            continue
        weight = float(item.get("weight", 0))
        if weight < 0:
            raise ValueError(f"Weight cannot be negative for {ticker}.")
        aggregate[ticker] += weight

    if not aggregate:
        raise ValueError("Portfolio must contain at least one valid ticker.")

    weights = list(aggregate.values())
    if any(weight > 1 for weight in weights):
        aggregate = {ticker: weight / 100 for ticker, weight in aggregate.items()}

    total_weight = sum(aggregate.values())
    if total_weight <= 0:
        raise ValueError("Portfolio weights must add up to a positive value.")

    normalized = []
    for ticker, weight in aggregate.items():
        meta = STOCK_META.get(ticker, {"name": ticker, "sector": "Unknown", "yahoo": ticker})
        normalized.append(
            {
                "ticker": ticker,
                "name": meta["name"],
                "sector": meta["sector"],
                "yahoo": meta["yahoo"],
                "weight": weight / total_weight,
            }
        )

    return sorted(normalized, key=lambda item: item["weight"], reverse=True)


@lru_cache(maxsize=8)
def _market_factor(period: str) -> pd.Series:
    n = PERIOD_DAYS.get(period, PERIOD_DAYS["3y"])
    rng = np.random.default_rng(_seed_for("market", period))
    base = rng.normal(0.00036, 0.0081, n)
    cycle = np.sin(np.linspace(0, math.pi * 5, n)) * 0.0011
    dates = pd.bdate_range(end=pd.Timestamp.now().normalize(), periods=n)
    return pd.Series(base + cycle, index=dates, name="market")


@lru_cache(maxsize=32)
def _sector_factor(sector: str, period: str) -> pd.Series:
    n = PERIOD_DAYS.get(period, PERIOD_DAYS["3y"])
    profile = SECTOR_PROFILES.get(sector, {"drift": 0.00030, "sector_vol": 0.0058})
    rng = np.random.default_rng(_seed_for("sector", sector, period))
    pulse = np.sin(np.linspace(0, math.pi * 3.5, n) + (len(sector) * 0.2)) * 0.0009
    noise = rng.normal(profile["drift"], profile["sector_vol"], n)
    dates = pd.bdate_range(end=pd.Timestamp.now().normalize(), periods=n)
    return pd.Series(noise + pulse, index=dates, name=sector)


def _simulated_returns(ticker: str, sector: str, period: str) -> pd.Series:
    market = _market_factor(period)
    sector_series = _sector_factor(sector, period)
    profile = SECTOR_PROFILES.get(sector, {"drift": 0.00030, "sector_vol": 0.0058, "beta": 1.0})
    rng = np.random.default_rng(_seed_for("ticker", ticker, period))
    idiosyncratic = rng.normal(0, 0.0095, len(market))
    drift_adjustment = rng.normal(profile["drift"], 0.00005)
    combined = market.values * profile["beta"] * 0.58 + sector_series.values * 0.32 + idiosyncratic * 0.24 + drift_adjustment
    combined = np.clip(combined, -0.12, 0.12)
    return pd.Series(combined, index=market.index, name=ticker)


def _coerce_series(series: Any) -> pd.Series | None:
    if series is None:
        return None
    if isinstance(series, pd.DataFrame):
        if "Close" in series.columns:
            series = series["Close"]
        elif len(series.columns) > 0:
            series = series.iloc[:, 0]
    if not isinstance(series, pd.Series):
        return None
    series = series.dropna().astype(float)
    if isinstance(series.index, pd.DatetimeIndex):
        index = pd.DatetimeIndex(series.index)
        if index.tz is not None:
            index = index.tz_localize(None)
        series = series.copy()
        series.index = index.normalize()
        series = series[~series.index.duplicated(keep="last")].sort_index()
    if len(series) < 60:
        return None
    return series


@lru_cache(maxsize=128)
def get_return_series(ticker: str, period: str = "3y") -> tuple[pd.Series, str]:
    period = period if period in PERIOD_DAYS else "3y"
    meta = STOCK_META.get(ticker, {"name": ticker, "sector": "Unknown", "yahoo": ticker})
    yahoo_ticker = meta["yahoo"]

    if QS_AVAILABLE:
        try:
            series = _coerce_series(qs.utils.download_returns(yahoo_ticker, period=period))
            if series is not None:
                return series, "live"
        except Exception:
            pass

    if YF_AVAILABLE:
        try:
            history = yf.download(yahoo_ticker, period=period, auto_adjust=True, progress=False, threads=False)
            prices = _coerce_series(history.get("Close") if isinstance(history, pd.DataFrame) else history)
            if prices is not None:
                returns = prices.pct_change().dropna()
                if len(returns) >= 60:
                    return returns.astype(float), "live"
        except Exception:
            pass

    return _simulated_returns(ticker, meta["sector"], period), "simulated"


def _compute_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    delta = prices.diff()
    gains = delta.clip(lower=0).rolling(period).mean()
    losses = (-delta.clip(upper=0)).rolling(period).mean().replace(0, np.nan)
    rs = gains / losses
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def _annualized_return(returns: pd.Series) -> float:
    if returns.empty:
        return 0.0
    growth = float((1 + returns).prod())
    years = len(returns) / 252
    if years <= 0 or growth <= 0:
        return 0.0
    return growth ** (1 / years) - 1


def _annualized_volatility(returns: pd.Series) -> float:
    if len(returns) < 2:
        return 0.0
    return float(returns.std(ddof=0) * math.sqrt(252))


def _max_drawdown(returns: pd.Series) -> float:
    if returns.empty:
        return 0.0
    prices = (1 + returns).cumprod()
    peak = prices.cummax().replace(0, np.nan)
    drawdown = prices / peak - 1
    return float(drawdown.min())


def _sharpe_ratio(returns: pd.Series) -> float:
    vol = returns.std(ddof=0)
    if len(returns) < 2 or vol == 0:
        return 0.0
    return float((returns.mean() / vol) * math.sqrt(252))


def _signal_from_returns(returns: pd.Series) -> tuple[str, float]:
    prices = 100 * (1 + returns).cumprod()
    features = pd.DataFrame(index=returns.index)
    features["rsi"] = _compute_rsi(prices)
    sma20 = prices.rolling(20).mean()
    sma50 = prices.rolling(50).mean()
    features["sma_gap"] = (prices / sma20) - 1
    features["trend_gap"] = (sma20 / sma50) - 1
    features["momentum_20"] = prices.pct_change(20)
    features["vol_20"] = returns.rolling(20).std()
    features["drawdown"] = prices / prices.cummax() - 1
    features["target"] = (returns.shift(-1) > 0).astype(int)
    features = features.dropna()

    if len(features) < 90:
        latest = features.iloc[-1] if not features.empty else pd.Series({"rsi": 50, "sma_gap": 0, "trend_gap": 0, "momentum_20": 0, "vol_20": 0.02, "drawdown": 0})
        score = (
            latest["sma_gap"] * 4.0
            + latest["trend_gap"] * 3.2
            + latest["momentum_20"] * 2.4
            - latest["vol_20"] * 3.0
            - abs(latest["drawdown"]) * 1.3
            + ((latest["rsi"] - 50) / 50) * 0.7
        )
        probability = 1 / (1 + math.exp(-score))
    elif ML_AVAILABLE:
        columns = ["rsi", "sma_gap", "trend_gap", "momentum_20", "vol_20", "drawdown"]
        model_data = features[columns + ["target"]].dropna()
        x = model_data[columns]
        y = model_data["target"]
        x_train, _, y_train, _ = train_test_split(x, y, test_size=0.2, shuffle=False)
        model = RandomForestClassifier(n_estimators=160, max_depth=6, min_samples_leaf=3, random_state=42)
        model.fit(x_train, y_train)
        probability = float(model.predict_proba(x.iloc[[-1]])[0][1])
    else:
        latest = features.iloc[-1]
        score = (
            latest["sma_gap"] * 4.0
            + latest["trend_gap"] * 3.2
            + latest["momentum_20"] * 2.4
            - latest["vol_20"] * 3.0
            - abs(latest["drawdown"]) * 1.3
            + ((latest["rsi"] - 50) / 50) * 0.7
        )
        probability = 1 / (1 + math.exp(-score))

    probability = _clamp(probability, 0.12, 0.88)
    if probability >= 0.62:
        signal = "buy"
    elif probability <= 0.42:
        signal = "sell"
    else:
        signal = "hold"
    return signal, probability


def _sparkline(prices: pd.Series) -> list[float]:
    tail = prices.tail(PRICE_LOOKBACK)
    if tail.empty:
        return []
    normalized = (tail / tail.iloc[0]) * 100
    return [round(float(value), 2) for value in normalized]


def analyze_stock(ticker: str, weight: float, period: str = "3y") -> dict[str, Any]:
    meta = STOCK_META.get(ticker, {"name": ticker, "sector": "Unknown", "yahoo": ticker})
    returns, source = get_return_series(ticker, period)
    prices = 100 * (1 + returns).cumprod()
    cagr = _annualized_return(returns)
    sharpe = _sharpe_ratio(returns)
    volatility = _annualized_volatility(returns)
    max_drawdown = _max_drawdown(returns)
    signal, probability = _signal_from_returns(returns)
    one_month = float(prices.iloc[-1] / prices.iloc[-22] - 1) if len(prices) >= 22 else float(prices.iloc[-1] / prices.iloc[0] - 1)
    conviction = _clamp((cagr * 2.4) + (sharpe * 0.12) + ((probability - 0.5) * 1.4) - abs(max_drawdown) * 0.5, 0.0, 1.0)

    stock = {
        "ticker": ticker,
        "name": meta["name"],
        "sector": meta["sector"],
        "weight": round(weight, 6),
        "cagr": round(cagr, 4),
        "sharpe": round(sharpe, 2),
        "volatility": round(volatility, 4),
        "maxDD": round(max_drawdown, 4),
        "mlSignal": signal,
        "mlProb": round(probability, 4),
        "oneMonthChange": round(one_month, 4),
        "sparkline": _sparkline(prices),
        "thesis": _build_stock_thesis(meta["sector"], signal, probability, cagr, max_drawdown),
        "conviction": round(conviction, 4),
        "dataSource": source,
    }
    stock["_returns"] = returns
    return stock


def _build_stock_thesis(sector: str, signal: str, probability: float, cagr: float, max_drawdown: float) -> str:
    signal_text = {"buy": "constructive", "hold": "balanced", "sell": "fragile"}[signal]
    drawdown_text = "contained" if abs(max_drawdown) < 0.18 else "elevated"
    return (
        f"{sector} exposure looks {signal_text}; model confidence is {probability * 100:.0f}% "
        f"with an annualized return profile near {cagr * 100:.1f}% and {drawdown_text} downside."
    )


def _sector_exposure(stocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, float] = defaultdict(float)
    signal_scores: dict[str, list[float]] = defaultdict(list)
    for stock in stocks:
        grouped[stock["sector"]] += stock["weight"]
        signal_scores[stock["sector"]].append(stock["mlProb"])

    rows = []
    for sector, weight in grouped.items():
        confidence = float(np.mean(signal_scores[sector])) if signal_scores[sector] else 0.5
        tone = "positive" if confidence >= 0.58 else "balanced" if confidence >= 0.46 else "negative"
        rows.append(
            {
                "sector": sector,
                "weight": round(weight, 4),
                "confidence": round(confidence, 4),
                "tone": tone,
            }
        )
    return sorted(rows, key=lambda row: row["weight"], reverse=True)


def _correlation_payload(returns_frame: pd.DataFrame) -> dict[str, Any]:
    correlation = returns_frame.tail(180).corr().replace([np.inf, -np.inf], 0).fillna(0)
    return {
        "tickers": correlation.columns.tolist(),
        "matrix": correlation.round(2).values.tolist(),
        "average": round(float(correlation.where(~np.eye(len(correlation), dtype=bool)).stack().abs().mean()), 2) if len(correlation) > 1 else 0.0,
    }


def _fii_dii_flows() -> list[dict[str, Any]]:
    series = [
        ("Mon", -1320, 1550),
        ("Tue", -940, 1180),
        ("Wed", -2260, 1910),
        ("Thu", 480, 760),
        ("Fri", -1680, 2140),
        ("Sat", -360, 620),
        ("Today", -1180, 1480),
    ]
    rows = []
    for day, fii, dii in series:
        rows.append({"day": day, "fii": fii, "dii": dii, "net": fii + dii})
    return rows


def _build_market_events(stocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events = []
    by_ticker = {stock["ticker"]: stock for stock in stocks}
    for template in EVENT_LIBRARY:
        affected = []
        weighted_impact = 0.0
        exposure = 0.0
        for stock in stocks:
            effect = template["effects"].get(stock["sector"], 0.0)
            if abs(effect) < 1e-9:
                continue
            weighted_impact += stock["weight"] * effect
            exposure += stock["weight"]
            affected.append(
                {
                    "ticker": stock["ticker"],
                    "weight": round(stock["weight"], 4),
                    "impact": round(effect, 4),
                    "confidence": round(by_ticker[stock["ticker"]]["mlProb"], 4),
                }
            )

        if not affected:
            continue

        severity = "high" if abs(weighted_impact) >= 0.018 else "medium" if abs(weighted_impact) >= 0.009 else "low"
        direction = "positive" if weighted_impact >= 0 else "negative"
        events.append(
            {
                "title": template["title"],
                "type": template["type"],
                "summary": template["summary"],
                "impact": round(weighted_impact, 4),
                "exposure": round(exposure, 4),
                "direction": direction,
                "severity": severity,
                "affectedTickers": [item["ticker"] for item in affected],
                "affected": sorted(affected, key=lambda item: abs(item["impact"] * item["weight"]), reverse=True),
            }
        )

    return sorted(events, key=lambda event: abs(event["impact"]), reverse=True)


def _portfolio_metrics(portfolio_returns: pd.Series, stocks: list[dict[str, Any]], aum: float, period: str) -> dict[str, Any]:
    cagr = _annualized_return(portfolio_returns)
    volatility = _annualized_volatility(portfolio_returns)
    sharpe = _sharpe_ratio(portfolio_returns)
    max_drawdown = _max_drawdown(portfolio_returns)
    cumulative = (1 + portfolio_returns).cumprod()
    diversification = 1 - min(0.92, abs(portfolio_returns.corr(_market_factor(period).tail(len(portfolio_returns)))) if len(portfolio_returns) > 50 else 0.25)
    concentration = sum(stock["weight"] ** 2 for stock in stocks)
    diversification_score = _clamp((diversification * 65) + (1 - concentration) * 45 + min(len(stocks), 12) * 2, 20, 92)
    win_rate = float((portfolio_returns > 0).mean()) if len(portfolio_returns) else 0.0

    return {
        "aum": float(aum),
        "period": period,
        "cagr": round(cagr, 4),
        "sharpe": round(sharpe, 2),
        "volatility": round(volatility, 4),
        "maxDD": round(max_drawdown, 4),
        "winRate": round(win_rate, 4),
        "currentValue": round(float(aum * cumulative.iloc[-1]), 2) if len(cumulative) else float(aum),
        "netProfit": round(float(aum * (cumulative.iloc[-1] - 1)), 2) if len(cumulative) else 0.0,
        "diversificationScore": round(diversification_score, 1),
        "stockCount": len(stocks),
        "healthLabel": _portfolio_health_label(cagr, sharpe, max_drawdown),
    }


def _portfolio_health_label(cagr: float, sharpe: float, max_drawdown: float) -> str:
    score = (cagr * 3.2) + (sharpe * 0.18) - abs(max_drawdown) * 0.8
    if score >= 0.85:
        return "Constructive"
    if score >= 0.55:
        return "Stable"
    if score >= 0.30:
        return "Mixed"
    return "Fragile"


def _build_recommendation(
    stocks: list[dict[str, Any]],
    portfolio: dict[str, Any],
    events: list[dict[str, Any]],
    correlation: dict[str, Any],
    flows: list[dict[str, Any]],
) -> dict[str, Any]:
    positive_weight = sum(stock["weight"] for stock in stocks if stock["mlSignal"] == "buy")
    negative_weight = sum(stock["weight"] for stock in stocks if stock["mlSignal"] == "sell")
    average_probability = float(np.mean([stock["mlProb"] for stock in stocks])) if stocks else 0.5
    top_event = events[0] if events else {"impact": 0.0, "exposure": 0.0, "title": "No material event detected"}
    flow_score = sum(item["net"] for item in flows) / 10_000

    score = (
        average_probability * 0.38
        + positive_weight * 0.18
        - negative_weight * 0.12
        + _clamp(top_event["impact"] * 8, -0.20, 0.20)
        + _clamp(portfolio["sharpe"] / 8, -0.10, 0.18)
        + _clamp(portfolio["diversificationScore"] / 200, 0.0, 0.18)
        + _clamp(flow_score, -0.08, 0.08)
        - _clamp(abs(portfolio["maxDD"]) * 0.35, 0.0, 0.16)
        - _clamp(correlation["average"] / 10, 0.0, 0.09)
    )
    score = _clamp(score, 0.0, 1.0)

    if score >= 0.67:
        action = "ACCUMULATE"
    elif score >= 0.48:
        action = "HOLD"
    else:
        action = "REDUCE"

    confidence = _clamp(0.57 + abs(score - 0.5) * 0.90 + abs(top_event["impact"]) * 4, 0.58, 0.92)

    ranked = sorted(stocks, key=lambda stock: stock["conviction"], reverse=True)
    additions = [
        {
            "ticker": stock["ticker"],
            "label": stock["name"],
            "reason": stock["thesis"],
            "signal": stock["mlSignal"],
            "confidence": stock["mlProb"],
        }
        for stock in ranked
        if stock["mlSignal"] == "buy"
    ][:3]
    trims = [
        {
            "ticker": stock["ticker"],
            "label": stock["name"],
            "reason": f"Volatility is running at {stock['volatility'] * 100:.1f}% with drawdown near {stock['maxDD'] * 100:.1f}%.",
            "signal": stock["mlSignal"],
            "confidence": stock["mlProb"],
        }
        for stock in sorted(stocks, key=lambda stock: (stock["mlSignal"] == "sell", -stock["volatility"], stock["conviction"]), reverse=True)
    ][:3]
    holds = [
        {
            "ticker": stock["ticker"],
            "label": stock["name"],
            "reason": stock["thesis"],
            "signal": stock["mlSignal"],
            "confidence": stock["mlProb"],
        }
        for stock in ranked
        if stock["ticker"] not in {item["ticker"] for item in additions}
    ][:3]

    signals = [
        {"label": "Model support", "value": f"{average_probability * 100:.0f}% avg", "tone": "positive" if average_probability >= 0.58 else "balanced"},
        {"label": "Portfolio Sharpe", "value": f"{portfolio['sharpe']:.2f}", "tone": "positive" if portfolio["sharpe"] >= 1.0 else "balanced"},
        {"label": "Top event exposure", "value": f"{top_event['exposure'] * 100:.0f}%", "tone": "positive" if top_event["impact"] >= 0 else "negative"},
        {"label": "Correlation drag", "value": f"{correlation['average']:.2f}", "tone": "balanced" if correlation["average"] <= 0.50 else "negative"},
    ]

    scenarios = _build_scenarios(portfolio, top_event)

    return {
        "action": action,
        "confidence": round(confidence, 4),
        "summary": (
            f"{action} with {confidence * 100:.0f}% confidence. "
            f"{top_event['title']} currently touches {top_event['exposure'] * 100:.0f}% of the book, "
            f"while the portfolio is running at {portfolio['cagr'] * 100:.1f}% CAGR and {portfolio['sharpe']:.2f} Sharpe."
        ),
        "drivers": [
            f"Positive signals cover {positive_weight * 100:.0f}% of the portfolio.",
            f"Top macro driver contributes an estimated {top_event['impact'] * 100:.1f}% portfolio effect.",
            f"Diversification score is {portfolio['diversificationScore']:.0f}/100 with {portfolio['stockCount']} holdings.",
        ],
        "additions": additions,
        "holds": holds,
        "trims": trims,
        "signals": signals,
        "scenarios": scenarios,
    }


def _build_scenarios(portfolio: dict[str, Any], top_event: dict[str, Any]) -> list[dict[str, Any]]:
    base = _clamp((portfolio["cagr"] * 0.45) + top_event["impact"] * 0.85, -0.08, 0.10)
    stress = -_clamp(portfolio["volatility"] * 0.48 + abs(top_event["impact"]) * 0.35, 0.016, 0.07)
    worst = -_clamp(abs(portfolio["maxDD"]) * 0.40 + portfolio["volatility"] * 0.30, 0.028, 0.12)
    upside = _clamp(base * 1.8 + portfolio["cagr"] * 0.25, 0.018, 0.14)

    return [
        {"label": "Base case", "value": round(base, 4), "tone": "positive", "detail": "Carry remains constructive if domestic flows stay supportive."},
        {"label": "Stress case", "value": round(stress, 4), "tone": "negative", "detail": "A delay in rate transmission or weak earnings would compress upside."},
        {"label": "Drawdown case", "value": round(worst, 4), "tone": "negative", "detail": "A risk-off global tape would hit cyclicals, leverage, and correlated exposures together."},
        {"label": "Bull case", "value": round(upside, 4), "tone": "positive", "detail": "Momentum extends if the macro tailwind coincides with strong quarterly delivery."},
    ]


def _build_pipeline(
    stocks: list[dict[str, Any]],
    portfolio: dict[str, Any],
    events: list[dict[str, Any]],
    recommendation: dict[str, Any],
    correlation: dict[str, Any],
) -> list[dict[str, str]]:
    top_event = events[0] if events else {"title": "No dominant event", "impact": 0.0, "exposure": 0.0}
    buy_count = sum(1 for stock in stocks if stock["mlSignal"] == "buy")
    sell_count = sum(1 for stock in stocks if stock["mlSignal"] == "sell")

    return [
        {
            "step": "01",
            "title": "Portfolio normalization",
            "summary": f"{portfolio['stockCount']} holdings were normalized across {len({stock['sector'] for stock in stocks})} sectors.",
            "detail": "Weights are cleaned, deduplicated, and scaled to a 100% book before any metrics are calculated.",
        },
        {
            "step": "02",
            "title": "Return stream generation",
            "summary": "Each ticker is mapped to a return series using live market data when available, otherwise a deterministic fallback engine.",
            "detail": "This keeps the app usable offline while preserving stable portfolio structure for demo mode.",
        },
        {
            "step": "03",
            "title": "Risk and return scoring",
            "summary": f"Portfolio CAGR is {portfolio['cagr'] * 100:.1f}% with volatility at {portfolio['volatility'] * 100:.1f}%.",
            "detail": "CAGR, Sharpe, volatility, drawdown, and win rate are computed from the actual weighted portfolio return stream.",
        },
        {
            "step": "04",
            "title": "Signal extraction",
            "summary": f"Model signals currently show {buy_count} BUY, {portfolio['stockCount'] - buy_count - sell_count} HOLD, and {sell_count} SELL names.",
            "detail": "RSI, moving-average spread, momentum, volatility, and drawdown are used to infer next-step conviction.",
        },
        {
            "step": "05",
            "title": "Cross-holding interaction",
            "summary": f"Average pairwise correlation is {correlation['average']:.2f}.",
            "detail": "This highlights when diversification is real versus when holdings are just different names with the same behavior.",
        },
        {
            "step": "06",
            "title": "Market event ranking",
            "summary": f"Top event: {top_event['title']} with estimated portfolio effect of {top_event['impact'] * 100:.1f}%.",
            "detail": "Sector and ticker exposure are mapped to current themes so users can see why an event matters to them specifically.",
        },
        {
            "step": "07",
            "title": "Action drafting",
            "summary": f"Recommendation is {recommendation['action']} at {recommendation['confidence'] * 100:.0f}% confidence.",
            "detail": "Position actions are split into add, hold, and trim lists so the verdict becomes executable.",
        },
        {
            "step": "08",
            "title": "Scenario testing",
            "summary": "Base, stress, drawdown, and bull cases are generated from portfolio volatility and event sensitivity.",
            "detail": "The goal is to show payoff asymmetry, not just a single upside number.",
        },
        {
            "step": "09",
            "title": "Decision brief",
            "summary": "Final output combines signals, correlations, event exposure, and scenario analysis into one operating note.",
            "detail": "This is meant for orientation and risk framing, not as a substitute for regulated financial advice.",
        },
    ]


def analyze_portfolio(stocks: list[dict[str, Any]] | None = None, period: str = "3y", aum: float = DEFAULT_AUM) -> dict[str, Any]:
    period = period if period in PERIOD_DAYS else "3y"
    normalized = normalize_portfolio(stocks)
    analyzed = [analyze_stock(item["ticker"], item["weight"], period) for item in normalized]

    returns_frame = pd.concat(
        [stock["_returns"].rename(stock["ticker"]) for stock in analyzed],
        axis=1,
    ).dropna(how="any")

    weights = pd.Series({stock["ticker"]: stock["weight"] for stock in analyzed})
    returns_frame = returns_frame[weights.index.tolist()]
    portfolio_returns = returns_frame.mul(weights, axis=1).sum(axis=1)

    portfolio = _portfolio_metrics(portfolio_returns, analyzed, aum, period)
    correlation = _correlation_payload(returns_frame)
    sector_exposure = _sector_exposure(analyzed)
    flows = _fii_dii_flows()
    events = _build_market_events(analyzed)
    recommendation = _build_recommendation(analyzed, portfolio, events, correlation, flows)
    pipeline = _build_pipeline(analyzed, portfolio, events, recommendation, correlation)

    top_event = events[0] if events else None
    for stock in analyzed:
        stock["expectedEventImpact"] = 0.0
        if top_event:
            match = next((item for item in top_event["affected"] if item["ticker"] == stock["ticker"]), None)
            if match:
                stock["expectedEventImpact"] = match["impact"]
        stock["notional"] = round(aum * stock["weight"], 2)
        stock["contribution"] = round(stock["cagr"] * stock["weight"], 4)
        stock.pop("_returns", None)

    sources = {stock["dataSource"] for stock in analyzed}
    if sources == {"live"}:
        data_source = "live"
    elif "live" in sources and "simulated" in sources:
        data_source = "mixed"
    else:
        data_source = "simulated"

    market = {
        "topEvent": top_event,
        "events": events,
        "flows": flows,
        "sectorExposure": sector_exposure,
        "narrative": (
            f"{recommendation['action']} bias is being driven by {top_event['title'].lower() if top_event else 'portfolio internals'}, "
            f"with domestic flow support partly offsetting volatility risk."
        ),
    }

    return {
        "stocks": analyzed,
        "portfolio": portfolio,
        "correlationMatrix": correlation,
        "market": market,
        "recommendation": recommendation,
        "pipeline": pipeline,
        "assumptions": [
            "Signals are derived from historical returns and deterministic factors when live data is unavailable.",
            "Event impacts are scenario estimates, not guaranteed price moves.",
            "The app is educational and should not replace advice from a registered financial professional.",
        ],
        "timestamp": _now_ist(),
        "dataSource": data_source,
    }


def analyze_single_stock(ticker: str, period: str = "3y") -> dict[str, Any]:
    return analyze_stock(ticker.upper().strip(), 1.0, period)


def get_engine_status() -> dict[str, Any]:
    return {
        "status": "ok",
        "warmup": dict(_WARMUP_STATE),
        "quantstats": QS_AVAILABLE,
        "yfinance": YF_AVAILABLE,
        "sklearn": ML_AVAILABLE,
        "timestamp": _now_ist(),
    }


def _warmup_job() -> None:
    try:
        analyze_portfolio(DEFAULT_PORTFOLIO, "1y", DEFAULT_AUM)
        _WARMUP_STATE["completed"] = True
        _WARMUP_STATE["completed_at"] = _now_ist()
    except Exception as exc:
        _WARMUP_STATE["error"] = str(exc)


def warm_engine(background: bool = True) -> None:
    with _WARMUP_LOCK:
        if _WARMUP_STATE["started"]:
            return
        _WARMUP_STATE["started"] = True
        _WARMUP_STATE["started_at"] = _now_ist()

    if background:
        thread = threading.Thread(target=_warmup_job, name="quantbrief-warmup", daemon=True)
        thread.start()
    else:
        _warmup_job()
