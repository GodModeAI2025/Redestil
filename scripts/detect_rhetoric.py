#!/usr/bin/env python3
"""Rhetorical figure detection for German texts."""

import json
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

from _shared import nlp, load_texts


def get_sentences(text: str) -> list[str]:
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]


def _detect_repeated_position(sentences: list[str], position: str, typ: str, min_consecutive: int = 2) -> list[dict]:
    findings = []
    i = 0
    while i < len(sentences) - 1:
        if position == "start":
            words = sentences[i].split()
            key_word = words[0].lower().strip("„\"'»«") if words else ""
        else:
            words = sentences[i].rstrip(".!?…").split()
            key_word = words[-1].lower() if words else ""

        if not key_word:
            i += 1
            continue

        consecutive = [sentences[i]]
        j = i + 1
        while j < len(sentences):
            if position == "start":
                nw = sentences[j].split()
                next_key = nw[0].lower().strip("„\"'»«") if nw else ""
            else:
                nw = sentences[j].rstrip(".!?…").split()
                next_key = nw[-1].lower() if nw else ""
            if next_key == key_word:
                consecutive.append(sentences[j])
                j += 1
            else:
                break

        if len(consecutive) >= min_consecutive:
            findings.append({
                "typ": typ,
                "wiederholung": key_word,
                "anzahl": len(consecutive),
                "beispiel": consecutive[:3],
            })
            i = j
        else:
            i += 1

    return findings


def detect_anaphora(sentences: list[str], min_consecutive: int = 2) -> list[dict]:
    return _detect_repeated_position(sentences, "start", "anapher", min_consecutive)


def detect_epiphora(sentences: list[str], min_consecutive: int = 2) -> list[dict]:
    return _detect_repeated_position(sentences, "end", "epipher", min_consecutive)


def detect_tricolon(sentences: list[str]) -> list[dict]:
    findings = []
    for sent in sentences:
        parts = [p.strip() for p in sent.split(",")]
        if len(parts) >= 3:
            for k in range(len(parts) - 2):
                trio = parts[k : k + 3]
                lens = [len(p.split()) for p in trio]
                if all(lens) and max(lens) <= min(lens) * 2.5:
                    findings.append({
                        "typ": "trikolon",
                        "elemente": trio,
                        "beispiel": sent,
                    })
                    break

        match = re.search(
            r"(\w[\w\s]{2,30}),\s+(\w[\w\s]{2,30})\s+und\s+(\w[\w\s]{2,30})", sent
        )
        if match:
            findings.append({
                "typ": "trikolon",
                "elemente": [match.group(1).strip(), match.group(2).strip(), match.group(3).strip()],
                "beispiel": sent,
            })

    return findings


def detect_rhetorical_questions(sentences: list[str]) -> list[dict]:
    findings = []
    rhetorical_starters = [
        r"^wollen wir\b", r"^ist es nicht\b", r"^können wir\b",
        r"^sollen wir\b", r"^was wäre\b", r"^wer kann\b",
        r"^wer will\b", r"^wie lange\b", r"^warum nicht\b",
        r"^sind wir nicht\b", r"^haben wir nicht\b",
    ]
    answer_starters = {
        "ja", "nein", "doch", "genau", "richtig", "natürlich", "selbstverständlich"
    }

    for i, sent in enumerate(sentences):
        if not sent.endswith("?"):
            continue

        is_rhetorical = False
        for pattern in rhetorical_starters:
            if re.match(pattern, sent, re.IGNORECASE):
                is_rhetorical = True
                break

        if not is_rhetorical and i + 1 < len(sentences):
            first_word = sentences[i + 1].split()[0].lower().rstrip(",.:") if sentences[i + 1].split() else ""
            if first_word not in answer_starters:
                is_rhetorical = True
        elif not is_rhetorical:
            is_rhetorical = True

        if is_rhetorical:
            findings.append({"typ": "rhetorische_frage", "beispiel": sent})

    return findings


