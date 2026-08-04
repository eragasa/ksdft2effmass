"""Software verification of ``CpnToken`` public token-state contract.

Evidence class and represented meaning
--------------------------------------
Software-verification evidence covers the public ``CpnToken`` DataObject: a finite
software representation of workflow-control token state. No physical model or
mathematical operator is represented by these synthetic cases.

Owned contract, oracle, and scope
---------------------------------
The sole primary SUT is ``CpnToken``. The owned contract comprises public constructor
invariants, canonical stored identities, and operational immutability; its oracle is the
documented exact token contract and Python exception taxonomy. Inputs use synthetic
identifiers and the approved nonnegative signed-i64 control range without exercising
external services.

VVUQ and scientific exclusions
------------------------------
Passing confirms only the stated represented-software behavior; failure may indicate
production, fixture, oracle, or public-contract drift. This module does not provide
numerical verification, scientific validation, uncertainty quantification,
physical-correctness, persistence, SNAKES-adapter, cross-language, or
scientific-execution evidence."""

from collections.abc import Callable
from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.workflows.cpn import (
    CpnToken,
)

pytestmark = pytest.mark.software_verification

SUT = CpnToken


def test_constructor__routing_state__canonicalizes_and_freezes_token(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify canonical identity tuples and immutable token storage.

    Evidence ID
    SV-CPN-001

    Requirement
    Public ``CpnToken`` construction must sort provenance and parent-token identities
    into canonical tuples, and constructed state must reject field assignment.

    Method
    Construct a token through ``token_factory`` with deliberately unsorted synthetic
    identity tuples, inspect both public fields, and attempt to assign a different
    ``run_id``. No warnings are expected.

    Oracle
    Exact Unicode lexical order independently fixes the two expected tuples as
    ``('provenance-a', 'provenance-b')`` and ``('parent-a', 'parent-b')``;
    frozen-dataclass assignment semantics require ``FrozenInstanceError``.

    Acceptance
    Both fields equal the exact expected tuples and assignment raises
    ``FrozenInstanceError``.

    Interpretation
    A pass confirms token-owned canonicalization and operational immutability. A failure
    may reflect constructor, fixture, language-semantics, or contract drift rather than
    establishing a scientific defect.

    Limitations
    Synthetic identities do not validate referenced provenance or lineage, persistence,
    numerical mathematics, physical correctness, scientific validation, uncertainty
    quantification, or cross-language behavior."""
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


def test_constructor__payload_reference__requires_all_fields_or_none(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify rejection of a partial payload reference.

    Evidence ID
    SV-CPN-002

    Requirement
    A public ``CpnToken`` payload reference must supply payload type, payload identity,
    and schema version together, or omit all three.

    Method
    Construct through ``token_factory`` with only ``payload_type_id`` present, creating
    the controlled-invalid partial-reference boundary. No warnings are expected.

    Oracle
    The documented all-or-none payload-reference invariant independently makes a
    one-field reference invalid and assigns invariant violations to ``ValueError``.

    Acceptance
    Construction raises ``ValueError`` with text matching ``all present or all absent``.

    Interpretation
    A pass confirms enforcement of relational payload-reference completeness. A failure
    may arise from constructor, fixture, message, taxonomy, or contract drift and would
    permit unusable represented state if construction succeeds.

    Limitations
    The synthetic reference does not test payload content, schema validity, persistence,
    numerical verification, physical correctness, scientific validation, uncertainty
    quantification, or cross-language behavior."""
    with pytest.raises(ValueError, match="all present or all absent"):
        token_factory("token-1", payload_type_id="payload.type")


def test_field__iteration_index__rejects_boolean(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify Boolean rejection at the iteration-index boundary.

    Evidence ID
    SV-CPN-003

    Requirement
    The public ``iteration_index`` field must accept an exact integer contract rather
    than treating Python Boolean values as integers.

    Method
    Invoke public token construction through ``token_factory`` with
    ``iteration_index=True`` as a controlled semantic-type fault. No warnings are
    expected.

    Oracle
    The documented public type taxonomy distinguishes ``bool`` from the exact
    nonnegative integer required for an iteration index and assigns wrong semantic types
    to ``TypeError``.

    Acceptance
    Construction raises ``TypeError`` whose message names ``iteration_index``.

    Interpretation
    A pass confirms the Boolean/integer boundary; any other result may indicate
    constructor, fixture, error-message, taxonomy, or contract drift.

    Limitations
    This case excludes integer width and overflow, payload behavior, numerical
    verification, physical correctness, scientific validation, uncertainty
    quantification, and cross-language conformance."""
    with pytest.raises(TypeError, match="iteration_index"):
        token_factory("token-1", iteration_index=True)


def test_constructor__required_identities__requires_exact_nonempty_strings(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify every required routing identity at the constructor boundary.

    Evidence ID
    SV-CPN-063

    Requirement
    ``token_id``, ``color_id``, ``workflow_id``, ``run_id``, and ``attempt_id`` must
    each be exact nonempty strings.

    Method
    Use ``token_factory`` to pass an integer and an empty string for the primary token
    identity and for each named required routing field. These are controlled-invalid
    public inputs; no warnings are expected.

    Oracle
    The documented identity contract independently classifies nonstrings as semantic
    type errors and empty strings as invariant violations.

    Acceptance
    Every integer case raises ``TypeError`` and every empty-string case raises
    ``ValueError``.

    Interpretation
    A pass confirms uniform enforcement across all required identities. A failure may
    indicate constructor, fixture, parameter-loop, taxonomy, or contract drift and could
    admit unusable routing state.

    Limitations
    Synthetic strings do not test identifier registries, Unicode normalization,
    persistence, numerical verification, physical correctness, scientific validation,
    uncertainty quantification, or cross-language behavior."""
    with pytest.raises(TypeError):
        token_factory(1)
    with pytest.raises(ValueError):
        token_factory("")
    for field in ("color_id", "workflow_id", "run_id", "attempt_id"):
        with pytest.raises(TypeError):
            token_factory("token", **{field: 1})
        with pytest.raises(ValueError):
            token_factory("token", **{field: ""})


def test_constructor__optional_identities__rejects_wrong_or_empty_values(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify optional routing and payload identities when present.

    Evidence ID
    SV-CPN-064

    Requirement
    Optional routing identities and present payload type/identity fields must be
    nonempty strings rather than wrong-typed or empty values.

    Method
    Through ``token_factory``, override each optional routing identity with an integer
    and an empty string, then do the same for payload type and identity while supplying
    an otherwise complete payload reference. No warnings are expected.

    Oracle
    The public optional-identity union permits only ``None`` or a nonempty exact string;
    its error taxonomy assigns wrong types to ``TypeError`` and empty values to
    ``ValueError``.

    Acceptance
    Each integer override raises ``TypeError`` and each empty-string override raises
    ``ValueError`` for every exercised field.

    Interpretation
    A pass confirms optional references cannot become ambiguous represented identities.
    A failure may reflect constructor, fixture, loop coverage, taxonomy, or
    public-contract drift.

    Limitations
    This does not inspect referenced records or payload schemas and provides no
    persistence, numerical-verification, physical-correctness, scientific-validation,
    uncertainty-quantification, or cross-language claim."""
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


def test_field__iteration_index__requires_nonnegative_exact_integer(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify the iteration-index exact type and lower boundary.

    Evidence ID
    SV-CPN-065

    Requirement
    ``iteration_index`` must accept zero as a nonnegative exact integer, reject a
    floating-point value as the wrong semantic type, and reject negative one as outside
    its invariant domain.

    Method
    Construct public tokens through ``token_factory`` at zero, with ``1.0``, and with
    ``-1``. The inputs are exact boundary and controlled-invalid cases; no warnings are
    expected.

    Oracle
    The approved integer-domain contract independently includes zero, excludes floats,
    and places negative integers below the inclusive lower bound.

    Acceptance
    Zero is stored exactly as ``0``; ``1.0`` raises ``TypeError``; and ``-1`` raises
    ``ValueError``.

    Interpretation
    A pass confirms the represented lower boundary and exception taxonomy. A failure may
    arise from constructor, fixture, Python-type, or contract drift.

    Limitations
    Upper-bound behavior is owned by separate evidence; these dimensionless control
    values provide no numerical algorithm verification, physical correctness, scientific
    validation, UQ, or cross-language conformance."""
    assert token_factory("token", iteration_index=0).iteration_index == 0
    with pytest.raises(TypeError):
        token_factory("token", iteration_index=1.0)
    with pytest.raises(ValueError):
        token_factory("token", iteration_index=-1)


def test_field__payload_schema_version__requires_nonnegative_exact_integer(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify payload-schema-version type and lower boundary.

    Evidence ID
    SV-CPN-066

    Requirement
    In a complete payload reference, ``payload_schema_version`` must accept zero as a
    nonnegative exact integer, reject Boolean, and reject negative one.

    Method
    Supply synthetic payload type and identity fields through ``token_factory`` and
    construct at schema version zero, ``True``, and ``-1``. Completeness isolates the
    scalar boundary; no warnings are expected.

    Oracle
    The approved schema-version contract independently includes zero, excludes Boolean
    from exact integers, and excludes values below the inclusive nonnegative lower
    bound.

    Acceptance
    Zero is stored exactly as ``0``; ``True`` raises ``TypeError``; and ``-1`` raises
    ``ValueError``.

    Interpretation
    A pass confirms the represented lower boundary without conflating it with payload
    completeness. A failure may reflect constructor, fixture, type-taxonomy, or contract
    drift.

    Limitations
    The upper signed-i64 boundary and payload schema content are covered elsewhere; this
    establishes no numerical verification, physical correctness, scientific validation,
    UQ, persistence, or cross-language behavior."""
    base = {"payload_type_id": "type", "payload_id": "payload"}
    assert (
        token_factory("token", **base, payload_schema_version=0).payload_schema_version
        == 0
    )
    with pytest.raises(TypeError):
        token_factory("token", **base, payload_schema_version=True)
    with pytest.raises(ValueError):
        token_factory("token", **base, payload_schema_version=-1)


def test_field__expression_visible_controls__enforces_nonnegative_i64_range(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify signed-i64 boundaries for expression-visible token controls.

    Evidence ID
    SV-CPN-082

    Requirement
    ``iteration_index`` and ``payload_schema_version`` must accept the inclusive
    nonnegative signed-i64 endpoints zero and ``2**63 - 1`` and reject ``2**63``.

    Method
    Construct public tokens through ``token_factory`` at both endpoints for each
    control, using a complete synthetic payload reference where required, then inject
    one-above-maximum values. No warnings are expected.

    Oracle
    The approved, dimensionless signed-i64 interval is independently ``[0, 2**63 - 1]``;
    exact integer comparison fixes both endpoints, while ``2**63`` lies outside the
    inclusive range.

    Acceptance
    Both endpoints are stored exactly for both fields, and each ``2**63`` case raises
    ``ValueError`` with text matching ``signed i64``; accepted nonzero maxima must not
    be replaced by zero.

    Interpretation
    A pass confirms portable expression-visible storage boundaries. A failure may
    indicate constructor, fixture, boundary-oracle, message, or contract drift and could
    admit a value unavailable to INTEGER expressions.

    Limitations
    These exact range checks do not exercise expression evaluation, payload persistence,
    numerical algorithms, physical correctness, scientific validation, uncertainty
    quantification, or cross-language execution."""
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


def test_constructor__identity_tuples_and_outcome__enforces_strict_types(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify strict lineage tuples and outcome ownership.

    Evidence ID
    SV-CPN-067

    Requirement
    Provenance and parent-token collections must be tuples of unique nonempty strings,
    and ``outcome`` must be a ``TokenOutcome`` value rather than a Boolean.

    Method
    For both identity-tuple fields, pass a list, an integer member, an empty member, and
    a duplicate member through ``token_factory``; separately pass ``outcome=True``.
    These are controlled-invalid inputs and emit no warnings.

    Oracle
    The documented public field types require immutable tuples and the declared outcome
    owner type, while tuple identity invariants independently require nonempty unique
    strings.

    Acceptance
    Lists, integer members, and Boolean outcome raise ``TypeError``; empty and duplicate
    tuple members raise ``ValueError`` for both tuple fields.

    Interpretation
    A pass confirms strict represented lineage and outcome boundaries. A failure may
    arise from constructor, fixture, loop coverage, collaborator type, error taxonomy,
    or contract drift.

    Limitations
    The test does not validate provenance records, parent tokens, or ``TokenOutcome``
    internals and provides no persistence, numerical-verification, physical-correctness,
    scientific-validation, UQ, or cross-language evidence."""
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
