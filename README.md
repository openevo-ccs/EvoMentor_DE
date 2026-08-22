# EvoMentor - Deutsch
#### Digitale Werkzeuge zur Integration von Evolution im Biologieunterricht

[![OpenEvo](https://img.shields.io/badge/OpenEvo-openevo.eva.mpg.de-teal)](http://openevo.eva.mpg.de) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📘 Überblick

**EvoMentor - Deutsch** ist die deutschsprachige Version des EvoMentor-Projekts des [OpenEvo CCS Labs](http://openevo.eva.mpg.de). Ziel des Projekts ist es, praktische und effiziente digitale Werkzeuge zu entwickeln und bereitzustellen, die mithilfe von KI konzipiert wurden, für die Endnutzenden jedoch keine KI voraussetzen.

Im Mittelpunkt steht die **Integration von Evolution als zentrales Thema im Biologieunterricht** – sowie als fächerübergreifendes Leitthema in verschiedenen Schulfächern und Klassenstufen.

Die aktuelle Version enthält mehrere Apps, die darauf ausgerichtet sind, evolutionäre Konzepte in den **Biologielehrplan der Klassen 5–10 im Bundesland Thüringen** einzubetten. Mittelfristig planen wir, das Angebot auf weitere deutschsprachige Bundesländer, Klassenstufen und Unterrichtsfächer auszuweiten.

---

## 🎯 Projektziele

- **Evolution als roten Faden** im Biologieunterricht sichtbar machen
- Lehrkräfte bei der **Lehrplanintegration** evolutionärer Konzepte unterstützen
- **Fächerübergreifende Verbindungen** zu Evolution aufzeigen und fördern
- Digitale Werkzeuge bereitstellen, die **ohne KI-Kenntnisse** nutzbar sind, aber von KI-gestützter Entwicklung profitieren
- Schrittweise Ausweitung auf alle **deutschsprachigen Bundesländer**

---

## 🗂️ Aktuelle Inhalte

| Datensatz | Beschreibung | Bundesland | Klassenstufe | Fach |
|---|---|---|---|---|
| EvoMentor Thüringen 5–10 | Integration von Evolution in den Biologie-/MNT-Lehrplan | Thüringen | 5–10 | Biologie, MNT |

> Weitere Datensätze für andere Bundesländer, Klassenstufen und Fächer sind in Planung.

---

## 🖥️ Alle Apps

Alle Apps sind eigenständige HTML-Dateien ohne Build-Schritt — direkt über GitHub Pages nutzbar, kein Download nötig. Mehrere Versionsstände sind parallel verfügbar (siehe Spalte „Stand"), damit ältere Auswertungen und Exporte nachvollziehbar bleiben.

| App | Beschreibung | Stand |
|---|---|---|
| [🧭 LehrplanKompass](https://openevo-ccs.github.io/EvoMentor_DE/apps/index.html) | **Aktuelles Hauptwerkzeug.** Vereint Konzept-Explorer (Konzeptnetz mit Kohärenzfaden-Ansicht, Dashboard, Detailansicht) und Sequenzplaner (Jahresplanung, Qualitätsanalyse, Export) in einer Oberfläche | v4.0 (aktuell) |
| [🗺️ LehrplanNavigator](https://openevo-ccs.github.io/EvoMentor_DE/apps/lehrplannavigator.html) | Eigenständige Einzeldatei-Variante von LehrplanKompass — Konzeptnetz und Sequenzplaner in einer HTML-Datei ohne iframe-Aufbau | — |
| [📋 EvoMentor DE v1.1](https://openevo-ccs.github.io/EvoMentor_DE/apps/evomentor_de_v1_1.html) | Lernziel-Browser mit Filtern, eigenen Tags, Favoriten, Notizen, KI-Prompt-Generierung und Export; deckt Klassen 5–10 ab | v1.1 |
| [📋 EvoMentor DE v1.0](https://openevo-ccs.github.io/EvoMentor_DE/apps/evomentor_de.html) | Vorläuferversion desselben Lernziel-Browsers, aus dem ursprünglichen Prototyp-Repository | v1.0 |
| [🧬 Evolutionsbezug Biologie](https://openevo-ccs.github.io/EvoMentor_DE/apps/lernziele_evolution.html) | Übersicht der Evolutionsbezüge einzelner Lernziele (Klassen 7–8) mit wissenschaftlicher Begründung | — |
| [🤖 Evolutionsbezug – LLM-Prompter](https://openevo-ccs.github.io/EvoMentor_DE/apps/lernziele_evolution_llmprompter.html) | Wie oben, zusätzlich mit Generierung von KI-Prompts zur Unterstützung der Evolutionsintegration | — |

> Der Konzept-Explorer (`apps/explore.html`) und der Sequenzplaner (`apps/sequenz.html`) sind als eigene Ansichten in LehrplanKompass eingebettet, lassen sich aber auch direkt öffnen.

## 🧵 Basiskonzept-Kohärenzfäden

[`docs/basiskonzepte-kohaerenz-strategie.md`](docs/basiskonzepte-kohaerenz-strategie.md)
beschreibt, wie die Beziehungen zwischen den fünf KMK-Basiskonzepten (v. a.
"wird durch Evolution erklärt") datengetrieben genutzt werden, um horizontale
und vertikale Kohärenz über die Klassenstufen 5–10 hinweg herzustellen — mit
vier vollständig ausgearbeiteten, an echte Lernziele verankerten Fäden in
[`data/kohaerenzfaeden.json`](data/kohaerenzfaeden.json).

---

## 🗺️ Geplante Erweiterungen

- 📍 **Weitere Bundesländer:** Bayern, Berlin, Sachsen, u. a.
- 📚 **Weitere Klassenstufen:** Klassen 5–6, 9–10, gymnasiale Oberstufe
- 🔬 **Weitere Fächer:** Geographie, Chemie, Ethik, Geschichte u. a.

---

## 🧩 Das CCS Lab Ökosystem

Dieses Repository ist ein Bestandteil des umfassenderen **Computational Curriculum Studies (CCS) Labs**, das folgende Komponenten umfasst:

- **CCS Graph:** Konzepte, Theorien, Methoden und Maßnahmen, die mögliche Richtungen der CCS-Forschung abbilden
- **OpenEvo Graph:** Konzepte, Theorien, Methoden und Ressourcen, die das OpenEvo-Bildungsdesignkonzept und Forschungsmodell beschreiben
- **Werkzeuge zur Lehrplangestaltung**
- **Metadaten, Provenienz sowie offene und FAIR-Datenpipelines**

Weitere Informationen finden Sie auf der [OpenEvo CCS Website](http://openevo.eva.mpg.de/projectbase/ccs).

---

## 🚀 Erste Schritte

```bash
# Repository klonen
git clone https://github.com/openevo-ccs/EvoMentor_DE.git

# In das Projektverzeichnis wechseln
cd EvoMentor_DE
```

Öffnen Sie [`apps/index.html`](apps/index.html) direkt im Browser — die Apps sind
eigenständige HTML-Dateien ohne Build-Schritt oder Server. Da die Apps ihre
Daten per `fetch()` nachladen, funktionieren sie über GitHub Pages
zuverlässiger als über `file://` — siehe die Linkliste weiter oben unter
„🖥️ Alle Apps".

---

## 🤝 Mitwirken

Beiträge sind herzlich willkommen! Wenn Sie Ideen, Fehlerberichte oder Vorschläge haben, öffnen Sie bitte ein [Issue](https://github.com/openevo-ccs/EvoMentor_DE/issues) oder reichen Sie einen Pull Request ein.

Bitte beachten Sie unsere [Beitragsrichtlinien](CONTRIBUTING.md).

---

## 📄 Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).

---

## 📬 Kontakt

OpenEvo CCS Lab
🌐 [openevo.eva.mpg.de](http://openevo.eva.mpg.de)

---

*Entwickelt mit ❤️ für den deutschsprachigen Biologieunterricht.*