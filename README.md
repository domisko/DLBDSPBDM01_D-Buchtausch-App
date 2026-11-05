# Data-Mart-Erstellung in SQL (DLBDSPBDM01_D): Buchtausch-App

Portfolio-Projekt: relationale PostgreSQL-Datenbank für eine Buchtausch-App, über die Nachbarinnen und Nachbarn Bücher zeitlich befristet verleihen und ausleihen. Die Datenbank enthält bibliografische Daten, Personen und Adressen, Exemplare mit Verleihbedingungen, Abholorte mit Geokoordinaten, Zeitfenster, Ausleihvorgänge und Bewertungen und unterstützt neben tabellarischen auch räumliche Abfragen ("Bücher in meiner Nähe").

## Ergebnis auf einen Blick

- 14 Tabellen, 342 Datensätze (jede Tabelle mit mindestens 10 Einträgen)
- 14 Primärschlüssel, 17 Fremdschlüssel, 7 UNIQUE- und 16 CHECK-Constraints, 31 Indizes, 8 Trigger
- 37 automatisierte Testfälle: 16 positive Abfragen und 21 Negativtests (je Geschäftsregel einer)
- Zentrale Entwurfsentscheidung: Trennung von **Buch** (bibliografische Ausgabe) und **Exemplar** (konkrete Kopie einer Person)

## Installation

Voraussetzung: PostgreSQL ab Version 14 (getestet mit 16).

```bash
createdb buchtausch_app
psql -d buchtausch_app -f 03_Finalisierungsphase/sql/01_schema.sql      # Tabellen, Constraints, Trigger, Indizes
psql -d buchtausch_app -f 03_Finalisierungsphase/sql/02_dummy_data.sql  # 342 Datensätze
psql -d buchtausch_app -f 03_Finalisierungsphase/sql/03_testfaelle.sql  # optional: Testfälle (Negativtests mit ROLLBACK)
psql -d buchtausch_app -f 03_Finalisierungsphase/sql/04_metadaten.sql   # optional: Tabellen, Einträge, Größe
```

Automatisierte Tests mit Erwartungsprüfung (benötigt `pip3 install pillow`):

```bash
python3 03_Finalisierungsphase/sql/run_tests.py buchtausch_app
```

`01_schema.sql` löscht vorhandene Tabellen gleichen Namens und kann daher beliebig oft neu ausgeführt werden.

## Struktur

```
01_Konzeptionsphase/               Anforderungsspezifikation, ER-Modell (Chen), Datenwörterbuch, PDF-Erzeugung
02_Erarbeitungs-Reflexionsphase/   Schema und Daten der Zwischenabgabe, Präsentation (PR), Zusammenfassung (KZ)
03_Finalisierungsphase/
  sql/                             01_schema.sql, 02_dummy_data.sql, 03_testfaelle.sql, 04_metadaten.sql,
                                   generate_dummy_data.py, run_tests.py
  export/                          BE (3 Seiten), Abstract (AB), SQL-Dokumentation, GitHub-Link (GH), Abgabe-ZIP
  build_phase3_docs.py             erzeugt die PDFs (Zahlen live aus der Datenbank)
  build_zip.py                     baut die Abgabe-ZIP
PLAN.md                            Projektplan, Entscheidungen, Tutor-Feedback und Status je Phase
```

## Datenmodell in Kürze

`benutzer` 1:N `adresse`, `abholort`, `verfuegbarkeitszeitfenster`, `exemplar` (Besitzer). `buch` N:M `autor` (über `buch_autor`), N:1 `genre`, `verlag`, `sprache`. Die beiden Dreifachbeziehungen aus dem ER-Modell sind als Tabellen umgesetzt: `angebot` (Exemplar × Abholort × Zeitfenster) und `ausleihvorgang` (Exemplar × Entleiher × Zeitfenster). `bewertung` verweist 1:1 auf einen abgeschlossenen `ausleihvorgang`.

## Geschäftsregeln und ihre Absicherung

Die vollständige Zuordnung (Regel, Mechanismus, Datenbankobjekt, Negativtest) steht in der SQL-Dokumentation `03_Finalisierungsphase/export/*_Abschlussphase_SQL.pdf`. Beispiele: doppelte offene Ausleihen verhindert ein partieller UNIQUE-Index, die maximale Leihdauer und die Zuordnung von Zeitfenstern zum Besitzer sichern Trigger, Koordinaten und Sternebewertungen sichern CHECK-Constraints.
