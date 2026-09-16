#!/usr/bin/env python3
"""Validate a generated speech against style DNA metrics."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _shared import num, load_single_text
from extract_metrics import extract_single_text


def check_metric(
    name: str,
    target_val,
    actual_val,
    tolerance_pct: float = 25,
) -> dict | None:
    if target_val is None or actual_val is None:
        return None

    t = num(target_val)
    a = num(actual_val)
    if t is None or a is None:
        return None

    if t == 0:
        deviation = abs(a) * 100
    else:
        deviation = abs(a - t) / abs(t) * 100

    return {
        "name": name,
        "ziel": round(t, 2),
        "ist": round(a, 2),
        "abweichung_pct": round(deviation, 1),
        "status": "✓" if deviation <= tolerance_pct else "⚠️",
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python validate_speech.py <speech_file> <metrics_file>")
        sys.exit(1)

    speech_path = Path(sys.argv[1])
    metrics_path = Path(sys.argv[2])

    text = load_single_text(speech_path)

    target = json.loads(metrics_path.read_text(encoding="utf-8"))
    ta = target["metriken"]["aggregiert"]

    print(f"Validiere: {speech_path.name} ({len(text.split())} Wörter)")
    print(f"Gegen DNA: {metrics_path.name}")
    print(f"{'=' * 60}")

    actual = extract_single_text(text)

    checks = []

    def _add(name, tp, ap, tol=25):
        c = check_metric(name, tp, ap, tol)
        if c:
            checks.append(c)

    _add("Satzlänge (Ø Wörter)", ta.get("sätze", {}).get("wörter_pro_satz"), actual.get("sätze", {}).get("wörter_pro_satz"))
    _add("Stakkato-Quote", ta.get("sätze", {}).get("stakkato_quote"), actual.get("sätze", {}).get("stakkato_quote"), 40)
    _add("Type-Token-Ratio", ta.get("wörter", {}).get("type_token_ratio"), actual.get("wörter", {}).get("type_token_ratio"))
    _add("Füllwörter/1000", ta.get("wörter", {}).get("füllwörter_pro_1000"), actual.get("wörter", {}).get("füllwörter", {}).get("pro_1000_wörter"), 40)
    _add("Modalverben/1000", ta.get("wörter", {}).get("modalverben_pro_1000"), actual.get("wörter", {}).get("modalverben", {}).get("pro_1000_wörter"), 35)
    _add("Wortlänge (Ø)", ta.get("wörter", {}).get("wortlänge"), actual.get("wörter", {}).get("wortlänge"))
    _add("Wir/Ich-Verhältnis", ta.get("pronomen", {}).get("wir_ich_verhältnis"), actual.get("pronomen", {}).get("wir_ich_verhältnis"), 50)
    _add("Aktiv-Anteil (%)", ta.get("grammatik", {}).get("aktiv_prozent"), actual.get("grammatik", {}).get("aktiv_passiv", {}).get("aktiv_prozent"), 15)
    _add("Adjektiv-Dichte (%)", ta.get("grammatik", {}).get("adjektiv_dichte"), actual.get("grammatik", {}).get("adjektiv_dichte_prozent"), 30)
    _add("Flesch-Index", ta.get("lesbarkeit", {}).get("flesch_reading_ease"), actual.get("lesbarkeit", {}).get("flesch_reading_ease"), 20)
    _add("Silben/Wort (Ø)", ta.get("lesbarkeit", {}).get("silben_pro_wort"), actual.get("lesbarkeit", {}).get("durchschnitt_silben_pro_wort"))

    tp = ta.get("interpunktion", {}).get("pro_1000_wörter", {})
    ap = actual.get("interpunktion", {}).get("pro_1000_wörter", {})
    for key in ("gedankenstriche", "fragezeichen", "ausrufezeichen", "kommas"):
        if key in tp and key in ap:
            _add(f"Interpunktion: {key.capitalize()}/1000", tp[key], ap[key], 40)

    passed = sum(1 for c in checks if c["status"] == "✓")
    total = len(checks)
    score = round(passed / total * 100) if total else 0

    print()
    print(f"{'Dimension':<32} {'Ziel':>8} {'Ist':>8} {'Abw.':>8} Status")
    print(f"{'-' * 32} {'-' * 8} {'-' * 8} {'-' * 8} {'-' * 6}")
    for c in checks:
        print(f"{c['name']:<32} {c['ziel']:>8} {c['ist']:>8} {c['abweichung_pct']:>7}% {c['status']}")

    print(f"\n{'=' * 60}")
    print(f"STIL-ÜBEREINSTIMMUNG: {score}/100  ({passed}/{total} Dimensionen im Toleranzbereich)")

    if score >= 85:
        print("→ Sehr gute Übereinstimmung mit der Sprach-DNA")
    elif score >= 70:
        print("→ Gute Übereinstimmung, einzelne Dimensionen weichen ab")
    elif score >= 50:
        print("→ Moderate Übereinstimmung, Überarbeitung empfohlen")
    else:
        print("→ Niedrige Übereinstimmung, Rede sollte überarbeitet werden")

    report = {"score": score, "passed": passed, "total": total, "checks": checks}
    report_path = speech_path.parent / f"validation-{speech_path.stem}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nReport gespeichert: {report_path}")


if __name__ == "__main__":
    main()
