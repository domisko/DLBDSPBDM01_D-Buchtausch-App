"""
Erzeugt 02_dummy_data.sql (Phase 3): >= 280 Datensaetze, alle Tabellen >= 10 Zeilen.

Alle Geschaeftsregeln aus 01_schema.sql werden hier bereits per assert geprueft,
damit die erzeugten Daten garantiert gueltig sind (Selbst-Ausleihe, max. Leihdauer,
Zeitfenster gehoert zum Besitzer und ist als Angebot eingerichtet, nie zwei
offene Ausleihen je Exemplar, Bewertung nur fuer zurueckgegebene Ausleihen).
"""
import datetime
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "02_dummy_data.sql")
lines = []


def q(s):
    return "'" + str(s).replace("'", "''") + "'"


def emit(s=""):
    lines.append(s)


def seq(table, n, col=None):
    col = col or f"{table}_id"
    emit(f"SELECT setval(pg_get_serial_sequence('{table}', '{col}'), {n});")


emit("-- ============================================================")
emit("-- Data-Mart-Erstellung in SQL (DLBDSPBDM01_D) - Buchtausch-App")
emit("-- Phase 3: Dummy-Daten (>= 280 Datensaetze, alle Tabellen >= 10 Zeilen)")
emit("-- Erzeugt mit generate_dummy_data.py (Regeln werden dort per assert geprueft).")
emit("-- ============================================================")
emit()

# ---------------------------------------------------------------- Benutzer (24)
vornamen = ["Lena", "Karsten", "Mira", "Jonas", "Selin", "Paul", "Anna", "Tom", "Nora", "Felix", "Ines", "David",
            "Clara", "Marek", "Yasmin", "Lukas", "Hanna", "Emre", "Sophie", "Ben", "Leyla", "Max", "Greta", "Tobias"]
nachnamen = ["Vogt", "Brandt", "Falk", "Hoffmann", "Aydin", "Krause", "Schreiber", "Weidner", "Klemm", "Bergmann",
             "Wagner", "Schuster", "Neumann", "Kowalski", "Demir", "Richter", "Pohl", "Yilmaz", "Lorenz", "Hartmann",
             "Sommer", "Jung", "Albrecht", "Stein"]
N_USER = 24
emit("-- Benutzer")
for i in range(1, N_USER + 1):
    v, n = vornamen[i - 1], nachnamen[i - 1]
    email = f"{v.lower()}.{n.lower()}@example.com"
    reg = datetime.date(2025, 1, 1) + datetime.timedelta(days=i * 3)
    emit(f"INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES "
         f"({i}, {q(v)}, {q(n)}, {q(email)}, {q('0151-20000%02d' % i)}, {q(reg)});")
seq("benutzer", N_USER)
emit()

# ---------------------------------------------------------------- Adresse (24 + 6 = 30)
staedte = [
    ("Berlin", "10115", 52.520, 13.405), ("Hamburg", "20095", 53.551, 9.994), ("München", "80331", 48.137, 11.576),
    ("Köln", "50667", 50.938, 6.960), ("Frankfurt am Main", "60313", 50.110, 8.682), ("Stuttgart", "70173", 48.775, 9.182),
    ("Düsseldorf", "40213", 51.227, 6.773), ("Dresden", "01067", 51.050, 13.738), ("Leipzig", "04109", 51.340, 12.375),
    ("Hannover", "30159", 52.375, 9.732), ("Nürnberg", "90402", 49.452, 11.077), ("Bremen", "28195", 53.079, 8.802),
    ("Essen", "45127", 51.455, 7.012), ("Dortmund", "44135", 51.514, 7.468), ("Karlsruhe", "76133", 49.007, 8.404),
    ("Mainz", "55116", 49.993, 8.247), ("Freiburg", "79098", 47.999, 7.842), ("Kiel", "24103", 54.323, 10.123),
    ("Rostock", "18055", 54.092, 12.099), ("Erfurt", "99084", 50.978, 11.029), ("Münster", "48143", 51.961, 7.629),
    ("Bonn", "53111", 50.737, 7.098), ("Augsburg", "86150", 48.371, 10.898), ("Lübeck", "23552", 53.866, 10.687),
]
strassen = ["Bahnhofstraße", "Hauptstraße", "Gartenweg", "Lindenallee", "Schulstraße", "Marktplatz", "Ringstraße", "Kirchgasse"]
emit("-- Adresse (jede Person eine Hauptadresse, 6 Personen zusaetzlich eine Zweitadresse: 1:N)")
aid = 0
for i in range(1, N_USER + 1):
    stadt, plz, lat, lng = staedte[i - 1]
    aid += 1
    emit(f"INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES "
         f"({aid}, {i}, {q(strassen[i % len(strassen)])}, {q(str(i + 2))}, {q(plz)}, {q(stadt)}, {lat}, {lng}, TRUE);")
