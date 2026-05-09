#!/bin/bash
set -e

echo "=== RedenSkill Setup ==="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Fehler: Python 3 nicht gefunden"
    exit 1
fi

echo "1/3 Installiere Python-Dependencies..."
pip install -r "$(dirname "$0")/requirements.txt"

echo ""
echo "2/3 Lade spaCy Deutsch-Modell (de_core_news_lg)..."
python3 -m spacy download de_core_news_lg

echo ""
echo "3/3 Prüfe Installation..."
python3 -c "
import spacy
import textstat
nlp = spacy.load('de_core_news_lg')
doc = nlp('Das ist ein Test.')
print(f'  spaCy {spacy.__version__}: OK ({len(list(doc.sents))} Satz erkannt)')
print(f'  textstat: OK')
print()
print('Setup erfolgreich! Starte den Skill mit: /project:reden')
"
