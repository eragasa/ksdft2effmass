r"""Software verification of ``ContractValue``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public ``ContractValue``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
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
from typing import cast

import pytest

from ksdft2effmass.workflows.cpn import ContractValue, ContractValueKind

pytestmark = pytest.mark.software_verification

SUT = ContractValue


def test_constructor__fields__string_sequence_rejects_empty_entries() -> None:
    """Evidence ID: SV-CPN-035

    Requirement: preserve nonempty identities in string-sequence values.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: preserve nonempty identities in
    string-sequence values. Requirement: every string-sequence member is a nonempty
    identity. Method: construct the public tagged value with one empty member. Oracle:
    the explicit nonempty identity invariant. Acceptance: ``ValueError`` mentions
    nonempty. Failure means malformed routing identity state became representable.
    Limitation: no serialization or scientific payload is exercised.

    Oracle: The documented public rule that the SUT must preserve nonempty identities in
    string-sequence values is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance: Every preserved exact equality, identity, ordering, representation, and
    expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation: Pass supports only this named software contract. Failure may
    indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations: The case excludes unexercised inputs and dependencies, physical
    conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
    with pytest.raises(ValueError, match="nonempty"):
        ContractValue(ContractValueKind.STRING_SEQUENCE, ("",))


def test_constructor__fields__closed_tags_admit_exact_public_values() -> None:
    """Evidence ID: SV-CPN-058

    Requirement: admit each resolved exact tagged-value representation.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: admit each resolved exact tagged-value
    representation. Requirement: tags select exact Python representations. Method:
    construct all resolved tags through the public API. Oracle: exact stored type and
    value. Acceptance preserves the supplied values. Failure breaks the closed union.
    Numeric boundary and canonicalization details are covered separately.

    Oracle: The documented public rule that the SUT must admit each resolved exact
    tagged-value
    representation is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance: Every preserved exact equality, identity, ordering, representation, and
    expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation: Pass supports only this named software contract. Failure may
    indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations: The case excludes unexercised inputs and dependencies, physical
    conclusions,
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


@pytest.mark.parametrize(
    ("kind", "value"),
    (
        pytest.param(ContractValueKind.NONE, False, id="none_with_boolean"),
        pytest.param(ContractValueKind.BOOLEAN, 1, id="boolean_with_integer"),
        pytest.param(ContractValueKind.INTEGER, True, id="integer_with_boolean"),
        pytest.param(ContractValueKind.REAL, True, id="real_with_boolean"),
        pytest.param(ContractValueKind.REAL, "1.5", id="real_with_numeric_string"),
        pytest.param(ContractValueKind.STRING, 1, id="string_with_integer"),
        pytest.param(ContractValueKind.STRING_SEQUENCE, ["a"], id="sequence_with_list"),
        pytest.param(
            ContractValueKind.STRING_SEQUENCE, (1,), id="sequence_with_integer_item"
        ),
    ),
)
def test_constructor__tag_value_types__rejects_mismatched_types(
    kind: ContractValueKind,
    value: object,
) -> None:
    """Evidence ID: SV-CPN-059

    Requirement: reject every resolved tag/value type mismatch.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: reject every resolved tag/value type
    mismatch. Public construction is the method; exact built-in type identity is the
    oracle. Acceptance requires ``TypeError`` for every explicitly identified tag/value
    mismatch, including Boolean-as-integer, Boolean-as-REAL, and list-as-sequence.
    Failure permits implicit coercion. Numeric range behavior is covered separately.

    Oracle: The documented public rule that the SUT must reject every resolved tag/value
    type
    mismatch is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

    Acceptance: Every preserved exact equality, identity, ordering, representation, and
    expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation: Pass supports only this named software contract. Failure may
    indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations: The case excludes unexercised inputs and dependencies, physical
    conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
    with pytest.raises(TypeError):
        SUT(kind, value)  # type: ignore[arg-type]


def test_constructor__fields__real_values_must_be_finite() -> None:
    """Evidence ID: SV-CPN-060

    Requirement: reject nonfinite exact-float contract values.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: reject nonfinite exact-float contract
    values. IEEE nonfinite built-in floats are synthetic boundary inputs;
    ``math.isfinite`` semantics are the oracle. Acceptance requires ``ValueError`` for
    both infinity signs and NaN. Failure admits nonstandard JSON states. No tolerance,
    scientific number, or integer-valued REAL branch is tested.

    Oracle: The documented public rule that the SUT must reject nonfinite exact-float
    contract
    values is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

    Acceptance: Every preserved exact equality, identity, ordering, representation, and
    expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation: Pass supports only this named software contract. Failure may
    indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations: The case excludes unexercised inputs and dependencies, physical
    conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
    with pytest.raises(ValueError, match="finite"):
        SUT(ContractValueKind.REAL, float("inf"))
    with pytest.raises(ValueError, match="finite"):
        SUT(ContractValueKind.REAL, float("-inf"))
    with pytest.raises(ValueError, match="finite"):
        SUT(ContractValueKind.REAL, float("nan"))


def test_constructor__real_is__preserves_valid_state() -> None:
    """Evidence ID: SV-CPN-080

    Requirement: ``ContractValue`` preserves the documented exact valid-state behavior
    for its
    ``real_is`` contract.

    Method: Construct the public SUT with the retained valid synthetic inputs and
    inspect
    exact public state.

    Oracle: The fixed inputs and documented canonical public representation provide the
    independent exact oracle.

    Acceptance: Every retained exact identity, equality, ordering, type, and
    represented-state
    assertion holds.

    Interpretation: Pass supports this valid-state mapping; failure may identify
    implementation,
    fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    exact_inputs = (0, -7, 0.0, -2.5, float.fromhex("0x1.fffffffffffffp+1023"))
    stored_inputs = tuple(
        SUT(ContractValueKind.REAL, value).value for value in exact_inputs
    )
    rounded = SUT(ContractValueKind.REAL, 2**53 + 1).value
    assert all(type(stored) is float for stored in stored_inputs)
    assert all(math.isfinite(cast(float, stored)) for stored in stored_inputs)
    assert stored_inputs == tuple(float(value) for value in exact_inputs)
    assert type(rounded) is float
    assert rounded == float(2**53)
    assert rounded != 2**53 + 1