zweit = [(1, "Ferienweg", "2", "83512", "Wasserburg am Inn", 48.058, 12.232),
         (4, "Uferpromenade", "5", "88131", "Lindau", 47.546, 9.684),
         (7, "Seestraße", "11", "17454", "Zinnowitz", 54.082, 13.916),
         (10, "Bergblick", "3", "82467", "Garmisch-Partenkirchen", 47.492, 11.095),
         (13, "Dorfstraße", "8", "25980", "Westerland", 54.908, 8.307),
         (16, "Moselufer", "14", "54470", "Bernkastel-Kues", 49.917, 7.068)]
for uid, s, h, plz, stadt, lat, lng in zweit:
    aid += 1
    emit(f"INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES "
         f"({aid}, {uid}, {q(s)}, {q(h)}, {q(plz)}, {q(stadt)}, {lat}, {lng}, FALSE);")
seq("adresse", aid)
emit()

# ---------------------------------------------------------------- Lookups (je 12)
verlage = [("Rowohlt Verlag", "Deutschland"), ("S. Fischer Verlag", "Deutschland"), ("dtv", "Deutschland"),
           ("Suhrkamp Verlag", "Deutschland"), ("Diogenes Verlag", "Schweiz"), ("Piper Verlag", "Deutschland"),
           ("Heyne Verlag", "Deutschland"), ("Klett-Cotta", "Deutschland"), ("btb Verlag", "Deutschland"),
           ("Kiepenheuer & Witsch", "Deutschland"), ("Aufbau Verlag", "Deutschland"), ("Carl Hanser Verlag", "Deutschland")]
genres = ["Roman", "Krimi", "Fantasy", "Sachbuch", "Biografie", "Kinderbuch", "Lyrik", "Thriller",
          "Science-Fiction", "Kochbuch", "Reisebericht", "Graphic Novel"]
sprachen = [("Deutsch", "de"), ("Englisch", "en"), ("Französisch", "fr"), ("Spanisch", "es"), ("Italienisch", "it"),
            ("Niederländisch", "nl"), ("Polnisch", "pl"), ("Schwedisch", "sv"), ("Türkisch", "tr"),
            ("Portugiesisch", "pt"), ("Russisch", "ru"), ("Griechisch", "el")]
emit("-- Verlag")
for i, (n, land) in enumerate(verlage, 1):
    emit(f"INSERT INTO verlag (verlag_id, name, land) VALUES ({i}, {q(n)}, {q(land)});")
seq("verlag", len(verlage))
emit("-- Genre")
for i, n in enumerate(genres, 1):
    emit(f"INSERT INTO genre (genre_id, bezeichnung) VALUES ({i}, {q(n)});")
seq("genre", len(genres))
emit("-- Sprache")
for i, (n, c) in enumerate(sprachen, 1):
    emit(f"INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES ({i}, {q(n)}, {q(c)});")
seq("sprache", len(sprachen))
emit()

