# Lecture 03 : exercices et devoir — créer un agent d’aide à l’apprentissage

## Objectifs de la séance

- Vérifier dans votre code qu’un agent se compose d’un « modèle + boucle + outils »
- Savoir lire quels outils sont appelés et avec quels arguments
- Savoir ajouter un outil

## Préparation

Si vous avez terminé le travail des séances précédentes, créez la branche `lec03` depuis `main`.

```bash
git switch main && git switch -c lec03
```

Sinon, créez une branche depuis le code initial de l’exercice dans le dépôt du cours (tag `lec03-start`).

```bash
git remote -v                     # Si upstream manque, l’ajouter avec la ligne suivante
git remote add upstream https://github.com/matsuolab/lecture-ai-engineering-2026.git
git fetch upstream --tags
git switch -c lec03 lec03-start
```

## Exercice (30 minutes)

### 1. Poser à l’agent la même question que dans Lecture 01

```bash
uv run python -m app.agent "Qu’est-ce que le tag lecNN-start utilisé dans le cours AIE2026 ?"
```

Comparez avec la réponse de `app.ask` dans Lecture 01.

### 2. Lire les appels d’outils

```bash
uv run python -m app.agent --trace "Quelle différence entre LoRA et QLoRA ?"
```

Les lignes `[tool call]` indiquent les outils et arguments choisis par le modèle. La valeur `requests` dans `[usage]` indique le nombre d’appels au LLM pour une question.

### 3. Ajouter un outil

Ajoutez `make_quiz` à `app/tools.py`, puis enregistrez-le dans `app/agent.py` à l’emplacement `TODO(Lecture 03 exercice)`.

- Exemple : choisir un terme de la séance indiquée (`lecture: int`) et renvoyer une question « Que signifie ce terme ? » avec sa réponse
- Dans la docstring, expliquez quand et pourquoi utiliser l’outil (le modèle la lit pour décider de l’utiliser)

```bash
uv run python -m app.agent --trace "Pose-moi une question de révision sur Lecture 02"
uv run pytest -q
```

### 4. Remise

Remplissez `lectures/03/answer.md` et ouvrez une PR de `lec03` vers `main` dans votre fork.

## Devoir (un seul niveau suffit)

| Niveau | Travail |
|---|---|
| Bases | Modifiez `INSTRUCTIONS` ou les docstrings des outils. Comparez et notez avec `--trace` les changements dans les appels et les réponses |
| Mise en œuvre | Créez l’outil `save_learning_log` pour enregistrer un journal d’apprentissage dans `learning_log/`. Demandez la confirmation de l’utilisateur avant l’enregistrement (`requires_approval=True` de Pydantic AI). Écrivez aussi un test avec TestModel |
| Approfondissement | Choisissez (a) recréer le même agent avec ADK de Google et comparer le code et l’affichage dans `adk web`, ou (b) exécuter Pi, présenté en cours, dans Codespaces et comparer son prompt système public à `INSTRUCTIONS` de votre agent |

### Procédure pour l’approfondissement (b)

Pi est un agent de programmation capable de lire et d’écrire des fichiers et d’exécuter des commandes. Il ne demande pas de confirmation avant chaque appel d’outil. Essayez-le dans Codespaces, pas sur votre PC.

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
pi
```

- Gemini lit la variable d’environnement `GEMINI_API_KEY` : le secret Codespaces suffit. Dans Pi, tapez `/model` et choisissez un modèle Gemini
- Le nom du paquet npm est `@earendil-works/pi-coding-agent` (les anciens articles utilisent l’ancien nom `@mariozechner/...`)
- Le prompt système de Pi se trouve dans `packages/coding-agent/src/core/system-prompt.ts` du dépôt public https://github.com/earendil-works/pi. Comparez-le à vos `INSTRUCTIONS` et examinez ce qu’il contient ou non
- Documentation officielle : https://github.com/earendil-works/pi/tree/main/packages/coding-agent/docs

## Références

- Pydantic AI : https://ai.pydantic.dev/
- ADK : https://google.github.io/adk-docs/
