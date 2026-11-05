-- ============================================================
-- Data-Mart-Erstellung in SQL (DLBDSPBDM01_D) - Buchtausch-App
-- Phase 2: Dummy-Daten (>= 10 Zeilen je Tabelle)
-- Generiert mit generate_dummy_data.py, danach mit psql eingespielt.
-- ============================================================

-- Benutzer
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (1, 'Lena', 'Vogt', 'lena.vogt@example.com', '0151-1000001', '2025-01-10');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (2, 'Karsten', 'Brandt', 'karsten.brandt@example.com', '0151-1000002', '2025-01-12');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (3, 'Mira', 'Falk', 'mira.falk@example.com', '0151-1000003', '2025-01-15');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (4, 'Jonas', 'Hoffmann', 'jonas.hoffmann@example.com', '0151-1000004', '2025-01-18');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (5, 'Selin', 'Aydin', 'selin.aydin@example.com', '0151-1000005', '2025-01-20');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (6, 'Paul', 'Krause', 'paul.krause@example.com', '0151-1000006', '2025-01-22');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (7, 'Anna', 'Schreiber', 'anna.schreiber@example.com', '0151-1000007', '2025-01-25');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (8, 'Tom', 'Weidner', 'tom.weidner@example.com', '0151-1000008', '2025-02-01');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (9, 'Nora', 'Klemm', 'nora.klemm@example.com', '0151-1000009', '2025-02-03');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (10, 'Felix', 'Bergmann', 'felix.bergmann@example.com', '0151-1000010', '2025-02-05');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (11, 'Ines', 'Wagner', 'ines.wagner@example.com', '0151-1000011', '2025-02-08');
INSERT INTO benutzer (benutzer_id, vorname, nachname, email, telefon, registrierdatum) VALUES (12, 'David', 'Schuster', 'david.schuster@example.com', '0151-1000012', '2025-02-10');
SELECT setval('benutzer_benutzer_id_seq', 12);

