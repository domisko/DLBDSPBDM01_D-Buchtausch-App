-- ============================================================
-- Data-Mart-Erstellung in SQL (DLBDSPBDM01_D) - Buchtausch-App
-- Phase 3 (Finalisierung): Schema (DDL), Version 2
-- DBMS: PostgreSQL 16
--
-- Aenderungen gegenueber Phase 2 (Tutor-Feedback):
--   1. erscheinungsjahr: CHECK nur noch mit festen Grenzen (kein CURRENT_DATE
--      in einem CHECK); die zeitabhaengige Pruefung ("nicht in der Zukunft")
--      liegt in einem Trigger, der zum Schreibzeitpunkt ausgewertet wird.
--   2. Doppelte Ausleihen: partieller UNIQUE-Index auf aktive/ueberfaellige.
--   3. Maximale Leihdauer: Trigger vergleicht geplante Dauer mit
--      exemplar.max_leihdauer_tage.
--   4. Zeitfenster/Angebot: Trigger stellen sicher, dass Abholort und
--      Zeitfenster dem Besitzer des Exemplars gehoeren und dass ein Ausleih-
--      vorgang nur ueber ein tatsaechlich angebotenes Zeitfenster entsteht.
--   5. Bewertungen: bewertete Ausleihen koennen nicht mehr auf einen
--      nicht abgeschlossenen Status zurueckgesetzt werden.
--   6. Datenintegritaet: CHECKs fuer Koordinaten, status = 'zurueckgegeben'
--      <=> tatsaechliches Rueckgabedatum vorhanden.
--
-- Reihenfolge: Lookup-Tabellen zuerst, dann Kernentitaeten, zuletzt die
-- reifizierten Ternaerbeziehungen Angebot und Ausleihvorgang sowie Bewertung.
-- ============================================================

DROP TABLE IF EXISTS bewertung CASCADE;
DROP TABLE IF EXISTS ausleihvorgang CASCADE;
DROP TABLE IF EXISTS angebot CASCADE;
DROP TABLE IF EXISTS verfuegbarkeitszeitfenster CASCADE;
DROP TABLE IF EXISTS abholort CASCADE;
DROP TABLE IF EXISTS exemplar CASCADE;
DROP TABLE IF EXISTS buch_autor CASCADE;
DROP TABLE IF EXISTS autor CASCADE;
DROP TABLE IF EXISTS buch CASCADE;
DROP TABLE IF EXISTS sprache CASCADE;
DROP TABLE IF EXISTS genre CASCADE;
DROP TABLE IF EXISTS verlag CASCADE;
DROP TABLE IF EXISTS adresse CASCADE;
DROP TABLE IF EXISTS benutzer CASCADE;

-- ------------------------------------------------------------
-- Generische Hilfsfunktion: Spalte darf nach dem Anlegen nicht
-- mehr geaendert werden (Argument: Spaltenname).
-- ------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_spalte_unveraenderlich() RETURNS TRIGGER AS $$
BEGIN
    IF to_jsonb(NEW) ->> TG_ARGV[0] IS DISTINCT FROM to_jsonb(OLD) ->> TG_ARGV[0] THEN
        RAISE EXCEPTION 'Spalte %.% ist unveraenderlich (Aenderung wuerde Zuordnungen von Angeboten/Ausleihen ungueltig machen).',
            TG_TABLE_NAME, TG_ARGV[0];
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ------------------------------------------------------------
-- 1. Benutzer
-- ------------------------------------------------------------
CREATE TABLE benutzer (
    benutzer_id      SERIAL PRIMARY KEY,
    vorname           VARCHAR(50)  NOT NULL,
    nachname          VARCHAR(50)  NOT NULL,
    email             VARCHAR(100) NOT NULL UNIQUE
                       CHECK (email LIKE '_%@_%._%'),
    telefon           VARCHAR(20),
    registrierdatum   DATE NOT NULL DEFAULT CURRENT_DATE
);