def test_constructor__real_is__rejects_wrong_types() -> None:
    """Evidence ID: SV-CPN-132

    Requirement: ``ContractValue`` rejects wrong semantic types for its ``real_is``
    contract.

    Method: Exercise every retained synthetic wrong-type input through the public SUT
    without private mutation.

    Oracle: The documented exact-type taxonomy independently requires ``TypeError`` for
    every retained call.

    Acceptance: Every retained wrong-type call raises exactly ``TypeError``.

    Interpretation: Pass supports this type partition; failure may identify
    implementation, fixture,
    oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError, match="real kind"):
        SUT(ContractValueKind.REAL, True)


def test_constructor__real_is__rejects_invalid_values() -> None:
    """Evidence ID: SV-CPN-108

    Requirement: ``ContractValue`` rejects malformed values of accepted semantic
    types for its
    ``real_is`` contract.

    Method: Exercise each preserved synthetic invalid-value input through the public SUT
    with
    no warning acceptance or private-state mutation.

    Oracle: The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance: Every preserved partition assertion raises exactly ``ValueError``;
    retained
    exact setup and state assertions also hold.

    Interpretation: Pass supports only this named value partition; failure may identify
    implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(ValueError, match="overflows binary64"):
        SUT(ContractValueKind.REAL, 10**400)


def test_constructor__integer_is__preserves_valid_state() -> None:
    """Evidence ID: SV-CPN-081

    Requirement: ``ContractValue`` preserves the documented exact valid-state behavior
    for its
    ``integer_is`` contract.

    Method: Construct the public SUT with the retained valid synthetic inputs and
    inspect
    exact public state.

    Oracle: The fixed inputs and documented canonical public representation provide the
    independent exact oracle.

    Acceptance: Every retained exact identity, equality, ordering, type, and
    represented-state
    assertion holds.

    Interpretation: Pass supports this valid-state mapping; failure may identify
    implementation,
    fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    minimum = -(2**63)
    maximum = 2**63 - 1
    stored_values = tuple(
        SUT(ContractValueKind.INTEGER, value).value for value in (minimum, 0, maximum)
    )
    assert all(type(stored) is int for stored in stored_values)
    assert stored_values == (minimum, 0, maximum)


def test_constructor__integer_is__rejects_wrong_types() -> None:
    """Evidence ID: SV-CPN-133

    Requirement: ``ContractValue`` rejects wrong semantic types for its ``integer_is``
    contract.

    Method: Exercise every retained synthetic wrong-type input through the public SUT
    without private mutation.

    Oracle: The documented exact-type taxonomy independently requires ``TypeError`` for
    every retained call.

    Acceptance: Every retained wrong-type call raises exactly ``TypeError``.

    Interpretation: Pass supports this type partition; failure may identify
    implementation, fixture,
    oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    minimum = -(2**63)
    maximum = 2**63 - 1
    tuple(
        SUT(ContractValueKind.INTEGER, value).value for value in (minimum, 0, maximum)
    )
    with pytest.raises(TypeError, match="integer kind"):
        SUT(ContractValueKind.INTEGER, False)


def test_constructor__integer_is__rejects_invalid_values() -> None:
    """Evidence ID: SV-CPN-109

    Requirement: ``ContractValue`` rejects malformed values of accepted semantic
    types for its
    ``integer_is`` contract.

    Method: Exercise each preserved synthetic invalid-value input through the public SUT
    with
    no warning acceptance or private-state mutation.

    Oracle: The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance: Every preserved partition assertion raises exactly ``ValueError``;
    retained
    exact setup and state assertions also hold.

    Interpretation: Pass supports only this named value partition; failure may identify
    implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    minimum = -(2**63)
    maximum = 2**63 - 1
    with pytest.raises(ValueError, match="signed i64"):
        SUT(ContractValueKind.INTEGER, minimum - 1)
    with pytest.raises(ValueError, match="signed i64"):
        SUT(ContractValueKind.INTEGER, maximum + 1)
