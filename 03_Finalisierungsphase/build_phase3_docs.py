"""
Erzeugt die vier PDF-Dokumente der Finalisierungsphase in export/:
  BE  3-seitiges PDF (Funktionalitaet + Metadaten)
  AB  Abstract (1 bis 1,5 Seiten, Formalia aus Aufgabenstellung 4.3)
  SQL SQL-Dokumentation mit Installationsanleitung und Testergebnissen
  GH  Link zum GitHub-Repository

Alle Zahlen (Tabellen, Eintraege, Groesse, Testanzahl) werden live aus der
Datenbank bzw. aus run_tests.py gelesen und nicht von Hand gepflegt.
Aufruf:  python3 build_phase3_docs.py
"""
import json
import os
import shutil
import subprocess
import sys

import fitz  # PyMuPDF, nur zur Seitenzahl-Kontrolle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle, KeepTogether)

BASE = os.path.dirname(os.path.abspath(__file__))
SQLDIR = os.path.join(BASE, "sql")
SHOTS = os.path.join(BASE, "assets", "screenshots")
EXPORT = os.path.join(BASE, "export")
os.makedirs(EXPORT, exist_ok=True)
sys.path.insert(0, SQLDIR)
import run_tests as rt  # noqa: E402  (liefert POSITIV, NEGATIV, PSQL, DB)

NAME = "Miskovic-Dominik_14133980_DLBDSPBDM01_D_Abschlussphase"
KOPF = "Miskovic, Dominik &middot; Matrikelnummer: 14133980 &middot; Kurs: DLBDSPBDM01_D"

cfg_path = os.path.join(BASE, "config.json")
GITHUB = ""
if os.path.exists(cfg_path):
    GITHUB = json.load(open(cfg_path, encoding="utf-8")).get("github_url", "").strip()
GITHUB_ANZEIGE = GITHUB or "https://github.com/[BENUTZERNAME]/[REPOSITORY] (Platzhalter, siehe config.json)"
if not GITHUB:
    print("HINWEIS: config.json enthaelt noch keine github_url, Platzhalter wird im PDF angezeigt.")

