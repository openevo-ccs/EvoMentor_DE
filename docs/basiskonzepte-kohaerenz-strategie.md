# Strategie: Basiskonzept-Kohärenzfäden als Treiber horizontaler und vertikaler Kohärenz (Klassen 5–10)

**Status:** Erste Umsetzung, datengetrieben, validiert. **Daten:**
[`data/kohaerenzfaeden.json`](../data/kohaerenzfaeden.json) (4 Fäden, validiert
gegen [`schema/kohaerenzfaden.schema.json`](../schema/kohaerenzfaden.schema.json)).
**Verwandte Artefakte:** [`data/basiskonzepte.json`](../data/basiskonzepte.json)
(die `bk_verbindungen`, die diese Strategie als Ausgangspunkt nimmt),
conceptbase RFC-0018 (`frameworkRelation.schema.yaml`, dasselbe kontrollierte
Vokabular), [`mem-ontology/`](../mem-ontology/) (die Fäden sind dort als
`evomentor:teilVonKohaerenzfaden`-Kanten queryable).

---

## 1. Das Prinzip: Evolution als Nabe, nicht als Speiche

`basiskonzepte.json` v4.1 macht explizit, dass jedes der vier
Nicht-Evolutions-Basiskonzepte (Struktur/Funktion, Stoff-/Energieumwandlung,
Information/Kommunikation, Steuerung/Regelung) eine `wird_erklaert_durch`-
Beziehung zu Individuelle/Evolutive Entwicklung hat — nicht nur umgekehrt.
Das ist mehr als eine Datenmodellierungs-Feinheit: es ist die formale
Voraussetzung für die eigentliche Strategie dieses Dokuments.

**Die Falle, die dieses Dokument vermeiden soll:** "mehr Basiskonzepte pro
Stunde abdecken" ist KEIN Kohärenzgewinn. Eine Stunde, die beiläufig
Struktur/Funktion, Stoff/Energie und Evolution erwähnt, ohne zu erklären,
*warum* diese drei zusammenhängen, produziert Themenhäufung, keine Kohärenz.
Kohärenz entsteht erst, wenn Evolution explizit als das gemeinsame
Erklärungsprinzip benannt wird, das mehrere Basiskonzepte gleichzeitig
verständlich macht — die Dobzhansky-Position operationalisiert, nicht nur
zitiert.

Konkret: jeder Kohärenzfaden in diesem Dokument beantwortet eine Frage der
Form *"Warum tauchen X, Y und Z in genau dieser Reihenfolge/Verbindung auf,
und was hat Evolution damit zu tun?"* — nicht nur *"Welche Basiskonzepte
kommen hier vor?"*.

---

## 2. Empirische Grundlage: was in den echten Daten tatsächlich da ist

Alle Zahlen unten wurden direkt aus `data/lernziele_MNT56.json`,
`lernziele_gy78.json` und `lernziele_gy910.json` berechnet (271 Lernziele,
Klassen 5–10), nicht angenommen. Reproduzierbar mit den Methoden in Abschnitt 4.

| Befund | Zahl | Bedeutung |
|---|---|---|
| Lernziele, die Evolution UND ein anderes Basiskonzept taggen (primär oder sekundär) | 95 / 271 (35 %) | Ein latentes Kohärenz-Rückgrat existiert bereits in allen Klassenstufen 5–10, ist aber nicht als Erklärungsfaden ausformuliert |
| Basiskonzept-überschreitende `ermoeglichende_lernziele`-Kanten (A primär BK-X ermöglicht B primär BK-Y, X≠Y) | 138 | Echte Sequenzierungsbrücken zwischen Basiskonzepten existieren bereits in der Lehrplanlogik |
| ... davon mit Evolution als Quelle oder Ziel | 53 | Über ein Drittel der Basiskonzept-Übergänge führt direkt durch Evolution |
| **Klassenstufen-übergreifende (dateiübergreifende) `voraussetzende_lernziele`/`ermoeglichende_lernziele`-Referenzen** | **0** | **Der zentrale Befund: vertikale Kohärenz über Klassenstufen hinweg ist strukturell nicht kodiert — nur über gemeinsame `unterthema`-Stichworte indirekt erkennbar** |
| Datenqualitätsfund (behoben) | 1 | `GY-910-GEN-WGE-3` trug den nicht-kanonischen Tag `bk_individuelle_entwicklung` statt `bk_individuelle_evolutive_entwicklung` — korrigiert in `lernziele_gy910.json` |

