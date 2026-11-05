# Anforderungsspezifikation Buchtausch-App

## 1. Problembeschreibung und Zielsetzung

Viele Menschen besitzen Bücher, die sie aktuell nicht lesen, aber nicht endgültig weggeben möchten. Gleichzeitig gibt es in der Nachbarschaft Personen, die genau diese Bücher gerne lesen würden, sie aber nicht dauerhaft besitzen müssen. Die **Buchtausch-App** löst dieses Problem, indem sie Buchbesitzende und Interessierte in einer lokalen Gemeinschaft zusammenbringt und den zeitlich befristeten Verleih von Büchern organisiert. Ziel dieses Projekts ist die Konzeption einer normalisierten, relationalen Datenbank, die alle für den Ausleihprozess notwendigen Daten strukturiert speichert und sowohl klassische tabellarische Abfragen als auch eine räumliche Suche ("Bücher in meiner Nähe") unterstützt.

## 2. Lösungsansatz

Die Datenbank wird als relationales Schema mit PostgreSQL umgesetzt. PostgreSQL wurde gewählt, da es sich um ein modernes, quelloffenes DBMS mit vollständiger SQL-Unterstützung handelt, das über die Erweiterung PostGIS zusätzlich effiziente räumliche Abfragen (z. B. Umkreissuche über Geokoordinaten) ermöglicht. Das ist eine zentrale Anforderung der Aufgabenstellung. Das Datenmodell trennt konsequent zwischen der **Buchausgabe** (unveränderliche bibliografische Daten wie Titel, Autor:in, Verlag, Genre, Sprache) und dem **Exemplar** (die konkrete, ausleihbare Kopie einer Person mit individuellem Zustand, Verleihbedingungen und Standort). Diese Trennung vermeidet redundante Datenspeicherung und bildet die Grundlage für eine angemessene Normalisierung (3NF).

## 3. Rollen (Personen/Benutzendengruppen)

| Rolle | Beschreibung |
|---|---|
| **Benutzer:in** | Registrierte Person der App. Jede Person kann gleichzeitig als Verleiher:in eigener Bücher und als Entleiher:in fremder Bücher auftreten. Es handelt sich funktional um eine einzige Rolle mit zwei kontextabhängigen Aktionsbereichen, nicht um zwei getrennte Rollen. |
| **Verleiher:in** (Kontext) | Benutzer:in in der Funktion als Besitzer:in eines eingestellten Exemplars. |
| **Entleiher:in** (Kontext) | Benutzer:in in der Funktion als Ausleihende:r eines fremden Exemplars. |
| **System/App** | Technische Instanz, die Suche, Kartenanzeige und Transaktionsabwicklung koordiniert (kein eigener Datenbestand als "Rolle", aber Ausgangspunkt der Funktionsanforderungen). |

## 4. Aktionen der Rollen

**Verleiher:in:**
- Eigenes Profil mit Name, Adresse und Kontaktinformationen anlegen und pflegen.
- Ein Buch (Titel, Autor:in, Verlag, Genre, Erscheinungsjahr, Sprache) als eigenes Exemplar einstellen, inkl. Zustand, maximaler Leihdauer und Versandoption.
- Einen oder mehrere Abholorte definieren.
- Verfügbarkeitszeitfenster für die Übergabe festlegen.
- Ein Exemplar mit einer Kombination aus Abholort und Zeitfenster als aktiv anbieten.
- Ausleihvorgänge der eigenen Exemplare einsehen und die Rückgabe bestätigen.

**Entleiher:in:**
- Bücher tabellarisch durchsuchen und filtern (z. B. nach Genre, Sprache, Zustand).
- Verfügbare Bücher auf einer Karte im Umkreis des eigenen Standorts anzeigen lassen.
- Ein Exemplar zu einem bestimmten Zeitfenster ausleihen (Ausleihvorgang anlegen).
- Ein ausgeliehenes Buch zurückgeben.
- Nach Rückgabe eine Bewertung und einen Kommentar zu einem Buch abgeben.

## 5. Erforderliche Daten und Funktionen

**Daten:**
- Bibliografische Daten je Buchausgabe: Titel, ISBN, Erscheinungsjahr, Genre, Verlag, Sprache, Autor:in.
- Personendaten je Benutzer:in: Name, Adresse, Kontaktinformationen.
- Exemplardaten: Zustand, maximale Leihdauer, Versandmöglichkeit, Besitzer:in.
- Logistikdaten: Abholorte mit Geokoordinaten, Verfügbarkeitszeitfenster.
- Transaktionsdaten: Ausleihdatum, geplantes und tatsächliches Rückgabedatum, Status.
- Bewertungsdaten: Sternebewertung und Kommentar je Buch.

**Funktionen:**
- Tabellarische Suche/Filterung über Bücher und Exemplare.
- Räumliche Suche (Umkreissuche über Geokoordinaten von Abholorten).
- Verwaltung von Ausleihvorgängen (Anlegen, Status verfolgen, Rückgabe erfassen).
- Erfassen und Anzeigen von Bewertungen je Buch.

*(Umfang: ca. 1,5 Seiten bei 11-Punkt-Schrift, innerhalb der vorgegebenen max. 2 Seiten für die Anforderungsspezifikation.)*
