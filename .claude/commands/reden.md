---
name: reden
description: |
  Sprach-DNA-Extraktion, Reden-Generator und Feedback-Lernschleife.
  Drei Modi: (1) Stilprofil aus Beispielreden erstellen, (2) neue Rede im
  Zielstil generieren, (3) aus Feedback lernen und Skill selbst verbessern.
  Verwende diesen Skill wenn der User "Rede schreiben", "Sprach-DNA",
  "Stilanalyse", "Tonalität analysieren", "Rede generieren", "Redetext",
  "Ghostwriting", "Speech", "Stil übernehmen", "Feedback zur Rede",
  "Rede verbessern", "schreib wie...", "im Stil von...", "Ansprache",
  "Grußwort", "Keynote", oder ähnliches erwähnt. Auch bei Fragen zu
  rhetorischen Mitteln, Satzrhythmus, oder Redner-Stil.
---

# RedenSkill – Orchestrator (v1.0)

Du orchestrierst drei Modi und koordinierst Python-Analyse-Scripts mit
Claudes qualitativer Analysefähigkeit. Antworte auf Deutsch.

## Referenz-Dateien

Lies diese bei Bedarf — sie enthalten Details die hier nur referenziert werden:

| Datei | Wann lesen |
|-------|------------|
| `references/sprach-dna-template.md` | In Phase 1c beim Erstellen der DNA |
| `references/generierung-regeln.md` | In Phase 2c beim Generieren der Rede |
| `references/beispiele.md` | Wenn du unsicher bist wie Output aussehen soll |

## Projektpfade

```
SCRIPTS         = scripts/
ARCHIVE_REDEN   = archive/beispielreden/
ARCHIVE_QUELLEN = archive/quellen/
OUTPUT_DNA      = output/sprach-dna/
OUTPUT_REDEN    = output/reden/
```

## Einstieg

Zeige mit `AskUserQuestion`:

**Frage:** "Welchen Modus möchtest du starten?"

1. **Sprach-DNA erstellen** – Analysiert Beispielreden + Quellen → Stilprofil
2. **Rede generieren** – Nutzt DNA + Briefing → neue Rede im Zielstil
3. **Feedback & Lernen** – Aus Korrekturen lernen → DNA + Skill verbessern
4. **Skill exportieren** – Aktuelle Skill-Version als Paket exportieren

---

## MODUS 1: Sprach-DNA erstellen

### Voraussetzungen

1. Prüfe `archive/beispielreden/` auf .txt/.md Dateien
2. Prüfe `archive/quellen/` auf Referenzmaterial
3. Falls leer: User auffordern, min. 3 Beispielreden + optionale Quellen abzulegen

### Phase 1a: Konvergenz-Diagnose (Python)

Prüfe zuerst ob genug Reden vorliegen und ob die DNA stabil wird:

```bash
python scripts/diagnose_convergence.py archive/beispielreden/ output/sprach-dna/convergence.json
```

Lies die Ausgabe und zeige sie dem User. Das Script analysiert inkrementell:
- Wie stark verschieben sich die Metriken mit jeder neuen Rede?
- Welche Rede hat den Stil ERWEITERT, VERFEINERT oder nur BESTÄTIGT?
- Ist die DNA STABIL, FAST STABIL oder INSTABIL?

Reagiere auf das Ergebnis:
- **STABIL**: Genug Material, weiter mit Phase 1b
- **FAST STABIL**: Hinweis geben, aber weiter (User kann später ergänzen)
- **INSTABIL**: Empfehle mehr Reden, frage ob User trotzdem fortfahren will
- **UNZUREICHEND** (<3 Reden): Fordere mehr Material an

### Phase 1b: Quantitative Analyse (Python)

```bash
python scripts/analyze_style.py archive/beispielreden/ output/sprach-dna/ archive/quellen/
```

Lies die `output/sprach-dna/style-metrics.json` danach vollständig.

### Phase 1c: Qualitative Analyse (Claude)

Lies ALLE Beispielreden vollständig. Lies die Quellen. Lies die Metriken.

Analysiere diese Dimensionen — mit Zitaten aus den Reden als Beleg:

1. **Tonalität & Register** — Formalität (1-10), emotionale Grundtemperatur,
   Autoritätsstil, Humor-Typ + Frequenz, Empathie-Signale
2. **Argumentationsarchitektur** — Muster (deduktiv/induktiv/narrativ/dialektisch),
   Evidenz-Präferenz, Gegenargument-Behandlung, Logos/Pathos/Ethos-Gewichtung
3. **Aufbau-Blueprint** — Eröffnungstechnik, Übergänge, Spannungsbogen,
   Schluss-Technik, Proportionen (Einleitung:Hauptteil:Schluss)
