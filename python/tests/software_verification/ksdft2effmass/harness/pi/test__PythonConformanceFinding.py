r"""Software verification of ``PythonConformanceFinding``.

Facet and represented meaning

This module verifies one immutable deterministic structural diagnostic value.

Intrinsic and cross-object scope

The sole SUT is ``PythonConformanceFinding``; the public TE namespace, severity,
and one-based line contracts supply independent exact oracles.

VVUQ and scientific exclusions

Passing establishes finding software semantics only, not diagnostic completeness,
scientific validity, numerical verification, UQ, portability, or human acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness.pi.evidence import PythonConformanceFinding

pytestmark = pytest.mark.software_verification
SUT = PythonConformanceFinding


def test_constructor__diagnostic_fields__preserves_exact_value() -> None:
    """Evidence ID: SV-TEV-009

    Requirement: A valid finding preserves its stable code, path, message, severity, and
    line.

    Method: Construct one finding through the direct public import with explicit values.

    Oracle: The literal constructor values independently fix the complete expected
    record.

    Acceptance: The five public fields equal the literal tuple exactly.

    Interpretation: Failure identifies constructor or represented-state drift.

    Limitations: Finding ordering and validator rule selection are excluded.
    """
    value = SUT("TE.EXAMPLE", "module.py", "controlled message", "error", 7)
    assert (value.code, value.path, value.message, value.severity, value.line) == (
        "TE.EXAMPLE",
        "module.py",
        "controlled message",
        "error",
        7,
    )


def test_field__immutable_state__rejects_reassignment() -> None:
    """Evidence ID: SV-TEV-010

    Requirement: A constructed finding is operationally immutable.

    Method: Construct a valid finding and attempt public message reassignment.

    Oracle: Frozen dataclass semantics require reassignment to raise
    FrozenInstanceError.

    Acceptance: Reassignment raises exactly FrozenInstanceError.

    Interpretation: Failure identifies loss of the immutable finding boundary.

    Limitations: Equality, hashing, and validator aggregation are excluded.
    """
    value = SUT("TE.EXAMPLE", "module.py", "message")
    with pytest.raises(FrozenInstanceError):
        value.message = "other"  # type: ignore[misc]


@pytest.mark.parametrize(
    "arguments",
    (
        pytest.param((1, "module.py", "message"), id="integer_code_wrong_type"),
        pytest.param(("TE.X", 1, "message"), id="integer_path_wrong_type"),
        pytest.param(("TE.X", "module.py", 1), id="integer_message_wrong_type"),
        pytest.param(
            ("TE.X", "module.py", "message", 1), id="integer_severity_wrong_type"
        ),
        pytest.param(
            ("TE.X", "module.py", "message", "error", True),
            id="boolean_line_wrong_type",
        ),
    ),
)
def test_constructor__diagnostic_types__rejects_wrong_semantic_types(
    arguments: tuple[object, ...],
) -> None:
    """Evidence ID: SV-TEV-011

    Requirement: Finding fields reject values outside their declared semantic types.

    Method: Supply one wrong semantic type in each controlled field partition.

    Oracle: The public finding contract assigns TypeError to semantic type violations.

    Acceptance: Every declared partition raises TypeError.

    Interpretation: Failure identifies public type-policy or constructor drift.

    Limitations: Correct-type lexical and range violations are covered separately.
    """
    with pytest.raises(TypeError):
        SUT(*arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "arguments",
    (
        pytest.param(("OTHER.X", "module.py", "message"), id="foreign_code_namespace"),
        pytest.param(
            ("TE.X", "module.py", "message", "warning"), id="unsupported_severity"
        ),
        pytest.param(("TE.X", "module.py", "message", "error", 0), id="zero_line"),
    ),
)
def test_constructor__diagnostic_values__rejects_invalid_invariants(
    arguments: tuple[object, ...],
) -> None:
    """Evidence ID: SV-TEV-012

    Requirement: Correctly typed code, severity, and line values obey intrinsic
    invariants.

    Method: Construct foreign-namespace, unsupported-severity, and nonpositive-line
    cases.

    Oracle: The public contract fixes the TE namespace, error severity, and positive
    lines.

    Acceptance: Every declared invalid value raises ValueError.

    Interpretation: Failure identifies lexical, range, or contract drift.

    Limitations: The vocabulary of individual TE codes is not exhaustively validated.
    """
    with pytest.raises(ValueError):
        SUT(*arguments)  # type: ignore[arg-type]
