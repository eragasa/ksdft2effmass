r"""Software verification of ``ValidatePythonTestEvidence``.

Facet and represented meaning

This module verifies the explicit-byte structural-validation action and result ordering.

Intrinsic and cross-object scope

The sole SUT is ``ValidatePythonTestEvidence``; request records are collaborators and
controlled literal source/JSON inputs provide independent exact rule oracles.

VVUQ and scientific exclusions

Passing establishes controlled software behavior only, not oracle independence, test
cohesion, numerical verification, scientific validation, UQ, or human acceptance.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import (
    PythonTestEvidenceRequest,
    PythonTestEvidenceSource,
    PythonTestEvidenceValidationResult,
    ValidatePythonTestEvidence,
)

pytestmark = pytest.mark.software_verification
SUT = ValidatePythonTestEvidence
PATH = "test__controlled_artifact.py"
VALID_SOURCE = b'''r"""Software verification of controlled artifact.

Facet and represented meaning

This fixture represents one exact public artifact value.

Intrinsic and cross-object scope

The controlled artifact is primary and literal equality supplies the oracle.

VVUQ and scientific exclusions

Passing establishes software structure only, not validation or UQ.
"""


def test_artifact__literal_value__equals_itself():
    """Evidence ID: SV-TEV-FIX-001

    Requirement: The controlled literal retains exact equality.

    Method: Compare one literal with itself.

    Oracle: Python integer equality fixes the result.

    Acceptance: The equality is exactly true.

    Interpretation: Failure identifies controlled fixture drift.

    Limitations: No scientific, numerical, or UQ claim is made.
    """
    assert 1 == 1
'''
VALID_OWNERSHIP = json.dumps(
    {
        "schema_version": 1,
        "modules": [
            {
                "path": PATH,
                "mode": "artifact_owned",
                "evidence_class": "software_verification",
                "artifact": "controlled artifact",
            }
        ],
    },
    separators=(",", ":"),
).encode()


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID: SV-TEV-017

    Requirement: ValidatePythonTestEvidence is a concrete stateless ActionObject.

    Method: Construct two instances and inspect their instance storage boundary.

    Oracle: The accepted placement contract requires no root, filesystem, cache, or
    state.

    Acceptance: Both construct, lack instance dictionaries, and the class slots are
    empty.

    Interpretation: Failure identifies unauthorized retained state or contract drift.

    Limitations: Execute semantics are covered separately.
    """
    first = SUT()
    second = SUT()
    assert type(first) is type(second) is SUT
    assert not hasattr(first, "__dict__")
    assert SUT.__slots__ == ()


def test_method__execute_valid_source__returns_exact_inventory() -> None:
    """Evidence ID: SV-TEV-018

    Requirement: Execute accepts a controlled conforming artifact-owned module and
    reports its
    exact static inventory.

    Method: Supply literal source and ownership bytes directly through the public
    request.

    Oracle: Manual inspection gives one module, one test, one evidence owner, no helpers
    or
    parameter cases, and one artifact-owned software-verification owner.

    Acceptance: The exact status, paths, findings, owner counts, and function counts
    match.

    Interpretation: Failure identifies validator, fixture, or accepted-rule drift.

    Limitations: A structural pass does not establish semantic quality or scientific
    claims.
    """
    request = PythonTestEvidenceRequest(
        (PythonTestEvidenceSource(PATH, VALID_SOURCE),),
        "ownership.json",
        VALID_OWNERSHIP,
    )
    result = SUT().execute(request)
    assert type(result) is PythonTestEvidenceValidationResult
    assert result.status == "PASS"
    assert result.paths == (PATH,)
    assert result.findings == ()
    assert result.artifact_owned_modules == result.modules == result.test_functions == 1
    assert result.class_owned_modules == result.helper_functions == 0
    assert (
        result.parameterized_functions == result.static_collected_parameter_cases == 0
    )
    assert result.unique_evidence_owners == 1


def test_method__execute_invalid_source__retains_multiple_finding_order() -> None:
    """Evidence ID: SV-TEV-019

    Requirement: Execute retains multiple findings in deterministic rule traversal
    order.

    Method: Supply one controlled source with a nonraw opening, missing headings,
    malformed
    test name, and incomplete function documentation.

    Oracle: The documented traversal checks module opening, module documentation, then
    the
    top-level function name and documentation in that order.

    Acceptance: Status is FAIL and the first four codes equal the literal expected
    sequence.

    Interpretation: Failure identifies rule presence, aggregation, or
    deterministic-order drift.

    Limitations: This representative invalid source does not exhaust every validator
    code.
    """
    source = PythonTestEvidenceSource(
        PATH,
        b'"""Software verification of controlled artifact."""\n\n'
        b"def test_bad():\n    pass\n",
    )
    request = PythonTestEvidenceRequest((source,), "ownership.json", VALID_OWNERSHIP)
    result = SUT().execute(request)
    assert result.status == "FAIL"
    assert tuple(item.code for item in result.findings[:4]) == (
        "TE.MODULE_OPENING",
        "TE.MODULE_DOC",
        "TE.TEST_NAME",
        "TE.FUNCTION_DOC",
    )
    assert result.findings_by_code == tuple(sorted(result.findings_by_code))


