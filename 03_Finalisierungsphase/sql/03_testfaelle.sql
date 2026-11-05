-- ============================================================
-- Phase 3: Testfaelle (16 positive Abfragen + 21 Negativtests)
-- Negativtests sind jeweils in BEGIN ... ROLLBACK gekapselt und muessen
-- mit einem ERROR scheitern; es werden keine Daten veraendert.
-- ============================================================

-- ===== A) Positive Testfaelle =====

-- Benutzer
SELECT benutzer_id, vorname, nachname, email, registrierdatum
FROM benutzer ORDER BY benutzer_id LIMIT 5;

-- Adresse (1:N)
SELECT b.vorname, b.nachname, a.stadt, a.ist_hauptadresse
FROM adresse a JOIN benutzer b USING (benutzer_id)
WHERE b.benutzer_id = 1 ORDER BY a.ist_hauptadresse DESC;

-- Verlag
SELECT verlag_id, name, land FROM verlag ORDER BY name LIMIT 5;

-- Genre
SELECT genre_id, bezeichnung FROM genre ORDER BY genre_id LIMIT 8;

-- Sprache
SELECT sprache_id, bezeichnung, iso_code FROM sprache ORDER BY bezeichnung LIMIT 5;

-- Buch
SELECT bu.titel, bu.erscheinungsjahr, g.bezeichnung AS genre, v.name AS verlag, s.bezeichnung AS sprache
FROM buch bu JOIN genre g USING (genre_id) JOIN verlag v USING (verlag_id)
JOIN sprache s USING (sprache_id) ORDER BY bu.titel LIMIT 5;

-- Autor (N:M)
SELECT bu.titel, string_agg(a.vorname || ' ' || a.nachname, ', ') AS autor_innen
FROM buch bu JOIN buch_autor ba USING (buch_id) JOIN autor a USING (autor_id)
GROUP BY bu.buch_id, bu.titel HAVING count(*) > 1 ORDER BY bu.titel;

-- Buch_Autor
SELECT buch_id, autor_id FROM buch_autor ORDER BY buch_id LIMIT 6;

-- Exemplar
SELECT e.exemplar_id, bu.titel, be.vorname || ' ' || be.nachname AS besitzer_in,
       e.zustand, e.max_leihdauer_tage
FROM exemplar e JOIN buch bu USING (buch_id)
JOIN benutzer be ON be.benutzer_id = e.besitzer_id ORDER BY e.exemplar_id LIMIT 5;

-- Abholort
SELECT abholort_id, bezeichnung, stadt, breitengrad, laengengrad
FROM abholort ORDER BY abholort_id LIMIT 5;

-- Verfuegbarkeitszeitfenster
SELECT zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit
FROM verfuegbarkeitszeitfenster ORDER BY zeitfenster_id LIMIT 5;

-- Angebot
SELECT an.angebot_id, bu.titel, ao.stadt, an.aktiv
FROM angebot an JOIN exemplar e USING (exemplar_id) JOIN buch bu USING (buch_id)
JOIN abholort ao USING (abholort_id) ORDER BY an.angebot_id LIMIT 6;

-- Ausleihvorgang
SELECT av.ausleihvorgang_id, bu.titel, en.vorname || ' ' || en.nachname AS entleiher_in,
       av.ausleihdatum, av.status
FROM ausleihvorgang av JOIN exemplar e USING (exemplar_id) JOIN buch bu USING (buch_id)
JOIN benutzer en ON en.benutzer_id = av.entleiher_id
ORDER BY av.ausleihvorgang_id DESC LIMIT 6;

-- Bewertung
SELECT bu.titel, ROUND(AVG(bw.sternebewertung), 1) AS durchschnitt, count(*) AS anzahl
FROM bewertung bw JOIN ausleihvorgang av USING (ausleihvorgang_id)
JOIN exemplar e USING (exemplar_id) JOIN buch bu USING (buch_id)
GROUP BY bu.buch_id, bu.titel ORDER BY durchschnitt DESC, bu.titel LIMIT 6;

-- Raeumliche Suche (Berlin)
SELECT DISTINCT bu.titel, ao.stadt,
       ROUND((6371 * acos(cos(radians(52.520)) * cos(radians(ao.breitengrad)) *
         cos(radians(ao.laengengrad) - radians(13.405)) +
         sin(radians(52.520)) * sin(radians(ao.breitengrad))))::numeric, 1) AS entfernung_km
