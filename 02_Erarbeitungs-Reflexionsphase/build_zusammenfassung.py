import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Arial", os.path.join(FONT_DIR, "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(FONT_DIR, "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", os.path.join(FONT_DIR, "Arial Italic.ttf")))

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "export")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "Miskovic-Dominik_14133980_DLBDSPBDM01_D_Erarbeitungsphase_KZ.pdf")

styles = {
    "title": ParagraphStyle("title", fontName="Arial-Bold", fontSize=15, leading=18, alignment=TA_CENTER, spaceAfter=4),
    "subtitle": ParagraphStyle("subtitle", fontName="Arial-Italic", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceAfter=14, textColor=colors.HexColor("#444444")),
    "h1": ParagraphStyle("h1", fontName="Arial-Bold", fontSize=13, leading=16, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#1a1a1a")),
    "body": ParagraphStyle("body", fontName="Arial", fontSize=11, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=7),
}


def P(text, style="body"):
    return Paragraph(text, styles[style])


story = [
    P("Data-Mart-Erstellung in SQL (DLBDSPBDM01_D): Kurze Zusammenfassung der Implementierung", "title"),
    P("Miskovic, Dominik &middot; Matrikelnummer: 14133980 &middot; Kurs: DLBDSPBDM01_D", "subtitle"),
    P("Erarbeitungs-/Reflexionsphase", "h1"),
    P(
        "Das Datenbankschema der Buchtausch-App wurde in PostgreSQL 16 umgesetzt und besteht aus 14 Tabellen: "
        "den 13 Entitäten aus dem ER-Modell der Konzeptionsphase sowie der Verbindungstabelle buch_autor zur "
        "Auflösung der N:M-Beziehung zwischen Buch und Autor:in. Beide Ternärbeziehungen aus Phase 1 (AUSLEIHT "
        "und ANGEBOTEN_ALS) wurden als eigene Tabellen mit Surrogatschlüssel umgesetzt (ausleihvorgang, angebot). "
        "Das ist eine Standardtechnik, wenn eine Beziehung selbst wieder referenziert werden muss, wie es das "
        "Tutor-Feedback zur Bewertung erforderte."
    ),
    P(
        "Alle drei Rückmeldungen aus dem Feedback zu Phase 1 wurden eingearbeitet. Erstens ist die Bewertung "
        "jetzt über einen UNIQUE-Fremdschlüssel an einen konkreten Ausleihvorgang gekoppelt statt direkt an "
        "Buch und Benutzer:in, zusätzlich per Trigger abgesichert, dass nur abgeschlossene ('zurueckgegeben') "
        "Ausleihvorgänge bewertet werden können. Zweitens wurde die Beziehung zwischen Benutzer und Adresse von "
        "1:1 auf 1:N geändert, sodass mehrere Adressen je Person möglich sind, ergänzt um ein Flag für die "
        "Hauptadresse. Drittens wurden die geforderten Constraints konsequent implementiert: CHECK-Constraints "
        "auf die Sternebewertung (1 bis 5), auf positive Leihdauer und auf die zeitliche Reihenfolge von "
        "Ausleih- und Zeitfenster-Daten, UNIQUE auf die E-Mail-Adresse sowie ein zusätzlicher Trigger, der "
        "verhindert, dass Nutzende ihr eigenes Exemplar ausleihen."
    ),
    P(
        "Die Datenbank wurde mit insgesamt über 175 Dummy-Datensätzen befüllt (mindestens 10 pro Tabelle), "
        "alle referenziell konsistent und alle Geschäftsregeln respektierend. Die räumliche Suchanforderung "
        "('Bücher in meiner Nähe') wurde über eine Haversine-Distanzformel direkt in SQL umgesetzt, ganz ohne "
        "zusätzliche Erweiterung wie PostGIS, und liefert nachweislich plausible, nach Entfernung sortierte "
        "Ergebnisse. Zwei Negativtests belegen, dass die implementierten Trigger tatsächlich greifen und "
        "fehlerhafte Eingaben zuverlässig zurückweisen: eine versuchte Selbst-Ausleihe sowie eine Bewertung "
        "für einen noch nicht abgeschlossenen Ausleihvorgang wurden beide korrekt abgelehnt."
    ),
    P(
        "Alle 15 dokumentierten Testfälle (ein SELECT-Statement je Entität, plus die räumliche Suche und die "
        "zwei Negativtests) wurden gegen die tatsächlich befüllte Datenbank ausgeführt; die zugehörigen "
        "Screenshots in der Präsentation zeigen die echten Ergebnisse aus psql."
    ),
]

doc = SimpleDocTemplate(
    OUT_PATH, pagesize=A4,
    topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm,
    title="Data-Mart-Erstellung in SQL (DLBDSPBDM01_D) - Kurze Zusammenfassung",
)
doc.build(story)
print("written", OUT_PATH)
