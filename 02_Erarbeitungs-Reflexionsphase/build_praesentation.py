import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Arial", os.path.join(FONT_DIR, "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(FONT_DIR, "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", os.path.join(FONT_DIR, "Arial Italic.ttf")))
pdfmetrics.registerFont(TTFont("Menlo", "/System/Library/Fonts/Menlo.ttc"))

BASE = os.path.dirname(os.path.abspath(__file__))
SHOT_DIR = os.path.join(BASE, "assets", "screenshots")
OUT_DIR = os.path.join(BASE, "export")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "Miskovic-Dominik_14133980_DLBDSPBDM01_D_Erarbeitungsphase_PR.pdf")

PAGE_SIZE = landscape(A4)
PAGE_W, PAGE_H = PAGE_SIZE

styles = {
    "title": ParagraphStyle("title", fontName="Arial-Bold", fontSize=28, leading=32, alignment=TA_CENTER),
    "subtitle": ParagraphStyle("subtitle", fontName="Arial", fontSize=14, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#444444")),
    "h1": ParagraphStyle("h1", fontName="Arial-Bold", fontSize=18, leading=22, textColor=colors.HexColor("#1a1a1a")),
    "label": ParagraphStyle("label", fontName="Arial-Bold", fontSize=10.5, leading=13, textColor=colors.HexColor("#555555"), spaceBefore=6, spaceAfter=2),
    "code": ParagraphStyle("code", fontName="Menlo", fontSize=8, leading=10.5, textColor=colors.HexColor("#111111")),
    "body": ParagraphStyle("body", fontName="Arial", fontSize=11, leading=15, alignment=TA_LEFT),
    "small": ParagraphStyle("small", fontName="Arial-Italic", fontSize=9, leading=12, textColor=colors.HexColor("#555555")),
}


def code_block(text):
    lines = text.strip("\n").split("\n")
    html = "<br/>".join(l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;") for l in lines)
    return Paragraph(html, styles["code"])


def slide_image(path, max_w, max_h):
    img = Image(path)
    ratio = min(max_w / img.imageWidth, max_h / img.imageHeight, 1.0)
    img.drawWidth = img.imageWidth * ratio
    img.drawHeight = img.imageHeight * ratio
    return img


story = []

# ---------------- Titelfolie ----------------
story.append(Spacer(1, 4 * cm))
story.append(Paragraph("Data-Mart-Erstellung in SQL (DLBDSPBDM01_D)", styles["title"]))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("Erarbeitungs-/Reflexionsphase: Implementierung der Buchtausch-App-Datenbank", styles["subtitle"]))
story.append(Spacer(1, 0.6 * cm))
story.append(Paragraph("Miskovic, Dominik &middot; Matrikelnummer: 14133980 &middot; Kurs: DLBDSPBDM01_D", styles["subtitle"]))
story.append(PageBreak())

# ---------------- Entitaets-Folien ----------------
entities = [
    ("Benutzer", """CREATE TABLE benutzer (
    benutzer_id      SERIAL PRIMARY KEY,
    vorname           VARCHAR(50)  NOT NULL,
    nachname          VARCHAR(50)  NOT NULL,
    email             VARCHAR(100) NOT NULL UNIQUE,
    telefon           VARCHAR(20),
    registrierdatum   DATE NOT NULL DEFAULT CURRENT_DATE
);""",
     "SELECT benutzer_id, vorname, nachname, email, registrierdatum\nFROM benutzer ORDER BY registrierdatum LIMIT 5;",
     "benutzer.png",
     "email ist UNIQUE (Constraint aus dem Tutor-Feedback)."),

    ("Adresse", """CREATE TABLE adresse (
    adresse_id     SERIAL PRIMARY KEY,
    benutzer_id     INTEGER NOT NULL REFERENCES benutzer(benutzer_id),
    strasse, hausnummer, plz, stadt ...
    breitengrad DECIMAL(9,6), laengengrad DECIMAL(9,6),
    ist_hauptadresse BOOLEAN NOT NULL DEFAULT FALSE
);
-- max. 1 Hauptadresse je Person:
CREATE UNIQUE INDEX ux_adresse_hauptadresse
    ON adresse (benutzer_id) WHERE ist_hauptadresse = TRUE;""",
     "SELECT b.vorname, b.nachname, a.stadt, a.ist_hauptadresse\nFROM adresse a JOIN benutzer b USING (benutzer_id)\nWHERE b.benutzer_id = 1;",
     "adresse.png",
     "Nach Tutor-Feedback von 1:1 auf 1:N geändert: eine Person kann mehrere Adressen haben."),

    ("Verlag", """CREATE TABLE verlag (
    verlag_id  SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    land        VARCHAR(50)
);""",
     "SELECT verlag_id, name, land FROM verlag ORDER BY name LIMIT 5;",
     "verlag.png",
     "Lookup-Entität, vermeidet Wiederholung von Verlagsnamen bei jedem Buch."),

    ("Genre", """CREATE TABLE genre (
    genre_id     SERIAL PRIMARY KEY,
    bezeichnung   VARCHAR(50) NOT NULL UNIQUE
);""",
     "SELECT genre_id, bezeichnung FROM genre ORDER BY genre_id;",
     "genre.png",
     "10 Genres als Dummy-Daten, UNIQUE verhindert Duplikate."),

    ("Sprache", """CREATE TABLE sprache (
    sprache_id   SERIAL PRIMARY KEY,
    bezeichnung   VARCHAR(50) NOT NULL,
    iso_code      CHAR(2) NOT NULL UNIQUE
);""",
     "SELECT sprache_id, bezeichnung, iso_code\nFROM sprache ORDER BY bezeichnung LIMIT 5;",
     "sprache.png",
     "ISO-639-1-Code als zusätzliches, eindeutiges Attribut."),

    ("Buch", """CREATE TABLE buch (
    buch_id  SERIAL PRIMARY KEY,
    titel VARCHAR(200) NOT NULL, isbn VARCHAR(20) UNIQUE,
    erscheinungsjahr INTEGER CHECK (erscheinungsjahr BETWEEN 1450 AND ...),
    genre_id INTEGER REFERENCES genre(genre_id),
    verlag_id INTEGER REFERENCES verlag(verlag_id),
    sprache_id INTEGER NOT NULL REFERENCES sprache(sprache_id)
);""",
     "SELECT bu.titel, bu.erscheinungsjahr, g.bezeichnung genre,\n       v.name verlag, s.bezeichnung sprache\nFROM buch bu JOIN genre g USING (genre_id)\nJOIN verlag v USING (verlag_id) JOIN sprache s USING (sprache_id)\nORDER BY bu.titel LIMIT 5;",
     "buch.png",
     "Bibliografische Ausgabe, bewusst getrennt vom Exemplar (siehe Phase 1)."),

    ("Autor", """CREATE TABLE autor (
    autor_id   SERIAL PRIMARY KEY,
    vorname     VARCHAR(50) NOT NULL,
    nachname    VARCHAR(50) NOT NULL
);
CREATE TABLE buch_autor (   -- Aufloesung der N:M-Beziehung
    buch_id INTEGER REFERENCES buch(buch_id),
    autor_id INTEGER REFERENCES autor(autor_id),
    PRIMARY KEY (buch_id, autor_id)
);""",
     "SELECT bu.titel, string_agg(a.vorname||' '||a.nachname, ', ') autor_innen\nFROM buch bu JOIN buch_autor ba USING (buch_id)\nJOIN autor a USING (autor_id)\nGROUP BY bu.buch_id, bu.titel HAVING count(*) > 1;",
     "autor.png",
     "Testfall zeigt gezielt Bücher mit mehreren Autor:innen (N:M-Fall)."),

    ("Buch_Autor (Verbindungstabelle)", """CREATE TABLE buch_autor (
    buch_id   INTEGER NOT NULL REFERENCES buch(buch_id),
    autor_id  INTEGER NOT NULL REFERENCES autor(autor_id),
    PRIMARY KEY (buch_id, autor_id)
);""",
     "SELECT buch_id, autor_id FROM buch_autor\nORDER BY buch_id LIMIT 6;",
     "buch_autor.png",
     "Physische Umsetzung der N:M-Beziehung Buch-Autor als eigene Tabelle."),

    ("Exemplar", """CREATE TABLE exemplar (
    exemplar_id  SERIAL PRIMARY KEY,
    buch_id INTEGER NOT NULL REFERENCES buch(buch_id),
    besitzer_id INTEGER NOT NULL REFERENCES benutzer(benutzer_id),
    zustand VARCHAR(20) NOT NULL CHECK (zustand IN
        ('neu','sehr gut','gut','gebraucht','stark gebraucht')),
    versand_moeglich BOOLEAN NOT NULL DEFAULT FALSE,
    max_leihdauer_tage INTEGER NOT NULL CHECK (max_leihdauer_tage > 0),
    eingestellt_am DATE NOT NULL DEFAULT CURRENT_DATE
);""",
     "SELECT e.exemplar_id, bu.titel, be.vorname||' '||be.nachname besitzer_in,\n       e.zustand, e.max_leihdauer_tage\nFROM exemplar e JOIN buch bu USING (buch_id)\nJOIN benutzer be ON be.benutzer_id = e.besitzer_id\nORDER BY e.exemplar_id LIMIT 5;",
     "exemplar.png",
     "max_leihdauer_tage > 0 per CHECK erzwungen (Tutor-Feedback Punkt 3)."),

    ("Abholort", """CREATE TABLE abholort (
    abholort_id  SERIAL PRIMARY KEY,
    benutzer_id   INTEGER NOT NULL REFERENCES benutzer(benutzer_id),
    bezeichnung, strasse, plz, stadt VARCHAR ...,
    breitengrad DECIMAL(9,6) NOT NULL,
    laengengrad DECIMAL(9,6) NOT NULL
);""",
     "SELECT abholort_id, bezeichnung, stadt\nFROM abholort ORDER BY abholort_id LIMIT 5;",
     "abholort.png",
     "Öffentliche Übergabepunkte, getrennt von der privaten Adresse."),

    ("Verfügbarkeitszeitfenster", """CREATE TABLE verfuegbarkeitszeitfenster (
    zeitfenster_id  SERIAL PRIMARY KEY,
    benutzer_id      INTEGER NOT NULL REFERENCES benutzer(benutzer_id),
    wochentag        VARCHAR(10) NOT NULL CHECK (wochentag IN
                      ('Montag', ..., 'Sonntag')),
    startzeit TIME NOT NULL, endzeit TIME NOT NULL,
    CONSTRAINT chk_zeitfenster_reihenfolge CHECK (endzeit > startzeit)
);""",
     "SELECT zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit\nFROM verfuegbarkeitszeitfenster ORDER BY zeitfenster_id LIMIT 5;",
     "zeitfenster.png",
     "endzeit > startzeit per CHECK validiert (Tutor-Feedback Punkt 3)."),

    ("Ausleihvorgang", """CREATE TABLE ausleihvorgang (   -- reifizierte Ternärbeziehung AUSLEIHT
    ausleihvorgang_id  SERIAL PRIMARY KEY,
    exemplar_id INTEGER NOT NULL REFERENCES exemplar(exemplar_id),
    entleiher_id INTEGER NOT NULL REFERENCES benutzer(benutzer_id),
    zeitfenster_id INTEGER NOT NULL REFERENCES verfuegbarkeitszeitfenster(...),
    ausleihdatum DATE NOT NULL DEFAULT CURRENT_DATE,
    geplantes_rueckgabedatum DATE NOT NULL,
    tatsaechliches_rueckgabedatum DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'aktiv'
        CHECK (status IN ('aktiv','zurueckgegeben','ueberfaellig'))
);
-- Trigger: entleiher_id darf nicht besitzer_id des Exemplars sein.""",
     "SELECT av.ausleihvorgang_id, bu.titel,\n       en.vorname||' '||en.nachname entleiher_in,\n       av.ausleihdatum, av.status\nFROM ausleihvorgang av JOIN exemplar e USING (exemplar_id)\nJOIN buch bu USING (buch_id)\nJOIN benutzer en ON en.benutzer_id = av.entleiher_id\nORDER BY av.ausleihvorgang_id LIMIT 6;",
     "ausleihvorgang.png",
     "Reifizierung der Ternärbeziehung AUSLEIHT aus Phase 1 (eigener PK nötig, damit Bewertung darauf verweisen kann)."),

    ("Angebot", """CREATE TABLE angebot (   -- reifizierte Ternärbeziehung ANGEBOTEN_ALS
    angebot_id   SERIAL PRIMARY KEY,
    exemplar_id   INTEGER NOT NULL REFERENCES exemplar(exemplar_id),
    abholort_id   INTEGER NOT NULL REFERENCES abholort(abholort_id),
    zeitfenster_id INTEGER NOT NULL REFERENCES verfuegbarkeitszeitfenster(...),
    aktiv         BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (exemplar_id, abholort_id, zeitfenster_id)
);""",
     "SELECT an.angebot_id, bu.titel, ao.stadt, an.aktiv\nFROM angebot an JOIN exemplar e USING (exemplar_id)\nJOIN buch bu USING (buch_id)\nJOIN abholort ao USING (abholort_id)\nORDER BY an.angebot_id LIMIT 6;",
     "angebot.png",
     "Reifizierung der zweiten Ternärbeziehung aus Phase 1."),

    ("Bewertung", """CREATE TABLE bewertung (
    bewertung_id       SERIAL PRIMARY KEY,
    ausleihvorgang_id   INTEGER NOT NULL UNIQUE
                         REFERENCES ausleihvorgang(ausleihvorgang_id),
    sternebewertung      INTEGER NOT NULL CHECK (sternebewertung BETWEEN 1 AND 5),
    kommentar            TEXT,
    erstellt_am          DATE NOT NULL DEFAULT CURRENT_DATE
);
-- Trigger: nur INSERT, wenn ausleihvorgang.status = 'zurueckgegeben'.""",
     "SELECT bu.titel, ROUND(AVG(bw.sternebewertung),1) durchschnitt,\n       count(*) anzahl_bewertungen\nFROM bewertung bw JOIN ausleihvorgang av USING (ausleihvorgang_id)\nJOIN exemplar e USING (exemplar_id) JOIN buch bu USING (buch_id)\nGROUP BY bu.buch_id, bu.titel ORDER BY durchschnitt DESC LIMIT 6;",
     "bewertung.png",
     "Feedback Phase 1 umgesetzt: Bewertung hängt jetzt am Ausleihvorgang, nicht direkt an Buch/Benutzer."),
]

for name, ddl, test, shot, note in entities:
    story.append(Paragraph(f"Entität: {name}", styles["h1"]))
    tbl_data = [
        [Paragraph("CREATE TABLE (Ausschnitt)", styles["label"]), ""],
    ]
    left_col = [
        Paragraph("CREATE TABLE (ggf. gekürzt)", styles["label"]),
        code_block(ddl),
        Paragraph("Testfall", styles["label"]),
        code_block(test),
        Paragraph(note, styles["small"]),
    ]
    right_col = [slide_image(os.path.join(SHOT_DIR, shot), 13.5 * cm, 10.5 * cm)]
    grid = Table([[left_col, right_col]], colWidths=[15.5 * cm, 13.5 * cm])
    grid.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(Spacer(1, 4))
    story.append(grid)
    story.append(PageBreak())

# ---------------- Bonus-Folien ----------------
bonus = [
    ("Bonus: Räumliche Suche (\"Bücher in meiner Nähe\")",
     """-- Umkreissuche per Haversine-Formel (ohne PostGIS-Erweiterung),
-- Referenzpunkt hier beispielhaft: Berlin (52.520 / 13.405)
SELECT ..., ROUND((6371 * acos(
    cos(radians(:lat)) * cos(radians(ao.breitengrad)) *
    cos(radians(ao.laengengrad) - radians(:lng)) +
    sin(radians(:lat)) * sin(radians(ao.breitengrad))
))::numeric, 1) AS entfernung_km
FROM angebot a JOIN exemplar e USING (exemplar_id)
JOIN buch bu USING (buch_id) JOIN abholort ao USING (abholort_id)
WHERE a.aktiv = TRUE ORDER BY entfernung_km;""",
     "-- siehe CREATE-Statement oben, direkt ausführbar mit festen Koordinaten:\nSELECT bu.titel, ao.stadt, ao.bezeichnung, entfernung_km ...\nORDER BY entfernung_km LIMIT 5;",
     "raeumliche_suche.png",
     "Setzt die Anforderung \"Bücher in meiner Nähe auf einer Karte anzeigen\" aus der Anforderungsspezifikation um."),

    ("Bonus: Negativtest 1 (Datenintegrität)",
     """CREATE OR REPLACE FUNCTION fn_check_nicht_selbst_ausleihen()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.entleiher_id = (SELECT besitzer_id FROM exemplar
                          WHERE exemplar_id = NEW.exemplar_id) THEN
    RAISE EXCEPTION 'Exemplar kann nicht von der besitzenden Person
                      selbst ausgeliehen werden (exemplar_id=%).',
                      NEW.exemplar_id;
  END IF;
  RETURN NEW;
END; $$ LANGUAGE plpgsql;""",
     "-- Testfall: Besitzer:in von Exemplar 1 versucht, es selbst auszuleihen\nINSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id,\n    ausleihdatum, geplantes_rueckgabedatum)\nVALUES (1, (SELECT besitzer_id FROM exemplar WHERE exemplar_id=1),\n    1, CURRENT_DATE, CURRENT_DATE + 7);",
     "negativtest_selbstausleihe.png",
     "Erwartetes und tatsächliches Ergebnis: INSERT wird vom Trigger abgelehnt."),

    ("Bonus: Negativtest 2 (Tutor-Feedback Punkt 1)",
     """CREATE OR REPLACE FUNCTION fn_check_bewertung_nur_abgeschlossen()
RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT status FROM ausleihvorgang
      WHERE ausleihvorgang_id = NEW.ausleihvorgang_id) <> 'zurueckgegeben' THEN
    RAISE EXCEPTION 'Bewertung nur fuer abgeschlossene Ausleihvorgaenge
                      moeglich (ausleihvorgang_id=%).', NEW.ausleihvorgang_id;
  END IF;
  RETURN NEW;
END; $$ LANGUAGE plpgsql;""",
     "-- Testfall: Bewertung fuer einen noch aktiven Ausleihvorgang (id=12)\nINSERT INTO bewertung (ausleihvorgang_id, sternebewertung, kommentar)\nVALUES (12, 5, 'Sollte scheitern, da Ausleihvorgang 12 noch aktiv ist');",
     "negativtest_bewertung.png",
     "Setzt Tutor-Feedback direkt technisch um: Bewertung nur nach abgeschlossener Ausleihe."),
]

for name, ddl, test, shot, note in bonus:
    story.append(Paragraph(name, styles["h1"]))
    left_col = [
        Paragraph("SQL", styles["label"]),
        code_block(ddl),
        Paragraph("Testfall", styles["label"]),
        code_block(test),
        Paragraph(note, styles["small"]),
    ]
    right_col = [slide_image(os.path.join(SHOT_DIR, shot), 13.5 * cm, 10.5 * cm)]
    grid = Table([[left_col, right_col]], colWidths=[15.5 * cm, 13.5 * cm])
    grid.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(Spacer(1, 4))
    story.append(grid)
    story.append(PageBreak())

# ---------------- Zusammenfassung (mind. 0,5 Seiten) ----------------
story.append(Paragraph("Kurze Zusammenfassung der Implementierung", styles["h1"]))
story.append(Spacer(1, 8))
summary_text = """
Das Datenbankschema der Buchtausch-App wurde in PostgreSQL 16 umgesetzt und besteht aus 14 Tabellen:
den 13 Entitäten aus dem ER-Modell der Konzeptionsphase sowie der Verbindungstabelle buch_autor zur
Auflösung der N:M-Beziehung zwischen Buch und Autor:in. Beide Ternärbeziehungen aus Phase 1
(AUSLEIHT und ANGEBOTEN_ALS) wurden als eigene Tabellen mit Surrogatschlüssel umgesetzt
(ausleihvorgang, angebot). Das ist eine Standardtechnik, wenn eine Beziehung selbst wieder referenziert
werden muss, wie es das Tutor-Feedback zur Bewertung erforderte.<br/><br/>

Alle drei Rückmeldungen aus dem Feedback zu Phase 1 wurden eingearbeitet: Die Bewertung ist jetzt
über einen UNIQUE-Fremdschlüssel an einen konkreten Ausleihvorgang gekoppelt statt direkt an Buch
und Benutzer:in, zusätzlich per Trigger abgesichert, dass nur abgeschlossene ("zurueckgegeben")
Ausleihvorgänge bewertet werden können. Die Beziehung zwischen Benutzer und Adresse wurde von 1:1
auf 1:N geändert, sodass mehrere Adressen je Person möglich sind. Und die geforderten Constraints
wurden konsequent implementiert: CHECK-Constraints auf Sternebewertung (1&ndash;5), auf positive
Leihdauer und auf die zeitliche Reihenfolge von Ausleih- und Zeitfenster-Daten, UNIQUE auf die
E-Mail-Adresse sowie ein zusätzlicher Trigger, der verhindert, dass Nutzende ihr eigenes Exemplar
ausleihen.<br/><br/>

Die Datenbank wurde mit insgesamt über 175 Dummy-Datensätzen befüllt (mindestens 10 pro Tabelle),
alle referenziell konsistent und alle Geschäftsregeln respektierend. Die räumliche Suchanforderung
("Bücher in meiner Nähe") wurde über eine Haversine-Distanzformel direkt in SQL umgesetzt, ganz ohne
zusätzliche Erweiterung wie PostGIS, und liefert nachweislich plausible, nach Entfernung sortierte
Ergebnisse. Zwei Negativtests belegen, dass die implementierten Trigger tatsächlich greifen und
fehlerhafte Eingaben zuverlässig zurückweisen.
"""
story.append(Paragraph(summary_text, styles["body"]))

doc = SimpleDocTemplate(
    OUT_PATH, pagesize=PAGE_SIZE,
    topMargin=1.2 * cm, bottomMargin=1.2 * cm, leftMargin=1.3 * cm, rightMargin=1.3 * cm,
    title="Data-Mart-Erstellung in SQL (DLBDSPBDM01_D) - Erarbeitungsphase",
)
doc.build(story)
print("written", OUT_PATH)