# ---------------------------------------------------------------- Autor (20), Buch (24), Buch_Autor (30)
autoren = [("Lea", "Winter"), ("Bruno", "Achterberg"), ("Carla", "Reimann"), ("Jens", "Dornbusch"), ("Sofie", "Lindqvist"),
           ("Milan", "Kovac"), ("Rebecca", "Thorn"), ("Elias", "Marquardt"), ("Nadine", "Fuchs"), ("Oskar", "Lehmann"),
           ("Yvonne", "Petri"), ("Hannes", "Rott"), ("Ida", "Brenner"), ("Konrad", "Salm"), ("Mathilda", "Eck"),
           ("Viktor", "Ruppert"), ("Amelie", "Dorn"), ("Samuel", "Kern"), ("Lotte", "Haas"), ("Erik", "Voss")]
emit("-- Autor")
for i, (v, n) in enumerate(autoren, 1):
    emit(f"INSERT INTO autor (autor_id, vorname, nachname) VALUES ({i}, {q(v)}, {q(n)});")
seq("autor", len(autoren))

buecher = [  # titel, jahr, genre, verlag, sprache
    ("Der Winterpfad", 2018, 1, 1, 1), ("Mord im Nebel", 2020, 2, 2, 1), ("Die Drachenkönigin", 2016, 3, 3, 1),
    ("Wege durch die Stille", 2021, 1, 4, 1), ("Der letzte Leuchtturm", 2014, 2, 5, 2), ("Sternenstaub", 2019, 9, 6, 1),
    ("Kurze Wege", 2022, 7, 7, 1), ("Die Uhrmacherin", 2017, 8, 8, 1), ("Salz und Meer", 2015, 1, 9, 3),
    ("Kleine Fluchten", 2023, 5, 10, 1), ("Der Gartenbriefkasten", 2013, 6, 3, 1), ("Nordlicht", 2020, 4, 5, 1),
    ("Schatten über Lübeck", 2012, 2, 11, 1), ("Die Kartografin", 2018, 1, 12, 1), ("Mondfinsternis", 2021, 9, 7, 2),
    ("Backen mit Brot", 2022, 10, 6, 1), ("Reise nach Samarkand", 2011, 11, 8, 1), ("Der Glasbläser", 2019, 1, 1, 1),
    ("Pixel und Papier", 2023, 12, 10, 1), ("Heimat im Sturm", 2016, 5, 2, 1), ("Das Echo der Berge", 2024, 8, 9, 1),
    ("Zwischen den Zeilen", 2015, 7, 4, 1), ("Kleiner Drache, großer Mut", 2020, 6, 3, 1), ("Die letzte Fähre", 2017, 2, 12, 5),
]
emit("-- Buch")
for i, (t, y, g, v, s) in enumerate(buecher, 1):
    isbn = f"978-3-100-{i:05d}-{i % 10}"
    emit(f"INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES "
         f"({i}, {q(t)}, {q(isbn)}, {y}, {g}, {v}, {s});")
seq("buch", len(buecher))

buch_autor = [(i, ((i - 1) % len(autoren)) + 1) for i in range(1, len(buecher) + 1)]
buch_autor += [(3, 5), (9, 1), (14, 7), (18, 12), (21, 3), (24, 16)]  # Co-Autor:innen -> N:M
emit("-- Buch_Autor (Aufloesung der N:M-Beziehung)")
for b, a in buch_autor:
    emit(f"INSERT INTO buch_autor (buch_id, autor_id) VALUES ({b}, {a});")
emit()

# ---------------------------------------------------------------- Exemplar (32)
zustaende = ["neu", "sehr gut", "gut", "gebraucht"]
max_tage_pool = [10, 14, 21, 28, 30]
exemplare = []  # (id, buch, besitzer, zustand, versand, max_tage, eingestellt)
for i in range(1, 33):
    buch = ((i - 1) % len(buecher)) + 1
    besitzer = ((i - 1) % N_USER) + 1 if i <= 24 else ((i * 7) % N_USER) + 1
    exemplare.append((i, buch, besitzer, zustaende[i % 4], i % 3 != 0, max_tage_pool[i % 5],
                      datetime.date(2025, 3, 1) + datetime.timedelta(days=i * 5)))