FD = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Arial", f"{FD}/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", f"{FD}/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", f"{FD}/Arial Italic.ttf"))
pdfmetrics.registerFont(TTFont("Menlo", "/System/Library/Fonts/Menlo.ttc"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-Bold")

GREY = colors.HexColor("#444444")
ST = {
    "title": ParagraphStyle("title", fontName="Arial-Bold", fontSize=15, leading=18, alignment=TA_CENTER, spaceAfter=3),
    "sub": ParagraphStyle("sub", fontName="Arial-Italic", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceAfter=10, textColor=GREY),
    "h1": ParagraphStyle("h1", fontName="Arial-Bold", fontSize=12.5, leading=15, spaceBefore=8, spaceAfter=4),
    "h2": ParagraphStyle("h2", fontName="Arial-Bold", fontSize=11, leading=13.5, spaceBefore=6, spaceAfter=3),
    "body": ParagraphStyle("body", fontName="Arial", fontSize=11, leading=14, alignment=TA_JUSTIFY, spaceAfter=5),
    "small": ParagraphStyle("small", fontName="Arial-Italic", fontSize=9, leading=11.5, textColor=GREY, spaceAfter=3),
    "th": ParagraphStyle("th", fontName="Arial-Bold", fontSize=8.5, leading=10.5),
    "td": ParagraphStyle("td", fontName="Arial", fontSize=8.5, leading=10.5),
    "tdc": ParagraphStyle("tdc", fontName="Arial", fontSize=8.5, leading=10.5, alignment=TA_CENTER),
    "code": ParagraphStyle("code", fontName="Menlo", fontSize=8.5, leading=11, backColor=colors.HexColor("#f3f3f3"),
                           borderPadding=(4, 4, 4, 4), spaceBefore=3, spaceAfter=7),
}


def P(t, s="body"):
    return Paragraph(t, ST[s])


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def code(t):
    return Paragraph(esc(t).replace("\n", "<br/>").replace(" ", "&nbsp;"), ST["code"])


def tabelle(kopf, zeilen, breiten, zentriert=()):
    data = [[P(k, "th") for k in kopf]]
    for z in zeilen:
        data.append([P(str(v), "tdc" if i in zentriert else "td") for i, v in enumerate(z)])
    t = Table(data, colWidths=[b * cm for b in breiten], repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ededed")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


# ------------------------------------------------------------------ Live-Daten
def sql_rows(stmt):
    r = subprocess.run([rt.PSQL, "-At", "-F", "|", "-d", rt.DB, "-c", stmt], capture_output=True, text=True, check=True)
    return [l.split("|") for l in r.stdout.strip().split("\n") if l]


meta_sql = open(os.path.join(SQLDIR, "04_metadaten.sql"), encoding="utf-8").read()
stmts = [s.strip() for s in "\n".join(l for l in meta_sql.split("\n") if not l.strip().startswith("--")).split(";") if s.strip()]
TAB = sql_rows(stmts[0])                       # tabelle | eintraege | groesse
SUM = sql_rows(stmts[1])[0]                    # tabellen | eintraege | dbgroesse | tab+idx
OBJ = sql_rows(stmts[2])[0]                    # pk fk uq ck idx trg fn
N_TAB, N_ROWS, DB_SIZE, TAB_SIZE = int(SUM[0]), int(SUM[1]), SUM[2], SUM[3]
PK, FK, UQ, CK, IDX, TRG, FN = (int(x) for x in OBJ)
N_POS, N_NEG = len(rt.POSITIV), len(rt.NEGATIV)
assert N_TAB == 14 and N_ROWS >= 280 and min(int(t[1]) for t in TAB) >= 10

ZWECK = {
    "abholort": "Öffentliche Übergabeorte mit Geokoordinaten", "adresse": "Private Adressen (1:N zu Benutzer)",
    "angebot": "Exemplar × Abholort × Zeitfenster (ANGEBOTEN_ALS)", "ausleihvorgang": "Exemplar × Entleiher × Zeitfenster (AUSLEIHT)",
    "autor": "Autor:innen", "benutzer": "Registrierte Personen", "bewertung": "Bewertung je abgeschlossenem Ausleihvorgang",
    "buch": "Bibliografische Ausgabe", "buch_autor": "Auflösung der N:M-Beziehung Buch–Autor",
    "exemplar": "Konkrete, ausleihbare Kopie einer Person", "genre": "Genres (Lookup)", "sprache": "Sprachen (Lookup)",
    "verfuegbarkeitszeitfenster": "Zeitfenster der Übergabe je Person", "verlag": "Verlage (Lookup)",
}

# Geschaeftsregeln: (Regel, Mechanismus, Objekt, Testname)
REGELN = [
    ("E-Mail eindeutig und formal plausibel", "UNIQUE + CHECK", "benutzer_email_key, CHECK auf benutzer.email", "neg_email"),
    ("Höchstens eine Hauptadresse je Person", "Partieller UNIQUE-Index", "ux_adresse_hauptadresse", "neg_hauptadresse"),
    ("Gültige geografische Koordinaten", "CHECK (5 Constraints)", "chk_adresse_*, chk_abholort_*", "neg_koordinaten"),
    ("Erscheinungsjahr plausibel und nicht in der Zukunft", "CHECK (feste Grenzen) + Trigger", "buch.erscheinungsjahr, trg_buch_erscheinungsjahr", "neg_erscheinungsjahr"),
    ("Leihdauer eines Exemplars 1 bis 365 Tage", "CHECK", "exemplar_max_leihdauer_tage_check", "neg_leihdauer_null"),
    ("Besitzer eines Exemplars wechselt nicht", "Trigger", "trg_exemplar_besitzer_unveraenderlich", "neg_besitzerwechsel"),
    ("Zeitfenster: Ende nach Beginn", "CHECK", "chk_zeitfenster_reihenfolge", "neg_zeitfenster_reihenfolge"),
    ("Angebot nur mit Abholort und Zeitfenster des Besitzers", "Trigger", "trg_angebot_besitzer", "neg_angebot_fremder_abholort"),
    ("Gleiche Angebotskombination nur einmal", "UNIQUE", "UNIQUE (exemplar_id, abholort_id, zeitfenster_id)", "neg_doppeltes_angebot"),
    ("Keine Ausleihe des eigenen Exemplars", "Trigger", "trg_ausleihvorgang_regeln", "neg_selbstausleihe"),
    ("Geplante Dauer höchstens max_leihdauer_tage", "Trigger", "trg_ausleihvorgang_regeln", "neg_leihdauer"),
    ("Zeitfenster gehört dem Besitzer des Exemplars", "Trigger", "trg_ausleihvorgang_regeln", "neg_fremdes_zeitfenster"),
    ("Ausleihe nur über ein als Angebot eingerichtetes Zeitfenster", "Trigger", "trg_ausleihvorgang_regeln", "neg_kein_angebot"),
    ("Ein Exemplar nie mehrfach gleichzeitig offen ausgeliehen", "Partieller UNIQUE-Index", "ux_ausleihvorgang_offen_je_exemplar", "neg_doppelte_ausleihe"),
    ("Geplantes Rückgabedatum nach Ausleihdatum", "CHECK", "chk_ausleih_rueckgabe_reihenfolge", "neg_rueckgabe_vor_ausleihe"),
    ("Status 'zurueckgegeben' genau dann mit Rückgabedatum", "CHECK", "chk_ausleih_status_rueckgabe", "neg_status_ohne_datum"),
    ("Bewertung nur nach Abschluss, nicht vor Rückgabe", "Trigger", "trg_bewertung_nur_abgeschlossen", "neg_bewertung_aktiv"),
    ("Höchstens eine Bewertung je Ausleihvorgang", "UNIQUE", "bewertung_ausleihvorgang_id_key", "neg_doppelte_bewertung"),
    ("Sternebewertung 1 bis 5", "CHECK", "bewertung_sternebewertung_check", "neg_sterne"),
    ("Bewertete Ausleihe bleibt abgeschlossen", "Trigger", "trg_ausleihvorgang_status_nach_bewertung", "neg_status_zurueck"),
    ("Referenzielle Integrität", f"FOREIGN KEY ({FK} Stück)", "alle Fremdschlüssel", "neg_fremdschluessel"),
]
assert {r[3] for r in REGELN} == {n[0] for n in rt.NEGATIV}, "jede Regel braucht genau einen Negativtest"

FEEDBACK = [
    ("CHECK auf erscheinungsjahr mit CURRENT_DATE", "CHECK nur mit festen Grenzen (1450 bis 2100); die zeitabhängige Prüfung läuft in einem Trigger, der beim Schreiben ausgewertet wird.", "neg_erscheinungsjahr"),
    ("Doppelte Ausleihen verhindern", "Partieller UNIQUE-Index auf exemplar_id für Status 'aktiv' und 'ueberfaellig'.", "neg_doppelte_ausleihe"),
    ("Maximale Leihdauer prüfen", "Trigger vergleicht geplante Dauer mit exemplar.max_leihdauer_tage.", "neg_leihdauer"),
    ("Zeitfenster und Angebote konsistent", "Trigger prüfen: Abholort und Zeitfenster gehören dem Besitzer; Ausleihe nur über ein eingerichtetes Angebot; Besitzer-Spalten sind unveränderlich.", "neg_fremdes_zeitfenster, neg_kein_angebot, neg_angebot_fremder_abholort"),
    ("Bewerteten Status nicht zurücksetzbar", "Trigger auf ausleihvorgang.status sperrt Rücksetzen, sobald eine Bewertung existiert.", "neg_status_zurueck"),
    ("Koordinaten und Status/Rückgabedatum", "CHECK auf Breite/Länge (Adresse, Abholort) und CHECK: Status 'zurueckgegeben' genau dann, wenn ein Rückgabedatum gesetzt ist.", "neg_koordinaten, neg_status_ohne_datum"),
    ("Weitere Negativtests", f"{N_NEG} Negativtests statt 2, je Geschäftsregel ein Test; zusätzlich Konsistenzprüfung.", "alle neg_*"),
    ("Mindestens 280 Datensätze", f"{N_ROWS} Datensätze (vorher 172), alle Tabellen mit mindestens 10 Einträgen.", "Metadaten"),
    ("Dokumentation der Absicherung", "Tabelle 'Geschäftsregeln und ihre Absicherung' (BE, SQL-Dokumentation).", "-"),
]


def build(path, story, pagesize=A4, margins=(2, 2, 2, 2), title=""):
    doc = SimpleDocTemplate(path, pagesize=pagesize, topMargin=margins[0] * cm, bottomMargin=margins[1] * cm,
                            leftMargin=margins[2] * cm, rightMargin=margins[3] * cm, title=title, author="Dominik Miskovic")
    doc.build(story)
    return len(fitz.open(path))


def link(url):
    return f'<link href="{url}" color="#1a4fa0">{esc(url)}</link>' if GITHUB else esc(url)


# ================================================================== BE (3 Seiten)
def build_be():
    s = [P("Data-Mart-Erstellung in SQL (DLBDSPBDM01_D): Finalisierungsphase", "title"), P(KOPF, "sub"),
         P("1. Funktionalität des Datenbanksystems", "h1"),
         P("Die Buchtausch-App-Datenbank (PostgreSQL 16) bildet den Verleih von Büchern in der Nachbarschaft ab. "
           f"Sie besteht aus {N_TAB} normalisierten Tabellen und deckt folgende Funktionen ab:"),
         P("<b>Katalog und Bestand:</b> Bücher als bibliografische Ausgabe (Titel, ISBN, Jahr, Verlag, Genre, Sprache, mehrere Autor:innen) "
           "sind von den Exemplaren getrennt, der konkreten Kopie einer Person mit Zustand, maximaler Leihdauer und Versandoption. "
           "<b>Logistik:</b> Personen legen mehrere Abholorte (mit Geokoordinaten) und Zeitfenster an und bieten ein Exemplar über die Tabelle "
           "<i>angebot</i> in einer gültigen Kombination aus Ort und Zeitfenster an. "
           "<b>Ausleihprozess:</b> <i>ausleihvorgang</i> hält Ausleih-, geplantes und tatsächliches Rückgabedatum sowie den Status (aktiv, überfällig, zurückgegeben). "
           "<b>Bewertungen:</b> je abgeschlossener Ausleihe höchstens eine Bewertung, sodass nur tatsächlich ausgeliehene Bücher bewertet werden. "
           "<b>Suche:</b> tabellarische Filter über Genre, Sprache und Zustand sowie eine räumliche Umkreissuche (\"Bücher in meiner Nähe\") "
           "per Haversine-Formel direkt in SQL, unterstützt durch einen Index auf die Koordinaten."),
         P("2. Umsetzung der Tutor-Rückmeldungen aus Phase 2", "h1"),
         tabelle(["Rückmeldung", "Umsetzung", "Nachweis (Test)"], FEEDBACK, [3.9, 8.4, 4.7]),
         P("3. Testabdeckung", "h1"),
         P(f"Insgesamt wurden {N_POS + N_NEG} Testfälle automatisiert gegen die befüllte Datenbank ausgeführt: {N_POS} positive Abfragen "
           f"(eine je Tabelle, räumliche Suche, Konsistenzprüfung mit 0 Verstößen) und {N_NEG} Negativtests, die jeweils in einer "
           "Transaktion mit ROLLBACK laufen und mit der erwarteten Fehlermeldung scheitern. Alle Erwartungen wurden erfüllt; "
           "die Ergebnisse stehen im SQL-Dokument dieser Phase."),
         PageBreak(),
         P("4. Geschäftsregeln und ihre Absicherung", "h1"),
         P(f"Jede Regel ist durch einen Constraint, einen Index oder einen Trigger abgesichert und durch einen eigenen Negativtest belegt "
           f"({PK} Primärschlüssel, {FK} Fremdschlüssel, {UQ} UNIQUE-Constraints, {CK} CHECK-Constraints, {IDX} Indizes, {TRG} Trigger)."),
         tabelle(["Regel", "Mechanismus", "Objekt", "Negativtest"], REGELN, [4.5, 2.7, 5.2, 4.6]),
         PageBreak(),
         P("5. Metadaten der Datenbank", "h1"),
         tabelle(["Tabelle", "Zweck", "Einträge", "Größe (inkl. Indizes)"],
                 [(t[0], ZWECK[t[0]], t[1], t[2]) for t in TAB] + [("<b>Summe</b>", "", f"<b>{N_ROWS}</b>", f"<b>{TAB_SIZE}</b>")],
                 [4.4, 7.5, 1.8, 3.3], zentriert=(2, 3)),
         Spacer(1, 6),
         tabelle(["Kennzahl", "Wert"],
                 [("Anzahl Tabellen", N_TAB), ("Anzahl Einträge (alle Tabellen)", N_ROWS),
                  ("Kleinste Tabelle (Einträge)", min(int(t[1]) for t in TAB)),
                  ("Größe der Datenbank (gesamt, inkl. Systemkatalog)", DB_SIZE),
                  ("Größe der Tabellen inkl. Indizes", TAB_SIZE),
                  ("Primär- / Fremdschlüssel / UNIQUE / CHECK", f"{PK} / {FK} / {UQ} / {CK}"),
                  ("Indizes / Trigger / Funktionen", f"{IDX} / {TRG} / {FN}")],
                 [10.5, 6.5], zentriert=(1,)),
         Spacer(1, 4),
         P("Die Größe wurde mit <i>pg_database_size</i> bzw. <i>pg_total_relation_size</i> ermittelt (Skript 04_metadaten.sql).", "small"),
         P("6. Repository", "h1"),
         P("Code, Berichte und README liegen im GitHub-Repository:"),
         Paragraph(link(GITHUB_ANZEIGE), ParagraphStyle("lnk", parent=ST["body"], alignment=TA_LEFT))]
    n = build(os.path.join(EXPORT, NAME + "_BE.pdf"), s, title="Finalisierungsphase: Funktionalität und Metadaten")
    return n


# ================================================================== AB (Abstract)
def build_ab():
    ab_body = ParagraphStyle("ab", fontName="Arial", fontSize=11, leading=19, alignment=TA_JUSTIFY, spaceAfter=6,
                             hyphenationLang="de_DE", embeddedHyphenation=1, uriWasteReduce=0.3)
    ab_h = ParagraphStyle("abh", fontName="Arial-Bold", fontSize=12, leading=19, alignment=TA_JUSTIFY, spaceBefore=2, spaceAfter=6)
    H = lambda t: Paragraph(t, ab_h)
    B = lambda t: Paragraph(t, ab_body)
    s = [H("Abstract: Data-Mart-Erstellung in SQL (DLBDSPBDM01_D), Buchtausch-App"),
         H("Ausgangslage und Zielsetzung"),
         B("Ziel des Projekts war der Entwurf und die Umsetzung einer normalisierten relationalen Datenbank für eine Buchtausch-App, "
           "über die Nachbarinnen und Nachbarn Bücher zeitlich befristet verleihen und ausleihen. Die Datenbank muss bibliografische Daten, "
           "Personen- und Adressdaten, Verleihbedingungen, Übergabeorte mit Geokoordinaten, Zeitfenster, Ausleihvorgänge und Bewertungen "
           "aufnehmen und neben tabellarischen auch räumliche Abfragen (\"Bücher in meiner Nähe\") ermöglichen."),
         H("Konzept und Methodik"),
         B("Die Arbeit folgte den drei Phasen des Portfolios. In der Konzeptionsphase entstanden eine Anforderungsspezifikation, ein ER-Modell "
           "in Chen-Notation mit elf Entitäten und zwei echten Dreifachbeziehungen sowie ein Datenwörterbuch. Zentrale Entwurfsentscheidung ist die "
           "Trennung von Buch (bibliografische Ausgabe) und Exemplar (konkrete Kopie einer Person), sodass Titel-, Autor- und Verlagsdaten nicht je Kopie "
           "wiederholt werden (dritte Normalform). Als DBMS wurde PostgreSQL gewählt, da die Aufgabenstellung kein System vorgibt und PostgreSQL "
           "deklarative Constraints, partielle Indizes und Trigger in PL/pgSQL bietet."),
         H("Umsetzung"),
         B(f"In der Erarbeitungsphase wurde das Modell in ein Schema mit {N_TAB} Tabellen überführt. Die beiden Dreifachbeziehungen wurden als eigene "
           "Tabellen mit Surrogatschlüssel umgesetzt, weil eine Bewertung auf einen konkreten Ausleihvorgang verweisen muss. Die Testdaten erzeugt ein "
           "Python-Skript, das die Geschäftsregeln bereits beim Erzeugen prüft. Testfälle laufen automatisiert gegen die Datenbank; Negativtests werden "
           "in einer Transaktion mit ROLLBACK ausgeführt. Die Rückmeldungen zu beiden Zwischenabgaben führten zu gezielten Verbesserungen: Bewertungen "
           "sind an Ausleihvorgänge gekoppelt, Adressen stehen in einer 1:N-Beziehung zum Benutzer, der zeitabhängige CHECK auf das Erscheinungsjahr wurde "
           "durch feste Grenzen und einen Trigger ersetzt, ein partieller UNIQUE-Index verhindert doppelte offene Ausleihen, und weitere Trigger sichern "
           "die maximale Leihdauer sowie die Zuordnung von Zeitfenstern zu Besitzer und Angebot. Die räumliche Suche nutzt die Haversine-Formel direkt in SQL."),
         H("Ergebnis und Reflexion"),
         B(f"Das Ergebnis umfasst {N_TAB} Tabellen mit {N_ROWS} Datensätzen (jede Tabelle mit mindestens zehn Einträgen), {PK} Primär-, {FK} Fremdschlüssel- "
           f"und {CK} CHECK-Constraints, {TRG} Trigger sowie {N_POS + N_NEG} automatisierte Testfälle ({N_POS} positive, {N_NEG} negative), die alle die erwartete "
           "Wirkung zeigen. Die Anforderungen der Aufgabenstellung sind damit erfüllt. Als wesentliche Erkenntnis zeigte sich, dass tabellenübergreifende Regeln "
           "(Zeitfenster gehört zum Besitzer, Bewertung nur nach Rückgabe) nicht als einfache CHECK-Constraints formulierbar sind, sondern Trigger erfordern, die "
           "wiederum durch Negativtests abgesichert werden müssen. Einschränkungen sind der Verzicht auf die Erweiterung PostGIS, die rein synthetischen Testdaten "
           "und fehlende Tests unter paralleler Last. Eingesetzt wurden PostgreSQL 16 (psql), Python 3 für Datengenerierung, Testautomatisierung und "
           "Dokumenterstellung sowie Git und GitHub.")]
    return build(os.path.join(EXPORT, NAME + "_AB.pdf"), s, margins=(2, 2, 2, 2), title="Abstract")


# ================================================================== GH
def build_gh():
    s = [Spacer(1, 3 * cm), P("GitHub-Repository", "title"), P(KOPF, "sub"), Spacer(1, 1 * cm),
         P("Das Repository enthält den Code (SQL-Schema, Dummy-Daten, Testfälle, Skripte), die Berichte aller drei Phasen und eine README mit Installationsanleitung."),
         Spacer(1, 0.5 * cm), P(f"<b>Link:</b> {link(GITHUB_ANZEIGE)}")]
    return build(os.path.join(EXPORT, NAME + "_GH.pdf"), s, title="Link zum GitHub-Repository")


# ================================================================== SQL-Dokumentation (Querformat)
def build_sql():
    W = landscape(A4)
    inst = [
        ("PostgreSQL installieren (ab Version 14; getestet mit 16)", "macOS (Homebrew):  brew install postgresql@16 && brew services start postgresql@16\nDebian/Ubuntu:     sudo apt install postgresql\nWindows:           Installer von postgresql.org"),
        ("Datenbank anlegen", "createdb buchtausch_app"),
        ("Schema einspielen (Tabellen, Constraints, Trigger, Indizes)", "psql -d buchtausch_app -f 01_schema.sql"),
        ("Dummy-Daten einspielen", "psql -d buchtausch_app -f 02_dummy_data.sql"),
        ("Testfälle ausführen (optional; Negativtests mit ROLLBACK)", "psql -d buchtausch_app -f 03_testfaelle.sql"),
        ("Metadaten abrufen (optional)", "psql -d buchtausch_app -f 04_metadaten.sql"),
        ("Automatisierte Tests mit Erwartungsprüfung (optional)", "pip3 install pillow\npython3 run_tests.py buchtausch_app"),
    ]
    s = [P("SQL-Dokumentation, Installationsanleitung und Testergebnisse", "title"), P(KOPF + " &middot; Finalisierungsphase", "sub"),
         P("1. Dateien", "h1"),
         tabelle(["Datei", "Inhalt"],
                 [("01_schema.sql", f"DDL: {N_TAB} Tabellen, {PK} Primär-, {FK} Fremdschlüssel-, {UQ} UNIQUE- und {CK} CHECK-Constraints, {IDX} Indizes, {TRG} Trigger, {FN} Funktionen"),
                  ("02_dummy_data.sql", f"{N_ROWS} Datensätze, jede Tabelle mit mindestens 10 Einträgen (erzeugt mit generate_dummy_data.py)"),
                  ("03_testfaelle.sql", f"{N_POS} positive Abfragen und {N_NEG} Negativtests (jeweils BEGIN ... ROLLBACK)"),
                  ("04_metadaten.sql", "Anzahl Tabellen, Einträge, Größen und Objektanzahlen"),
                  ("generate_dummy_data.py, run_tests.py", "Hilfsskripte: Datengenerierung mit Regelprüfung, Testautomatisierung und Screenshot-Erzeugung")],
                 [6.0, 19.5]),
         P("2. Installationsanleitung", "h1")]
    for i, (titel, befehl) in enumerate(inst, 1):
        s += [KeepTogether([P(f"<b>Schritt {i}:</b> {titel}", "body"), code(befehl)])]
    s += [P("Die Dateien müssen in dieser Reihenfolge eingespielt werden, da 02_dummy_data.sql die Tabellen aus 01_schema.sql voraussetzt. "
            "01_schema.sql löscht vorhandene Tabellen gleichen Namens (DROP TABLE IF EXISTS) und kann daher beliebig oft neu ausgeführt werden.", "small"),
          PageBreak(),
          P("3. Geschäftsregeln und ihre Absicherung", "h1"),
          tabelle(["Nr.", "Regel", "Mechanismus", "Datenbankobjekt", "Negativtest"],
                  [(i, r[0], r[1], r[2], r[3]) for i, r in enumerate(REGELN, 1)], [1.0, 9.2, 5.0, 6.3, 4.0], zentriert=(0,)),
          Spacer(1, 4),
          P("4. Umsetzung der Tutor-Rückmeldungen aus Phase 2", "h1"),
          tabelle(["Rückmeldung", "Umsetzung", "Nachweis"], FEEDBACK, [6.0, 13.5, 6.0]),
          PageBreak(),
          P("5. Ergebnisse: positive Testfälle", "h1"),
          P("Jeder Screenshot zeigt die echte psql-Ausgabe des Testfalls gegen die befüllte Datenbank.", "small")]

    def shot(name, titel, zusatz=""):
        img = Image(os.path.join(SHOTS, name + ".png"))
        r = min(23.5 * cm / img.imageWidth, 10.5 * cm / img.imageHeight, 1.0)
        img.drawWidth, img.drawHeight = img.imageWidth * r, img.imageHeight * r
        img.hAlign = "LEFT"
        return KeepTogether([P(f"<b>{titel}</b>" + (f" &middot; {zusatz}" if zusatz else ""), "h2"), img, Spacer(1, 4)])

    for name, titel, _sql in rt.POSITIV:
        s.append(shot(name, titel))
    s += [PageBreak(), P("6. Ergebnisse: Negativtests", "h1"),
          P("Jeder Negativtest wird in einer Transaktion mit ROLLBACK ausgeführt und muss mit einer Fehlermeldung scheitern. "
            "Es werden keine Daten verändert (nach allen Tests: unverändert " + str(N_ROWS) + " Datensätze).", "small")]
    for name, titel, regel, schutz, _sql in rt.NEGATIV:
        s.append(shot(name, titel, f"Regel: {regel}; abgesichert durch: {schutz}"))
    return build(os.path.join(EXPORT, NAME + "_SQL.pdf"), s, pagesize=W, margins=(1.5, 1.5, 1.8, 1.8), title="SQL-Dokumentation")


if __name__ == "__main__":
    ergebnis = {"BE": build_be(), "AB": build_ab(), "GH": build_gh(), "SQL": build_sql()}
    for k, v in ergebnis.items():
        print(f"{k}: {v} Seite(n)")
    if ergebnis["BE"] != 3:
        print("WARNUNG: BE muss genau 3 Seiten haben!")
    if not 1 <= ergebnis["AB"] <= 2:
        print("WARNUNG: Abstract muss 1 bis 1,5 Seiten haben!")
