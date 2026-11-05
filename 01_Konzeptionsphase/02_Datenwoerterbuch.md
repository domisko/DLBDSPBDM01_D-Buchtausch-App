# Datenwörterbuch Buchtausch-App

Alle Attribute werden auf die in `01_Anforderungsspezifikation.md` genannten Daten- und Funktionsanforderungen zurückgeführt (Traceability).

## Änderungen für Phase 2 (nach Tutor-Feedback zu Phase 1)

Das konzeptionelle ERM aus Phase 1 bleibt als eingereichte Leistung unverändert (siehe `04_Gesamtdokument.md`). Für die logische/physische Umsetzung in Phase 2 wurden drei Rückmeldungen des Tutors eingearbeitet:

1. **Bewertung an Ausleihvorgang koppeln, statt an Buch + Benutzer:in direkt.** Damit technisch sichergestellt ist, dass nur tatsächlich ausgeliehene Bücher bewertet werden können, referenziert `Bewertung` jetzt einen konkreten `Ausleihvorgang` (UNIQUE-FK). `buch_id` und `benutzer_id` sind darüber weiterhin erreichbar (Ausleihvorgang → Exemplar → Buch bzw. Ausleihvorgang → Benutzer), müssen aber nicht redundant gespeichert werden.
   - Das erfordert, die Ternärbeziehung **AUSLEIHT** aus Phase 1 zu einer eigenen Entität **Ausleihvorgang** zu "reifizieren" (mit eigenem Primärschlüssel), da eine Beziehung selbst nicht Ziel einer weiteren Fremdschlüsselbeziehung sein kann, eine referenzierbare Entität hingegen schon. Das ist eine Standardtechnik beim Übergang vom konzeptionellen zum logischen Modell und kein Widerspruch zum Phase-1-ERM.
   - Aus Konsistenzgründen wird die zweite Ternärbeziehung **ANGEBOTEN_ALS** ebenso als eigene Entität **Angebot** umgesetzt (gleiche Begründung: jede N:N:N-Beziehung wird bei der SQL-Umsetzung ohnehin zu einer Tabelle mit drei Fremdschlüsseln; hier bekommt sie zusätzlich einen Surrogatschlüssel).
2. **Benutzer–Adresse von 1:1 auf 1:N geändert.** Nutzende dürfen mehrere Adressen hinterlegen (z. B. Haupt- und Zweitwohnsitz). Zur Unterscheidung wurde `ist_hauptadresse` (BOOLEAN) ergänzt.
3. **Constraints konsequent implementiert** (Details siehe SQL-DDL in Phase 2): `sternebewertung` per CHECK auf 1–5 begrenzt, `email` UNIQUE, Zeitfenster validiert (`endzeit > startzeit`), `max_leihdauer_tage` per CHECK auf positive Werte begrenzt. Die Regel "nur abgeschlossene Ausleihvorgänge dürfen bewertet werden" wird per Trigger durchgesetzt, da sie sich nicht als einfacher Spalten-CHECK ausdrücken lässt (sie hängt vom Status einer anderen Zeile ab).

Damit umfasst das logische Modell für Phase 2 **13 Entitäten** (11 aus Phase 1 + Ausleihvorgang + Angebot).

### Ergänzungen in Phase 3 (nach Tutor-Feedback zu Phase 2)

Das Schema (`03_Finalisierungsphase/sql/01_schema.sql`) wurde um weitere Integritätsregeln erweitert, ohne Tabellen oder Attribute zu ändern:

