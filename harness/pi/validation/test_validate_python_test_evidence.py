"""Focused regression tests for the static Python test-evidence validator."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / "harness/pi/validation/validate_python_test_evidence.py"
CASES_PATH = (
    ROOT
    / "harness/pi/fixtures/python-test-evidence/named-parameter-inventories/cases.json"
)
CASES = json.loads(CASES_PATH.read_text(encoding="utf-8"))


def consumer_source(
    index: int,
    parameter_names: str,
    decorator_values: str,
    decorator_suffix: str = "",
) -> str:
    """Return one complete controlled maintained-evidence consumer function."""
    words = ("one", "two", "three")
    name = words[index]
    arguments = parameter_names.split(",")
    acceptance = " and ".join(f"{argument} is not None" for argument in arguments)
    decorator = (
        f'@pytest.mark.parametrize("{parameter_names}", '
        f"{decorator_values}{decorator_suffix})"
    )
    return f'''{decorator}
def test_artifact__consumer_{name}__accepts_named_cases({parameter_names}):
    """Evidence ID
    SV-FIX-{900 + index:03d}
    Requirement
    The controlled consumer represents one explicit static parameter family.
    Method
    Supply the declared cases through one pytest parametrize decorator.
    Oracle
    The controlled fixture source fixes the expected static case inventory.
    Acceptance
    Every supplied argument is non-null in the illustrative test body.
    Interpretation
    Validator findings identify controlled static-grammar acceptance or rejection.
    Limitations
    This fixture is not executed and makes no scientific, numerical, or UQ claim.
    """
    assert {acceptance}
'''


def fixture_source(case: dict[str, Any]) -> str:
    """Assemble one controlled module without evaluating its parameter expressions."""
    imports = case.get("imports", "")
    assignment = case.get("assignment", "")
    consumers = "\n".join(
        consumer_source(
            index,
            case.get("parameter_names", "case"),
            case["decorator_values"],
            case.get("decorator_suffix", ""),
        )
        for index in range(case.get("consumer_count", 1))
    )
    assignment_after = case.get("assignment_after", "")
    return f'''r"""Software verification of named parameter inventory validator fixture.

