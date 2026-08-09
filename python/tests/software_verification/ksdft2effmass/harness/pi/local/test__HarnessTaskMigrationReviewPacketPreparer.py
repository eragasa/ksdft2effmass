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

import json
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


@pytest.mark.parametrize(
    "field,mutation",
    (
        pytest.param("path", "omit", id="omit_source_path"),
        pytest.param("revision", "omit", id="omit_source_revision"),
        pytest.param("git_object", "omit", id="omit_git_object"),
        pytest.param("byte_count", "omit", id="omit_byte_count"),
        pytest.param("artifact_identity", "omit", id="omit_artifact_identity"),
        pytest.param("path", "change", id="change_source_path"),
        pytest.param("revision", "change", id="change_source_revision"),
        pytest.param("git_object", "change", id="change_git_object"),
        pytest.param("byte_count", "change", id="change_byte_count"),
        pytest.param("artifact_identity", "change", id="change_artifact_identity"),
    ),
)
def test_method__source_observation__binds_complete_provenance(
    field: str, mutation: str
) -> None:
    """Evidence ID: ``SV-HT-057``.

    Requirement: The source observation binds path, revision, optional Git object,
    byte count, and SHA-256 identity, including explicit Git-object absence.

    Method: Independently omit or change each canonical detail field and also prepare
    one valid request whose Git object is ``None``.

    Oracle: The explicit source DataObject fields supply the complete exact provenance
    account; JSON ``null`` represents absent Git identity.

    Acceptance: The unchanged requests prepare; every omitted or changed field raises
    ``ValueError`` during packet preparation.

    Interpretation: Failure exposes source provenance that can drift without changing
    the human-facing packet.

    Limitations: Exact provenance binding does not establish provenance truth, semantic
    migration correctness, authority, or acceptance.
    """
    request = make_request(git_object=None)
    assert SUT().execute(request).request.source.git_object is None
    review = request.human_review_packet
    source_observation = next(
        item
        for item in review.observations
        if item.observation_id == "harness-task-migration.source"
    )
    detail = json.loads(source_observation.detail or "")
    assert detail["git_object"] is None
    if mutation == "omit":
        del detail[field]
    else:
        detail[field] = "changed" if field != "byte_count" else 999
    changed_observation = replace(
        source_observation,
        detail=json.dumps(
            detail, ensure_ascii=True, separators=(",", ":"), sort_keys=True
        ),
    )
    observations = tuple(
        changed_observation
        if item.observation_id == "harness-task-migration.source"
        else item
        for item in review.observations
    )
    changed_review = HumanReviewPreparer().execute(
        review.target, observations, review.findings, review.limitations
    )
    with pytest.raises(ValueError, match="observations"):
        SUT().execute(replace(request, human_review_packet=changed_review))


def test_method__source_observation__rejects_git_object_drift() -> None:
    """Evidence ID: ``SV-HT-058``.

    Requirement: Changing only the source Git object invalidates retained observations.

    Method: Replace the valid source DataObject with an equal object carrying another
    valid 40-character Git object while retaining the original review packet.

    Oracle: The source observation's explicit Git-object field must equal the source.

    Acceptance: Packet preparation raises ``ValueError`` for observation disagreement.

    Interpretation: Failure permits rollback provenance to drift after review material
    is prepared.

    Limitations: A lexical Git object is caller-supplied and is not repository-verified.
    """
    request = make_request()
    changed_source = replace(request.source, git_object="c" * 40)
    with pytest.raises(ValueError, match="observations"):
        SUT().execute(replace(request, source=changed_source))


@pytest.mark.parametrize(
    "partition",
    (
        pytest.param("review-id", id="stale_review_id"),
        pytest.param("subject", id="unrelated_subject"),
        pytest.param("evidence-class", id="wrong_evidence_class"),
        pytest.param("missing-contract", id="missing_contract_reference"),
        pytest.param("altered-contract", id="altered_contract_reference"),
        pytest.param("revision", id="stale_revision"),
        pytest.param("additional-path", id="additional_path"),
        pytest.param("missing-path", id="missing_path"),
    ),
)
def test_method__review_target__binds_exact_candidate_migration(partition: str) -> None:
    """Evidence ID: ``SV-HT-059``.

    Requirement: The generic target exactly identifies the candidate Task/file review,
    software-verification class, accepted contracts, source revision, and two paths.

    Method: Alter one target partition while retaining the complete validated internal
    migration bundle.

    Oracle: Candidate Task ID and paths derive the exact review ID and subject; the
    accepted contract paths and software-verification classification are fixed.

    Acceptance: Every unrelated, stale, additional, or missing target partition raises
    ``ValueError``.

    Interpretation: Failure permits a valid data bundle to be presented under another
    review target.

    Limitations: Target agreement does not authenticate a human or accept a migration.
    """
    request = make_request()
    review = request.human_review_packet
    target = review.target
    if partition == "review-id":
        changed_target = replace(target, review_id="harness-task-migration.stale")
    elif partition == "subject":
        changed_target = replace(target, represented_subject="Unrelated migration")
    elif partition == "evidence-class":
        changed_target = replace(target, evidence_class="not_applicable")
    elif partition == "missing-contract":
        changed_target = replace(
            target, contract_references=target.contract_references[:-1]
        )
    elif partition == "altered-contract":
        changed_target = replace(
            target,
            contract_references=target.contract_references[:-1]
            + ("records/unrelated-contract.md",),
        )
    elif partition == "revision":
        changed_target = replace(target, revision="c" * 40)
    elif partition == "additional-path":
        changed_target = replace(target, paths=target.paths + ("records/extra.md",))
    else:
        changed_target = replace(target, paths=(target.paths[1],))
    changed_review = replace(review, target=changed_target)
    with pytest.raises(ValueError):
        SUT().execute(replace(request, human_review_packet=changed_review))
