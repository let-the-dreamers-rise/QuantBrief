# QuantBrief PPT Outline

## Slide 1: Title

Title:

`QuantBrief v3: An OpenClaw-First Portfolio Decision Engine`

What to show:

- Product name
- Tagline
- Your name / team / submission info
- One polished product screenshot

What to say:

"QuantBrief is a decision-first investing assistant for retail portfolios, built as both a web product and an OpenClaw-native agent."

## Slide 2: Problem

Title:

`The Problem With Retail Portfolio Tools`

What to show:

- 3-4 short pain points
- Optional icons or simple infographic

Content:

- Too many passive charts, not enough decision guidance
- Market news is noisy and generic
- Users struggle to connect events to their own portfolio
- Chat assistants often lack structured portfolio logic

What to say:

"Investors do not just need data. They need a clear answer to what matters now and what action makes sense."

## Slide 3: Solution

Title:

`Our Solution: QuantBrief`

What to show:

- One-line product definition
- 3 core pillars

Content:

- Portfolio-aware analysis
- Event-driven recommendation engine
- Same intelligence layer available via UI and agent chat

What to say:

"QuantBrief turns a portfolio into an actionable brief: recommendation, confidence, event impact, and downside scenarios."

## Slide 4: Target User

Title:

`Who It Is For`

What to show:

- Persona card for an Indian retail investor
- Short use cases

Content:

- Retail investors managing Indian equities
- Users who want fast decision support, not research overload
- Demo-friendly for advisors, student showcases, and product judges

## Slide 5: Product Experience

Title:

`Functional Prototype`

What to show:

- Screenshot collage of the 4 tabs

Content:

- My Portfolio
- Market Pulse
- What To Do
- Deep Analysis

What to say:

"The prototype is functional, not just conceptual. It runs live as a web app and exposes portfolio intelligence across multiple surfaces."

## Slide 6: Core Features

Title:

`Key Features`

What to show:

- Clean feature grid

Content:

- Portfolio editor and persistence
- Recommendation engine with confidence
- Market event ranking
- Scenario analysis
- Correlation and risk views
- OpenClaw cockpit and chat integration

## Slide 7: System Architecture

Title:

`System Architecture`

What to show:

- [docs/system-architecture.png](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/docs/system-architecture.png)

Talk track:

"The system centers on one shared analysis engine. The web app, FastAPI API, and OpenClaw MCP server all use the same core logic so the answers stay consistent across UI and chat."

## Slide 8: OpenClaw Integration

Title:

`Why OpenClaw Matters`

What to show:

- Flow from user -> OpenClaw -> gateway -> MCP -> analysis engine

Content:

- Local CLI agent
- WhatsApp self-chat entry point
- MCP tools for portfolio analysis, stock lookup, and recommendations
- OpenClaw-first experience instead of a dashboard-only product

## Slide 9: Safety and Control

Title:

`Safety, Scope, and Personal Account Controls`

What to show:

- 3 short policy bullets

Content:

- WhatsApp is linked to a personal account
- Locked to own number via allowlist
- Group replies disabled
- Self-chat mode enabled

What to say:

"We intentionally restricted the linked WhatsApp surface to the owner's own number so the bot cannot broadly interact with contacts or groups."

## Slide 10: Demo Walkthrough

Title:

`2-3 Minute Demo Story`

What to show:

- 5-step numbered flow

Content:

1. Open web app
2. Edit portfolio
3. Run analysis
4. Show recommendation and event impact
5. Ask the OpenClaw agent a portfolio question

Reference:

- [DEMO_SCRIPT.md](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/DEMO_SCRIPT.md)

## Slide 11: Repository and Deliverables

Title:

`Submission Assets`

What to show:

- Repo URL
- Checklist of assets

Content:

- Public GitHub repository
- Functional prototype
- Architecture diagram
- Demo video
- README and documentation

Reference:

- [SUBMISSION_CHECKLIST.md](C:/Users/ASHWIN%20GOYAL/Downloads/QuantBrief-v3/SUBMISSION_CHECKLIST.md)

## Slide 12: Roadmap

Title:

`What Comes Next`

What to show:

- Short roadmap timeline

Content:

- Public hosted deployment
- Multi-user accounts
- More robust market-data/news ingestion
- Better model layer and richer recommendation logic
- Stronger automated testing

## Slide 13: Closing

Title:

`Closing`

What to show:

- Strong closing line and one hero screenshot

Closing line:

"QuantBrief turns portfolio analysis from passive information into an actionable agent experience."

## Design Notes For The Deck

- Keep the deck to 10-13 slides.
- Use 1 strong screenshot per slide instead of crowded collages.
- Use the architecture diagram only once, on its own slide.
- Keep text minimal and speak the rest.
- For a 2-3 minute presentation, spend the most time on slides 5, 7, 8, and 10.
