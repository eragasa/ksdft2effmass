r"""Software verification for the public difference numerical-error-code enum.

System under test
-----------------
``OperatorRecordDifferenceNumericalErrorCode`` is a public closed numerical-
error-code enum that categorizes failures owned by ``OperatorRecordDifferencer``.
Its only approved member is ``NONFINITE_DIFFERENCE``, with stable machine-
readable value ``"nonfinite_difference"``. The member denotes that subtracting
two individually finite, compatible represented matrices produced at least one
nonfinite entry in
``Delta H = H_candidate - H_reference``.

Ownership and scope
-------------------
The enum supplies classification vocabulary only. It does not perform matrix
subtraction or detect nonfinite values. Error production remains owned by
``OperatorRecordDifferencer``; exception construction remains owned by
``OperatorRecordDifferenceNumericalError``. Difference failures are distinct
from residual-analysis failures such as nonfinite metrics, SVD failure, and
metric-order violation.

Evidence class, strategy, and oracle
------------------------------------
This cohesive module provides software-verification evidence ``SV-ORDNEC-001``
through ``SV-ORDNEC-006``. The independently written literal member sequence is
the oracle for exact membership, name, value, and declaration order. Public
``Enum.__members__``, Python 3.14 ``StrEnum`` behavior, public value/name lookup,
and standard Enum exceptions provide the remaining contract oracles. Passing
establishes the closed one-member enum, alias absence, stable string behavior,
lookup round trips, and invalid-lookup taxonomy. Failure may indicate an enum
regression, documentation mismatch, or evidence defect requiring investigation.

Cross-language and VVUQ boundaries
----------------------------------
The stable string code supports future conceptual mapping to a Rust error enum,
but no Rust implementation or conformance is established. These tests verify
classification vocabulary, not whether a particular matrix operation should be
scientifically accepted. They are not numerical verification of subtraction
behavior, scientific validation, or uncertainty quantification. Passing does
not establish subtraction accuracy, physical operator compatibility, residual-
metric correctness, scientific validity, or uncertainty propagation.
"""

import re
from enum import StrEnum

import pytest

from ksdft2effmass.operators import OperatorRecordDifferenceNumericalErrorCode

pytestmark = pytest.mark.software_verification


def test_exact_closed_member_sequence_and_stable_value() -> None:
    """SV-ORDNEC-001: verify the exact closed member sequence and value.

    Evidence ID
        ``SV-ORDNEC-001``.
    Requirement
        Public iteration contains exactly ``NONFINITE_DIFFERENCE`` with value
        ``"nonfinite_difference"`` in its deterministic declaration order.
    Method
        Compare public enum iteration with an independently written literal
        tuple of name/value pairs.
    Oracle
        The approved closed public enum contract is the literal expected tuple.
    Interpretation
        Passing establishes exact member count, name, value, order, and absence
        of any unapproved additional iterable member.
    Limitations
        This does not inspect source location or establish differencer execution,
        subtraction accuracy, scientific validation, uncertainty quantification,
        or Rust conformance.
    """

    expected_members = (
        (
            "NONFINITE_DIFFERENCE",
            "nonfinite_difference",
        ),
    )

    assert (
        tuple(
            (code.name, code.value)
            for code in OperatorRecordDifferenceNumericalErrorCode
        )
        == expected_members
    )


def test_public_member_registry_contains_no_aliases() -> None:
    """SV-ORDNEC-002: verify one declared member and no alias names.

    Evidence ID
        ``SV-ORDNEC-002``.
    Requirement
        The documented public Enum registry contains exactly one declared name,
        mapped to the one iterable member, with no hidden aliases.
    Method
        Compare ``Enum.__members__`` with the exact approved mapping and compare
        declared-member and iterable-member counts.
    Oracle
        The approved alias policy permits only ``NONFINITE_DIFFERENCE`` and no
        aliases or compatibility names.
    Interpretation
        Passing distinguishes one declared member, one iterable member, and zero
        alias names.
    Limitations
        No implementation-private Enum attributes, differencer behavior,
        scientific validation, uncertainty quantification, or Rust conformance
        are tested.
    """

    expected_members = {
        "NONFINITE_DIFFERENCE": (
            OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE
        ),
    }

    assert OperatorRecordDifferenceNumericalErrorCode.__members__ == expected_members
    assert len(OperatorRecordDifferenceNumericalErrorCode.__members__) == 1
    assert len(tuple(OperatorRecordDifferenceNumericalErrorCode)) == 1


