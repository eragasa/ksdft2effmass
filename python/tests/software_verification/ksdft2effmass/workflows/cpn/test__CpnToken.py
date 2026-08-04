"""Software verification for ``CpnToken`` as the sole primary SUT.

Evidence class: software verification. Requirement and strategy are stated per
case; public construction/execution supplies the method and exact state or the
documented exception taxonomy supplies the independent oracle. Passing verifies
only the named class contract. It does not provide numerical verification,
scientific validation, uncertainty quantification, persistence, SNAKES-adapter,
Rust-conformance, or scientific-execution evidence. Collaborators are synthetic
setup only.
"""

from collections.abc import Callable
from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.workflows.cpn import (
    CpnToken,
)

pytestmark = pytest.mark.software_verification

SUT = CpnToken


def test_cpn_sv_p1_001_token_is_immutable_and_canonical(
    token_factory: Callable[..., CpnToken],
) -> None:
    """SV-CPN-001: immutable token storage and canonical identity tuples.

    Requirement
    -----------
    The version-1 P1 contract requires immutable token storage and canonical
    identity tuples.

    Method
    ------
    Construct ``CpnToken`` through ``token_factory`` with unsorted provenance/parent
    IDs, then attempt assignment to ``run_id``.

    Independent oracle
    ------------------
    Lexical Unicode order gives ``('provenance-a', 'provenance-b')`` and
    ``('parent-a', 'parent-b')``; frozen dataclasses raise ``FrozenInstanceError``
    on assignment.

    Acceptance criterion
    --------------------
    Both tuples equal those sequences and mutation is rejected.

    Failure interpretation
    ----------------------
    A failure means token-owned canonicalization or operational immutability
    regressed.

    Limitations
    -----------
    This does not verify referenced provenance/lineage records or scientific
    meaning.
    """
    token = token_factory(
        "token-1",
        parent_run_id="parent-run",
        retry_parent_attempt_id="attempt-0",
        iteration_index=2,
        payload_type_id="payload.type",
        payload_id="payload-1",
        payload_schema_version=1,
        provenance_ids=("provenance-b", "provenance-a"),
        parent_token_ids=("parent-b", "parent-a"),
    )
    assert token.provenance_ids == ("provenance-a", "provenance-b")
    assert token.parent_token_ids == ("parent-a", "parent-b")
    with pytest.raises(FrozenInstanceError):
        token.run_id = "changed"  # type: ignore[misc]


def test_cpn_sv_p1_002_payload_reference_is_all_or_none(
    token_factory: Callable[..., CpnToken],
) -> None:
    """SV-CPN-002: all-or-none payload references.

    Requirement
    -----------
    The version-1 P1 contract requires all-or-none payload references.

    Method
    ------
    Call the public ``CpnToken`` constructor with only ``payload_type_id`` present.

    Independent oracle
    ------------------
    The token invariant requires type, identity, and schema version to be
    simultaneously present or absent.

    Acceptance criterion
    --------------------
    Construction raises ``ValueError`` containing ``all present or all absent``.

    Failure interpretation
    ----------------------
    Acceptance of the token would create an unusable payload reference.

    Limitations
    -----------
    No payload schema content or persistence is tested.
    """
    with pytest.raises(ValueError, match="all present or all absent"):
        token_factory("token-1", payload_type_id="payload.type")


def test_cpn_sv_p1_003_boolean_iteration_is_rejected(
    token_factory: Callable[..., CpnToken],
) -> None:
    """SV-CPN-003: Boolean rejection at the iteration-index boundary.

    Requirement
    -----------
    The version-1 P1 contract requires Boolean rejection at the iteration-index
    boundary.

    Method
    ------
    Call ``CpnToken`` with ``iteration_index=True`` through the public constructor
    path.

    Independent oracle
    ------------------
    The documented Python semantic taxonomy treats Boolean as distinct from the
    nonnegative integer iteration index.

    Acceptance criterion
    --------------------
    Construction raises ``TypeError`` naming ``iteration_index``.

    Failure interpretation
    ----------------------
    Any other result means the public Boolean/integer boundary changed.

    Limitations
    -----------
    This Boolean-rejection case excludes portable integer width and overflow; those
    resolved contracts are covered separately by ``SV-CPN-080``--``SV-CPN-088``.
    """
    with pytest.raises(TypeError, match="iteration_index"):
        token_factory("token-1", iteration_index=True)


def test_cpn_sv_p1_063_required_identities_are_exact_nonempty_strings(
    token_factory: Callable[..., CpnToken],
) -> None:
    """SV-CPN-063: validate every required routing identity.

    Controlled overrides exercise the public boundary; exact string/nonempty rules
    are the oracle. Acceptance requires ``TypeError`` for integers and ``ValueError``
    for empties. Failure admits unusable token identity state.
    """
    with pytest.raises(TypeError):
        token_factory(1)
    with pytest.raises(ValueError):
        token_factory("")
    for field in ("color_id", "workflow_id", "run_id", "attempt_id"):
        with pytest.raises(TypeError):
            token_factory("token", **{field: 1})
        with pytest.raises(ValueError):
            token_factory("token", **{field: ""})