Facet and represented meaning
This controlled artifact represents one static parameter-inventory syntax.
Intrinsic and cross-object scope
The module AST and validator finding set are the complete controlled relation.
VVUQ and scientific exclusions
Passing concerns static software verification only, not scientific validation or UQ.
"""

import pytest
{imports}

{assignment}

{consumers}
{assignment_after}
'''


def run_controlled_validator(tmp_path: Path, case: dict[str, Any]) -> dict[str, Any]:
    """Run the validator against one disposable controlled source module."""
    module = tmp_path / "test__named_parameter_inventory.py"
    module.write_text(fixture_source(case), encoding="utf-8")
    ownership = tmp_path / "ownership.json"
    ownership.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "modules": [
                    {
                        "path": module.as_posix(),
                        "mode": "artifact_owned",
                        "evidence_class": "software_verification",
                        "artifact": "named parameter inventory validator fixture",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--ownership",
            str(ownership),
            str(module),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    result = json.loads(completed.stdout)
    assert completed.returncode == (0 if result["status"] == "PASS" else 1)
    return result


@pytest.mark.parametrize(
    "case",
    [pytest.param(case, id=case["case_id"]) for case in CASES["valid"]],
)
def test_named_inventory_valid_cases(case: dict[str, Any], tmp_path: Path) -> None:
    """Accept every controlled inline or named static parameter inventory."""
    result = run_controlled_validator(tmp_path, case)
    assert result["status"] == "PASS", result["findings"]
    assert result["counts"]["test_functions"] == case.get("consumer_count", 1)
    assert result["counts"]["parameterized_functions"] == case.get("consumer_count", 1)
    assert (
        result["counts"]["static_collected_parameter_cases"]
        == case["expected_static_cases"]
    )


@pytest.mark.parametrize(
    "case",
    [pytest.param(case, id=case["case_id"]) for case in CASES["invalid"]],
)
def test_named_inventory_invalid_cases(case: dict[str, Any], tmp_path: Path) -> None:
    """Reject each controlled unresolved, dynamic, malformed, or mutated inventory."""
    result = run_controlled_validator(tmp_path, case)
    assert result["status"] == "FAIL"
    matching = [
        finding
        for finding in result["findings"]
        if finding["code"] == case["expected_code"]
        and case["message_contains"] in finding["message"]
    ]
    assert matching, result["findings"]


def test_intended_a09_pattern_reuses_one_inventory_three_times(
    tmp_path: Path,
) -> None:
    """Accept the intended three-consumer A09 pattern with six static cases."""
    case = next(
        case
        for case in CASES["valid"]
        if case["case_id"] == "intended_a09_three_consumer_pattern"
    )
    source = fixture_source(case)
    assert source.count("VALID_FIXTURE_CASES =") == 1
    result = run_controlled_validator(tmp_path, case)
    assert result["status"] == "PASS", result["findings"]
    assert result["counts"]["test_functions"] == 3
    assert result["counts"]["parameterized_functions"] == 3
    assert result["counts"]["static_collected_parameter_cases"] == 6


@pytest.mark.parametrize(
    ("relative_module", "relative_ownership", "expected_status"),
    [
        pytest.param(
            "valid/test__ExampleRecord.py",
            "valid/ownership.json",
            "PASS",
            id="class_owned_valid",
        ),
        pytest.param(
            "valid-artifact/test__json_schema.py",
            "valid-artifact/ownership.json",
            "PASS",
            id="artifact_owned_valid",
        ),
        pytest.param(
            "invalid/test__bad-artifact.py",
            "invalid/ownership.json",
            "FAIL",
            id="structurally_invalid",
        ),
    ],
)
def test_existing_structural_fixture_regressions(
    relative_module: str,
    relative_ownership: str,
    expected_status: str,
) -> None:
    """Preserve existing ownership, heading, helper, ID, and filename behavior."""
    base = Path("harness/pi/fixtures/python-test-evidence")
    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--ownership",
            str(base / relative_ownership),
            str(base / relative_module),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    result = json.loads(completed.stdout)
    assert result["status"] == expected_status


def run_semantic_rule_source(
    tmp_path: Path,
    body: str,
    *,
    test_name: str = "test_artifact__member__has_expected_outcome",
    requirement: str = "The concrete artifact has one declared behavior.",
    prelude: str = "",
    case_id: str = "SV-FIX-990",
    mode: str = "artifact_owned",
) -> dict[str, Any]:
    """Run one controlled semantic-rule source through the structural validator."""
    if mode == "class_owned":
        module = tmp_path / "test__ExampleEnum.py"
        opening = "Software verification of ``ExampleEnum``."
        owner = {
            "path": module.as_posix(),
            "mode": mode,
            "evidence_class": "software_verification",
            "sut": "ExampleEnum",
        }
        imports = "from enum import Enum as ExampleEnum\n\nSUT = ExampleEnum"
    else:
        module = tmp_path / "test__semantic_rule.py"
        opening = "Software verification of semantic rule fixture."
        owner = {
            "path": module.as_posix(),
            "mode": mode,
            "evidence_class": "software_verification",
            "artifact": "semantic rule fixture",
        }
        imports = ""
    source = f'''r"""{opening}