- `buch.erscheinungsjahr`: CHECK nur mit festen Grenzen (1450 bis 2100), die zeitabhängige Prüfung ("nicht in der Zukunft") liegt in einem Trigger.
- `ausleihvorgang`: partieller UNIQUE-Index gegen doppelte offene Ausleihen, Trigger für maximale Leihdauer, für Selbst-Ausleihe sowie für die Zuordnung von Zeitfenster zu Besitzer und Angebot, CHECK `status = 'zurueckgegeben'` genau dann, wenn `tatsaechliches_rueckgabedatum` gesetzt ist.
- `angebot`: Trigger stellt sicher, dass Abholort und Zeitfenster dem Besitzer des Exemplars gehören.
- `bewertung`: bewertete Ausleihen können nicht auf einen nicht abgeschlossenen Status zurückgesetzt werden; Bewertung nicht vor dem Rückgabedatum.
- `adresse`, `abholort`: CHECK-Constraints für gültige Koordinaten.
- Besitzer-Spalten (`exemplar.besitzer_id`, `abholort.benutzer_id`, `verfuegbarkeitszeitfenster.benutzer_id`) sind unveränderlich.

Die vollständige Zuordnung Regel → Mechanismus → Test steht in der SQL-Dokumentation der Finalisierungsphase.

## Entitäten (13, davon 2 neu für Phase 2: Ausleihvorgang, Angebot)

### 1. Benutzer
| Attribut | Typ | Beschreibung |
|---|---|---|
| benutzer_id | INT (PK) | Eindeutige ID |
| vorname | VARCHAR(50) | Vorname |
| nachname | VARCHAR(50) | Nachname |
| email | VARCHAR(100), UNIQUE | Kontakt/Login |
| telefon | VARCHAR(20) | Kontaktinformation |
| registrierdatum | DATE | Zeitpunkt der Registrierung |

### 2. Adresse
| Attribut | Typ | Beschreibung |
|---|---|---|
| adresse_id | INT (PK) | Eindeutige ID |
| benutzer_id | INT (FK → Benutzer) | Zugehörige Person (1:N, siehe Änderungen für Phase 2) |
| strasse | VARCHAR(100) | Straße |
| hausnummer | VARCHAR(10) | Hausnummer |
| plz | VARCHAR(10) | Postleitzahl |
| stadt | VARCHAR(50) | Stadt |
| breitengrad | DECIMAL(9,6) | Geokoordinate (privat) |
| laengengrad | DECIMAL(9,6) | Geokoordinate (privat) |
| ist_hauptadresse | BOOLEAN | Kennzeichnet die primäre Adresse einer Person |

### 3. Buch (bibliografische Ausgabe)
| Attribut | Typ | Beschreibung |
|---|---|---|
| buch_id | INT (PK) | Eindeutige ID |
| titel | VARCHAR(200) | Buchtitel |
| isbn | VARCHAR(20) | ISBN |
| erscheinungsjahr | INT | Erscheinungsjahr |
| genre_id | INT (FK → Genre) | Genre |
| verlag_id | INT (FK → Verlag) | Verlag |
| sprache_id | INT (FK → Sprache) | Sprache |

### 4. Autor
| Attribut | Typ | Beschreibung |
|---|---|---|
| autor_id | INT (PK) | Eindeutige ID |
| vorname | VARCHAR(50) | Vorname |
| nachname | VARCHAR(50) | Nachname |

### 5. Verlag
| Attribut | Typ | Beschreibung |
|---|---|---|
| verlag_id | INT (PK) | Eindeutige ID |
| name | VARCHAR(100) | Verlagsname |
| land | VARCHAR(50) | Sitzland |

### 6. Genre
| Attribut | Typ | Beschreibung |
|---|---|---|
| genre_id | INT (PK) | Eindeutige ID |
| bezeichnung | VARCHAR(50) | Genrebezeichnung |

### 7. Sprache
| Attribut | Typ | Beschreibung |
|---|---|---|
| sprache_id | INT (PK) | Eindeutige ID |
| bezeichnung | VARCHAR(50) | Sprachbezeichnung |
| iso_code | CHAR(2) | ISO-639-1-Code |

