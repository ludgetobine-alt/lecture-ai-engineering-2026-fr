"""Lecture 02, devoir d’approfondissement : créer des paires Q&R pour SFT (JSONL) à partir du glossaire.

Utilisation :
    uv run python scripts/make_sft_dataset.py > glossary_sft.jsonl

Téléverser le fichier dans Colab et l’utiliser comme données d’entraînement LoRA.
Essayer de varier les formulations, de créer des questions avec les alias ou de réserver des données de validation.
"""

import json
import sys
from pathlib import Path

GLOSSARY = Path(__file__).resolve().parent.parent / "data" / "glossary.json"
TEMPLATES = ["Qu’est-ce que « {term} » ?", "Expliquez brièvement {term}."]


def main() -> None:
    terms = json.loads(GLOSSARY.read_text(encoding="utf-8"))["terms"]
    for t in terms:
        for template in TEMPLATES:
            record = {
                "messages": [
                    {"role": "user", "content": template.format(term=t["term"])},
                    {"role": "assistant", "content": t["definition"]},
                ]
            }
            sys.stdout.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
