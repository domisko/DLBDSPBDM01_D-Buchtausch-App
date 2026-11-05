"""Rendert die erfassten psql-Ausgaben (sql/out/*.txt) als Terminal-Screenshots (PNG)."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "out")
IMG_DIR = os.path.join(BASE, "..", "assets", "screenshots")
os.makedirs(IMG_DIR, exist_ok=True)

FONT_PATH = "/System/Library/Fonts/Monaco.ttf" if os.path.exists("/System/Library/Fonts/Monaco.ttf") \
    else "/System/Library/Fonts/Menlo.ttc"
FONT_SIZE = 22
PADDING = 28
LINE_SPACING = 8
BG = (30, 30, 32)
FG = (223, 225, 226)
BAR = (58, 58, 60)
DOT_COLORS = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)


def render(txt_path, title, png_path):
    with open(txt_path, encoding="utf-8") as f:
        content = f.read().rstrip("\n")
    lines = content.split("\n") if content else ["(keine Ausgabe)"]

    dummy = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(dummy)
    max_w = max(d.textbbox((0, 0), line, font=font)[2] for line in lines) if lines else 400
    line_h = FONT_SIZE + LINE_SPACING

    titlebar_h = 44
    width = max_w + 2 * PADDING
    height = titlebar_h + len(lines) * line_h + 2 * PADDING

    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width, titlebar_h], fill=BAR)
    for i, c in enumerate(DOT_COLORS):
        draw.ellipse([14 + i * 22, titlebar_h // 2 - 7, 14 + i * 22 + 14, titlebar_h // 2 + 7], fill=c)
    tb_font = ImageFont.truetype(FONT_PATH, 16)
    tw = draw.textbbox((0, 0), title, font=tb_font)[2]
    draw.text(((width - tw) / 2, titlebar_h // 2 - 9), title, font=tb_font, fill=(200, 200, 200))

    y = titlebar_h + PADDING
    for line in lines:
        draw.text((PADDING, y), line, font=font, fill=FG)
        y += line_h

    img.save(png_path)
    print("saved", png_path, img.size)


jobs = [
    ("benutzer", "psql - buchtausch_app - benutzer"),
    ("adresse", "psql - buchtausch_app - adresse"),
    ("verlag", "psql - buchtausch_app - verlag"),
    ("genre", "psql - buchtausch_app - genre"),
    ("sprache", "psql - buchtausch_app - sprache"),
    ("buch", "psql - buchtausch_app - buch"),
    ("autor", "psql - buchtausch_app - autor"),
    ("buch_autor", "psql - buchtausch_app - buch_autor"),
    ("exemplar", "psql - buchtausch_app - exemplar"),
    ("abholort", "psql - buchtausch_app - abholort"),
    ("zeitfenster", "psql - buchtausch_app - verfuegbarkeitszeitfenster"),
    ("ausleihvorgang", "psql - buchtausch_app - ausleihvorgang"),
    ("angebot", "psql - buchtausch_app - angebot"),
    ("bewertung", "psql - buchtausch_app - bewertung"),
    ("raeumliche_suche", "psql - buchtausch_app - raeumliche Suche"),
    ("negativtest_selbstausleihe", "psql - buchtausch_app - Negativtest 1"),
    ("negativtest_bewertung", "psql - buchtausch_app - Negativtest 2"),
]

for name, title in jobs:
    render(os.path.join(OUT_DIR, f"{name}.txt"), title, os.path.join(IMG_DIR, f"{name}.png"))
