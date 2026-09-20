#!/usr/bin/env python3
"""Compare function word usage of a speech against the example speeches.

The 47 dimensions cover content-bearing style (sentence length, TTR,
rhetoric) and a few hand-picked closed-class groups (fillers, modals,
pronouns). What they do not show is which of the many small words a speaker
actually prefers: "aber" or "jedoch", "weil" or "denn", "sehr" or "ganz".
These choices are made unconsciously, stay stable across topics and are
therefore one of the oldest markers in stylometry.

This script counts closed-class tokens (determiners, prepositions,
conjunctions, auxiliaries, pronouns, particles) in the speech and in the
example speeches and shows where the rates per 1000 tokens differ most.
The word classes come from the spaCy POS tags, so no word list has to be
maintained; only the connective adverbs are listed explicitly, because
spaCy tags them as ADV, together with "heute" or "schnell".

Descriptive comparison, nothing more: with the corpus sizes that are usual
here, a difference is a hint to look at a word, not proof of anything. The
result does not affect the validation score.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _shared import nlp, load_texts, load_single_text

# Closed word classes: new members are practically never added to them,
# which is what makes their distribution a stable speaker fingerprint.
FUNCTION_POS = {"DET", "ADP", "CCONJ", "SCONJ", "AUX", "PRON", "PART"}

# Connective adverbs: they join sentences like conjunctions ("aber" vs.
# "jedoch"), but spaCy tags them as ADV, so they need to be named.
CONNECTIVE_ADVERBS = {
    "jedoch", "allerdings", "dennoch", "trotzdem", "gleichwohl", "hingegen",
    "dagegen", "stattdessen", "vielmehr", "deshalb", "deswegen", "darum",
    "daher", "somit", "folglich", "außerdem", "zudem", "ferner", "ebenfalls",
    "ebenso", "insofern", "dabei", "dadurch", "dazu", "damit", "dafür",
}

MIN_OCCURRENCES = 5
TOP_N = 12
SMALL_CORPUS_WORDS = 5000


def fmt_int(n: int) -> str:
    """German thousands separator: 12345 -> 12.345"""
    return f"{n:,}".replace(",", ".")


def function_word_counts(texts: list[dict]) -> tuple[Counter, int]:
    counts: Counter = Counter()
    total = 0
    for t in texts:
        for token in nlp(t["text"]):
            if token.is_alpha:
                total += 1
                if token.pos_ in FUNCTION_POS or token.lower_ in CONNECTIVE_ADVERBS:
                    counts[token.lower_] += 1
    return counts, total


def rate(count: int, total: int) -> float:
    return round(count / total * 1000, 2) if total else 0.0


def main():
    argv = sys.argv[1:]
    top_n = TOP_N
    if "--anzahl" in argv:
        i = argv.index("--anzahl")
        top_n = int(argv[i + 1])
        del argv[i:i + 2]

    if len(argv) < 2:
        print("Usage: python check_function_words.py <speech_file> <speeches_dir> "
              "[--anzahl N]")
        print("  speech_file:  Speech to check (.txt/.md)")
        print("  speeches_dir: Example speeches of the speaker (comparison base)")
        print("  --anzahl:     How many deviations to show (default 12)")
        sys.exit(1)

    speech_path = Path(argv[0])
    speeches_dir = Path(argv[1])

    corpus = [t for t in load_texts(speeches_dir)
              if Path(t["path"]).resolve() != speech_path.resolve()]
    if not corpus:
        print(f"Fehler: Keine Beispielreden in {speeches_dir} gefunden")
        sys.exit(1)

    corpus_counts, corpus_words = function_word_counts(corpus)
    speech_counts, speech_words = function_word_counts(
        [{"text": load_single_text(speech_path)}]
    )

    rows = []
    for word in set(corpus_counts) | set(speech_counts):
        in_corpus = corpus_counts[word]
        in_speech = speech_counts[word]
        if in_corpus + in_speech < MIN_OCCURRENCES:
            continue
        r_corpus = rate(in_corpus, corpus_words)
        r_speech = rate(in_speech, speech_words)
        rows.append({
            "wort": word,
            "korpus_pro_1000": r_corpus,
            "rede_pro_1000": r_speech,
            "differenz": round(r_speech - r_corpus, 2),
            "korpus_anzahl": in_corpus,
            "rede_anzahl": in_speech,
        })

    rows.sort(key=lambda r: -abs(r["differenz"]))
    shown = rows[:top_n]

    print(f"Funktionswort-Abgleich: {speech_path.name} ({fmt_int(speech_words)} Wörter)")
    print(f"Vergleichsbasis: {len(corpus)} Beispielreden, {fmt_int(corpus_words)} Wörter")
    print(f"{'=' * 60}")

    if corpus_words < SMALL_CORPUS_WORDS:
        print(f"⚠️  Vergleichsbasis unter {fmt_int(SMALL_CORPUS_WORDS)} Wörtern — die "
              "Raten schwanken dann stark.")

    if shown:
        print("\nGRÖSSTE ABWEICHUNGEN (je 1000 Wörter):")
        print(f"\n{'Wort':<16} {'Korpus':>9} {'Rede':>9} {'Diff':>9}")
        print(f"{'-' * 16} {'-' * 9} {'-' * 9} {'-' * 9}")
        for r in shown:
            mark = "↑" if r["differenz"] > 0 else "↓"
            print(f"{r['wort']:<16} {r['korpus_pro_1000']:>9} {r['rede_pro_1000']:>9} "
                  f"{r['differenz']:>8} {mark}")
        print("\n↑ in der Rede häufiger als beim Redner üblich, ↓ seltener.")
    else:
        print("\nZu wenig Material für einen Vergleich.")

    print("\nDie Liste zeigt, wo nachgeschaut werden kann — sie ist kein Urteil. "
          "Thema und\nLänge verschieben diese Raten mit. Keine Wörter einsetzen, "
          "nur damit eine Rate passt.")

    report = {
        "rede": speech_path.name,
        "rede_wörter": speech_words,
        "korpus_reden": len(corpus),
        "korpus_wörter": corpus_words,
        "abweichungen": shown,
    }
    report_path = speech_path.parent / f"funktionswörter-{speech_path.stem}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nReport gespeichert: {report_path}")


if __name__ == "__main__":
    main()
