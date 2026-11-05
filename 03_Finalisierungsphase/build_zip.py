"""
Baut die Abgabe-ZIP gemaess Aufgabenstellung (Kap. 4.2, Finalisierungsphase):

  Miskovic_Dominik_14133980_DLBDSPBDM01_D/
    01_Konzeptionsphase/            Anforderungsspezifikation (max. 2 S.) + Beschreibung (max. 2 S.)
    02_Erarbeitungs-Reflexionsphase/ PR-PDF, KZ-PDF, .sql-Dateien (so wie in Phase 2 abgegeben)
    03_Finalisierungsphase/         Dateien aus Phase 1+2 (PDF), SQL-/BE-/AB-/GH-PDF, finale .sql-Dateien

Die Phase-1-Datei wird aus dem eingereichten PDF geteilt (Seite 1 / Seiten 2-3);
Phase-1- und Phase-2-Endergebnisse bleiben unveraendert und separat erhalten.
Aufruf:  python3 build_zip.py
"""
import os
import shutil
import tempfile
import zipfile

import fitz

BASE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(BASE)
P1 = os.path.join(PROJ, "01_Konzeptionsphase", "export")
P2 = os.path.join(PROJ, "02_Erarbeitungs-Reflexionsphase", "export")
P3 = os.path.join(BASE, "export")
SQL3 = os.path.join(BASE, "sql")

PRAEFIX = "Miskovic-Dominik_14133980_DLBDSPBDM01_D"
ROOT = "Miskovic_Dominik_14133980_DLBDSPBDM01_D"
ZIP_PATH = os.path.join(P3, ROOT + ".zip")

p1_pdf = os.path.join(P1, f"{PRAEFIX}_Konzeptionsphase_AB.pdf")
assert os.path.exists(p1_pdf), "Phase-1-PDF fehlt"

eintraege = []  # (quelle, pfad_im_zip)


def add(src, ziel):
    assert os.path.exists(src), f"fehlt: {src}"
    eintraege.append((src, f"{ROOT}/{ziel}"))


tmp = tempfile.mkdtemp(prefix="zipbuild_")
try:
    # --- Phase 1: Teilung des eingereichten PDFs
    d = fitz.open(p1_pdf)
    assert len(d) == 3
    for teil, seiten, name in [("AS", (0, 0), "Anforderungsspezifikation"), ("BE", (1, 2), "Beschreibung")]:
        out = fitz.open()
        out.insert_pdf(d, from_page=seiten[0], to_page=seiten[1])
        pfad = os.path.join(tmp, f"{PRAEFIX}_Konzeptionsphase_{name}.pdf")
        out.save(pfad)
        assert len(out) <= 2
        add(pfad, f"01_Konzeptionsphase/{os.path.basename(pfad)}")

    # --- Phase 2: unveraendert wie eingereicht
    for f in sorted(os.listdir(P2)):
        if f.endswith((".pdf", ".sql")):
            add(os.path.join(P2, f), f"02_Erarbeitungs-Reflexionsphase/{f}")

    # --- Phase 3
    add(p1_pdf, f"03_Finalisierungsphase/Phase1_Endergebnis/{os.path.basename(p1_pdf)}")
    for f in sorted(os.listdir(P2)):
        if f.endswith(".pdf"):
            add(os.path.join(P2, f), f"03_Finalisierungsphase/Phase2_Endergebnis/{f}")
    for typ in ("SQL", "BE", "AB", "GH"):
        add(os.path.join(P3, f"{PRAEFIX.replace('_D', '_D')}_Abschlussphase_{typ}.pdf"), f"03_Finalisierungsphase/{PRAEFIX}_Abschlussphase_{typ}.pdf")
    for f in ("01_schema.sql", "02_dummy_data.sql", "03_testfaelle.sql", "04_metadaten.sql", "generate_dummy_data.py", "run_tests.py"):
        add(os.path.join(SQL3, f), f"03_Finalisierungsphase/sql/{f}")

    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        for src, ziel in eintraege:
            z.write(src, ziel)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"geschrieben: {ZIP_PATH} ({os.path.getsize(ZIP_PATH) / 1024:.0f} kB, {len(eintraege)} Dateien)")
with zipfile.ZipFile(ZIP_PATH) as z:
    for n in z.namelist():
        print("  ", n.replace(ROOT + "/", ""))
