"""Tests des outils (sans LLM ni clé API)."""

import json

from app import tools


def test_glossary_ids_are_unique_and_related_links_exist():
    terms = tools.load_glossary()
    ids = [t["id"] for t in terms]
    assert len(ids) == len(set(ids))
    for t in terms:
        for r in t["related"]:
            assert r in ids, f"Identifiant inexistant dans related de {t['id']} : {r}"


def test_search_finds_term_by_name_and_alias():
    for query in ["LoRA", "lora", "Low-Rank Adaptation"]:
        hits = json.loads(tools.search_glossary(query))
        assert hits[0]["term"] == "LoRA", query


def test_search_finds_course_specific_term():
    hits = json.loads(tools.search_glossary("lecNN-start"))
    assert hits[0]["term"] == "tag lecNN-start"


def test_search_limits_number_of_results():
    hits = json.loads(tools.search_glossary("agent"))
    assert 1 <= len(hits) <= tools.MAX_RESULTS


def test_search_reports_not_found():
    assert "introuvable" in tools.search_glossary("terme-inexistant-xyz")


def test_lecture_summary():
    assert "agent" in tools.get_lecture_summary(3)
    assert "pas encore disponible" in tools.get_lecture_summary(99)


def test_default_question_of_lecture1_is_answerable_from_glossary():
    """L’agent de Lecture 03 peut répondre à la question par défaut de Lecture 01 (app.ask) grâce au glossaire."""
    from app.ask import DEFAULT_QUESTION

    assert "3 niveaux" in DEFAULT_QUESTION
    hits = json.loads(tools.search_glossary("3 niveaux"))
    assert hits[0]["term"] == "3 niveaux de devoirs"
