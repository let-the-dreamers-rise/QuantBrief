const DEFAULT_AUM = 2500000;
const DEFAULT_PORTFOLIO = [
    { ticker: "RELIANCE", weight: 0.20 },
    { ticker: "HDFCBANK", weight: 0.18 },
    { ticker: "TCS", weight: 0.15 },
    { ticker: "INFY", weight: 0.12 },
    { ticker: "ICICIBANK", weight: 0.10 },
    { ticker: "BAJFINANCE", weight: 0.08 },
    { ticker: "MARUTI", weight: 0.06 },
    { ticker: "DLF", weight: 0.04 },
    { ticker: "SUNPHARMA", weight: 0.04 },
    { ticker: "LT", weight: 0.03 },
];

const FALLBACK_CATALOG = [
    { ticker: "AAPL", name: "Apple", sector: "Technology" },
    { ticker: "ADANIENT", name: "Adani Enterprises", sector: "Conglomerate" },
    { ticker: "ASIANPAINT", name: "Asian Paints", sector: "Consumer" },
    { ticker: "BAJFINANCE", name: "Bajaj Finance", sector: "NBFC" },
    { ticker: "BHARTIARTL", name: "Bharti Airtel", sector: "Telecom" },
    { ticker: "DLF", name: "DLF", sector: "Real Estate" },
    { ticker: "GOOGL", name: "Alphabet", sector: "Technology" },
    { ticker: "HCLTECH", name: "HCL Technologies", sector: "IT" },
    { ticker: "HDFCBANK", name: "HDFC Bank", sector: "Banking" },
    { ticker: "ICICIBANK", name: "ICICI Bank", sector: "Banking" },
    { ticker: "INFY", name: "Infosys", sector: "IT" },
    { ticker: "KOTAKBANK", name: "Kotak Mahindra Bank", sector: "Banking" },
    { ticker: "LT", name: "Larsen & Toubro", sector: "Infrastructure" },
    { ticker: "MARUTI", name: "Maruti Suzuki", sector: "Auto" },
    { ticker: "MSFT", name: "Microsoft", sector: "Technology" },
    { ticker: "NVDA", name: "NVIDIA", sector: "Semiconductors" },
    { ticker: "RELIANCE", name: "Reliance Industries", sector: "Conglomerate" },
    { ticker: "SBIN", name: "State Bank of India", sector: "Banking" },
    { ticker: "SUNPHARMA", name: "Sun Pharma", sector: "Pharma" },
    { ticker: "TATAMOTORS", name: "Tata Motors", sector: "Auto" },
    { ticker: "TCS", name: "Tata Consultancy Services", sector: "IT" },
    { ticker: "TITAN", name: "Titan Company", sector: "Consumer" },
    { ticker: "TSLA", name: "Tesla", sector: "Auto" },
    { ticker: "ULTRACEMCO", name: "UltraTech Cement", sector: "Cement" },
    { ticker: "WIPRO", name: "Wipro", sector: "IT" },
];

const SECTOR_PROFILES = {
    Banking: { cagr: 0.17, vol: 0.20, sharpe: 1.12 },
    NBFC: { cagr: 0.19, vol: 0.26, sharpe: 1.05 },
    IT: { cagr: 0.16, vol: 0.19, sharpe: 1.02 },
    Auto: { cagr: 0.14, vol: 0.23, sharpe: 0.92 },
    "Real Estate": { cagr: 0.18, vol: 0.29, sharpe: 0.86 },
    Pharma: { cagr: 0.13, vol: 0.17, sharpe: 1.00 },
    Infrastructure: { cagr: 0.15, vol: 0.20, sharpe: 0.97 },
    Conglomerate: { cagr: 0.14, vol: 0.18, sharpe: 0.92 },
    Telecom: { cagr: 0.12, vol: 0.15, sharpe: 0.95 },
    Consumer: { cagr: 0.13, vol: 0.16, sharpe: 0.98 },
    Cement: { cagr: 0.14, vol: 0.18, sharpe: 0.90 },
    Technology: { cagr: 0.18, vol: 0.22, sharpe: 1.05 },
    Semiconductors: { cagr: 0.21, vol: 0.30, sharpe: 1.08 },
    Unknown: { cagr: 0.12, vol: 0.18, sharpe: 0.88 },
};

const EVENT_TEMPLATES = [
    {
        title: "RBI easing bias continues to support rate-sensitive pockets",
        type: "macro",
        summary: "Lower funding costs usually help lenders, NBFCs, autos, real estate, and capex names first.",
        effects: { Banking: 0.022, NBFC: 0.034, Auto: 0.017, "Real Estate": 0.028, Infrastructure: 0.013, Conglomerate: 0.008 },
    },
    {
        title: "Large-cap IT order books remain healthy despite mixed global demand",
        type: "sector",
        summary: "Deal wins are cushioning the IT sleeve and keeping operating leverage intact.",
        effects: { IT: 0.015, Technology: 0.013, Semiconductors: 0.018 },
    },
    {
        title: "Domestic flows are absorbing foreign selling pressure",
        type: "flow",
        summary: "SIP and insurance flows continue to provide support on every dip.",
        effects: { Banking: 0.006, Consumer: 0.005, Pharma: 0.004, Conglomerate: 0.005, Infrastructure: 0.004, IT: 0.004 },
    },
    {
        title: "Crude and global risk sentiment remain the main downside watch",
        type: "risk",
        summary: "An external macro shock would pressure autos, cyclicals, and margin-sensitive holdings first.",
        effects: { Auto: -0.018, Conglomerate: -0.010, Consumer: -0.007, Infrastructure: -0.006 },
    },
];

const FLOW_SERIES = [
    { day: "Mon", fii: -1320, dii: 1550 },
    { day: "Tue", fii: -940, dii: 1180 },
    { day: "Wed", fii: -2260, dii: 1910 },
    { day: "Thu", fii: 480, dii: 760 },
    { day: "Fri", fii: -1680, dii: 2140 },
    { day: "Sat", fii: -360, dii: 620 },
    { day: "Today", fii: -1180, dii: 1480 },
];

const PALETTE = ["#d9ff63", "#7af2ba", "#ffcf70", "#ff7a84", "#99f5ff", "#c0ffb2", "#a7d0ff", "#ffe9a0", "#b6a3ff", "#8ef2d6"];
const STORAGE_KEYS = {
    portfolio: "quantbrief-v3-portfolio",
    aum: "quantbrief-v3-aum",
    period: "quantbrief-v3-period",
    analysis: "quantbrief-v3-analysis",
};

const state = {
    portfolio: [],
    aum: DEFAULT_AUM,
    period: "3y",
    analysis: null,
    catalog: [...FALLBACK_CATALOG],
    view: "overview",
    engineStatus: null,
    openclawStatus: null,
    usesBackend: false,
};

document.addEventListener("DOMContentLoaded", () => {
    bootstrap();
});

async function bootstrap() {
    hydrateState();
    state.analysis = buildFallbackAnalysis(state.portfolio, state.period, state.aum);
    initializeMotion();
    bindUI();
    populateStockSelect();
    syncInputs();
    renderAll();
    requestAnimationFrame(() => document.body.classList.add("ready"));

    await Promise.allSettled([loadCatalog(), loadEngineStatus(), loadOpenClawStatus()]);
    await loadPersistedPortfolio();
    await refreshAnalysis({ silent: true });
}

function initializeMotion() {
    document.querySelectorAll(".reveal").forEach((element) => {
        const delay = Number(element.dataset.delay || 0);
        element.style.setProperty("--delay", `${delay}ms`);
    });
}