Der Null-Befund bei klassenstufen-übergreifenden Referenzen ist der
eigentliche Auftrag dieser Strategie: **vertikale Kohärenz muss aktiv
konstruiert werden, sie ergibt sich nicht von selbst aus der vorhandenen
Sequenzierungslogik**, die ausschließlich innerhalb einer Klassenstufen-Datei
denkt.

---

## 3. Vier echte, datengetriebene Kohärenzfäden

Vollständige Daten inkl. Basiskonzept-Pfad, Lernziel-Stationen,
Kohärenzerklärung und Unterrichtsimpuls in
[`data/kohaerenzfaeden.json`](../data/kohaerenzfaeden.json). Zusammenfassung:

| ID | Typ | Spannweite | Evolutionärer Kern |
|---|---|---|---|
| `kf-001-mensch-in-der-natur` | vertikal | Kl. 6 → Kl. 10 | Naive Bewertung menschlicher Eingriffe (Kl. 6) wird durch formale Hominisationstheorie (Kl. 10) neu beantwortet — inklusive biologischer Widerlegung des Rassenkonzepts |
| `kf-002-fortpflanzung-lebensgeschichte` | vertikal-horizontal | Kl. 5 → 6 → 8 | Fortpflanzungsstrategien bei Pflanze, Wirbeltier und Mensch als artspezifische Life-History-Lösungen desselben evolutionären Trade-offs |
| `kf-003-zelle-enzym-immun-puberaet` | horizontal | Kl. 7–8, eine reale `ermoeglichende_lernziele`-Kette | Das Schlüssel-Schloss-Prinzip als ein einziger evolvierter Mechanismus, wiederverwendet in Verdauung, Immunabwehr und Hormonsteuerung (Exaptation) |
| `kf-004-vergleichende-anatomie-insekt-mensch` | horizontal | Kl. 7–8, zwei reale Ermöglichungskanten | Analogie (Tracheen/Lunge) vs. Homologie (Nervensystem) am Insekt-Mensch-Vergleich |

Jeder Faden ist **an echte Lernziel-IDs verankert** (nicht hypothetisch),
**gegen `kohaerenzfaden.schema.json` validiert** und **gegen die
Basiskonzept-Ids in `basiskonzepte.json` sowie die Lernziel-IDs in den
Quelldateien geprüft** (0 hängende Referenzen, siehe Validierungslauf in der
Commit-Historie).

---

## 4. Methode: wie weitere Fäden gefunden werden (reproduzierbar)

Drei Data-Mining-Verfahren, alle über die 271 Lernziele lauffähig:

1. **Ko-Vorkommen-Analyse.** Für jedes Lernziel: `basiskonzepte_primaer ∪
   basiskonzepte_sekundaer`. Wo Evolution mit einem anderen Basiskonzept
   gemeinsam auftritt, ist ein potenzieller Fadenpunkt markiert (95 Treffer).
2. **Basiskonzept-überschreitende Ermöglichungsketten-Suche.** Für jedes
   Lernziel A mit primärem Basiskonzept X: folge `ermoeglichende_lernziele`
   zu B; wenn B ein anderes primäres Basiskonzept Y hat, ist A→B eine reale,
   im Lehrplan bereits sequenzierte Brücke (138 Treffer, 53 mit Evolution
   beteiligt). Das ist die stärkste Evidenzform für einen **horizontalen**
   Faden, weil die Reihenfolge nicht didaktisch konstruiert, sondern in den
   Quelldaten bereits vorgesehen ist.
