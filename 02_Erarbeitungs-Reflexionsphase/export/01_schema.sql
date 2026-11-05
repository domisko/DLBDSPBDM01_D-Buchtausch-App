-- ============================================================
-- Data-Mart-Erstellung in SQL (DLBDSPBDM01_D) - Buchtausch-App
-- Phase 2: Erarbeitungs-/Reflexionsphase - Schema (DDL)
-- DBMS: PostgreSQL
--
-- Reihenfolge der Tabellen folgt den Abhaengigkeiten (Lookup-Tabellen
-- zuerst, dann Kernentitaeten, zuletzt die reifizierten Ternaerbeziehungen
-- Ausleihvorgang und Angebot, die auf mehreren vorherigen Tabellen aufbauen).
-- ============================================================

DROP TABLE IF EXISTS bewertung CASCADE;
DROP TABLE IF EXISTS angebot CASCADE;
DROP TABLE IF EXISTS ausleihvorgang CASCADE;
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
-- 1. Benutzer
-- ------------------------------------------------------------
CREATE TABLE benutzer (
    benutzer_id      SERIAL PRIMARY KEY,
    vorname           VARCHAR(50)  NOT NULL,
    nachname          VARCHAR(50)  NOT NULL,
    email             VARCHAR(100) NOT NULL UNIQUE,
    telefon           VARCHAR(20),
    registrierdatum   DATE         NOT NULL DEFAULT CURRENT_DATE
);

-- ------------------------------------------------------------
-- 2. Adresse (1:N zu Benutzer, siehe Aenderungen fuer Phase 2)
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
    ist_hauptadresse    BOOLEAN NOT NULL DEFAULT FALSE
);

-- Pro Benutzer:in darf es hoechstens eine Hauptadresse geben.
CREATE UNIQUE INDEX ux_adresse_hauptadresse
    ON adresse (benutzer_id)
    WHERE ist_hauptadresse = TRUE;

-- ------------------------------------------------------------
-- 3-6. Lookup-Entitaeten fuer Buch
-- ------------------------------------------------------------
CREATE TABLE verlag (
    verlag_id   SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
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
-- Buch (bibliografische Ausgabe)
-- ------------------------------------------------------------
CREATE TABLE buch (
    buch_id            SERIAL PRIMARY KEY,
    titel               VARCHAR(200) NOT NULL,
    isbn                VARCHAR(20) UNIQUE,
    erscheinungsjahr    INTEGER CHECK (erscheinungsjahr BETWEEN 1450 AND EXTRACT(YEAR FROM CURRENT_DATE)::INT),
    genre_id            INTEGER REFERENCES genre(genre_id),
    verlag_id           INTEGER REFERENCES verlag(verlag_id),
    sprache_id          INTEGER NOT NULL REFERENCES sprache(sprache_id)
);

-- ------------------------------------------------------------
-- Autor + Buch-Autor (Aufloesung der N:M-Beziehung Buch-Autor)
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
    max_leihdauer_tage   INTEGER NOT NULL CHECK (max_leihdauer_tage > 0),
    eingestellt_am       DATE NOT NULL DEFAULT CURRENT_DATE
);

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
    laengengrad      DECIMAL(9,6) NOT NULL
);

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
        CHECK (tatsaechliches_rueckgabedatum IS NULL OR tatsaechliches_rueckgabedatum >= ausleihdatum)
);

-- Eine Person kann sich nicht ihr eigenes Exemplar ausleihen.
CREATE OR REPLACE FUNCTION fn_check_nicht_selbst_ausleihen() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.entleiher_id = (SELECT besitzer_id FROM exemplar WHERE exemplar_id = NEW.exemplar_id) THEN
        RAISE EXCEPTION 'Ein Exemplar kann nicht von der besitzenden Person selbst ausgeliehen werden (exemplar_id=%).', NEW.exemplar_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_nicht_selbst_ausleihen
    BEFORE INSERT OR UPDATE ON ausleihvorgang
    FOR EACH ROW EXECUTE FUNCTION fn_check_nicht_selbst_ausleihen();

-- ------------------------------------------------------------
-- 13. Angebot (reifizierte Ternaerbeziehung ANGEBOTEN_ALS:
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

-- ------------------------------------------------------------
-- 11. Bewertung (Feedback Phase 1: an Ausleihvorgang gekoppelt,
--     nicht mehr direkt an Buch/Benutzer)
-- ------------------------------------------------------------
CREATE TABLE bewertung (
    bewertung_id        SERIAL PRIMARY KEY,
    ausleihvorgang_id    INTEGER NOT NULL UNIQUE REFERENCES ausleihvorgang(ausleihvorgang_id),
    sternebewertung      INTEGER NOT NULL CHECK (sternebewertung BETWEEN 1 AND 5),
    kommentar            TEXT,
    erstellt_am          DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Feedback Phase 1: "nur tatsaechlich ausgeliehene (und zurueckgegebene)
-- Buecher duerfen bewertet werden" laesst sich nicht als Spalten-CHECK
-- ausdruecken (haengt vom Status einer anderen Zeile ab) -> Trigger.
CREATE OR REPLACE FUNCTION fn_check_bewertung_nur_abgeschlossen() RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT status FROM ausleihvorgang WHERE ausleihvorgang_id = NEW.ausleihvorgang_id) <> 'zurueckgegeben' THEN
        RAISE EXCEPTION 'Bewertung nur fuer abgeschlossene (zurueckgegebene) Ausleihvorgaenge moeglich (ausleihvorgang_id=%).', NEW.ausleihvorgang_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_bewertung_nur_abgeschlossen
    BEFORE INSERT OR UPDATE ON bewertung
    FOR EACH ROW EXECUTE FUNCTION fn_check_bewertung_nur_abgeschlossen();

-- ------------------------------------------------------------
-- Indizes fuer haeufige Abfragen (Suche/Filterung, siehe Anforderungsspezifikation)
-- ------------------------------------------------------------
CREATE INDEX ix_exemplar_buch ON exemplar(buch_id);
CREATE INDEX ix_exemplar_besitzer ON exemplar(besitzer_id);
CREATE INDEX ix_buch_genre ON buch(genre_id);
CREATE INDEX ix_buch_sprache ON buch(sprache_id);
CREATE INDEX ix_ausleihvorgang_exemplar ON ausleihvorgang(exemplar_id);
CREATE INDEX ix_ausleihvorgang_entleiher ON ausleihvorgang(entleiher_id);
CREATE INDEX ix_abholort_geo ON abholort(breitengrad, laengengrad);
