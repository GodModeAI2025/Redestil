# RedenSkill

**Sprach-DNA-Extraktion, Reden-Generator und selbstlernende Feedback-Schleife.**

Ein Claude Code Skill der den individuellen Redestil eines Sprechers aus Beispielreden extrahiert, quantifiziert und reproduzierbar macht. Neue Reden werden nicht einfach "im Stil von" generiert — sie werden gegen ein messbares Stilprofil validiert und iterativ verfeinert.

---

## Was ist das?

RedenSkill kombiniert zwei Ansätze:

1. **Quantitative Stilanalyse** (Python + spaCy) — 47 messbare Dimensionen: Satzlänge, Vokabularreichtum, rhetorische Figuren, Interpunktion, Grammatik-Profile, Lesbarkeit
2. **Qualitative Stilanalyse** (Claude) — Tonalität, Argumentationsmuster, Bildsprache, Aufbau-Architektur, Anti-Patterns

Das Ergebnis ist eine **Sprach-DNA**: ein vollständiges, belegtes Stilprofil das als Generierungsgrundlage dient. Generierte Reden werden automatisch gegen die DNA-Metriken validiert (Score 0-100) und iterativ nachgebessert.

Der Feedback-Modus schließt den Kreis: Korrekturen werden analysiert, die DNA wird aktualisiert, und akkumulierte Learnings fließen in jede weitere Generierung ein. Ein Stil-Check prüft ob eine Rede zum Profil passt — und ob sie als Trainingsmaterial geeignet ist.

---

## Fünf Modi

### Modus 1: Sprach-DNA erstellen

```
Beispielreden + Quellen → Konvergenz-Check → Python-Analyse → Claude-Analyse → SPRACH-DNA.md
```

- **Konvergenz-Diagnose**: Prüft inkrementell ob genug Reden vorliegen — zeigt pro Rede ob sie den Stil ERWEITERT, VERFEINERT oder BESTÄTIGT hat
- Python extrahiert quantitative Metriken (Satzlänge, TTR, Rhetorik, POS, ...)
- Claude analysiert qualitative Dimensionen (Tonalität, Argumentation, Bildsprache, ...)
- Ergebnis: Ein 15-Abschnitte-Stilprofil mit Belegen und Zielwerten

### Modus 2: Rede generieren

```
DNA + Learnings + Briefing + Quellen → Gliederung → Generierung → Validierung → Rede
```

- Briefing aufnehmen (Thema, Zielgruppe, Kernbotschaft, Länge)
- Learnings aus bisherigem Feedback automatisch mitlesen
- Gliederung nach DNA-Blueprint erstellen
- Rede abschnittsweise generieren (DNA + Learnings als Stil-Constraint)
- Python validiert gegen Metriken (Score 0-100)
- Iterative Verfeinerung bis Score ≥ 85

### Modus 3: Feedback & Lernen

```
Feedback/Korrektur → Delta-Analyse → DNA-Update → Learnings speichern
```

- Akzeptiert Text-Feedback ("zu formell") oder überarbeitete Reden
- Python berechnet Deltas zwischen Original und Korrektur
- Identifiziert welche DNA-Dimensionen angepasst werden müssen
- Speichert konkrete Regeln als Learnings (`LEARNINGS-{Name}.md`)
- Learnings haben Vorrang vor generischen DNA-Zielwerten

### Modus 4: Stil-Check

```
Rede + DNA → Quantitativer Vergleich + Qualitative Analyse → Authentizitäts-Verdikt
```

- Prüft ob eine Rede zum DNA-Profil passt (Score + Verdikt)
- Identifiziert konkrete Abweichungen mit Zitaten
- Verdikt: Authentisch (≥85) / Teilweise passend (60-84) / Stilfremd (<60)
- Bei hoher Übereinstimmung: Rede als Trainingsmaterial übernehmen
- Bei Abweichungen: Gezielt nachbessern oder DNA erweitern

### Modus 5: Skill exportieren

- Exportiert die aktuelle Skill-Version als lesbares Paket

---

## Installation

### Voraussetzungen

- Python 3.9+
- Claude Code (CLI, Desktop App, oder IDE Extension)
- ~600 MB Speicherplatz (für spaCy-Modell)