3. **`unterthema`-Stichwortabgleich über Klassenstufen-Dateien hinweg.** Da
   klassenstufen-übergreifende Prerequisite-Kanten fehlen (Befund oben), ist
   dies der einzige Weg, **vertikale** Kandidaten zu finden: gemeinsame
   inhaltstragende Wörter in `unterthema` zwischen `lernziele_MNT56.json`,
   `lernziele_gy78.json` und `lernziele_gy910.json` (z. B. "Entwicklung" in
   "Fortpflanzung und Entwicklung der Samenpflanzen" [Kl. 5] und
   "Fortpflanzung, Entwicklung und Sexualität" [Kl. 8]; "Menschen" in "Die
   Rolle des Menschen in der Natur" [Kl. 6] und "Evolution des Menschen"
   [Kl. 10]).

Ein vierter Schritt ist zwingend und nicht automatisierbar: **jeder
Kandidat aus (1)–(3) braucht eine von einer Fachperson geschriebene
`kohaerenzErklaerung`**, die tatsächlich erklärt, warum die Stationen
zusammenhängen — die drei Verfahren liefern nur Kandidaten, keine fertigen
Fäden. (`kf-003`s `luecken`-Feld und `kf-004`s `luecken`-Feld dokumentieren
zwei Stellen, an denen genau das noch aussteht.)

---

## 5. Wie das horizontale UND vertikale Kohärenz konkret treibt

**Horizontal (innerhalb einer Klassenstufe):** `kf-003` und `kf-004` zeigen,
dass echte, bereits im Lehrplan sequenzierte Übergänge zwischen
Basiskonzepten (Zellstruktur → Enzymfunktion → Immunsystem → Pubertät;
Insektenanatomie → Menschenanatomie) bislang nur als Aufgabenreihenfolge
existieren, nicht als benannte Erklärungslogik. Der Hebel ist klein und
konkret: an der Stelle, wo die Ermöglichungskante bereits existiert, einen
`unterrichtsimpuls` einbauen, der die Basiskonzept-Wechsel explizit macht
(siehe die vier `unterrichtsimpuls`-Felder in `kohaerenzfaeden.json`).

**Vertikal (über Klassenstufen hinweg):** `kf-001` und `kf-002` schließen
eine Lücke, die in den Rohdaten strukturell nicht existiert (0
dateiübergreifende Referenzen). Der Hebel ist größer: Lehrkräfte der
höheren Klassenstufe (9/10) müssten aktiv auf die entsprechenden Lernziele
der Klassenstufe 5/6/7/8 zurückgreifen — was ohne diese explizite
Verknüpfung praktisch nie passiert, weil die Lehrpläne pro Klassenstufen-Heft
gedacht und unterrichtet werden. `kf-001`s Unterrichtsimpuls (die
Klasse-6-Aufgabe in Klasse 10 wörtlich wieder vorlegen) ist das direkteste
Beispiel für diesen Mechanismus.

**Der eigentliche Hebel für Skalierung:** sobald ein Basiskonzept in Klasse
9/10 formal als "Evolution" behandelt wird (wie im `Evolution`-Thema in
`lernziele_gy910.json`, 12 Lernziele), sollte die Unterrichtsplanung
systematisch prüfen, welche früheren Lernziele (Kl. 5–8) implizit bereits
Ko-Vorkommen mit `bk_individuelle_evolutive_entwicklung` hatten (die 95
Treffer aus Abschnitt 2) — diese sind die Kandidatenliste für "Rückblicke",
die aus einer additiven Evolutions-Einheit eine echte Integrations-Einheit
machen.

---

## 6. Kompatibilität mit den bestehenden Datenformaten

Diese Strategie fügt **kein neues, inkompatibles Vokabular** hinzu:

- `basiskonzeptPfad[].basiskonzeptTag` verwendet exakt dasselbe
  `kmk-basiskonzepte-biologie:bk_...`-Format wie RFC-0018
  (`framework-relations/KMK-BASISKONZEPTE-BIOLOGIE-RELATIONS-v1.0.0.yaml`)
  und die MEM-Schattengraph-Literale (`evomentor:basiskonzeptPrimaer`).
