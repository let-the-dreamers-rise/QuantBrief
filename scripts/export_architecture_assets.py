from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
PNG_PATH = DOCS_DIR / "system-architecture.png"
PDF_PATH = DOCS_DIR / "system-architecture.pdf"

WIDTH = 1800
HEIGHT = 1120
BACKGROUND = "#07131e"
PANEL = "#0f2232"
PANEL_ALT = "#102d3d"
PANEL_SOFT = "#14354a"
STROKE = "#3ea4d9"
TEXT = "#ecf7ff"
MUTED = "#94b8cc"
ACCENT = "#7bf0c8"
WARNING = "#f4d35e"
WHATSAPP = "#4bd37b"
CLI = "#7bb8ff"


def load_font(size: int, bold: bool = False):
    candidates = [
        ("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        ("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


TITLE_FONT = load_font(50, bold=True)
SUBTITLE_FONT = load_font(24)
BOX_TITLE_FONT = load_font(27, bold=True)
BOX_BODY_FONT = load_font(20)
FOOTER_FONT = load_font(19)


def draw_round_box(draw: ImageDraw.ImageDraw, box, title, body_lines, *, fill, outline, title_fill=TEXT):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=24, fill=fill, outline=outline, width=3)
    draw.text((x1 + 22, y1 + 18), title, font=BOX_TITLE_FONT, fill=title_fill)
    y = y1 + 64
    for line in body_lines:
        draw.text((x1 + 22, y), line, font=BOX_BODY_FONT, fill=MUTED if line.startswith("  ") else TEXT)
        y += 28


def draw_arrow(draw: ImageDraw.ImageDraw, start, end, *, fill=STROKE, width=6, label=None, label_offset=(0, 0)):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=fill, width=width)
    head = 14
    if x1 == x2:
        direction = 1 if y2 >= y1 else -1
        draw.polygon(
            [(x2, y2), (x2 - head, y2 - head * direction), (x2 + head, y2 - head * direction)],
            fill=fill,
        )
    else:
        direction = 1 if x2 >= x1 else -1
        draw.polygon(
            [(x2, y2), (x2 - head * direction, y2 - head), (x2 - head * direction, y2 + head)],
            fill=fill,
        )
    if label:
        mid_x = (x1 + x2) / 2 + label_offset[0]
        mid_y = (y1 + y2) / 2 + label_offset[1]
        bbox = draw.textbbox((mid_x, mid_y), label, font=BOX_BODY_FONT)
        padded = (bbox[0] - 10, bbox[1] - 6, bbox[2] + 10, bbox[3] + 6)
        draw.rounded_rectangle(padded, radius=12, fill="#0a1b28", outline=fill, width=2)
        draw.text((mid_x, mid_y), label, font=BOX_BODY_FONT, fill=TEXT, anchor="la")


