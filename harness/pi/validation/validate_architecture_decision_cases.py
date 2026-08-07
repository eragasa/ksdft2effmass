#!/usr/bin/env -S python/.venv/bin/python
"""Validate controlled phase-six-only architecture-decision skill cases."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PI = Path(__file__).resolve().parents[1]
CASES = PI / "fixtures/architecture-decision/cases.json"
SKILL = PI / "skills/develop-architecture-decision/SKILL.md"
REFERENCE = (
    PI
    / "skills/develop-architecture-decision/references/architecture-decision-conventions.md"
)
APPLICABLE = {
    "live-agent-registry-versus-historical-ownership",
    "persistence-backend",
    "irreversible-serialization-migration",
}
NON_APPLICABLE = {
    "test-rename": "unsuitable",
    "contract-regex": "deterministic",
    "formatting": "unsuitable",
    "resolved-checkpoint": "deterministic",
    "fixed-contract-class": "deterministic",
}
HEADINGS = (
    "Problem",
    "Observed current behavior",
    "Decision requirements",
    "Option A",
    "Option B",
    "Option C",
    "Three-option comparison",
    "Recommendation",
    "Deferred questions",
    "Human decision required",
)
FACETS = (
    "Conceptual model",
    "Authority",
    "Ownership/dependency",
    "Runtime/dispatch",
    "Migration",
    "Reversibility",
    "Failures",
    "Complexity",
    "Maintenance",
    "Context-window consequences",
    "Future compatibility",
    "Advantage",
    "Risk",
)


def fail(message: str, issues: list[str]) -> None:
    issues.append(message)


def main() -> int:
    issues: list[str] = []
    try:
        payload: Any = json.loads(CASES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        payload = {}
        fail(f"cases unreadable: {error}", issues)
    if payload.get("fixture_scope") != "harness-phase-six-only-controlled-fixture":
        fail("fixtures must be explicitly limited to harness phase six", issues)
    cases = payload.get("cases", [])
    if not isinstance(cases, list) or len(cases) != 8:
        fail("exactly eight controlled cases are required", issues)
        cases = []
    by_id = {item.get("case_id"): item for item in cases if isinstance(item, dict)}
    if set(by_id) != APPLICABLE | set(NON_APPLICABLE):
        fail("controlled case identities differ from the closed expected set", issues)
    for case_id in APPLICABLE:
        case = by_id.get(case_id, {})
        if case.get("applicable") is not True:
            fail(f"{case_id}: must be applicable", issues)
            continue
        options = case.get("options")
        if not isinstance(options, dict) or list(options) != ["A", "B", "C"]:
            fail(f"{case_id}: options must be exactly ordered A/B/C", issues)
        elif len(set(options.values())) != 3 or any(
            not isinstance(x, str) or not x for x in options.values()
        ):
            fail(
                f"{case_id}: architectures must be three distinct nonempty summaries",
                issues,
            )
        if case.get("recommendation") not in {"A", "B", "C"}:
            fail(f"{case_id}: exactly one A/B/C recommendation is required", issues)
        if case.get("expected_checkpoint_choices") != ["A", "B", "C", "D"]:
            fail(f"{case_id}: checkpoint choices must be A/B/C/D", issues)
        separation = case.get("claim_separation")
        required_claims = {
            "observed_facts",
            "architectural_inferences",
            "human_choices",
            "implementation_details",
            "deferred_questions",
        }
        if (
            not isinstance(separation, dict)
            or set(separation) != required_claims
            or any(
                not isinstance(separation[field], list)
                or not separation[field]
                or any(
                    not isinstance(value, str) or not value
                    for value in separation[field]
                )
                for field in required_claims
            )
        ):
            fail(
                f"{case_id}: facts/inferences/choices/implementation/deferred separation is incomplete",
                issues,
            )
        if case.get("stop_before_implementation") is not True:
            fail(f"{case_id}: must stop before implementation", issues)
        if case.get("unsupported_vvuq_claims") != []:
            fail(f"{case_id}: unsupported VVUQ claims must be empty", issues)
        if not isinstance(case.get("decision_document_path"), str) or not case.get(
            "decision_document_path"
        ):
            fail(f"{case_id}: checkpoint must identify the decision document", issues)
        if "classification" in case:
            fail(
                f"{case_id}: applicable cases must not carry stop classification",
                issues,
            )
    for case_id, classification in NON_APPLICABLE.items():
        case = by_id.get(case_id, {})
        if (
            case.get("applicable") is not False
            or case.get("classification") != classification
        ):
            fail(f"{case_id}: incorrect non-applicable classification", issues)
        if (
            "options" in case
            or "recommendation" in case
            or "expected_checkpoint_choices" in case
        ):
            fail(
                f"{case_id}: non-applicable case must stop without options/checkpoint",
                issues,
            )
        if not case.get("missing_or_controlling_information"):
            fail(f"{case_id}: missing controlling information", issues)
        if case.get("stop_before_implementation") is not True:
            fail(
                f"{case_id}: non-applicable case must stop before implementation",
                issues,
            )
        if case.get("unsupported_vvuq_claims") != []:
            fail(f"{case_id}: unsupported VVUQ claims must be empty", issues)

    skill = SKILL.read_text(encoding="utf-8") if SKILL.is_file() else ""
    reference = REFERENCE.read_text(encoding="utf-8") if REFERENCE.is_file() else ""
    for heading in HEADINGS:
        if reference.count(f"## {heading}") != 1:
            fail(f"reference heading must occur exactly once: {heading}", issues)
    for facet in FACETS:
        if reference.count(f"**{facet}**") != 1:
            fail(f"reference facet must occur exactly once: {facet}", issues)
    for phrase in (
        "Observed fact",
        "Inference",
        "Human choice",
        "Implementation consequence",
        "Deferred question",
        "deterministic",
        "underspecified",
        "unsuitable",
        "D — Reconsider or defer",
        "stop before",
        "new attempt identity",
        "observationally idempotent",
    ):
        if phrase not in skill + reference:
            fail(f"required convention absent: {phrase}", issues)
    prohibited_claims = (
        "VVUQ established",
        "scientifically validated",
        "human accepted",
    )
    for phrase in prohibited_claims:
        if phrase.lower() in (skill + reference).lower():
            fail(f"prohibited success claim present: {phrase}", issues)

    result = {
        "schema_version": 1,
        "fixture_scope": "harness-phase-six-only-controlled-fixture",
        "applicable_cases": len(APPLICABLE),
        "non_applicable_cases": len(NON_APPLICABLE),
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