emit("-- Exemplar")
for (i, b, o, z, vs, mt, d) in exemplare:
    emit(f"INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage, eingestellt_am) VALUES "
         f"({i}, {b}, {o}, {q(z)}, {'TRUE' if vs else 'FALSE'}, {mt}, {q(d)});")
seq("exemplar", len(exemplare))
besitzer_von = {e[0]: e[2] for e in exemplare}
max_von = {e[0]: e[5] for e in exemplare}
emit()

# ---------------------------------------------------------------- Abholort (24, einer je Person)
emit("-- Abholort")
for i in range(1, N_USER + 1):
    stadt, plz, lat, lng = staedte[i - 1]
    emit(f"INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES "
         f"({i}, {i}, {q('Treffpunkt ' + stadt)}, {q('Marktplatz ' + str(i))}, {q(plz)}, {q(stadt)}, {lat + 0.004:.3f}, {lng + 0.004:.3f});")
seq("abholort", N_USER)
emit()

# ---------------------------------------------------------------- Zeitfenster (24 + 12 = 36)
tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
zeitfenster = []  # (id, user, tag, start, ende)
for u in range(1, N_USER + 1):
    start = "17:00" if u % 2 == 0 else "09:00"
    ende = "19:00" if u % 2 == 0 else "11:00"
    zeitfenster.append((u, u, tage[(u - 1) % 7], start, ende))
for k, u in enumerate(range(1, 13), start=1):
    zeitfenster.append((N_USER + k, u, tage[(u + 4) % 7], "10:00", "13:00"))
emit("-- Verfuegbarkeitszeitfenster (12 Personen mit zwei Zeitfenstern)")
for (i, u, t, s, e) in zeitfenster:
    emit(f"INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES "
         f"({i}, {u}, {q(t)}, {q(s)}, {q(e)});")
seq("verfuegbarkeitszeitfenster", len(zeitfenster), "zeitfenster_id")
zf_besitzer = {z[0]: z[1] for z in zeitfenster}
emit()

# ---------------------------------------------------------------- Angebot (32 + 4 = 36)
angebote = []  # (id, exemplar, abholort, zeitfenster, aktiv)
for (i, b, o, *_r) in exemplare:
    angebote.append((i, i, o, o, i % 9 != 0))  # abholort_id == zeitfenster_id == Besitzer-ID
for k in range(1, 5):  # zweites Zeitfenster fuer Exemplare 1..4
    ex = k
    o = besitzer_von[ex]
    angebote.append((32 + k, ex, o, N_USER + o, True))
emit("-- Angebot (reifizierte Ternaerbeziehung ANGEBOTEN_ALS)")
for (i, ex, ab, zf, akt) in angebote:
    assert zf_besitzer[zf] == besitzer_von[ex] and ab == besitzer_von[ex]
    emit(f"INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES "
         f"({i}, {ex}, {ab}, {zf}, {'TRUE' if akt else 'FALSE'});")
seq("angebot", len(angebote))
zf_je_exemplar = {}
for (_i, ex, _ab, zf, _a) in angebote:
    zf_je_exemplar.setdefault(ex, []).append(zf)
emit()

