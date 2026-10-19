"""Lecture 03 : outils mis à la disposition de l’agent.

Les docstrings et annotations de types des fonctions deviennent les descriptions d’outils fournies au modèle.
Modifier une description change la décision d’utiliser un outil et le choix de ses arguments.
"""

import json
from functools import cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MAX_RESULTS = 3


@cache
def load_glossary() -> list[dict]:
    with open(DATA_DIR / "glossary.json", encoding="utf-8") as f:
        return json.load(f)["terms"]


def _normalize(text: str) -> str:
    return text.casefold().replace(" ", "").replace("　", "")


def _names(entry: dict) -> list[str]:
    return [_normalize(entry["term"]), _normalize(entry["id"])] + [
        _normalize(a) for a in entry["aliases"]
    ]


def search_glossary(query: str) -> str:
    """Rechercher un terme dans le glossaire du cours et renvoyer sa définition et la séance associée.

    Utiliser cet outil avant de répondre sur un terme d’ingénierie de l’IA ou une expression propre
    au cours AIE2026. Mettre un seul terme à rechercher dans query (exemple : "LoRA").
    """
    q = _normalize(query)
    if not q:
        return "La recherche est vide. Indiquez un terme à rechercher."
    glossary = load_glossary()

    exact = [e for e in glossary if q in _names(e)]
    # Exclure les noms trop courts pour éviter qu’un alias comme « r » corresponde à tout
    partial = [
        e for e in glossary
        if e not in exact and any(q in n or (len(n) >= 3 and n in q) for n in _names(e))
    ]
    in_definition = [
        e for e in glossary
        if e not in exact and e not in partial and q in _normalize(e["definition"])
    ]
    hits = (exact + partial + in_definition)[:MAX_RESULTS]

    if not hits:
        return f"Le terme « {query} » est introuvable dans le glossaire."
    return json.dumps(
        [
            {
                "term": e["term"],
                "lecture": e["lecture"],
                "definition": e["definition"],
                "related": e["related"],
            }
            for e in hits
        ],
        ensure_ascii=False,
    )


def get_lecture_summary(lecture: int) -> str:
    """Renvoyer les points essentiels de la séance indiquée (entier à partir de 1).

    Utiliser pour une question sur le contenu ou les liens entre séances, par exemple « Qu’apprend-on dans Lecture 03 ? ».
    """
    path = DATA_DIR / "lectures" / f"{lecture:02d}.md"
    if not path.exists():
        available = sorted(p.stem for p in (DATA_DIR / "lectures").glob("*.md"))
        return f"Le résumé de Lecture {lecture:02d} n’est pas encore disponible. Séances disponibles : {', '.join(available)}"
    return path.read_text(encoding="utf-8")
