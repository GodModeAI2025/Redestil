#!/usr/bin/env python3
"""Flag words in a speech that the speaker (almost) never uses.

Aggregate metrics like TTR or sentence length can all be in range while a
generated speech still contains words that feel foreign to the speaker
("fundamental", "maßgeblich", "nahtlos" ...). This script compares the lemmas
of a speech against the lemmas of the example speeches and lists content
words that occur at most N times in the speaker's own material.

Lemma comparison (spaCy) instead of raw word forms, so that inflected forms
("gestalten", "gestaltet", "gestaltete") do not cause false alarms. Words
that appear in the reference sources can be excluded, because topic
vocabulary from the briefing is legitimately new.

The result is a list to look at, not a list to delete. It does not affect
the validation score.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _shared import nlp, load_texts, load_single_text

MIN_WORD_LENGTH = 5
SMALL_CORPUS_WORDS = 5000


def fmt_int(n: int) -> str:
    """German thousands separator: 12345 -> 12.345"""
    return f"{n:,}".replace(",", ".")


def is_candidate(token) -> bool:
    """Content words only: no names, numbers, stop words or short words."""
    return (
        token.is_alpha
        and not token.is_stop
        and token.pos_ not in ("PROPN", "NUM", "X")
        and len(token.text) >= MIN_WORD_LENGTH
    )


def lemma_counts(texts: list[dict]) -> tuple[Counter, int]:
    counts: Counter = Counter()
    total = 0
    for t in texts:
        for token in nlp(t["text"]):
            if token.is_alpha:
                total += 1
                counts[token.lemma_.lower()] += 1
    return counts, total


def main():
    argv = sys.argv[1:]
    threshold = 1
    sources_dir = None
    if "--schwelle" in argv:
        i = argv.index("--schwelle")
        threshold = int(argv[i + 1])
        del argv[i:i + 2]
    if "--quellen" in argv:
        i = argv.index("--quellen")
        sources_dir = Path(argv[i + 1])
        del argv[i:i + 2]

    if len(argv) < 2:
        print("Usage: python check_vocabulary.py <speech_file> <speeches_dir> "
              "[--quellen <sources_dir>] [--schwelle N]")
        print("  speech_file:  Speech to check (.txt/.md)")
        print("  speeches_dir: Example speeches of the speaker (comparison base)")
        print("  --quellen:    Optional sources; their vocabulary is not flagged")
        print("  --schwelle:   Max. occurrences in the corpus to flag a word (default 1)")
        sys.exit(1)

    speech_path = Path(argv[0])
    speeches_dir = Path(argv[1])

    corpus = [t for t in load_texts(speeches_dir)
              if Path(t["path"]).resolve() != speech_path.resolve()]
    if not corpus:
        print(f"Fehler: Keine Beispielreden in {speeches_dir} gefunden")
        sys.exit(1)

    counts, corpus_words = lemma_counts(corpus)

    source_lemmas: set[str] = set()
    if sources_dir and sources_dir.exists():
        source_counts, _ = lemma_counts(load_texts(sources_dir))
        source_lemmas = set(source_counts)

    doc = nlp(load_single_text(speech_path))
    suspects: dict[str, dict] = {}
    for token in doc:
        if not is_candidate(token):
            continue
        lemma = token.lemma_.lower()
        if lemma in source_lemmas:
            continue
        n = counts[lemma]
        if n <= threshold:
            entry = suspects.setdefault(lemma, {"lemma": lemma, "im_korpus": n, "formen": []})
            if token.text not in entry["formen"]:
                entry["formen"].append(token.text)

    ranked = sorted(suspects.values(), key=lambda e: (e["im_korpus"], e["lemma"]))

    print(f"Wortschatz-Abgleich: {speech_path.name}")
    print(f"Vergleichsbasis: {len(corpus)} Beispielreden, {fmt_int(corpus_words)} Wörter")
    if source_lemmas:
        print(f"Quellen-Vokabular ausgenommen: {len(source_lemmas)} Lemmata")
    print(f"{'=' * 60}")

    if corpus_words < SMALL_CORPUS_WORDS:
        print(f"⚠️  Vergleichsbasis unter {fmt_int(SMALL_CORPUS_WORDS)} Wörtern — viele Treffer "
              "sind dann Zufall, nicht Stilbruch.")

    if ranked:
        print(f"\nAUFFÄLLIG — Lemma kommt höchstens {threshold}x in den Beispielreden vor:")
        for e in ranked:
            print(f"  {e['im_korpus']:>3}x  {e['lemma']:<24} ({', '.join(e['formen'])})")
    else:
        print("\nKeine auffälligen Wörter.")

    print("\nNicht jeder Treffer ist falsch — Fachbegriffe und Themenwörter landen "
          "hier auch.\nDas ist eine Liste zum Anschauen, keine Streichliste.")

    report = {
        "rede": speech_path.name,
        "korpus_reden": len(corpus),
        "korpus_wörter": corpus_words,
        "schwelle": threshold,
        "auffällig": ranked,
    }
    report_path = speech_path.parent / f"vokabular-{speech_path.stem}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nReport gespeichert: {report_path}")


if __name__ == "__main__":
    main()
