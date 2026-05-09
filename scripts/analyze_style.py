#!/usr/bin/env python3
"""Main style analysis orchestrator. Combines quantitative metrics and rhetorical analysis."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _shared import load_texts
from extract_metrics import extract_single_text, aggregate_metrics
from detect_rhetoric import analyze_rhetoric


def main():
    if len(sys.argv) < 3:
        print("Usage: python analyze_style.py <speeches_dir> <output_dir> [sources_dir]")
        print("  speeches_dir: Directory with example speeches (.txt/.md)")
        print("  output_dir:   Directory for output files")
        print("  sources_dir:  Optional directory with reference sources")
        sys.exit(1)

    speeches_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    sources_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else None

    output_dir.mkdir(parents=True, exist_ok=True)

    texts = load_texts(speeches_dir)
    if not texts:
        print(f"Fehler: Keine .txt oder .md Dateien in {speeches_dir}")
        sys.exit(1)

    total_words = sum(len(t["text"].split()) for t in texts)

    print(f"{'=' * 60}")
    print("SPRACH-DNA ANALYSE")
    print(f"{'=' * 60}")
    print(f"Gefunden: {len(texts)} Beispielreden")
    print(f"Gesamt:   {total_words} Wörter")
    print()

    print("Phase 1/3: Quantitative Metriken extrahieren...")
    per_text_metrics = []
    for t in texts:
        print(f"  → {Path(t['path']).name} ({len(t['text'].split())} Wörter)")
        metrics = extract_single_text(t["text"])
        metrics["_datei"] = Path(t["path"]).name
        per_text_metrics.append(metrics)

    aggregated = aggregate_metrics(per_text_metrics)

    print("\nPhase 2/3: Rhetorische Figuren erkennen...")
    per_text_rhetoric = []
    for t in texts:
        print(f"  → {Path(t['path']).name}")
        rhetoric = analyze_rhetoric(t["text"])
        rhetoric["_datei"] = Path(t["path"]).name
        per_text_rhetoric.append(rhetoric)

    rhetoric_agg: dict = {
        "anaphern_gesamt": sum(r["statistik"]["anaphern_anzahl"] for r in per_text_rhetoric),
        "rhetorische_fragen_gesamt": sum(r["statistik"]["rhetorische_fragen_anzahl"] for r in per_text_rhetoric),
        "antithesen_gesamt": sum(r["statistik"]["antithesen_anzahl"] for r in per_text_rhetoric),
        "trikola_gesamt": sum(r["statistik"]["trikola_anzahl"] for r in per_text_rhetoric),
    }
    if total_words > 0:
        f = 1000 / total_words
        rhetoric_agg["pro_1000_wörter"] = {
            k.replace("_gesamt", ""): round(v * f, 2)
            for k, v in rhetoric_agg.items()
            if k.endswith("_gesamt")
        }

    all_examples: dict[str, list] = {
        "anaphern": [], "rhetorische_fragen": [], "antithesen": [],
        "trikola": [], "wiederholungen": [],
    }
    for r in per_text_rhetoric:
        for key in all_examples:
            all_examples[key].extend(r.get(key, []))

    sources_info = None
    if sources_dir and sources_dir.is_dir():
        print("\nPhase 3/3: Quellenmaterial inventarisieren...")
        source_texts = load_texts(sources_dir)
        sources_info = {
            "anzahl": len(source_texts),
            "dateien": [Path(t["path"]).name for t in source_texts],
            "gesamt_wörter": sum(len(t["text"].split()) for t in source_texts),
        }
        print(f"  → {len(source_texts)} Quellen ({sources_info['gesamt_wörter']} Wörter)")
    else:
        print("\nPhase 3/3: Kein Quellenverzeichnis angegeben, überspringe.")

    result = {
        "meta": {
            "anzahl_reden": len(texts),
            "dateien": [Path(t["path"]).name for t in texts],
            "gesamt_wörter": total_words,
            "quellen": sources_info,
        },
        "metriken": {
            "aggregiert": aggregated,
            "pro_text": per_text_metrics,
        },
        "rhetorik": {
            "aggregiert": rhetoric_agg,
            "beispiele": {k: v[:10] for k, v in all_examples.items()},
            "pro_text": per_text_rhetoric,
        },
    }

    output_path = output_dir / "style-metrics.json"
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\n{'=' * 60}")
    print("ERGEBNIS")
    print(f"{'=' * 60}")
    print(f"Style-Metriken gespeichert: {output_path}")

    s = aggregated.get("sätze", {})
    w = aggregated.get("wörter", {})
    l = aggregated.get("lesbarkeit", {})
    g = aggregated.get("grammatik", {})

    def _mv(d):
        return d.get("mittelwert", "N/A") if isinstance(d, dict) else d

    print(f"\nZusammenfassung:")
    print(f"  Satzlänge (Ø):      {_mv(s.get('wörter_pro_satz', {}))} Wörter")
    print(f"  Vokabular (TTR):    {_mv(w.get('type_token_ratio', {}))}")
    print(f"  Flesch-Index:       {_mv(l.get('flesch_reading_ease', {}))}")
    print(f"  Aktiv/Passiv:       {_mv(g.get('aktiv_prozent', {}))}% / {_mv(g.get('passiv_prozent', {}))}%")
    print(f"  Rhet. Fragen:       {rhetoric_agg.get('rhetorische_fragen_gesamt', 0)}")
    print(f"  Anaphern:           {rhetoric_agg.get('anaphern_gesamt', 0)}")
    print()
    print("Nächster Schritt: Claude liest die Metriken und erstellt die qualitative SPRACH-DNA.")


if __name__ == "__main__":
    main()
