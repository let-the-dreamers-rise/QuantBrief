# QuantBrief Demo Script

## One-Line Setup

QuantBrief is an OpenClaw-first investing copilot that turns a noisy retail portfolio into a ranked action brief: what matters, what to do, and why.

## 30-Second Opening

"Most retail investors don't need more charts. They need a fast, trustworthy decision layer. QuantBrief takes a portfolio, checks quant signals, market events, and risk scenarios, then turns that into a clear recommendation: accumulate, hold, or reduce."

## 3-Minute Demo Flow

### 1. Show the product shell

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

Say:

"This is QuantBrief's decision cockpit. The interface is organized around four jobs: portfolio state, market pulse, recommended action, and deeper analysis."

### 2. Show the portfolio tab

Say:

"Here I can add or remove holdings, set portfolio size, and run analysis against either fallback or live data. The point is not just performance stats. The point is decision support."

Click:

- Add or edit 2-3 recognizable holdings
- Run analysis

### 3. Explain the recommendation

Say:

"QuantBrief does not stop at CAGR and volatility. It translates the portfolio into an action recommendation with confidence, event impact, and scenario framing. That makes it usable for an actual investor conversation."

Point to:

- Recommendation card
- Confidence gauge
- Event ranking
- Risk scenarios

### 4. Show the OpenClaw angle

Say:

"The real differentiator is that QuantBrief is not just a dashboard. It's an agent. The same analysis engine is exposed through OpenClaw, so the user can ask portfolio questions in chat instead of navigating a screen."

Point to:

- OpenClaw cockpit
- Gateway status
- WhatsApp / Telegram / Local Agent surfaces

### 5. Show the CLI agent prompt

Run:

```powershell
Set-Location "C:\Users\ASHWIN GOYAL\Downloads\QuantBrief-v3"
$env:PYTHONIOENCODING="utf-8"
openclaw --profile quantbrief agent --local --session-id qb --message "How does my portfolio look?"
```

Say:

"The same portfolio logic powers the chat experience. So whether the user is in the web app or messaging the agent, the answer stays consistent."

## 60-Second Investor Version

"QuantBrief is an OpenClaw-native investing assistant for retail portfolios. Instead of giving users raw market noise, it gives them a ranked decision brief with recommendation, confidence, event impact, and downside scenarios. It works as a visual web product, but it also works as a conversational agent through OpenClaw, which means the interface can move from browser to chat without rebuilding the intelligence layer."

## Live Prompts That Work Well

- `How does my portfolio look right now?`
- `Should I buy HDFCBANK?`
- `What is the biggest risk in my portfolio?`
- `Which event is driving the recommendation?`
- `Show me worst, base, and best case.`

## Fallback Demo Path

If WhatsApp is flaky, say:

"The OpenClaw integration is already live through the local agent and gateway. WhatsApp is the mobile surface we are finishing, but the agent workflow itself is already working end to end."

Then show:

- Local agent CLI
- OpenClaw cockpit in the web app
- `/api/openclaw/status`

## Closing Line

"QuantBrief turns portfolio analysis from a passive dashboard into an actionable agent experience. The value is not just insight. The value is clarity at the moment of decision."
