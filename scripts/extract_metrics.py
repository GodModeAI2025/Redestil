#!/usr/bin/env python3
"""Quantitative style metrics extraction for German speeches."""

import json
import re
import sys
import statistics
from pathlib import Path
from collections import Counter

import textstat

textstat.set_lang("de")

from _shared import nlp, strip_markdown, load_texts, content_words

GERMAN_FILLERS = {
    "also", "eigentlich", "natürlich", "sozusagen", "quasi", "eben",
    "halt", "irgendwie", "gewissermaßen", "praktisch", "tatsächlich",
    "grundsätzlich", "letztendlich", "schlussendlich", "ja", "nun",
    "doch", "wohl", "schon", "mal", "jedenfalls", "übrigens",
    "immerhin", "allerdings", "durchaus", "gewiss",
}

GERMAN_MODALS = {"können", "sollen", "müssen", "dürfen", "wollen", "mögen"}

PRONOUN_MAP = {
    "ich": "ich", "mich": "ich", "mir": "ich", "mein": "ich",
    "meine": "ich", "meinem": "ich", "meinen": "ich", "meiner": "ich",
    "wir": "wir", "uns": "wir", "unser": "wir", "unsere": "wir",
    "unserem": "wir", "unseren": "wir", "unserer": "wir",
    "du": "du", "dich": "du", "dir": "du", "dein": "du",
    "deine": "du", "deinem": "du", "deinen": "du", "deiner": "du",
    "man": "man", "es": "es",
}

FORMAL_SIE = {"Sie", "Ihnen", "Ihr", "Ihre", "Ihrem", "Ihren", "Ihrer", "Ihres"}



def _safe_stdev(values):
    return round(statistics.stdev(values), 1) if len(values) > 1 else 0.0


STRIP_CHARS = ".,!?;:\"'()[]{}»«„“–—"


def count_syllables_de(word: str) -> int:
    word = word.lower().strip(STRIP_CHARS)
    vowels = "aeiouyäöü"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    return max(count, 1)


def analyze_sentences(doc) -> dict:
    sents = list(doc.sents)
    if not sents:
        return {}

    word_lengths = [
        len([t for t in s if not t.is_punct and not t.is_space]) for s in sents
    ]
    char_lengths = [len(s.text.strip()) for s in sents]

    types = Counter()
    for s in sents:
        text = s.text.strip()
        if text.endswith("?"):
            types["frage"] += 1
        elif text.endswith("!"):
            types["ausruf"] += 1
        elif text.endswith("…") or text.endswith("..."):
            types["ellipse"] += 1
        else:
            types["aussage"] += 1
    total = sum(types.values()) or 1
    type_pct = {k: round(v / total * 100, 1) for k, v in types.items()}

    starts = Counter()
    for s in sents:
        for token in s:
            if not token.is_space and not token.is_punct:
                pos = token.pos_
                bucket = {
                    "PRON": "pronomen", "CCONJ": "konjunktion",
                    "SCONJ": "konjunktion", "ADV": "adverb",
                    "NOUN": "substantiv", "PROPN": "substantiv",
                    "DET": "artikel", "VERB": "verb", "AUX": "verb",
                    "ADJ": "adjektiv",
                }.get(pos, "sonstige")
                starts[bucket] += 1
                break
    total_s = sum(starts.values()) or 1
    start_pct = {k: round(v / total_s * 100, 1) for k, v in starts.most_common()}

    return {
        "anzahl": len(sents),
        "wörter_pro_satz": {
            "mittelwert": round(statistics.mean(word_lengths), 1),
            "median": round(statistics.median(word_lengths), 1),
            "stddev": _safe_stdev(word_lengths),
            "min": min(word_lengths),
            "max": max(word_lengths),
        },
        "zeichen_pro_satz": {
            "mittelwert": round(statistics.mean(char_lengths), 1),
            "median": round(statistics.median(char_lengths), 1),
        },
        "satztypen_prozent": type_pct,
        "satzanfänge_prozent": start_pct,
        "stakkato_quote": round(
            sum(1 for w in word_lengths if w <= 3) / len(word_lengths) * 100, 1
        ),
    }


