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

from ksdft2effmass.harness.pi import HumanReviewDecision, HumanReviewPreparer
from ksdft2effmass.harness.pi.local import (
    HarnessTaskMigrationDisposition,
    HarnessTaskMigrationFileDispositionRecorder,
    HarnessTaskMigrationReviewPacket,
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
