# RedenSkill

Sprach-DNA-Extraktion und Reden-Generator mit Feedback-Lernschleife.

## Skill

Starte den Skill mit `/project:reden`. Er bietet fünf Modi:

1. **Sprach-DNA erstellen**: Analysiert Beispielreden + Quellen → Stilprofil
2. **Rede generieren**: Nutzt DNA + Learnings + Briefing → neue Rede im Zielstil
3. **Feedback & Lernen**: Analysiert Korrekturen → aktualisiert DNA + Learnings
4. **Stil-Check**: Prüft ob eine Rede zum DNA-Profil passt (QS/Authentizität)
5. **Skill exportieren**: Aktuelle Skill-Version als Paket exportieren

## Projektstruktur

```
archive/beispielreden/           # Beispielreden (.txt/.md) hierher legen
archive/quellen/                 # Referenzquellen (.txt/.md) hierher legen
scripts/                         # Python-Analyse-Pipeline
output/sprach-dna/               # Stilprofile + Metriken + Learnings
output/reden/                    # Generierte Reden
.claude/commands/reden.md        # Skill-Definition
```

## Python-Dependencies

```bash
pip install -r scripts/requirements.txt
python -m spacy download de_core_news_lg
```

## Scripts

| Script | Zweck |
|--------|-------|
| `analyze_style.py` | Haupt-Orchestrator: quantitative Metriken + Rhetorik |
| `diagnose_convergence.py` | Konvergenz-Check: genug Reden für stabile DNA? |
| `extract_metrics.py` | Satzlänge, TTR, POS, Lesbarkeit, Interpunktion |
| `detect_rhetoric.py` | Anaphern, Trikola, rhetorische Fragen, Antithesen |
| `validate_speech.py` | Generierte Rede gegen DNA-Metriken validieren |
| `compare_feedback.py` | Original vs. überarbeitete Rede → Learnings |
| `check_vocabulary.py` | Wörter in einer Rede, die der Redner (fast) nie verwendet |
| `check_function_words.py` | Funktionswörter: Rate in der Rede vs. Rate im Korpus |

## Konventionen

- Alle Ausgaben auf Deutsch
- Dateibenennung: `SPRACH-DNA-{Name}.md`, `REDE-{Thema}-{Datum}.md`
- Metriken als JSON: `style-metrics.json`, `validation-*.json`, `vokabular-*.json`, `funktionswörter-*.json`, `feedback-*.json`
- Learnings pro DNA: `LEARNINGS-{Name}.md`
