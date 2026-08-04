"""Software verification for ``CpnMarking`` as the sole primary SUT.

Evidence class: software verification. Requirement and strategy are stated per
case; public construction/execution supplies the method and exact state or the
documented exception taxonomy supplies the independent oracle. Passing verifies
only the named class contract. It does not provide numerical verification,
scientific validation, uncertainty quantification, persistence, SNAKES-adapter,
Rust-conformance, or scientific-execution evidence. Collaborators are synthetic
setup only.
"""

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


def test_cpn_sv_p1_012_marking_preserves_multiplicity_and_order(
    token_factory: Callable[..., CpnToken], executable_net: CpnNetDefinition
) -> None:
    """SV-CPN-012: multiset multiplicity and canonical token order.

    Requirement
    -----------
    The version-1 P1 contract requires multiset multiplicity and canonical token
    order.

    Method
    ------
    Construct ``CpnMarking`` with ``work-b`` then ``work-a`` at one place.

    Independent oracle
    ------------------
    Stable token identity defines lexical order while two distinct identities
    establish multiplicity two.

    Acceptance criterion
    --------------------
    Stored IDs are exactly ``work-a, work-b`` while both identities remain present.

    Failure interpretation
    ----------------------
    Failure implies order dependence or Boolean/multiplicity collapse.

    Limitations
    -----------
    No durable marking repository is tested.
    """
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


def test_cpn_sv_p1_061_marking_version_identity_and_revision_taxonomy() -> None:
    """SV-CPN-061: enforce fixed version, model identity, and nonnegative revision.

    Public construction is the method; documented exact scalar types and lower
    bounds are the oracle. Acceptance distinguishes ``TypeError`` from ``ValueError``.
    Failure admits malformed revision state. The upper bound is covered separately.
    """
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


def test_cpn_sv_p1_083_revision_uses_nonnegative_signed_i64_range() -> None:
    """SV-CPN-083: admit the full representable marking-revision interval.

    Requirement: marking revisions are exact built-in integers from zero through
    ``2**63 - 1`` and reject ``2**63``; schema version remains the fixed v1 tag.
    Method: construct empty synthetic markings at both endpoints and immediately
    above the maximum. Oracle: the approved nonnegative signed-i64 bounds.
    Acceptance preserves each endpoint and raises ``ValueError`` for overflow.
    Failure prevents expression-compatible revision routing or admits an
    unrepresentable successor. No persistence or scientific state is tested.
    """
    maximum = 2**63 - 1
    assert SUT(1, "m", 0, ()).revision == 0
    assert SUT(1, "m", maximum, ()).revision == maximum
    with pytest.raises(ValueError, match="signed i64"):
        SUT(1, "m", maximum + 1, ())


def test_cpn_sv_p1_062_places_require_immutable_owner_types() -> None:
    """SV-CPN-062: accept only an immutable tuple of PlaceMarking owners.

    Empty complete synthetic state is the valid fixture; declared tuple/item types
    are the oracle. Acceptance admits the tuple and rejects mutable or foreign items
    with ``TypeError``. Failure permits an unstable marking container.
    """
    assert SUT(1, "m", 0, ()).places == ()
    with pytest.raises(TypeError):
        SUT(1, "m", 0, [])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(1, "m", 0, ("p",))  # type: ignore[arg-type]