4. **Zielgruppen-Ansprache** — Anrede-Muster, Inklusion, Vorwissen-Annahme, Appelle
5. **Bildsprache & Metaphorik** — Dichte, Bildfelder, Vergleiche, Abstrakt/Konkret
6. **Rhythmus & Mündlichkeit** — Sprechbarkeit, Pausen, Emphase-Wiederholungen
7. **Quellen-Integrationsstil** — Zitat-Einbau, Quellennennung, Daten-Präsentation
8. **Anti-Patterns** — Was wird bewusst NICHT getan?

### Phase 1d: SPRACH-DNA schreiben

Frage den User nach einem Namen für die DNA (z.B. Firmenname, Rednername).

Lies `references/sprach-dna-template.md` und fülle das Template mit den
Ergebnissen aus Phase 1a + 1b. Speichere als `output/sprach-dna/SPRACH-DNA-{Name}.md`.

Jede Behauptung in der DNA muss durch ein Zitat oder eine Metrik belegt sein.
Eine DNA ohne Belege ist wertlos — sie wäre nicht unterscheidbar von einer
generischen Stilvorgabe.

### Phase 1e: Bestätigung

Zeige eine Zusammenfassung und frage:

**AskUserQuestion:** "Ist die Sprach-DNA vollständig?"
- "Ja, fertig" → Abschluss
- "Anpassungen nötig" → User beschreibt, du überarbeitest

---

## MODUS 2: Rede generieren

### Voraussetzungen

1. Prüfe ob `output/sprach-dna/SPRACH-DNA-*.md` existiert
2. Mehrere vorhanden → User wählt
3. Keine vorhanden → Schlage Modus 1 vor

### Sprechdauer → Wortanzahl

Standard-Sprechgeschwindigkeit ist **130 Wörter pro Minute** (ruhiger Vortragsstil).
Der User kann eine eigene WPM-Angabe machen. Umrechnung:

| Dauer | Wörter (bei 130 WPM) |
|-------|---------------------|
| 3 Min | ~390 |
| 5 Min | ~650 |
| 10 Min | ~1300 |
| 15 Min | ~1950 |
| 20 Min | ~2600 |
| 30 Min | ~3900 |

Wenn der User "10 Minuten" sagt, rechne mit 130 WPM (oder seiner eigenen Angabe)
und zeige die resultierende Wortanzahl zur Bestätigung.

### Phase 2a: Briefing aufnehmen

Frage EINE Sache pro Turn (AskUserQuestion):

1. Thema/Anlass
2. Zielgruppe
3. Kernbotschaft (1-3 Sätze)
4. Länge — akzeptiere Minuten ODER Wortanzahl. Bei Minuten: frage ob 130 WPM
   passt oder ob der User schneller/langsamer spricht. Zeige die Umrechnung.
5. Pflicht-Elemente (Zitate, Danksagungen, ...)
6. Quellen aus `archive/quellen/` einbauen? Wenn ja: welche?

### Phase 2b: Gliederung

Lies die DNA (besonders Abschnitt 6 "Aufbau-Blueprint") und die Quellen.
Erstelle eine Gliederung die dem DNA-Blueprint folgt. Markiere wo
rhetorische Figuren und Quellen platziert werden.

**AskUserQuestion:** "Passt die Gliederung?"
- "Ja, weiter" → Phase 2c
- "Anpassungen" → überarbeiten

### Phase 2c: Rohtext generieren

Lies `references/generierung-regeln.md` für die Qualitäts-Regeln.

Generiere abschnittsweise. Für jeden Abschnitt den relevanten DNA-Abschnitt
konsultieren. Beachte:
- Quantitative Zielwerte aus DNA Abschnitt 14
- Rhetorische Figuren in DNA-Frequenz
- Pronomen-Profil und Signalwörter aus DNA
- Quellen im DNA-eigenen Integrationsstil
- Anti-Patterns aus DNA Abschnitt 12 vermeiden

Speichere als `output/reden/REDE-{Thema}-{Datum}.md` mit Meta-Block.

### Phase 2d: Validierung (Python)

```bash
python scripts/validate_speech.py output/reden/REDE-{...}.md output/sprach-dna/style-metrics.json
```

### Phase 2e: Iterative Verfeinerung

Score < 85 → Abweichungen zeigen, gezielt überarbeiten, erneut validieren.
Max 3 Iterationen. Score ≥ 85 → User die Rede präsentieren.

### Phase 2f: Abschluss

**AskUserQuestion:** "Wie weiter?"
- "Fertig" → Speichern
- "Überarbeiten" → User gibt Richtung
- "Feedback-Modus" → Wechsel zu Modus 3

---

## MODUS 3: Feedback & Selbstverbesserung

Zwei Eingänge — der User kann Feedback als Text geben ODER eine überarbeitete
Version der Rede liefern. Beides zusammen ist auch möglich.

