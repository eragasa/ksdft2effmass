"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``ContractValue``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``ContractValue`` is the sole primary SUT. Tests exercise its documented public contract
with synthetic routing inputs; exact constructor, language, enum, ordering, and
error-taxonomy rules provide the independent oracles. Collaborators only construct
inputs or expose public outcomes.

VVUQ and scientific exclusions
------------------------------
Passing means the named software contracts hold; failure may identify an implementation,
fixture, oracle transcription, environment, or public-contract inconsistency. This
module excludes numerical verification, scientific validation, uncertainty
quantification, physical correctness, persistence and engine-adapter behavior, and
cross-language conformance."""

import math

import pytest

from ksdft2effmass.workflows.cpn import ContractValue, ContractValueKind

pytestmark = pytest.mark.software_verification

SUT = ContractValue


def test_constructor__contract__string_sequence_rejects_empty_entries() -> None:
    """Evidence ID
    -----------
    SV-CPN-035

    Requirement
    -----------
    preserve nonempty identities in string-sequence values.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: preserve nonempty identities in
    string-sequence values. Requirement: every string-sequence member is a nonempty
    identity. Method: construct the public tagged value with one empty member. Oracle:
    the explicit nonempty identity invariant. Acceptance: ``ValueError`` mentions
    nonempty. Failure means malformed routing identity state became representable.
    Limitation: no serialization or scientific payload is exercised.

    Oracle
    ------
    The documented public rule that the SUT must preserve nonempty identities in
    string-sequence values is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
    with pytest.raises(ValueError, match="nonempty"):
        ContractValue(ContractValueKind.STRING_SEQUENCE, ("",))


def test_constructor__contract__closed_tags_admit_exact_public_values() -> None:
    """Evidence ID
    -----------
    SV-CPN-058

    Requirement
    -----------
    admit each resolved exact tagged-value representation.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: admit each resolved exact tagged-value
    representation. Requirement: tags select exact Python representations. Method:
    construct all resolved tags through the public API. Oracle: exact stored type and
    value. Acceptance preserves the supplied values. Failure breaks the closed union.
    Numeric boundary and canonicalization details are covered separately.

    Oracle
    ------
    The documented public rule that the SUT must admit each resolved exact tagged-value
    representation is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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


def test_constructor__contract__mismatched_tags_raise_type_error() -> None:
    """Evidence ID
    -----------
    SV-CPN-059

    Requirement
    -----------
    reject every resolved tag/value type mismatch.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: reject every resolved tag/value type
    mismatch. Public construction is the method; exact built-in type identity is the
    oracle. Acceptance requires ``TypeError`` for mismatches including
    Boolean-as-integer, Boolean-as-REAL, and list-as-sequence. Failure permits implicit
    coercion. Numeric range behavior is covered separately.

    Oracle
    ------
    The documented public rule that the SUT must reject every resolved tag/value type
    mismatch is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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


def test_constructor__contract__real_values_must_be_finite() -> None:
    """Evidence ID
    -----------
    SV-CPN-060

    Requirement
    -----------
    reject nonfinite exact-float contract values.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: reject nonfinite exact-float contract
    values. IEEE nonfinite built-in floats are synthetic boundary inputs;
    ``math.isfinite`` semantics are the oracle. Acceptance requires ``ValueError`` for
    both infinity signs and NaN. Failure admits nonstandard JSON states. No tolerance,
    scientific number, or integer-valued REAL branch is tested.

    Oracle
    ------
    The documented public rule that the SUT must reject nonfinite exact-float contract
    values is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
    for value in (float("inf"), float("-inf"), float("nan")):
        with pytest.raises(ValueError, match="finite"):
            SUT(ContractValueKind.REAL, value)


def test_constructor__contract__real_is_finite_binary64_with_documented_rounding() -> (
    None
):
    """Evidence ID
    -----------
    SV-CPN-080

    Requirement
    -----------
    binary64 REAL admission, canonicalization, rounding, and conversion-overflow
    rejection.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: canonicalize admitted REAL inputs to finite
    binary64. Requirement: REAL admits exact built-in ``int`` and ``float`` except
    Boolean, stores a built-in finite float, and reports integer-to-binary64 overflow as
    ``ValueError``. Method: exercise exact-type, large-integer rounding, finite
    boundary, and overflow cases through the public constructor. Oracle: Python's
    specified binary64 conversion, including ``2**53 + 1`` rounding to ``2**53``.
    Acceptance requires exact stored types/values and documented exceptions. Failure
    means the Python tagged value disagrees with the approved f64 wire contract. These
    synthetic controls are not scientific numerical evidence.

    Oracle
    ------
    The documented public rule that the SUT must binary64 REAL admission,
    canonicalization, rounding, and conversion-overflow rejection is the contract
    oracle; fixed synthetic values, Python exact type/value semantics, and the public
    error taxonomy provide independently inspectable expected outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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


def test_constructor__contract__integer_is_exact_signed_i64() -> None:
    """Evidence ID
    -----------
    SV-CPN-081

    Requirement
    -----------
    exact signed-i64 INTEGER boundaries and Boolean rejection.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: enforce the exact built-in signed-i64
    INTEGER domain. Requirement: INTEGER admits exact built-in integers except Boolean
    only from ``-2**63`` through ``2**63 - 1``. Method: construct both endpoints,
    interior zero, both adjacent out-of-range values, and Boolean. Oracle: fixed signed
    64-bit bounds, independent of Python's arbitrary-precision range. Acceptance
    preserves admitted integers exactly, rejects Boolean with ``TypeError``, and rejects
    either overflow side with ``ValueError``. Failure breaks Python/Rust/ schema
    portability; no arithmetic or scientific quantity is evaluated.

    Oracle
    ------
    The documented public rule that the SUT must exact signed-i64 INTEGER boundaries and
    Boolean rejection is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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