function bindUI() {
    document.getElementById("refresh-button")?.addEventListener("click", () => refreshAnalysis());
    document.getElementById("run-analysis-button")?.addEventListener("click", () => refreshAnalysis());
    document.getElementById("jump-action-button")?.addEventListener("click", () => setView("actions"));
    document.getElementById("export-button")?.addEventListener("click", () => window.print());
    document.getElementById("add-stock-button")?.addEventListener("click", addOrUpdateHolding);
    document.getElementById("copy-openclaw-button")?.addEventListener("click", () => copyOpenClawCommand("ask"));
    document.getElementById("period-select")?.addEventListener("change", (event) => {
        state.period = event.target.value;
        persistState();
        state.analysis = buildFallbackAnalysis(state.portfolio, state.period, state.aum);
        renderAll();
        savePortfolioState({ silent: true });
    });
    document.getElementById("aum-input")?.addEventListener("change", (event) => {
        const nextValue = Number(event.target.value);
        state.aum = Number.isFinite(nextValue) && nextValue > 0 ? nextValue : DEFAULT_AUM;
        persistState();
        state.analysis = buildFallbackAnalysis(state.portfolio, state.period, state.aum);
        syncInputs();
        renderAll();
        savePortfolioState({ silent: true });
    });

    document.querySelectorAll(".nav-button, .mobile-nav-button").forEach((button) => {
        button.addEventListener("click", () => setView(button.dataset.view));
    });

    document.addEventListener("click", (event) => {
        const removeButton = event.target.closest(".pill-remove");
        if (removeButton) {
            removeHolding(removeButton.dataset.ticker);
            return;
        }
        const commandButton = event.target.closest("[data-copy-command-target]");
        if (commandButton) {
            copyOpenClawCommand(commandButton.dataset.copyCommandTarget);
        }
    });

    document.addEventListener("keydown", (event) => {
        const activeTag = document.activeElement?.tagName;
        if (["INPUT", "SELECT", "TEXTAREA"].includes(activeTag)) {
            return;
        }
        const viewMap = { "1": "overview", "2": "market", "3": "actions", "4": "deep" };
        if (viewMap[event.key]) {
            setView(viewMap[event.key]);
        }
    });
}

function hydrateState() {
    const savedPortfolio = safeParse(localStorage.getItem(STORAGE_KEYS.portfolio));
    const savedAnalysis = safeParse(localStorage.getItem(STORAGE_KEYS.analysis));
    const savedAum = Number(localStorage.getItem(STORAGE_KEYS.aum));
    const savedPeriod = localStorage.getItem(STORAGE_KEYS.period);

    state.portfolio = normalizePortfolio(Array.isArray(savedPortfolio) && savedPortfolio.length ? savedPortfolio : DEFAULT_PORTFOLIO);
    state.aum = Number.isFinite(savedAum) && savedAum > 0 ? savedAum : DEFAULT_AUM;
    state.period = ["1y", "3y", "5y"].includes(savedPeriod) ? savedPeriod : "3y";
    if (savedAnalysis && typeof savedAnalysis === "object") {
        state.analysis = savedAnalysis;
    }
}

function syncInputs() {
    const aumInput = document.getElementById("aum-input");
    const periodSelect = document.getElementById("period-select");
    if (aumInput) {
        aumInput.value = String(Math.round(state.aum));
    }
    if (periodSelect) {
        periodSelect.value = state.period;
    }
}

function persistState() {
    localStorage.setItem(STORAGE_KEYS.portfolio, JSON.stringify(state.portfolio));
    localStorage.setItem(STORAGE_KEYS.aum, String(Math.round(state.aum)));
    localStorage.setItem(STORAGE_KEYS.period, state.period);
    if (state.analysis) {
        localStorage.setItem(STORAGE_KEYS.analysis, JSON.stringify(state.analysis));
    }
}

async function loadCatalog() {
    if (!canUseApi()) {
        populateStockSelect();
        return;
    }
    try {
        const response = await fetch("/api/stocks");
        if (!response.ok) {
            throw new Error("Unable to load stock catalog.");
        }
        const catalog = await response.json();
        if (Array.isArray(catalog) && catalog.length) {
            state.catalog = catalog.sort((left, right) => left.ticker.localeCompare(right.ticker));
            populateStockSelect();
        }
    } catch (error) {
        state.catalog = [...FALLBACK_CATALOG];
        populateStockSelect();
    }
}

async function loadEngineStatus() {
    if (!canUseApi()) {
        state.engineStatus = { status: "offline", timestamp: fallbackTimestamp() };
        updateStatusPills();
        return;
    }
    try {
        const response = await fetch("/api/health");
        if (!response.ok) {
            throw new Error("Health check failed.");
        }
        state.engineStatus = await response.json();
    } catch (error) {
        state.engineStatus = { status: "offline", timestamp: fallbackTimestamp() };
    }
    updateStatusPills();
}

async function loadOpenClawStatus() {
    if (!canUseApi()) {
        state.openclawStatus = fallbackOpenClawStatus();
        renderOpenClaw();
        updateStatusPills();
        return;
    }
    try {
        const response = await fetch("/api/openclaw/status");
        if (!response.ok) {
            throw new Error("OpenClaw status request failed.");
        }
        state.openclawStatus = await response.json();
    } catch (error) {
        state.openclawStatus = fallbackOpenClawStatus();
    }
    renderOpenClaw();
    updateStatusPills();
}

async function loadPersistedPortfolio() {
    if (!canUseApi()) {
        return;
    }
    try {
        const response = await fetch("/api/portfolio");
        if (!response.ok) {
            throw new Error("Unable to load persisted portfolio.");
        }
        const payload = await response.json();
        if (Array.isArray(payload.stocks) && payload.stocks.length) {
            state.portfolio = normalizePortfolio(payload.stocks);
            state.aum = Number.isFinite(Number(payload.aum)) && Number(payload.aum) > 0 ? Number(payload.aum) : state.aum;
            state.period = ["1y", "3y", "5y"].includes(payload.period) ? payload.period : state.period;
            persistState();
            syncInputs();
            state.analysis = buildFallbackAnalysis(state.portfolio, state.period, state.aum);
            renderAll();
        }
    } catch (error) {
        // Local storage remains the fallback when the persistence endpoint is unavailable.
    }
}

async function savePortfolioState(options = {}) {
    if (!canUseApi()) {
        return false;
    }
    try {
        const response = await fetch("/api/portfolio", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                stocks: state.portfolio,
                period: state.period,
                aum: state.aum,
            }),
        });
        if (!response.ok) {
            throw new Error("Unable to persist portfolio.");
        }
        const payload = await response.json();
        if (Array.isArray(payload.stocks) && payload.stocks.length) {
            state.portfolio = normalizePortfolio(payload.stocks);
            state.period = payload.period || state.period;
            state.aum = Number.isFinite(Number(payload.aum)) && Number(payload.aum) > 0 ? Number(payload.aum) : state.aum;
            persistState();
        }
        if (!options.silent) {
            toast("Portfolio saved to the backend store.", "positive");
        }
        return true;
    } catch (error) {
        if (!options.silent) {
            toast("Saved locally. Backend persistence is unavailable.", "balanced");
        }
        return false;
    }
}

async function refreshAnalysis(options = {}) {
    const runButton = document.getElementById("run-analysis-button");
    const refreshButton = document.getElementById("refresh-button");
    setBusy([runButton, refreshButton], true);

    const fallback = buildFallbackAnalysis(state.portfolio, state.period, state.aum);
    try {
        if (!canUseApi()) {
            throw new Error("No HTTP origin detected.");
        }
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                stocks: state.portfolio,
                period: state.period,
                aum: state.aum,
            }),
        });
        if (!response.ok) {
            throw new Error(`Analysis failed with status ${response.status}`);
        }
        state.analysis = await response.json();
        state.usesBackend = true;
        localStorage.setItem(STORAGE_KEYS.analysis, JSON.stringify(state.analysis));
        if (!options.silent) {
            toast("Analysis refreshed from the backend.", "positive");
        }
    } catch (error) {
        state.analysis = fallback;
        state.usesBackend = false;
        localStorage.setItem(STORAGE_KEYS.analysis, JSON.stringify(state.analysis));
        if (!options.silent) {
            toast("Backend unavailable, using local demo analytics.", "balanced");
        }
    }

    persistState();
    updateStatusPills();
    renderAll();
    setBusy([runButton, refreshButton], false);
}