@pytest.mark.parametrize(
    ("ownership_payload", "migration_payload", "expected_code"),
    (
        pytest.param(b"null", None, "TE.OWNERSHIP_INPUT", id="invalid_ownership_shape"),
        pytest.param(
            VALID_OWNERSHIP, b"null", "TE.MIGRATION_INPUT", id="invalid_migration_shape"
        ),
    ),
)
def test_method__execute_metadata_contract__reports_controlled_invalidity(
    ownership_payload: bytes,
    migration_payload: bytes | None,
    expected_code: str,
) -> None:
    """Evidence ID: SV-TEV-020

    Requirement: Malformed ownership and migration metadata become their stable public
    findings.

    Method: Supply one correct source with a controlled malformed JSON object at each
    layer.

    Oracle: The closed version-one metadata contracts assign distinct exact finding
    codes.

    Acceptance: The result fails and contains the declared code for the selected layer.

    Interpretation: Failure identifies metadata routing, code, or accepted-contract
    drift.

    Limitations: This covers representative shape defects, not every metadata rule.
    """
    request = PythonTestEvidenceRequest(
        (PythonTestEvidenceSource(PATH, VALID_SOURCE),),
        "ownership.json",
        ownership_payload,
        None,
        "migration.json" if migration_payload is not None else None,
        migration_payload,
    )
    result = SUT().execute(request)
    assert result.status == "FAIL"
    assert expected_code in tuple(item.code for item in result.findings)


def test_method__execute_explicit_bytes__is_repeatable_without_filesystem_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: SV-TEV-021

    Requirement: Execute depends only on the explicit request and returns equal repeated
    results.

    Method: Construct one request, make ``Path.read_bytes`` fail if called, and execute
    twice.

    Oracle: The placement contract prohibits hidden filesystem access and immutable
    value
    semantics require equal outputs for identical explicit inputs.

    Acceptance: No injected filesystem failure occurs and the two results are exactly
    equal.

    Interpretation: Failure identifies hidden I/O, retained state, nondeterminism, or
    equality drift.

    Limitations: Other process-global services and performance characteristics are
    excluded.
    """
    request = PythonTestEvidenceRequest(
        (PythonTestEvidenceSource(PATH, VALID_SOURCE),),
        "ownership.json",
        VALID_OWNERSHIP,
    )

    def reject_read_bytes(path: Path) -> bytes:
        raise AssertionError(f"unexpected filesystem read: {path}")

    monkeypatch.setattr(Path, "read_bytes", reject_read_bytes)
    action = SUT()
    assert action.execute(request) == action.execute(request)


def test_method__execute_docstring_format__requires_inline_labels_and_blank_lines() -> (
    None
):
    """Evidence ID: SV-TEV-026

    Requirement: Evidence fields use ``Label: value`` paragraphs separated by blank
    lines.

    Method: Replace the valid fixture with one standalone label and with zero or two
    blank lines between paragraphs.

    Oracle: The accepted maintained-evidence documentation grammar requires inline
    labels and exactly one blank line.

    Acceptance: Each controlled source fails with ``TE.FUNCTION_DOC``.

    Interpretation: Failure indicates that compact or standalone field syntax remains
    accepted.

    Limitations: Module-section spacing and prose quality beyond structure are not
    assessed.
    """
    standalone = VALID_SOURCE.replace(
        b"Evidence ID: SV-TEV-FIX-001", b"Evidence ID\n    SV-TEV-FIX-001", 1
    )
    adjacent = VALID_SOURCE.replace(
        b"SV-TEV-FIX-001\n\n    Requirement:",
        b"SV-TEV-FIX-001\n    Requirement:",
        1,
    )
    excess = VALID_SOURCE.replace(
        b"SV-TEV-FIX-001\n\n    Requirement:",
        b"SV-TEV-FIX-001\n\n\n    Requirement:",
        1,
    )
    standalone_result = SUT().execute(
        PythonTestEvidenceRequest(
            (PythonTestEvidenceSource(PATH, standalone),),
            "ownership.json",
            VALID_OWNERSHIP,
        )
    )
    adjacent_result = SUT().execute(
        PythonTestEvidenceRequest(
            (PythonTestEvidenceSource(PATH, adjacent),),
            "ownership.json",
            VALID_OWNERSHIP,
        )
    )
    assert (
        tuple(item.code for item in standalone_result.findings).count("TE.FUNCTION_DOC")
        == 1
    )
    excess_result = SUT().execute(
        PythonTestEvidenceRequest(
            (PythonTestEvidenceSource(PATH, excess),),
            "ownership.json",
            VALID_OWNERSHIP,
        )
    )
    assert (
        tuple(item.code for item in adjacent_result.findings).count("TE.FUNCTION_DOC")
        == 1
    )
    assert (
        tuple(item.code for item in excess_result.findings).count("TE.FUNCTION_DOC")
        == 1
    )


def test_method__execute_request_type__rejects_foreign_object() -> None:
    """Evidence ID: SV-TEV-022

    Requirement: Execute accepts exactly PythonTestEvidenceRequest values.

    Method: Invoke the public action with a generic foreign object.

    Oracle: The public method contract assigns TypeError to a wrong semantic request
    type.

    Acceptance: The invocation raises TypeError.

    Interpretation: Failure identifies action-boundary type-policy drift.

    Limitations: Correctly typed malformed evidence is represented as findings and
    covered above.
    """
    with pytest.raises(TypeError):
        SUT().execute(object())  # type: ignore[arg-type]