FROM angebot a JOIN exemplar e USING (exemplar_id) JOIN buch bu USING (buch_id)
JOIN abholort ao USING (abholort_id) WHERE a.aktiv
ORDER BY entfernung_km, bu.titel LIMIT 5;

-- Konsistenzpruefung (erwartet: 0 Verstoesse)
SELECT 'mehrere offene Ausleihen je Exemplar' AS regel, count(*) AS verstoesse FROM (
  SELECT exemplar_id FROM ausleihvorgang WHERE status IN ('aktiv','ueberfaellig')
  GROUP BY exemplar_id HAVING count(*) > 1) x
UNION ALL SELECT 'Leihdauer ueber max_leihdauer_tage', count(*)
  FROM ausleihvorgang av JOIN exemplar e USING (exemplar_id)
  WHERE av.geplantes_rueckgabedatum - av.ausleihdatum > e.max_leihdauer_tage
UNION ALL SELECT 'Zeitfenster gehoert nicht zum Besitzer', count(*)
  FROM ausleihvorgang av JOIN exemplar e USING (exemplar_id)
  JOIN verfuegbarkeitszeitfenster z USING (zeitfenster_id) WHERE z.benutzer_id <> e.besitzer_id
UNION ALL SELECT 'Bewertung ohne zurueckgegebene Ausleihe', count(*)
  FROM bewertung b JOIN ausleihvorgang av USING (ausleihvorgang_id)
  WHERE av.status <> 'zurueckgegeben';

-- ===== B) Negativtests (jeder Befehl muss mit ERROR scheitern) =====

-- Selbst-Ausleihe (Regel: Eigenes Exemplar nicht ausleihbar; abgesichert durch: Trigger)
BEGIN;
INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)
VALUES (1, 1, 1, '2026-10-28', '2026-11-04');
ROLLBACK;

-- Bewertung vor Abschluss (Regel: Nur abgeschlossene Ausleihen bewertbar; abgesichert durch: Trigger)
BEGIN;
INSERT INTO bewertung (ausleihvorgang_id, sternebewertung, kommentar)
VALUES (28, 5, 'Ausleihe 28 ist noch aktiv');
ROLLBACK;

-- Doppelte Ausleihe (Regel: Ein Exemplar nicht mehrfach gleichzeitig offen; abgesichert durch: Partieller UNIQUE-Index)
BEGIN;
INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)
VALUES (24, 1, 24, '2026-10-28', '2026-11-05');
ROLLBACK;

-- Max. Leihdauer ueberschritten (Regel: Geplante Dauer <= max_leihdauer_tage; abgesichert durch: Trigger)
BEGIN;
INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)
VALUES (5, 1, 5, '2026-10-28', '2026-11-28');
ROLLBACK;

-- Ungueltige Koordinaten (Regel: Breitengrad -90..90, Laengengrad -180..180; abgesichert durch: CHECK-Constraint)
BEGIN;
INSERT INTO abholort (benutzer_id, bezeichnung, strasse, plz, stadt, breitengrad, laengengrad)
VALUES (1, 'Testort', 'Weg 1', '10115', 'Berlin', 95.0, 13.4);
ROLLBACK;

-- Zeitfenster eines anderen Besitzers (Regel: Zeitfenster gehoert dem Besitzer des Exemplars; abgesichert durch: Trigger)
BEGIN;
INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)
VALUES (6, 1, 2, '2026-10-28', '2026-11-04');
ROLLBACK;

-- Zeitfenster nicht als Angebot eingerichtet (Regel: Ausleihe nur ueber ein angebotenes Zeitfenster; abgesichert durch: Trigger)
BEGIN;
INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)
VALUES (7, 1, 31, '2026-10-28', '2026-11-04');
ROLLBACK;

-- Angebot mit fremdem Abholort (Regel: Abholort/Zeitfenster gehoeren dem Besitzer; abgesichert durch: Trigger)
BEGIN;
INSERT INTO angebot (exemplar_id, abholort_id, zeitfenster_id)
VALUES (8, 9, 8);
ROLLBACK;