- `basiskonzeptPfad[].relationTypeZumNaechsten` verwendet exakt dasselbe
  kontrollierte 10-Term-Vokabular wie RFC-0018s
  `frameworkRelation.schema.yaml` (`enables`, `requires`, `regulates`,
  `isRegulatedBy`, `implements`, `isImplementedBy`, `controls`,
  `isControlledBy`, `explainsOriginOf`, `isExplainedBy`) — keine neue
  Relationstypologie.
- `lernzielStationen[].lernzielId` sind die rohen Quell-IDs, identisch zu
  `basiskonzepte.json`s eigenen `lernziel_ids_thuringia`-Arrays. Daraus
  mechanisch ableitbar: `em-item:thuringia-{id.lower()}` (EvoMentor v2
  canonical items) und `thsh:lz-{gradeband}-{slug}` (MEM-Schattengraph).
- Der MEM-Schattengraph (`mem-ontology/lehrplan-th-shadow.ttl`) wurde
  erweitert (`scripts/export_mem_th_shadow.py`): jede
  `Kompetenzerwartung_TH`, die Station eines Fadens ist, trägt jetzt
  `evomentor:teilVonKohaerenzfaden` zu einem `evomentor:Kohaerenzfaden`-
  Individuum. Bewusst ein **anderes, schwächeres Prädikat** als
  `obo:BFO_0000051`/`evomentor:buildsOn` — Fadenzugehörigkeit ist ein
  vorgeschlagener didaktischer Zusammenhang, keine im Lehrplan real
  bestehende Voraussetzungsbeziehung, und darf mit dieser nicht verwechselt
  werden.

Keine Duplizierung: die Basiskonzept-Definitionen selbst bleiben allein in
`basiskonzepte.json`; die kontrollierte Relationstypologie bleibt allein in
RFC-0018; dieses Dokument und `kohaerenzfaeden.json` referenzieren beide,
statt sie neu zu erfinden.

---

## 7. Nächste Schritte

1. **App:** `apps/explore.html`s "Kohärenzfaden"-Toggle zeigt aktuell nur
   die paarweisen `wird_erklaert_durch`/`erklaert_entstehung_von`-Kanten
   zwischen den 5 Basiskonzepten. Eine natürliche Erweiterung: eine
   "Fadenansicht", die einen konkreten `kf-...`-Faden auswählt und seine
   `lernzielStationen` (über Klassenstufen hinweg, nicht nur Basiskonzepte)
   im Netz hervorhebt — technisch ein zusätzlicher Datensatz-Import
   (`data/kohaerenzfaeden.json`) plus ein neuer Filtermodus, kein
   struktureller Umbau der bestehenden `renderNet()`-Logik.
2. **Lücken schließen:** `kf-003` und `kf-004` markieren explizit fehlende
   Klasse-9/10-Anschlussstellen (Enzym/Immunsystem-Vertiefung;
   Homologie/Analogie-Begriffseinführung). Das sind die konkretesten,
   kleinsten nächsten Content-Ergänzungen.
3. **Weitere Fäden:** die Methode aus Abschnitt 4 ist auf alle 95
   Ko-Vorkommen-Kandidaten und 138 Ermöglichungskanten anwendbar, nicht nur
   auf die vier hier ausgearbeiteten — dies ist ein Startsatz, kein
   vollständiger Katalog.
4. **KoMet:** diese vier Fäden sind ein zweites, kleineres Analogon zum
   "einen konkreten interdisziplinären Kohärenz-Demo", den
   `KoMet/Docs/KoMet_Grant_Strategy_and_Monitoring_Plan.md` §3 als
   fehlendes, überzeugendstes Beweisstück nennt — hier allerdings
   intra-fachlich (innerhalb Biologie) und bereits vollständig mit echten
   Lernzieldaten hinterlegt, nicht nur konzipiert.
