"""Shared utilities for the RedenSkill analysis pipeline."""

import re
from pathlib import Path

import spacy

nlp = spacy.load("de_core_news_lg")
nlp.max_length = 2_000_000


def get_nested(d: dict, *keys, default=None):
    obj = d
    for k in keys:
        if isinstance(obj, dict) and k in obj:
            obj = obj[k]
        else:
            return default
    return obj


def num(v):
    if isinstance(v, dict) and "mittelwert" in v:
        return v["mittelwert"]
    if isinstance(v, (int, float)):
        return v
    return None


def pct_change(old, new):
    if old is None or new is None:
        return None
    if old == 0:
        return abs(new) * 100 if new != 0 else 0.0
    return (new - old) / abs(old) * 100


def strip_markdown(text: str) -> str:
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^>\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^---+$", "", text, flags=re.MULTILINE)
    return text.strip()


def load_single_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    clean = strip_markdown(raw) if path.suffix == ".md" else raw
    return clean.strip()


def load_texts(directory: Path) -> list[dict]:
    texts = []
    for ext in ("*.txt", "*.md"):
        for fpath in sorted(directory.glob(ext)):
            clean = load_single_text(fpath)
            if clean:
                texts.append({"path": str(fpath), "text": clean})
    return texts


def content_words(doc) -> list:
    return [t for t in doc if not t.is_punct and not t.is_space]
