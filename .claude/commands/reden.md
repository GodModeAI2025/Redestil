---
name: reden
description: |
  Sprach-DNA-Extraktion, Reden-Generator und Feedback-Lernschleife.
  Fünf Modi: (1) Stilprofil aus Beispielreden erstellen, (2) neue Rede im
  Zielstil generieren, (3) aus Feedback lernen (DNA + Learnings aktualisieren),
  (4) Stil-Check einer Rede gegen die DNA, (5) Skill exportieren.
  Verwende diesen Skill wenn der User "Rede schreiben", "Sprach-DNA",
  "Stilanalyse", "Tonalität analysieren", "Rede generieren", "Redetext",
  "Ghostwriting", "Speech", "Stil übernehmen", "Feedback zur Rede",
  "Rede verbessern", "schreib wie...", "im Stil von...", "Ansprache",
  "Grußwort", "Keynote", oder ähnliches erwähnt. Auch bei Fragen zu
  rhetorischen Mitteln, Satzrhythmus, oder Redner-Stil.
---

# RedenSkill – Orchestrator (v1.0)

Du orchestrierst fünf Modi und koordinierst Python-Analyse-Scripts mit
Claudes qualitativer Analysefähigkeit. Antworte auf Deutsch.

## Referenz-Dateien

Lies diese bei Bedarf — sie enthalten Details die hier nur referenziert werden:

| Datei | Wann lesen |
|-------|------------|
| `references/sprach-dna-template.md` | In Phase 1c beim Erstellen der DNA |
| `references/generierung-regeln.md` | In Phase 2c beim Generieren der Rede |
| `references/beispiele.md` | Wenn du unsicher bist wie Output aussehen soll (lokal, nicht versioniert — fehlt die Datei, ohne sie weiterarbeiten) |

## Projektpfade

```
SCRIPTS         = scripts/
ARCHIVE_REDEN   = archive/beispielreden/
ARCHIVE_QUELLEN = archive/quellen/
OUTPUT_DNA      = output/sprach-dna/
OUTPUT_REDEN    = output/reden/
LEARNINGS       = output/sprach-dna/LEARNINGS-{Name}.md
```

## Einstieg

Zeige mit `AskUserQuestion`:

**Frage:** "Welchen Modus möchtest du starten?"

1. **Sprach-DNA erstellen** – Analysiert Beispielreden + Quellen → Stilprofil
2. **Rede generieren** – Nutzt DNA + Learnings + Briefing → neue Rede im Zielstil
3. **Feedback & Lernen** – Aus Korrekturen lernen → DNA + Learnings aktualisieren
4. **Stil-Check** – Rede gegen DNA prüfen: stammt sie vom Redner?
5. **Skill exportieren** – Aktuelle Skill-Version als Paket exportieren

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

