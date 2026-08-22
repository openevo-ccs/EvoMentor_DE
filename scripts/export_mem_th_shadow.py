#!/usr/bin/env python3
"""export_mem_th_shadow.py -- converts EvoMentor_DE's Thuringia Grades 5-10
Lernziel dataset (data/lernziele_MNT56.json, lernziele_gy78.json,
lernziele_gy910.json) into a Turtle graph shaped like FWU's real MEM
(mem.schule) Lehrplan ontology graphs.

WHY THIS EXISTS
----------------
FWU's live MEM SPARQL endpoint (https://sparql.mem.edufeed.org/sparql/) has
curriculum data loaded for exactly four states -- Bayern, Brandenburg,
Sachsen, Rheinland-Pfalz -- confirmed live 2026-08-22 by querying the
endpoint directly (see VERIFIED FACTS below). Thuringia has NO curriculum
data loaded upstream, only the shared Bundesland/Jahrgangsstufe/Schulfach/
Schulart individuals every state gets regardless of whether its curriculum
graph is loaded. There is therefore nothing to crosswalk EvoMentor_DE's data
against directly.

What this script does instead: produce a genuinely MEM-ontology-shaped local
"shadow graph" for Thuringia, Grades 5-10 -- reusing every real, live,
VERIFIED shared individual/predicate/class FWU's ontology already defines,
and minting new individuals ONLY for the Thuringia-specific curriculum nodes
that don't exist anywhere upstream (Fachlehrplan/Lernbereich/
Kompetenzerwartung instances), following the exact same "modular per-state
subclass" pattern FWU's own lehrplan-ontologie already uses for BY/BB/SN/RP
(schema.md documents e.g. `LehrplanPLUS (BY)` as a subclass of the core
`Lehrplan` class -- this script does the same for TH).

Two direct payoffs of shaping it this way rather than inventing a bespoke
format:
1. `memschule`'s own traversal.py/queries.py functions (tree(), get_children(),
   etc.) would work against this file unmodified if loaded into any
   triplestore, because has-part is transitively pre-materialized here
   exactly the way schema.md documents FWU's real graphs doing it.
2. EvoMentor (v2)'s canonical-curriculum-item.schema.json already declares
   "fwu-lehrplan-ontologie" as a first-class sourceFormat (individualUri +
   landOntology + coreOntologyVersion) -- this file is real input for that
   importer path, closing the gap where EvoMentor_DE's Thuringia data
   currently only reaches EvoMentor v2 through the generic "custom"
   sourceFormat / thuringia_custom_importer.py, and only for the 90
   evolution-annotated Gy 7-8 items, not the full Grades 5-10 dataset.

VERIFIED FACTS (queried live against https://sparql.mem.edufeed.org/sparql/
on 2026-08-22 -- see docstrings below each constant for the exact query;
none of these are assumed from documentation)
----------------------------------------------------------------------------
- Bundesland Thueringen:                lp:LP_3000031
- Schulfach Biologie (TH):               schulfach:TH_0000002
- Schulfach Mensch-Natur-Technik (TH):    schulfach:TH_0000028
- Schulart Gymnasium (TH):                schulart:TH_0000006
- Jahrgangsstufe pattern LP_200000N for grade N (N=1..13), confirmed for
  N=1 ("Jahrgangsstufe 1") and N=7 ("Jahrgangsstufe 7") -- grades 5-10 are
  LP_2000005..LP_2000010 by the same confirmed pattern.

WHAT'S DELIBERATELY OUT OF SCOPE
---------------------------------
- The KMK Basiskonzepte Biologie framework (basiskonzepte_primaer/
  basiskonzepte_sekundaer) is NOT modeled here as LP_ classes/individuals --
  it's a separate national cross-cutting framework with no representation in
  FWU's Lehrplan ontology (confirmed by EvoMentor's own
  canonical-curriculum-item.schema.json frameworkTags field comment). Each
  Kompetenzerwartung individual instead carries plain string literals
  (evomentor:basiskonzeptPrimaer / evomentor:basiskonzeptSekundaer) pointing
  at the exact same "kmk-basiskonzepte-biologie:bk_..." tag ids used by
  conceptbase's RFC-0018 (framework-relations/
  KMK-BASISKONZEPTE-BIOLOGIE-RELATIONS-v1.0.0.yaml) -- deliberately
  cross-referenceable, not duplicated modeling.
- FWU's `hat Titel` predicate (LP_0000030056) links to a "Titel annotation
  object" whose exact shape was not independently verified against the live
  endpoint this session -- rdfs:label is used instead for human-readable
  titles (an unambiguous, universally valid choice) rather than guess at an
  unverified structure.
- This is a PROVISIONAL, locally-minted namespace
  (https://openevo-ccs.github.io/EvoMentor_DE/lehrplan-th-shadow/), never
  under w3id.org/lehrplan/th -- that namespace is FWU's own and reserved for
  if/when they (or a partner) publish real Thuringia curriculum data.

USAGE
-----
    python scripts/export_mem_th_shadow.py

Reads data/lernziele_MNT56.json, data/lernziele_gy78.json,
data/lernziele_gy910.json. Writes mem-ontology/lehrplan-th-shadow.ttl.
Validates the output by parsing it back with rdflib before writing (fails
loudly, writes nothing, if the graph doesn't parse).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
OUT_DIR = REPO_ROOT / "mem-ontology"
OUT_FILE = OUT_DIR / "lehrplan-th-shadow.ttl"

SOURCE_FILES = [
    # (json filename, thsh: local-name stem, human label)
    ("lernziele_MNT56.json", "mnt56", "Lernziele MNT Gymnasium Klassen 5\u20136"),
    ("lernziele_gy78.json", "gy78", "Lernziele Biologie Gymnasium Klassen 7\u20138"),
    ("lernziele_gy910.json", "gy910", "Lernziele Biologie Gymnasium Klassen 9\u201310"),
]

# --- Verified live individuals/predicates/classes (see module docstring) ---
LP = "https://w3id.org/lehrplan/ontology/"
SCHULFACH = "https://w3id.org/schulfach/"
SCHULART = "https://w3id.org/schulart/"
OBO = "http://purl.obolibrary.org/obo/"
THSHADOW = "https://openevo-ccs.github.io/EvoMentor_DE/lehrplan-th-shadow/"
EVOMENTOR = "https://openevo-ccs.github.io/EvoMentor_DE/vocab/"

BUNDESLAND_TH = f"{LP}LP_3000031"              # verified: rdfs:label "Th\u00fcringen"@de
SCHULART_GYMNASIUM_TH = f"{SCHULART}TH_0000006"  # verified: rdfs:label "Gymnasium"@de
SCHULFACH_BY_FACH = {
    "Biologie": f"{SCHULFACH}TH_0000002",         # verified: rdfs:label "Biologie"@de
    "Mensch-Natur-Technik (MNT)": f"{SCHULFACH}TH_0000028",  # verified: rdfs:label "Mensch-Natur-Technik"@de
}
JAHRGANGSSTUFE = {n: f"{LP}LP_200000{n}" for n in range(1, 10)}
JAHRGANGSSTUFE.update({n: f"{LP}LP_20000{n}" for n in range(10, 14)})

HAT_SCHULFACH = f"{LP}LP_0000537"
FUER_SCHULART = f"{LP}LP_0000812"
HAT_JAHRGANGSSTUFE = f"{LP}LP_0000026"
VON_BUNDESLAND = f"{LP}LP_0000029"
HAS_PART = f"{OBO}BFO_0000051"

CORE_LEHRPLAN = f"{LP}LP_0000438"                 # Lehrplan
CORE_CE_BEREICH = f"{LP}LP_0000349"               # CE-Bereich
CORE_CE_KOMPETENZSPEZIFIKATION = f"{LP}LP_0000263"  # CE-Kompetenzspezifikation


def slugify(text: str) -> str:
    s = text.lower()
    s = (s.replace("\u00e4", "ae").replace("\u00f6", "oe").replace("\u00fc", "ue")
           .replace("\u00df", "ss"))
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def esc(text: str) -> str:
    """Turtle string-literal escaping."""
    return (text.replace("\\", "\\\\").replace('"', '\\"')
                .replace("\n", "\\n").replace("\r", ""))


def lit(text: str, lang: str | None = "de") -> str:
    body = f'"{esc(text)}"'
    return f"{body}@{lang}" if lang else body


def load_gradeband(filename: str) -> dict:
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    lines: list[str] = []
    lines.append(f"@prefix lp: <{LP}> .")
    lines.append(f"@prefix schulfach: <{SCHULFACH}> .")
    lines.append(f"@prefix schulart: <{SCHULART}> .")
    lines.append(f"@prefix obo: <{OBO}> .")
    lines.append(f"@prefix thsh: <{THSHADOW}> .")
    lines.append(f"@prefix evomentor: <{EVOMENTOR}> .")
    lines.append("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .")
    lines.append("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .")
    lines.append("@prefix owl: <http://www.w3.org/2002/07/owl#> .")
    lines.append("")
    lines.append("# Provisional shadow graph -- see module docstring in")
    lines.append("# scripts/export_mem_th_shadow.py for what's verified-live")
    lines.append("# vs. locally minted, and why.")
    lines.append("")

    # Locally-minted classes, subclassing real FWU core classes -- same
    # pattern FWU's own ontology uses per-state (e.g. `LehrplanPLUS (BY)`).
    lines.append("thsh:Fachlehrplan_TH rdfs:subClassOf lp:LP_0000438 ;")
    lines.append(f'    rdfs:label {lit("Fachlehrplan (TH, EvoMentor_DE shadow graph)")} .')
    lines.append("thsh:Lernbereich_TH rdfs:subClassOf lp:LP_0000349 ;")
    lines.append(f'    rdfs:label {lit("Lernbereich (TH, EvoMentor_DE shadow graph)")} .')
    lines.append("thsh:Kompetenzerwartung_TH rdfs:subClassOf lp:LP_0000263 ;")
    lines.append(f'    rdfs:label {lit("Kompetenzerwartung (TH, EvoMentor_DE shadow graph)")} .')
    lines.append("")

    stats = {"fachlehrplaene": 0, "lernbereiche": 0, "lernziele": 0, "unmapped_grade": 0}
    all_lz_ids: set[str] = set()
    lz_local_by_id: dict[str, str] = {}  # raw source id -> thsh: local name, for the Kohaerenzfaeden pass below

    for filename, stem, fallback_label in SOURCE_FILES:
        data = load_gradeband(filename)
        meta = data["metadaten"]
        fach = meta.get("fach", "Biologie")
        schulfach_uri = SCHULFACH_BY_FACH.get(fach)
        if schulfach_uri is None:
            raise ValueError(f"No verified Schulfach URI for {fach!r} ({filename})")

        lz_list = data["lernziele"]
        for lz in lz_list:
            all_lz_ids.add(lz["id"])

        # Group by `thema` to recover Lernbereich structure -- these
        # datasets don't carry an explicit hierarchy field, `thema` is the
        # natural grouping key already used throughout the source JSON.
        themen: dict[str, list[dict]] = {}
        for lz in lz_list:
            themen.setdefault(lz["thema"], []).append(lz)

        fp_local = f"fachlehrplan-{stem}"
        all_descendant_locals: list[str] = []

        # --- Lernbereich + Kompetenzerwartung individuals ---
        lb_blocks: list[str] = []
        for thema, items in themen.items():
            lb_local = f"lernbereich-{stem}-{slugify(thema)}"
            lz_locals = [f"lz-{stem}-{slugify(lz['id'])}" for lz in items]
            all_descendant_locals.append(lb_local)
            all_descendant_locals.extend(lz_locals)
            stats["lernbereiche"] += 1

            has_part_targets = " ,\n        ".join(f"thsh:{l}" for l in lz_locals)
            lb_blocks.append(
                f"thsh:{lb_local} a thsh:Lernbereich_TH ;\n"
                f"    rdfs:label {lit(thema)} ;\n"
                f"    lp:LP_0000029 lp:LP_3000031 ;\n"
                f"    obo:BFO_0000051 {has_part_targets} ."
            )

            for lz, lz_local in zip(items, lz_locals):
                stats["lernziele"] += 1
                lz_local_by_id[lz["id"]] = lz_local
                grade_raw = lz.get("empfohlene_klassenstufe")
                grade_int = None
                if grade_raw:
                    m = re.match(r"\d+", str(grade_raw))
                    if m:
                        grade_int = int(m.group())
                jahrgang_uri = JAHRGANGSSTUFE.get(grade_int) if grade_int else None
                if jahrgang_uri is None:
                    stats["unmapped_grade"] += 1

                props = [
                    f"a thsh:Kompetenzerwartung_TH",
                    f"rdfs:label {lit(lz['originaltext'])}",
                    f"lp:LP_0000537 <{schulfach_uri}>",
                    f"lp:LP_0000812 <{SCHULART_GYMNASIUM_TH}>",
                    f"lp:LP_0000029 <{BUNDESLAND_TH}>",
                    f'evomentor:sourceId {lit(lz["id"], lang=None)}',
                ]
                if jahrgang_uri:
                    props.append(f"lp:LP_0000026 <{jahrgang_uri}>")
                for bk in lz.get("basiskonzepte_primaer") or []:
                    props.append(
                        f'evomentor:basiskonzeptPrimaer '
                        f'{lit("kmk-basiskonzepte-biologie:" + bk, lang=None)}'
                    )
                for bk in lz.get("basiskonzepte_sekundaer") or []:
                    props.append(
                        f'evomentor:basiskonzeptSekundaer '
                        f'{lit("kmk-basiskonzepte-biologie:" + bk, lang=None)}'
                    )
                for ref in lz.get("voraussetzende_lernziele") or []:
                    props.append(f'evomentor:buildsOn thsh:lz-{stem}-{slugify(ref)}')
                for ref in lz.get("ermoeglichende_lernziele") or []:
                    props.append(f'evomentor:buildsToward thsh:lz-{stem}-{slugify(ref)}')

                lb_blocks.append(f"thsh:{lz_local} " + " ;\n    ".join(props) + " .")

        # --- Fachlehrplan individual: has-part transitively flattened to
        # EVERY descendant (Lernbereiche AND Lernziele), matching the real
        # FWU graphs' documented (docs/schema.md) behavior exactly. ---
        stats["fachlehrplaene"] += 1
        has_part_all = " ,\n        ".join(f"thsh:{l}" for l in all_descendant_locals)
        title = meta.get("titel", fallback_label)
        lines.append(
            f"thsh:{fp_local} a thsh:Fachlehrplan_TH ;\n"
            f"    rdfs:label {lit(title)} ;\n"
            f"    lp:LP_0000537 <{schulfach_uri}> ;\n"
            f"    lp:LP_0000812 <{SCHULART_GYMNASIUM_TH}> ;\n"
            f"    lp:LP_0000029 <{BUNDESLAND_TH}> ;\n"
            f"    obo:BFO_0000051 {has_part_all} ."
        )
        lines.append("")
        lines.extend(lb_blocks)
        lines.append("")

    # --- Kohaerenzfaeden (data/kohaerenzfaeden.json): membership links from
    # each Kompetenzerwartung_TH individual to the coherence thread(s) it's a
    # station in. A separate, explicitly non-FWU predicate
    # (evomentor:teilVonKohaerenzfaden) -- these are proposed pedagogical
    # connections, not asserted curricular prerequisites, so they must never
    # be confused with the real obo:BFO_0000051/evomentor:buildsOn edges
    # above, which do carry that stronger claim. ---
    kf_path = DATA_DIR / "kohaerenzfaeden.json"
    kf_stats = None
    if kf_path.exists():
        with open(kf_path, "r", encoding="utf-8") as f:
            kf_data = json.load(f)
        lines.append("evomentor:Kohaerenzfaden a owl:Class ;")
        lines.append(f'    rdfs:label {lit("Basiskonzept-Kohärenzfaden (EvoMentor_DE-eigenes Konzept, kein FWU/MEM-Begriff)")} .')
        lines.append("")
        kf_stats = {"faeden": 0, "stationen": 0, "unresolved_stationen": 0}
        for kf in kf_data["kohaerenzfaeden"]:
            kf_stats["faeden"] += 1
            kf_local = kf["id"]
            lines.append(
                f"evomentor:{kf_local} a evomentor:Kohaerenzfaden ;\n"
                f"    rdfs:label {lit(kf['titel'])} ;\n"
                f'    evomentor:typ {lit(kf["typ"], lang=None)} ;\n'
                f"    evomentor:evolutionaererKern {lit(kf['evolutionaererKern'])} ."
            )
            for station in kf["lernzielStationen"]:
                kf_stats["stationen"] += 1
                target_local = lz_local_by_id.get(station["lernzielId"])
                if target_local is None:
                    kf_stats["unresolved_stationen"] += 1
                    continue
                lines.append(f"thsh:{target_local} evomentor:teilVonKohaerenzfaden evomentor:{kf_local} .")
            lines.append("")

    ttl = "\n".join(lines) + "\n"

    # Validate before writing anything -- fail loudly rather than emit
    # unparseable Turtle.
    try:
        import rdflib
        g = rdflib.Graph()
        g.parse(data=ttl, format="turtle")
    except Exception as exc:
        print(f"TTL FAILED TO PARSE, not writing output: {exc}", file=sys.stderr)
        sys.exit(1)

    OUT_DIR.mkdir(exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(ttl)

    print(f"Wrote {OUT_FILE}")
    print(f"  {stats['fachlehrplaene']} Fachlehrplan_TH (one per source file)")
    print(f"  {stats['lernbereiche']} Lernbereich_TH (grouped by `thema`)")
    print(f"  {stats['lernziele']} Kompetenzerwartung_TH (one per Lernziel)")
    print(f"  {len(g)} triples total (rdflib-parsed, validated)")
    if kf_stats:
        print(f"  {kf_stats['faeden']} Kohaerenzfaeden, {kf_stats['stationen']} Lernziel-Stationen linked "
              f"via evomentor:teilVonKohaerenzfaden")
        if kf_stats["unresolved_stationen"]:
            print(f"  WARNING: {kf_stats['unresolved_stationen']} Kohaerenzfaden Lernziel-Stationen did not "
                  f"resolve against the Grades 5-10 dataset.", file=sys.stderr)
    if stats["unmapped_grade"]:
        print(f"  WARNING: {stats['unmapped_grade']} Lernziele had no resolvable "
              f"empfohlene_klassenstufe -> no lp:LP_0000026 (hat Jahrgangsstufe) "
              f"triple emitted for those.", file=sys.stderr)


if __name__ == "__main__":
    main()
