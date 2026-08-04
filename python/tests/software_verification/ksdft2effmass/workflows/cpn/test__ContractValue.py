"""Software verification for ``ContractValue`` as the sole primary SUT.

The synthetic case checks the closed tagged value invariant through the public
constructor. Exact rejection is the oracle. Passing verifies only this Python
DataObject boundary; numerical verification, scientific validation, uncertainty
quantification, persistence, and Rust conformance are excluded.
"""

import math

import pytest

from ksdft2effmass.workflows.cpn import ContractValue, ContractValueKind

pytestmark = pytest.mark.software_verification

SUT = ContractValue


def test_cpn_sv_p1_035_string_sequence_rejects_empty_entries() -> None:
    """SV-CPN-035: preserve nonempty identities in string-sequence values.

    Requirement: every string-sequence member is a nonempty identity. Method:
    construct the public tagged value with one empty member. Oracle: the explicit
    nonempty identity invariant. Acceptance: ``ValueError`` mentions nonempty.
    Failure means malformed routing identity state became representable.
    Limitation: no serialization or scientific payload is exercised.
    """
    with pytest.raises(ValueError, match="nonempty"):
        ContractValue(ContractValueKind.STRING_SEQUENCE, ("",))


def test_cpn_sv_p1_058_closed_tags_admit_exact_public_values() -> None:
    """SV-CPN-058: admit each resolved exact tagged-value representation.

    Requirement: tags select exact Python representations. Method: construct all
    resolved tags through the public API. Oracle: exact stored type and value.
    Acceptance preserves the supplied values. Failure breaks the closed union.
    Numeric boundary and canonicalization details are covered separately.
    """
    cases = (
        (ContractValueKind.NONE, None),
        (ContractValueKind.BOOLEAN, True),
        (ContractValueKind.INTEGER, 3),
        (ContractValueKind.REAL, 3.5),
        (ContractValueKind.STRING, "value"),
        (ContractValueKind.STRING_SEQUENCE, ("a", "a")),
    )
    assert tuple(SUT(kind, value).value for kind, value in cases) == tuple(
        value for _, value in cases
    )


def test_cpn_sv_p1_059_mismatched_tags_raise_type_error() -> None:
    """SV-CPN-059: reject every resolved tag/value type mismatch.

    Public construction is the method; exact built-in type identity is the oracle.
    Acceptance requires ``TypeError`` for mismatches including Boolean-as-integer,
    Boolean-as-REAL, and list-as-sequence. Failure permits implicit coercion.
    Numeric range behavior is covered separately.
    """
    with pytest.raises(TypeError, match="kind"):
        SUT("integer", 3)  # type: ignore[arg-type]
    cases = (
        (ContractValueKind.NONE, False),
        (ContractValueKind.BOOLEAN, 1),
        (ContractValueKind.INTEGER, True),
        (ContractValueKind.REAL, True),
        (ContractValueKind.REAL, "1.5"),
        (ContractValueKind.STRING, 1),
        (ContractValueKind.STRING_SEQUENCE, ["a"]),
        (ContractValueKind.STRING_SEQUENCE, (1,)),
    )
    for kind, value in cases:
        with pytest.raises(TypeError):
            SUT(kind, value)  # type: ignore[arg-type]


def test_cpn_sv_p1_060_real_values_must_be_finite() -> None:
    """SV-CPN-060: reject nonfinite exact-float contract values.

    IEEE nonfinite built-in floats are synthetic boundary inputs; ``math.isfinite``
    semantics are the oracle. Acceptance requires ``ValueError`` for both infinity
    signs and NaN. Failure admits nonstandard JSON states. No tolerance,
    scientific number, or integer-valued REAL branch is tested.
    """
    for value in (float("inf"), float("-inf"), float("nan")):
        with pytest.raises(ValueError, match="finite"):
            SUT(ContractValueKind.REAL, value)


def test_cpn_sv_p1_080_real_is_finite_binary64_with_documented_rounding() -> None:
    """SV-CPN-080: canonicalize admitted REAL inputs to finite binary64.

    Requirement: REAL admits exact built-in ``int`` and ``float`` except Boolean,
    stores a built-in finite float, and reports integer-to-binary64 overflow as
    ``ValueError``. Method: exercise exact-type, large-integer rounding, finite
    boundary, and overflow cases through the public constructor. Oracle: Python's
    specified binary64 conversion, including ``2**53 + 1`` rounding to ``2**53``.
    Acceptance requires exact stored types/values and documented exceptions.
    Failure means the Python tagged value disagrees with the approved f64 wire
    contract. These synthetic controls are not scientific numerical evidence.
    """
    exact_inputs = (0, -7, 0.0, -2.5, float.fromhex("0x1.fffffffffffffp+1023"))
    for value in exact_inputs:
        stored = SUT(ContractValueKind.REAL, value).value
        assert type(stored) is float
        assert math.isfinite(stored)
        assert stored == float(value)

    rounded = SUT(ContractValueKind.REAL, 2**53 + 1).value
    assert type(rounded) is float
    assert rounded == float(2**53)
    assert rounded != 2**53 + 1

    with pytest.raises(TypeError, match="real kind"):
        SUT(ContractValueKind.REAL, True)
    with pytest.raises(ValueError, match="overflows binary64"):
        SUT(ContractValueKind.REAL, 10**400)


def test_cpn_sv_p1_081_integer_is_exact_signed_i64() -> None:
    """SV-CPN-081: enforce the exact built-in signed-i64 INTEGER domain.

    Requirement: INTEGER admits exact built-in integers except Boolean only from
    ``-2**63`` through ``2**63 - 1``. Method: construct both endpoints, interior
    zero, both adjacent out-of-range values, and Boolean. Oracle: fixed signed
    64-bit bounds, independent of Python's arbitrary-precision range. Acceptance
    preserves admitted integers exactly, rejects Boolean with ``TypeError``, and
    rejects either overflow side with ``ValueError``. Failure breaks Python/Rust/
    schema portability; no arithmetic or scientific quantity is evaluated.
    """
    minimum = -(2**63)
    maximum = 2**63 - 1
    for value in (minimum, 0, maximum):
        stored = SUT(ContractValueKind.INTEGER, value).value
        assert type(stored) is int
        assert stored == value
    with pytest.raises(TypeError, match="integer kind"):
        SUT(ContractValueKind.INTEGER, False)
    for value in (minimum - 1, maximum + 1):
        with pytest.raises(ValueError, match="signed i64"):
            SUT(ContractValueKind.INTEGER, value)
