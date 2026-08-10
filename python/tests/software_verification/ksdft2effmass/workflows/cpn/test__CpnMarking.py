r"""Software verification of ``CpnMarking``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public ``CpnMarking``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
``CpnMarking`` is the sole primary SUT. Tests exercise its documented public contract
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

from collections.abc import Callable

import pytest

from ksdft2effmass.workflows.cpn import (
    CpnMarking,
    CpnNetDefinition,
    CpnToken,
    PlaceMarking,
)

pytestmark = pytest.mark.software_verification

SUT = CpnMarking


def test_constructor__fields__marking_preserves_multiplicity_and_order(
    token_factory: Callable[..., CpnToken], executable_net: CpnNetDefinition
) -> None:
    """Evidence ID: SV-CPN-012

    Requirement: multiset multiplicity and canonical token order.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: multiset multiplicity and canonical token
    order. Prior requirement detail: The version-1 P1 contract requires multiset
    multiplicity and canonical token order. Prior method detail: Construct
    ``CpnMarking`` with ``work-b`` then ``work-a`` at one place. Prior independent
    oracle detail: Stable token identity defines lexical order while two distinct
    identities establish multiplicity two. Prior acceptance criterion detail: Stored IDs
    are exactly ``work-a, work-b`` while both identities remain present. Prior failure
    interpretation detail: Failure implies order dependence or Boolean/multiplicity
    collapse. Prior limitations detail: No durable marking repository is tested.

    Oracle: The documented public rule that the SUT must multiset multiplicity and
    canonical
    token order is the contract oracle; fixed synthetic values, Python exact type/value
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
    marking = CpnMarking(
        1,
        executable_net.model_id,
        0,
        (
            PlaceMarking("ready", (token_factory("work-b"), token_factory("work-a"))),
            PlaceMarking("completed", ()),
            PlaceMarking("authorization", (token_factory("auth", "authorization"),)),
        ),
    )
    assert tuple(token.token_id for token in marking.places[2].tokens) == (
        "work-a",
        "work-b",
    )


def test_constructor__marking_version__rejects_wrong_types() -> None:
    """Evidence ID: SV-CPN-061

    Requirement: ``CpnMarking`` rejects wrong semantic types at the public
    constructor boundary for its
    ``marking_version`` contract.

    Method: Exercise each preserved synthetic wrong-type input through the public SUT
    with
    no warning acceptance or private-state mutation.

    Oracle: The documented public exact-type taxonomy and Python exception taxonomy
    independently require ``TypeError`` for these inputs.

    Acceptance: Every preserved partition assertion raises exactly ``TypeError``;
    retained
    exact setup and state assertions also hold.

    Interpretation: Pass supports only this named type partition; failure may identify
    implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError):
        SUT(True, "m", 0, ())
    with pytest.raises(TypeError):
        SUT(1, 1, 0, ())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(1, "m", 0.0, ())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(1, "m", True, ())


def test_constructor__marking_version__rejects_invalid_values() -> None:
    """Evidence ID: SV-CPN-091

    Requirement: ``CpnMarking`` rejects malformed values of accepted semantic
    types for its
    ``marking_version`` contract.

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
    with pytest.raises(ValueError):
        SUT(2, "m", 0, ())
    with pytest.raises(ValueError):
        SUT(1, "", 0, ())
    with pytest.raises(ValueError):
        SUT(1, "m", -1, ())


def test_constructor__fields__revision_uses_nonnegative_signed_i64_range() -> None:
    """Evidence ID: SV-CPN-083

    Requirement: ``CpnMarking`` preserves the exact accepted state for its
    ``fields`` contract.

    Method: Construct the public SUT and inspect retained exact public outcomes.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact state oracle.

    Acceptance: Every retained exact state assertion holds.

    Interpretation: Pass supports only this accepted-state partition; failure may
    identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    maximum = 2**63 - 1
    assert SUT(1, "m", 0, ()).revision == 0
    assert SUT(1, "m", maximum, ()).revision == maximum


def test_constructor__fields__rejects_invalid_state() -> None:
    """Evidence ID: SV-CPN-139

    Requirement: ``CpnMarking`` rejects the documented invalid state for its
    ``fields`` contract.

    Method: Exercise the retained synthetic invalid inputs through the public SUT.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact error-taxonomy oracle.

    Acceptance: Every retained invalid call raises the documented exact public
    exception.

    Interpretation: Pass supports only this rejection partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    maximum = 2**63 - 1
    with pytest.raises(ValueError, match="signed i64"):
        SUT(1, "m", maximum + 1, ())


def test_constructor__fields__places_require_immutable_owner_types() -> None:
    """Evidence ID: SV-CPN-062

    Requirement: ``CpnMarking`` preserves the exact accepted state for its
    ``fields`` contract.

    Method: Construct the public SUT and inspect retained exact public outcomes.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact state oracle.

    Acceptance: Every retained exact state assertion holds.

    Interpretation: Pass supports only this accepted-state partition; failure may
    identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    assert SUT(1, "m", 0, ()).places == ()


def test_constructor__fields__rejects_invalid_52() -> None:
    """Evidence ID: SV-CPN-140

    Requirement: ``CpnMarking`` rejects the documented invalid state for its
    ``fields`` contract.

    Method: Exercise the retained synthetic invalid inputs through the public SUT.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact error-taxonomy oracle.

    Acceptance: Every retained invalid call raises the documented exact public
    exception.

    Interpretation: Pass supports only this rejection partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError):
        SUT(1, "m", 0, [])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(1, "m", 0, ("p",))  # type: ignore[arg-type]