### 8. Exemplar (konkrete ausleihbare Kopie)
| Attribut | Typ | Beschreibung |
|---|---|---|
| exemplar_id | INT (PK) | Eindeutige ID |
| buch_id | INT (FK → Buch) | Zugehörige Buchausgabe |
| besitzer_id | INT (FK → Benutzer) | Besitzende Person |
| zustand | VARCHAR(20) | Zustand des Buches |
| versand_moeglich | BOOLEAN | Versand per Post möglich |
| max_leihdauer_tage | INT | Maximale Leihdauer in Tagen |
| eingestellt_am | DATE | Datum der Einstellung |

### 9. Abholort
| Attribut | Typ | Beschreibung |
|---|---|---|
| abholort_id | INT (PK) | Eindeutige ID |
| benutzer_id | INT (FK → Benutzer) | Anbietende Person |
| bezeichnung | VARCHAR(100) | Bezeichnung des Ortes |
| strasse | VARCHAR(100) | Straße |
| plz | VARCHAR(10) | Postleitzahl |
| stadt | VARCHAR(50) | Stadt |
| breitengrad | DECIMAL(9,6) | Geokoordinate (öffentlich) |
| laengengrad | DECIMAL(9,6) | Geokoordinate (öffentlich) |

### 10. Verfuegbarkeitszeitfenster
| Attribut | Typ | Beschreibung |
|---|---|---|
| zeitfenster_id | INT (PK) | Eindeutige ID |
| benutzer_id | INT (FK → Benutzer) | Anbietende Person |
| wochentag | VARCHAR(10) | Wochentag |
| startzeit | TIME | Beginn des Zeitfensters |
| endzeit | TIME | Ende des Zeitfensters |

### 11. Bewertung
| Attribut | Typ | Beschreibung |
|---|---|---|
| bewertung_id | INT (PK) | Eindeutige ID |
| ausleihvorgang_id | INT (FK → Ausleihvorgang), UNIQUE | Bewerteter, abgeschlossener Ausleihvorgang (ersetzt die direkten FKs auf Buch/Benutzer aus Phase 1) |
| sternebewertung | INT, CHECK (1–5) | Sterne-Bewertung |
| kommentar | TEXT | Freitextkommentar |
| erstellt_am | DATE | Erstellungsdatum |

### 12. Ausleihvorgang (neu für Phase 2: reifizierte Ternärbeziehung AUSLEIHT)
| Attribut | Typ | Beschreibung |
|---|---|---|
| ausleihvorgang_id | INT (PK) | Eindeutige ID |
| exemplar_id | INT (FK → Exemplar) | Ausgeliehenes Exemplar |
| entleiher_id | INT (FK → Benutzer) | Ausleihende Person |
| zeitfenster_id | INT (FK → Verfuegbarkeitszeitfenster) | Genutztes Zeitfenster der besitzenden Person |
| ausleihdatum | DATE | Datum der Ausleihe |
| geplantes_rueckgabedatum | DATE | Geplantes Rückgabedatum |
| tatsaechliches_rueckgabedatum | DATE, NULL bis Rückgabe | Tatsächliches Rückgabedatum |
| status | VARCHAR(20), CHECK (aktiv/zurückgegeben/ueberfaellig) | Status des Ausleihvorgangs |

### 13. Angebot (neu für Phase 2: reifizierte Ternärbeziehung ANGEBOTEN_ALS)
| Attribut | Typ | Beschreibung |
|---|---|---|
| angebot_id | INT (PK) | Eindeutige ID |
| exemplar_id | INT (FK → Exemplar) | Angebotenes Exemplar |
| abholort_id | INT (FK → Abholort) | Gültiger Abholort für dieses Angebot |
| zeitfenster_id | INT (FK → Verfuegbarkeitszeitfenster) | Gültiges Zeitfenster für dieses Angebot |
| aktiv | BOOLEAN | Angebot derzeit aktiv |

## Binäre Beziehungen (Phase 2, nach Reifizierung)

