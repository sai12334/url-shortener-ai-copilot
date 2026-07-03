"""
Unit tests for the copilot engine's requirement-analysis logic.
"""
from app.services.copilot_engine import run_copilot


def test_url_shortener_requirement_uses_specific_analysis():
    result = run_copilot(
        "Build a scalable URL shortener service with APIs, persistence, and analytics."
    )
    fr_ids = {fr.id for fr in result.requirement_analysis.functional_requirements}
    assert "FR-1" in fr_ids
    assert len(result.requirement_analysis.functional_requirements) >= 5
    assert len(result.task_decomposition) >= 5
    assert "urls" in result.engineering_artifacts.database_schema
    assert any("POST /shorten" in c for c in result.engineering_artifacts.api_contracts)


def test_url_shortener_detects_ambiguous_scalable_term():
    result = run_copilot("Build a scalable URL shortener with analytics.")
    ambiguity_text = " ".join(result.requirement_analysis.ambiguities).lower()
    assert "scalable" in ambiguity_text or "analytics" in ambiguity_text


def test_generic_requirement_falls_back_to_heuristic_analysis():
    result = run_copilot("Add a dark mode toggle to the user settings page.")
    assert len(result.requirement_analysis.functional_requirements) >= 1
    assert result.final_summary.generated_artifacts == ["Requirement analysis only"]


def test_task_dependencies_reference_valid_task_ids():
    result = run_copilot(
        "Build a scalable URL shortener service with APIs, persistence, and analytics."
    )
    task_ids = {t.id for t in result.task_decomposition}
    for task in result.task_decomposition:
        for dep in task.depends_on:
            assert dep in task_ids


def test_risk_analysis_includes_ai_related_category():
    result = run_copilot(
        "Build a scalable URL shortener service with APIs, persistence, and analytics."
    )
    categories = {r.category for r in result.risk_analysis.risks}
    assert "AI-related" in categories
