"""
Fuehrt alle Testfaelle gegen die Datenbank aus (psql), prueft die Erwartung
(Ergebnis bzw. erwarteter Fehler), speichert die echte psql-Ausgabe in out/*.txt,
schreibt 03_testfaelle.sql und rendert die Ausgaben als Terminal-Screenshots.

Aufruf:  python3 run_tests.py [datenbankname]     (Standard: buchtausch_final)
"""
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "out")
SHOT_DIR = os.path.join(BASE, "..", "assets", "screenshots")
DB = sys.argv[1] if len(sys.argv) > 1 else "buchtausch_app"
PSQL = os.environ.get("PSQL") or shutil.which("psql") or "/opt/homebrew/opt/postgresql@16/bin/psql"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SHOT_DIR, exist_ok=True)

# (name, titel, sql, erwartet_fehler, geschaeftsregel/Absicherung)
POSITIV = [
    ("benutzer", "Benutzer", "SELECT benutzer_id, vorname, nachname, email, registrierdatum\nFROM benutzer ORDER BY benutzer_id LIMIT 5;"),
    ("adresse", "Adresse (1:N)", "SELECT b.vorname, b.nachname, a.stadt, a.ist_hauptadresse\nFROM adresse a JOIN benutzer b USING (benutzer_id)\nWHERE b.benutzer_id = 1 ORDER BY a.ist_hauptadresse DESC;"),
    ("verlag", "Verlag", "SELECT verlag_id, name, land FROM verlag ORDER BY name LIMIT 5;"),
    ("genre", "Genre", "SELECT genre_id, bezeichnung FROM genre ORDER BY genre_id LIMIT 8;"),
    ("sprache", "Sprache", "SELECT sprache_id, bezeichnung, iso_code FROM sprache ORDER BY bezeichnung LIMIT 5;"),
    ("buch", "Buch", "SELECT bu.titel, bu.erscheinungsjahr, g.bezeichnung AS genre, v.name AS verlag, s.bezeichnung AS sprache\nFROM buch bu JOIN genre g USING (genre_id) JOIN verlag v USING (verlag_id)\nJOIN sprache s USING (sprache_id) ORDER BY bu.titel LIMIT 5;"),
    ("autor", "Autor (N:M)", "SELECT bu.titel, string_agg(a.vorname || ' ' || a.nachname, ', ') AS autor_innen\nFROM buch bu JOIN buch_autor ba USING (buch_id) JOIN autor a USING (autor_id)\nGROUP BY bu.buch_id, bu.titel HAVING count(*) > 1 ORDER BY bu.titel;"),
    ("buch_autor", "Buch_Autor", "SELECT buch_id, autor_id FROM buch_autor ORDER BY buch_id LIMIT 6;"),
    ("exemplar", "Exemplar", "SELECT e.exemplar_id, bu.titel, be.vorname || ' ' || be.nachname AS besitzer_in,\n       e.zustand, e.max_leihdauer_tage\nFROM exemplar e JOIN buch bu USING (buch_id)\nJOIN benutzer be ON be.benutzer_id = e.besitzer_id ORDER BY e.exemplar_id LIMIT 5;"),
    ("abholort", "Abholort", "SELECT abholort_id, bezeichnung, stadt, breitengrad, laengengrad\nFROM abholort ORDER BY abholort_id LIMIT 5;"),
    ("zeitfenster", "Verfuegbarkeitszeitfenster", "SELECT zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit\nFROM verfuegbarkeitszeitfenster ORDER BY zeitfenster_id LIMIT 5;"),
    ("angebot", "Angebot", "SELECT an.angebot_id, bu.titel, ao.stadt, an.aktiv\nFROM angebot an JOIN exemplar e USING (exemplar_id) JOIN buch bu USING (buch_id)\nJOIN abholort ao USING (abholort_id) ORDER BY an.angebot_id LIMIT 6;"),
    ("ausleihvorgang", "Ausleihvorgang", "SELECT av.ausleihvorgang_id, bu.titel, en.vorname || ' ' || en.nachname AS entleiher_in,\n       av.ausleihdatum, av.status\nFROM ausleihvorgang av JOIN exemplar e USING (exemplar_id) JOIN buch bu USING (buch_id)\nJOIN benutzer en ON en.benutzer_id = av.entleiher_id\nORDER BY av.ausleihvorgang_id DESC LIMIT 6;"),
    ("bewertung", "Bewertung", "SELECT bu.titel, ROUND(AVG(bw.sternebewertung), 1) AS durchschnitt, count(*) AS anzahl\nFROM bewertung bw JOIN ausleihvorgang av USING (ausleihvorgang_id)\nJOIN exemplar e USING (exemplar_id) JOIN buch bu USING (buch_id)\nGROUP BY bu.buch_id, bu.titel ORDER BY durchschnitt DESC, bu.titel LIMIT 6;"),
    ("raeumliche_suche", "Raeumliche Suche (Berlin)", "SELECT DISTINCT bu.titel, ao.stadt,\n       ROUND((6371 * acos(cos(radians(52.520)) * cos(radians(ao.breitengrad)) *\n         cos(radians(ao.laengengrad) - radians(13.405)) +\n         sin(radians(52.520)) * sin(radians(ao.breitengrad))))::numeric, 1) AS entfernung_km\nFROM angebot a JOIN exemplar e USING (exemplar_id) JOIN buch bu USING (buch_id)\nJOIN abholort ao USING (abholort_id) WHERE a.aktiv\nORDER BY entfernung_km, bu.titel LIMIT 5;"),
    ("konsistenz", "Konsistenzpruefung (erwartet: 0 Verstoesse)",
     "SELECT 'mehrere offene Ausleihen je Exemplar' AS regel, count(*) AS verstoesse FROM (\n  SELECT exemplar_id FROM ausleihvorgang WHERE status IN ('aktiv','ueberfaellig')\n  GROUP BY exemplar_id HAVING count(*) > 1) x\nUNION ALL SELECT 'Leihdauer ueber max_leihdauer_tage', count(*)\n  FROM ausleihvorgang av JOIN exemplar e USING (exemplar_id)\n  WHERE av.geplantes_rueckgabedatum - av.ausleihdatum > e.max_leihdauer_tage\nUNION ALL SELECT 'Zeitfenster gehoert nicht zum Besitzer', count(*)\n  FROM ausleihvorgang av JOIN exemplar e USING (exemplar_id)\n  JOIN verfuegbarkeitszeitfenster z USING (zeitfenster_id) WHERE z.benutzer_id <> e.besitzer_id\nUNION ALL SELECT 'Bewertung ohne zurueckgegebene Ausleihe', count(*)\n  FROM bewertung b JOIN ausleihvorgang av USING (ausleihvorgang_id)\n  WHERE av.status <> 'zurueckgegeben';"),
]

