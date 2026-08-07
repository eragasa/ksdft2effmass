r"""Software verification of ``PythonTestEvidenceSource``.

Facet and represented meaning
This module verifies exact construction and immutable represented read outcomes.
Intrinsic and cross-object scope
The sole SUT is ``PythonTestEvidenceSource``; Python type and dataclass semantics
and the public constructor contract provide exact oracles.
VVUQ and scientific exclusions
Passing establishes only this software contract, not validator semantics, numerical
verification, scientific validation, UQ, portability, or human acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness.pi import PythonTestEvidenceSource

pytestmark = pytest.mark.software_verification
SUT = PythonTestEvidenceSource


@pytest.mark.parametrize(
    ("arguments", "expected"),
    (
        pytest.param(
            ("module.py", b"pass\n", True, None),
            ("module.py", b"pass\n", True, None),
            id="regular_payload",
        ),
        pytest.param(
            ("module.py", None, True, "read failed"),
            ("module.py", None, True, "read failed"),
            id="regular_read_error",
        ),
        pytest.param(
            ("module.py", None, False, None),
            ("module.py", None, False, None),
            id="nonregular_path",
        ),
    ),
)
def test_constructor__read_outcome__preserves_exact_state(
    arguments: tuple[object, ...], expected: tuple[object, ...]
) -> None:
    """Evidence ID
    SV-TEV-001
    Requirement
    Construction preserves each controlled consistent source-read outcome exactly.
    Method
    Construct the public record for payload, read-error, and nonregular partitions.
    Oracle
    The literal arguments independently fix the four represented field values.
    Acceptance
    The resulting field tuple equals the corresponding literal tuple exactly.
    Interpretation
    Failure identifies constructor or accepted-contract drift.
    Limitations
    Filesystem observation and validator behavior are excluded.
    """
    value = SUT(*arguments)  # type: ignore[arg-type]
    assert (
        value.path,
        value.payload,
        value.is_regular_file,
        value.read_error,
    ) == expected


def test_field__immutable_state__rejects_reassignment() -> None:
    """Evidence ID
    SV-TEV-002
    Requirement
    A constructed source record is operationally immutable.
    Method
    Construct a valid payload outcome and attempt one public field reassignment.
    Oracle
    Frozen dataclass semantics require reassignment to raise FrozenInstanceError.
    Acceptance
    Reassigning ``path`` raises exactly FrozenInstanceError.
    Interpretation
    Failure identifies loss of the public immutable-record boundary.
    Limitations
    Equality, hashing, and deep mutability of external objects are excluded.
    """
    value = SUT("module.py", b"pass\n")
    with pytest.raises(FrozenInstanceError):
        value.path = "other.py"  # type: ignore[misc]


@pytest.mark.parametrize(
    "arguments",
    (
        pytest.param((1, b"pass\n", True, None), id="integer_path_wrong_type"),
        pytest.param(("module.py", "pass", True, None), id="string_payload_wrong_type"),
        pytest.param(
            ("module.py", b"pass\n", 1, None), id="integer_file_flag_wrong_type"
        ),
        pytest.param(("module.py", None, True, 1), id="integer_error_wrong_type"),
    ),
)
def test_constructor__field_types__rejects_wrong_semantic_types(
    arguments: tuple[object, ...],
) -> None:
    """Evidence ID
    SV-TEV-003
    Requirement
    Source fields reject values outside their declared semantic types.
    Method
    Construct with one wrong-type value in each controlled field partition.
    Oracle
    The public constructor contract assigns TypeError to semantic type violations.
    Acceptance
    Every declared partition raises TypeError.
    Interpretation
    Failure identifies type-policy or constructor drift.
    Limitations
    Correct-type invariant violations are covered separately.
    """
    with pytest.raises(TypeError):
        SUT(*arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "arguments",
    (
        pytest.param(("module.py", b"pass\n", True, "error"), id="payload_and_error"),
        pytest.param(("module.py", None, True, None), id="regular_without_outcome"),
        pytest.param(
            ("module.py", b"pass\n", False, None), id="nonregular_with_payload"
        ),
    ),
)
def test_constructor__read_outcome__rejects_contradictory_values(
    arguments: tuple[object, ...],
) -> None:
    """Evidence ID
    SV-TEV-004
    Requirement
    Correctly typed but contradictory read outcomes are invalid.
    Method
    Construct each controlled payload, error, and regularity contradiction.
    Oracle
    The public state table permits exactly one outcome for a regular source and no
    outcome for a nonregular source.
    Acceptance
    Every declared contradiction raises ValueError.
    Interpretation
    Failure identifies invariant enforcement or contract drift.
    Limitations
    The caller's truthfulness about file kind is not established.
    """
    with pytest.raises(ValueError):
        SUT(*arguments)  # type: ignore[arg-type]
