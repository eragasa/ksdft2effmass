r"""Software verification of ``HarnessTaskMigrationReviewPacketPreparer``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskMigrationReviewPacketPreparer``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.harness.pi import HumanReviewPacket, HumanReviewPreparer
from ksdft2effmass.harness.pi.local import (
    HarnessTaskMigrationReviewPacketPreparer,
    HarnessTaskMigrationReviewPacketRequest,
)

from .task_model_examples import identity, make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskMigrationReviewPacketPreparer


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-015``.

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


def test_method__agreement__rejects_identity_and_json_drift() -> None:
    """Evidence ID: ``SV-HT-046``.

    Requirement: Packet preparation recomputes span identities and canonical Task JSON.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    request = make_request()
    mapping = request.mappings[0]
    bad = type(mapping)(
        mapping.mapping_id,
        mapping.source_identity,
        mapping.start_byte,
        mapping.end_byte,
        identity(b"other"),
        mapping.disposition,
        mapping.target_references,
        mapping.transformation,
        mapping.rationale,
    )
    values = [getattr(request, name) for name in request.__dataclass_fields__]
    values[1] = (bad,)
    with pytest.raises(ValueError, match="span identity"):
        SUT().execute(type(request)(*values))
    values[1] = request.mappings
    values[3] = b"{}\n"
    with pytest.raises(ValueError, match="canonical_task_json"):
        SUT().execute(type(request)(*values))


def make_review_without_observation(
    request: HarnessTaskMigrationReviewPacketRequest, observation_id: str
) -> HumanReviewPacket:
    """Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: One named required observation can be removed independently.

    Method: Filter immutable observations by exact identifier and use the public
    generic preparer to restore canonical ordering and status.

    Oracle: Tuple filtering and exact identifier equality define the support result.

    Acceptance: The returned generic packet omits only the named observation.

    Interpretation: Failure identifies invalid support setup for packet-binding tests.

    Limitations: This helper makes no independent pass or human-acceptance claim.
    """
    review = request.human_review_packet
    observations = tuple(
        item for item in review.observations if item.observation_id != observation_id
    )
    return HumanReviewPreparer().execute(
        review.target, observations, review.findings, review.limitations
    )


@pytest.mark.parametrize(
    "partition",
    (
        pytest.param("empty", id="empty_observations"),
        pytest.param("source", id="missing_source_identity_and_byte_count"),
        pytest.param("candidate-json", id="missing_candidate_json_identity"),
        pytest.param("mappings", id="missing_mapping_and_unmapped_span_account"),
        pytest.param("rendered", id="missing_rendered_identity"),
        pytest.param("comparison", id="missing_comparison_result"),
        pytest.param("opaque-blocks", id="missing_opaque_block_preservation"),
        pytest.param("limitations", id="missing_applicable_limitations"),
        pytest.param("altered-comparison", id="altered_comparison_result"),
        pytest.param("stale-revision", id="stale_revision"),
        pytest.param("stale-path", id="stale_path"),
        pytest.param("different-candidate", id="observation_for_different_candidate"),
    ),
)
def test_method__packet_binding__rejects_incomplete_stale_or_unrelated_review(
    partition: str,
) -> None:
    """Evidence ID: ``SV-HT-050``.

    Requirement: Packet preparation requires an exact human-facing account of source
    identity and bytes, candidate JSON, mappings and unmapped spans, rendering,
    comparison, opaque blocks, limitations, revision, and paths.

    Method: Independently remove or alter one required immutable observation or target
    field in an otherwise valid explicit synthetic request.

    Oracle: The accepted packet boundary lists each required reviewed item and exact
    source, candidate, rendered, comparison, revision, and path identities.

    Acceptance: Every semantic partition raises ``ValueError`` while the unchanged
    request prepares successfully.

    Interpretation: Failure identifies a packet that can omit, stale, or substitute
    material while remaining dispositionable.

    Limitations: Synthetic bytes establish binding behavior only, not migration
    correctness, human authority, or acceptance.
    """
    request = make_request()
    review = request.human_review_packet
    assert type(SUT().execute(request)).__name__ == "HarnessTaskMigrationReviewPacket"
    if partition == "empty":
        changed_review = HumanReviewPreparer().execute(
            review.target, (), review.findings, review.limitations
        )
    elif partition in {
        "source",
        "candidate-json",
        "mappings",
        "rendered",
        "comparison",
        "opaque-blocks",
        "limitations",
    }:
        changed_review = make_review_without_observation(
            request, f"harness-task-migration.{partition}"
        )
    elif partition in {"altered-comparison", "different-candidate"}:
        observation_id = (
            "harness-task-migration.comparison"
            if partition == "altered-comparison"
            else "harness-task-migration.candidate-json"
        )
        observations = tuple(
            replace(item, detail='{"unrelated":true}')
            if item.observation_id == observation_id
            else item
            for item in review.observations
        )
        changed_review = HumanReviewPreparer().execute(
            review.target, observations, review.findings, review.limitations
        )
    elif partition == "stale-revision":
        changed_review = HumanReviewPreparer().execute(
            replace(review.target, revision="c" * 40),
            review.observations,
            review.findings,
            review.limitations,
        )
    else:
        changed_review = HumanReviewPreparer().execute(
            replace(review.target, paths=review.target.paths + ("records/stale.md",)),
            review.observations,
            review.findings,
            review.limitations,
        )
    with pytest.raises(ValueError):
        SUT().execute(replace(request, human_review_packet=changed_review))
