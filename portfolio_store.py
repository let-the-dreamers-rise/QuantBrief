from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from threading import Lock
from typing import Any

from analysis_engine import DEFAULT_AUM, DEFAULT_PORTFOLIO, normalize_portfolio


IST = timezone(timedelta(hours=5, minutes=30))
DB_PATH = Path(__file__).resolve().parent / "quantbrief.db"
_LOCK = Lock()


def _timestamp() -> str:
    return datetime.now(IST).isoformat(timespec="seconds")


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_store() -> None:
    with _LOCK:
        connection = _connect()
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS portfolio_state (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    stocks_json TEXT NOT NULL,
                    period TEXT NOT NULL,
                    aum REAL NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.commit()
            row = connection.execute("SELECT id FROM portfolio_state WHERE id = 1").fetchone()
            if row is None:
                connection.execute(
                    """
                    INSERT INTO portfolio_state (id, stocks_json, period, aum, updated_at)
                    VALUES (1, ?, ?, ?, ?)
                    """,
                    (json.dumps(DEFAULT_PORTFOLIO), "3y", DEFAULT_AUM, _timestamp()),
                )
                connection.commit()
        finally:
            connection.close()


def load_portfolio_state() -> dict[str, Any]:
    initialize_store()
    connection = _connect()
    try:
        row = connection.execute(
            "SELECT stocks_json, period, aum, updated_at FROM portfolio_state WHERE id = 1"
        ).fetchone()
    finally:
        connection.close()

    if row is None:
        return {
            "stocks": DEFAULT_PORTFOLIO,
            "period": "3y",
            "aum": DEFAULT_AUM,
            "updatedAt": _timestamp(),
        }

    stocks = normalize_portfolio(json.loads(row["stocks_json"]))
    return {
        "stocks": stocks,
        "period": row["period"],
        "aum": float(row["aum"]),
        "updatedAt": row["updated_at"],
    }


def save_portfolio_state(stocks: list[dict[str, Any]], period: str, aum: float) -> dict[str, Any]:
    normalized = normalize_portfolio(stocks)
    updated_at = _timestamp()

    with _LOCK:
        connection = _connect()
        try:
            connection.execute(
                """
                INSERT INTO portfolio_state (id, stocks_json, period, aum, updated_at)
                VALUES (1, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    stocks_json = excluded.stocks_json,
                    period = excluded.period,
                    aum = excluded.aum,
                    updated_at = excluded.updated_at
                """,
                (json.dumps(normalized), period, aum, updated_at),
            )
            connection.commit()
        finally:
            connection.close()

    return {
        "stocks": normalized,
        "period": period,
        "aum": float(aum),
        "updatedAt": updated_at,
    }