# Negativtests: (name, titel, regel, absicherung, sql). Alle muessen mit ERROR scheitern.
NEGATIV = [
    ("neg_selbstausleihe", "Selbst-Ausleihe", "Eigenes Exemplar nicht ausleihbar", "Trigger",
     "INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)\nVALUES (1, 1, 1, '2026-10-28', '2026-11-04');"),
    ("neg_bewertung_aktiv", "Bewertung vor Abschluss", "Nur abgeschlossene Ausleihen bewertbar", "Trigger",
     "INSERT INTO bewertung (ausleihvorgang_id, sternebewertung, kommentar)\nVALUES (28, 5, 'Ausleihe 28 ist noch aktiv');"),
    ("neg_doppelte_ausleihe", "Doppelte Ausleihe", "Ein Exemplar nicht mehrfach gleichzeitig offen", "Partieller UNIQUE-Index",
     "INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)\nVALUES (24, 1, 24, '2026-10-28', '2026-11-05');"),
    ("neg_leihdauer", "Max. Leihdauer ueberschritten", "Geplante Dauer <= max_leihdauer_tage", "Trigger",
     "INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)\nVALUES (5, 1, 5, '2026-10-28', '2026-11-28');"),
    ("neg_koordinaten", "Ungueltige Koordinaten", "Breitengrad -90..90, Laengengrad -180..180", "CHECK-Constraint",
     "INSERT INTO abholort (benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad)\nVALUES (1, 'Testort', 'Weg 1', '10115', 'Berlin', 95.0, 13.4);"),
    ("neg_fremdes_zeitfenster", "Zeitfenster eines anderen Besitzers", "Zeitfenster gehoert dem Besitzer des Exemplars", "Trigger",
     "INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)\nVALUES (6, 1, 2, '2026-10-28', '2026-11-04');"),
    ("neg_kein_angebot", "Zeitfenster nicht als Angebot eingerichtet", "Ausleihe nur ueber ein angebotenes Zeitfenster", "Trigger",
     "INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)\nVALUES (7, 1, 31, '2026-10-28', '2026-11-04');"),
    ("neg_angebot_fremder_abholort", "Angebot mit fremdem Abholort", "Abholort/Zeitfenster gehoeren dem Besitzer", "Trigger",
     "INSERT INTO angebot (exemplar_id, abholort_id, zeitfenster_id)\nVALUES (8, 9, 8);"),
    ("neg_status_zurueck", "Bewertete Ausleihe wieder aktiv", "Bewertete Ausleihe bleibt abgeschlossen", "Trigger",
     "UPDATE ausleihvorgang SET status = 'aktiv', tatsaechliches_rueckgabedatum = NULL\nWHERE ausleihvorgang_id = 1;"),
    ("neg_status_ohne_datum", "zurueckgegeben ohne Rueckgabedatum", "status 'zurueckgegeben' <=> Rueckgabedatum vorhanden", "CHECK-Constraint",
     "UPDATE ausleihvorgang SET status = 'zurueckgegeben'\nWHERE ausleihvorgang_id = 28;"),
    ("neg_sterne", "Sternebewertung 6", "Sterne 1 bis 5", "CHECK-Constraint",
     "INSERT INTO bewertung (ausleihvorgang_id, sternebewertung, erstellt_am)\nVALUES (21, 6, '2026-10-28');"),
    ("neg_email", "Doppelte E-Mail-Adresse", "E-Mail eindeutig", "UNIQUE-Constraint",
     "INSERT INTO benutzer (vorname, nachname, email)\nVALUES ('Test', 'Person', 'lena.vogt@example.com');"),
    ("neg_zeitfenster_reihenfolge", "Zeitfenster Ende vor Beginn", "endzeit > startzeit", "CHECK-Constraint",
     "INSERT INTO verfuegbarkeitszeitfenster (benutzer_id, wochentag, startzeit, endzeit)\nVALUES (1, 'Montag', '12:00', '10:00');"),
    ("neg_erscheinungsjahr", "Erscheinungsjahr in der Zukunft", "Erscheinungsjahr nicht in der Zukunft (zeitabhaengig)", "Trigger (statt CHECK)",
     "INSERT INTO buch (titel, erscheinungsjahr, sprache_id)\nVALUES ('Zukunftsroman', 2090, 1);"),
    ("neg_besitzerwechsel", "Besitzerwechsel eines Exemplars", "besitzer_id unveraenderlich", "Trigger",
     "UPDATE exemplar SET besitzer_id = 2 WHERE exemplar_id = 1;"),
    ("neg_hauptadresse", "Zweite Hauptadresse", "Hoechstens eine Hauptadresse je Person", "Partieller UNIQUE-Index",
     "INSERT INTO adresse (benutzer_id, strasse, hausnummer, plz, stadt, ist_hauptadresse)\nVALUES (1, 'Testweg', '1', '10115', 'Berlin', TRUE);"),
    ("neg_leihdauer_null", "Leihdauer 0 Tage", "max_leihdauer_tage zwischen 1 und 365", "CHECK-Constraint",
     "INSERT INTO exemplar (buch_id, besitzer_id, zustand, max_leihdauer_tage)\nVALUES (1, 1, 'gut', 0);"),
    ("neg_doppeltes_angebot", "Doppeltes Angebot", "Gleiche Kombination Exemplar/Abholort/Zeitfenster nur einmal", "UNIQUE-Constraint",
     "INSERT INTO angebot (exemplar_id, abholort_id, zeitfenster_id)\nVALUES (1, 1, 1);"),
    ("neg_rueckgabe_vor_ausleihe", "Rueckgabedatum vor Ausleihdatum", "geplantes Rueckgabedatum nach Ausleihdatum", "CHECK-Constraint",
     "INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)\nVALUES (9, 1, 9, '2026-10-28', '2026-10-20');"),
    ("neg_doppelte_bewertung", "Zweite Bewertung derselben Ausleihe", "Hoechstens eine Bewertung je Ausleihvorgang", "UNIQUE-Constraint",
     "INSERT INTO bewertung (ausleihvorgang_id, sternebewertung)\nVALUES (1, 4);"),
    ("neg_fremdschluessel", "Nicht existierendes Buch", "Referenzielle Integritaet", "FOREIGN KEY",
     "INSERT INTO exemplar (buch_id, besitzer_id, zustand, max_leihdauer_tage)\nVALUES (9999, 1, 'gut', 14);"),
]


