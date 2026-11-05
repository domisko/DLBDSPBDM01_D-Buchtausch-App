import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Arial", os.path.join(FONT_DIR, "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(FONT_DIR, "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", os.path.join(FONT_DIR, "Arial Italic.ttf")))

# Regenerate anytime with: python3 build_pdf.py
# Requires: pip3 install --user reportlab pymupdf (pymupdf only needed for the page-preview step below)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(PROJECT_DIR, "assets", "erm_diagramm.png")
OUT_DIR = os.path.join(PROJECT_DIR, "export")
OUT_FILENAME = "Miskovic-Dominik_14133980_DLBDSPBDM01_D_Konzeptionsphase_AB.pdf"

styles = {
    "title": ParagraphStyle("title", fontName="Arial-Bold", fontSize=15, leading=18, alignment=TA_CENTER, spaceAfter=4),
    "subtitle": ParagraphStyle("subtitle", fontName="Arial-Italic", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceAfter=14, textColor=colors.HexColor("#444444")),
    "h1": ParagraphStyle("h1", fontName="Arial-Bold", fontSize=13, leading=16, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#1a1a1a")),
    "h2": ParagraphStyle("h2", fontName="Arial-Bold", fontSize=11.5, leading=14, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#1a1a1a")),
    "body": ParagraphStyle("body", fontName="Arial", fontSize=11, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=7),
    "small_italic": ParagraphStyle("small_italic", fontName="Arial-Italic", fontSize=9, leading=11.5, spaceAfter=4, textColor=colors.HexColor("#444444")),
    "table_head": ParagraphStyle("table_head", fontName="Arial-Bold", fontSize=9, leading=11),
    "table_cell": ParagraphStyle("table_cell", fontName="Arial", fontSize=9, leading=11),
}

def P(text, style="body"):
    return Paragraph(text, styles[style])

story = []
story.append(P("Data-Mart-Erstellung in SQL (DLBDSPBDM01_D): Konzeptionsphase", "title"))
story.append(P("Miskovic, Dominik · Matrikelnummer: 14133980 · Kurs: DLBDSPBDM01_D", "subtitle"))

story.append(P("1. Problembeschreibung und Lösungsansatz", "h1"))
story.append(P(
    "Viele Menschen besitzen Bücher, die sie aktuell nicht lesen, aber nicht endgültig weggeben möchten, "
    "während andere in der Nachbarschaft genau diese Bücher gerne lesen würden, ohne sie dauerhaft zu besitzen. "
    "Die Buchtausch-App löst dieses Problem, indem sie Buchbesitzende und Interessierte in einer lokalen "
    "Gemeinschaft zusammenbringt und den zeitlich befristeten Verleih organisiert."
))
story.append(P(
    "Die Datenbank wird als relationales Schema mit PostgreSQL umgesetzt: ein modernes, quelloffenes DBMS mit "
    "vollständiger SQL-Unterstützung, das über die Erweiterung PostGIS zusätzlich effiziente räumliche Abfragen "
    "(Umkreissuche über Geokoordinaten) ermöglicht, was für die geforderte Kartenansicht zentral ist. Das "
    "Datenmodell trennt konsequent zwischen der <b>Buchausgabe</b> (unveränderliche bibliografische Daten wie "
    "Titel, Autor:in, Verlag, Genre, Sprache) und dem <b>Exemplar</b> (die konkrete, ausleihbare Kopie einer Person "
    "mit individuellem Zustand, Verleihbedingungen und Standort). Diese Trennung vermeidet redundante "
    "Datenspeicherung und bildet die Grundlage für eine angemessene Normalisierung (3NF)."
))

story.append(P("2. Anforderungsspezifikation", "h1"))
story.append(P("2.1 Rollen", "h2"))
story.append(P(
    "Jede registrierte Benutzer:in kann gleichzeitig als <b>Verleiher:in</b> (Besitzer:in eines eingestellten "
    "Exemplars) und als <b>Entleiher:in</b> (Ausleihende:r eines fremden Exemplars) auftreten. Funktional ist das "
    "eine Rolle mit zwei kontextabhängigen Aktionsbereichen, nicht zwei getrennte Rollen."
))

story.append(P("2.2 Aktionen", "h2"))
story.append(P(
    "<b>Verleiher:in:</b> Profil (Name, Adresse, Kontakt) pflegen · Buch als Exemplar einstellen (Zustand, max. "
    "Leihdauer, Versandoption) · Abholorte definieren · Verfügbarkeitszeitfenster festlegen · Exemplar mit "
    "Ort/Zeitfenster-Kombination aktiv anbieten · Ausleihvorgänge einsehen, Rückgabe bestätigen."
))
story.append(P(
    "<b>Entleiher:in:</b> Bücher tabellarisch durchsuchen/filtern (Genre, Sprache, Zustand) · verfügbare Bücher "
    "auf einer Karte im Umkreis anzeigen · Exemplar zu einem Zeitfenster ausleihen · Buch zurückgeben · nach "
    "Rückgabe bewerten und kommentieren."
))

story.append(P("2.3 Daten und Funktionen", "h2"))
story.append(P(
    "<b>Daten:</b> bibliografische Daten je Buchausgabe (Titel, ISBN, Erscheinungsjahr, Genre, Verlag, Sprache, "
    "Autor:in) · Personendaten (Name, Adresse, Kontakt) · Exemplardaten (Zustand, Leihdauer, Versand, Besitzer:in) "
    "· Logistikdaten (Abholorte mit Geokoordinaten, Zeitfenster) · Transaktionsdaten (Ausleih-/Rückgabedatum, "
    "Status) · Bewertungsdaten (Sterne, Kommentar)."
))
story.append(P(
    "<b>Funktionen:</b> tabellarische Suche/Filterung · räumliche Umkreissuche über Geokoordinaten · Verwaltung "
    "von Ausleihvorgängen · Erfassen/Anzeigen von Bewertungen."
))

story.append(PageBreak())

story.append(P("3. Entity-Relationship-Modell", "h1"))
story.append(P(
    "Das Modell umfasst 11 Entitäten und wird in Chen-Notation dargestellt (Rechteck = Entität, Raute = "
    "Beziehung). Zwei Beziehungen sind echte Dreifachbeziehungen (orange hervorgehoben):"
))
story.append(P(
    "<b>AUSLEIHT</b> (Exemplar × Benutzer × Zeitfenster, N:N:N): Da das Zeitfenster der besitzenden Person "
    "zugeordnet ist, bestimmt kein Paar der drei Entitäten das dritte Element eindeutig. "
    "<i>Bewusst vermieden wurde die naheliegende Triade „Verleiher:in, Entleiher:in, Exemplar\" aus der "
    "Aufgabenstellung, da die verleihende Person bereits über Exemplar.besitzer_id feststeht. Dies wäre eine "
    "unechte, auf eine binäre Beziehung reduzierbare Ternärbeziehung.</i>"
))
story.append(P(
    "<b>ANGEBOTEN_ALS</b> (Exemplar × Abholort × Zeitfenster, N:N:N): Eine besitzende Person kann pro Exemplar "
    "eine individuelle, gültige Kombination aus Ort und Zeitfenster festlegen."
))
story.append(Spacer(1, 6))

img = Image(IMG_PATH)
max_w = 16.5 * cm
max_h = 15.5 * cm
ratio = min(max_w / img.imageWidth, max_h / img.imageHeight)
img.drawWidth = img.imageWidth * ratio
img.drawHeight = img.imageHeight * ratio
img.hAlign = "CENTER"
story.append(img)

story.append(PageBreak())

story.append(P("4. Datenwörterbuch (kompakt)", "h1"))

dict_rows = [
    ["Entität", "Schlüsselattribute (Auswahl)"],
    ["Benutzer", "benutzer_id (PK), vorname, nachname, email (UNIQUE), telefon, registrierdatum"],
    ["Adresse", "adresse_id (PK), benutzer_id (FK), strasse, plz, stadt, breitengrad, laengengrad"],
    ["Buch", "buch_id (PK), titel, isbn, erscheinungsjahr, genre_id (FK), verlag_id (FK), sprache_id (FK)"],
    ["Autor", "autor_id (PK), vorname, nachname"],
    ["Verlag", "verlag_id (PK), name, land"],
    ["Genre", "genre_id (PK), bezeichnung"],
    ["Sprache", "sprache_id (PK), bezeichnung, iso_code"],
    ["Exemplar", "exemplar_id (PK), buch_id (FK), besitzer_id (FK), zustand, versand_moeglich, max_leihdauer_tage"],
    ["Abholort", "abholort_id (PK), benutzer_id (FK), bezeichnung, breitengrad, laengengrad"],
    ["Zeitfenster", "zeitfenster_id (PK), benutzer_id (FK), wochentag, startzeit, endzeit"],
    ["Bewertung", "bewertung_id (PK), buch_id (FK), benutzer_id (FK), sternebewertung (1–5), kommentar"],
]
dict_table_data = [[Paragraph(r[0], styles["table_head"] if i == 0 else styles["table_cell"]),
                     Paragraph(r[1], styles["table_head"] if i == 0 else styles["table_cell"])]
                    for i, r in enumerate(dict_rows)]
t1 = Table(dict_table_data, colWidths=[3.2 * cm, 13.3 * cm], repeatRows=1)
t1.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#999999")),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ededed")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t1)
story.append(P("Vollständiges Datenwörterbuch mit allen Attributen und Datentypen: siehe 02_Datenwoerterbuch.md.", "small_italic"))
story.append(Spacer(1, 6))

story.append(P("Beziehungsübersicht (Kardinalitäten, Chen-Notation)", "h2"))
rel_rows = [
    ["Beziehung", "Kardinalität"],
    ["Benutzer–Adresse", "1:1"],
    ["Benutzer–Exemplar, Benutzer–Abholort, Benutzer–Zeitfenster, Benutzer–Bewertung", "1:N"],
    ["Exemplar–Buch, Buch–Genre, Buch–Verlag, Buch–Sprache", "N:1"],
    ["Buch–Autor", "N:M"],
    ["Buch–Bewertung", "1:N"],
    ["AUSLEIHT (Exemplar, Benutzer, Zeitfenster)", "N:N:N"],
    ["ANGEBOTEN_ALS (Exemplar, Abholort, Zeitfenster)", "N:N:N"],
]
rel_table_data = [[Paragraph(r[0], styles["table_head"] if i == 0 else styles["table_cell"]),
                    Paragraph(r[1], styles["table_head"] if i == 0 else styles["table_cell"])]
                   for i, r in enumerate(rel_rows)]
t2 = Table(rel_table_data, colWidths=[13.3 * cm, 3.2 * cm], repeatRows=1)
t2.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#999999")),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ededed")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t2)
story.append(Spacer(1, 8))
story.append(P("Umfang: Anforderungsspezifikation max. 2 Seiten, Gesamtdokument max. 4 Seiten, 11pt (gemäß Aufgabenstellung Kap. 1.1).", "small_italic"))

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, OUT_FILENAME)
doc = SimpleDocTemplate(
    out_path, pagesize=A4,
    topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm,
    title="Data-Mart-Erstellung in SQL (DLBDSPBDM01_D) - Konzeptionsphase",
)
doc.build(story)
print("written", out_path)
