r"""Software verification of development-prerequisite-resolution.

Evidence profile: routine

Bounded artifact scope: consumer sidecar requirements, owner-retained observations,
closed per-edge outcomes, aggregate blocking, and public import behavior.

Facet and represented meaning

The artifact represents explicit development prerequisite matching without lifecycle
status inference or operation authority.

Intrinsic and cross-object scope

Tests cover immutable record invariants and resolver agreement among an exact Task,
its content-bound contract, and explicit owner observations.

VVUQ and scientific exclusions

This is software verification only. It establishes no authority, protected execution,
scientific validation, numerical verification, uncertainty quantification, or human
acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness import (
    ContentIdentity,
    DevelopmentPrerequisiteAggregateStatus,
    DevelopmentPrerequisiteContract,
    DevelopmentPrerequisiteEdgeResult,
    DevelopmentPrerequisiteKind,
    DevelopmentPrerequisiteLineage,
    DevelopmentPrerequisiteLineagePolicy,
    DevelopmentPrerequisiteObservationStatus,
    DevelopmentPrerequisiteOutcome,
    DevelopmentPrerequisiteRequirement,
    DevelopmentPrerequisiteResolutionResult,
    DevelopmentPrerequisiteResolver,
    HarnessTask,
    RetainedPrerequisiteObservation,
    RetainedPrerequisiteResultReference,
)

pytestmark = pytest.mark.software_verification


def content(digit: str = "a") -> ContentIdentity:
    """Construct one exact SHA-256 content identity for test setup.

    Evidence ID: Owns no identifier; supports the module evidence owners.

    Requirement: Test setup uses valid independent exact content identities.

    Acceptance: Return a version-1 SHA-256 identity using the requested digest digit.
    """
    return ContentIdentity(1, "sha256", digit * 64)


def task(status: str = "active") -> HarnessTask:
    """Construct one consumer with distinct Task and external edges.

    Evidence ID: Owns no identifier; supports the module evidence owners.

    Requirement: Test setup distinguishes Task and external declarations.

    Acceptance: Return one intrinsically valid Task with one edge of each kind.
    """
    return HarnessTask(
        3,
        "consumer.task",
        "Consumer",
        status,
        None,
        None,
        ("producer.task",),
        ("external.event",),
        (),
        True,
        "Consume exact results.",
        ("docs/contract.md",),
        ("Resolve explicit prerequisites.",),
        ("Every edge is satisfied.",),
        ("No authority.",),
        None,
    )


def requirement(
    kind: DevelopmentPrerequisiteKind, identifier: str
) -> DevelopmentPrerequisiteRequirement:
    """Construct the accepted exact matching requirement for one edge.

    Evidence ID: Owns no identifier; supports the module evidence owners.

    Requirement: Setup binds every matching dimension to fixed independent values.

    Acceptance: Return one valid requirement for the requested kind and identity.
    """
    return DevelopmentPrerequisiteRequirement(
        1,
        kind,
        identifier,
        "owner.domain",
        "verified.result",
        "claim.complete",
        "revision.one",
        "retention.repository",
        DevelopmentPrerequisiteLineagePolicy.EFFECTIVE_NOT_REVOKED,
    )


def contract(
    task_identity: ContentIdentity | None = None,
) -> DevelopmentPrerequisiteContract:
    """Construct complete requirements in canonical edge-key order.

    Evidence ID: Owns no identifier; supports the module evidence owners.

    Requirement: Setup covers both declared edges and exact Task content.

    Acceptance: Return a valid sidecar with external then Task edge ordering.
    """
    return DevelopmentPrerequisiteContract(
        1,
        "contract.consumer.v1",
        "consumer.task",
        content() if task_identity is None else task_identity,
        (
            requirement(DevelopmentPrerequisiteKind.EXTERNAL, "external.event"),
            requirement(DevelopmentPrerequisiteKind.TASK, "producer.task"),
        ),
    )


def reference(
    kind: DevelopmentPrerequisiteKind,
    identifier: str,
    lineage: DevelopmentPrerequisiteLineage = DevelopmentPrerequisiteLineage.EFFECTIVE,
    *,
    owner_id: str = "owner.domain",
    result_id: str = "result.one",
    result_kind: str = "verified.result",
    claim_id: str = "claim.complete",
    producer_revision_id: str = "revision.one",
    retention_boundary_id: str = "retention.repository",
) -> RetainedPrerequisiteResultReference:
    """Construct one exact owner-retained reference with configurable bindings.

    Evidence ID: Owns no identifier; supports the module evidence owners.

    Requirement: Setup independently varies matching fields while preserving valid
    lineage-specific companion identities.

    Acceptance: Return a valid exact reference for the requested field partition.
    """
    return RetainedPrerequisiteResultReference(
        1,
        kind,
        identifier,
        owner_id,
        result_id,
        result_kind,
        claim_id,
        producer_revision_id,
        retention_boundary_id,
        content("b"),
        lineage,
        "result.successor"
        if lineage is DevelopmentPrerequisiteLineage.SUPERSEDED
        else None,
        "revocation.one" if lineage is DevelopmentPrerequisiteLineage.REVOKED else None,
    )


def found(
    kind: DevelopmentPrerequisiteKind,
    identifier: str,
    *items: RetainedPrerequisiteResultReference,
    owner_id: str = "owner.domain",
    retention_boundary_id: str = "retention.repository",
) -> RetainedPrerequisiteObservation:
    """Construct one complete owner-bound found observation for an edge.

    Evidence ID: Owns no identifier; supports the module evidence owners.

    Requirement: A found observation binds owner and retention, contains explicit
    references, and contains no diagnostic.

    Acceptance: Return the valid represented observation.
    """
    return RetainedPrerequisiteObservation(
        1,
        kind,
        identifier,
        owner_id,
        retention_boundary_id,
        DevelopmentPrerequisiteObservationStatus.FOUND,
        tuple(items),
        None,
    )


def effective_observations() -> tuple[RetainedPrerequisiteObservation, ...]:
    """Return complete satisfying observations for both declared edges.

    Evidence ID: Owns no identifier; supports the module evidence owners.

    Requirement: Satisfying setup provides one effective result per edge.

    Acceptance: Return canonically ordered external and Task observations.
    """
    return (
        found(
            DevelopmentPrerequisiteKind.EXTERNAL,
            "external.event",
            reference(
                DevelopmentPrerequisiteKind.EXTERNAL,
                "external.event",
                result_id="result.external",
            ),
        ),
        found(
            DevelopmentPrerequisiteKind.TASK,
            "producer.task",
            reference(
                DevelopmentPrerequisiteKind.TASK,
                "producer.task",
                result_id="result.task",
            ),
        ),
    )


def test_artifact__construction__enforces_immutability_and_lineage_fields() -> None:
    """Public records are immutable and lineage fields are closed.

    Evidence ID: SV-PREREQ-001

    Requirement: Sidecar and retained-reference state is immutable, with exactly the
    lineage-specific supersession or revocation identity.

    Acceptance: Mutation and an effective reference carrying a successor both fail.
    """
    value = contract()
    with pytest.raises(FrozenInstanceError):
        value.contract_id = "changed"  # type: ignore[misc]
    with pytest.raises(ValueError, match="lineage requires"):
        RetainedPrerequisiteResultReference(
            1,
            DevelopmentPrerequisiteKind.TASK,
            "producer.task",
            "owner.domain",
            "result.one",
            "verified.result",
            "claim.complete",
            "revision.one",
            "retention.repository",
            content(),
            DevelopmentPrerequisiteLineage.EFFECTIVE,
            "result.two",
            None,
        )


def test_artifact__resolution__satisfies_only_complete_exact_edge_coverage() -> None:
    """Every declared edge requires one exact effective owner result.

    Evidence ID: SV-PREREQ-002

    Requirement: Aggregate satisfaction requires exact Task binding, complete
    one-to-one edge coverage, and one effective matching result per edge.

    Acceptance: Both edge outcomes and the aggregate are exactly satisfied.
    """
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(), effective_observations()
    )
    assert result.status is DevelopmentPrerequisiteAggregateStatus.SATISFIED
    assert result.is_satisfied
    assert tuple(
        (item.prerequisite_kind.value, item.prerequisite_id)
        for item in result.edge_results
    ) == (("external", "external.event"), ("task", "producer.task"))
    assert tuple(item.outcome for item in result.edge_results) == (
        DevelopmentPrerequisiteOutcome.SATISFIED,
        DevelopmentPrerequisiteOutcome.SATISFIED,
    )
    assert tuple(item.matched_result_id for item in result.edge_results) == (
        "result.external",
        "result.task",
    )
    assert result.diagnostic_ids == ()


@pytest.mark.parametrize(
    ("status", "diagnostic", "expected"),
    (
        pytest.param(
            DevelopmentPrerequisiteObservationStatus.ABSENT,
            None,
            DevelopmentPrerequisiteOutcome.MISSING,
            id="complete_absence_is_missing",
        ),
        pytest.param(
            DevelopmentPrerequisiteObservationStatus.UNAVAILABLE,
            "owner.unavailable",
            DevelopmentPrerequisiteOutcome.UNAVAILABLE,
            id="identified_inaccessible_is_unavailable",
        ),
        pytest.param(
            DevelopmentPrerequisiteObservationStatus.INDETERMINATE,
            "owner.indeterminate",
            DevelopmentPrerequisiteOutcome.INDETERMINATE,
            id="uncertain_observation_is_indeterminate",
        ),
    ),
)
def test_artifact__resolution__preserves_observation_failure_meaning(
    status: DevelopmentPrerequisiteObservationStatus,
    diagnostic: str | None,
    expected: DevelopmentPrerequisiteOutcome,
) -> None:
    """Absent, unavailable, and indeterminate observations remain distinct.

    Evidence ID: SV-PREREQ-003

    Requirement: A complete absence is missing, identified inaccessibility is
    unavailable, and failed observation or integrity is indeterminate.

    Acceptance: The Task edge returns the parameterized exact outcome and blocks the
    aggregate without changing the satisfying external edge.
    """
    external, _task_observation = effective_observations()
    represented = RetainedPrerequisiteObservation(
        1,
        DevelopmentPrerequisiteKind.TASK,
        "producer.task",
        "owner.domain",
        "retention.repository",
        status,
        (),
        diagnostic,
    )
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(), (external, represented)
    )
    assert result.status is DevelopmentPrerequisiteAggregateStatus.BLOCKED
    assert result.edge_results[0].matched_result_id == "result.external"
    assert result.edge_results[1].outcome is expected
    assert result.edge_results[1].diagnostic_ids == (
        () if diagnostic is None else (diagnostic,)
    )
    assert result.diagnostic_ids == ()


@pytest.mark.parametrize(
    ("lineages", "expected"),
    (
        pytest.param(
            (DevelopmentPrerequisiteLineage.SUPERSEDED,),
            DevelopmentPrerequisiteOutcome.SUPERSEDED,
            id="only_superseded_result",
        ),
        pytest.param(
            (DevelopmentPrerequisiteLineage.REVOKED,),
            DevelopmentPrerequisiteOutcome.REVOKED,
            id="only_revoked_result",
        ),
        pytest.param(
            (
                DevelopmentPrerequisiteLineage.SUPERSEDED,
                DevelopmentPrerequisiteLineage.REVOKED,
            ),
            DevelopmentPrerequisiteOutcome.CONFLICTING,
            id="contradictory_stale_lineage",
        ),
    ),
)
def test_artifact__resolution__preserves_owner_reported_lineage(
    lineages: tuple[DevelopmentPrerequisiteLineage, ...],
    expected: DevelopmentPrerequisiteOutcome,
) -> None:
    """Supersession, revocation, and contradictory lineage remain distinct.

    Evidence ID: SV-PREREQ-004

    Requirement: Owner-reported non-effective lineage is not treated as completion.

    Acceptance: The exact expected stale or conflicting outcome is returned.
    """
    external, _ = effective_observations()
    refs = tuple(
        reference(
            DevelopmentPrerequisiteKind.TASK,
            "producer.task",
            item,
            result_id=f"result.{item.value}",
        )
        for item in lineages
    )
    represented = found(DevelopmentPrerequisiteKind.TASK, "producer.task", *refs)
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(), (external, represented)
    )
    assert result.edge_results[1].outcome is expected
    expected_diagnostic = {
        DevelopmentPrerequisiteOutcome.SUPERSEDED: "prerequisite.result.superseded",
        DevelopmentPrerequisiteOutcome.REVOKED: "prerequisite.result.revoked",
        DevelopmentPrerequisiteOutcome.CONFLICTING: (
            "prerequisite.result.lineage-conflict"
        ),
    }[expected]
    assert result.edge_results[1].diagnostic_ids == (expected_diagnostic,)


def test_artifact__resolution__multiple_effective_candidates_conflict() -> None:
    """Multiple effective matches cannot satisfy one edge.

    Evidence ID: SV-PREREQ-005

    Requirement: One edge has exactly one effective matching owner result.

    Acceptance: Two distinct effective results produce ``conflicting`` and no matched
    result identity.
    """
    external, _ = effective_observations()
    represented = found(
        DevelopmentPrerequisiteKind.TASK,
        "producer.task",
        reference(
            DevelopmentPrerequisiteKind.TASK, "producer.task", result_id="result.one"
        ),
        reference(
            DevelopmentPrerequisiteKind.TASK, "producer.task", result_id="result.two"
        ),
    )
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(), (external, represented)
    )
    assert result.edge_results[1].outcome is DevelopmentPrerequisiteOutcome.CONFLICTING
    assert result.edge_results[1].matched_result_id is None
    assert result.edge_results[1].diagnostic_ids == (
        "prerequisite.result.multiple-effective",
    )


def test_artifact__resolution__fails_closed_for_stale_task_binding() -> None:
    """A sidecar bound to different Task bytes cannot satisfy any edge.

    Evidence ID: SV-PREREQ-006

    Requirement: The consumer contract binds to the exact supplied Task content
    identity, independently of matching Task ID or lifecycle status.

    Acceptance: Every edge is indeterminate and the aggregate identifies the content
    mismatch.
    """
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(content("c")), effective_observations()
    )
    assert not result.is_satisfied
    assert {item.outcome for item in result.edge_results} == {
        DevelopmentPrerequisiteOutcome.INDETERMINATE
    }
    assert tuple(item.diagnostic_ids for item in result.edge_results) == (
        ("prerequisite.contract.invalid",),
        ("prerequisite.contract.invalid",),
    )
    assert result.diagnostic_ids == ("prerequisite.contract.task-content-mismatch",)


def test_artifact__resolution__fails_closed_for_wrong_consumer_task_id() -> None:
    """A sidecar bound to another consumer Task cannot satisfy any edge.

    Evidence ID: SV-PREREQ-020

    Requirement: The consumer contract binds to the exact supplied Task identity as
    well as its content identity.

    Acceptance: Every edge is indeterminate and the aggregate retains only the exact
    Task-ID mismatch diagnostic.
    """
    wrong_consumer = DevelopmentPrerequisiteContract(
        1,
        "contract.other.v1",
        "consumer.other",
        content(),
        contract().requirements,
    )
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), wrong_consumer, effective_observations()
    )
    assert tuple(item.outcome for item in result.edge_results) == (
        DevelopmentPrerequisiteOutcome.INDETERMINATE,
        DevelopmentPrerequisiteOutcome.INDETERMINATE,
    )
    assert result.diagnostic_ids == ("prerequisite.contract.task-id-mismatch",)


def test_artifact__resolution__invalid_contract_coverage_fails_closed() -> None:
    """A sidecar must cover every canonical edge exactly once.

    Evidence ID: SV-PREREQ-007

    Requirement: Incomplete contract coverage is a contract failure, not evidence that
    an owner observed a missing result.

    Acceptance: Every declared edge is indeterminate and the exact aggregate coverage
    diagnostic is retained.
    """
    incomplete = DevelopmentPrerequisiteContract(
        1,
        "contract.incomplete",
        "consumer.task",
        content(),
        (requirement(DevelopmentPrerequisiteKind.TASK, "producer.task"),),
    )
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), incomplete, effective_observations()
    )
    assert tuple(item.outcome for item in result.edge_results) == (
        DevelopmentPrerequisiteOutcome.INDETERMINATE,
        DevelopmentPrerequisiteOutcome.INDETERMINATE,
    )
    assert result.diagnostic_ids == ("prerequisite.contract.edge-coverage-mismatch",)


def test_public_api__package__exports_exact_prerequisite_contract() -> None:
    """The supported package exports the exact accepted prerequisite contract.

    Evidence ID: SV-PREREQ-008

    Requirement: The prerequisite public inventory contains exactly the accepted
    enums, immutable records, ResultObjects, and resolver in stable package order.

    Acceptance: The literal prerequisite slice of ``__all__`` agrees exactly.
    """
    import ksdft2effmass.harness as harness

    assert harness.__all__[26:39] == (
        "DevelopmentPrerequisiteKind",
        "DevelopmentPrerequisiteLineage",
        "DevelopmentPrerequisiteLineagePolicy",
        "DevelopmentPrerequisiteObservationStatus",
        "DevelopmentPrerequisiteOutcome",
        "DevelopmentPrerequisiteAggregateStatus",
        "DevelopmentPrerequisiteRequirement",
        "DevelopmentPrerequisiteContract",
        "RetainedPrerequisiteResultReference",
        "RetainedPrerequisiteObservation",
        "DevelopmentPrerequisiteEdgeResult",
        "DevelopmentPrerequisiteResolutionResult",
        "DevelopmentPrerequisiteResolver",
    )


def test_artifact__resolution__undeclared_observation_blocks_aggregate() -> None:
    """An undeclared observation cannot coexist with aggregate satisfaction.

    Evidence ID: SV-PREREQ-009

    Requirement: Aggregate satisfaction requires satisfied declared edges and no
    blocking aggregate diagnostic.

    Acceptance: Declared edges retain their exact matches, but the aggregate is blocked
    by the exact undeclared-edge diagnostic; an inconsistent ResultObject is rejected.
    """
    extra = found(
        DevelopmentPrerequisiteKind.EXTERNAL,
        "undeclared.event",
        reference(DevelopmentPrerequisiteKind.EXTERNAL, "undeclared.event"),
    )
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(), (*effective_observations(), extra)
    )
    assert tuple(item.matched_result_id for item in result.edge_results) == (
        "result.external",
        "result.task",
    )
    assert result.status is DevelopmentPrerequisiteAggregateStatus.BLOCKED
    assert result.diagnostic_ids == ("prerequisite.observation.undeclared-edge",)
    with pytest.raises(ValueError, match="aggregate status"):
        DevelopmentPrerequisiteResolutionResult(
            result.consumer_task_id,
            result.consumer_task_content_identity,
            result.contract_id,
            DevelopmentPrerequisiteAggregateStatus.SATISFIED,
            result.edge_results,
            result.diagnostic_ids,
        )


@pytest.mark.parametrize(
    ("status", "diagnostic", "owner_id", "retention_boundary_id"),
    (
        pytest.param(
            DevelopmentPrerequisiteObservationStatus.ABSENT,
            None,
            "owner.other",
            "retention.repository",
            id="absent_owner_mismatch",
        ),
        pytest.param(
            DevelopmentPrerequisiteObservationStatus.ABSENT,
            None,
            "owner.domain",
            "retention.other",
            id="absent_retention_mismatch",
        ),
        pytest.param(
            DevelopmentPrerequisiteObservationStatus.UNAVAILABLE,
            "owner.unavailable",
            "owner.other",
            "retention.repository",
            id="unavailable_owner_mismatch",
        ),
        pytest.param(
            DevelopmentPrerequisiteObservationStatus.UNAVAILABLE,
            "owner.unavailable",
            "owner.domain",
            "retention.other",
            id="unavailable_retention_mismatch",
        ),
        pytest.param(
            DevelopmentPrerequisiteObservationStatus.INDETERMINATE,
            "owner.indeterminate",
            "owner.other",
            "retention.repository",
            id="indeterminate_owner_mismatch",
        ),
        pytest.param(
            DevelopmentPrerequisiteObservationStatus.INDETERMINATE,
            "owner.indeterminate",
            "owner.domain",
            "retention.other",
            id="indeterminate_retention_mismatch",
        ),
    ),
)
def test_artifact__resolution__negative_observation_binding_mismatch(
    status: DevelopmentPrerequisiteObservationStatus,
    diagnostic: str | None,
    owner_id: str,
    retention_boundary_id: str,
) -> None:
    """Negative observations remain bound to the required owner and retention.

    Evidence ID: SV-PREREQ-010

    Requirement: Absent, unavailable, and indeterminate claims cannot be accepted from
    a different owner or retention boundary.

    Acceptance: Every mismatched negative status is indeterminate with the exact
    observation-binding diagnostic.
    """
    external, _ = effective_observations()
    negative = RetainedPrerequisiteObservation(
        1,
        DevelopmentPrerequisiteKind.TASK,
        "producer.task",
        owner_id,
        retention_boundary_id,
        status,
        (),
        diagnostic,
    )
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(), (external, negative)
    )
    assert (
        result.edge_results[1].outcome is DevelopmentPrerequisiteOutcome.INDETERMINATE
    )
    assert result.edge_results[1].diagnostic_ids == (
        "prerequisite.observation.binding-mismatch",
    )


@pytest.mark.parametrize(
    ("owner_id", "retention_boundary_id"),
    (
        pytest.param("owner.other", "retention.repository", id="found_owner_mismatch"),
        pytest.param("owner.domain", "retention.other", id="found_retention_mismatch"),
    ),
)
def test_artifact__resolution__found_observation_binding_mismatch(
    owner_id: str, retention_boundary_id: str
) -> None:
    """Found observations remain bound independently of their references.

    Evidence ID: SV-PREREQ-011

    Requirement: A matching reference cannot satisfy an observation made by the wrong
    owner or against the wrong retention boundary.

    Acceptance: The edge is indeterminate with the exact observation diagnostic.
    """
    external, task_observation = effective_observations()
    found_mismatch = found(
        DevelopmentPrerequisiteKind.TASK,
        "producer.task",
        *task_observation.references,
        owner_id=owner_id,
        retention_boundary_id=retention_boundary_id,
    )
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(), (external, found_mismatch)
    )
    assert (
        result.edge_results[1].outcome is DevelopmentPrerequisiteOutcome.INDETERMINATE
    )
    assert result.edge_results[1].diagnostic_ids == (
        "prerequisite.observation.binding-mismatch",
    )


def mismatched_reference(case: str) -> RetainedPrerequisiteResultReference:
    """Vary exactly one owner-result binding field for a semantic partition.

    Evidence ID: Owns no identifier; supports SV-PREREQ-012.

    Requirement: Each case changes one resolver-compared field independently.

    Acceptance: Return one intrinsically valid but requirement-mismatched reference.
    """
    if case == "kind":
        return reference(DevelopmentPrerequisiteKind.EXTERNAL, "producer.task")
    if case == "prerequisite_id":
        return reference(DevelopmentPrerequisiteKind.TASK, "producer.other")
    if case == "owner_id":
        return reference(
            DevelopmentPrerequisiteKind.TASK,
            "producer.task",
            owner_id="owner.other",
        )
    if case == "result_kind":
        return reference(
            DevelopmentPrerequisiteKind.TASK,
            "producer.task",
            result_kind="unverified.result",
        )
    if case == "claim_id":
        return reference(
            DevelopmentPrerequisiteKind.TASK,
            "producer.task",
            claim_id="claim.other",
        )
    if case == "producer_revision_id":
        return reference(
            DevelopmentPrerequisiteKind.TASK,
            "producer.task",
            producer_revision_id="revision.other",
        )
    return reference(
        DevelopmentPrerequisiteKind.TASK,
        "producer.task",
        retention_boundary_id="retention.other",
    )


@pytest.mark.parametrize(
    "case",
    (
        pytest.param("kind", id="prerequisite_kind"),
        pytest.param("prerequisite_id", id="prerequisite_identity"),
        pytest.param("owner_id", id="owner_identity"),
        pytest.param("result_kind", id="result_kind"),
        pytest.param("claim_id", id="claim_identity"),
        pytest.param("producer_revision_id", id="producer_revision"),
        pytest.param("retention_boundary_id", id="retention_boundary"),
    ),
)
def test_artifact__resolution__independently_checks_result_bindings(case: str) -> None:
    """Every result-binding dimension is matched independently.

    Evidence ID: SV-PREREQ-012

    Requirement: Kind, edge identity, owner, result kind, claim, producer revision,
    and retention boundary must all match the requirement and observation.

    Acceptance: Each one-field mismatch is indeterminate with the exact result-binding
    diagnostic.
    """
    external, _ = effective_observations()
    represented = found(
        DevelopmentPrerequisiteKind.TASK,
        "producer.task",
        mismatched_reference(case),
    )
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(), (external, represented)
    )
    assert (
        result.edge_results[1].outcome is DevelopmentPrerequisiteOutcome.INDETERMINATE
    )
    assert result.edge_results[1].diagnostic_ids == (
        "prerequisite.result.binding-mismatch",
    )


def test_artifact__resolution__duplicate_result_identity_conflicts() -> None:
    """Duplicate result identities do not count as distinct effective candidates.

    Evidence ID: SV-PREREQ-013

    Requirement: Owner observations contain unique retained result identities.

    Acceptance: Repeating one result identity produces the exact conflict diagnostic.
    """
    external, _ = effective_observations()
    represented = found(
        DevelopmentPrerequisiteKind.TASK,
        "producer.task",
        reference(DevelopmentPrerequisiteKind.TASK, "producer.task"),
        reference(DevelopmentPrerequisiteKind.TASK, "producer.task"),
    )
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(), (external, represented)
    )
    assert result.edge_results[1].outcome is DevelopmentPrerequisiteOutcome.CONFLICTING
    assert result.edge_results[1].diagnostic_ids == (
        "prerequisite.result.duplicate-identity",
    )


def test_artifact__resolution__missing_observation_is_indeterminate() -> None:
    """Omitted observation is not a complete owner absence claim.

    Evidence ID: SV-PREREQ-014

    Requirement: Every declared edge has exactly one explicit observation.

    Acceptance: The omitted Task observation is indeterminate with the exact missing
    observation diagnostic.
    """
    external, _ = effective_observations()
    result = DevelopmentPrerequisiteResolver().execute(
        task(), content(), contract(), (external,)
    )
    assert (
        result.edge_results[1].outcome is DevelopmentPrerequisiteOutcome.INDETERMINATE
    )
    assert result.edge_results[1].diagnostic_ids == (
        "prerequisite.observation.missing",
    )


def test_artifact__resolution__duplicate_observation_conflicts() -> None:
    """Multiple observations for one edge are contradictory inputs.

    Evidence ID: SV-PREREQ-015

    Requirement: Every declared edge has exactly one explicit observation.

    Acceptance: Duplicate Task observations conflict with the exact diagnostic.
    """
    external, task_observation = effective_observations()
    result = DevelopmentPrerequisiteResolver().execute(
        task(),
        content(),
        contract(),
        (external, task_observation, task_observation),
    )
    assert result.edge_results[1].outcome is DevelopmentPrerequisiteOutcome.CONFLICTING
    assert result.edge_results[1].diagnostic_ids == (
        "prerequisite.observation.duplicate",
    )


@pytest.mark.parametrize(
    "status",
    (
        pytest.param("planning", id="planning_status"),
        pytest.param("implementation_active", id="active_status"),
        pytest.param("completed", id="completed_status"),
    ),
)
def test_artifact__resolution__ignores_opaque_lifecycle_status(status: str) -> None:
    """Opaque lifecycle spelling cannot satisfy or block a prerequisite.

    Evidence ID: SV-PREREQ-016

    Requirement: Resolution depends only on exact contract and owner observations.

    Acceptance: Identical explicit inputs produce identical satisfied results for every
    representative Task status spelling.
    """
    result = DevelopmentPrerequisiteResolver().execute(
        task(status), content(), contract(), effective_observations()
    )
    assert result.is_satisfied
    assert tuple(item.matched_result_id for item in result.edge_results) == (
        "result.external",
        "result.task",
    )


def test_artifact__requirement__accepts_only_effective_not_revoked_policy() -> None:
    """The sidecar exposes one closed accepted lineage policy.

    Evidence ID: SV-PREREQ-017

    Requirement: Requirements explicitly select ``effective_not_revoked`` and expose
    no string coercion or alternate policy.

    Acceptance: The helper requirement contains the exact enum; a raw string fails the
    exact semantic type contract.
    """
    assert (
        requirement(DevelopmentPrerequisiteKind.TASK, "producer.task").lineage_policy
        is DevelopmentPrerequisiteLineagePolicy.EFFECTIVE_NOT_REVOKED
    )
    with pytest.raises(TypeError, match="lineage_policy"):
        DevelopmentPrerequisiteRequirement(
            1,
            DevelopmentPrerequisiteKind.TASK,
            "producer.task",
            "owner.domain",
            "verified.result",
            "claim.complete",
            "revision.one",
            "retention.repository",
            "effective_not_revoked",  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("lineage", "successor", "revocation", "valid"),
    (
        pytest.param(
            DevelopmentPrerequisiteLineage.EFFECTIVE,
            None,
            None,
            True,
            id="effective_has_no_companion",
        ),
        pytest.param(
            DevelopmentPrerequisiteLineage.EFFECTIVE,
            "result.next",
            None,
            False,
            id="effective_rejects_successor",
        ),
        pytest.param(
            DevelopmentPrerequisiteLineage.SUPERSEDED,
            "result.next",
            None,
            True,
            id="superseded_requires_successor",
        ),
        pytest.param(
            DevelopmentPrerequisiteLineage.SUPERSEDED,
            None,
            None,
            False,
            id="superseded_rejects_missing_successor",
        ),
        pytest.param(
            DevelopmentPrerequisiteLineage.REVOKED,
            None,
            "revocation.one",
            True,
            id="revoked_requires_revocation",
        ),
        pytest.param(
            DevelopmentPrerequisiteLineage.REVOKED,
            None,
            None,
            False,
            id="revoked_rejects_missing_revocation",
        ),
    ),
)
def test_artifact__construction__lineage_companion_partition(
    lineage: DevelopmentPrerequisiteLineage,
    successor: str | None,
    revocation: str | None,
    valid: bool,
) -> None:
    """Every lineage variant owns one exact companion-field shape.

    Evidence ID: SV-PREREQ-018

    Requirement: Effective, superseded, and revoked references preserve distinct
    intrinsic companion identities.

    Acceptance: Every valid semantic partition constructs and every invalid partition
    raises the lineage invariant error.
    """
    arguments = (
        1,
        DevelopmentPrerequisiteKind.TASK,
        "producer.task",
        "owner.domain",
        "result.one",
        "verified.result",
        "claim.complete",
        "revision.one",
        "retention.repository",
        content(),
        lineage,
        successor,
        revocation,
    )
    if valid:
        assert RetainedPrerequisiteResultReference(*arguments).lineage is lineage
    else:
        with pytest.raises(ValueError, match="lineage requires"):
            RetainedPrerequisiteResultReference(*arguments)


def test_artifact__result__preserves_failure_diagnostics_exactly() -> None:
    """Aggregate and edge diagnostics are immutable represented failure state.

    Evidence ID: SV-PREREQ-019

    Requirement: A blocked result preserves exact edge and aggregate diagnostics and
    cannot be relabeled satisfied.

    Acceptance: Exact fields agree and inconsistent aggregate construction fails.
    """
    edge = DevelopmentPrerequisiteEdgeResult(
        DevelopmentPrerequisiteKind.TASK,
        "producer.task",
        DevelopmentPrerequisiteOutcome.INDETERMINATE,
        None,
        ("edge.failure",),
    )
    result = DevelopmentPrerequisiteResolutionResult(
        "consumer.task",
        content(),
        "contract.consumer.v1",
        DevelopmentPrerequisiteAggregateStatus.BLOCKED,
        (edge,),
        ("aggregate.failure",),
    )
    assert result.edge_results[0].diagnostic_ids == ("edge.failure",)
    assert result.diagnostic_ids == ("aggregate.failure",)
    with pytest.raises(ValueError, match="satisfied outcomes contain no diagnostics"):
        DevelopmentPrerequisiteEdgeResult(
            DevelopmentPrerequisiteKind.TASK,
            "producer.task",
            DevelopmentPrerequisiteOutcome.SATISFIED,
            "result.task",
            ("edge.failure",),
        )
    with pytest.raises(ValueError, match="aggregate status"):
        DevelopmentPrerequisiteResolutionResult(
            result.consumer_task_id,
            result.consumer_task_content_identity,
            result.contract_id,
            DevelopmentPrerequisiteAggregateStatus.SATISFIED,
            result.edge_results,
            result.diagnostic_ids,
        )