def analyze_words(doc, words=None) -> dict:
    if words is None:
        words = content_words(doc)
    if not words:
        return {}

    word_texts = [t.text for t in words]
    word_lower = [t.lower_ for t in words]
    tokens_count = len(word_lower)

    word_lens = [len(w) for w in word_texts]
    types_count = len(set(word_lower))
    ttr = round(types_count / tokens_count, 3) if tokens_count else 0

    freq = Counter(word_lower)
    hapax = sum(1 for c in freq.values() if c == 1)
    hapax_ratio = round(hapax / types_count * 100, 1) if types_count else 0

    filler_found = {
        w: freq[w] for w in GERMAN_FILLERS if w in freq
    }
    filler_count = sum(filler_found.values())
    filler_per_1000 = round(filler_count / tokens_count * 1000, 1)

    modal_found: dict[str, int] = {}
    for t in words:
        lemma = t.lemma_.lower()
        if lemma in GERMAN_MODALS:
            modal_found[lemma] = modal_found.get(lemma, 0) + 1
    modal_count = sum(modal_found.values())
    modal_per_1000 = round(modal_count / tokens_count * 1000, 1)

    content_words = [
        t.lemma_.lower()
        for t in words
        if t.pos_ in ("NOUN", "VERB", "ADJ", "ADV") and len(t.text) > 2
    ]
    top_words = Counter(content_words).most_common(50)

    return {
        "anzahl_wörter": tokens_count,
        "wortlänge": {
            "mittelwert": round(statistics.mean(word_lens), 1),
            "median": round(statistics.median(word_lens), 1),
        },
        "type_token_ratio": ttr,
        "hapax_legomena_prozent": hapax_ratio,
        "füllwörter": {
            "pro_1000_wörter": filler_per_1000,
            "gefunden": dict(sorted(filler_found.items(), key=lambda x: -x[1])),
        },
        "modalverben": {
            "pro_1000_wörter": modal_per_1000,
            "verteilung": modal_found,
        },
        "top_50_signalwörter": [{"wort": w, "anzahl": c} for w, c in top_words],
    }


def analyze_pronouns(doc, words=None) -> dict:
    if words is None:
        words = content_words(doc)
    if not words:
        return {}

    total = len(words)
    groups: Counter = Counter()

    for t in words:
        if t.text in FORMAL_SIE:
            prev = doc[t.i - 1] if t.i > 0 else None
            if prev and prev.text not in (".", "!", "?", ":", ";", "\n"):
                groups["Sie_formal"] += 1
                continue
        lower = t.lower_
        if lower in PRONOUN_MAP:
            groups[PRONOUN_MAP[lower]] += 1

    pct = {k: round(v / total * 1000, 1) for k, v in groups.items()}

    wir = groups.get("wir", 0)
    ich = groups.get("ich", 0)
    wir_ich = round(wir / ich, 2) if ich else (float("inf") if wir else 0)

    return {
        "pro_1000_wörter": pct,
        "wir_ich_verhältnis": wir_ich,
        "gesamt_pronomen_anteil": round(sum(groups.values()) / total * 100, 1),
    }


def analyze_paragraphs(text: str) -> dict:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        return {}

    char_lens = [len(p) for p in paragraphs]
    sent_counts = [
        max(len(re.findall(r"[.!?…]+(?:\s|$)", p)), 1) for p in paragraphs
    ]

    return {
        "anzahl_absätze": len(paragraphs),
        "sätze_pro_absatz": {
            "mittelwert": round(statistics.mean(sent_counts), 1),
            "median": round(statistics.median(sent_counts), 1),
        },
        "zeichen_pro_absatz": {
            "mittelwert": round(statistics.mean(char_lens), 1),
            "median": round(statistics.median(char_lens), 1),
        },
    }


def analyze_punctuation(text: str) -> dict:
    wc = len(text.split())
    if wc == 0:
        return {}
    f = 1000 / wc
    return {
        "pro_1000_wörter": {
            "gedankenstriche": round((text.count("–") + text.count("—")) * f, 1),
            "doppelpunkte": round(text.count(":") * f, 1),
            "semikolons": round(text.count(";") * f, 1),
            "ellipsen": round((text.count("...") + text.count("…")) * f, 1),
            "ausrufezeichen": round(text.count("!") * f, 1),
            "fragezeichen": round(text.count("?") * f, 1),
            "klammern": round(text.count("(") * f, 1),
            "anführungszeichen": round(
                (text.count("„") + text.count("“") + text.count("»") + text.count('"')) / 2 * f, 1
            ),
            "kommas": round(text.count(",") * f, 1),
        }
    }


