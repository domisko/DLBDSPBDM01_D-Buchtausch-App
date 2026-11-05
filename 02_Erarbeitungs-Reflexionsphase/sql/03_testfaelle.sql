-- ============================================================
-- Phase 2: Testfaelle - ein passender SELECT je Entitaet (+ Extras)
-- ============================================================

-- === Benutzer ===
SELECT benutzer_id, vorname, nachname, email, registrierdatum
FROM benutzer ORDER BY registrierdatum LIMIT 5;

-- === Adresse (zeigt 1:N nach Feedback Phase 1) ===
SELECT b.vorname, b.nachname, a.stadt, a.ist_hauptadresse
FROM adresse a JOIN benutzer b ON b.benutzer_id = a.benutzer_id
WHERE b.benutzer_id = 1
ORDER BY a.ist_hauptadresse DESC;

-- === Verlag ===
SELECT verlag_id, name, land FROM verlag ORDER BY name LIMIT 5;

-- === Genre ===
SELECT genre_id, bezeichnung FROM genre ORDER BY genre_id;

-- === Sprache ===
SELECT sprache_id, bezeichnung, iso_code FROM sprache ORDER BY bezeichnung LIMIT 5;

-- === Buch ===
SELECT bu.titel, bu.erscheinungsjahr, g.bezeichnung AS genre, v.name AS verlag, s.bezeichnung AS sprache
FROM buch bu
JOIN genre g ON g.genre_id = bu.genre_id
JOIN verlag v ON v.verlag_id = bu.verlag_id
JOIN sprache s ON s.sprache_id = bu.sprache_id
ORDER BY bu.titel LIMIT 5;

-- === Autor (N:M ueber Buch_Autor: Buecher mit mehreren Autor:innen) ===
SELECT bu.titel, string_agg(a.vorname || ' ' || a.nachname, ', ') AS autor_innen
FROM buch bu
JOIN buch_autor ba ON ba.buch_id = bu.buch_id
JOIN autor a ON a.autor_id = ba.autor_id
GROUP BY bu.buch_id, bu.titel
HAVING count(*) > 1;

-- === Buch_Autor (Verbindungstabelle direkt) ===
SELECT buch_id, autor_id FROM buch_autor ORDER BY buch_id LIMIT 6;

-- === Exemplar ===
SELECT e.exemplar_id, bu.titel, be.vorname || ' ' || be.nachname AS besitzer_in, e.zustand, e.max_leihdauer_tage
FROM exemplar e
JOIN buch bu ON bu.buch_id = e.buch_id
JOIN benutzer be ON be.benutzer_id = e.besitzer_id
ORDER BY e.exemplar_id LIMIT 5;

-- === Abholort ===
SELECT abholort_id, bezeichnung, stadt FROM abholort ORDER BY abholort_id LIMIT 5;

-- === Verfuegbarkeitszeitfenster ===
SELECT zeitfenster_id, benutzer_id, wochentag, startzeit, endzeit
FROM verfuegbarkeitszeitfenster ORDER BY zeitfenster_id LIMIT 5;

-- === Ausleihvorgang ===
SELECT av.ausleihvorgang_id, bu.titel, en.vorname || ' ' || en.nachname AS entleiher_in,
       av.ausleihdatum, av.status
FROM ausleihvorgang av
JOIN exemplar e ON e.exemplar_id = av.exemplar_id
JOIN buch bu ON bu.buch_id = e.buch_id
JOIN benutzer en ON en.benutzer_id = av.entleiher_id
ORDER BY av.ausleihvorgang_id LIMIT 6;

-- === Angebot ===
SELECT an.angebot_id, bu.titel, ao.stadt, an.aktiv
FROM angebot an
JOIN exemplar e ON e.exemplar_id = an.exemplar_id
JOIN buch bu ON bu.buch_id = e.buch_id
JOIN abholort ao ON ao.abholort_id = an.abholort_id
ORDER BY an.angebot_id LIMIT 6;

-- === Bewertung (Durchschnitt je Buch, ueber Ausleihvorgang->Exemplar->Buch) ===
SELECT bu.titel, ROUND(AVG(bw.sternebewertung), 1) AS durchschnitt, count(*) AS anzahl_bewertungen
FROM bewertung bw
JOIN ausleihvorgang av ON av.ausleihvorgang_id = bw.ausleihvorgang_id
JOIN exemplar e ON e.exemplar_id = av.exemplar_id
JOIN buch bu ON bu.buch_id = e.buch_id
GROUP BY bu.buch_id, bu.titel
ORDER BY durchschnitt DESC LIMIT 6;

-- === Bonus: raeumliche Suche "Buecher in meiner Naehe" (Referenz: Berlin) ===
SELECT bu.titel, ao.stadt, ao.bezeichnung,
       ROUND((6371 * acos(
           cos(radians(52.520)) * cos(radians(ao.breitengrad)) *
           cos(radians(ao.laengengrad) - radians(13.405)) +
           sin(radians(52.520)) * sin(radians(ao.breitengrad))
       ))::numeric, 1) AS entfernung_km
FROM angebot a
JOIN exemplar e ON e.exemplar_id = a.exemplar_id
JOIN buch bu ON bu.buch_id = e.buch_id
JOIN abholort ao ON ao.abholort_id = a.abholort_id
WHERE a.aktiv = TRUE
ORDER BY entfernung_km LIMIT 5;

-- === Negativtest 1: Selbst-Ausleihe wird durch Trigger verhindert ===
INSERT INTO ausleihvorgang (exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum)
VALUES (1, (SELECT besitzer_id FROM exemplar WHERE exemplar_id = 1), 1, CURRENT_DATE, CURRENT_DATE + 7);

-- === Negativtest 2: Bewertung ohne abgeschlossenen Ausleihvorgang wird verhindert ===
INSERT INTO bewertung (ausleihvorgang_id, sternebewertung, kommentar)
VALUES (12, 5, 'Sollte scheitern, da Ausleihvorgang 12 noch aktiv ist');
