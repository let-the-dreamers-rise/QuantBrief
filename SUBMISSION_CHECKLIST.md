# QuantBrief Submission Checklist

## Required Deliverables

### 1. System Architecture Diagram

Primary files:

- [docs/system-architecture.png](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/docs/system-architecture.png)
- [docs/system-architecture.pdf](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/docs/system-architecture.pdf)
- [docs/system-architecture.mmd](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/docs/system-architecture.mmd)

What it shows:

- User touchpoints: web app, OpenClaw CLI, WhatsApp self-chat
- FastAPI backend and API routes
- Shared analysis engine
- SQLite portfolio persistence
- OpenClaw gateway and MCP server
- Live-data / fallback-data path

### 2. Functional Prototype

Prototype surfaces already available:

- Web app at `http://127.0.0.1:8000`
- OpenClaw local agent via `openclaw --profile quantbrief agent --local`
- WhatsApp linked through the QuantBrief OpenClaw profile

What to demonstrate:

- Portfolio edit and analysis
- Recommendation + confidence + event impact
- OpenClaw status cockpit
- Local agent question flow
- Optional WhatsApp self-chat flow

### 3. Public GitHub Repository

Public repo:

- [QuantBrief GitHub Repository](https://github.com/let-the-dreamers-rise/QuantBrief)

Minimum repo quality bar:

- Clear README
- Working run instructions
- Project structure explained
- Functional prototype committed
- No broken placeholder setup steps

### 4. 2-3 Minute Demo Video

Use these files:

- [DEMO_SCRIPT.md](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/DEMO_SCRIPT.md)
- [PPT_OUTLINE.md](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/PPT_OUTLINE.md)

Recommended video sequence:

1. Open the web app and show the 4-tab interface.
2. Edit the portfolio and run analysis.
3. Show recommendation, confidence, and event impact.
4. Show OpenClaw cockpit and linked WhatsApp / local agent story.
5. Run one local OpenClaw prompt.
6. Close with why QuantBrief is decision-first, not dashboard-first.

### 5. README / Documentation

Core documentation files:

- [README.md](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/README.md)
- [DEMO_SCRIPT.md](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/DEMO_SCRIPT.md)
- [PPT_OUTLINE.md](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/PPT_OUTLINE.md)
- [SUBMISSION_CHECKLIST.md](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/SUBMISSION_CHECKLIST.md)

## Submission Notes

### WhatsApp Safety

QuantBrief is linked to your personal WhatsApp, but it is locked down:

- `dmPolicy: allowlist`
- `allowFrom: ["+918097251640"]`
- `selfChatMode: true`
- `groupPolicy: disabled`

That means it is restricted to your own WhatsApp identity and is not intended to respond broadly to contacts or groups.

### Best Demo Path

Most reliable demo stack:

1. Web UI on `http://127.0.0.1:8000`
2. OpenClaw local agent CLI
3. Optional WhatsApp self-chat if needed

### Recommended Submission Zip Contents

- Source code
- README
- Architecture diagram PNG/PDF
- Demo script
- PPT outline
- Optional screenshots used in slides