Facet and represented meaning
This controlled artifact represents one deterministic validator rule.
Intrinsic and cross-object scope
The source AST and validator finding set are the complete controlled relation.
VVUQ and scientific exclusions
Passing concerns structural software verification only, not semantic correctness.
"""

import pytest
{imports}
{prelude}


def {test_name}():
    """Evidence ID
    {case_id}
    Requirement
    {requirement}
    Method
    Execute one controlled public syntax pattern without production dependencies.
    Oracle
    The fixture declares the exact expected deterministic finding class.
    Acceptance
    The validator emits or omits that finding exactly as declared.
    Interpretation
    The result verifies only the controlled structural rule implementation.
    Limitations
    This fixture proves no oracle independence, scientific validity, or UQ.
    """
    {body}
'''
    module.write_text(source, encoding="utf-8")
    ownership = tmp_path / "ownership-semantic.json"
    ownership.write_text(
        json.dumps({"schema_version": 1, "modules": [owner]}), encoding="utf-8"
    )
    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--ownership",
            str(ownership),
            str(module),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return json.loads(completed.stdout)


@pytest.mark.parametrize(
    ("expected_code", "arguments"),
    [
        pytest.param(
            "TE.VAGUE_TEST_FACET",
            {
                "test_name": "test_protocol__behavior__returns_member",
                "body": "assert iter(()) is not None",
            },
            id="vague_protocol_facet",
        ),
        pytest.param(
            "TE.MIXED_ENUM_LOOKUP",
            {"mode": "class_owned", "body": "assert SUT(1) is not SUT['name']"},
            id="mixed_enum_call_and_getitem",
        ),
        pytest.param(
            "TE.CIRCULAR_ENUM_ORACLE",
            {
                "mode": "class_owned",
                "body": (
                    "name = 'name'\n"
                    "    expected = SUT.__members__[name]\n"
                    "    assert SUT[name] is expected"
                ),
            },
            id="circular_enum_member_oracle",
        ),
        pytest.param(
            "TE.MIXED_INVALID_PARTITION",
            {
                "prelude": (
                    "CASES = (pytest.param('unknown', id='unknown_value'), "
                    "pytest.param(1, id='integer_wrong_type'))"
                ),
                "test_name": "test_artifact__value__rejects_invalid_cases",
                "body": "assert value is not None",
            },
            id="unknown_and_wrong_type_partition",
        ),
        pytest.param(
            "TE.PROSE_PUNCTUATION",
            {
                "requirement": "The concrete artifact has one declared behavior..",
                "body": "assert True",
            },
            id="doubled_terminal_punctuation",
        ),
        pytest.param(
            "TE.PLACEHOLDER_PROSE",
            {
                "requirement": "TODO replace this incomplete requirement.",
                "body": "assert True",
            },
            id="placeholder_prose",
        ),
        pytest.param(
            "TE.EQUALITY_FIELD_INVENTORY",
            {
                "requirement": "Equality compares the complete represented state.",
                "body": "assert 1 == 1",
            },
            id="missing_equality_inventory",
        ),
        pytest.param(
            "TE.EQUALITY_FIELD_INVENTORY",
            {
                "test_name": "test_method__eq__compares_public_values",
                "requirement": (
                    "Exact equality distinguishes every declared public field."
                ),
                "body": "assert 1 == 1",
            },
            id="missing_synonymous_equality_inventory",
        ),
        pytest.param(
            "TE.FROZEN_FIELD_INVENTORY",
            {"requirement": "All fields are frozen.", "body": "assert True"},
            id="missing_frozen_inventory",
        ),
        pytest.param(
            "TE.FROZEN_FIELD_INVENTORY",
            {
                "test_name": "test_field__immutable_state__is_enforced",
                "requirement": (
                    "Every declared public field rejects post-construction assignment."
                ),
                "body": "assert True",
            },
            id="missing_synonymous_frozen_inventory",
        ),
    ],
)
def test_deterministic_semantic_rules_report_controlled_defects(
    expected_code: str, arguments: dict[str, str], tmp_path: Path
) -> None:
    """Reject each controlled mixed-surface, oracle, prose, or completeness defect."""
    if expected_code == "TE.MIXED_INVALID_PARTITION":
        arguments = dict(arguments)
        arguments["test_name"] = "test_artifact__value__rejects_invalid_cases"
        result = run_semantic_rule_source(tmp_path, **arguments)
        # Insert the controlled decorator separately to keep the builder small.
        module = tmp_path / "test__semantic_rule.py"
        source = module.read_text(encoding="utf-8")
        source = source.replace(
            "def test_artifact__value__rejects_invalid_cases():",
            '@pytest.mark.parametrize("value", CASES)\n'
            "def test_artifact__value__rejects_invalid_cases(value):",
        )
        module.write_text(source, encoding="utf-8")
        ownership = tmp_path / "ownership-semantic.json"
        completed = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--ownership",
                str(ownership),
                str(module),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        result = json.loads(completed.stdout)
    else:
        result = run_semantic_rule_source(tmp_path, **arguments)
    assert expected_code in {finding["code"] for finding in result["findings"]}


@pytest.mark.parametrize(
    ("absent_code", "arguments"),
    [
        pytest.param(
            "TE.VAGUE_TEST_FACET",
            {
                "test_name": "test_protocol__iter__returns_declared_members",
                "body": "assert list(iter(())) == []",
            },
            id="genuine_protocol_surface",
        ),
        pytest.param(
            "TE.MIXED_ENUM_LOOKUP",
            {"mode": "class_owned", "body": "assert SUT(1) is not None"},
            id="enum_value_lookup_only",
        ),
        pytest.param(
            "TE.CIRCULAR_ENUM_ORACLE",
            {"mode": "class_owned", "body": "assert SUT['name'] is SUT.name"},
            id="literal_enum_oracle",
        ),
        pytest.param(
            "TE.PROSE_PUNCTUATION",
            {
                "requirement": "The concrete artifact preserves an ellipsis...",
                "body": "assert True",
            },
            id="ellipsis_is_not_doubled_punctuation",
        ),
        pytest.param(
            "TE.EQUALITY_FIELD_INVENTORY",
            {
                "prelude": "EQUALITY_FIELDS = ('identifier', 'value')",
                "requirement": "Equality compares the complete represented state.",
                "body": "assert 1 == 1",
            },
            id="declared_equality_inventory",
        ),
        pytest.param(
            "TE.FROZEN_FIELD_INVENTORY",
            {
                "prelude": "FROZEN_FIELDS = ('identifier', 'value')",
                "requirement": "All fields are frozen.",
                "body": "assert True",
            },
            id="declared_frozen_inventory",
        ),
        pytest.param(
            "TE.EQUALITY_FIELD_INVENTORY",
            {
                "test_name": "test_field__validation__rejects_invalid_values",
                "requirement": "Every field-specific invalid partition is rejected.",
                "body": "assert True",
            },
            id="unrelated_every_field_validation_claim",
        ),
        pytest.param(
            "TE.FROZEN_FIELD_INVENTORY",
            {
                "test_name": "test_field__tuple__preserves_immutable_input",
                "requirement": "The immutable input tuple preserves all labels.",
                "body": "assert True",
            },
            id="unrelated_immutable_input_claim",
        ),
    ],
)
def test_deterministic_semantic_rules_preserve_false_positive_guards(
    absent_code: str, arguments: dict[str, str], tmp_path: Path
) -> None:
    """Accept each controlled genuine surface, oracle, or inventory guard."""
    result = run_semantic_rule_source(tmp_path, **arguments)
    assert absent_code not in {finding["code"] for finding in result["findings"]}


@pytest.mark.parametrize(
    ("suppression", "should_report"),
    [
        pytest.param("# ruff: noqa: E501\n", True, id="blanket_file_suppression"),
        pytest.param("", False, id="ordinary_formatting"),
    ],
)
def test_blanket_e501_suppression_rule_has_a_false_positive_guard(
    suppression: str, should_report: bool, tmp_path: Path
) -> None:
    """Reject only file-level blanket E501 suppression in controlled evidence."""
    run_semantic_rule_source(tmp_path, body="assert True")
    module = tmp_path / "test__semantic_rule.py"
    module.write_text(
        suppression + module.read_text(encoding="utf-8"), encoding="utf-8"
    )
    ownership = tmp_path / "ownership-semantic.json"
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR), "--ownership", str(ownership), str(module)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    result = json.loads(completed.stdout)
    codes = {finding["code"] for finding in result["findings"]}
    assert ("TE.BLANKET_SUPPRESSION" in codes) is should_report


def test_mixed_invalid_partition_rule_accepts_one_semantic_partition(
    tmp_path: Path,
) -> None:
    """Accept an explicit parameter family containing only unknown string values."""
    run_semantic_rule_source(
        tmp_path,
        prelude=(
            "CASES = (pytest.param('unknown', id='unknown_value'), "
            "pytest.param('other', id='unsupported_value'))"
        ),
        test_name="test_artifact__value__rejects_unknown_values",
        body="assert value",
    )
    module = tmp_path / "test__semantic_rule.py"
    module.write_text(
        module.read_text(encoding="utf-8").replace(
            "def test_artifact__value__rejects_unknown_values():",
            '@pytest.mark.parametrize("value", CASES)\n'
            "def test_artifact__value__rejects_unknown_values(value):",
        ),
        encoding="utf-8",
    )
    ownership = tmp_path / "ownership-semantic.json"
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR), "--ownership", str(ownership), str(module)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    result = json.loads(completed.stdout)
    assert "TE.MIXED_INVALID_PARTITION" not in {
        finding["code"] for finding in result["findings"]
    }


def test_recurrence_control_fixture_enumerates_every_rule_and_guard() -> None:
    """Keep the durable recurrence fixture synchronized with deterministic codes."""
    fixture = json.loads(
        (
            ROOT
            / "harness/pi/fixtures/python-test-evidence/recurrence-controls/cases.json"
        ).read_text(encoding="utf-8")
    )
    expected = {
        "TE.VAGUE_TEST_FACET",
        "TE.MIXED_ENUM_LOOKUP",
        "TE.CIRCULAR_ENUM_ORACLE",
        "TE.MIXED_INVALID_PARTITION",
        "TE.BLANKET_SUPPRESSION",
        "TE.PROSE_PUNCTUATION",
        "TE.PLACEHOLDER_PROSE",
        "TE.EQUALITY_FIELD_INVENTORY",
        "TE.FROZEN_FIELD_INVENTORY",
    }
    assert {case["expected_code"] for case in fixture["invalid"]} == expected
    assert {case["absent_code"] for case in fixture["valid_guards"]} == expected
