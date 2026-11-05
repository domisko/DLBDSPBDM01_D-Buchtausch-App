"""
Generiert 02_dummy_data.sql: konsistente, referenziell korrekte Dummy-Daten
fuer die Buchtausch-App (>= 10 Zeilen je Tabelle, respektiert alle
CHECK-Constraints und Trigger aus 01_schema.sql).
"""
import datetime

out = []


def sql(stmt):
    out.append(stmt)


sql("-- ============================================================")
sql("-- Data-Mart-Erstellung in SQL (DLBDSPBDM01_D) - Buchtausch-App")
sql("-- Phase 2: Dummy-Daten (>= 10 Zeilen je Tabelle)")
sql("-- Generiert mit generate_dummy_data.py, danach mit psql eingespielt.")
sql("-- ============================================================\n")

# ---------------------------------------------------------------
# Benutzer (12)
# ---------------------------------------------------------------
benutzer = [
    ("Lena", "Vogt", "lena.vogt@example.com", "0151-1000001", "2025-01-10"),
    ("Karsten", "Brandt", "karsten.brandt@example.com", "0151-1000002", "2025-01-12"),
    ("Mira", "Falk", "mira.falk@example.com", "0151-1000003", "2025-01-15"),
    ("Jonas", "Hoffmann", "jonas.hoffmann@example.com", "0151-1000004", "2025-01-18"),
    ("Selin", "Aydin", "selin.aydin@example.com", "0151-1000005", "2025-01-20"),
    ("Paul", "Krause", "paul.krause@example.com", "0151-1000006", "2025-01-22"),
    ("Anna", "Schreiber", "anna.schreiber@example.com", "0151-1000007", "2025-01-25"),
    ("Tom", "Weidner", "tom.weidner@example.com", "0151-1000008", "2025-02-01"),
    ("Nora", "Klemm", "nora.klemm@example.com", "0151-1000009", "2025-02-03"),
    ("Felix", "Bergmann", "felix.bergmann@example.com", "0151-1000010", "2025-02-05"),
    ("Ines", "Wagner", "ines.wagner@example.com", "0151-1000011", "2025-02-08"),
    ("David", "Schuster", "david.schuster@example.com", "0151-1000012", "2025-02-10"),
]
sql("-- Benutzer")
for i, (v, n, e, t, d) in enumerate(benutzer, start=1):
    sql(f"INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES "
        f"({i}, '{v}', '{n}', '{e}', '{t}', '{d}');")
sql("SELECT setval('benutzer_benutzer_id_seq', 12);\n")

# ---------------------------------------------------------------
# Adresse (12 Hauptadressen + 2 Zweitadressen = 14) -> zeigt 1:N
# ---------------------------------------------------------------
staedte = [
    ("Musterstr. 1", "10", "10115", "Berlin", 52.532, 13.384),
    ("Bahnhofstr. 22", "22", "20095", "Hamburg", 53.552, 9.994),
    ("Marienplatz 3", "3", "80331", "München", 48.137, 11.576),
    ("Domstr. 14", "14", "50667", "Köln", 50.941, 6.958),
    ("Zeil 9", "9", "60313", "Frankfurt am Main", 50.114, 8.682),
    ("Königstr. 55", "55", "70173", "Stuttgart", 48.777, 9.180),
    ("Prager Str. 4", "4", "01069", "Dresden", 51.038, 13.732),
    ("Leipziger Str. 30", "30", "04109", "Leipzig", 51.339, 12.373),
    ("Kröpcke 1", "1", "30159", "Hannover", 52.373, 9.738),
    ("Sternschanze 7", "7", "20357", "Hamburg", 53.564, 9.963),
    ("Kaiserstr. 12", "12", "76133", "Karlsruhe", 49.009, 8.404),
    ("Rheinstr. 8", "8", "55116", "Mainz", 49.999, 8.271),
]
sql("-- Adresse")
adresse_id = 1
for i in range(1, 13):
    s, h, p, c, lat, lng = staedte[i - 1]
    sql(f"INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES "
        f"({adresse_id}, {i}, '{s}', '{h}', '{p}', '{c}', {lat}, {lng}, TRUE);")
    adresse_id += 1