### Phase 3a: Feedback aufnehmen

**AskUserQuestion:** "Wie möchtest du Feedback geben?"
- "Text-Feedback" → User schreibt was nicht passt
- "Überarbeitete Rede" → User gibt Pfad zur korrigierten Version
- "Beides" → Text + korrigierte Datei

### Phase 3b: Delta-Analyse

Falls überarbeitete Rede vorhanden:

```bash
python scripts/compare_feedback.py output/reden/REDE-{Original}.md {Pfad-zur-Überarbeitung} "{Text-Feedback}"
```

Falls nur Text-Feedback: Qualitativ analysieren ohne Python.

### Phase 3c: Learnings strukturieren

Lies den Feedback-Report. Identifiziere:
1. Quantitative Deltas (welche Metriken wurden verschoben?)
2. Qualitative Änderungen (was wurde inhaltlich/stilistisch korrigiert?)
3. Muster über mehrere Feedbacks hinweg (gibt es wiederkehrende Korrekturen?)

Zeige dem User eine strukturierte Zusammenfassung:
- Erkannte Korrekturen mit vermuteter Absicht
- DNA-Update-Empfehlungen (welcher Abschnitt, wie anpassen)
- Skill-Verbesserungen (welche Instruktion hat zum Problem geführt)

### Phase 3d: DNA aktualisieren

**AskUserQuestion:** "DNA anhand des Feedbacks aktualisieren?"
- "Ja" → Zielwerte anpassen, qualitative Beschreibungen korrigieren,
  Feedback-Eintrag in Abschnitt 15 ergänzen
- "Nein" → Learnings nur dokumentieren

### Phase 3e: Skill-Selbstverbesserung

**AskUserQuestion:** "Soll der Skill selbst verbessert werden?"
- "Ja, Vorschlag zeigen" → Konkrete Änderungen vorschlagen (s.u.)
- "Nein" → Fertig

Bei "Ja":
1. Lies `.claude/commands/reden.md`
2. Identifiziere welche Instruktion zum Problem geführt hat
3. Zeige konkreten Änderungsvorschlag mit Begründung:
   ```
   SKILL-VERBESSERUNG v{N+1}
   Änderung 1: [Bereich] — Problem → Lösung → Betroffene Phase
   ```
4. **AskUserQuestion:** "Änderungen übernehmen?"
   - "Ja" → Backup als `reden-v{N}.md.bak`, Änderungen durchführen, Version erhöhen
   - "Teilweise" → User wählt welche
   - "Nein" → Verwerfen

---

## MODUS 4: Skill exportieren

Exportiert die aktuelle Skill-Version als lesbares Paket nach `output/skill-export/`.

### Ablauf

1. Erstelle `output/skill-export/` (überschreibe falls vorhanden)
2. Kopiere folgende Dateien dorthin:
   ```bash
   mkdir -p output/skill-export/references
   cp .claude/commands/reden.md output/skill-export/SKILL-reden.md
   cp references/sprach-dna-template.md output/skill-export/references/
   cp references/generierung-regeln.md output/skill-export/references/
   cp references/beispiele.md output/skill-export/references/
   ```
3. Falls Backups existieren (`.claude/commands/reden-v*.md.bak`), kopiere diese auch:
   ```bash
   cp .claude/commands/reden-v*.md.bak output/skill-export/ 2>/dev/null
   ```
4. Erstelle eine `output/skill-export/VERSION.md` mit:
   ```markdown
   # RedenSkill Export
   - Exportiert: {Datum + Uhrzeit}
   - Version: {aktuelle Version aus dem Skill-Header}
   - Dateien:
     - SKILL-reden.md (Skill-Definition + Orchestrator)
     - references/sprach-dna-template.md
     - references/generierung-regeln.md
     - references/beispiele.md
     {- reden-v{N}.md.bak (falls vorhanden)}
   ```
5. Zeige dem User den Pfad und eine Zusammenfassung:
   ```
   Skill exportiert nach: output/skill-export/
   Version: v{X}
   Dateien: {N} Dateien ({X} KB)
   ```

---

## Versionierung

Bei jeder Selbstverbesserung (Phase 3e):
- Backup: `.claude/commands/reden-v{N}.md.bak`
- Version im Header erhöhen
- Änderung in DNA Feedback-Historie dokumentieren

---

## Fehlerbehandlung

- **Python-Fehler**: Prüfe ob spaCy installiert ist, schlage `bash scripts/setup.sh` vor
- **Keine Beispielreden**: Fordere min. 3 Reden an, erkläre wo sie abzulegen sind
- **Keine DNA**: Schlage Modus 1 vor
- **DNA veraltet** (viele Feedback-Einträge): Schlage Neuanalyse vor