Prüfe ob `output/sprach-dna/LEARNINGS-{Name}.md` existiert. Falls ja: lies
die Datei vollständig. Jedes Learning enthält eine konkrete Regel die bei
der Generierung beachtet werden muss — sie haben Vorrang vor generischen
DNA-Zielwerten, weil sie aus echtem Feedback des Users stammen.

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
python scripts/check_vocabulary.py output/reden/REDE-{...}.md archive/beispielreden/ --quellen archive/quellen/
python scripts/check_function_words.py output/reden/REDE-{...}.md archive/beispielreden/
```

Der Wortschatz-Abgleich listet Wörter, deren Lemma in den Beispielreden
höchstens einmal vorkommt. Metriken können alle im Toleranzbereich liegen,
während einzelne Wörter („nahtlos", „maßgeblich") sofort fremd klingen —
genau das fängt dieser Check. Er fließt nicht in den Score ein. Prüfe jeden
Treffer: Fachbegriffe und Themenwörter sind legitim, generische
Füll- und Prunkwörter ersetzt du durch Formulierungen aus der DNA.

Der Funktionswort-Abgleich zeigt die andere Hälfte: nicht welche Wörter
fremd sind, sondern welche kleinen Wörter in falscher Menge vorkommen —
„jedoch" statt „aber", „da" statt „weil", mehr Passiv-Hilfsverben als der
Redner nutzt. Auch dieser Check fließt nicht in den Score ein. Korrigiere
nur dort, wo eine Stelle die Änderung ohnehin trägt. Setze niemals Wörter
ein, damit eine Rate besser aussieht — die Rede wird davon nicht besser,
nur die Tabelle.

### Phase 2e: Iterative Verfeinerung

Score < 85 → Abweichungen zeigen, gezielt überarbeiten, erneut validieren.
Auffällige Wörter aus den beiden Wort-Abgleichen im selben Durchgang
bereinigen. Max 3 Iterationen. Score ≥ 85 → User die Rede präsentieren.
Ein Durchgang darf auch null Änderungen ergeben, wenn die Abweichungen
inhaltlich gerechtfertigt sind — dann benenne sie und mache weiter.

### Phase 2f: Abschluss

**AskUserQuestion:** "Wie weiter?"
- "Fertig" → Speichern
- "Überarbeiten" → User gibt Richtung
- "Feedback-Modus" → Wechsel zu Modus 3

---

## MODUS 3: Feedback & Lernen

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
- Vorgeschlagene Learnings für künftige Generierungen

### Phase 3d: DNA aktualisieren

**AskUserQuestion:** "DNA anhand des Feedbacks aktualisieren?"
- "Ja" → Zielwerte anpassen, qualitative Beschreibungen korrigieren,
  Feedback-Eintrag in Abschnitt 15 ergänzen
- "Nein" → Nur Learnings dokumentieren (Phase 3e)

### Phase 3e: Learnings speichern

Schreibe die Erkenntnisse in `output/sprach-dna/LEARNINGS-{Name}.md`.
Falls die Datei noch nicht existiert, erstelle sie mit diesem Format:

```markdown
# Learnings: {Name}

> Akkumulierte Erkenntnisse aus Feedback-Runden.
> Wird bei jeder Reden-Generierung automatisch mitgelesen.
> Learnings haben Vorrang vor generischen DNA-Zielwerten.

