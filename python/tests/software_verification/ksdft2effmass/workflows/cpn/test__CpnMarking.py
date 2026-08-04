"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``CpnMarking``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
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


def test_constructor__contract__marking_preserves_multiplicity_and_order(
    token_factory: Callable[..., CpnToken], executable_net: CpnNetDefinition
) -> None:
    """Evidence ID
    -----------
    SV-CPN-012

    Requirement
    -----------
    multiset multiplicity and canonical token order.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
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

    Oracle
    ------
    The documented public rule that the SUT must multiset multiplicity and canonical
    token order is the contract oracle; fixed synthetic values, Python exact type/value
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


def test_constructor__contract__marking_version_identity_and_revision_taxonomy() -> (
    None
):
    """Evidence ID
    -----------
    SV-CPN-061

    Requirement
    -----------
    enforce fixed version, model identity, and nonnegative revision.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: enforce fixed version, model identity, and
    nonnegative revision. Public construction is the method; documented exact scalar
    types and lower bounds are the oracle. Acceptance distinguishes ``TypeError`` from
    ``ValueError``. Failure admits malformed revision state. The upper bound is covered
    separately.

    Oracle
    ------
    The documented public rule that the SUT must enforce fixed version, model identity,
    and nonnegative revision is the contract oracle; fixed synthetic values, Python
    exact type/value semantics, and the public error taxonomy provide independently
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
    with pytest.raises(TypeError):
        SUT(True, "m", 0, ())
    with pytest.raises(ValueError):
        SUT(2, "m", 0, ())
    with pytest.raises(TypeError):
        SUT(1, 1, 0, ())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT(1, "", 0, ())
    with pytest.raises(TypeError):
        SUT(1, "m", 0.0, ())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(1, "m", True, ())
    with pytest.raises(ValueError):
        SUT(1, "m", -1, ())


def test_constructor__contract__revision_uses_nonnegative_signed_i64_range() -> None:
    """Evidence ID
    -----------
    SV-CPN-083

    Requirement
    -----------
    marking revision uses the nonnegative signed-i64 interval.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: admit the full representable
    marking-revision interval. Requirement: marking revisions are exact built-in
    integers from zero through ``2**63 - 1`` and reject ``2**63``; schema version
    remains the fixed v1 tag. Method: construct empty synthetic markings at both
    endpoints and immediately above the maximum. Oracle: the approved nonnegative
    signed-i64 bounds. Acceptance preserves each endpoint and raises ``ValueError`` for
    overflow. Failure prevents expression-compatible revision routing or admits an
    unrepresentable successor. No persistence or scientific state is tested.

    Oracle
    ------
    The documented public rule that the SUT must marking revision uses the nonnegative
    signed-i64 interval is the contract oracle; fixed synthetic values, Python exact
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
    maximum = 2**63 - 1
    assert SUT(1, "m", 0, ()).revision == 0
    assert SUT(1, "m", maximum, ()).revision == maximum
    with pytest.raises(ValueError, match="signed i64"):
        SUT(1, "m", maximum + 1, ())


def test_constructor__contract__places_require_immutable_owner_types() -> None:
    """Evidence ID
    -----------
    SV-CPN-062

    Requirement
    -----------
    accept only an immutable tuple of PlaceMarking owners.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: accept only an immutable tuple of
    PlaceMarking owners. Empty complete synthetic state is the valid fixture; declared
    tuple/item types are the oracle. Acceptance admits the tuple and rejects mutable or
    foreign items with ``TypeError``. Failure permits an unstable marking container.

    Oracle
    ------
    The documented public rule that the SUT must accept only an immutable tuple of
    PlaceMarking owners is the contract oracle; fixed synthetic values, Python exact
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
    assert SUT(1, "m", 0, ()).places == ()
    with pytest.raises(TypeError):
        SUT(1, "m", 0, [])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(1, "m", 0, ("p",))  # type: ignore[arg-type]