def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    # Background accents
    draw.ellipse((-220, -120, 620, 620), fill="#0c1e2b")
    draw.ellipse((1220, 700, 1960, 1420), fill="#0c1e2b")
    draw.rounded_rectangle((42, 42, WIDTH - 42, HEIGHT - 42), radius=34, outline="#113149", width=3)

    draw.text((84, 72), "QuantBrief v3 System Architecture", font=TITLE_FONT, fill=TEXT)
    draw.text(
        (86, 136),
        "OpenClaw-first portfolio intelligence across browser, CLI, and WhatsApp self-chat",
        font=SUBTITLE_FONT,
        fill=MUTED,
    )

    user_box = (88, 248, 410, 424)
    ui_box = (500, 214, 910, 412)
    wa_box = (500, 462, 910, 660)
    cli_box = (500, 710, 910, 908)
    api_box = (990, 214, 1360, 412)
    status_box = (990, 462, 1360, 660)
    gateway_box = (990, 710, 1360, 908)
    engine_box = (1435, 214, 1760, 432)
    store_box = (1435, 494, 1760, 684)
    mcp_box = (1435, 774, 1760, 964)

    draw_round_box(
        draw,
        user_box,
        "Investor / Demo User",
        [
            "Single owner of the linked WhatsApp account",
            "Edits holdings, runs analysis, asks questions",
        ],
        fill=PANEL,
        outline=ACCENT,
        title_fill=ACCENT,
    )
    draw_round_box(
        draw,
        ui_box,
        "Web UI",
        [
            "index.html / index.css / app.js",
            "4-tab decision cockpit",
            "Portfolio editor and OpenClaw status",
        ],
        fill=PANEL_ALT,
        outline=CLI,
        title_fill=CLI,
    )
    draw_round_box(
        draw,
        wa_box,
        "WhatsApp Self-Chat",
        [
            "Linked personal account",
            "Allowlist: +918097251640",
            "Self-chat only, groups disabled",
        ],
        fill=PANEL_ALT,
        outline=WHATSAPP,
        title_fill=WHATSAPP,
    )
    draw_round_box(
        draw,
        cli_box,
        "OpenClaw Local Agent",
        [
            "openclaw --profile quantbrief agent --local",
            "Reliable demo path if mobile pairing is flaky",
        ],
        fill=PANEL_ALT,
        outline=CLI,
        title_fill=CLI,
    )
    draw_round_box(
        draw,
        api_box,
        "FastAPI Backend",
        [
            "backend.py",
            "Serves UI and portfolio analysis APIs",
            "Reports health and OpenClaw status",
        ],
        fill=PANEL_SOFT,
        outline=STROKE,
    )
    draw_round_box(
        draw,
        status_box,
        "OpenClaw Status Layer",
        [
            "openclaw_status.py",
            "Reads gateway, channel, and workspace health",
        ],
        fill=PANEL_SOFT,
        outline=WARNING,
        title_fill=WARNING,
    )
    draw_round_box(
        draw,
        gateway_box,
        "OpenClaw Gateway",
        [
            "Profile: quantbrief",
            "Dedicated port and isolated session state",
            "Routes CLI and WhatsApp requests to MCP tools",
        ],
        fill=PANEL_SOFT,
        outline=ACCENT,
        title_fill=ACCENT,
    )
    draw_round_box(
        draw,
        engine_box,
        "Shared Analysis Engine",
        [
            "analysis_engine.py",
            "Signals, events, scenarios",
            "Recommendations and scoring",
            "Live data + fallback models",
        ],
        fill="#153749",
        outline=ACCENT,
        title_fill=ACCENT,
    )
    draw_round_box(
        draw,
        store_box,
        "SQLite Portfolio Store",
        [
            "portfolio_store.py",
            "Persists the active portfolio state",
        ],
        fill="#153749",
        outline=WARNING,
        title_fill=WARNING,
    )
    draw_round_box(
        draw,
        mcp_box,
        "QuantBrief MCP",
        [
            "mcp_server.py",
            "Portfolio analysis, recommendation,",
            "lookup, and risk tools",
        ],
        fill="#153749",
        outline=CLI,
        title_fill=CLI,
    )

    draw_arrow(draw, (410, 338), (500, 313), fill=CLI, label="browser flow", label_offset=(-22, -34))
    draw_arrow(draw, (410, 338), (500, 561), fill=WHATSAPP, label="mobile chat", label_offset=(-16, -24))
    draw_arrow(draw, (410, 338), (500, 809), fill=CLI, label="local CLI", label_offset=(-16, -22))

    draw_arrow(draw, (910, 313), (990, 313), fill=STROKE, label="/api/*", label_offset=(-8, -34))
    draw_arrow(draw, (910, 561), (990, 809), fill=WHATSAPP, label="messages", label_offset=(-10, -24))
    draw_arrow(draw, (910, 809), (990, 809), fill=CLI, label="agent calls", label_offset=(-4, -34))

    draw_arrow(draw, (1360, 323), (1435, 323), fill=ACCENT, label="analysis", label_offset=(-8, -34))
    draw_arrow(draw, (1175, 412), (1175, 462), fill=WARNING, label="status", label_offset=(16, -8))
    draw_arrow(draw, (1175, 660), (1175, 710), fill=WARNING, label="probe", label_offset=(16, -8))
    draw_arrow(draw, (1360, 809), (1435, 869), fill=CLI, label="MCP", label_offset=(-10, -30))
    draw_arrow(draw, (1598, 869), (1598, 432), fill=ACCENT, label="shared core", label_offset=(18, -8))
    draw_arrow(draw, (1360, 323), (1435, 589), fill=WARNING, label="portfolio state", label_offset=(-10, -18))

    footer = (
        "Submission note: WhatsApp is intentionally restricted to the owner's own number via allowlist + self-chat mode."
    )
    draw.text((84, HEIGHT - 88), footer, font=FOOTER_FONT, fill=MUTED)

    image.save(PNG_PATH)
    image.save(PDF_PATH, "PDF", resolution=200.0)
    print(f"Exported {PNG_PATH}")
    print(f"Exported {PDF_PATH}")


if __name__ == "__main__":
    main()
