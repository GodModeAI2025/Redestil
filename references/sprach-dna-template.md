# SPRACH-DNA Template

Verwende dieses Template wenn du in Modus 1, Phase 1c die DNA-Datei erstellst.
Ersetze alle `{Platzhalter}` mit den Analyseergebnissen.

---

```markdown
# Sprach-DNA: {Name}

## Meta
- Erstellt: {Datum}
- Version: 1.0
- Basierend auf: {N} Beispielreden, {M} Referenzquellen
- Analysiertes Textvolumen: {X} Wörter
- Metriken-Referenz: style-metrics.json

## 1. Identitäts-Profil

> {Ein-Absatz-Zusammenfassung: Wer spricht so? Welchen Eindruck hinterlässt
> diese Stimme? Was macht sie unverwechselbar?}

## 2. Tonalität & Register

### Formalitätsgrad: {1-10} / 10
{Beschreibung: Was bedeutet dieser Grad konkret? Vergleichsanker.}

### Emotionale Grundtemperatur
{sachlich / warm / leidenschaftlich / provokant — mit Begründung und Zitat}

### Autoritätsstil
{belehrend / einladend / kollegial / inspirierend — mit Beispiel}

### Humor-Einsatz
- Typ: {Ironie / Selbstironie / Anekdote / Wortspiel / keiner}
- Frequenz: {selten / gelegentlich / häufig}
- Beispiel: "{Zitat aus Beispielrede}"

### Empathie-Signale
{Wie wird Verständnis gezeigt? Welche Formulierungen werden verwendet?}
- Beispiel: "{Zitat}"

## 3. Satz-Architektur

### Quantitativ (aus style-metrics.json)
| Metrik | Wert | Toleranz |
|--------|------|----------|
| Satzlänge (Ø) | {X} Wörter | ±{Y} |
| Satzlänge (Median) | {X} Wörter | — |
| Satzlänge (Bereich) | {min}–{max} | — |
| Stakkato-Quote (≤3 Wörter) | {X}% | ±{Y}% |

### Satztypen-Mix
| Typ | Anteil |
|-----|--------|
| Aussagesätze | {X}% |
| Fragen | {X}% |
| Ausrufe | {X}% |
| Ellipsen | {X}% |

### Satzanfänge
| Wortart | Anteil |
|---------|--------|
| Pronomen | {X}% |
| Substantiv | {X}% |
| Adverb | {X}% |
| Konjunktion | {X}% |
| Verb | {X}% |
| Artikel | {X}% |

### Qualitativ — Rhythmus-Muster
{Beschreibung des typischen Satzrhythmus: Wechsel lang/kurz, Stakkato-Passagen,
wo werden bewusst lange Sätze eingesetzt, wo kurze?}

Beispiel für typischen Rhythmus:
> "{3-4 aufeinanderfolgende Sätze die den Rhythmus zeigen}"

## 4. Wort-DNA

### Quantitativ
| Metrik | Wert |
|--------|------|
| Type-Token-Ratio | {X} |
| Hapax-Legomena | {X}% |
| Wortlänge (Ø) | {X} Zeichen |
| Füllwörter/1000 | {X} |
| Modalverben/1000 | {X} |

### Füllwort-Profil
{Top-Füllwörter mit Frequenz — diese gezielt einsetzen}

### Modalverb-Profil
{Verteilung: können/müssen/sollen/wollen/dürfen — zeigt Verbindlichkeitsstil}

### Signalwörter (Top-20)
{Die 20 häufigsten inhaltlichen Wörter — zeigt thematische DNA}

### Qualitativ — Register & Eigenheiten
{Beschreibung: Alltagssprache vs. Fachsprache, Fremdwort-Neigung,
besondere Vokabular-Eigenheiten, wiederkehrende Lieblingsformulierungen}

## 5. Rhetorische Werkzeugkiste

### Quantitativ (pro 1000 Wörter)
| Figur | Frequenz |
|-------|----------|
| Anaphern | {X} |
| Rhetorische Fragen | {X} |
| Antithesen | {X} |
| Trikola | {X} |
| Epiphern | {X} |

### Anaphern — Beispiele
> "{Zitat 1}"
> "{Zitat 2}"

### Rhetorische Fragen — Beispiele
> "{Zitat 1}"
> "{Zitat 2}"

### Antithesen — Beispiele
> "{Zitat 1}"

### Trikola — Beispiele
> "{Zitat 1}"

### Wiederholungen (bewusste Redundanz)
{Top-Phrasen die mehrfach verwendet werden, mit Beispielkontext}

## 6. Aufbau-Blueprint

### Eröffnungstechnik
- Typ: {Zitat / Frage / Provokation / Anekdote / Statistik / direkte Ansprache}
- Anteil an Gesamtlänge: ~{X}%
- Beispiel:
  > "{Typische Eröffnung aus einer Beispielrede}"

### Übergangs-Muster
{Wie werden Abschnitte verbunden? Typische Übergangsformulierungen:}
- "{Übergangsformulierung 1}"
- "{Übergangsformulierung 2}"
- "{Übergangsformulierung 3}"

### Spannungsbogen
- Typ: {linear steigend / Wellenbewegung / Sandwich / Klimax}
- Beschreibung: {Wie baut sich die Spannung auf?}

### Schluss-Technik
- Typ: {Call-to-Action / Zusammenfassung / Rückbezug / offene Frage / Vision}
- Anteil an Gesamtlänge: ~{X}%
- Beispiel:
  > "{Typischer Schluss aus einer Beispielrede}"

### Muster-Gliederung
1. Eröffnung ({X}%): {Technik}
2. Überleitung: {Muster}
3. Hauptteil ({X}%): {Struktur-Beschreibung}
4. Schluss ({X}%): {Technik}

## 7. Argumentations-Muster

### Primäres Muster
{deduktiv / induktiv / narrativ / dialektisch — mit Erklärung}

### Evidenz-Präferenz
| Evidenz-Typ | Häufigkeit |
|-------------|------------|
| Statistiken/Zahlen | {hoch/mittel/niedrig} |
| Anekdoten/Geschichten | {hoch/mittel/niedrig} |
| Expertenzitate | {hoch/mittel/niedrig} |
| Analogien/Vergleiche | {hoch/mittel/niedrig} |

### Überzeugungsstrategie
- Logos (Logik/Fakten): ~{X}%
- Pathos (Emotion): ~{X}%
- Ethos (Glaubwürdigkeit): ~{X}%

### Gegenargument-Behandlung
{ignorieren / kurz entkräften / ausführlich integrieren — mit Beispiel}

## 8. Bildsprache & Metaphorik

### Metaphern-Dichte
{hoch (>5 pro 1000 Wörter) / mittel (2-5) / niedrig (<2)}

### Bevorzugte Bildfelder
1. {Bildfeld 1}: Beispiel "{Zitat}"
2. {Bildfeld 2}: Beispiel "{Zitat}"
3. {Bildfeld 3}: Beispiel "{Zitat}"

### Vergleichs-Häufigkeit
{"wie ein..." Konstruktionen: X pro 1000 Wörter}

### Abstrakt-vs-Konkret
{Verhältnis, Tendenz: eher bildhaft-konkret oder abstrakt-konzeptuell?}

## 9. Zielgruppen-Ansprache

### Direkte Anrede
{Typische Anrede-Muster mit Zitaten}
- "{Anrede 1}"
- "{Anrede 2}"

### Inklusions-Sprache
{Wie wird Gemeinschaft hergestellt? "Wir alle...", "Jeder von uns..."}

### Vorwissen-Annahme
{Werden Fachbegriffe erklärt oder vorausgesetzt?}

### Appell-Frequenz
{Wie oft und wie wird zum Handeln aufgefordert?}

### Pronomen-Profil
| Pronomen | pro 1000 Wörter |
|----------|----------------|
| ich | {X} |
| wir | {X} |
| Sie (formal) | {X} |
| man | {X} |
| **Wir/Ich-Verhältnis** | **{X}** |

## 10. Rhythmus & Mündlichkeit

### Sprechbarkeit
{Bewertung 1-10: Wie gut klingt der Text laut gelesen?}
{Begründung}

### Pause-Markierungen
{Wie werden Sprechpausen markiert? Gedankenstriche, Ellipsen, Zeilenumbrüche?}

### Wiederholungs-Muster für Emphase
{Welche Wörter/Phrasen werden bewusst wiederholt?}
- Beispiel: > "{Zitat mit bewusster Wiederholung}"

### Atem-Einheiten
{Typische Satzlänge in Silben — korreliert mit natürlichen Sprechpausen}

## 11. Quellen-Integrationsstil

### Zitat-Einbau
{direkt zitiert / paraphrasiert / als Autorität / als Gegenposition}
- Beispiel: > "{Wie ein Zitat typischerweise eingebaut wird}"

### Quellennennung
{explizit ("laut Studie X") / implizit ("Experten sagen") / gar nicht}

### Daten-Präsentation
{nackte Zahlen / kontextualisiert / durch Vergleich greifbar gemacht}
- Beispiel: > "{Typische Daten-Einbindung}"

## 12. Anti-Patterns

### Was dieser Stil NICHT tut
{Liste von Dingen die in den Beispielreden nie vorkommen und bewusst vermieden
werden sollten}

- ❌ {Anti-Pattern 1}
- ❌ {Anti-Pattern 2}
- ❌ {Anti-Pattern 3}
- ❌ {Anti-Pattern 4}
- ❌ {Anti-Pattern 5}

### Vermiedene Wörter/Konstruktionen
{Spezifische Wörter oder Phrasen die nie auftauchen}

### Fehlende rhetorische Mittel
{Welche gängigen Mittel werden bewusst NICHT eingesetzt?}

## 13. Goldene Beispiele

{5 Passagen aus den Beispielreden die den Stil perfekt verkörpern.
Jedes mit Begründung warum es den Stil zeigt.}

### Beispiel 1
> "{Zitat — 2-4 Sätze}"
— Quelle: {Dateiname}
— Zeigt: {Warum dieses Zitat den Stil verkörpert}

### Beispiel 2
> "{Zitat}"
— Quelle: {Dateiname}
— Zeigt: {Begründung}

### Beispiel 3
> "{Zitat}"
— Quelle: {Dateiname}
— Zeigt: {Begründung}

### Beispiel 4
> "{Zitat}"
— Quelle: {Dateiname}
— Zeigt: {Begründung}

### Beispiel 5
> "{Zitat}"
— Quelle: {Dateiname}
— Zeigt: {Begründung}

## 14. Quantitative Referenzwerte

Kompakte Übersicht aller Zielwerte für die Validierung.

| Dimension | Zielwert | Toleranz (±%) |
|-----------|----------|---------------|
| Satzlänge (Ø Wörter) | {X} | 25 |
| Stakkato-Quote | {X}% | 40 |
| Type-Token-Ratio | {X} | 25 |
| Füllwörter/1000 | {X} | 40 |
| Modalverben/1000 | {X} | 35 |
| Wortlänge (Ø) | {X} | 25 |
| Wir/Ich-Verhältnis | {X} | 50 |
| Aktiv-Anteil | {X}% | 15 |
| Adjektiv-Dichte | {X}% | 30 |
| Flesch-Index | {X} | 20 |
| Silben/Wort | {X} | 25 |
| Fragezeichen/1000 | {X} | 40 |
| Ausrufezeichen/1000 | {X} | 40 |
| Kommas/1000 | {X} | 40 |
| Gedankenstriche/1000 | {X} | 40 |

## 15. Feedback-Historie

> Wird automatisch durch Modus 3 (Feedback & Lernen) ergänzt.
> Jeder Eintrag dokumentiert was gelernt wurde und wie die DNA angepasst wurde.

| Datum | Rede | Änderung | Betroffene Abschnitte |
|-------|------|----------|----------------------|
| — | — | — | — |
```