-- ------------------------------------------------------------
-- 2. Adresse (1:N zu Benutzer)
-- ------------------------------------------------------------
CREATE TABLE adresse (
    adresse_id        SERIAL PRIMARY KEY,
    benutzer_id        INTEGER NOT NULL REFERENCES benutzer(benutzer_id) ON DELETE CASCADE,
    strasse             VARCHAR(100) NOT NULL,
    hausnummer          VARCHAR(10)  NOT NULL,
    plz                 VARCHAR(10)  NOT NULL,
    stadt               VARCHAR(50)  NOT NULL,
    breitengrad         DECIMAL(9,6),
    laengengrad         DECIMAL(9,6),
    ist_hauptadresse    BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT chk_adresse_breitengrad CHECK (breitengrad BETWEEN -90 AND 90),
    CONSTRAINT chk_adresse_laengengrad CHECK (laengengrad BETWEEN -180 AND 180),
    CONSTRAINT chk_adresse_koordinaten_paar CHECK ((breitengrad IS NULL) = (laengengrad IS NULL))
);

-- Pro Benutzer:in hoechstens eine Hauptadresse.
CREATE UNIQUE INDEX ux_adresse_hauptadresse
    ON adresse (benutzer_id)
    WHERE ist_hauptadresse = TRUE;

-- ------------------------------------------------------------
-- 3-5. Lookup-Entitaeten
-- ------------------------------------------------------------
CREATE TABLE verlag (
    verlag_id   SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    land         VARCHAR(50)
);

