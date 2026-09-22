r"""Software verification of ``PythonConformanceResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies immutable validation status, findings, inventories, and counts.

Intrinsic and cross-object scope

The sole SUT is ``PythonConformanceResult``; finding values are input
collaborators and the public result invariants provide exact oracles.

VVUQ and scientific exclusions

Passing establishes result-record software semantics only, not validator completeness,
numerical verification, scientific validation, UQ, portability, or acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from ksdft2effmass.harness.pi.conformance.python import (
    PythonConformanceFinding,
    PythonConformanceResult,
)

pytestmark = pytest.mark.software_verification
SUT = PythonConformanceResult
FINDING = PythonConformanceFinding("TE.EXAMPLE", "module.py", "message")


def make_validation_result(**changes: Any) -> PythonConformanceResult:
    """Evidence ID: Owns no identifier; supports SV-TEV-013 through SV-TEV-016.

    Requirement: Controlled result cases differ only in explicitly overridden public
    fields.

    Method: Merge named overrides into one literal valid constructor argument mapping.

    Oracle: The literal mapping fixes the shared valid baseline used by the supported
    tests.

    Acceptance: Construction receives the baseline with exactly the requested
    replacements.

    Interpretation: Failure identifies test setup drift rather than independent
    production evidence.

    Limitations: This helper owns no result, validator behavior, or scientific claim.
    """
    values: dict[str, Any] = {
        "schema_version": 1,
        "status": "PASS",
        "claim_boundary": ("oracle independence",),
        "paths": ("module.py",),
        "findings": (),
        "artifact_owned_modules": 0,
        "class_owned_modules": 1,
        "evidence_class_modules": (("software_verification", 1),),
        "findings_by_code": (),
        "helper_functions": 0,
        "modules": 1,
        "parameterized_functions": 0,
        "static_collected_parameter_cases": 0,
        "test_functions": 1,
        "unique_evidence_owners": 1,
    }
    values.update(changes)
    return SUT(**values)


def test_constructor__validation_inventory__preserves_exact_value() -> None:
    """Evidence ID: SV-TEV-013

    Requirement: A valid result preserves status, ordered paths, immutable findings, and
    counts.

    Method: Construct the controlled valid baseline through the public result
    constructor.

    Oracle: The literal baseline independently fixes every asserted value and ordering.

    Acceptance: Status is PASS, paths and findings are tuples, and all declared counts
    are exact.

    Interpretation: Failure identifies constructor or represented-state drift.

    Limitations: The action's derivation of these values is excluded.
    """
    value = make_validation_result()
    assert value.status == "PASS"
    assert value.paths == ("module.py",)
    assert value.findings == ()
    assert value.class_owned_modules == 1
    assert value.modules == value.test_functions == value.unique_evidence_owners == 1
    assert value.static_collected_parameter_cases == 0


def test_field__immutable_state__rejects_reassignment() -> None:
    """Evidence ID: SV-TEV-014

    Requirement: A constructed validation result is operationally immutable.

    Method: Construct a valid result and attempt public status reassignment.

    Oracle: Frozen dataclass semantics require reassignment to raise
    FrozenInstanceError.

    Acceptance: Reassignment raises exactly FrozenInstanceError.

    Interpretation: Failure identifies loss of the immutable result boundary.

    Limitations: Collaborator construction and hashing are excluded.
    """
    value = make_validation_result()
    with pytest.raises(FrozenInstanceError):
        value.status = "FAIL"  # type: ignore[misc]


@pytest.mark.parametrize(
    "changes",
    (
        pytest.param({"schema_version": True}, id="boolean_schema_version_wrong_type"),
        pytest.param({"findings": []}, id="list_findings_wrong_type"),
        pytest.param(
            {"findings": (object(),), "status": "FAIL"}, id="foreign_finding_wrong_type"
        ),
        pytest.param({"modules": True}, id="boolean_count_wrong_type"),
        pytest.param(
            {"static_collected_parameter_cases": 1.0},
            id="float_static_count_wrong_type",
        ),
    ),
)
def test_constructor__result_types__rejects_wrong_semantic_types(
    changes: dict[str, object],
) -> None:
    """Evidence ID: SV-TEV-015

    Requirement: Result fields reject values outside their declared semantic types.

    Method: Replace one controlled baseline field with a wrong semantic type.

    Oracle: The public result contract assigns TypeError to semantic type violations.

    Acceptance: Every declared partition raises TypeError.

    Interpretation: Failure identifies result type-policy or constructor drift.

    Limitations: Correct-type relational and range violations are covered separately.
    """
    with pytest.raises(TypeError):
        make_validation_result(**changes)


@pytest.mark.parametrize(
    "changes",
    (
        pytest.param({"schema_version": 2}, id="unsupported_schema_version"),
        pytest.param({"status": "FAIL"}, id="status_without_findings"),
        pytest.param({"findings": (FINDING,)}, id="findings_with_pass_status"),
        pytest.param({"modules": -1}, id="negative_count"),
        pytest.param(
            {"findings_by_code": (("TE.Z", 1), ("TE.A", 1))},
            id="unsorted_finding_counts",
        ),
    ),
)
def test_constructor__result_invariants__rejects_invalid_values(
    changes: dict[str, object],
) -> None:
    """Evidence ID: SV-TEV-016

    Requirement: Correctly typed result values obey version, status, range, and ordering
    invariants.

    Method: Replace one baseline value with each controlled invariant violation.

    Oracle: The public contract fixes version one, status/finding agreement, nonnegative
    counts, and sorted key/count tuples.

    Acceptance: Every declared invalid value raises ValueError.

    Interpretation: Failure identifies invariant enforcement or contract drift.

    Limitations: Completeness of the claim boundary and finding vocabulary is excluded.
    """
    with pytest.raises(ValueError):
        make_validation_result(**changes)
