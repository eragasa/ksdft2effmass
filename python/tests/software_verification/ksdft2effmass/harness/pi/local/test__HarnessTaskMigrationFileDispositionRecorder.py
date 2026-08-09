r"""Software verification of ``HarnessTaskMigrationFileDispositionRecorder``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskMigrationFileDispositionRecorder``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.harness.pi import (
    HumanReviewDecision,
    HumanReviewDecisionRecorder,
    HumanReviewPreparer,
)
from ksdft2effmass.harness.pi.local import (
    HarnessTaskMigrationDisposition,
    HarnessTaskMigrationFileDispositionRecorder,
    HarnessTaskMigrationReviewPacket,
    HarnessTaskMigrationReviewPacketPreparer,
)

from .task_model_examples import make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskMigrationFileDispositionRecorder


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-019``.

    Requirement: The public ActionObject is fieldless, stateless, and can be
    constructed directly.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    assert SUT.__slots__ == ()
    assert type(SUT()) is SUT


def test_method__execute__rejects_wrong_public_types() -> None:
    """Evidence ID: ``SV-HT-049``.

    Requirement: Disposition recording fails before policy when exact public input
    types are wrong.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    with pytest.raises(TypeError, match="packet"):
        SUT().execute(object(), object(), object())  # type: ignore[arg-type]


def test_method__execute__revalidates_directly_constructed_packet() -> None:
    """Evidence ID: ``SV-HT-051``.

    Requirement: Disposition recording must reject a directly constructed migration
    packet whose retained request has not passed packet preparation.

    Method: Remove all required binding observations, directly construct the public
    packet, and attempt an otherwise compatible deferred disposition.

    Oracle: The public packet preparer is the accepted deterministic validator for the
    exact retained request.

    Acceptance: The recorder raises ``ValueError`` before returning a disposition.

    Interpretation: Failure exposes an unvalidated-packet disposition path.

    Limitations: The synthetic decision does not authenticate a person, persist a
    decision, authorize migration, or activate work.
    """
    request = make_request()
    review = request.human_review_packet
    incomplete_review = HumanReviewPreparer().execute(
        review.target, (), review.findings, review.limitations
    )
    incomplete_request = replace(request, human_review_packet=incomplete_review)
    direct_packet = HarnessTaskMigrationReviewPacket(incomplete_request)
    decision = HumanReviewDecision(
        incomplete_review, "Synthetic defer response", "deferred", ()
    )
    with pytest.raises(ValueError, match="observations"):
        SUT().execute(
            direct_packet,
            decision,
            HarnessTaskMigrationDisposition.DEFER_FILE,
        )


@pytest.mark.parametrize(
    "generic,migration",
    (
        pytest.param("accepted", "ACCEPT_FILE_MIGRATION", id="accept"),
        pytest.param("bounded_correction", "REVISE_CONTRACT_OR_MAPPING", id="revise"),
        pytest.param("rejected", "RETAIN_DOCUMENTATION_OWNERSHIP", id="retain"),
        pytest.param("deferred", "DEFER_FILE", id="defer"),
    ),
)
def test_method__decision_revalidation__accepts_all_canonical_dispositions(
    generic: str, migration: str
) -> None:
    """Evidence ID: ``SV-HT-060``.

    Requirement: The recorder reconstructs the generic decision publicly before
    applying every row of the migration-specific compatibility table.

    Method: Prepare one packet and use ``HumanReviewDecisionRecorder`` for all four
    generic dispositions before invoking the migration recorder.

    Oracle: The accepted four-row table fixes each exact disposition pair; only bounded
    correction carries one nonempty scope item.

    Acceptance: Every canonical pair returns a record retaining the exact packet,
    decision, response, and disposition.

    Interpretation: Failure identifies generic-decision or compatibility-table drift.

    Limitations: Synthetic responses do not authenticate a human or authorize work.
    """
    packet = HarnessTaskMigrationReviewPacketPreparer().execute(make_request())
    scope = ("Revise mappings.",) if generic == "bounded_correction" else ()
    decision = HumanReviewDecisionRecorder().execute(
        packet.request.human_review_packet,
        "Verbatim synthetic human response",
        generic,
        scope,
    )
    result = SUT().execute(packet, decision, HarnessTaskMigrationDisposition(migration))
    assert result.packet is packet
    assert result.human_decision == decision
    assert result.human_decision.human_response == "Verbatim synthetic human response"


def test_method__decision_revalidation__rejects_blocked_direct_acceptance() -> None:
    """Evidence ID: ``SV-HT-061``.

    Requirement: Direct construction cannot make a blocked generic packet acceptable.

    Method: Change one required observation to failed, directly construct its migration
    packet and an accepted decision, and invoke disposition recording.

    Oracle: Public packet preparation and ``HumanReviewDecisionRecorder`` both fail
    closed before an accepted migration result can be returned.

    Acceptance: The migration recorder raises ``ValueError``.

    Interpretation: Failure permits direct constructors to bypass a blocked review.

    Limitations: The first failing public validation boundary need not be distinguished.
    """
    request = make_request()
    review = request.human_review_packet
    observations = tuple(
        replace(item, status="failed")
        if item.observation_id == "harness-task-migration.comparison"
        else item
        for item in review.observations
    )
    blocked = HumanReviewPreparer().execute(
        review.target, observations, review.findings, review.limitations
    )
    direct_packet = HarnessTaskMigrationReviewPacket(
        replace(request, human_review_packet=blocked)
    )
    direct_decision = HumanReviewDecision(blocked, "Accept", "accepted", ())
    with pytest.raises(ValueError):
        SUT().execute(
            direct_packet,
            direct_decision,
            HarnessTaskMigrationDisposition.ACCEPT_FILE_MIGRATION,
        )


def test_method__decision_revalidation__rejects_scope_and_packet_substitution() -> None:
    """Evidence ID: ``SV-HT-062``.

    Requirement: Only bounded correction carries scope, and the exact review packet
    remains bound through generic and migration decision recording.

    Method: Ask the public generic recorder to attach scope to acceptance, then supply a
    canonical deferred decision for a different prepared packet.

    Oracle: ``HumanReviewDecisionRecorder`` owns scope compatibility and the migration
    recorder requires exact packet equality.

    Acceptance: Both independent invalid operations raise ``ValueError``.

    Interpretation: Failure permits incompatible scope or packet substitution.

    Limitations: Scope content is opaque and is not interpreted for meaning.
    """
    packet = HarnessTaskMigrationReviewPacketPreparer().execute(make_request())
    with pytest.raises(ValueError, match="authorized_scope"):
        HumanReviewDecisionRecorder().execute(
            packet.request.human_review_packet,
            "Accept",
            "accepted",
            ("Incompatible scope.",),
        )
    other_packet = HarnessTaskMigrationReviewPacketPreparer().execute(
        make_request(source_bytes=b"Different synthetic source.\n")
    )
    other_decision = HumanReviewDecisionRecorder().execute(
        other_packet.request.human_review_packet,
        "Defer other packet",
        "deferred",
        (),
    )
    with pytest.raises(ValueError, match="exact review packet"):
        SUT().execute(
            packet,
            other_decision,
            HarnessTaskMigrationDisposition.DEFER_FILE,
        )