---
```

Hänge dann das neue Learning an:

```markdown
### L-{NNN}: {Kurztitel} — {Datum}
- **Rede:** REDE-{Thema}-{Datum}.md
- **Problem:** {Was war nicht stimmig?}
- **Korrektur:** {Was wurde geändert?}
- **Regel für künftige Reden:** {Konkrete, umsetzbare Anweisung}
- **Betroffene DNA-Abschnitte:** {Nummern}
```

Die `{NNN}` Nummer ist fortlaufend (001, 002, ...). Zeige dem User das
fertige Learning zur Bestätigung bevor es gespeichert wird.

Prüfe ob es bereits Learnings gibt die widersprüchlich sind — falls ja,
weise den User darauf hin und schlage vor, das ältere Learning zu
aktualisieren oder zu entfernen.

---

## MODUS 4: Stil-Check (Authentizitätsprüfung)

Prüft ob eine Rede zum DNA-Profil passt — also ob sie stilistisch vom Redner
stammen könnte. Nützlich um zu entscheiden ob eine Rede als Trainingsmaterial
(Beispielrede) geeignet ist oder ob sie noch angepasst werden muss.

### Phase 4a: Input

**AskUserQuestion:** "Welche Rede soll geprüft werden?"
- "Datei angeben" → User gibt Pfad zur Rede
- "Aus output/reden/ wählen" → Zeige vorhandene Reden zur Auswahl

Prüfe ob eine DNA existiert. Mehrere vorhanden → User wählt welche.

### Phase 4b: Quantitative Prüfung (Python)

```bash
python scripts/validate_speech.py {Pfad-zur-Rede} output/sprach-dna/style-metrics.json
python scripts/check_vocabulary.py {Pfad-zur-Rede} archive/beispielreden/ --quellen archive/quellen/
python scripts/check_function_words.py {Pfad-zur-Rede} archive/beispielreden/
```

Lies die Ergebnisse. Der Validierungs-Score gibt die quantitative
Übereinstimmung mit dem Stil. Der Wortschatz-Abgleich zeigt Wörter, die der
Redner in seinen Beispielreden (fast) nie verwendet, der Funktionswort-Abgleich
Konjunktionen, Präpositionen und Partikeln in ungewohnter Menge — nutze beides
als Belege für die Abweichungen in Phase 4d.

### Phase 4c: Qualitative Prüfung (Claude)

Lies die Rede und die DNA vollständig. Prüfe:
1. **Tonalität** — Stimmt der Formalitätsgrad? Die emotionale Temperatur?
2. **Satz-Architektur** — Passt der Rhythmus? Stakkato-Muster?
3. **Rhetorische Figuren** — Werden die DNA-typischen Mittel verwendet?
4. **Wort-DNA** — Signalwörter, Füllwort-Profil, Pronomen-Verhältnis?
5. **Anti-Patterns** — Tauchen Dinge auf die der Stil vermeidet?
6. **Bildsprache** — Passen Bildfelder und Metaphern-Dichte?

### Phase 4d: Ergebnis

Zeige ein Verdikt mit Begründung:

| Verdikt | Score | Bedeutung |
|---------|-------|-----------|
| **Authentisch** | ≥85 | Passt zum Redner, kann als Trainingsmaterial dienen |
| **Teilweise passend** | 60-84 | Grundstil erkennbar, aber Abweichungen vorhanden |
| **Stilfremd** | <60 | Passt nicht zum Profil |

Für jede Abweichung:
- Was genau weicht ab (mit Zitat)
- Wie würde der Redner es laut DNA formulieren
- Betroffener DNA-Abschnitt

**AskUserQuestion:** "Wie weiter?"
- "Als Trainingsmaterial übernehmen" → Kopiere die Rede nach `archive/beispielreden/`
  und empfehle DNA-Neuanalyse (Modus 1).
  **Vorher prüfen:** Stammt die Rede aus Modus 2 und wurde vom Redner nicht
  selbst überarbeitet oder freigegeben? Dann weise darauf hin, dass sie die
  Vergleichsbasis verfälscht: Generiertes Vokabular landet im Korpus, und
  der Wortschatz-Abgleich erkennt genau diese Wörter danach nicht mehr.
  Nur übernehmen, wenn der User das bestätigt.
- "Rede anpassen" → Wechsel zu Modus 2 mit den Abweichungen als Vorgabe
- "Fertig" → Ergebnis nur dokumentieren

---

## MODUS 5: Skill exportieren

Exportiert die aktuelle Skill-Version als lesbares Paket nach `output/skill-export/`.

### Ablauf

1. Erstelle `output/skill-export/` (überschreibe falls vorhanden)
2. Kopiere folgende Dateien dorthin:
   ```bash
   mkdir -p output/skill-export/references
   cp .claude/commands/reden.md output/skill-export/SKILL-reden.md
   cp references/sprach-dna-template.md output/skill-export/references/
   cp references/generierung-regeln.md output/skill-export/references/
   cp references/beispiele.md output/skill-export/references/ 2>/dev/null
   ```
3. Erstelle eine `output/skill-export/VERSION.md` mit:
   ```markdown
   # RedenSkill Export
   - Exportiert: {Datum + Uhrzeit}
   - Dateien:
     - SKILL-reden.md (Skill-Definition + Orchestrator)
     - references/sprach-dna-template.md
     - references/generierung-regeln.md
     - references/beispiele.md (falls vorhanden)
   ```
4. Zeige dem User den Pfad und eine Zusammenfassung

---

## Fehlerbehandlung

- **Python-Fehler**: Prüfe ob spaCy installiert ist, schlage `bash scripts/setup.sh` vor
- **Keine Beispielreden**: Fordere min. 3 Reden an, erkläre wo sie abzulegen sind
- **Keine DNA**: Schlage Modus 1 vor
- **DNA veraltet** (viele Feedback-Einträge): Schlage Neuanalyse vor
- **Keine Learnings**: Kein Problem — Learnings entstehen erst durch Feedback (Modus 3)
