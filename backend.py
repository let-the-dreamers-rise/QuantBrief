from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from analysis_engine import (
    DEFAULT_AUM,
    analyze_portfolio,
    get_engine_status,
    list_supported_stocks,
    warm_engine,
)
from openclaw_status import get_openclaw_status
from portfolio_store import initialize_store, load_portfolio_state, save_portfolio_state


BASE_DIR = Path(__file__).resolve().parent


class StockInput(BaseModel):
    ticker: str
    weight: float


class PortfolioRequest(BaseModel):
    stocks: list[StockInput] | None = None
    period: str = "3y"
    aum: float = Field(default=DEFAULT_AUM, gt=0)


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_store()
    warm_engine(background=True)
    yield


app = FastAPI(title="QuantBrief API", version="3.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def serve_frontend() -> FileResponse:
    return FileResponse(BASE_DIR / "index.html")


@app.get("/index.css")
async def serve_styles() -> FileResponse:
    return FileResponse(BASE_DIR / "index.css", media_type="text/css")


@app.get("/app.js")
async def serve_script() -> FileResponse:
    return FileResponse(BASE_DIR / "app.js", media_type="application/javascript")


@app.get("/api/stocks")
async def stocks() -> list[dict[str, str]]:
    return list_supported_stocks()


@app.post("/api/analyze")
async def analyze(request: PortfolioRequest) -> dict:
    try:
        payload = analyze_portfolio(
            stocks=[stock.model_dump() for stock in request.stocks] if request.stocks else None,
            period=request.period,
            aum=request.aum,
        )
        return payload
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc


@app.get("/api/portfolio")
async def get_portfolio() -> dict:
    return load_portfolio_state()


@app.put("/api/portfolio")
async def save_portfolio(request: PortfolioRequest) -> dict:
    try:
        if not request.stocks:
            raise ValueError("Portfolio must contain at least one holding.")
        return save_portfolio_state(
            stocks=[stock.model_dump() for stock in request.stocks],
            period=request.period,
            aum=request.aum,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/health")
async def health() -> dict:
    return get_engine_status()


@app.get("/api/openclaw/status")
async def openclaw_status() -> dict:
    return get_openclaw_status(BASE_DIR)


if __name__ == "__main__":
    import uvicorn

    warm_engine(background=True)
    print("\nQuantBrief backend v3.0")
    print("Serving on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