### Setup

```bash
git clone <repository-url> RedenSkill
cd RedenSkill
bash scripts/setup.sh
```

Das Setup-Script installiert:
- **spaCy** (NLP-Bibliothek, MIT-Lizenz)
- **de_core_news_lg** (deutsches Sprachmodell, MIT-Lizenz)
- **textstat** (Lesbarkeits-Indizes)

### Manuelles Setup (alternativ)

```bash
pip install -r scripts/requirements.txt
python -m spacy download de_core_news_lg
```

---

## Nutzung

### Schritt 1: Material ablegen

**Beispielreden** (mindestens 3, je mehr desto besser) in `archive/beispielreden/`:

```
archive/beispielreden/
├── keynote-jahreskonferenz.txt
├── ansprache-teammeeting.md
├── gruswort-kundenveranstaltung.txt
├── rede-strategietag.txt
└── impulsvortrag-innovation.md
```

**Referenzquellen** (optional) in `archive/quellen/`:

```
archive/quellen/
├── marktstudie-2025.txt
├── kundenfeedback-zusammenfassung.md
├── branchenzahlen.txt
└── zitate-sammlung.md
```

Unterstützte Formate: `.txt` und `.md` (Markdown wird automatisch bereinigt).

### Sprechdauer angeben

Du kannst die Reden-Länge in **Minuten** angeben — der Skill rechnet automatisch um (Standard: 130 Wörter/Minute, anpassbar):

| Dauer | Wörter |
|-------|--------|
| 3 Min | ~390 |
| 5 Min | ~650 |
| 10 Min | ~1.300 |
| 15 Min | ~1.950 |
| 20 Min | ~2.600 |
| 30 Min | ~3.900 |

### Schritt 2: Skill starten

In Claude Code, im RedenSkill-Verzeichnis:

```
/project:reden
```

Es erscheint die Modus-Auswahl.

### Schritt 3: Workflow durchlaufen

**Erster Durchlauf:**
1. Modus 1 → Sprach-DNA erstellen
2. Modus 2 → Erste Rede generieren
3. Modus 3 → Feedback geben, DNA + Learnings aufbauen

**Danach:**
- Direkt Modus 2 für neue Reden (DNA + Learnings werden mitgelesen)
- Modus 3 nach jeder Rede die korrigiert wird
- Modus 4 um externe Reden auf Stil-Passung zu prüfen

---

## Projektstruktur

```
RedenSkill/
├── .claude/
│   └── commands/
│       └── reden.md                ← Skill-Definition + Orchestrator
├── references/
│   ├── sprach-dna-template.md      ← Vollständiges DNA-Template
│   ├── generierung-regeln.md       ← Qualitäts-Regeln mit Begründungen
│   └── beispiele.md                ← Input→Output Beispiele
├── scripts/
│   ├── analyze_style.py            ← Haupt-Orchestrator (Metriken + Rhetorik)
│   ├── diagnose_convergence.py     ← Konvergenz-Diagnose (genug Reden?)
│   ├── extract_metrics.py          ← 47 quantitative Stil-Dimensionen
│   ├── detect_rhetoric.py          ← Rhetorische Figuren erkennen
│   ├── validate_speech.py          ← Generierte Rede validieren (Score)
│   ├── compare_feedback.py         ← Feedback-Delta-Analyse
│   ├── requirements.txt
│   └── setup.sh
├── archive/
│   ├── beispielreden/              ← Hier Beispielreden ablegen
│   └── quellen/                    ← Hier Referenzquellen ablegen
├── output/
│   ├── sprach-dna/                 ← Stilprofile + Metriken + Learnings
│   └── reden/                      ← Generierte Reden + Validierungsreports
├── CLAUDE.md
├── README.md
└── index.html                      ← Landingpage / Dokumentation
```

---

## Was die Sprach-DNA erfasst

### Quantitativ (Python — 47 Dimensionen)