-- Adresse
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (1, 1, 'Musterstr. 1', '10', '10115', 'Berlin', 52.532, 13.384, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (2, 2, 'Bahnhofstr. 22', '22', '20095', 'Hamburg', 53.552, 9.994, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (3, 3, 'Marienplatz 3', '3', '80331', 'München', 48.137, 11.576, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (4, 4, 'Domstr. 14', '14', '50667', 'Köln', 50.941, 6.958, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (5, 5, 'Zeil 9', '9', '60313', 'Frankfurt am Main', 50.114, 8.682, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (6, 6, 'Königstr. 55', '55', '70173', 'Stuttgart', 48.777, 9.18, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (7, 7, 'Prager Str. 4', '4', '01069', 'Dresden', 51.038, 13.732, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (8, 8, 'Leipziger Str. 30', '30', '04109', 'Leipzig', 51.339, 12.373, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (9, 9, 'Kröpcke 1', '1', '30159', 'Hannover', 52.373, 9.738, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (10, 10, 'Sternschanze 7', '7', '20357', 'Hamburg', 53.564, 9.963, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (11, 11, 'Kaiserstr. 12', '12', '76133', 'Karlsruhe', 49.009, 8.404, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (12, 12, 'Rheinstr. 8', '8', '55116', 'Mainz', 49.999, 8.271, TRUE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (13, 1, 'Ferienweg 2', '2', '83512', 'Wasserburg am Inn', 48.058, 12.232, FALSE);
INSERT INTO adresse (adresse_id, benutzer_id, strasse, hausnummer, plz, stadt, breitengrad, laengengrad, ist_hauptadresse) VALUES (14, 4, 'Uferpromenade 5', '5', '88131', 'Lindau', 47.546, 9.684, FALSE);
SELECT setval('adresse_adresse_id_seq', 14);

-- Verlag
INSERT INTO verlag (verlag_id, name, land) VALUES (1, 'Rowohlt Verlag', 'Deutschland');
INSERT INTO verlag (verlag_id, name, land) VALUES (2, 'S. Fischer Verlag', 'Deutschland');
INSERT INTO verlag (verlag_id, name, land) VALUES (3, 'dtv', 'Deutschland');
INSERT INTO verlag (verlag_id, name, land) VALUES (4, 'Suhrkamp Verlag', 'Deutschland');
INSERT INTO verlag (verlag_id, name, land) VALUES (5, 'Diogenes Verlag', 'Schweiz');
INSERT INTO verlag (verlag_id, name, land) VALUES (6, 'Piper Verlag', 'Deutschland');
INSERT INTO verlag (verlag_id, name, land) VALUES (7, 'Heyne Verlag', 'Deutschland');
INSERT INTO verlag (verlag_id, name, land) VALUES (8, 'Klett-Cotta', 'Deutschland');
INSERT INTO verlag (verlag_id, name, land) VALUES (9, 'btb Verlag', 'Deutschland');
INSERT INTO verlag (verlag_id, name, land) VALUES (10, 'Kiepenheuer & Witsch', 'Deutschland');
SELECT setval('verlag_verlag_id_seq', 10);

-- Genre
INSERT INTO genre (genre_id, bezeichnung) VALUES (1, 'Roman');
INSERT INTO genre (genre_id, bezeichnung) VALUES (2, 'Krimi');
INSERT INTO genre (genre_id, bezeichnung) VALUES (3, 'Fantasy');
INSERT INTO genre (genre_id, bezeichnung) VALUES (4, 'Sachbuch');
INSERT INTO genre (genre_id, bezeichnung) VALUES (5, 'Biografie');
INSERT INTO genre (genre_id, bezeichnung) VALUES (6, 'Kinderbuch');
INSERT INTO genre (genre_id, bezeichnung) VALUES (7, 'Lyrik');
INSERT INTO genre (genre_id, bezeichnung) VALUES (8, 'Thriller');
INSERT INTO genre (genre_id, bezeichnung) VALUES (9, 'Science-Fiction');
INSERT INTO genre (genre_id, bezeichnung) VALUES (10, 'Kochbuch');
SELECT setval('genre_genre_id_seq', 10);

-- Sprache
INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES (1, 'Deutsch', 'de');
INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES (2, 'Englisch', 'en');
INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES (3, 'Französisch', 'fr');
INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES (4, 'Spanisch', 'es');
INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES (5, 'Italienisch', 'it');
INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES (6, 'Niederländisch', 'nl');
INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES (7, 'Polnisch', 'pl');
INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES (8, 'Schwedisch', 'sv');
INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES (9, 'Türkisch', 'tr');
INSERT INTO sprache (sprache_id, bezeichnung, iso_code) VALUES (10, 'Portugiesisch', 'pt');
SELECT setval('sprache_sprache_id_seq', 10);

-- Autor
INSERT INTO autor (autor_id, vorname, nachname) VALUES (1, 'Lea', 'Winter');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (2, 'Bruno', 'Achterberg');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (3, 'Carla', 'Reimann');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (4, 'Jens', 'Dornbusch');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (5, 'Sofie', 'Lindqvist');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (6, 'Milan', 'Kovac');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (7, 'Rebecca', 'Thorn');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (8, 'Elias', 'Marquardt');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (9, 'Nadine', 'Fuchs');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (10, 'Oskar', 'Lehmann');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (11, 'Yvonne', 'Petri');
INSERT INTO autor (autor_id, vorname, nachname) VALUES (12, 'Hannes', 'Rott');
SELECT setval('autor_autor_id_seq', 12);

-- Buch (bibliografische Ausgabe)
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (1, 'Der Winterpfad', '978-3-000-00001-1', 2018, 1, 1, 1);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (2, 'Mord im Nebel', '978-3-000-00002-8', 2020, 2, 2, 1);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (3, 'Die Drachenkönigin', '978-3-000-00003-5', 2016, 3, 3, 1);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (4, 'Wege durch die Stille', '978-3-000-00004-2', 2021, 1, 4, 1);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (5, 'Der letzte Leuchtturm', '978-3-000-00005-9', 2014, 2, 5, 2);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (6, 'Sternenstaub', '978-3-000-00006-6', 2019, 9, 6, 1);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (7, 'Kurze Wege', '978-3-000-00007-3', 2022, 7, 7, 1);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (8, 'Die Uhrmacherin', '978-3-000-00008-0', 2017, 8, 8, 1);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (9, 'Salz und Meer', '978-3-000-00009-7', 2015, 1, 9, 3);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (10, 'Kleine Fluchten', '978-3-000-00010-3', 2023, 5, 10, 1);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (11, 'Der Gartenbriefkasten', '978-3-000-00011-0', 2013, 6, 3, 1);
INSERT INTO buch (buch_id, titel, isbn, erscheinungsjahr, genre_id, verlag_id, sprache_id) VALUES (12, 'Nordlicht', '978-3-000-00012-7', 2020, 4, 5, 1);
SELECT setval('buch_buch_id_seq', 12);

-- Buch_Autor (Aufloesung Buch-Autor N:M)
INSERT INTO buch_autor (buch_id, autor_id) VALUES (1, 1);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (2, 2);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (3, 3);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (4, 4);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (5, 5);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (6, 6);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (7, 7);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (8, 8);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (9, 9);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (10, 10);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (11, 11);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (12, 12);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (3, 5);
INSERT INTO buch_autor (buch_id, autor_id) VALUES (9, 1);

-- Exemplar
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (1, 1, 1, 'sehr gut', True, 21);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (2, 2, 2, 'gut', False, 14);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (3, 3, 3, 'neu', True, 28);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (4, 4, 4, 'gebraucht', False, 10);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (5, 5, 5, 'gut', True, 21);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (6, 6, 6, 'sehr gut', False, 14);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (7, 7, 7, 'neu', True, 21);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (8, 8, 8, 'gut', True, 14);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (9, 9, 9, 'sehr gut', False, 21);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (10, 10, 10, 'gut', True, 30);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (11, 11, 11, 'neu', False, 14);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (12, 12, 12, 'sehr gut', True, 21);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (13, 1, 3, 'gut', False, 14);
INSERT INTO exemplar (exemplar_id, buch_id, besitzer_id, zustand, versand_moeglich, max_leihdauer_tage) VALUES (14, 5, 7, 'neu', True, 21);
SELECT setval('exemplar_exemplar_id_seq', 14);

-- Abholort
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (1, 1, 'Treffpunkt Berlin', 'Musterstr. 1', '10115', 'Berlin', 52.532, 13.384);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (2, 2, 'Treffpunkt Hamburg', 'Bahnhofstr. 22', '20095', 'Hamburg', 53.552, 9.994);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (3, 3, 'Treffpunkt München', 'Marienplatz 3', '80331', 'München', 48.137, 11.576);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (4, 4, 'Treffpunkt Köln', 'Domstr. 14', '50667', 'Köln', 50.941, 6.958);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (5, 5, 'Treffpunkt Frankfurt am Main', 'Zeil 9', '60313', 'Frankfurt am Main', 50.114, 8.682);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (6, 6, 'Treffpunkt Stuttgart', 'Königstr. 55', '70173', 'Stuttgart', 48.777, 9.18);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (7, 7, 'Treffpunkt Dresden', 'Prager Str. 4', '01069', 'Dresden', 51.038, 13.732);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (8, 8, 'Treffpunkt Leipzig', 'Leipziger Str. 30', '04109', 'Leipzig', 51.339, 12.373);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (9, 9, 'Treffpunkt Hannover', 'Kröpcke 1', '30159', 'Hannover', 52.373, 9.738);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (10, 10, 'Treffpunkt Hamburg', 'Sternschanze 7', '20357', 'Hamburg', 53.564, 9.963);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (11, 11, 'Treffpunkt Karlsruhe', 'Kaiserstr. 12', '76133', 'Karlsruhe', 49.009, 8.404);
INSERT INTO abholort (abholort_id, benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad) VALUES (12, 12, 'Treffpunkt Mainz', 'Rheinstr. 8', '55116', 'Mainz', 49.999, 8.271);
SELECT setval('abholort_abholort_id_seq', 12);

-- Verfuegbarkeitszeitfenster
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (1, 1, 'Montag', '09:00', '11:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (2, 2, 'Dienstag', '17:00', '19:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (3, 3, 'Mittwoch', '09:00', '11:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (4, 4, 'Donnerstag', '17:00', '19:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (5, 5, 'Freitag', '09:00', '11:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (6, 6, 'Samstag', '17:00', '19:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (7, 7, 'Sonntag', '09:00', '11:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (8, 8, 'Montag', '17:00', '19:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (9, 9, 'Dienstag', '09:00', '11:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (10, 10, 'Mittwoch', '17:00', '19:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (11, 11, 'Donnerstag', '09:00', '11:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (12, 12, 'Freitag', '17:00', '19:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (13, 1, 'Samstag', '10:00', '13:00');
INSERT INTO verfuegbarkeitszeitfenster (zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit) VALUES (14, 5, 'Sonntag', '14:00', '16:00');
SELECT setval('verfuegbarkeitszeitfenster_zeitfenster_id_seq', 14);

-- Ausleihvorgang (reifizierte Ternaerbeziehung AUSLEIHT)
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (1, 1, 3, 1, '2026-07-26', '2026-08-09', '2026-08-06', 'zurueckgegeben');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (2, 2, 4, 2, '2026-07-28', '2026-08-11', '2026-08-09', 'zurueckgegeben');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (3, 3, 5, 3, '2026-07-30', '2026-08-13', '2026-08-12', 'zurueckgegeben');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (4, 4, 6, 4, '2026-08-01', '2026-08-15', '2026-08-11', 'zurueckgegeben');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (5, 5, 7, 5, '2026-08-03', '2026-08-17', '2026-08-14', 'zurueckgegeben');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (6, 6, 8, 6, '2026-08-05', '2026-08-19', '2026-08-17', 'zurueckgegeben');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (7, 7, 9, 7, '2026-08-07', '2026-08-21', '2026-08-20', 'zurueckgegeben');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (8, 8, 10, 8, '2026-08-09', '2026-08-23', '2026-08-19', 'zurueckgegeben');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (9, 9, 11, 9, '2026-08-11', '2026-08-25', '2026-08-22', 'zurueckgegeben');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (10, 10, 12, 10, '2026-08-13', '2026-08-27', '2026-08-25', 'zurueckgegeben');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (11, 11, 1, 11, '2026-08-15', '2026-08-29', NULL, 'ueberfaellig');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (12, 12, 2, 12, '2026-08-17', '2026-08-31', NULL, 'aktiv');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (13, 13, 4, 3, '2026-08-19', '2026-09-02', NULL, 'aktiv');
INSERT INTO ausleihvorgang (ausleihvorgang_id, exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status) VALUES (14, 14, 4, 7, '2026-08-21', '2026-09-04', NULL, 'aktiv');
SELECT setval('ausleihvorgang_ausleihvorgang_id_seq', 14);

-- Angebot (reifizierte Ternaerbeziehung ANGEBOTEN_ALS)
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (1, 1, 1, 1, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (2, 2, 2, 2, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (3, 3, 3, 3, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (4, 4, 4, 4, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (5, 5, 5, 5, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (6, 6, 6, 6, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (7, 7, 7, 7, FALSE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (8, 8, 8, 8, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (9, 9, 9, 9, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (10, 10, 10, 10, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (11, 11, 11, 11, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (12, 12, 12, 12, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (13, 13, 3, 3, TRUE);
INSERT INTO angebot (angebot_id, exemplar_id, abholort_id, zeitfenster_id, aktiv) VALUES (14, 14, 7, 7, FALSE);
SELECT setval('angebot_angebot_id_seq', 14);

-- Bewertung (nur fuer abgeschlossene Ausleihvorgaenge, Feedback Phase 1)
INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES (1, 1, 5, 'Tolles Buch, top Zustand!');
INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES (2, 2, 4, 'Wie beschrieben, gerne wieder.');
INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES (3, 3, 5, 'Etwas verspätete Abholung, sonst top.');
INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES (4, 4, 4, 'Sehr freundlicher Austausch.');
INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES (5, 5, 3, 'Buch war stärker abgenutzt als angegeben.');
INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES (6, 6, 5, 'Perfekt fürs Wochenende.');
INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES (7, 7, 4, 'Kommunikation war unkompliziert.');
INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES (8, 8, 5, 'Würde ich weiterempfehlen.');
INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES (9, 9, 4, 'Abholung hat gut geklappt.');
INSERT INTO bewertung (bewertung_id, ausleihvorgang_id, sternebewertung, kommentar) VALUES (10, 10, 3, 'Inhaltlich super, Einband leicht beschädigt.');
SELECT setval('bewertung_bewertung_id_seq', 10);

