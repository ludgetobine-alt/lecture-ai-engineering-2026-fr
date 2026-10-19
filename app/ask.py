"""Lecture 01 : script posant une seule question à un LLM sans outils.

Utilisation :
    uv run python -m app.ask "Qu’est-ce que LoRA ?"
    uv run python -m app.ask            # Sans question, poser une question propre au cours

Appel direct sans outils ni historique de conversation.
Vérifier que, pour une question propre au cours, le modèle répond qu’il ne sait pas,
ou donne une réponse générale plausible qui ne correspond pas à la réalité du cours.
(L’agent capable de chercher dans le glossaire améliorera cela dans Lecture 03.)
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# Question propre au cours. Bonne réponse dans homework-levels de data/glossary.json
DEFAULT_QUESTION = "Quels sont les 3 niveaux de devoirs du cours AIE2026 ?"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(model=MODEL, contents=question)

    # TODO(Lecture 01 exercice) : à partir de response.usage_metadata,
    #   afficher le nombre de tokens d’entrée et de sortie (vous pouvez demander à Copilot)

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="Poser une question à un LLM sans outils")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[Question] {args.question}\n")
    try:
        print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
