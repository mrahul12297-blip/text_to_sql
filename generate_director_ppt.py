#!/usr/bin/env python3
"""Classic, short director deck: overview, architecture, flow, routing, controls."""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

BLUE = RGBColor(31, 78, 121)
BLUE_DARK = RGBColor(15, 47, 82)
BLUE_MID = RGBColor(47, 84, 150)
BLUE_LIGHT = RGBColor(217, 226, 243)
GOLD = RGBColor(191, 144, 0)
GREEN = RGBColor(84, 130, 53)
GREEN_BG = RGBColor(226, 239, 218)
AMBER = RGBColor(197, 90, 17)
AMBER_BG = RGBColor(252, 228, 214)
RED = RGBColor(192, 80, 77)
RED_BG = RGBColor(252, 228, 214)
GRAY = RGBColor(89, 89, 89)
GRAY_DARK = RGBColor(51, 51, 51)
GRAY_LINE = RGBColor(191, 191, 191)
WHITE = RGBColor(255, 255, 255)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
TOTAL = 5


def run(p, text, size=14, bold=False, color=GRAY_DARK, font="Calibri"):
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = font


def textbox(slide, left, top, width, height, text, size=14, bold=False, color=GRAY_DARK, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run(p, text, size, bold, color)
    return box


def fill(shape, color, line=None):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(0.75)


def rect(slide, left, top, width, height, bg, text="", size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    fill(shape, bg, line)
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    try:
        tf._txBody.bodyPr.set("anchor", "ctr")
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.alignment = align
    run(p, text, size, bold, color)
    return shape


def diamond(slide, left, top, width, height, bg, text, size=11, color=WHITE):
    shape = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, left, top, width, height)
    fill(shape, bg)
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.08)
    tf.margin_right = Inches(0.08)
    try:
        tf._txBody.bodyPr.set("anchor", "ctr")
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run(p, text, size, True, color)
    return shape


def header(slide, title, subtitle=None):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_W, Inches(0.9))
    fill(bar, BLUE)
    gold = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0.9), SLIDE_W, Inches(0.05))
    fill(gold, GOLD)
    textbox(slide, Inches(0.45), Inches(0.16), Inches(12.4), Inches(0.38), title, 24, True, WHITE)
    if subtitle:
        textbox(slide, Inches(0.45), Inches(0.52), Inches(12.4), Inches(0.3), subtitle, 12, False, RGBColor(210, 220, 235))


def footer(slide, page):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(7.18), Inches(12.5), Inches(0.015))
    fill(line, GRAY_LINE)
    textbox(slide, Inches(0.4), Inches(7.22), Inches(9), Inches(0.22),
            "Text-to-SQL Agent", 10, False, GRAY)
    textbox(slide, Inches(11.4), Inches(7.22), Inches(1.5), Inches(0.22),
            f"{page} / {TOTAL}", 10, False, GRAY, PP_ALIGN.RIGHT)


def arrow_right(slide, left, top):
    textbox(slide, left, top, Inches(0.28), Inches(0.35), "→", 16, True, GOLD, PP_ALIGN.CENTER)


def arrow_down(slide, left, top):
    textbox(slide, left, top, Inches(0.35), Inches(0.28), "↓", 16, True, GOLD, PP_ALIGN.CENTER)


