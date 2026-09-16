#!/usr/bin/env python3
"""Diagnose whether enough example speeches exist for a stable style DNA.

Incrementally analyzes speeches and measures how much each new speech
shifts the aggregated metrics. Reports convergence status and recommends
whether more material is needed.
"""

from __future__ import annotations

import json
import sys
import statistics
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _shared import load_texts, get_nested, num, pct_change
from extract_metrics import extract_single_text, aggregate_metrics
from detect_rhetoric import analyze_rhetoric


# Paths refer to the structure returned by aggregate_metrics()
TRACKED_DIMENSIONS = [
    ("Satzlänge (Ø)", ["sätze", "wörter_pro_satz"]),
    ("Stakkato-Quote", ["sätze", "stakkato_quote"]),
    ("Type-Token-Ratio", ["wörter", "type_token_ratio"]),
    ("Füllwörter/1000", ["wörter", "füllwörter_pro_1000"]),
    ("Modalverben/1000", ["wörter", "modalverben_pro_1000"]),
    ("Wortlänge (Ø)", ["wörter", "wortlänge"]),
    ("Aktiv-Anteil (%)", ["grammatik", "aktiv_prozent"]),
    ("Adjektiv-Dichte (%)", ["grammatik", "adjektiv_dichte"]),
    ("Flesch-Index", ["lesbarkeit", "flesch_reading_ease"]),
    ("Silben/Wort", ["lesbarkeit", "silben_pro_wort"]),
]

SIGNIFICANCE_THRESHOLD = 10.0
STABILITY_THRESHOLD = 5.0


def extract_signal_words(metrics: dict, top_n: int = 30) -> set:
    words = metrics.get("wörter", {}).get("top_50_signalwörter", [])
    return {w["wort"] for w in words[:top_n]}


def count_rhetoric_types(rhetoric: dict) -> dict:
    return {
        "anaphern": len(rhetoric.get("anaphern", [])),
        "rhetorische_fragen": len(rhetoric.get("rhetorische_fragen", [])),
        "antithesen": len(rhetoric.get("antithesen", [])),
        "trikola": len(rhetoric.get("trikola", [])),
        "epiphern": len(rhetoric.get("epiphern", [])),
        "wiederholungen": len(rhetoric.get("wiederholungen", [])),
    }


