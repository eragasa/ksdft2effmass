r"""Software verification of ``HumanReviewPacket``.

Facet and represented meaning
Software verification of the immutable result prepared for direct human review.

Intrinsic and cross-object scope
The sole primary SUT is ``HumanReviewPacket``. Intrinsic result shape is covered;
cross-object compatibility and deterministic ordering belong to packet preparation.

VVUQ and scientific exclusions
Passing establishes only the stated software contract. A packet contains no human
disposition and establishes no numerical, scientific-validation, UQ, or acceptance
claim.
"""

from dataclasses import FrozenInstanceError, replace

import pytest

from ksdft2effmass.harness.pi import (
    HumanReviewFinding,
    HumanReviewObservation,
    HumanReviewPacket,
    HumanReviewTarget,
)

pytestmark = pytest.mark.software_verification
SUT = HumanReviewPacket


def make_components() -> tuple[
    HumanReviewTarget, HumanReviewObservation, HumanReviewFinding
]:
    """Evidence ID
    Owns no identifier; supports packet evidence.
    Requirement
    Packet tests require independently valid component records.
    Method
    Construct fixed target, observation, and finding values.
    Oracle
    Their accepted constructors define valid support input.
    Acceptance
    Return the three expected public object types.
    Interpretation
    Failure identifies setup drift.
    Limitations
    This helper owns no independent evidence claim.
    """
    target = HumanReviewTarget(
        "human-review.example",
        "a" * 40,
        "ExampleSubject",
        ("python/src/example.py",),
        "software_verification",
        (),
    )
    observation = HumanReviewObservation(
        "human-review.observation.tests",
        "pytest focused",
        "passed",
        "Focused tests passed.",
        "python/src/example.py",
    )
    finding = HumanReviewFinding(
        "human-review.finding.limit",
        "advisory",
        "Human review remains required.",
        None,
        (observation.observation_id,),
        "No human disposition has been recorded.",
    )
    return target, observation, finding


def make_packet() -> HumanReviewPacket:
    """Evidence ID
    Owns no identifier; supports packet evidence.
    Requirement
    Packet tests require one intrinsically valid result.
    Method
    Construct a packet from fixed support components.
    Oracle
    The accepted result constructor defines valid support input.
    Acceptance
    Return one HumanReviewPacket.
    Interpretation
    Failure identifies setup drift.
    Limitations
    This helper owns no independent evidence claim.
    """
    target, observation, finding = make_components()
    return SUT(
        target,
        (observation,),
        (finding,),
        ("Software verification does not establish human acceptance.",),
        "ready_for_human_review",
    )


def test_constructor__exact_result__owns_canonical_tuple_fields() -> None:
    """Evidence ID
    ``SV-HARNESS-138``.
    Requirement
    A packet stores exact component types and defensively owns immutable tuples.
    Method
    Construct a complete result and inspect public values, types, and tuple identity.
    Oracle
    The accepted result-field contract and built-in tuple semantics are exact.
    Acceptance
    Components are unchanged and all collection fields are separately owned tuples.
    Interpretation
    Failure identifies result mapping or immutable ownership drift.
    Limitations
    Direct construction does not perform preparation compatibility checks.
    """
    target, observation, finding = make_components()
    observations = (observation,)
    findings = (finding,)
    limitations = ("Software verification does not establish human acceptance.",)
    packet = SUT(
        target,
        observations,
        findings,
        limitations,
        "ready_for_human_review",
    )
    assert packet == make_packet()
    assert packet.target is target
    assert type(packet.observations) is tuple
    assert type(packet.findings) is tuple
    assert type(packet.limitations) is tuple
    assert packet.observations is not observations
    assert packet.findings is not findings
    assert packet.limitations is not limitations


def test_field__immutability__has_exact_value_semantics() -> None:
    """Evidence ID
    ``SV-HARNESS-139``.
    Requirement
    Packet result state is frozen with exact dataclass equality.
    Method
    Compare independently constructed packets and attempt status mutation.
    Oracle
    Frozen dataclass semantics are exact.
    Acceptance
    Packets compare equal and mutation raises FrozenInstanceError.
    Interpretation
    Failure identifies result mutability or equality drift.
    Limitations
    Persistence and serialization are excluded.
    """
    first = make_packet()
    assert first == make_packet()
    with pytest.raises(FrozenInstanceError):
        first.status = "blocked_by_failed_observation"  # type: ignore[misc]


@pytest.mark.parametrize(
    "status",
    (
        pytest.param("ready_for_human_review", id="ready_for_human_review"),
        pytest.param(
            "blocked_by_failed_observation", id="blocked_by_failed_observation"
        ),
    ),
)
def test_constructor__status__accepts_closed_vocabulary(status: str) -> None:
    """Evidence ID
    ``SV-HARNESS-140``.
    Requirement
    Packet status accepts both and only the declared preparation statuses.
    Method
    Replace one valid result status with each declared member.
    Oracle
    The public two-value vocabulary supplies exact expected strings.
    Acceptance
    Both declared values are retained exactly.
    Interpretation
    Failure identifies packet-status drift.
    Limitations
    Neither status is human acceptance.
    """
    assert replace(make_packet(), status=status).status == status


@pytest.mark.parametrize(
    ("field", "value", "exception"),
    (
        pytest.param("target", object(), TypeError, id="wrong_target"),
        pytest.param(
            "observations", (object(),), TypeError, id="wrong_observation_member"
        ),
        pytest.param("findings", (object(),), TypeError, id="wrong_finding_member"),
        pytest.param("limitations", (" ",), ValueError, id="blank_limitation"),
        pytest.param("status", "PASS", ValueError, id="acceptance_like_status"),
        pytest.param("observations", [], TypeError, id="mutable_observation_container"),
    ),
)
def test_constructor__result_fields__rejects_invalid_partitions(
    field: str, value: object, exception: type[Exception]
) -> None:
    """Evidence ID
    ``SV-HARNESS-141``.
    Requirement
    Packet result fields reject wrong object types, mutable containers, blank text,
    and status values outside the closed vocabulary.
    Method
    Replace one field of a valid packet with each malformed semantic partition.
    Oracle
    Public exact-type and vocabulary contracts fix the exception taxonomy.
    Acceptance
    Every partition raises the specified exception.
    Interpretation
    Failure identifies intrinsic result validation drift.
    Limitations
    Cross-object relationship failures belong to HumanReviewPreparer.
    """
    with pytest.raises(exception):
        replace(make_packet(), **{field: value})  # type: ignore[arg-type]


def test_field__authority_boundary__stores_no_human_decision_or_recommendation() -> (
    None
):
    """Evidence ID
    ``SV-HARNESS-142``.
    Requirement
    The packet public state contains no human decision, disposition, or recommendation.
    Method
    Compare exact dataclass field names with the accepted five-field result contract.
    Oracle
    The authorized packet contract supplies the complete public field set.
    Acceptance
    Fields are exactly target, observations, findings, limitations, and status.
    Interpretation
    Failure identifies unauthorized expansion into human authority.
    Limitations
    Static field agreement does not record a human review outcome.
    """
    assert tuple(make_packet().__dataclass_fields__) == (
        "target",
        "observations",
        "findings",
        "limitations",
        "status",
    )
