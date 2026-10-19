"""Configuration commune à tout le cours.

Lire la clé API et le nom du modèle dans les variables d’environnement, sans les inscrire dans le code.
"""

import os

# Modèle par défaut. Définir AIE_MODEL pour en choisir un autre.
#   Exemple : export AIE_MODEL=gemini-3.5-flash
DEFAULT_MODEL = "gemini-3.5-flash-lite"
MODEL = os.getenv("AIE_MODEL", DEFAULT_MODEL)


def api_error_message(status: int, detail: str = "") -> str:
    """Convertir un code HTTP en explication en français pour les apprenants (partagé par ask.py et agent.py)."""
    if status == 429:
        return "Limite de débit atteinte. Attendez environ une minute, puis réessayez."
    if status == 503:
        return "Le modèle est saturé (503). Attendez un peu, puis réessayez."
    if status in (400, 401, 403, 404):
        return f"Problème de clé API ou de nom de modèle ({status}) : {detail}"
    return f"Erreur API ({status}) : {detail}"


def get_api_key() -> str:
    """Renvoyer GEMINI_API_KEY. Si elle manque, afficher les instructions et quitter."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise SystemExit(
            "La variable d’environnement GEMINI_API_KEY est introuvable.\n"
            "1. Dans GitHub, ajoutez GEMINI_API_KEY sous Settings → Codespaces → Secrets,\n"
            "   puis sélectionnez votre fork parmi les dépôts autorisés.\n"
            "2. Si vous l’avez ajoutée après le démarrage de Codespaces, redémarrez Codespaces.\n"
            "   (En bas à gauche : « Codespaces » → « Stop Current Codespace » → rouvrir)"
        )
    return key
