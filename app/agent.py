"""Lecture 03 : agent d’aide à l’apprentissage avec Pydantic AI.

Utilisation :
    uv run python -m app.agent "Qu’est-ce que le tag lecNN-start utilisé dans le cours AIE2026 ?"
    uv run python -m app.agent --trace "Quelle différence entre LoRA et QLoRA ?"  # Afficher les appels d’outils
    uv run python -m app.agent --mcp --trace "Qu’est-ce que LoRA ?"  # Lecture 05 : outils reçus d’un serveur MCP
    uv run python -m app.agent --mcp --list-tools  # Lecture 05 : outils visibles par le modèle (sans clé API)

Agent = modèle + boucle + outils.
Le modèle appelle les fonctions de tools.py comme outils, puis construit sa réponse à partir des résultats.
Dans Lecture 05, les mêmes outils sont reçus via le serveur MCP (app/mcp_server.py).
"""

import argparse
import inspect
import json
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelHTTPError
from fastmcp import Client
from pydantic_ai.mcp import MCPToolset, StdioTransport
from pydantic_ai.messages import ToolCallPart, ToolReturnPart
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.test import TestModel
from pydantic_ai.providers.google import GoogleProvider

from app import tools
from app.config import MODEL, api_error_message, get_api_key

INSTRUCTIONS = """\
Vous êtes l’agent d’aide à l’apprentissage du cours AI Engineering Pilot Course (AIE2026).
- Avant de répondre sur un terme ou une information propre au cours, consultez toujours le glossaire avec search_glossary.
- Pour une question sur le contenu d’une séance, utilisez get_lecture_summary.
- Si une information est absente du glossaire, indiquez-le au lieu d’affirmer une supposition.
- Terminez la réponse en indiquant les séances concernées (Lecture NN).
- Guidez l’apprenant avec des pistes de réflexion sans donner directement la réponse au devoir.
"""

# Le modèle est fourni à l’exécution pour pouvoir le remplacer par TestModel, sans appel API dans les tests
agent = Agent(instructions=INSTRUCTIONS)
agent.tool_plain(tools.search_glossary)
agent.tool_plain(tools.get_lecture_summary)

# TODO(Lecture 03 exercice) : créer make_quiz dans tools.py et l’enregistrer ici

# Lecture 05 : configuration des serveurs MCP, au même format "mcpServers" que Claude Desktop et Cursor
MCP_CONFIG = Path(__file__).resolve().parent / "mcp_servers.json"


def load_mcp_servers(config_path: Path = MCP_CONFIG) -> list[MCPToolset]:
    """Lire la configuration (format mcpServers) et créer une connexion MCPToolset par serveur.

    - Avec "command", utiliser stdio : démarrer le serveur comme sous-processus
    - Avec "url", utiliser Streamable HTTP : se connecter à un serveur déjà démarré
    Ajouter le préfixe « nom_du_serveur_ » aux outils (ex. glossary_search_glossary)
    pour distinguer les outils de même nom sur plusieurs serveurs.

    Pydantic AI propose aussi load_mcp_toolsets() pour cela. La construction manuelle évite
    les nombreux avertissements du mode de détection automatique ("auto") lors de connexions
    à des serveurs utilisant un ancien SDK, comme fetch. Le mode "legacy" permet de se connecter
    aux anciens comme aux nouveaux serveurs sans ces avertissements.
    """
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))["mcpServers"]
    toolsets = []
    for name, spec in config.items():
        if "url" in spec:
            transport = spec["url"]
        else:
            transport = StdioTransport(spec["command"], spec.get("args", []), env=spec.get("env"))
        toolsets.append(MCPToolset(Client(transport, mode="legacy")).prefixed(name))
    return toolsets


def build_mcp_agent(config_path: Path = MCP_CONFIG) -> Agent:
    """Lecture 05 : agent utilisant les outils exposés par MCP, au lieu de fonctions enregistrées directement. Mêmes INSTRUCTIONS."""
    return Agent(instructions=INSTRUCTIONS, toolsets=load_mcp_servers(config_path))


def build_model() -> GoogleModel:
    return GoogleModel(MODEL, provider=GoogleProvider(api_key=get_api_key()))


def print_tools(target: Agent) -> None:
    """Afficher les outils visibles par le modèle (noms, descriptions, arguments), sans appeler de LLM.

    Transmettre les outils à TestModel (faux modèle de test), puis les relire depuis ce modèle.
    Pour le modèle, les outils MCP et les fonctions outils de Lecture 03 ont la même forme.
    """
    model = TestModel(call_tools=[])
    target.run_sync("Liste des outils", model=model)
    tools_seen = model.last_model_request_parameters.function_tools
    print(f"Outils visibles par le modèle : {len(tools_seen)}")
    for tool in tools_seen:
        print(f"\n[{tool.name}]")
        print("  " + inspect.cleandoc(tool.description or "").replace("\n", "\n  "))
        params = tool.parameters_json_schema.get("properties", {})
        print(f"  Arguments : {json.dumps(params, ensure_ascii=False)}")


def print_trace(result) -> None:
    """Afficher quels outils sont appelés, avec quels arguments et quels résultats."""
    print("\n--- trace ---")
    for message in result.all_messages():
        for part in message.parts:
            if isinstance(part, ToolCallPart):
                print(f"[tool call]   {part.tool_name}({part.args})")
            elif isinstance(part, ToolReturnPart):
                print(f"[tool return] {part.tool_name} -> {str(part.content)[:120]}…")
    print(f"[usage] {result.usage}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Poser une question à l’agent d’aide à l’apprentissage")
    parser.add_argument("question", nargs="?")
    parser.add_argument("--trace", action="store_true", help="Afficher les appels d’outils")
    parser.add_argument("--mcp", action="store_true", help="Lecture 05 : recevoir les outils des serveurs MCP (app/mcp_servers.json)")
    parser.add_argument("--list-tools", action="store_true", help="Afficher les outils visibles par le modèle et quitter (sans clé API)")
    args = parser.parse_args()

    target = build_mcp_agent() if args.mcp else agent
    if args.list_tools:
        print_tools(target)
        return
    if not args.question:
        parser.error("Veuillez fournir une question")

    print(f"[model] {MODEL}")
    if args.mcp:
        print("[tools] Serveurs MCP (app/mcp_servers.json)")
    try:
        result = target.run_sync(args.question, model=build_model())
    except ModelHTTPError as e:
        print(api_error_message(e.status_code, str(e.body)[:200]))
        raise SystemExit(1)
    print(result.output)
    if args.trace:
        print_trace(result)


if __name__ == "__main__":
    main()