| Kategorie | Beispiel-Metriken |
|-----------|-------------------|
| **Satzebene** | Ø Satzlänge, Satztypen-Mix (Aussage/Frage/Ausruf), Satzanfänge, Stakkato-Quote |
| **Wortebene** | Type-Token-Ratio, Hapax-Legomena, Füllwort-Profil, Modalverb-Frequenz, Top-50 Signalwörter |
| **Pronomen** | Ich/Wir/Sie-Verteilung, Wir/Ich-Verhältnis |
| **Interpunktion** | Gedankenstriche, Ellipsen, Fragezeichen, Kommas (je pro 1000 Wörter) |
| **Lesbarkeit** | Flesch-Index (deutsch), Silben/Wort, Lange-Wörter-Anteil |
| **Grammatik** | Aktiv/Passiv-Verhältnis, Tempus-Verteilung, POS-Profil, Adjektiv-Dichte |
| **Rhetorik** | Anaphern, Trikola, Rhetorische Fragen, Antithesen, Epiphern (je pro 1000 Wörter) |

### Qualitativ (Claude — 8 Dimensionen)

| Dimension | Was erfasst wird |
|-----------|-----------------|
| **Tonalität** | Formalitätsgrad, emotionale Temperatur, Autoritätsstil, Humor, Empathie |
| **Argumentation** | Muster (deduktiv/induktiv/narrativ), Evidenz-Präferenz, Logos/Pathos/Ethos |
| **Aufbau** | Eröffnungstechnik, Übergänge, Spannungsbogen, Schluss-Technik, Proportionen |
| **Zielgruppe** | Anrede-Muster, Inklusion, Vorwissen-Annahme, Appell-Frequenz |
| **Bildsprache** | Metaphern-Dichte, Bildfelder, Vergleiche, Abstrakt/Konkret |
| **Rhythmus** | Sprechbarkeit, Pausen, Emphase-Wiederholungen, Atem-Einheiten |
| **Quellen-Stil** | Zitat-Einbau, Quellennennung, Daten-Präsentation |
| **Anti-Patterns** | Was bewusst NICHT getan wird |

---

## Validierungs-System

Jede generierte Rede wird automatisch gegen die DNA-Metriken geprüft:

```
Dimension                        Ziel     Ist      Abw.    Status
──────────────────────────────── ──────── ──────── ──────── ──────
Satzlänge (Ø Wörter)              14.2     15.8     11.3%  ✓
Stakkato-Quote                     18.0     12.0     33.3%  ⚠️
Type-Token-Ratio                    0.42     0.45      7.1%  ✓
Aktiv-Anteil (%)                   78.0     74.0      5.1%  ✓
Flesch-Index                       52.0     48.0      7.7%  ✓

STIL-ÜBEREINSTIMMUNG: 82/100  (9/11 Dimensionen im Toleranzbereich)
→ Gute Übereinstimmung, einzelne Dimensionen weichen ab
```

Scoring:
- **≥ 85**: Sehr gute Übereinstimmung
- **70-84**: Gut, einzelne Abweichungen
- **50-69**: Moderat, Überarbeitung empfohlen
- **< 50**: Niedrig, Rede sollte überarbeitet werden

---

## Konvergenz-Diagnose

Bevor die DNA erstellt wird, prüft der Skill automatisch ob genug Material vorliegt. Jede Rede wird inkrementell hinzugefügt und ihr Einfluss auf die Gesamtmetriken gemessen:

```
KONVERGENZ-DIAGNOSE
════════════════════════════════════════════════════

Rede 1-2: Basis-Analyse (keynote-maerz.txt, 820 Wörter)

Rede 3 "gruswort-juni.txt" (450 Wörter):
  Metriken-Drift:     Ø 12.3% (4 signifikante Shifts)
  Neue Signalwörter:  +8 (innovation, wandel, zukunft...)
  Neue Rhetorik:      trikolon
  🔵 Bewertung:        Diese Rede hat den Stil ERWEITERT

Rede 4 "ansprache-herbst.txt" (680 Wörter):
  Metriken-Drift:     Ø 4.2% (1 signifikanter Shift)
  Neue Signalwörter:  +2
  Neue Rhetorik:      keine neuen Muster
  🟢 Bewertung:        Diese Rede hat den Stil BESTÄTIGT

🟢 GESAMTBEWERTUNG: STABIL
   DNA konvergiert (Ø Shift der letzten Reden: 4.2%). 4 Reden sind eine solide Basis.
```