def analyze_readability(text: str) -> dict:
    words = text.split()
    total_words = len(words)
    if total_words == 0:
        return {}

    sentences = max(len(re.findall(r"[.!?]+", text)), 1)
    total_syllables = sum(count_syllables_de(w) for w in words)
    avg_syllables = total_syllables / total_words
    long_words = sum(1 for w in words if count_syllables_de(w) >= 3)

    try:
        flesch = textstat.flesch_reading_ease(text)
    except Exception:
        flesch = None

    return {
        "flesch_reading_ease": round(flesch, 1) if flesch is not None else None,
        "durchschnitt_silben_pro_wort": round(avg_syllables, 2),
        "lange_wörter_prozent": round(long_words / total_words * 100, 1),
        "durchschnitt_wörter_pro_satz": round(total_words / sentences, 1),
    }


def analyze_grammar(doc, words=None) -> dict:
    if words is None:
        words = content_words(doc)
    if not words:
        return {}

    total = len(words)
    pos_counter = Counter(t.pos_ for t in words)
    pos_pct = {k: round(v / total * 100, 1) for k, v in pos_counter.most_common()}

    passive_count = 0
    for i, t in enumerate(words):
        if t.lemma_.lower() == "werden" and t.pos_ == "AUX":
            window = words[max(0, i - 5):min(len(words), i + 6)]
            for w in window:
                if w.tag_ and "PP" in w.tag_:
                    passive_count += 1
                    break

    clauses = max(len(list(doc.sents)), 1)
    passive_pct = round(passive_count / clauses * 100, 1)

    tense_counter: Counter = Counter()
    for t in words:
        if t.pos_ not in ("VERB", "AUX"):
            continue
        morph = t.morph.to_dict()
        tense = morph.get("Tense", "")
        mood = morph.get("Mood", "")
        if tense == "Pres":
            tense_counter["präsens"] += 1
        elif tense == "Past":
            tense_counter["präteritum"] += 1
        if mood == "Sub":
            tense_counter["konjunktiv"] += 1
    total_t = sum(tense_counter.values()) or 1
    tense_pct = {k: round(v / total_t * 100, 1) for k, v in tense_counter.items()}

    noun_count = pos_counter.get("NOUN", 0) + pos_counter.get("PROPN", 0)
    return {
        "pos_verteilung_prozent": pos_pct,
        "aktiv_passiv": {
            "aktiv_prozent": round(100 - passive_pct, 1),
            "passiv_prozent": passive_pct,
        },
        "tempus_verteilung": tense_pct,
        "adjektiv_dichte_prozent": round(pos_counter.get("ADJ", 0) / total * 100, 1),
        "verb_substantiv_ratio": round(
            pos_counter.get("VERB", 0) / noun_count, 2
        ) if noun_count else 0,
    }


def extract_single_text(text: str, doc=None) -> dict:
    if doc is None:
        doc = nlp(text)
    words = content_words(doc)
    return {
        "sätze": analyze_sentences(doc),
        "wörter": analyze_words(doc, words),
        "pronomen": analyze_pronouns(doc, words),
        "absätze": analyze_paragraphs(text),
        "interpunktion": analyze_punctuation(text),
        "lesbarkeit": analyze_readability(text),
        "grammatik": analyze_grammar(doc, words),
    }


def _agg_numeric(all_metrics: list[dict], path_parts: list[str]):
    values = []
    for m in all_metrics:
        obj = m
        for p in path_parts:
            if isinstance(obj, dict) and p in obj:
                obj = obj[p]
            else:
                obj = None
                break
        if isinstance(obj, (int, float)) and obj != float("inf"):
            values.append(obj)
    if values:
        return {
            "mittelwert": round(statistics.mean(values), 2),
            "bereich": [round(min(values), 2), round(max(values), 2)],
        }
    return None


def _agg_pct(all_metrics: list[dict], path_parts: list[str]) -> dict:
    keys: set[str] = set()
    for m in all_metrics:
        obj = m
        for p in path_parts:
            if isinstance(obj, dict) and p in obj:
                obj = obj[p]
            else:
                obj = None
                break
        if isinstance(obj, dict):
            keys.update(obj.keys())
    result = {}
    for key in keys:
        vals = []
        for m in all_metrics:
            obj = m
            for p in path_parts:
                if isinstance(obj, dict) and p in obj:
                    obj = obj[p]
                else:
                    obj = None
                    break
            if isinstance(obj, dict):
                vals.append(obj.get(key, 0))
        result[key] = round(statistics.mean(vals), 1) if vals else 0
    return result