-- Bewertete Ausleihe wieder aktiv (Regel: Bewertete Ausleihe bleibt abgeschlossen; abgesichert durch: Trigger)
BEGIN;
UPDATE ausleihvorgang SET status = 'aktiv', tatsaechliches_rueckgabedatum = NULL
WHERE ausleihvorgang_id = 1;
ROLLBACK;

-- zurueckgegeben ohne Rueckgabedatum (Regel: status 'zurueckgegeben' <=> Rueckgabedatum vorhanden; abgesichert durch: CHECK-Constraint)
BEGIN;
UPDATE ausleihvorgang SET status = 'zurueckgegeben'
WHERE ausleihvorgang_id = 28;
ROLLBACK;

-- Sternebewertung 6 (Regel: Sterne 1 bis 5; abgesichert durch: CHECK-Constraint)
BEGIN;
INSERT INTO bewertung (ausleihvorgang_id, sternebewertung, erstellt_am)
VALUES (21, 6, '2026-10-28');
ROLLBACK;

-- Doppelte E-Mail-Adresse (Regel: E-Mail eindeutig; abgesichert durch: UNIQUE-Constraint)
BEGIN;
INSERT INTO benutzer (vorname, nachname, email)
VALUES ('Test', 'Person', 'lena.vogt@example.com');
ROLLBACK;

-- Zeitfenster Ende vor Beginn (Regel: endzeit > startzeit; abgesichert durch: CHECK-Constraint)
BEGIN;
INSERT INTO verfuegbarkeitszeitfenster (benutzer_id, wochentag, startzeit, endzeit)
VALUES (1, 'Montag', '12:00', '10:00');
ROLLBACK;

-- Erscheinungsjahr in der Zukunft (Regel: Erscheinungsjahr nicht in der Zukunft (zeitabhaengig); abgesichert durch: Trigger (statt CHECK))
BEGIN;
INSERT INTO buch (titel, erscheinungsjahr, sprache_id)
VALUES ('Zukunftsroman', 2090, 1);
ROLLBACK;

-- Besitzerwechsel eines Exemplars (Regel: besitzer_id unveraenderlich; abgesichert durch: Trigger)
BEGIN;
UPDATE exemplar SET besitzer_id = 2 WHERE exemplar_id = 1;
ROLLBACK;

-- Zweite Hauptadresse (Regel: Hoechstens eine Hauptadresse je Person; abgesichert durch: Partieller UNIQUE-Index)
BEGIN;
INSERT INTO adresse (benutzer_id, strasse, hausnummer, plz, stadt, ist_hauptadresse)
VALUES (1, 'Testweg', '1', '10115', 'Berlin', TRUE);
ROLLBACK;

-- Leihdauer 0 Tage (Regel: max_leihdauer_tage zwischen 1 und 365; abgesichert durch: CHECK-Constraint)
BEGIN;
INSERT INTO exemplar (buch_id, besitzer_id, zustand, max_leihdauer_tage)
VALUES (1, 1, 'gut', 0);
ROLLBACK;

-- Doppeltes Angebot (Regel: Gleiche Kombination Exemplar/Abholort/Zeitfenster nur einmal; abgesichert durch: UNIQUE-Constraint)
BEGIN;
INSERT INTO angebot (exemplar_id, abholort_id, zeitfenster_id)
VALUES (1, 1, 1);
ROLLBACK;

-- Rueckgabedatum vor Ausleihdatum (Regel: geplantes Rueckgabedatum nach Ausleihdatum; abgesichert durch: CHECK-Constraint)
BEGIN;
INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)
VALUES (9, 1, 9, '2026-10-28', '2026-10-20');
ROLLBACK;

-- Zweite Bewertung derselben Ausleihe (Regel: Hoechstens eine Bewertung je Ausleihvorgang; abgesichert durch: UNIQUE-Constraint)
BEGIN;
INSERT INTO bewertung (ausleihvorgang_id, sternebewertung)
VALUES (1, 4);
ROLLBACK;

-- Nicht existierendes Buch (Regel: Referenzielle Integritaet; abgesichert durch: FOREIGN KEY)
BEGIN;
INSERT INTO exemplar (buch_id, besitzer_id, zustand, max_leihdauer_tage)
VALUES (9999, 1, 'gut', 14);
ROLLBACK;