def diagnose(speeches_dir: Path, output_path: Path | None = None):
    texts = load_texts(speeches_dir)
    if not texts:
        print(f"Fehler: Keine .txt oder .md Dateien in {speeches_dir}")
        sys.exit(1)

    n = len(texts)

    print(f"{'=' * 60}")
    print(f"KONVERGENZ-DIAGNOSE")
    print(f"{'=' * 60}")
    print(f"Gefunden: {n} Beispielreden")
    print()

    if n < 2:
        print("ERGEBNIS: Mindestens 2 Reden nötig für eine Diagnose.")
        print("EMPFEHLUNG: Bitte mindestens 3 Reden ablegen.")
        return {"status": "insufficient", "reden": n, "minimum": 3}

    # Incrementally analyze
    per_text_metrics = []
    per_text_rhetoric = []
    per_text_signals = []

    for t in texts:
        m = extract_single_text(t["text"])
        m["_datei"] = Path(t["path"]).name
        per_text_metrics.append(m)

        r = analyze_rhetoric(t["text"])
        per_text_rhetoric.append(r)

        per_text_signals.append(extract_signal_words(m))

    increments = []
    prev_agg = None
    prev_signals = set()
    prev_rhetoric_types = set()

    for i in range(2, n + 1):
        subset = per_text_metrics[:i]
        agg = aggregate_metrics(subset)

        current_signals = set()
        for s in per_text_signals[:i]:
            current_signals.update(s)

        current_rhetoric_types = set()
        for r in per_text_rhetoric[:i]:
            counts = count_rhetoric_types(r)
            for typ, cnt in counts.items():
                if cnt > 0:
                    current_rhetoric_types.add(typ)

        entry = {
            "rede_nr": i,
            "datei": Path(texts[i - 1]["path"]).name,
            "wörter": len(texts[i - 1]["text"].split()),
        }

        if prev_agg is not None:
            deltas = []
            for label, keys in TRACKED_DIMENSIONS:
                old_val = num(get_nested(prev_agg, *keys))
                new_val = num(get_nested(agg, *keys))
                pct = pct_change(old_val, new_val)
                if pct is not None:
                    deltas.append({
                        "dimension": label,
                        "vorher": round(old_val, 2) if old_val is not None else None,
                        "nachher": round(new_val, 2) if new_val is not None else None,
                        "delta_pct": round(pct, 1),
                        "signifikant": abs(pct) > SIGNIFICANCE_THRESHOLD,
                    })

            new_words = current_signals - prev_signals
            new_rhetoric = current_rhetoric_types - prev_rhetoric_types

            significant_count = sum(1 for d in deltas if d["signifikant"])
            avg_shift = statistics.mean([abs(d["delta_pct"]) for d in deltas]) if deltas else 0

            if avg_shift > SIGNIFICANCE_THRESHOLD:
                verdict = "ERWEITERT"
            elif avg_shift > STABILITY_THRESHOLD:
                verdict = "VERFEINERT"
            else:
                verdict = "BESTÄTIGT"

            entry["deltas"] = deltas
            entry["signifikante_shifts"] = significant_count
            entry["durchschnitt_shift"] = round(avg_shift, 1)
            entry["neue_signalwörter"] = sorted(new_words)
            entry["neue_signalwörter_anzahl"] = len(new_words)
            entry["neue_rhetorik_muster"] = sorted(new_rhetoric)
            entry["bewertung"] = verdict
        else:
            entry["bewertung"] = "BASIS"
            entry["deltas"] = []
            entry["neue_signalwörter"] = []
            entry["neue_signalwörter_anzahl"] = 0
            entry["neue_rhetorik_muster"] = []

        increments.append(entry)
        prev_agg = agg
        prev_signals = current_signals
        prev_rhetoric_types = current_rhetoric_types

    # Overall convergence assessment
    if n <= 2:
        overall = "UNZUREICHEND"
        recommendation = "Mindestens 3 Reden empfohlen, besser 5-10."
    else:
        last_shifts = [
            inc["durchschnitt_shift"]
            for inc in increments
            if "durchschnitt_shift" in inc
        ]

        if not last_shifts:
            overall = "UNZUREICHEND"
            recommendation = "Zu wenig Daten für eine Bewertung."
        else:
            last_two = last_shifts[-2:] if len(last_shifts) >= 2 else last_shifts
            avg_recent = statistics.mean(last_two)

            if avg_recent <= STABILITY_THRESHOLD:
                overall = "STABIL"
                recommendation = (
                    f"DNA konvergiert (Ø Shift der letzten Reden: {avg_recent:.1f}%). "
                    f"{n} Reden sind eine solide Basis."
                )
            elif avg_recent <= SIGNIFICANCE_THRESHOLD:
                overall = "FAST STABIL"
                recommendation = (
                    f"DNA wird stabil (Ø Shift: {avg_recent:.1f}%). "
                    f"1-2 weitere Reden zur Absicherung empfohlen."
                )
            else:
                overall = "INSTABIL"
                recommendation = (
                    f"DNA verschiebt sich noch deutlich (Ø Shift: {avg_recent:.1f}%). "
                    f"Mehr Reden nötig — Ziel: Shift unter {STABILITY_THRESHOLD}%."
                )

    # Print report
    print(f"{'─' * 60}")
    for inc in increments:
        nr = inc["rede_nr"]
        name = inc["datei"]
        words = inc["wörter"]
        verdict = inc["bewertung"]

        if verdict == "BASIS":
            print(f"Rede 1-2: Basis-Analyse ({name}, {words} Wörter)")
            print()
            continue

        icon = {"ERWEITERT": "🔵", "VERFEINERT": "🟡", "BESTÄTIGT": "🟢"}.get(verdict, "⚪")
        print(f"Rede {nr} \"{name}\" ({words} Wörter):")

        sig = inc.get("signifikante_shifts", 0)
        avg = inc.get("durchschnitt_shift", 0)
        print(f"  Metriken-Drift:     Ø {avg}% ({sig} signifikante Shifts)")

        new_w = inc.get("neue_signalwörter_anzahl", 0)
        if new_w > 0:
            examples = inc["neue_signalwörter"][:5]
            print(f"  Neue Signalwörter:  +{new_w} ({', '.join(examples)}{'...' if new_w > 5 else ''})")
        else:
            print(f"  Neue Signalwörter:  keine")

        new_r = inc.get("neue_rhetorik_muster", [])
        if new_r:
            print(f"  Neue Rhetorik:      {', '.join(new_r)}")
        else:
            print(f"  Neue Rhetorik:      keine neuen Muster")

        print(f"  {icon} Bewertung:        Diese Rede hat den Stil {verdict}")

        # Show top shifting dimensions
        top_deltas = sorted(
            [d for d in inc.get("deltas", []) if d["signifikant"]],
            key=lambda x: abs(x["delta_pct"]),
            reverse=True,
        )[:3]
        if top_deltas:
            for d in top_deltas:
                sign = "+" if d["delta_pct"] > 0 else ""
                print(f"    ↳ {d['dimension']}: {d['vorher']} → {d['nachher']} ({sign}{d['delta_pct']}%)")

        print()

    print(f"{'=' * 60}")
    icon = {"STABIL": "🟢", "FAST STABIL": "🟡", "INSTABIL": "🔴", "UNZUREICHEND": "⚪"}.get(overall, "⚪")
    print(f"{icon} GESAMTBEWERTUNG: {overall}")
    print(f"   {recommendation}")
    print(f"{'=' * 60}")

    result = {
        "status": overall.lower().replace(" ", "_"),
        "reden": n,
        "empfehlung": recommendation,
        "inkremente": increments,
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"\nDiagnose gespeichert: {output_path}")

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python diagnose_convergence.py <speeches_dir> [output_path]")
        print("  speeches_dir: Directory with example speeches (.txt/.md)")
        print("  output_path:  Optional path for JSON output")
        sys.exit(1)

    speeches_dir = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    diagnose(speeches_dir, output_path)


if __name__ == "__main__":
    main()
