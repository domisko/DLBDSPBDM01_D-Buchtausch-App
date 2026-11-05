-- ============================================================
-- Phase 3: Metadaten der Datenbank (Tabellen, Eintraege, Groesse, Objekte)
-- ============================================================

-- Anzahl Tabellen, Eintraege je Tabelle, Groesse je Tabelle (inkl. Indizes)
SELECT c.relname AS tabelle,
       (xpath('/row/n/text()', query_to_xml(format('SELECT count(*) AS n FROM %I', c.relname), false, true, '')))[1]::text::int AS eintraege,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS groesse
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r'
ORDER BY c.relname;

-- Summen und Datenbankgroesse
SELECT (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
         WHERE n.nspname = 'public' AND c.relkind = 'r') AS tabellen,
       (SELECT sum((xpath('/row/n/text()', query_to_xml(format('SELECT count(*) AS n FROM %I', c.relname), false, true, '')))[1]::text::int)
          FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
         WHERE n.nspname = 'public' AND c.relkind = 'r') AS eintraege_gesamt,
       pg_size_pretty(pg_database_size(current_database())) AS datenbankgroesse,
       pg_size_pretty((SELECT sum(pg_total_relation_size(c.oid)) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                        WHERE n.nspname = 'public' AND c.relkind = 'r')) AS tabellen_inkl_indizes;

-- Integritaets- und Performance-Objekte
SELECT (SELECT count(*) FROM pg_constraint WHERE connamespace = 'public'::regnamespace AND contype = 'p') AS primaerschluessel,
       (SELECT count(*) FROM pg_constraint WHERE connamespace = 'public'::regnamespace AND contype = 'f') AS fremdschluessel,
       (SELECT count(*) FROM pg_constraint WHERE connamespace = 'public'::regnamespace AND contype = 'u') AS unique_constraints,
       (SELECT count(*) FROM pg_constraint WHERE connamespace = 'public'::regnamespace AND contype = 'c') AS check_constraints,
       (SELECT count(*) FROM pg_indexes WHERE schemaname = 'public') AS indizes,
       (SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid = t.tgrelid
         WHERE NOT t.tgisinternal AND c.relnamespace = 'public'::regnamespace) AS trigger_gesamt,
       (SELECT count(*) FROM pg_proc WHERE pronamespace = 'public'::regnamespace) AS funktionen;