CREATE TABLE genre (
    genre_id     SERIAL PRIMARY KEY,
    bezeichnung   VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE sprache (
    sprache_id   SERIAL PRIMARY KEY,
    bezeichnung   VARCHAR(50) NOT NULL,
    iso_code      CHAR(2) NOT NULL UNIQUE
);

-- ------------------------------------------------------------
-- 6. Buch (bibliografische Ausgabe)
-- ------------------------------------------------------------
CREATE TABLE buch (
    buch_id            SERIAL PRIMARY KEY,
    titel               VARCHAR(200) NOT NULL,
    isbn                VARCHAR(20) UNIQUE,
    erscheinungsjahr    INTEGER CHECK (erscheinungsjahr BETWEEN 1450 AND 2100),
    genre_id            INTEGER REFERENCES genre(genre_id),
    verlag_id           INTEGER REFERENCES verlag(verlag_id),
    sprache_id          INTEGER NOT NULL REFERENCES sprache(sprache_id)
);

-- Zeitabhaengige Pruefung gehoert nicht in einen CHECK (Ausdruecke mit
-- CURRENT_DATE sind nicht immutable), sondern in einen Trigger.
CREATE OR REPLACE FUNCTION fn_check_erscheinungsjahr() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.erscheinungsjahr IS NOT NULL
       AND NEW.erscheinungsjahr > EXTRACT(YEAR FROM CURRENT_DATE)::INT + 1 THEN
        RAISE EXCEPTION 'erscheinungsjahr % liegt zu weit in der Zukunft (maximal naechstes Jahr erlaubt).', NEW.erscheinungsjahr;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_buch_erscheinungsjahr
    BEFORE INSERT OR UPDATE OF erscheinungsjahr ON buch
    FOR EACH ROW EXECUTE FUNCTION fn_check_erscheinungsjahr();

-- ------------------------------------------------------------
-- 7. Autor + Buch_Autor (Aufloesung der N:M-Beziehung)
-- ------------------------------------------------------------
CREATE TABLE autor (
    autor_id     SERIAL PRIMARY KEY,
    vorname       VARCHAR(50) NOT NULL,
    nachname      VARCHAR(50) NOT NULL
);

CREATE TABLE buch_autor (
    buch_id   INTEGER NOT NULL REFERENCES buch(buch_id) ON DELETE CASCADE,
    autor_id  INTEGER NOT NULL REFERENCES autor(autor_id) ON DELETE CASCADE,
    PRIMARY KEY (buch_id, autor_id)
);

-- ------------------------------------------------------------
-- 8. Exemplar (konkrete ausleihbare Kopie einer Person)
-- ------------------------------------------------------------
CREATE TABLE exemplar (
    exemplar_id         SERIAL PRIMARY KEY,
    buch_id              INTEGER NOT NULL REFERENCES buch(buch_id),
    besitzer_id          INTEGER NOT NULL REFERENCES benutzer(benutzer_id),
    zustand              VARCHAR(20) NOT NULL CHECK (zustand IN ('neu', 'sehr gut', 'gut', 'gebraucht', 'stark gebraucht')),
    versand_moeglich     BOOLEAN NOT NULL DEFAULT FALSE,
    max_leihdauer_tage   INTEGER NOT NULL CHECK (max_leihdauer_tage BETWEEN 1 AND 365),
    eingestellt_am       DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Der Besitzer eines Exemplars wechselt nicht (sonst wuerden bestehende
-- Angebote/Zeitfenster/Abholorte dem falschen Besitzer zugeordnet sein).
CREATE TRIGGER trg_exemplar_besitzer_unveraenderlich
    BEFORE UPDATE OF besitzer_id ON exemplar
    FOR EACH ROW EXECUTE FUNCTION fn_spalte_unveraenderlich('besitzer_id');

-- ------------------------------------------------------------
-- 9. Abholort
-- ------------------------------------------------------------
CREATE TABLE abholort (
    abholort_id     SERIAL PRIMARY KEY,
    benutzer_id      INTEGER NOT NULL REFERENCES benutzer(benutzer_id) ON DELETE CASCADE,
    bezeichnung      VARCHAR(100) NOT NULL,
    strasse          VARCHAR(100) NOT NULL,
    plz              VARCHAR(10)  NOT NULL,
    stadt            VARCHAR(50)  NOT NULL,
    breitengrad      DECIMAL(9,6) NOT NULL,
    laengengrad      DECIMAL(9,6) NOT NULL,
    CONSTRAINT chk_abholort_breitengrad CHECK (breitengrad BETWEEN -90 AND 90),
    CONSTRAINT chk_abholort_laengengrad CHECK (laengengrad BETWEEN -180 AND 180)
);

CREATE TRIGGER trg_abholort_benutzer_unveraenderlich
    BEFORE UPDATE OF benutzer_id ON abholort
    FOR EACH ROW EXECUTE FUNCTION fn_spalte_unveraenderlich('benutzer_id');

-- ------------------------------------------------------------
-- 10. Verfuegbarkeitszeitfenster
-- ------------------------------------------------------------
CREATE TABLE verfuegbarkeitszeitfenster (
    zeitfenster_id   SERIAL PRIMARY KEY,
    benutzer_id       INTEGER NOT NULL REFERENCES benutzer(benutzer_id) ON DELETE CASCADE,
    wochentag         VARCHAR(10) NOT NULL CHECK (wochentag IN
                        ('Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag')),
    startzeit         TIME NOT NULL,
    endzeit           TIME NOT NULL,
    CONSTRAINT chk_zeitfenster_reihenfolge CHECK (endzeit > startzeit)
);

CREATE TRIGGER trg_zeitfenster_benutzer_unveraenderlich
    BEFORE UPDATE OF benutzer_id ON verfuegbarkeitszeitfenster
    FOR EACH ROW EXECUTE FUNCTION fn_spalte_unveraenderlich('benutzer_id');

-- ------------------------------------------------------------
-- 11. Angebot (reifizierte Ternaerbeziehung ANGEBOTEN_ALS:
--     Exemplar x Abholort x Verfuegbarkeitszeitfenster)
-- ------------------------------------------------------------
CREATE TABLE angebot (
    angebot_id       SERIAL PRIMARY KEY,
    exemplar_id       INTEGER NOT NULL REFERENCES exemplar(exemplar_id),
    abholort_id       INTEGER NOT NULL REFERENCES abholort(abholort_id),
    zeitfenster_id    INTEGER NOT NULL REFERENCES verfuegbarkeitszeitfenster(zeitfenster_id),
    aktiv             BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (exemplar_id, abholort_id, zeitfenster_id)
);

-- Abholort UND Zeitfenster muessen vom Besitzer des Exemplars eingerichtet sein.
CREATE OR REPLACE FUNCTION fn_check_angebot_besitzer() RETURNS TRIGGER AS $$
DECLARE
    v_besitzer INTEGER;
BEGIN
    SELECT besitzer_id INTO v_besitzer FROM exemplar WHERE exemplar_id = NEW.exemplar_id;
    IF (SELECT benutzer_id FROM abholort WHERE abholort_id = NEW.abholort_id) <> v_besitzer THEN
        RAISE EXCEPTION 'Abholort % gehoert nicht zur besitzenden Person von Exemplar %.', NEW.abholort_id, NEW.exemplar_id;
    END IF;
    IF (SELECT benutzer_id FROM verfuegbarkeitszeitfenster WHERE zeitfenster_id = NEW.zeitfenster_id) <> v_besitzer THEN
        RAISE EXCEPTION 'Zeitfenster % gehoert nicht zur besitzenden Person von Exemplar %.', NEW.zeitfenster_id, NEW.exemplar_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_angebot_besitzer
    BEFORE INSERT OR UPDATE ON angebot
    FOR EACH ROW EXECUTE FUNCTION fn_check_angebot_besitzer();

-- ------------------------------------------------------------
-- 12. Ausleihvorgang (reifizierte Ternaerbeziehung AUSLEIHT:
--     Exemplar x Benutzer(Entleiher) x Verfuegbarkeitszeitfenster)
-- ------------------------------------------------------------
CREATE TABLE ausleihvorgang (
    ausleihvorgang_id              SERIAL PRIMARY KEY,
    exemplar_id                     INTEGER NOT NULL REFERENCES exemplar(exemplar_id),
    entleiher_id                    INTEGER NOT NULL REFERENCES benutzer(benutzer_id),
    zeitfenster_id                  INTEGER NOT NULL REFERENCES verfuegbarkeitszeitfenster(zeitfenster_id),
    ausleihdatum                    DATE NOT NULL DEFAULT CURRENT_DATE,
    geplantes_rueckgabedatum        DATE NOT NULL,
    tatsaechliches_rueckgabedatum   DATE,
    status                          VARCHAR(20) NOT NULL DEFAULT 'aktiv'
                                     CHECK (status IN ('aktiv', 'zurueckgegeben', 'ueberfaellig')),
    CONSTRAINT chk_ausleih_rueckgabe_reihenfolge
        CHECK (geplantes_rueckgabedatum > ausleihdatum),
    CONSTRAINT chk_ausleih_tatsaechlich_konsistent
        CHECK (tatsaechliches_rueckgabedatum IS NULL OR tatsaechliches_rueckgabedatum >= ausleihdatum),
    -- status 'zurueckgegeben' <=> tatsaechliches Rueckgabedatum vorhanden
    CONSTRAINT chk_ausleih_status_rueckgabe
        CHECK ((status = 'zurueckgegeben') = (tatsaechliches_rueckgabedatum IS NOT NULL))
);

-- Ein Exemplar kann nicht gleichzeitig mehrfach aktiv/ueberfaellig ausgeliehen sein.
CREATE UNIQUE INDEX ux_ausleihvorgang_offen_je_exemplar
    ON ausleihvorgang (exemplar_id)
    WHERE status IN ('aktiv', 'ueberfaellig');

-- Geschaeftsregeln beim Anlegen/Aendern eines Ausleihvorgangs.
CREATE OR REPLACE FUNCTION fn_check_ausleihvorgang() RETURNS TRIGGER AS $$
DECLARE
    v_besitzer INTEGER;
    v_max_tage INTEGER;
BEGIN
    SELECT besitzer_id, max_leihdauer_tage INTO v_besitzer, v_max_tage
      FROM exemplar WHERE exemplar_id = NEW.exemplar_id;

    -- keine Ausleihe des eigenen Exemplars
    IF NEW.entleiher_id = v_besitzer THEN
        RAISE EXCEPTION 'Ein Exemplar kann nicht von der besitzenden Person selbst ausgeliehen werden (exemplar_id=%).', NEW.exemplar_id;
    END IF;

    -- geplante Dauer darf max_leihdauer_tage des Exemplars nicht ueberschreiten
    IF (NEW.geplantes_rueckgabedatum - NEW.ausleihdatum) > v_max_tage THEN
        RAISE EXCEPTION 'Geplante Leihdauer (% Tage) ueberschreitet die maximale Leihdauer des Exemplars (% Tage).',
            (NEW.geplantes_rueckgabedatum - NEW.ausleihdatum), v_max_tage;
    END IF;

    -- Zeitfenster muss der besitzenden Person gehoeren ...
    IF (SELECT benutzer_id FROM verfuegbarkeitszeitfenster WHERE zeitfenster_id = NEW.zeitfenster_id) <> v_besitzer THEN
        RAISE EXCEPTION 'Zeitfenster % gehoert nicht zur besitzenden Person von Exemplar %.', NEW.zeitfenster_id, NEW.exemplar_id;
    END IF;

    -- ... und fuer dieses Exemplar tatsaechlich als Angebot eingerichtet sein.
    IF NOT EXISTS (SELECT 1 FROM angebot
                    WHERE exemplar_id = NEW.exemplar_id AND zeitfenster_id = NEW.zeitfenster_id) THEN
        RAISE EXCEPTION 'Zeitfenster % ist fuer Exemplar % nicht als Angebot eingerichtet.', NEW.zeitfenster_id, NEW.exemplar_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_ausleihvorgang_regeln
    BEFORE INSERT OR UPDATE OF exemplar_id, entleiher_id, zeitfenster_id, ausleihdatum, geplantes_rueckgabedatum
    ON ausleihvorgang
    FOR EACH ROW EXECUTE FUNCTION fn_check_ausleihvorgang();

-- Eine bereits bewertete (abgeschlossene) Ausleihe darf nicht wieder
-- auf einen nicht abgeschlossenen Status zurueckgesetzt werden.
CREATE OR REPLACE FUNCTION fn_check_status_nach_bewertung() RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status = 'zurueckgegeben' AND NEW.status <> 'zurueckgegeben'
       AND EXISTS (SELECT 1 FROM bewertung WHERE ausleihvorgang_id = OLD.ausleihvorgang_id) THEN
        RAISE EXCEPTION 'Ausleihvorgang % wurde bereits bewertet und kann nicht auf Status % zurueckgesetzt werden.',
            OLD.ausleihvorgang_id, NEW.status;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ------------------------------------------------------------
-- 13. Bewertung (an Ausleihvorgang gekoppelt)
-- ------------------------------------------------------------
CREATE TABLE bewertung (
    bewertung_id        SERIAL PRIMARY KEY,
    ausleihvorgang_id    INTEGER NOT NULL UNIQUE REFERENCES ausleihvorgang(ausleihvorgang_id),
    sternebewertung      INTEGER NOT NULL CHECK (sternebewertung BETWEEN 1 AND 5),
    kommentar            TEXT,
    erstellt_am          DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TRIGGER trg_ausleihvorgang_status_nach_bewertung
    BEFORE UPDATE OF status ON ausleihvorgang
    FOR EACH ROW EXECUTE FUNCTION fn_check_status_nach_bewertung();

-- Nur abgeschlossene Ausleihvorgaenge duerfen bewertet werden, und die
-- Bewertung darf nicht vor der tatsaechlichen Rueckgabe liegen.
CREATE OR REPLACE FUNCTION fn_check_bewertung_nur_abgeschlossen() RETURNS TRIGGER AS $$
DECLARE
    v_status VARCHAR(20);
    v_rueck  DATE;
BEGIN
    SELECT status, tatsaechliches_rueckgabedatum INTO v_status, v_rueck
      FROM ausleihvorgang WHERE ausleihvorgang_id = NEW.ausleihvorgang_id;
    IF v_status <> 'zurueckgegeben' THEN
        RAISE EXCEPTION 'Bewertung nur fuer abgeschlossene (zurueckgegebene) Ausleihvorgaenge moeglich (ausleihvorgang_id=%).', NEW.ausleihvorgang_id;
    END IF;
    IF NEW.erstellt_am < v_rueck THEN
        RAISE EXCEPTION 'Bewertung darf nicht vor dem Rueckgabedatum (%) erstellt werden.', v_rueck;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_bewertung_nur_abgeschlossen
    BEFORE INSERT OR UPDATE ON bewertung
    FOR EACH ROW EXECUTE FUNCTION fn_check_bewertung_nur_abgeschlossen();

-- ------------------------------------------------------------
-- Indizes fuer haeufige Abfragen und Fremdschluessel
-- ------------------------------------------------------------
CREATE INDEX ix_adresse_benutzer ON adresse(benutzer_id);
CREATE INDEX ix_exemplar_buch ON exemplar(buch_id);
CREATE INDEX ix_exemplar_besitzer ON exemplar(besitzer_id);
CREATE INDEX ix_buch_genre ON buch(genre_id);
CREATE INDEX ix_buch_sprache ON buch(sprache_id);
CREATE INDEX ix_angebot_exemplar ON angebot(exemplar_id);
CREATE INDEX ix_ausleihvorgang_entleiher ON ausleihvorgang(entleiher_id);
CREATE INDEX ix_abholort_geo ON abholort(breitengrad, laengengrad);