| Beziehung | Kardinalität (Chen) |
|---|---|
| Benutzer — wohnt_an — Adresse | 1:N *(Phase 1: 1:1, siehe Änderungen für Phase 2)* |
| Benutzer — besitzt — Exemplar | 1:N |
| Benutzer — hat — Abholort | 1:N |
| Benutzer — hat — Zeitfenster | 1:N |
| Exemplar — ist_ausgabe_von — Buch | N:1 |
| Buch — hat — Genre | N:1 |
| Buch — erschienen_bei — Verlag | N:1 |
| Buch — in_sprache — Sprache | N:1 |
| Buch — geschrieben_von — Autor | N:M |
| Exemplar — wird_ausgeliehen_in — Ausleihvorgang | 1:N |
| Benutzer — leiht_aus_in — Ausleihvorgang (als Entleiher) | 1:N |
| Zeitfenster — genutzt_in — Ausleihvorgang | 1:N |
| Ausleihvorgang — bewertet_durch — Bewertung | 1:1 (0..1) |
| Exemplar — angeboten_in — Angebot | 1:N |
| Abholort — genutzt_in — Angebot | 1:N |
| Zeitfenster — genutzt_in — Angebot | 1:N |

*Hinweis:* `Buch — erhält — Bewertung` und `Benutzer — verfasst — Bewertung` aus Phase 1 entfallen als direkte Beziehungen; beide Informationen sind ab Phase 2 indirekt über `Ausleihvorgang` erreichbar (siehe Änderungen für Phase 2, Punkt 1).

## Ternäre Beziehungen (2 von max. 3, konzeptionelles Modell aus Phase 1)

### AUSLEIHT: Exemplar × Benutzer(Entleiher) × Verfuegbarkeitszeitfenster
Attribute: ausleihdatum, geplantes_rueckgabedatum, tatsaechliches_rueckgabedatum, status.

Kardinalität: N:N:N. Begründung: Da das Zeitfenster der besitzenden Person (nicht dem Exemplar) zugeordnet ist, lässt sich ein Ausleihvorgang erst durch das Zusammenspiel aller drei Entitäten vollständig beschreiben. Aus (Exemplar, Entleiher) allein folgt nicht, welches der mehreren Zeitfenster der besitzenden Person genutzt wurde; aus (Entleiher, Zeitfenster) folgt nicht, welches Exemplar ausgeliehen wird; aus (Exemplar, Zeitfenster) folgt nicht, wer ausleiht. Keines der drei Paare bestimmt das dritte Element eindeutig, eine Zerlegung in zwei binäre Beziehungen wäre daher verlustbehaftet.

**Bewusst vermiedene Alternative:** Die Aufgabenstellung legt eine Dreifachbeziehung aus "Verleiher:in, Entleiher:in, Exemplar" nahe. Dies ist jedoch eine *unechte* Dreifachbeziehung: Die verleihende Person ergibt sich bereits eindeutig aus `Exemplar.besitzer_id`, sodass dieses Tripel auf die binäre Beziehung (Exemplar, Entleiher) reduzierbar wäre. Aus diesem Grund wurde stattdessen AUSLEIHT mit dem Zeitfenster als drittem Bestandteil gewählt.

### ANGEBOTEN_ALS: Exemplar × Abholort × Verfuegbarkeitszeitfenster
Attribut: aktiv (BOOLEAN).

Kardinalität: N:N:N. Begründung: Eine besitzende Person kann mehrere Abholorte und mehrere Zeitfenster anbieten und pro Exemplar eine individuelle, gültige Kombination aus Ort und Zeitfenster festlegen (z. B. Exemplar A nur abends am Bahnhof, Exemplar B nur samstags an der Haustür). Diese Zuordnung ist nicht auf eine der drei paarweisen Beziehungen reduzierbar.

*Hinweis:* Eine dritte Kandidaten-Beziehung (Buch × Sprache × Verlag, im Sinne einer "Ausgaben-Ternärbeziehung") wurde geprüft, erwies sich jedoch als auf binäre Beziehungen zerlegbar und wurde daher verworfen. Es werden bewusst 2 statt 3 Dreifachbeziehungen ausgearbeitet, um im Rahmen des 4-Seiten-Budgets Qualität vor Quantität zu stellen.
