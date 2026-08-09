r"""Software verification of ``HumanReviewDecision``.

Facet and represented meaning
Software verification of the immutable runtime representation of an explicit human
decision.

Intrinsic and cross-object scope
The sole primary SUT is ``HumanReviewDecision``. Exact fields, intrinsic invariants,
immutability, and value semantics are covered; packet compatibility belongs to
``HumanReviewDecisionRecorder``.

VVUQ and scientific exclusions
Passing establishes only the stated software contract. It does not authenticate human
authority or establish numerical verification, scientific validation, UQ, or decision
persistence.
"""

from dataclasses import FrozenInstanceError, replace

import pytest

from ksdft2effmass.harness.pi import (
    HumanReviewDecision,
    HumanReviewPacket,
    HumanReviewTarget,
)

pytestmark = pytest.mark.software_verification
SUT = HumanReviewDecision


class StringSubclass(str):
    """Support exact built-in string rejection without owning evidence."""


def make_packet() -> HumanReviewPacket:
    """Evidence ID
    Owns no identifier; supports decision evidence.
    Requirement
    Decision tests require one exact immutable packet.
    Method
    Construct a fixed target and intrinsically valid empty ready packet.
    Oracle
    Public target and packet constructors define valid support values.
    Acceptance
    Return one HumanReviewPacket.
    Interpretation
    Failure identifies setup drift rather than decision behavior.
    Limitations
    The helper does not prepare, review, or disposition the packet.
    """
    target = HumanReviewTarget(
        "human-review.example",
        "a" * 40,
        "ExampleSubject",
        ("python/src/example.py",),
        "software_verification",
        (),
    )
    return HumanReviewPacket(target, (), (), (), "ready_for_human_review")


def make_decision() -> HumanReviewDecision:
    """Evidence ID
    Owns no identifier; supports decision evidence.
    Requirement
    Decision tests require one intrinsically valid bounded-correction result.
    Method
    Construct fixed explicit values through the public constructor.
    Oracle
    The accepted constructor contract defines valid support input.
    Acceptance
    Return one HumanReviewDecision.
    Interpretation
    Failure identifies setup drift rather than independent behavior.
    Limitations
    This helper owns no evidence claim.
    """
    return SUT(
        make_packet(),
        "  Correct only the stated paths.  ",
        "bounded_correction",
        ("Modify source.py only.",),
    )


def test_constructor__exact_fields__preserves_packet_text_and_scope() -> None:
    """Evidence ID
    ``SV-HARNESS-155``.
    Requirement
    A decision binds the exact immutable packet and defensively owns ordered scope.
    Method
    Construct a bounded decision with an explicit packet, whitespace, and punctuation,
    then inspect field values, exact types, tuple identity, and dataclass field order.
    Oracle
    Caller-supplied values, public packet identity, and the accepted four-field contract
    are exact independent oracles.
    Acceptance
    The packet is retained by identity, text is unchanged, scope order is retained in a
    separately owned tuple, and fields match the contract.
    Interpretation
    Failure identifies packet detachment, normalization, typing, or ownership drift.
    Limitations
    Construction does not establish caller authority or packet preparation provenance.
    """
    packet = make_packet()
    scope = ("First exact scope.", "Second exact scope!")
    response = "\n Accept exactly this; preserve punctuation! \t"
    decision = SUT(packet, response, "bounded_correction", scope)
    assert tuple(decision.__dataclass_fields__) == (
        "packet",
        "human_response",
        "disposition",
        "authorized_scope",
    )
    assert decision.packet is packet
    assert decision.human_response == response
    assert decision.disposition == "bounded_correction"
    assert decision.authorized_scope == scope
    assert decision.authorized_scope is not scope
    assert type(decision.packet) is HumanReviewPacket
    assert type(decision.human_response) is str
    assert type(decision.disposition) is str
    assert type(decision.authorized_scope) is tuple
    assert all(type(item) is str for item in decision.authorized_scope)
    with pytest.raises(TypeError, match="^packet must be HumanReviewPacket$"):
        replace(decision, packet=object())  # type: ignore[arg-type]


def test_field__immutability_and_equality__use_exact_value_semantics() -> None:
    """Evidence ID
    ``SV-HARNESS-156``.
    Requirement
    Decision state is frozen and independently equal constructions compare exactly.
    Method
    Compare two fixed decisions and attempt to replace the stored disposition in place.
    Oracle
    Frozen dataclass equality and assignment semantics are exact.
    Acceptance
    Equal inputs yield equal results and mutation raises FrozenInstanceError.
    Interpretation
    Failure identifies mutability or value-semantics drift.
    Limitations
    No serialization or persistence representation is implied.
    """
    first = make_decision()
    assert first == make_decision()
    with pytest.raises(FrozenInstanceError):
        first.disposition = "rejected"  # type: ignore[misc]


@pytest.mark.parametrize(
    "disposition",
    (
        pytest.param("accepted", id="accepted"),
        pytest.param("bounded_correction", id="bounded_correction"),
        pytest.param("deferred", id="deferred"),
        pytest.param("rejected", id="rejected"),
    ),
)
def test_constructor__disposition__accepts_closed_vocabulary(disposition: str) -> None:
    """Evidence ID
    ``SV-HARNESS-157``.
    Requirement
    The normalized disposition vocabulary contains exactly four accepted values.
    Method
    Construct each declared disposition with its contract-compatible scope.
    Oracle
    The accepted closed vocabulary supplies the exact strings.
    Acceptance
    Every declared value is retained unchanged.
    Interpretation
    Failure identifies vocabulary or scope-policy drift.
    Limitations
    The constructor does not infer a disposition from response text.
    """
    scope = (
        ("Correct one bounded surface.",) if disposition == "bounded_correction" else ()
    )
    decision = SUT(make_packet(), "Exact response.", disposition, scope)
    assert decision.disposition == disposition