def test_cpn_sv_p1_064_optional_identities_reject_wrong_or_empty_values(
    token_factory: Callable[..., CpnToken],
) -> None:
    """SV-CPN-064: constrain optional identities to None or nonempty strings.

    Public controlled-invalid overrides are the method; the documented optional
    identity union is the oracle. Acceptance distinguishes type and invariant errors.
    Failure admits ambiguous routing references.
    """
    fields = (
        "parent_run_id",
        "retry_parent_attempt_id",
        "correlation_id",
        "authorization_id",
    )
    for field in fields:
        with pytest.raises(TypeError):
            token_factory("token", **{field: 1})
        with pytest.raises(ValueError):
            token_factory("token", **{field: ""})
    complete_payload = {
        "payload_type_id": "type",
        "payload_id": "payload",
        "payload_schema_version": 1,
    }
    for field in ("payload_type_id", "payload_id"):
        with pytest.raises(TypeError):
            token_factory("token", **(complete_payload | {field: 1}))
        with pytest.raises(ValueError):
            token_factory("token", **(complete_payload | {field: ""}))


def test_cpn_sv_p1_065_iteration_requires_nonnegative_exact_integer(
    token_factory: Callable[..., CpnToken],
) -> None:
    """SV-CPN-065: enforce the resolved iteration type and lower bound.

    Public construction is checked against exact built-in type and zero lower bound.
    Acceptance admits zero, rejects a float with ``TypeError``, and negative one with
    ``ValueError``. Width and upper-bound behavior are explicitly excluded.
    """
    assert token_factory("token", iteration_index=0).iteration_index == 0
    with pytest.raises(TypeError):
        token_factory("token", iteration_index=1.0)
    with pytest.raises(ValueError):
        token_factory("token", iteration_index=-1)


def test_cpn_sv_p1_066_payload_version_requires_nonnegative_exact_integer(
    token_factory: Callable[..., CpnToken],
) -> None:
    """SV-CPN-066: enforce the payload-version type and nonnegative lower bound.

    A complete payload reference avoids relational invalidity. Acceptance admits
    zero, rejects Boolean with ``TypeError``, and rejects negative one with
    ``ValueError``. The signed-i64 upper boundary is covered separately.
    """
    base = {"payload_type_id": "type", "payload_id": "payload"}
    assert (
        token_factory("token", **base, payload_schema_version=0).payload_schema_version
        == 0
    )
    with pytest.raises(TypeError):
        token_factory("token", **base, payload_schema_version=True)
    with pytest.raises(ValueError):
        token_factory("token", **base, payload_schema_version=-1)


def test_cpn_sv_p1_082_expression_visible_controls_use_nonnegative_i64_range(
    token_factory: Callable[..., CpnToken],
) -> None:
    """SV-CPN-082: bound token control fields to nonnegative signed-i64.

    Requirement: expression-visible ``iteration_index`` and payload schema version
    accept every endpoint from zero through ``2**63 - 1`` and reject ``2**63``;
    Boolean remains a semantic type error. Method: construct public tokens at the
    lower/upper boundaries with a complete payload reference. Oracle: the approved
    nonnegative signed-i64 interval. Acceptance preserves exact built-in integers
    and applies the documented exception taxonomy. Failure creates a stored control
    that cannot route through INTEGER expressions. Payloads are synthetic IDs; no
    persistence, scientific validation, or UQ is exercised.
    """
    maximum = 2**63 - 1
    for value in (0, maximum):
        assert (
            token_factory("iteration", iteration_index=value).iteration_index == value
        )
        payload = token_factory(
            "payload",
            payload_type_id="type",
            payload_id="payload-id",
            payload_schema_version=value,
        )
        assert payload.payload_schema_version == value
    for field in ("iteration_index", "payload_schema_version"):
        overrides: dict[str, object] = {field: 2**63}
        if field == "payload_schema_version":
            overrides.update(payload_type_id="type", payload_id="payload-id")
        with pytest.raises(ValueError, match="signed i64"):
            token_factory("overflow", **overrides)


def test_cpn_sv_p1_067_identity_tuples_and_outcome_are_strict(
    token_factory: Callable[..., CpnToken],
) -> None:
    """SV-CPN-067: require unique nonempty identity tuples and typed outcome state.

    Controlled public overrides are compared with tuple uniqueness and declared
    owner type. Acceptance raises exact type/value categories. Failure permits
    mutable lineage or foreign outcome state; collaborators are not validated.
    """
    for field in ("provenance_ids", "parent_token_ids"):
        with pytest.raises(TypeError):
            token_factory("token", **{field: ["p"]})
        with pytest.raises(TypeError):
            token_factory("token", **{field: (1,)})
        with pytest.raises(ValueError):
            token_factory("token", **{field: ("",)})
        with pytest.raises(ValueError):
            token_factory("token", **{field: ("p", "p")})
    with pytest.raises(TypeError):
        token_factory("token", outcome=True)