function addOrUpdateHolding() {
    const stockSelect = document.getElementById("stock-select");
    const weightInput = document.getElementById("weight-input");
    const ticker = stockSelect?.value?.trim();
    const nextWeight = Number(weightInput?.value);

    if (!ticker || !Number.isFinite(nextWeight) || nextWeight <= 0) {
        toast("Choose a stock and a valid weight percentage.", "negative");
        return;
    }

    const normalizedWeight = nextWeight / 100;
    const existing = state.portfolio.find((item) => item.ticker === ticker);
    if (existing) {
        existing.weight = normalizedWeight;
    } else {
        state.portfolio.push({ ticker, weight: normalizedWeight });
    }

    state.portfolio = normalizePortfolio(state.portfolio);
    state.analysis = buildFallbackAnalysis(state.portfolio, state.period, state.aum);
    persistState();
    renderAll();
    savePortfolioState({ silent: true });

    if (stockSelect) {
        stockSelect.value = "";
    }
    if (weightInput) {
        weightInput.value = "";
    }

    toast(`${ticker} is in the book. Run analysis to refresh live data.`, "positive");
}

function removeHolding(ticker) {
    if (state.portfolio.length <= 1) {
        toast("Keep at least one holding in the portfolio.", "negative");
        return;
    }
    state.portfolio = normalizePortfolio(state.portfolio.filter((item) => item.ticker !== ticker));
    state.analysis = buildFallbackAnalysis(state.portfolio, state.period, state.aum);
    persistState();
    renderAll();
    savePortfolioState({ silent: true });
    toast(`${ticker} removed from the portfolio.`, "balanced");
}