def test_python_314_strenum_and_machine_readable_value_behavior() -> None:
    """SV-ORDNEC-003: verify Python 3.14 ``StrEnum`` string behavior.

    Evidence ID
        ``SV-ORDNEC-003``.
    Requirement
        The public enum subclasses ``StrEnum`` and its code is the exact ASCII
        lowercase snake-case machine identifier ``"nonfinite_difference"``.
    Method
        Inspect public inheritance and string equality, call ``str()``, apply an
        explicit full-match rule, and encode the value as ASCII.
    Oracle
        Python 3.14 ``StrEnum`` semantics and the approved stable enum value.
    Interpretation
        Passing establishes ordinary string behavior and the required machine-
        readable lexical form.
    Limitations
        String-valued behavior does not approve JSON, pickle, ``repr()``, or any
        error wire format and establishes no numerical verification, scientific
        validation, uncertainty quantification, or Rust conformance.
    """

    code = OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE

    assert issubclass(OperatorRecordDifferenceNumericalErrorCode, StrEnum)
    assert isinstance(code, str)
    assert code == "nonfinite_difference"
    assert str(code) == "nonfinite_difference"
    assert re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", code.value) is not None
    code.value.encode("ascii")


def test_value_based_lookup_round_trip() -> None:
    """SV-ORDNEC-004: verify construction by machine-readable value.

    Evidence ID
        ``SV-ORDNEC-004``.
    Requirement
        ``EnumClass(value)`` returns the canonical member for both its public
        ``value`` attribute and the approved literal machine code.
    Method
        Perform both public value-based lookup forms and compare by identity.
    Oracle
        Standard Enum value lookup and the approved stable value.
    Interpretation
        Passing establishes deterministic value-based construction round trips.
    Limitations
        No successful coercion from integers, bytes, case variants, or padded
        strings is specified; subtraction behavior, scientific validation,
        uncertainty quantification, and Rust conformance are not tested.
    """

    code = OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE

    assert OperatorRecordDifferenceNumericalErrorCode(code.value) is code
    assert OperatorRecordDifferenceNumericalErrorCode("nonfinite_difference") is code


def test_name_based_lookup_round_trip() -> None:
    """SV-ORDNEC-005: verify subscription by public member name.

    Evidence ID
        ``SV-ORDNEC-005``.
    Requirement
        ``EnumClass[name]`` returns the canonical member for both its public
        ``name`` attribute and the approved literal member name.
    Method
        Perform both public name-based lookup forms and compare by identity.
    Oracle
        Standard Enum name lookup and the approved public member name.
    Interpretation
        Passing establishes deterministic name-based lookup distinct from value-
        based construction.
    Limitations
        The Python member name is not the machine-readable value. No differencer
        execution, scientific validation, uncertainty quantification, or Rust
        conformance is tested.
    """

    code = OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE

    assert OperatorRecordDifferenceNumericalErrorCode[code.name] is code
    assert OperatorRecordDifferenceNumericalErrorCode["NONFINITE_DIFFERENCE"] is code


@pytest.mark.parametrize(
    "lookup_kind",
    [
        pytest.param("invalid-value", id="SV-ORDNEC-006-invalid-value"),
        pytest.param("invalid-name", id="SV-ORDNEC-006-invalid-name"),
    ],
)
def test_invalid_lookup_exception_taxonomy(lookup_kind: str) -> None:
    """SV-ORDNEC-006: verify exact standard Enum lookup exceptions.

    Evidence ID
        ``SV-ORDNEC-006``; parameter IDs distinguish invalid value and name
        lookup without assigning new evidence identifiers.
    Requirement
        An invalid enum value raises ``ValueError`` and an invalid enum name
        raises ``KeyError``.
    Method
        Exercise one representative unknown value through ``EnumClass(value)``
        and one unknown name through ``EnumClass[name]``.
    Oracle
        The standard public Enum lookup taxonomy is ``ValueError`` for values
        and ``KeyError`` for names.
    Interpretation
        Passing establishes the exact exception category for each lookup form.
    Limitations
        Standard-library exception messages are not frozen. No broad exception
        tuple, exception construction, differencer behavior, numerical
        verification, scientific validation, uncertainty quantification, or
        Rust conformance is tested.
    """

    if lookup_kind == "invalid-value":
        with pytest.raises(ValueError):
            OperatorRecordDifferenceNumericalErrorCode("unknown_difference_error")
    else:
        with pytest.raises(KeyError):
            OperatorRecordDifferenceNumericalErrorCode["UNKNOWN_DIFFERENCE_ERROR"]