| Status | Bedeutung |
|--------|-----------|
| STABIL | DNA konvergiert, genug Material |
| FAST STABIL | Noch leichte Shifts, 1-2 Reden zur Absicherung |
| INSTABIL | Deutliche Verschiebungen, mehr Reden nötig |
| UNZUREICHEND | Weniger als 3 Reden, Minimum nicht erreicht |

---

## Feedback-Lernschleife

Der Skill lernt aus jeder Korrektur — akkumuliert als Learnings im Arbeitsverzeichnis:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Generierte  │────▶│   Feedback   │────▶│   Learnings  │
│    Rede      │     │  (Text oder  │     │   extrahiert │
│              │     │   Korrektur) │     │              │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                          ┌───────────────────────┼───────────────────┐
                          ▼                       ▼                   ▼
                   ┌──────────────┐     ┌──────────────┐   ┌──────────────┐
                   │  DNA-Update  │     │  LEARNINGS-  │   │  Nächste Rede│
                   │ (Zielwerte   │     │  {Name}.md   │   │  wird besser │
                   │  anpassen)   │     │ (akkumuliert)│   │              │
                   └──────────────┘     └──────────────┘   └──────────────┘
```

**Zwei Feedback-Formen:**
- **Text:** "Die Rede ist zu formell, mehr Umgangssprache"
- **Überarbeitete Rede:** Du korrigierst die Rede selbst, der Skill analysiert was du geändert hast

Das Python-Script `compare_feedback.py` berechnet exakt welche Metriken du verschoben hast. Learnings werden pro DNA als `LEARNINGS-{Name}.md` gespeichert und bei jeder künftigen Generierung automatisch mitgelesen — sie haben Vorrang vor generischen DNA-Zielwerten.

---

## Technologie

| Komponente | Technologie | Lizenz | Zweck |
|------------|-------------|--------|-------|
| Orchestrator | Claude Code Skill | — | Workflow-Steuerung, qualitative Analyse, Generierung |
| NLP-Pipeline | spaCy 3.7+ | MIT | Tokenisierung, POS-Tagging, Morphologie |
| Sprachmodell | de_core_news_lg | MIT | Deutsche Grammatik-Erkennung |
| Lesbarkeit | textstat | MIT | Flesch-Index, Lesbarkeits-Scores |
| Laufzeit | Python 3.9+ | PSF | Script-Ausführung |

Alle Abhängigkeiten sind MIT-lizenziert — kommerziell uneingeschränkt nutzbar.

---

## Inspiration

Der Ansatz ist inspiriert von [TinyStyler](https://github.com/zacharyhorvitz/TinyStyler) (EMNLP 2024), einem Few-Shot Style Transfer System das Schreibstile in messbare Embeddings überführt. RedenSkill adaptiert dieses Prinzip — Style als quantifizierbaren Fingerabdruck behandeln — für deutschsprachige Reden und nutzt Claude statt eines Fine-Tuned T5-Modells für die Generierung.

---

## Häufige Fragen

### Wie viele Beispielreden brauche ich?

Minimum 3, empfohlen 5-10. Mehr Reden = stabilere Metriken. Bei nur 3 Reden können Ausreißer die Durchschnittswerte verzerren.

### Kann ich mehrere Stile haben?

Ja. Lege verschiedene Sets von Beispielreden an und erstelle je eine DNA. In Modus 2 wählst du welche DNA verwendet wird.

### Was gehört in die Quellen?

Alles woraus sich die Rede inhaltlich speisen darf: Studien, Zahlen, Zitate, Hintergrundinfos, Pressemitteilungen. Die Quellen beeinflussen nicht den Stil, nur den Inhalt.

### Funktioniert es auch für englische Reden?

Prinzipiell ja, aber `de_core_news_lg` ist für Deutsch optimiert. Für Englisch müsste in `extract_metrics.py` das Modell auf `en_core_web_lg` gewechselt und die Füllwort-/Modalverb-Listen angepasst werden.

### Brauche ich eine GPU?

Nein. spaCy's CPU-Performance reicht völlig — die Analyse von 10 Reden dauert typisch 10-30 Sekunden.

---

## Lizenz

Apache License 2.0 — frei nutzbar, auch kommerziell. Siehe [LICENSE](LICENSE).