function setView(view) {
    state.view = view;
    document.querySelectorAll(".view").forEach((panel) => {
        panel.classList.toggle("is-active", panel.id === `view-${view}`);
    });
    document.querySelectorAll(".nav-button, .mobile-nav-button").forEach((button) => {
        button.classList.toggle("is-active", button.dataset.view === view);
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function populateStockSelect() {
    const select = document.getElementById("stock-select");
    if (!select) {
        return;
    }
    const previousValue = select.value;
    const options = ['<option value="">Select stock</option>'];
    state.catalog.forEach((stock) => {
        options.push(`<option value="${stock.ticker}">${stock.ticker} - ${stock.name}</option>`);
    });
    select.innerHTML = options.join("");
    if (previousValue && state.catalog.some((stock) => stock.ticker === previousValue)) {
        select.value = previousValue;
    }
}

function buildFallbackAnalysis(portfolio, period, aum) {
    const normalized = normalizePortfolio(portfolio);
    const stocks = normalized.map((item) => buildSeedStock(item, period));
    const correlationMatrix = buildCorrelationMatrix(stocks);
    const portfolioMetrics = buildPortfolioMetrics(stocks, correlationMatrix, aum, period);
    const events = buildEvents(stocks);
    const sectorExposure = buildSectorExposure(stocks);
    const topEvent = events[0] || null;
    const recommendation = buildRecommendation(stocks, portfolioMetrics, correlationMatrix, topEvent);
    const pipeline = buildPipeline(stocks, portfolioMetrics, correlationMatrix, topEvent, recommendation);

    return {
        stocks,
        portfolio: portfolioMetrics,
        correlationMatrix,
        market: {
            topEvent,
            events,
            flows: FLOW_SERIES.map((item) => ({ ...item, net: item.fii + item.dii })),
            sectorExposure,
            narrative: topEvent
                ? `${topEvent.title} is the biggest driver in this mix, while institutional flows are still cushioning drawdowns.`
                : "The portfolio is running without a single dominant event right now.",
        },
        recommendation,
        pipeline,
        assumptions: [
            "Fallback mode uses deterministic market proxies instead of live prices.",
            "Event impacts are scenario estimates designed for decision framing, not exact forecasts.",
            "QuantBrief is educational and should not replace advice from a registered financial professional.",
        ],
        timestamp: fallbackTimestamp(),
        dataSource: "demo",
    };
}

function buildSeedStock(position, period) {
    const meta = lookupStock(position.ticker);
    const profile = SECTOR_PROFILES[meta.sector] || SECTOR_PROFILES.Unknown;
    const rand = makeRng(`${position.ticker}:${period}`);
    const cagr = clamp(profile.cagr + (rand() - 0.5) * 0.08, 0.05, 0.32);
    const volatility = clamp(profile.vol + (rand() - 0.5) * 0.09, 0.11, 0.38);
    const sharpe = clamp(profile.sharpe + (rand() - 0.5) * 0.45, 0.45, 1.9);
    const maxDD = -clamp(volatility * 0.78 + rand() * 0.09, 0.08, 0.42);
    const oneMonthChange = clamp((rand() - 0.42) * 0.18, -0.14, 0.18);
    const signalScore = cagr * 1.4 + sharpe * 0.12 - volatility * 0.65 - Math.abs(maxDD) * 0.30 + oneMonthChange * 0.70;
    const mlProb = clamp(0.48 + signalScore + (rand() - 0.5) * 0.08, 0.22, 0.84);
    const mlSignal = mlProb >= 0.58 ? "buy" : mlProb <= 0.43 ? "sell" : "hold";
    const sparkline = buildSparkline(position.ticker, period, cagr, volatility, oneMonthChange);
    const conviction = clamp((cagr * 2.2) + (sharpe * 0.15) + ((mlProb - 0.5) * 1.5) - Math.abs(maxDD) * 0.45, 0, 1);

    return {
        ticker: position.ticker,
        name: meta.name,
        sector: meta.sector,
        weight: round(position.weight, 6),
        cagr: round(cagr, 4),
        sharpe: round(sharpe, 2),
        volatility: round(volatility, 4),
        maxDD: round(maxDD, 4),
        mlSignal,
        mlProb: round(mlProb, 4),
        oneMonthChange: round(oneMonthChange, 4),
        sparkline,
        thesis: `${meta.sector} exposure looks ${mlSignal === "buy" ? "constructive" : mlSignal === "sell" ? "fragile" : "balanced"} with ${Math.round(mlProb * 100)}% model confidence.`,
        conviction: round(conviction, 4),
        dataSource: "demo",
        notional: round(position.weight * state.aum, 2),
        contribution: round(position.weight * cagr, 4),
        expectedEventImpact: 0,
    };
}

function buildCorrelationMatrix(stocks) {
    const matrix = stocks.map((left, rowIndex) => {
        return stocks.map((right, colIndex) => {
            if (rowIndex === colIndex) {
                return 1;
            }
            const pairSeed = hashString(`${left.ticker}:${right.ticker}`);
            const base = left.sector === right.sector ? 0.66 : 0.24;
            const modifier = (((pairSeed % 1000) / 1000) - 0.5) * 0.18;
            return round(clamp(base + modifier, -0.12, 0.94), 2);
        });
    });

    let total = 0;
    let count = 0;
    matrix.forEach((row, rowIndex) => {
        row.forEach((value, colIndex) => {
            if (rowIndex !== colIndex) {
                total += Math.abs(value);
                count += 1;
            }
        });
    });

    return {
        tickers: stocks.map((stock) => stock.ticker),
        matrix,
        average: count ? round(total / count, 2) : 0,
    };
}

function buildPortfolioMetrics(stocks, correlationMatrix, aum, period) {
    const cagr = stocks.reduce((sumValue, stock) => sumValue + stock.weight * stock.cagr, 0);
    let variance = 0;
    stocks.forEach((left, rowIndex) => {
        stocks.forEach((right, colIndex) => {
            variance += left.weight * right.weight * left.volatility * right.volatility * correlationMatrix.matrix[rowIndex][colIndex];
        });
    });
    const volatility = Math.sqrt(Math.max(variance, 0));
    const sharpe = volatility > 0 ? cagr / volatility : 0;
    const maxDD = -clamp(stocks.reduce((sumValue, stock) => sumValue + stock.weight * Math.abs(stock.maxDD), 0) * 0.78, 0.08, 0.36);
    const concentration = stocks.reduce((sumValue, stock) => sumValue + stock.weight ** 2, 0);
    const diversificationScore = clamp(96 - concentration * 150 - correlationMatrix.average * 26 + stocks.length * 1.8, 32, 90);
    const years = period === "1y" ? 1 : period === "5y" ? 5 : 3;
    const currentValue = aum * Math.pow(1 + cagr, years);
    const netProfit = currentValue - aum;
    const winRate = clamp(0.48 + sharpe * 0.05, 0.44, 0.67);

    return {
        aum,
        period,
        cagr: round(cagr, 4),
        sharpe: round(sharpe, 2),
        volatility: round(volatility, 4),
        maxDD: round(maxDD, 4),
        winRate: round(winRate, 4),
        currentValue: round(currentValue, 2),
        netProfit: round(netProfit, 2),
        diversificationScore: round(diversificationScore, 1),
        stockCount: stocks.length,
        healthLabel: portfolioHealthLabel(cagr, sharpe, maxDD),
    };
}

function buildEvents(stocks) {
    const events = EVENT_TEMPLATES.map((template) => {
        const affected = [];
        let impact = 0;
        let exposure = 0;

        stocks.forEach((stock) => {
            const stockImpact = template.effects[stock.sector] || 0;
            if (!stockImpact) {
                return;
            }
            impact += stock.weight * stockImpact;
            exposure += stock.weight;
            affected.push({
                ticker: stock.ticker,
                weight: round(stock.weight, 4),
                impact: round(stockImpact, 4),
                confidence: stock.mlProb,
            });
        });

        return {
            title: template.title,
            type: template.type,
            summary: template.summary,
            impact: round(impact, 4),
            exposure: round(exposure, 4),
            direction: impact >= 0 ? "positive" : "negative",
            severity: Math.abs(impact) >= 0.018 ? "high" : Math.abs(impact) >= 0.009 ? "medium" : "low",
            affectedTickers: affected.map((item) => item.ticker),
            affected: affected.sort((left, right) => Math.abs(right.impact * right.weight) - Math.abs(left.impact * left.weight)),
        };
    });

    const ranked = events.filter((event) => event.affected.length).sort((left, right) => Math.abs(right.impact) - Math.abs(left.impact));
    const topEvent = ranked[0];
    if (topEvent) {
        stocks.forEach((stock) => {
            const match = topEvent.affected.find((item) => item.ticker === stock.ticker);
            stock.expectedEventImpact = match ? match.impact : 0;
        });
    }
    return ranked;
}

function buildSectorExposure(stocks) {
    const grouped = new Map();
    stocks.forEach((stock) => {
        if (!grouped.has(stock.sector)) {
            grouped.set(stock.sector, { sector: stock.sector, weight: 0, confidence: 0, count: 0 });
        }
        const row = grouped.get(stock.sector);
        row.weight += stock.weight;
        row.confidence += stock.mlProb;
        row.count += 1;
    });

    return Array.from(grouped.values())
        .map((row) => {
            const confidence = row.count ? row.confidence / row.count : 0.5;
            return {
                sector: row.sector,
                weight: round(row.weight, 4),
                confidence: round(confidence, 4),
                tone: confidence >= 0.57 ? "positive" : confidence <= 0.44 ? "negative" : "balanced",
            };
        })
        .sort((left, right) => right.weight - left.weight);
}

function buildRecommendation(stocks, portfolioMetrics, correlationMatrix, topEvent) {
    const avgProb = average(stocks.map((stock) => stock.mlProb));
    const positiveWeight = sum(stocks.filter((stock) => stock.mlProb >= 0.54).map((stock) => stock.weight));
    const negativeWeight = sum(stocks.filter((stock) => stock.mlProb <= 0.42).map((stock) => stock.weight));
    const netFlows = sum(FLOW_SERIES.map((item) => item.fii + item.dii)) / 10000;
    const topImpact = topEvent ? topEvent.impact : 0;

    const score = clamp(
        avgProb * 0.40
        + positiveWeight * 0.18
        - negativeWeight * 0.10
        + clamp(topImpact * 8, -0.18, 0.20)
        + clamp(portfolioMetrics.sharpe / 6, 0, 0.16)
        + clamp(portfolioMetrics.diversificationScore / 220, 0, 0.14)
        + clamp(netFlows, -0.05, 0.08)
        - clamp(Math.abs(portfolioMetrics.maxDD) * 0.22, 0, 0.10)
        - clamp(correlationMatrix.average / 14, 0, 0.08),
        0,
        1
    );

    const action = score >= 0.59 ? "ACCUMULATE" : score >= 0.44 ? "HOLD" : "REDUCE";
    const confidence = clamp(0.61 + Math.abs(score - 0.5) * 0.80 + Math.abs(topImpact) * 3.2, 0.58, 0.92);
    const ranked = [...stocks].sort((left, right) => right.conviction - left.conviction);

    return {
        action,
        confidence: round(confidence, 4),
        summary: `${action} with ${Math.round(confidence * 100)}% confidence. ${topEvent ? `${topEvent.title} currently touches ${Math.round(topEvent.exposure * 100)}% of the book.` : "No single event dominates the book right now."} The portfolio is running at ${formatPercent(portfolioMetrics.cagr, 1)} CAGR and ${portfolioMetrics.sharpe.toFixed(2)} Sharpe.`,
        drivers: [
            `${Math.round(positiveWeight * 100)}% of the portfolio is sitting in positive or improving signal zones.`,
            `Top event contribution is ${formatPercent(topImpact, 1, true)} at the portfolio level.`,
            `Diversification score is ${Math.round(portfolioMetrics.diversificationScore)}/100 across ${portfolioMetrics.stockCount} holdings.`,
        ],
        additions: ranked.filter((stock) => stock.mlSignal === "buy").slice(0, 3).map((stock) => ({
            ticker: stock.ticker,
            label: stock.name,
            reason: stock.thesis,
            signal: stock.mlSignal,
            confidence: stock.mlProb,
        })),
        holds: ranked.filter((stock) => stock.mlSignal !== "sell").slice(0, 3).map((stock) => ({
            ticker: stock.ticker,
            label: stock.name,
            reason: stock.thesis,
            signal: stock.mlSignal,
            confidence: stock.mlProb,
        })),
        trims: [...stocks]
            .sort((left, right) => right.volatility - left.volatility || left.mlProb - right.mlProb)
            .slice(0, 3)
            .map((stock) => ({
                ticker: stock.ticker,
                label: stock.name,
                reason: `Volatility is running at ${formatPercent(stock.volatility, 1)} with drawdown near ${formatPercent(stock.maxDD, 1, true)}.`,
                signal: stock.mlSignal,
                confidence: stock.mlProb,
            })),
        signals: [
            { label: "Model support", value: `${Math.round(avgProb * 100)}% avg`, tone: avgProb >= 0.56 ? "positive" : avgProb <= 0.44 ? "negative" : "balanced" },
            { label: "Portfolio Sharpe", value: portfolioMetrics.sharpe.toFixed(2), tone: portfolioMetrics.sharpe >= 1 ? "positive" : "balanced" },
            { label: "Top event exposure", value: topEvent ? `${Math.round(topEvent.exposure * 100)}%` : "0%", tone: topEvent && topEvent.impact < 0 ? "negative" : "positive" },
            { label: "Correlation drag", value: correlationMatrix.average.toFixed(2), tone: correlationMatrix.average > 0.56 ? "negative" : "balanced" },
        ],
        scenarios: buildScenarios(portfolioMetrics, topImpact),
    };
}

function buildScenarios(portfolioMetrics, topImpact) {
    const base = clamp((portfolioMetrics.cagr * 0.48) + topImpact * 0.85, -0.08, 0.10);
    const stress = -clamp(portfolioMetrics.volatility * 0.52 + Math.abs(topImpact) * 0.40, 0.02, 0.07);
    const drawdown = -clamp(Math.abs(portfolioMetrics.maxDD) * 0.42 + portfolioMetrics.volatility * 0.28, 0.03, 0.12);
    const bull = clamp(base * 1.9 + portfolioMetrics.cagr * 0.25, 0.02, 0.14);

    return [
        { label: "Base case", value: round(base, 4), tone: "positive", detail: "Carry remains constructive if domestic flows stay supportive." },
        { label: "Stress case", value: round(stress, 4), tone: "negative", detail: "A delay in rate transmission or weak earnings would compress upside." },
        { label: "Drawdown case", value: round(drawdown, 4), tone: "negative", detail: "A risk-off global tape would hit cyclicals, leverage, and crowded exposures together." },
        { label: "Bull case", value: round(bull, 4), tone: "positive", detail: "Momentum extends if the macro tailwind lands alongside strong company delivery." },
    ];
}

function buildPipeline(stocks, portfolioMetrics, correlationMatrix, topEvent, recommendation) {
    const buyCount = stocks.filter((stock) => stock.mlSignal === "buy").length;
    const sellCount = stocks.filter((stock) => stock.mlSignal === "sell").length;

    return [
        { step: "01", title: "Portfolio normalization", summary: `${portfolioMetrics.stockCount} holdings were normalized into a fully weighted book.`, detail: "Edits are deduplicated and rescaled so every downstream metric works off a coherent allocation." },
        { step: "02", title: "Return stream generation", summary: "Each holding receives either a live series or a deterministic fallback proxy.", detail: "That keeps the app usable even when the backend or market dependencies are offline." },
        { step: "03", title: "Risk and return scoring", summary: `Portfolio CAGR is ${formatPercent(portfolioMetrics.cagr, 1)} with volatility at ${formatPercent(portfolioMetrics.volatility, 1)}.`, detail: "Risk, return, drawdown, and win-rate are blended into the operating snapshot." },
        { step: "04", title: "Signal extraction", summary: `Signals currently show ${buyCount} BUY, ${portfolioMetrics.stockCount - buyCount - sellCount} HOLD, and ${sellCount} SELL names.`, detail: "Momentum, drawdown, volatility, and relative trend create the current model posture." },
        { step: "05", title: "Cross-holding interaction", summary: `Average pairwise correlation is ${correlationMatrix.average.toFixed(2)}.`, detail: "This is where the app checks whether diversification is real or only cosmetic." },
        { step: "06", title: "Market event ranking", summary: topEvent ? `Top event: ${topEvent.title} at ${formatPercent(topEvent.impact, 1, true)}.` : "No single event dominates the portfolio right now.", detail: "Event weights are mapped back to the actual sector mix in your book." },
        { step: "07", title: "Action drafting", summary: `${recommendation.action} is the current posture at ${Math.round(recommendation.confidence * 100)}% confidence.`, detail: "Action lanes turn the verdict into adds, holds, and de-risk candidates." },
        { step: "08", title: "Scenario testing", summary: "Base, stress, drawdown, and bull cases frame the payoff range.", detail: "The goal is to show how skew changes, not to predict a single target price." },
        { step: "09", title: "Decision brief", summary: "Everything compresses into one operating note for the user-facing brief.", detail: "This is a decision-support output, not regulated financial advice." },
    ];
}

function buildSparkline(ticker, period, cagr, volatility, oneMonthChange) {
    const rand = makeRng(`spark:${ticker}:${period}`);
    const points = [];
    let value = 100;
    const phase = rand() * Math.PI * 2;
    for (let index = 0; index < 40; index += 1) {
        const drift = (cagr / 252) * 0.85;
        const wave = Math.sin(index / 4 + phase) * (volatility * 7);
        const noise = (rand() - 0.5) * volatility * 9;
        value *= 1 + drift + wave / 1000 + noise / 1000 + (index > 28 ? oneMonthChange / 90 : 0);
        points.push(round(value, 2));
    }
    const base = points[0] || 100;
    return points.map((point) => round((point / base) * 100, 2));
}

function lookupStock(ticker) {
    return state.catalog.find((item) => item.ticker === ticker)
        || FALLBACK_CATALOG.find((item) => item.ticker === ticker)
        || { ticker, name: ticker, sector: "Unknown" };
}

function normalizePortfolio(portfolio) {
    const aggregate = new Map();
    portfolio.forEach((item) => {
        if (!item?.ticker) {
            return;
        }
        const ticker = String(item.ticker).toUpperCase().trim();
        const weight = Number(item.weight);
        if (!Number.isFinite(weight) || weight <= 0) {
            return;
        }
        aggregate.set(ticker, (aggregate.get(ticker) || 0) + weight);
    });

    const total = sum(Array.from(aggregate.values()));
    if (!total) {
        return DEFAULT_PORTFOLIO.map((item) => ({ ...item }));
    }

    return Array.from(aggregate.entries())
        .map(([ticker, weight]) => ({ ticker, weight: weight / total }))
        .sort((left, right) => right.weight - left.weight);
}

function canUseApi() {
    return window.location.protocol.startsWith("http");
}

function fallbackOpenClawStatus() {
    return {
        status: "partial",
        headline: "QuantBrief can still behave like an OpenClaw copilot while the gateway status is unavailable.",
        summary: "Workspace file ready | Gateway state unknown | WhatsApp not configured | Telegram not configured",
        workspaceNote: "Launch OpenClaw from this project folder so the QuantBrief MCP server and skill attach to the right workspace.",
        model: "OpenClaw status unavailable",
        gateway: {
            configured: false,
            reachable: false,
            port: 18789,
            mode: "local",
            bind: "loopback",
            authMode: "token",
        },
        workspace: {
            configured: true,
            mcpRegistered: true,
            skillRegistered: true,
            projectPath: window.location.href,
            defaultWorkspace: "",
            matchesProject: true,
            mcpCwd: "",
        },
        channels: {
            whatsappConfigured: false,
            telegramConfigured: false,
        },
        commands: {
            ask: 'openclaw agent --local --session-id qb --message "How does my portfolio look?"',
            channels: "openclaw configure --section channels",
            gateway: "openclaw gateway run --force",
            probe: "openclaw gateway probe",
        },
        surfaces: [
            {
                id: "local-agent",
                label: "Local Agent",
                status: "ready",
                detail: "Run QuantBrief from the CLI in this repo for the cleanest OpenClaw-native flow.",
                meta: "Best for live testing while the backend is open.",
                actionLabel: "Copy CLI prompt",
                command: 'openclaw agent --local --session-id qb --message "How does my portfolio look?"',
            },
            {
                id: "gateway",
                label: "Gateway",
                status: "setup",
                detail: "Start the OpenClaw gateway to make channels and browser clients feel first-class.",
                meta: "Loopback mode on port 18789 is the default local setup.",
                actionLabel: "Copy gateway run",
                command: "openclaw gateway run --force",
            },
            {
                id: "whatsapp",
                label: "WhatsApp",
                status: "setup",
                detail: "Use OpenClaw channel setup to turn WhatsApp into a QuantBrief front door.",
                meta: "Great for mobile-first investor check-ins.",
                actionLabel: "Copy channel setup",
                command: "openclaw configure --section channels",
            },
            {
                id: "telegram",
                label: "Telegram",
                status: "setup",
                detail: "Telegram can mirror the same QuantBrief agent flow once channels are configured.",
                meta: "Useful when you want bot UX without the terminal.",
                actionLabel: "Copy channel setup",
                command: "openclaw configure --section channels",
            },
        ],
    };
}

function getOpenClawStatus() {
    return state.openclawStatus || fallbackOpenClawStatus();
}

async function copyOpenClawCommand(target) {
    const status = getOpenClawStatus();
    const command = status.commands?.[target] || status.surfaces?.find((item) => item.id === target)?.command;
    if (!command) {
        toast("No OpenClaw command is available for that action yet.", "negative");
        return;
    }
    try {
        await navigator.clipboard.writeText(command);
        const labelMap = {
            ask: "OpenClaw agent prompt copied.",
            gateway: "OpenClaw gateway command copied.",
            channels: "OpenClaw channel setup command copied.",
            probe: "OpenClaw probe command copied.",
        };
        toast(labelMap[target] || "OpenClaw command copied.", "positive");
    } catch (error) {
        toast("Clipboard access is blocked in this browser.", "negative");
    }
}

function setBusy(buttons, busy) {
    buttons.filter(Boolean).forEach((button) => {
        button.disabled = busy;
        if (button.id === "run-analysis-button") {
            button.textContent = busy ? "Running..." : "Run analysis";
        }
        if (button.id === "refresh-button") {
            button.textContent = busy ? "Refreshing..." : "Refresh analysis";
        }
    });
}

function portfolioHealthLabel(cagr, sharpe, maxDD) {
    const score = (cagr * 3.1) + (sharpe * 0.18) - Math.abs(maxDD) * 0.75;
    if (score >= 0.85) return "Constructive";
    if (score >= 0.58) return "Stable";
    if (score >= 0.32) return "Mixed";
    return "Fragile";
}

function fallbackTimestamp() {
    return new Intl.DateTimeFormat("en-IN", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "Asia/Kolkata",
    }).format(new Date());
}

function safeParse(value) {
    if (!value) {
        return null;
    }
    try {
        return JSON.parse(value);
    } catch (error) {
        return null;
    }
}

function makeRng(seedText) {
    let seed = hashString(seedText) || 1;
    return () => {
        seed = (seed * 1664525 + 1013904223) >>> 0;
        return seed / 4294967296;
    };
}

function hashString(value) {
    let hash = 2166136261;
    for (let index = 0; index < value.length; index += 1) {
        hash ^= value.charCodeAt(index);
        hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
}

function clamp(value, minimum, maximum) {
    return Math.min(Math.max(value, minimum), maximum);
}

function sum(values) {
    return values.reduce((total, value) => total + value, 0);
}

function average(values) {
    return values.length ? sum(values) / values.length : 0;
}

function round(value, digits = 2) {
    return Number(value.toFixed(digits));
}

function renderAll() {
    if (!state.analysis) {
        return;
    }
    renderHero();
    renderOpenClaw();
    renderPortfolioStrip();
    renderAllocation();
    renderSnapshot();
    renderPositions();
    renderCorrelation();
    renderScenarios();
    renderMarket();
    renderActions();
    renderDeep();
    updateStatusPills();
}

function renderHero() {
    const analysis = state.analysis;
    const topEvent = analysis.market.topEvent;
    const titleMap = {
        ACCUMULATE: "OpenClaw sees room to add, but only into the strongest pockets.",
        HOLD: "OpenClaw wants the book held together while fresh risk stays selective.",
        REDUCE: "OpenClaw is flagging weaker exposure before you reach for more upside.",
    };

    setText("hero-title", titleMap[analysis.recommendation.action] || "See what changed, what matters, and what to do next.");
    setText("hero-summary", analysis.recommendation.summary);
    setText("metric-decision", analysis.recommendation.action);
    setText("metric-confidence", `${Math.round(analysis.recommendation.confidence * 100)}% confidence`);
    setText("metric-cagr", formatPercent(analysis.portfolio.cagr, 1));
    setText("metric-health", `${analysis.portfolio.healthLabel} profile`);
    setText("metric-sharpe", analysis.portfolio.sharpe.toFixed(2));
    setText("metric-volatility", `Vol ${formatPercent(analysis.portfolio.volatility, 1)}`);
    setText("metric-value", formatCompactMoney(analysis.portfolio.currentValue));
    setText("metric-profit", `${analysis.portfolio.netProfit >= 0 ? "+" : "-"}${formatCompactMoney(Math.abs(analysis.portfolio.netProfit))}`);
    setText("allocation-note", topEvent ? `Top driver: ${topEvent.title}` : "No single event dominates this book right now.");
}

function renderOpenClaw() {
    const status = getOpenClawStatus();
    setText("openclaw-headline", status.headline || "QuantBrief is being shaped into an OpenClaw-first product.");
    setText("openclaw-summary", status.summary || "Gateway, workspace, and channels are loading.");
    setText("openclaw-note", status.workspaceNote || "OpenClaw context will appear here.");

    const points = document.getElementById("openclaw-points");
    const channelGrid = document.getElementById("channel-grid");

    if (points) {
        points.innerHTML = [
            openclawPoint(
                status.gateway?.reachable ? "ready" : status.gateway?.configured ? "setup" : "offline",
                "Gateway",
                status.gateway?.reachable
                    ? `Live on ws://127.0.0.1:${status.gateway.port} with ${status.gateway.authMode} auth.`
                    : `Not fully reachable yet. Expected local port ${status.gateway?.port || 18789}.`
            ),
            openclawPoint(
                status.workspace?.configured && status.workspace?.mcpRegistered ? "ready" : "setup",
                "Workspace",
                status.workspace?.matchesProject === false
                    ? "Global OpenClaw defaults point elsewhere, so launch QuantBrief from this folder."
                    : "QuantBrief ships its own workspace file, MCP registration, and local skill."
            ),
            openclawPoint(
                status.channels?.whatsappConfigured || status.channels?.telegramConfigured ? "setup" : "offline",
                "Channels",
                status.channels?.whatsappConfigured || status.channels?.telegramConfigured
                    ? "At least one mobile channel is configured. Finish the rest to make QuantBrief fully chat-first."
                    : "WhatsApp and Telegram still need setup through the OpenClaw channel wizard."
            ),
        ].join("");
    }

    if (channelGrid) {
        channelGrid.innerHTML = (status.surfaces || []).map((surface) => `
            <article class="channel-card">
                <div class="channel-topline">
                    <div>
                        <p class="panel-kicker">${surface.label}</p>
                        <strong>${surface.label}</strong>
                    </div>
                    <span class="channel-status ${surface.status}">${surface.status}</span>
                </div>
                <p>${surface.detail}</p>
                <small>${surface.meta}</small>
                <button class="ghost-button" data-copy-command-target="${surface.id === "gateway" && surface.status === "ready" ? "probe" : surface.id === "local-agent" ? "ask" : surface.id === "gateway" ? "gateway" : "channels"}" type="button">${surface.actionLabel}</button>
            </article>
        `).join("");
    }
}

function renderPortfolioStrip() {
    const container = document.getElementById("portfolio-strip");
    if (!container) {
        return;
    }
    const total = sum(state.portfolio.map((item) => item.weight));
    container.innerHTML = [
        ...state.portfolio.map((item) => `
            <div class="position-pill">
                <strong>${item.ticker}</strong>
                <span class="mono">${formatPercent(item.weight, 1)}</span>
                <button class="pill-remove" data-ticker="${item.ticker}" type="button">x</button>
            </div>
        `),
        `<div class="position-pill"><strong>Total</strong><span class="mono">${formatPercent(total, 1)}</span></div>`,
    ].join("");
}

function renderAllocation() {
    const ring = document.getElementById("allocation-ring");
    const legend = document.getElementById("allocation-legend");
    if (!ring || !legend) {
        return;
    }

    let offset = 0;
    const stops = state.analysis.stocks.map((stock, index) => {
        const start = offset * 360;
        offset += stock.weight;
        const end = offset * 360;
        return `${PALETTE[index % PALETTE.length]} ${start}deg ${end}deg`;
    });

    ring.style.background = `conic-gradient(${stops.join(", ")})`;
    setText("allocation-value", formatCompactMoney(state.analysis.portfolio.aum));
    setText("allocation-caption", `${state.analysis.portfolio.stockCount} holdings`);

    legend.innerHTML = state.analysis.stocks.map((stock, index) => `
        <div class="legend-line">
            <span class="legend-swatch" style="background:${PALETTE[index % PALETTE.length]}"></span>
            <div>
                <strong>${stock.ticker}</strong>
                <div class="position-subtitle">${stock.name}</div>
            </div>
            <span class="mono">${formatPercent(stock.weight, 1)}</span>
        </div>
    `).join("");
}

function renderSnapshot() {
    const snapshotGrid = document.getElementById("snapshot-grid");
    const sectorStack = document.getElementById("sector-stack");
    if (!snapshotGrid || !sectorStack) {
        return;
    }

    const topEvent = state.analysis.market.topEvent;
    snapshotGrid.innerHTML = [
        snapshotCard("Win rate", `${Math.round(state.analysis.portfolio.winRate * 100)}%`, "Percentage of positive sessions across the portfolio stream."),
        snapshotCard("Drawdown", formatPercent(state.analysis.portfolio.maxDD, 1, true), "Worst historical retreat in the current analysis window."),
        snapshotCard("Diversification", `${Math.round(state.analysis.portfolio.diversificationScore)}/100`, "Higher means the book is less crowded into a single move."),
        snapshotCard("Top event", topEvent ? formatPercent(topEvent.impact, 1, true) : "0.0%", topEvent ? topEvent.title : "No dominant event"),
    ].join("");

    sectorStack.innerHTML = state.analysis.market.sectorExposure.map((row) => sectorBar(row)).join("");
}

function renderPositions() {
    const container = document.getElementById("positions-table");
    if (!container) {
        return;
    }
    const rows = state.analysis.stocks.map((stock) => `
        <div class="position-row">
            <div class="position-primary">
                <strong>${stock.ticker}</strong>
                <span class="position-subtitle">${stock.name}</span>
                <small>${stock.thesis}</small>
            </div>
            <div class="mono">${formatPercent(stock.weight, 1)}</div>
            <div>
                ${sparklineSVG(stock.sparkline, stock.mlSignal)}
                <small class="${toneTextClass(stock.oneMonthChange)}">${formatPercent(stock.oneMonthChange, 1, true)} 1M</small>
            </div>
            <div class="mono ${toneTextClass(stock.cagr)}">${formatPercent(stock.cagr, 1)}</div>
            <div class="mono">${stock.sharpe.toFixed(2)}</div>
            <div>
                <div class="mono">${formatPercent(stock.volatility, 1)}</div>
                <small>${formatPercent(stock.maxDD, 1, true)} max DD</small>
            </div>
            <div>
                <span class="signal-tag ${stock.mlSignal}">${stock.mlSignal.toUpperCase()} ${Math.round(stock.mlProb * 100)}%</span>
                <small>${formatPercent(stock.expectedEventImpact, 1, true)} event</small>
            </div>
        </div>
    `).join("");

    container.innerHTML = `
        <div class="position-row position-header">
            <div>Holding</div>
            <div>Weight</div>
            <div>Trend</div>
            <div>CAGR</div>
            <div>Sharpe</div>
            <div>Risk</div>
            <div>Signal</div>
        </div>
        ${rows}
    `;
}

function renderCorrelation() {
    const container = document.getElementById("correlation-grid");
    if (!container) {
        return;
    }
    const tickers = state.analysis.correlationMatrix.tickers.slice(0, 6);
    const matrix = state.analysis.correlationMatrix.matrix.slice(0, 6).map((row) => row.slice(0, 6));
    container.style.gridTemplateColumns = `repeat(${tickers.length + 1}, minmax(0, 1fr))`;
    const html = ['<div class="matrix-cell header"></div>'];

    tickers.forEach((ticker) => html.push(`<div class="matrix-cell header">${ticker}</div>`));
    matrix.forEach((row, rowIndex) => {
        html.push(`<div class="matrix-cell header">${tickers[rowIndex]}</div>`);
        row.forEach((value) => {
            const tone = value >= 0.6 ? "positive" : value <= 0.15 ? "negative" : "balanced";
            html.push(`<div class="matrix-cell tone-${tone}">${value.toFixed(2)}</div>`);
        });
    });
    container.innerHTML = html.join("");
}

function renderScenarios() {
    const container = document.getElementById("scenario-list");
    if (!container) {
        return;
    }
    container.innerHTML = state.analysis.recommendation.scenarios.map((scenario) => `
        <div class="scenario-card">
            <strong class="${toneTextClass(scenario.value)}">${scenario.label}: ${formatPercent(scenario.value, 1, true)}</strong>
            <small>${scenario.detail}</small>
        </div>
    `).join("");
}

function renderMarket() {
    const topEvent = state.analysis.market.topEvent;
    setText("market-headline", topEvent ? topEvent.title : "No dominant market event");
    setText("market-summary", topEvent ? topEvent.summary : "Portfolio signals currently dominate over macro event pressure.");
    setText("flow-summary", state.analysis.market.narrative);

    const priorityStats = document.getElementById("priority-stats");
    const impactStrip = document.getElementById("impact-strip");
    const eventStack = document.getElementById("event-stack");
    const sectorStack = document.getElementById("market-sector-stack");
    const flowList = document.getElementById("flow-list");

    if (priorityStats) {
        priorityStats.innerHTML = topEvent ? [
            snapshotCard("Impact", formatPercent(topEvent.impact, 1, true), "Estimated effect on the full portfolio."),
            snapshotCard("Exposure", `${Math.round(topEvent.exposure * 100)}%`, "Share of the book touched by the event."),
            snapshotCard("Direction", topEvent.direction.toUpperCase(), "Current event bias."),
            snapshotCard("Severity", topEvent.severity.toUpperCase(), "Relative size of the move."),
        ].join("") : "";
    }

    if (impactStrip) {
        impactStrip.innerHTML = topEvent ? topEvent.affected.map((item) => `
            <div class="impact-chip">
                <strong>${item.ticker}</strong>
                <span>${formatPercent(item.weight, 1)} weight</span>
                <small>${formatPercent(item.impact, 1, true)} event lift</small>
            </div>
        `).join("") : "";
    }

    if (eventStack) {
        eventStack.innerHTML = state.analysis.market.events.map((event) => `
            <div class="event-card">
                <div class="event-topline">
                    <strong>${event.title}</strong>
                    <span class="${toneTextClass(event.impact)}">${formatPercent(event.impact, 1, true)}</span>
                </div>
                <div class="event-meta">
                    <span class="mini-pill">${event.type.toUpperCase()}</span>
                    <span class="mini-pill">${Math.round(event.exposure * 100)}% exposed</span>
                    <span class="mini-pill">${event.severity.toUpperCase()}</span>
                </div>
                <p>${event.summary}</p>
                <small>${event.affectedTickers.join(", ")}</small>
            </div>
        `).join("");
    }

    if (sectorStack) {
        sectorStack.innerHTML = state.analysis.market.sectorExposure.map((row) => sectorBar(row)).join("");
    }

    if (flowList) {
        const maxFlow = Math.max(...state.analysis.market.flows.flatMap((item) => [Math.abs(item.fii), Math.abs(item.dii)]));
        flowList.innerHTML = state.analysis.market.flows.map((item) => `
            <div class="flow-row">
                <div class="flow-topline">
                    <strong>${item.day}</strong>
                    <span class="flow-value ${toneTextClass(item.net / 10000)}">${item.net >= 0 ? "+" : ""}${item.net} Cr net</span>
                </div>
                <div class="flow-bars">
                    <div class="flow-rail">
                        <span>FII</span>
                        <div class="flow-track"><div class="flow-fill fii" style="width:${Math.round((Math.abs(item.fii) / maxFlow) * 100)}%"></div></div>
                        <span>${item.fii >= 0 ? "+" : ""}${item.fii}</span>
                    </div>
                    <div class="flow-rail">
                        <span>DII</span>
                        <div class="flow-track"><div class="flow-fill dii" style="width:${Math.round((Math.abs(item.dii) / maxFlow) * 100)}%"></div></div>
                        <span>+${item.dii}</span>
                    </div>
                </div>
            </div>
        `).join("");
    }
}

function renderActions() {
    const recommendation = state.analysis.recommendation;
    setText("decision-headline", recommendation.action);
    setText("decision-summary", recommendation.summary);
    setText("decision-badge", `${Math.round(recommendation.confidence * 100)}% confidence`);
    applyToneClass(document.getElementById("decision-badge"), recommendation.action === "ACCUMULATE" ? "positive" : recommendation.action === "REDUCE" ? "negative" : "balanced");

    const signalBoard = document.getElementById("signal-board");
    const driverList = document.getElementById("driver-list");
    const addLane = document.getElementById("add-lane");
    const holdLane = document.getElementById("hold-lane");
    const trimLane = document.getElementById("trim-lane");

    if (signalBoard) {
        signalBoard.innerHTML = recommendation.signals.map((signal) => `
            <div class="signal-chip tone-${signal.tone}">
                <strong>${signal.label}</strong>
                <span>${signal.value}</span>
            </div>
        `).join("");
    }

    if (driverList) {
        driverList.innerHTML = recommendation.drivers.map((driver, index) => `
            <div class="driver-card">
                <strong>Driver ${index + 1}</strong>
                <p>${driver}</p>
            </div>
        `).join("");
    }

    if (addLane) {
        addLane.innerHTML = recommendation.additions.map((item) => laneCard(item)).join("");
    }
    if (holdLane) {
        holdLane.innerHTML = recommendation.holds.map((item) => laneCard(item)).join("");
    }
    if (trimLane) {
        trimLane.innerHTML = recommendation.trims.map((item) => laneCard(item)).join("");
    }
}

function renderDeep() {
    const pipeline = document.getElementById("pipeline-list");
    const assumptions = document.getElementById("assumptions-list");
    if (pipeline) {
        pipeline.innerHTML = state.analysis.pipeline.map((item) => `
            <div class="pipeline-step">
                <div class="step-number">${item.step}</div>
                <div>
                    <strong>${item.title}</strong>
                    <p>${item.summary}</p>
                    <small>${item.detail}</small>
                </div>
            </div>
        `).join("");
    }
    if (assumptions) {
        assumptions.innerHTML = state.analysis.assumptions.map((item, index) => `
            <div class="assumption-card">
                <strong>Assumption ${index + 1}</strong>
                <p>${item}</p>
            </div>
        `).join("");
    }
    setText("meta-source", formatDataSource(state.analysis.dataSource));
    setText("meta-time", formatTimestamp(state.analysis.timestamp));
    setText("meta-holdings", `${state.analysis.portfolio.stockCount} names`);
}

function updateStatusPills() {
    const enginePill = document.getElementById("engine-pill");
    const dataPill = document.getElementById("data-pill");
    const clawPill = document.getElementById("claw-pill");
    if (!enginePill || !dataPill) {
        return;
    }

    if (state.engineStatus?.status === "ok") {
        enginePill.textContent = state.engineStatus.warmup?.completed ? "Engine warmed" : "Engine available";
    } else {
        enginePill.textContent = "Engine offline";
    }

    const sourceLabel = state.usesBackend ? formatDataSource(state.analysis.dataSource) : "Local demo";
    dataPill.textContent = sourceLabel;

    if (clawPill) {
        const openclaw = getOpenClawStatus();
        if (openclaw.gateway?.reachable && openclaw.channels?.whatsappConfigured) {
            clawPill.textContent = "OpenClaw + WhatsApp live";
        } else if (openclaw.gateway?.reachable) {
            clawPill.textContent = "OpenClaw live";
        } else if (openclaw.workspace?.configured) {
            clawPill.textContent = "OpenClaw workspace ready";
        } else {
            clawPill.textContent = "OpenClaw setup needed";
        }
    }
}

function openclawPoint(tone, title, detail) {
    return `
        <div class="openclaw-point">
            <span class="point-dot ${tone}"></span>
            <div>
                <strong>${title}</strong>
                <small>${detail}</small>
            </div>
        </div>
    `;
}

function snapshotCard(label, value, detail) {
    return `
        <div class="snapshot-card">
            <span class="metric-label">${label}</span>
            <strong>${value}</strong>
            <small>${detail}</small>
        </div>
    `;
}

function sectorBar(row) {
    return `
        <div class="sector-bar">
            <div class="sector-line">
                <strong>${row.sector}</strong>
                <span class="mono">${formatPercent(row.weight, 1)}</span>
            </div>
            <div class="bar-track"><div class="bar-fill" style="transform:scaleX(${row.weight})"></div></div>
        </div>
    `;
}

function laneCard(item) {
    return `
        <div class="lane-card">
            <div class="lane-topline">
                <strong>${item.ticker}</strong>
                <span class="mono">${Math.round(item.confidence * 100)}%</span>
            </div>
            <p>${item.reason}</p>
        </div>
    `;
}

function sparklineSVG(points, signal) {
    if (!Array.isArray(points) || !points.length) {
        return "";
    }
    const min = Math.min(...points);
    const max = Math.max(...points);
    const range = max - min || 1;
    const coords = points.map((point, index) => {
        const x = (index / (points.length - 1)) * 100;
        const y = 30 - ((point - min) / range) * 26 - 2;
        return `${x},${y}`;
    }).join(" ");
    const color = signal === "buy" ? "#d9ff63" : signal === "sell" ? "#ff7a84" : "#ffcf70";
    return `
        <svg class="sparkline" viewBox="0 0 100 32" preserveAspectRatio="none" aria-hidden="true">
            <polyline fill="none" stroke="${color}" stroke-width="2" points="${coords}"></polyline>
        </svg>
    `;
}

function formatPercent(value, digits = 1, signed = false) {
    const amount = Math.abs(value * 100).toFixed(digits);
    if (!signed) {
        return `${amount}%`;
    }
    return `${value >= 0 ? "+" : "-"}${amount}%`;
}

function formatCompactMoney(value) {
    const absolute = Math.abs(value);
    if (absolute >= 10000000) {
        return `Rs ${(absolute / 10000000).toFixed(2)}Cr`;
    }
    if (absolute >= 100000) {
        return `Rs ${(absolute / 100000).toFixed(1)}L`;
    }
    return `Rs ${Math.round(absolute).toLocaleString("en-IN")}`;
}

function formatTimestamp(value) {
    if (!value) {
        return fallbackTimestamp();
    }
    if (typeof value === "string" && value.includes("T")) {
        const parsed = new Date(value);
        if (!Number.isNaN(parsed.getTime())) {
            return new Intl.DateTimeFormat("en-IN", {
                dateStyle: "medium",
                timeStyle: "short",
                timeZone: "Asia/Kolkata",
            }).format(parsed);
        }
    }
    return String(value);
}

function formatDataSource(source) {
    if (source === "live") return "Live market data";
    if (source === "mixed") return "Mixed live and fallback";
    if (source === "simulated") return "Simulated market data";
    return "Local demo model";
}

function toneTextClass(value) {
    if (value > 0) return "positive-text";
    if (value < 0) return "negative-text";
    return "balanced-text";
}

function applyToneClass(element, tone) {
    if (!element) {
        return;
    }
    element.classList.remove("tone-positive", "tone-balanced", "tone-negative");
    element.classList.add(`tone-${tone}`);
}

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

let toastTimer = null;
function toast(message, tone = "balanced") {
    const element = document.getElementById("toast");
    if (!element) {
        return;
    }
    element.textContent = message;
    element.className = `toast show tone-${tone}`;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        element.className = "toast";
    }, 2600);
}
