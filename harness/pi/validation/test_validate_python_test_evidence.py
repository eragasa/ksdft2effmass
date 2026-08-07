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