def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    # ------------------------------------------------------------------
    # 1. Overview + tech stack
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    header(s, "Overview and technology stack", "A working Text-to-SQL agent for an e-commerce SQLite database.")
    footer(s, 1)

    rect(s, Inches(0.4), Inches(1.2), Inches(12.55), Inches(1.55), BLUE_LIGHT, line=BLUE)
    textbox(s, Inches(0.6), Inches(1.35), Inches(12.15), Inches(1.25),
            "A user asks a question in English. LangGraph orchestrates an OpenAI model to write a "
            "read-only SQL query, validates it, runs it on SQLite, and returns a short answer.\n\n"
            "Python owns security, routing, and execution. The model only writes SQL and the final answer.",
            16, False, GRAY_DARK)

    textbox(s, Inches(0.4), Inches(2.95), Inches(12), Inches(0.32), "Technology stack", 16, True, BLUE)

    stacks = [
        ("LangGraph", "Agent orchestration\nand routing"),
        ("OpenAI LLM", "SQL generation\nand answers"),
        ("LangChain", "Model client\n(langchain-openai)"),
        ("Streamlit", "Web user\ninterface"),
        ("SQLite", "E-commerce\ndatabase"),
        ("Python", "dotenv, pandas\nCLI entry point"),
    ]
    for i, (title, body) in enumerate(stacks):
        x = 0.4 + i * 2.15
        rect(s, Inches(x), Inches(3.4), Inches(2.05), Inches(0.42), BLUE, title, 14, True, WHITE)
        rect(s, Inches(x), Inches(3.82), Inches(2.05), Inches(1.15), WHITE, body, 13, False, GRAY_DARK, line=GRAY_LINE)

    textbox(s, Inches(0.4), Inches(5.2), Inches(12), Inches(0.32), "Database tables", 16, True, BLUE)
    tables = ["customers", "products", "orders", "order_items", "payment", "reviews", "shipments", "suppliers"]
    for i, name in enumerate(tables):
        x = 0.4 + (i % 8) * 1.6
        rect(s, Inches(x), Inches(5.6), Inches(1.5), Inches(0.45), WHITE, name, 12, False, BLUE, line=BLUE)

    textbox(s, Inches(0.4), Inches(6.25), Inches(12.5), Inches(0.65),
            "Interfaces: Streamlit UI (app/ui.py) and CLI (python -m app.main).\n"
            "Setup: CSV files in data/ are loaded into ecommerce.db by setup_database.py.",
            13, False, GRAY)

    # ------------------------------------------------------------------
    # 2. Full architecture
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    header(s, "Full architecture", "Three layers. The model proposes. The graph decides. The database only runs validated SELECT.")
    footer(s, 2)

    rect(s, Inches(4.9), Inches(1.2), Inches(3.5), Inches(0.5), BLUE, "User", 16, True, WHITE)
    arrow_down(s, Inches(6.45), Inches(1.7))

    rect(s, Inches(2.4), Inches(2.0), Inches(8.5), Inches(0.7), BLUE_MID, "Presentation     |     Streamlit UI     ·     CLI", 15, True, WHITE)
    arrow_down(s, Inches(6.45), Inches(2.7))

    rect(s, Inches(1.4), Inches(3.0), Inches(10.5), Inches(1.85), BLUE_DARK)
    textbox(s, Inches(1.55), Inches(3.08), Inches(10.2), Inches(0.28), "LangGraph agent", 13, True, GOLD)
    nodes = ["Guardrail", "Schema", "Generate SQL", "Validate", "Execute", "Answer"]
    for i, name in enumerate(nodes):
        x = 1.6 + i * 1.7
        rect(s, Inches(x), Inches(3.45), Inches(1.55), Inches(0.55), BLUE_MID, name, 11, True, WHITE)
    textbox(s, Inches(1.55), Inches(4.15), Inches(10.2), Inches(0.55),
            "Shared state:  question   ·   schema   ·   sql   ·   result   ·   answer   ·   error   ·   retry_count\n"
            "Fix SQL is off the happy path and returns to Validate (maximum 3 times).",
            12, False, RGBColor(220, 230, 245))

    arrow_down(s, Inches(3.85), Inches(4.88))
    arrow_down(s, Inches(8.85), Inches(4.88))

    rect(s, Inches(1.4), Inches(5.2), Inches(5.2), Inches(1.65), WHITE, line=BLUE)
    rect(s, Inches(1.4), Inches(5.2), Inches(5.2), Inches(0.38), BLUE, "OpenAI LLM", 13, True, WHITE)
    textbox(s, Inches(1.55), Inches(5.68), Inches(4.9), Inches(1.05),
            "Classify question\nWrite SELECT\nRewrite SQL after a failure\nTurn rows into an English answer",
            13, False, GRAY_DARK)

    rect(s, Inches(6.9), Inches(5.2), Inches(5.0), Inches(1.65), WHITE, line=BLUE)
    rect(s, Inches(6.9), Inches(5.2), Inches(5.0), Inches(0.38), BLUE, "SQLite  ·  ecommerce.db", 13, True, WHITE)
    textbox(s, Inches(7.05), Inches(5.68), Inches(4.7), Inches(1.05),
            "get_schema() — tables and columns\nexecute_query() — run validated SELECT\nNo writes from the application",
            13, False, GRAY_DARK)

    # ------------------------------------------------------------------
    # 3. Flow + conditional routing
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    header(s, "Flow and conditional routing", "Happy path is a straight line. Three routers branch only when something is off-topic, invalid, or broken.")
    footer(s, 3)

    textbox(s, Inches(0.4), Inches(1.15), Inches(12), Inches(0.28), "Happy path", 14, True, BLUE)
    steps = ["START", "Guardrail", "Schema", "Generate SQL", "Validate", "Execute", "Answer", "END"]
    for i, name in enumerate(steps):
        x = 0.35 + i * 1.62
        bg = GOLD if name in ("START", "END") else BLUE
        fg = BLUE if name in ("START", "END") else WHITE
        rect(s, Inches(x), Inches(1.5), Inches(1.45), Inches(0.5), bg, name, 11, True, fg)
        if i < 7:
            arrow_right(s, Inches(x + 1.4), Inches(1.55))

    # Router 1
    rect(s, Inches(0.35), Inches(2.25), Inches(4.15), Inches(4.55), WHITE, line=GRAY_LINE)
    rect(s, Inches(0.35), Inches(2.25), Inches(4.15), Inches(0.4), BLUE, "Router 1  ·  after Guardrail", 13, True, WHITE)
    diamond(s, Inches(1.25), Inches(2.85), Inches(2.35), Inches(1.15), BLUE, "Related to\nthe database?", 11)
    rect(s, Inches(0.55), Inches(4.25), Inches(3.75), Inches(0.55), GREEN, "Yes  →  Get Schema", 13, True, WHITE)
    rect(s, Inches(0.55), Inches(5.0), Inches(3.75), Inches(0.55), RED, "No  →  Answer and stop", 13, True, WHITE)
    textbox(s, Inches(0.55), Inches(5.7), Inches(3.75), Inches(0.85),
            "Off-topic questions never reach\nthe database. No SQL is generated.",
            12, False, GRAY)

    # Router 2
    rect(s, Inches(4.6), Inches(2.25), Inches(4.15), Inches(4.55), WHITE, line=GRAY_LINE)
    rect(s, Inches(4.6), Inches(2.25), Inches(4.15), Inches(0.4), AMBER, "Router 2  ·  after Validate", 13, True, WHITE)
    diamond(s, Inches(5.5), Inches(2.8), Inches(2.35), Inches(1.1), AMBER, "SQL valid\nand safe?", 11)
    rect(s, Inches(4.8), Inches(4.1), Inches(3.75), Inches(0.48), GREEN, "Yes  →  Execute SQL", 12, True, WHITE)
    rect(s, Inches(4.8), Inches(4.68), Inches(3.75), Inches(0.48), AMBER, "No + retries left  →  Fix SQL", 12, True, WHITE)
    rect(s, Inches(4.8), Inches(5.26), Inches(3.75), Inches(0.48), RED, "No + 3 failures  →  Answer", 12, True, WHITE)
    textbox(s, Inches(4.8), Inches(5.85), Inches(3.75), Inches(0.75),
            "Checks: SELECT only, blocked words,\nreal table, single statement.",
            12, False, GRAY)

    # Router 3
    rect(s, Inches(8.85), Inches(2.25), Inches(4.15), Inches(4.55), WHITE, line=GRAY_LINE)
    rect(s, Inches(8.85), Inches(2.25), Inches(4.15), Inches(0.4), RED, "Router 3  ·  after Execute", 13, True, WHITE)
    diamond(s, Inches(9.75), Inches(2.8), Inches(2.35), Inches(1.1), RED, "Query ran\nwithout error?", 11)
    rect(s, Inches(9.05), Inches(4.1), Inches(3.75), Inches(0.48), GREEN, "Yes  →  Generate Answer", 12, True, WHITE)
    rect(s, Inches(9.05), Inches(4.68), Inches(3.75), Inches(0.48), AMBER, "Error + retries left  →  Fix SQL", 12, True, WHITE)
    rect(s, Inches(9.05), Inches(5.26), Inches(3.75), Inches(0.48), RED, "3 failures  →  Answer", 12, True, WHITE)
    textbox(s, Inches(9.05), Inches(5.85), Inches(3.75), Inches(0.75),
            "SQLite errors go back through\nFix SQL, then Validate again.",
            12, False, GRAY)

    # ------------------------------------------------------------------
    # 4. Error architecture
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    header(s, "If an error comes", "Every failure has a path. The graph does not invent an answer.")
    footer(s, 4)

    # Top: error sources
    textbox(s, Inches(0.4), Inches(1.15), Inches(12), Inches(0.28), "Where the error is raised", 14, True, BLUE)
    sources = [
        (0.4, "Guardrail\nempty / off-topic", RED),
        (3.55, "Validate\nunsafe or invalid SQL", AMBER),
        (6.7, "Execute\nSQLite runtime error", AMBER),
        (9.85, "Answer\nzero rows", BLUE),
    ]
    for x, label, color in sources:
        rect(s, Inches(x), Inches(1.5), Inches(2.95), Inches(0.7), color, label, 13, True, WHITE)

    for x in (1.7, 4.85, 8.0, 11.15):
        arrow_down(s, Inches(x), Inches(2.22))

    # Middle: decision
    rect(s, Inches(3.4), Inches(2.5), Inches(6.5), Inches(0.7), BLUE_DARK, "Does retry_count allow another fix?   (maximum 3)", 15, True, WHITE)
    arrow_down(s, Inches(4.55), Inches(3.22))
    arrow_down(s, Inches(8.15), Inches(3.22))

    # Two branches
    rect(s, Inches(0.4), Inches(3.5), Inches(6.15), Inches(3.25), WHITE, line=AMBER)
    rect(s, Inches(0.4), Inches(3.5), Inches(6.15), Inches(0.4), AMBER, "Yes  —  retries left", 14, True, WHITE)
    steps = [
        (0.6, 4.05, "1. Fix SQL", "LLM rewrites the query using the error, the schema, and the question."),
        (0.6, 5.0, "2. Validate again", "The same security checks run on the new SQL."),
        (0.6, 5.95, "3. Execute if valid", "If it still fails, retry_count increases and the loop repeats."),
    ]
    for x, y, t, b in steps:
        rect(s, Inches(x), Inches(y), Inches(1.7), Inches(0.7), AMBER_BG, t, 12, True, AMBER, line=AMBER)
        textbox(s, Inches(x + 1.85), Inches(y), Inches(4.05), Inches(0.75), b, 12, False, GRAY_DARK)

    rect(s, Inches(6.8), Inches(3.5), Inches(6.15), Inches(3.25), WHITE, line=RED)
    rect(s, Inches(6.8), Inches(3.5), Inches(6.15), Inches(0.4), RED, "No  —  stop and answer", 14, True, WHITE)
    outcomes = [
        (7.0, 4.1, "Guardrail failure", "Return: this question is not related to the database. No SQL."),
        (7.0, 4.85, "Validation / execute exhausted", "Return the last error text. Do not invent SQL or numbers."),
        (7.0, 5.6, "Valid SQL, empty result", "Return: no matching data was found. The LLM is not called."),
        (7.0, 6.25, "LLM / API failure", "The request fails in the UI. Nothing is executed."),
    ]
    for x, y, t, b in outcomes:
        rect(s, Inches(x), Inches(y), Inches(2.3), Inches(0.55), RED_BG, t, 11, True, RED, line=RED)
        textbox(s, Inches(x + 2.4), Inches(y), Inches(3.35), Inches(0.6), b, 12, False, GRAY_DARK)

    # ------------------------------------------------------------------
    # 5. Additional controls
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    header(s, "Additional controls that can be added", "These are not in the project today. They harden the same architecture for a wider rollout.")
    footer(s, 5)

    controls = [
        ("Read-only DB user", "The database account can only SELECT. Writes fail even if SQL slips through."),
        ("Table-level permissions", "Each role may query only an allow-listed set of tables."),
        ("Column-level permissions", "Hide or block columns a user is not allowed to see."),
        ("SQL AST parser", "Parse the query as a tree. Stop keyword-matching bypasses."),
        ("Query timeout", "Kill queries that run too long and protect the database."),
        ("Maximum query complexity", "Block heavy joins, Cartesian products, and deep subqueries."),
        ("Audit logs", "Record who asked what, the SQL, the outcome, and the time."),
        ("Monitoring", "Track failures, latency, retry count, and blocked queries."),
        ("Rate limiting", "Cap questions per user so the model and database are not flooded."),
        ("PII masking", "Mask email, phone, and card values before the UI shows them."),
        ("Prompt-injection defenses", "Ignore “ignore previous rules” and attempts to dump the schema."),
        ("Sensitive table restrictions", "Never expose payroll, credentials, or other restricted tables."),
    ]
    for i, (title, body) in enumerate(controls):
        col = i % 3
        row = i // 3
        x = 0.4 + col * 4.3
        y = 1.2 + row * 1.4
        rect(s, Inches(x), Inches(y), Inches(4.15), Inches(1.25), WHITE, line=GRAY_LINE)
        rect(s, Inches(x), Inches(y), Inches(0.1), Inches(1.25), BLUE)
        textbox(s, Inches(x + 0.25), Inches(y + 0.1), Inches(3.75), Inches(0.35), title, 14, True, BLUE)
        textbox(s, Inches(x + 0.25), Inches(y + 0.48), Inches(3.75), Inches(0.65), body, 12, False, GRAY_DARK)

    out = "/Users/mrahul/Desktop/txt_sql_agent/Text_to_SQL_Agent_Director_Demo.pptx"
    prs.save(out)
    print(out)


if __name__ == "__main__":
    build()