def detect_antithesis(sentences: list[str]) -> list[dict]:
    findings = []
    patterns = [
        r"\baber\b", r"\bdoch\b", r"\bjedoch\b", r"\bsondern\b",
        r"\bwährend\b", r"\bstatt\b", r"\banstatt\b",
        r"\bnicht\s+\w+,\s+sondern\b",
        r"\beinerseits\b.*\bandererseits\b",
    ]

    for sent in sentences:
        for pat in patterns:
            m = re.search(pat, sent, re.IGNORECASE)
            if m:
                findings.append({
                    "typ": "antithese",
                    "marker": m.group(),
                    "beispiel": sent,
                })
                break

    return findings


def detect_repetition(sentences: list[str]) -> list[dict]:
    phrase_locs: dict[str, set[int]] = defaultdict(set)
    for i, sent in enumerate(sentences):
        words = sent.lower().split()
        for n in range(2, 5):
            for j in range(len(words) - n + 1):
                phrase = " ".join(words[j : j + n])
                if len(phrase) > 5:
                    phrase_locs[phrase].add(i)

    seen: set[str] = set()
    findings = []
    for phrase, locs in sorted(phrase_locs.items(), key=lambda x: -len(x[1])):
        if len(locs) < 3:
            continue
        if any(phrase in existing for existing in seen):
            continue
        seen.add(phrase)
        findings.append({
            "typ": "wiederholung",
            "phrase": phrase,
            "vorkommen": len(locs),
        })
    return findings[:20]


def analyze_rhetoric(text: str) -> dict:
    sentences = get_sentences(text)
    anaphern = detect_anaphora(sentences)
    epiphern = detect_epiphora(sentences)
    trikola = detect_tricolon(sentences)
    rhet_fragen = detect_rhetorical_questions(sentences)
    antithesen = detect_antithesis(sentences)
    wiederholungen = detect_repetition(sentences)

    return {
        "anaphern": anaphern,
        "epiphern": epiphern,
        "trikola": trikola,
        "rhetorische_fragen": rhet_fragen,
        "antithesen": antithesen,
        "wiederholungen": wiederholungen,
        "statistik": {
            "anaphern_anzahl": len(anaphern),
            "epiphern_anzahl": len(epiphern),
            "trikola_anzahl": len(trikola),
            "rhetorische_fragen_anzahl": len(rhet_fragen),
            "antithesen_anzahl": len(antithesen),
            "wiederholungen_anzahl": len(wiederholungen),
        },
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python detect_rhetoric.py <input_dir> <output_path>")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    texts = load_texts(input_dir)
    if not texts:
        print(f"Fehler: Keine .txt oder .md Dateien in {input_dir}")
        sys.exit(1)

    print(f"Analysiere Rhetorik in {len(texts)} Texten...")

    per_text = []
    for t in texts:
        print(f"  → {Path(t['path']).name}")
        result = analyze_rhetoric(t["text"])
        result["_datei"] = Path(t["path"]).name
        per_text.append(result)

    total_words = sum(len(t["text"].split()) for t in texts)
    agg_stats: dict = {
        "anaphern_gesamt": sum(r["statistik"]["anaphern_anzahl"] for r in per_text),
        "rhetorische_fragen_gesamt": sum(r["statistik"]["rhetorische_fragen_anzahl"] for r in per_text),
        "antithesen_gesamt": sum(r["statistik"]["antithesen_anzahl"] for r in per_text),
        "trikola_gesamt": sum(r["statistik"]["trikola_anzahl"] for r in per_text),
    }
    if total_words > 0:
        f = 1000 / total_words
        agg_stats["pro_1000_wörter"] = {
            k.replace("_gesamt", ""): round(v * f, 2)
            for k, v in agg_stats.items()
            if k.endswith("_gesamt")
        }

    result = {"aggregiert": agg_stats, "pro_text": per_text}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nRhetorik-Analyse gespeichert: {output_path}")


if __name__ == "__main__":
    main()
