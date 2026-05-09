#!/usr/bin/env python3
"""Compare original and revised speeches to extract feedback learnings.

Identifies what the user changed and maps deltas to SPRACH-DNA dimensions,
producing an actionable improvement report.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from _shared import get_nested, num, pct_change, load_single_text
from extract_metrics import extract_single_text


DIMENSION_LABELS = {
    "satzlänge": "Satzlänge (Wörter pro Satz)",
    "stakkato": "Stakkato-Quote (kurze Sätze)",
    "ttr": "Vokabularreichtum (Type-Token-Ratio)",
    "füllwörter": "Füllwort-Dichte",
    "modalverben": "Modalverb-Frequenz",
    "wortlänge": "Durchschnittliche Wortlänge",
    "aktiv_passiv": "Aktiv/Passiv-Verhältnis",
    "adjektive": "Adjektiv-Dichte",
    "flesch": "Lesbarkeit (Flesch-Index)",
    "silben": "Silben pro Wort",
    "fragen": "Fragezeichen-Dichte",
    "ausrufe": "Ausrufezeichen-Dichte",
    "kommas": "Komma-Dichte",
    "gedankenstriche": "Gedankenstrich-Verwendung",
    "pronomen_wir_ich": "Wir/Ich-Verhältnis",
}


def extract_deltas(original: dict, revised: dict) -> list[dict]:
    """Compare two metric sets and return significant deltas."""
    paths = [
        ("satzlänge", ["sätze", "wörter_pro_satz", "mittelwert"]),
        ("stakkato", ["sätze", "stakkato_quote"]),
        ("ttr", ["wörter", "type_token_ratio"]),
        ("füllwörter", ["wörter", "füllwörter", "pro_1000_wörter"]),
        ("modalverben", ["wörter", "modalverben", "pro_1000_wörter"]),
        ("wortlänge", ["wörter", "wortlänge", "mittelwert"]),
        ("aktiv_passiv", ["grammatik", "aktiv_passiv", "aktiv_prozent"]),
        ("adjektive", ["grammatik", "adjektiv_dichte_prozent"]),
        ("flesch", ["lesbarkeit", "flesch_reading_ease"]),
        ("silben", ["lesbarkeit", "durchschnitt_silben_pro_wort"]),
        ("fragen", ["interpunktion", "pro_1000_wörter", "fragezeichen"]),
        ("ausrufe", ["interpunktion", "pro_1000_wörter", "ausrufezeichen"]),
        ("kommas", ["interpunktion", "pro_1000_wörter", "kommas"]),
        ("gedankenstriche", ["interpunktion", "pro_1000_wörter", "gedankenstriche"]),
        ("pronomen_wir_ich", ["pronomen", "wir_ich_verhältnis"]),
    ]

    deltas = []
    for key, path in paths:
        o = get_nested(original, *path)
        r = get_nested(revised, *path)
        o_num = num(o) if not isinstance(o, (int, float)) else o
        r_num = num(r) if not isinstance(r, (int, float)) else r

        if o_num is None or r_num is None:
            continue

        abs_delta = r_num - o_num
        rel_delta = pct_change(o_num, r_num)
        if rel_delta is None:
            continue

        if abs(rel_delta) < 5:
            continue

        direction = "erhöht" if abs_delta > 0 else "reduziert"
        deltas.append({
            "dimension": key,
            "label": DIMENSION_LABELS.get(key, key),
            "original": round(o_num, 2),
            "überarbeitet": round(r_num, 2),
            "delta_absolut": round(abs_delta, 2),
            "delta_prozent": round(rel_delta, 1),
            "richtung": direction,
        })

    deltas.sort(key=lambda d: abs(d["delta_prozent"]), reverse=True)
    return deltas


def compare_satztypen(original: dict, revised: dict) -> list[dict]:
    """Compare sentence type distributions."""
    o_types = _get(original, "sätze", "satztypen_prozent", default={})
    r_types = _get(revised, "sätze", "satztypen_prozent", default={})
    all_keys = set(o_types) | set(r_types)
    changes = []
    for k in all_keys:
        ov = o_types.get(k, 0)
        rv = r_types.get(k, 0)
        if abs(rv - ov) > 3:
            changes.append({
                "satztyp": k,
                "original_pct": ov,
                "überarbeitet_pct": rv,
                "delta": round(rv - ov, 1),
            })
    return changes


def generate_learnings(deltas: list[dict], satztyp_changes: list[dict], text_feedback: str | None) -> dict:
    """Synthesize deltas + optional text feedback into structured learnings."""
    learnings = {
        "datum": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "quantitative_korrekturen": [],
        "satztyp_korrekturen": satztyp_changes,
        "text_feedback": text_feedback,
        "dna_update_empfehlungen": [],
        "skill_verbesserungen": [],
    }

    for d in deltas:
        severity = "hoch" if abs(d["delta_prozent"]) > 30 else "mittel" if abs(d["delta_prozent"]) > 15 else "niedrig"
        learnings["quantitative_korrekturen"].append({
            **d,
            "schweregrad": severity,
        })

        if severity in ("hoch", "mittel"):
            learnings["dna_update_empfehlungen"].append(
                f"{d['label']}: Zielwert von {d['original']} auf {d['überarbeitet']} anpassen "
                f"(User hat {d['richtung']} um {abs(d['delta_prozent'])}%)"
            )

    high_severity = [d for d in deltas if abs(d["delta_prozent"]) > 30]
    if high_severity:
        affected_dims = [d["dimension"] for d in high_severity]

        if "satzlänge" in affected_dims or "stakkato" in affected_dims:
            learnings["skill_verbesserungen"].append({
                "bereich": "Satz-Architektur",
                "problem": "Generierte Satzlänge weicht stark vom Nutzerwunsch ab",
                "empfehlung": "Satzlängen-Constraints im Generierungs-Prompt verschärfen",
            })

        if "füllwörter" in affected_dims or "modalverben" in affected_dims:
            learnings["skill_verbesserungen"].append({
                "bereich": "Wort-DNA",
                "problem": "Füllwort-/Modalverb-Dichte passt nicht",
                "empfehlung": "Explizite Wortlisten in DNA aufnehmen mit Frequenz-Vorgaben",
            })

        if "aktiv_passiv" in affected_dims:
            learnings["skill_verbesserungen"].append({
                "bereich": "Grammatik-Profil",
                "problem": "Aktiv/Passiv-Balance stimmt nicht",
                "empfehlung": "Voice-Constraint als harte Regel im Generierungs-Prompt",
            })

        if any(d in affected_dims for d in ("fragen", "ausrufe", "kommas", "gedankenstriche")):
            learnings["skill_verbesserungen"].append({
                "bereich": "Interpunktion",
                "problem": "Interpunktionsmuster weichen ab",
                "empfehlung": "Interpunktions-Profil als explizite Checkliste in den Validierungs-Loop",
            })

    return learnings


def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_feedback.py <original_speech> <revised_speech> [text_feedback]")
        print("  original_speech: Path to the generated speech")
        print("  revised_speech:  Path to the user-revised speech")
        print("  text_feedback:   Optional free-text feedback string")
        sys.exit(1)

    original_path = Path(sys.argv[1])
    revised_path = Path(sys.argv[2])
    text_feedback = sys.argv[3] if len(sys.argv) > 3 else None

    orig_text = load_single_text(original_path)
    rev_text = load_single_text(revised_path)

    print(f"Original:     {original_path.name} ({len(orig_text.split())} Wörter)")
    print(f"Überarbeitet: {revised_path.name} ({len(rev_text.split())} Wörter)")
    print(f"{'=' * 60}")

    print("\nAnalysiere Original...")
    orig_metrics = extract_single_text(orig_text)

    print("Analysiere Überarbeitung...")
    rev_metrics = extract_single_text(rev_text)

    print("\nBerechne Deltas...")
    deltas = extract_deltas(orig_metrics, rev_metrics)
    satztyp_changes = compare_satztypen(orig_metrics, rev_metrics)
    learnings = generate_learnings(deltas, satztyp_changes, text_feedback)

    print(f"\n{'=' * 60}")
    print("FEEDBACK-ANALYSE")
    print(f"{'=' * 60}")

    if deltas:
        print(f"\n{len(deltas)} signifikante Änderungen erkannt:")
        print(f"{'Dimension':<35} {'Orig':>8} {'Neu':>8} {'Delta':>8}")
        print(f"{'-' * 35} {'-' * 8} {'-' * 8} {'-' * 8}")
        for d in deltas:
            print(f"{d['label']:<35} {d['original']:>8} {d['überarbeitet']:>8} {d['delta_prozent']:>+7.1f}%")
    else:
        print("\nKeine signifikanten quantitativen Änderungen erkannt.")

    if learnings["dna_update_empfehlungen"]:
        print(f"\n--- DNA-Update-Empfehlungen ---")
        for emp in learnings["dna_update_empfehlungen"]:
            print(f"  • {emp}")

    if learnings["skill_verbesserungen"]:
        print(f"\n--- Skill-Verbesserungen ---")
        for sv in learnings["skill_verbesserungen"]:
            print(f"  [{sv['bereich']}] {sv['problem']}")
            print(f"    → {sv['empfehlung']}")

    if text_feedback:
        print(f"\n--- Text-Feedback ---")
        print(f"  \"{text_feedback}\"")

    output_path = original_path.parent / f"feedback-{original_path.stem}-{datetime.now().strftime('%Y%m%d-%H%M')}.json"
    output_path.write_text(
        json.dumps(learnings, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nFeedback-Report gespeichert: {output_path}")


if __name__ == "__main__":
    main()