# ---------------------------------------------------------------- Ausleihvorgang (30)
# 22 zurueckgegeben (Ex. 1..20, danach 1 und 2 erneut), 3 ueberfaellig (Ex. 21..23), 5 aktiv (Ex. 24..28)
loans = []  # (id, exemplar, entleiher, zeitfenster, ausleih, geplant, tatsaechlich|None, status)
heute = datetime.date(2026, 10, 28)
exemplar_plan = list(range(1, 21)) + [1, 2] + [21, 22, 23] + [24, 25, 26, 27, 28]
for idx, ex in enumerate(exemplar_plan, start=1):
    owner = besitzer_von[ex]
    entleiher = ((owner + idx * 3) % N_USER) + 1
    if entleiher == owner:
        entleiher = (entleiher % N_USER) + 1
    zf = zf_je_exemplar[ex][idx % len(zf_je_exemplar[ex])]
    dauer = min(14, max_von[ex])
    if idx <= 20:
        ausleih = datetime.date(2026, 3, 1) + datetime.timedelta(days=6 * idx)
        status, tats = "zurueckgegeben", ausleih + datetime.timedelta(days=dauer - 2)
    elif idx <= 22:
        ausleih = datetime.date(2026, 8, 10) + datetime.timedelta(days=4 * (idx - 20))
        status, tats = "zurueckgegeben", ausleih + datetime.timedelta(days=dauer - 3)
    elif idx <= 25:
        ausleih = datetime.date(2026, 9, 14) + datetime.timedelta(days=idx - 22)
        status, tats = "ueberfaellig", None
    else:
        ausleih = datetime.date(2026, 10, 20) + datetime.timedelta(days=idx - 26)
        status, tats = "aktiv", None
    geplant = ausleih + datetime.timedelta(days=dauer)
    # Regeln pruefen
    assert entleiher != owner
    assert (geplant - ausleih).days <= max_von[ex]
    assert zf_besitzer[zf] == owner and zf in zf_je_exemplar[ex]
    assert (status == "zurueckgegeben") == (tats is not None)
    if status == "ueberfaellig":
        assert geplant < heute
    loans.append((idx, ex, entleiher, zf, ausleih, geplant, tats, status))
offen = [l[1] for l in loans if l[7] in ("aktiv", "ueberfaellig")]
assert len(offen) == len(set(offen)), "zwei offene Ausleihen fuer dasselbe Exemplar"

emit("-- Ausleihvorgang (reifizierte Ternaerbeziehung AUSLEIHT)")
for (i, ex, en, zf, a, g, t, s) in loans:
    emit(f"INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, "
         f"geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES "
         f"({i}, {ex}, {en}, {zf}, {q(a)}, {q(g)}, {q(t) if t else 'NULL'}, {q(s)});")
seq("ausleihvorgang", len(loans))
emit()

# ---------------------------------------------------------------- Bewertung (20)
kommentare = [
    "Tolles Buch, top Zustand!", "Wie beschrieben, gerne wieder.", "Etwas verspätete Abholung, sonst top.",
    "Sehr freundlicher Austausch.", "Buch war stärker abgenutzt als angegeben.", "Perfekt fürs Wochenende.",
    "Kommunikation war unkompliziert.", "Würde ich weiterempfehlen.", "Abholung hat gut geklappt.",
    "Inhaltlich super, Einband leicht beschädigt.", "Spannend bis zur letzten Seite.", "Pünktliche Übergabe.",
    "Genau das, was ich gesucht habe.", "Zustand gut, Inhalt mittelmäßig.", "Sehr nette Person, unkomplizierte Rückgabe.",
    "Hat mir sehr gefallen.", "Leider einige Notizen im Buch.", "Schnelle Abwicklung.", "Gerne wieder.", "Top!",
]
sterne = [5, 4, 5, 4, 3, 5, 4, 5, 4, 3, 5, 5, 4, 3, 5, 4, 3, 4, 5, 5]
emit("-- Bewertung (nur fuer zurueckgegebene Ausleihvorgaenge, Feedback Phase 1)")
rueck = [l for l in loans if l[7] == "zurueckgegeben"]
for k in range(20):
    lid, _ex, _en, _zf, _a, _g, tats, s = rueck[k]
    erstellt = tats + datetime.timedelta(days=1 + k % 3)
    assert erstellt <= heute
    emit(f"INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar, erstellt_am) VALUES "
         f"({k + 1}, {lid}, {sterne[k]}, {q(kommentare[k])}, {q(erstellt)});")
seq("bewertung", 20)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

gesamt = (N_USER + aid + len(verlage) + len(genres) + len(sprachen) + len(buecher) + len(autoren) + len(buch_autor)
          + len(exemplare) + N_USER + len(zeitfenster) + len(angebote) + len(loans) + 20)
print(f"geschrieben: {OUT}\nDatensaetze gesamt (erwartet): {gesamt}")