# zwei Zweitadressen (Nutzende 1 und 4 haben einen Zweitwohnsitz)
zusatz = [(1, "Ferienweg 2", "2", "83512", "Wasserburg am Inn", 48.058, 12.232),
          (4, "Uferpromenade 5", "5", "88131", "Lindau", 47.546, 9.684)]
for uid, s, h, p, c, lat, lng in zusatz:
    sql(f"INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES "
        f"({adresse_id}, {uid}, '{s}', '{h}', '{p}', '{c}', {lat}, {lng}, FALSE);")
    adresse_id += 1
sql(f"SELECT setval('adresse_adresse_id_seq', {adresse_id - 1});\n")

# ---------------------------------------------------------------
# Verlag (10), Genre (10), Sprache (10)
# ---------------------------------------------------------------
verlage = ["Rowohlt Verlag", "S. Fischer Verlag", "dtv", "Suhrkamp Verlag", "Diogenes Verlag",
           "Piper Verlag", "Heyne Verlag", "Klett-Cotta", "btb Verlag", "Kiepenheuer & Witsch"]
sql("-- Verlag")
for i, name in enumerate(verlage, start=1):
    land = "Schweiz" if name == "Diogenes Verlag" else "Deutschland"
    sql(f"INSERT INTO verlag (verlag_id, name, land) VALUES ({i}, '{name}', '{land}');")
sql(f"SELECT setval('verlag_verlag_id_seq', {len(verlage)});\n")

genres = ["Roman", "Krimi", "Fantasy", "Sachbuch", "Biografie",
          "Kinderbuch", "Lyrik", "Thriller", "Science-Fiction", "Kochbuch"]
sql("-- Genre")
for i, name in enumerate(genres, start=1):
    sql(f"INSERT INTO genre (genre_id, bezeichnung) VALUES ({i}, '{name}');")
sql(f"SELECT setval('genre_genre_id_seq', {len(genres)});\n")

sprachen = [("Deutsch", "de"), ("Englisch", "en"), ("Französisch", "fr"), ("Spanisch", "es"),
            ("Italienisch", "it"), ("Niederländisch", "nl"), ("Polnisch", "pl"),
            ("Schwedisch", "sv"), ("Türkisch", "tr"), ("Portugiesisch", "pt")]
sql("-- Sprache")
for i, (name, code) in enumerate(sprachen, start=1):
    sql(f"INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES ({i}, '{name}', '{code}');")
sql(f"SELECT setval('sprache_sprache_id_seq', {len(sprachen)});\n")

# ---------------------------------------------------------------
# Autor (12), Buch (12), Buch_Autor (>=12, zwei Buecher mit 2 Autor:innen)
# ---------------------------------------------------------------
autoren = [
    ("Lea", "Winter"), ("Bruno", "Achterberg"), ("Carla", "Reimann"), ("Jens", "Dornbusch"),
    ("Sofie", "Lindqvist"), ("Milan", "Kovac"), ("Rebecca", "Thorn"), ("Elias", "Marquardt"),
    ("Nadine", "Fuchs"), ("Oskar", "Lehmann"), ("Yvonne", "Petri"), ("Hannes", "Rott"),
]
sql("-- Autor")
for i, (v, n) in enumerate(autoren, start=1):
    sql(f"INSERT INTO autor (autor_id, vorname, nachname) VALUES ({i}, '{v}', '{n}');")
sql(f"SELECT setval('autor_autor_id_seq', {len(autoren)});\n")

buecher = [
    ("Der Winterpfad", "978-3-000-00001-1", 2018, 1, 1, 1),
    ("Mord im Nebel", "978-3-000-00002-8", 2020, 2, 2, 1),
    ("Die Drachenkönigin", "978-3-000-00003-5", 2016, 3, 3, 1),
    ("Wege durch die Stille", "978-3-000-00004-2", 2021, 1, 4, 1),
    ("Der letzte Leuchtturm", "978-3-000-00005-9", 2014, 2, 5, 2),
    ("Sternenstaub", "978-3-000-00006-6", 2019, 9, 6, 1),
    ("Kurze Wege", "978-3-000-00007-3", 2022, 7, 7, 1),
    ("Die Uhrmacherin", "978-3-000-00008-0", 2017, 8, 8, 1),
    ("Salz und Meer", "978-3-000-00009-7", 2015, 1, 9, 3),
    ("Kleine Fluchten", "978-3-000-00010-3", 2023, 5, 10, 1),
    ("Der Gartenbriefkasten", "978-3-000-00011-0", 2013, 6, 3, 1),
    ("Nordlicht", "978-3-000-00012-7", 2020, 4, 5, 1),
]
sql("-- Buch (bibliografische Ausgabe)")
for i, (titel, isbn, jahr, genre_id, verlag_id, sprache_id) in enumerate(buecher, start=1):
    sql(f"INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES "
        f"({i}, '{titel}', '{isbn}', {jahr}, {genre_id}, {verlag_id}, {sprache_id});")