@pytest.mark.parametrize(
    ("disposition", "scope", "message"),
    (
        pytest.param(
            "bounded_correction",
            (),
            "bounded_correction requires authorized_scope",
            id="bounded_correction_requires_scope",
        ),
        pytest.param(
            "accepted",
            ("Unexpected scope.",),
            "authorized_scope requires bounded_correction",
            id="accepted_prohibits_scope",
        ),
        pytest.param(
            "deferred",
            ("Unexpected scope.",),
            "authorized_scope requires bounded_correction",
            id="deferred_prohibits_scope",
        ),
        pytest.param(
            "rejected",
            ("Unexpected scope.",),
            "authorized_scope requires bounded_correction",
            id="rejected_prohibits_scope",
        ),
    ),
)
def test_constructor__scope_policy__rejects_invalid_disposition_combinations(
    disposition: str, scope: tuple[str, ...], message: str
) -> None:
    """Evidence ID
    ``SV-HARNESS-158``.
    Requirement
    Bounded correction alone requires scope; all other dispositions prohibit scope.
    Method
    Construct each invalid disposition/scope semantic partition.
    Oracle
    The accepted cross-field intrinsic invariant fixes exact rejection messages.
    Acceptance
    Every partition raises ValueError with its exact stable message.
    Interpretation
    Failure identifies an overbroad or missing authorization-scope boundary.
    Limitations
    Scope statements are represented text, not executable authorization.
    """
    with pytest.raises(ValueError, match=f"^{message}$"):
        SUT(make_packet(), "Exact response.", disposition, scope)


@pytest.mark.parametrize(
    ("scope", "message"),
    (
        pytest.param(
            ("Duplicate.", "Duplicate."),
            "authorized_scope must contain unique items",
            id="duplicate_items",
        ),
        pytest.param(
            ("",),
            "authorized_scope item must be nonempty",
            id="empty_item",
        ),
    ),
)
def test_constructor__authorized_scope__rejects_duplicate_and_empty_items(
    scope: tuple[str, ...], message: str
) -> None:
    """Evidence ID
    ``SV-HARNESS-159``.
    Requirement
    Authorized-scope items are nonempty and unique while retaining supplied order.
    Method
    Construct duplicate-item and empty-item bounded scopes.
    Oracle
    Exact tuple membership and string emptiness provide independent rules.
    Acceptance
    Each invalid partition raises ValueError with the stable message.
    Interpretation
    Failure identifies ambiguous or empty represented scope.
    Limitations
    The API does not interpret the substantive meaning of scope text.
    """
    with pytest.raises(ValueError, match=f"^{message}$"):
        SUT(make_packet(), "Exact response.", "bounded_correction", scope)


@pytest.mark.parametrize(
    ("field", "value"),
    (
        pytest.param("human_response", "", id="empty_response"),
        pytest.param("disposition", "pass", id="unsupported_disposition"),
    ),
)
def test_constructor__decision_values__rejects_invalid_lexical_values(
    field: str, value: str
) -> None:
    """Evidence ID
    ``SV-HARNESS-160``.
    Requirement
    Built-in string fields enforce nonempty-response and closed disposition invariants.
    Method
    Replace one valid field with each invalid built-in string partition.
    Oracle
    Public response and disposition contracts fix ValueError rejection.
    Acceptance
    Every partition raises ValueError before a decision is constructed.
    Interpretation
    Failure identifies lexical or vocabulary validation drift.
    Limitations
    Wrong semantic types are covered by a separate evidence owner.
    """
    with pytest.raises(ValueError):
        replace(make_decision(), **{field: value})  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("field", "value"),
    (
        pytest.param("review_id", "", id="empty_review_identifier"),
        pytest.param("reviewed_revision", "A" * 40, id="uppercase_revision"),
        pytest.param("reviewed_revision", "a" * 39, id="short_revision"),
        pytest.param(
            "review_id",
            StringSubclass("human-review.example"),
            id="identifier_subclass",
        ),
        pytest.param("reviewed_revision", 1, id="revision_wrong_type"),
        pytest.param(
            "human_response",
            StringSubclass("response"),
            id="response_subclass",
        ),
        pytest.param("disposition", True, id="disposition_wrong_type"),
        pytest.param("authorized_scope", ["Mutable."], id="mutable_scope"),
        pytest.param(
            "authorized_scope",
            (StringSubclass("Scope."),),
            id="scope_item_subclass",
        ),
    ),
)
def test_constructor__decision_fields__rejects_wrong_semantic_types(
    field: str, value: object
) -> None:
    """Evidence ID
    ``SV-HARNESS-169``.
    Requirement
    Decision fields reject wrong semantic types, while removed copied identity fields
    reject every representative historical value without a compatibility alias.
    Method
    Replace one current field with each wrong type or pass each removed identity field
    and historical partition through dataclass replacement.
    Oracle
    The public exact-type and accepted four-field contracts fix TypeError rejection.
    Acceptance
    Every partition raises TypeError before a decision is constructed.
    Interpretation
    Failure identifies permissive coercion or a stale copied-identity constructor field.
    Limitations
    Target identity remains available through ``decision.packet.target``.
    """
    with pytest.raises(TypeError):
        replace(make_decision(), **{field: value})  # type: ignore[arg-type]