def aggregate_metrics(all_metrics: list[dict]) -> dict:
    if not all_metrics:
        return {}
    if len(all_metrics) == 1:
        return all_metrics[0]

    agg: dict = {}

    agg["sätze"] = {
        "wörter_pro_satz": _agg_numeric(all_metrics, ["sätze", "wörter_pro_satz", "mittelwert"]),
        "stakkato_quote": _agg_numeric(all_metrics, ["sätze", "stakkato_quote"]),
        "satztypen_prozent": _agg_pct(all_metrics, ["sätze", "satztypen_prozent"]),
        "satzanfänge_prozent": _agg_pct(all_metrics, ["sätze", "satzanfänge_prozent"]),
    }

    combined_words: Counter = Counter()
    for m in all_metrics:
        for entry in m.get("wörter", {}).get("top_50_signalwörter", []):
            combined_words[entry["wort"]] += entry["anzahl"]
    agg["wörter"] = {
        "type_token_ratio": _agg_numeric(all_metrics, ["wörter", "type_token_ratio"]),
        "hapax_legomena_prozent": _agg_numeric(all_metrics, ["wörter", "hapax_legomena_prozent"]),
        "füllwörter_pro_1000": _agg_numeric(all_metrics, ["wörter", "füllwörter", "pro_1000_wörter"]),
        "modalverben_pro_1000": _agg_numeric(all_metrics, ["wörter", "modalverben", "pro_1000_wörter"]),
        "wortlänge": _agg_numeric(all_metrics, ["wörter", "wortlänge", "mittelwert"]),
        "top_50_signalwörter": [
            {"wort": w, "anzahl": c} for w, c in combined_words.most_common(50)
        ],
    }

    agg["pronomen"] = {
        "pro_1000_wörter": _agg_pct(all_metrics, ["pronomen", "pro_1000_wörter"]),
        "wir_ich_verhältnis": _agg_numeric(all_metrics, ["pronomen", "wir_ich_verhältnis"]),
    }

    agg["interpunktion"] = {
        "pro_1000_wörter": _agg_pct(all_metrics, ["interpunktion", "pro_1000_wörter"]),
    }

    agg["lesbarkeit"] = {
        "flesch_reading_ease": _agg_numeric(all_metrics, ["lesbarkeit", "flesch_reading_ease"]),
        "silben_pro_wort": _agg_numeric(all_metrics, ["lesbarkeit", "durchschnitt_silben_pro_wort"]),
        "lange_wörter_prozent": _agg_numeric(all_metrics, ["lesbarkeit", "lange_wörter_prozent"]),
    }

    agg["grammatik"] = {
        "aktiv_prozent": _agg_numeric(all_metrics, ["grammatik", "aktiv_passiv", "aktiv_prozent"]),
        "passiv_prozent": _agg_numeric(all_metrics, ["grammatik", "aktiv_passiv", "passiv_prozent"]),
        "adjektiv_dichte": _agg_numeric(all_metrics, ["grammatik", "adjektiv_dichte_prozent"]),
        "pos_verteilung_prozent": _agg_pct(all_metrics, ["grammatik", "pos_verteilung_prozent"]),
    }

    agg["absätze"] = {
        "sätze_pro_absatz": _agg_numeric(all_metrics, ["absätze", "sätze_pro_absatz", "mittelwert"]),
        "zeichen_pro_absatz": _agg_numeric(all_metrics, ["absätze", "zeichen_pro_absatz", "mittelwert"]),
    }

    return agg


def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_metrics.py <input_dir> <output_path>")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_dir.is_dir():
        print(f"Fehler: {input_dir} ist kein Verzeichnis")
        sys.exit(1)

    texts = load_texts(input_dir)
    if not texts:
        print(f"Fehler: Keine .txt oder .md Dateien in {input_dir}")
        sys.exit(1)

    print(f"Analysiere {len(texts)} Texte aus {input_dir}...")

    per_text = []
    for t in texts:
        print(f"  → {Path(t['path']).name} ({len(t['text'].split())} Wörter)")
        metrics = extract_single_text(t["text"])
        metrics["_datei"] = Path(t["path"]).name
        per_text.append(metrics)

    aggregated = aggregate_metrics(per_text)

    result = {
        "meta": {
            "anzahl_texte": len(texts),
            "dateien": [Path(t["path"]).name for t in texts],
            "gesamt_wörter": sum(len(t["text"].split()) for t in texts),
        },
        "aggregiert": aggregated,
        "pro_text": per_text,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nMetriken gespeichert: {output_path}")


if __name__ == "__main__":
    main()