sql(f"SELECT setval('buch_buch_id_seq', {len(buecher)});\n")

buch_autor = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
              (11, 11), (12, 12), (3, 5), (9, 1)]  # zwei Buecher mit Co-Autor:in -> zeigt N:M
sql("-- Buch_Autor (Aufloesung Buch-Autor N:M)")
for buch_id, autor_id in buch_autor:
    sql(f"INSERT INTO buch_autor (buch_id, autor_id) VALUES ({buch_id}, {autor_id});")
sql("")

# ---------------------------------------------------------------
# Exemplar (14) - Besitzer:innen unter den 12 Benutzenden verteilt
# ---------------------------------------------------------------
zustaende = ["neu", "sehr gut", "gut", "gebraucht"]
exemplare = [
    (1, 1, "sehr gut", True, 21), (2, 2, "gut", False, 14), (3, 3, "neu", True, 28),
    (4, 4, "gebraucht", False, 10), (5, 5, "gut", True, 21), (6, 6, "sehr gut", False, 14),
    (7, 7, "neu", True, 21), (8, 8, "gut", True, 14), (9, 9, "sehr gut", False, 21),
    (10, 10, "gut", True, 30), (11, 11, "neu", False, 14), (12, 12, "sehr gut", True, 21),
    (1, 3, "gut", False, 14), (5, 7, "neu", True, 21),
]
sql("-- Exemplar")
for i, (buch_id, besitzer_id, zustand, versand, dauer) in enumerate(exemplare, start=1):
    sql(f"INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES "
        f"({i}, {buch_id}, {besitzer_id}, '{zustand}', {versand}, {dauer});")
sql(f"SELECT setval('exemplar_exemplar_id_seq', {len(exemplare)});\n")

# ---------------------------------------------------------------
# Abholort (12)
# ---------------------------------------------------------------
sql("-- Abholort")
abholorte = []
for i in range(1, 13):
    uid = ((i - 1) % 12) + 1
    s, h, p, c, lat, lng = staedte[uid - 1]
    bez = f"Treffpunkt {c}"
    abholorte.append((i, uid, bez, s, p, c, lat, lng))
    sql(f"INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES "
        f"({i}, {uid}, '{bez}', '{s}', '{p}', '{c}', {lat}, {lng});")
sql(f"SELECT setval('abholort_abholort_id_seq', {len(abholorte)});\n")

# ---------------------------------------------------------------
# Verfuegbarkeitszeitfenster (14)
# ---------------------------------------------------------------
wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
sql("-- Verfuegbarkeitszeitfenster")
zeitfenster = []
zf_id = 1
for uid in range(1, 13):
    tag = wochentage[(uid - 1) % 7]
    start = "17:00" if uid % 2 == 0 else "09:00"
    ende = "19:00" if uid % 2 == 0 else "11:00"
    zeitfenster.append((zf_id, uid, tag, start, ende))
    sql(f"INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES "
        f"({zf_id}, {uid}, '{tag}', '{start}', '{ende}');")
    zf_id += 1
# zwei zusaetzliche Zeitfenster fuer Nutzende 1 und 5 (mehrere Slots moeglich)
for uid, tag, start, ende in [(1, "Samstag", "10:00", "13:00"), (5, "Sonntag", "14:00", "16:00")]:
    zeitfenster.append((zf_id, uid, tag, start, ende))
    sql(f"INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES "
        f"({zf_id}, {uid}, '{tag}', '{start}', '{ende}');")
    zf_id += 1
sql(f"SELECT setval('verfuegbarkeitszeitfenster_zeitfenster_id_seq', {zf_id - 1});\n")


