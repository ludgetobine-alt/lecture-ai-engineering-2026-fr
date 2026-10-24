# Lecture 01 : réponses


## Devoir

- Niveau choisi : bases
- Travail réalisé :
  J'ai posé trois fois la même question, « Qu'est-ce que LoRA ? », en changeant de modèle
  avec la variable d'environnement AIE_MODEL. Je n'ai pas modifié la température.
  Modèles utilisés : gemini-3.5-flash-lite (modèle par défaut), gemini-3.8-flash
  et gemini-3.1-flash-lite.
- Résultats :

| Modèle | Tokens (entrée / sortie) | Structure de la réponse |
  |---|---|---|
  | gemini-3.5-flash-lite | 10 / 715 | Définition, problème, fonctionnement, avantages, résumé. Analogie du livre de 1000 pages avec des post-it |
  | gemini-3.8-flash | 10 / 898 | Les mêmes parties, plus une section sur les usages (images, LLM). Analogie du livre de cuisine avec des post-it |
  | gemini-3.1-flash-lite | 10 / 761 | Définition, problème, solution, avantages, analogie, résumé. Analogie de l'encyclopédie de 10 000 pages avec des post-it |

Les trois modèles donnent la même définition correcte  et proposent tous une analogie avec des post-it.
Le plus gros modèle, gemini-3.8-flash, donne la réponse la plus longue (898 tokens) , prend beaoucoup plus de temps pour répondre et la plus complète, avec une section supplémentaire sur les usages.
gemini-3.8-flash et gemini-3.1-flash-lite précisent qu'on n'entraîne que 0,1 % à 1 % des paramètres,
  ce que ne fait pas gemini-3.5-flash-lite. Les chiffres cités diffèrent d'un modèle à l'autre :
  taille d'un modèle complet « plusieurs dizaines ou centaines de Go » (3.5-flash-lite),
  « 15 à 40 Go » (3.8-flash), « plusieurs Go » (3.1-flash-lite).
  gemini-3.5-flash-lite affirme aussi qu'un fine-tuning complet coûte « des millions de dollars »,
  ce que les autres ne disent pas.
  Je n'ai rencontré ni erreur  ni limite de débit.

  - Observations et questions :
  Sur une question générale, les trois modèles répondent correctement et de façon très similaire :
  le changement de modèle modifie surtout la longueur, la structure et les détails chiffrés, pas le fond. Les chiffres précis semblent peu fiables, puisqu'ils varient selon le modèle
  (exemple : taille des modèles).
 