def run(sql, negative):
    stmt = f"BEGIN; {sql} ROLLBACK;" if negative else sql
    r = subprocess.run([PSQL, "-q", "-d", DB, "-c", stmt], capture_output=True, text=True)
    return (r.stdout + r.stderr).rstrip("\n")


font_path = "/System/Library/Fonts/Monaco.ttf" if os.path.exists("/System/Library/Fonts/Monaco.ttf") else "/System/Library/Fonts/Menlo.ttc"
FONT = ImageFont.truetype(font_path, 22)
TBFONT = ImageFont.truetype(font_path, 16)


def render(name, title, sql, output):
    lines = []
    sl = sql.split("\n")
    for k, l in enumerate(sl):
        lines.append(("buchtausch_app=# " if k == 0 else "buchtausch_app-# ") + l)
    lines.append("")
    lines += output.split("\n") if output else ["(keine Ausgabe)"]
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    w = max(d.textbbox((0, 0), l, font=FONT)[2] for l in lines)
    lh, pad, tb = 30, 28, 44
    img = Image.new("RGB", (w + 2 * pad, tb + len(lines) * lh + 2 * pad), (30, 30, 32))
    dr = ImageDraw.Draw(img)
    dr.rectangle([0, 0, img.width, tb], fill=(58, 58, 60))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        dr.ellipse([14 + i * 22, tb // 2 - 7, 28 + i * 22, tb // 2 + 7], fill=c)
    t = f"psql - {DB} - {title}"
    tw = dr.textbbox((0, 0), t, font=TBFONT)[2]
    dr.text(((img.width - tw) / 2, tb // 2 - 9), t, font=TBFONT, fill=(200, 200, 200))
    y = tb + pad
    n_sql = len(sl)
    for k, l in enumerate(lines):
        col = (130, 200, 255) if k < n_sql else ((255, 140, 130) if l.startswith("ERROR") or l.startswith("FEHLER") else (223, 225, 226))
        dr.text((pad, y), l, font=FONT, fill=col)
        y += lh
    img.save(os.path.join(SHOT_DIR, name + ".png"))


def main():
    fehler = []
    sqlfile = ["-- ============================================================",
               "-- Phase 3: Testfaelle (16 positive Abfragen + 21 Negativtests)",
               "-- Negativtests sind jeweils in BEGIN ... ROLLBACK gekapselt und muessen",
               "-- mit einem ERROR scheitern; es werden keine Daten veraendert.",
               "-- ============================================================\n",
               "-- ===== A) Positive Testfaelle =====\n"]
    for name, title, sql in POSITIV:
        out = run(sql, False)
        if "ERROR" in out or "FEHLER" in out:
            fehler.append((name, "unerwarteter Fehler", out))
        open(os.path.join(OUT_DIR, name + ".txt"), "w", encoding="utf-8").write(out + "\n")
        render(name, title, sql, out)
        sqlfile.append(f"-- {title}\n{sql}\n")
    sqlfile.append("-- ===== B) Negativtests (jeder Befehl muss mit ERROR scheitern) =====\n")
    for name, title, regel, schutz, sql in NEGATIV:
        out = run(sql, True)
        if "ERROR" not in out and "FEHLER" not in out:
            fehler.append((name, "Negativtest wurde NICHT abgelehnt", out))
        open(os.path.join(OUT_DIR, name + ".txt"), "w", encoding="utf-8").write(out + "\n")
        render(name, title, sql, out)
        sqlfile.append(f"-- {title} (Regel: {regel}; abgesichert durch: {schutz})\nBEGIN;\n{sql}\nROLLBACK;\n")
    open(os.path.join(BASE, "03_testfaelle.sql"), "w", encoding="utf-8").write("\n".join(sqlfile))
    print(f"{len(POSITIV)} positive Tests, {len(NEGATIV)} Negativtests ausgefuehrt gegen '{DB}'.")
    if fehler:
        for f in fehler:
            print("FEHLER:", f)
        sys.exit(1)
    print("Alle Erwartungen erfuellt.")


if __name__ == "__main__":
    main()