def zf_for(uid):
    for zid, u, *_ in zeitfenster:
        if u == uid:
            return zid
    raise ValueError(uid)


# ---------------------------------------------------------------
# Ausleihvorgang (14, davon >=10 zurueckgegeben) - entleiher != besitzer
# ---------------------------------------------------------------
exemplar_besitzer = {i: ex[1] for i, ex in enumerate(exemplare, start=1)}


def other_user(besitzer_id, offset):
    candidates = [u for u in range(1, 13) if u != besitzer_id]
    return candidates[offset % len(candidates)]


ausleihen = []
today = datetime.date(2026, 8, 23)
for i in range(1, 15):
    exemplar_id = ((i - 1) % 14) + 1
    besitzer = exemplar_besitzer[exemplar_id]
    entleiher = other_user(besitzer, i)
    zid = zf_for(besitzer)
    ausleihdatum = today - datetime.timedelta(days=30 - (i * 2))
    geplant = ausleihdatum + datetime.timedelta(days=14)
    if i <= 10:
        status = "zurueckgegeben"
        tatsaechlich = ausleihdatum + datetime.timedelta(days=10 + (i % 4))
    elif i == 11:
        status = "ueberfaellig"
        tatsaechlich = None
    else:
        status = "aktiv"
        tatsaechlich = None
    ausleihen.append((i, exemplar_id, entleiher, zid, ausleihdatum, geplant, tatsaechlich, status))

sql("-- Ausleihvorgang (reifizierte Ternaerbeziehung AUSLEIHT)")
for (i, exemplar_id, entleiher, zid, ad, gd, td, status) in ausleihen:
    td_sql = f"'{td.isoformat()}'" if td else "NULL"
    sql(f"INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, "
        f"ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES "
        f"({i}, {exemplar_id}, {entleiher}, {zid}, '{ad.isoformat()}', '{gd.isoformat()}', {td_sql}, '{status}');")
sql(f"SELECT setval('ausleihvorgang_ausleihvorgang_id_seq', {len(ausleihen)});\n")

# ---------------------------------------------------------------
# Angebot (14) - gueltige Kombination aus Exemplar x Abholort x Zeitfenster
# des jeweiligen Besitzers/der Besitzerin
# ---------------------------------------------------------------
sql("-- Angebot (reifizierte Ternaerbeziehung ANGEBOTEN_ALS)")
angebote = []
for i in range(1, 15):
    exemplar_id = ((i - 1) % 14) + 1
    besitzer = exemplar_besitzer[exemplar_id]
    abholort_id = besitzer  # abholort_id folgt 1:1 der Reihenfolge der Nutzenden (siehe oben)
    zid = zf_for(besitzer)
    aktiv = "TRUE" if i % 7 != 0 else "FALSE"
    angebote.append((i, exemplar_id, abholort_id, zid))
    sql(f"INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES "
        f"({i}, {exemplar_id}, {abholort_id}, {zid}, {aktiv});")
sql(f"SELECT setval('angebot_angebot_id_seq', {len(angebote)});\n")

# ---------------------------------------------------------------
# Bewertung (10) - nur fuer status = 'zurueckgegeben'
# ---------------------------------------------------------------
kommentare = [
    "Tolles Buch, top Zustand!", "Wie beschrieben, gerne wieder.",
    "Etwas verspätete Abholung, sonst top.", "Sehr freundlicher Austausch.",
    "Buch war stärker abgenutzt als angegeben.", "Perfekt fürs Wochenende.",
    "Kommunikation war unkompliziert.", "Würde ich weiterempfehlen.",
    "Abholung hat gut geklappt.", "Inhaltlich super, Einband leicht beschädigt.",
]
sql("-- Bewertung (nur fuer abgeschlossene Ausleihvorgaenge, Feedback Phase 1)")
sterne = [5, 4, 5, 4, 3, 5, 4, 5, 4, 3]
for idx, (i, *_rest) in enumerate(ausleihen[:10]):
    sql(f"INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES "
        f"({idx + 1}, {i}, {sterne[idx]}, '{kommentare[idx]}');")
sql(f"SELECT setval('bewertung_bewertung_id_seq', 10);\n")

with open("02_dummy_data.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print("written 02_dummy_data.sql,", len(out), "lines")
