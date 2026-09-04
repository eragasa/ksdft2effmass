r"""Software verification of Workflow artifact provenance contract.

Evidence profile: claim_bearing

Bounded artifact scope: ``ksdft2effmass.workflows.artifacts`` public records and
package-level exports.

Facet and represented meaning

The module verifies represented content identity, five closed producer-provenance
variants, Workflow attempt/result correlation, portable manifest entries, and immutable
manifest
revision lineage.

Intrinsic and cross-object scope

Constructors are the oracle for intrinsic and record-local joins.  The retained QE 7.5
silicon DOS observation supplies one concrete represented-Workflow example; synthetic
records exercise the four non-Workflow producer partitions without upgrading their
evidence status.

VVUQ and scientific exclusions

Passing establishes software-contract behavior only.  It does not observe files,
recompute hashes, validate formats, verify repository existence or graph-wide lineage,
execute a calculator, establish numerical verification, scientific validation,
uncertainty quantification, retention authority, or human acceptance.
"""

import hashlib
import json
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from typing import Any

import pytest

from ksdft2effmass import provenance as legacy_provenance
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactLineageKind,
    ArtifactLineageRelation,
    ArtifactLineageRelationIdentity,
    ArtifactLineageSourceIdentity,
    ArtifactManifest,
    ArtifactManifestEntry,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    ArtifactManifestSupersessionIdentity,
    ArtifactProducerKind,
    ArtifactProducerProvenanceIdentity,
    AttemptIdentity,
    ExternalSourceObservation,
    HumanAuthoredCompactInput,
    ImportedRetainedFixture,
    RepresentedWorkflowProducer,
    ResultArtifactRelationIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskInstanceIdentity,
    UnknownLegacyProducer,
    WorkflowIdentity,
    WorkflowRunIdentity,
)

pytestmark = pytest.mark.software_verification

_DOS_DIGEST = "b967ed73c7d2572123dbf0b928630e38868ad2f9afbb1b3e77f140ecd53bf6df"
_RUN = "qe-7.5-silicon-dos-20260903T102922Z"


def make_content(
    digest: str = _DOS_DIGEST,
    byte_count: int = 82_588,
) -> ArtifactContentIdentity:
    """Return one explicit represented content identity.

    Evidence ID: Helper owns no identifier.

    Requirement: Support artifact-contract evidence without an independent claim.

    Method: Construct the public fixed-SHA-256 content identity.

    Oracle: Consuming tests own expected values.

    Acceptance: Return the declared immutable value.

    Interpretation: Failure blocks consuming evidence owners.

    Limitations: No bytes are read or hashed.
    """
    return ArtifactContentIdentity("sha256", digest, byte_count)


def make_workflow_producer(
    *,
    artifact_identity: ArtifactIdentity | None = None,
    content_identity: ArtifactContentIdentity | None = None,
) -> RepresentedWorkflowProducer:
    """Return the represented producer for the retained DOS artifact.

    Evidence ID: Helper owns no identifier.

    Requirement: Support exact Workflow-lineage evidence without an independent claim.

    Method: Construct one public represented-Workflow producer.

    Oracle: Consuming tests compare fields with the retained compact observation.

    Acceptance: Return the declared immutable producer.

    Interpretation: Failure blocks consuming evidence owners.

    Limitations: The helper does not establish that any referenced record exists.
    """
    artifact = artifact_identity or ArtifactIdentity(f"{_RUN}:dos:artifact:si_dos.dat")
    content = content_identity or make_content()
    return RepresentedWorkflowProducer(
        ArtifactProducerProvenanceIdentity(f"{_RUN}:dos:producer:1"),
        1,
        ArtifactProducerKind.REPRESENTED_WORKFLOW,
        artifact,
        content,
        (
            f"{_RUN}:dos:process:1",
            "qe75-calculated-observation:sha256:"
            "d7890936fb7b3dbf98b048cea09ad4db830e489a3613bf1acca9fb0b191e39a7",
        ),
        (
            "claim.calculated-tutorial-observation-only",
            "claim.not-scientifically-validated",
        ),
        WorkflowIdentity("dft.scf-nscf-dos.v1"),
        WorkflowRunIdentity(_RUN),
        TaskInstanceIdentity(f"{_RUN}:dos"),
        TaskActivationIdentity(f"{_RUN}:dos:activation:1"),
        AttemptIdentity(f"{_RUN}:dos:attempt:1"),
        ResultObjectIdentity(f"{_RUN}:dos:result:1"),
        ResultArtifactRelationIdentity(f"{_RUN}:dos:result-artifact:si_dos.dat"),
    )


def make_entry() -> ArtifactManifestEntry:
    """Return one exact represented-Workflow DOS artifact entry.

    Evidence ID: Helper owns no identifier.

    Requirement: Support manifest evidence without an independent claim.

    Method: Correlate one artifact/content pair to its represented producer.

    Oracle: Consuming tests own expected closure.

    Acceptance: Return the declared entry.

    Interpretation: Failure blocks consuming evidence owners.

    Limitations: The portable store reference is an opaque identity, not a path.
    """
    producer = make_workflow_producer()
    artifact = producer.artifact_identity
    relations = (
        ArtifactLineageRelation(
            ArtifactLineageRelationIdentity(f"{_RUN}:dos:lineage:1:cpn-selection"),
            ArtifactLineageKind.CPN_SELECTION,
            ArtifactLineageSourceIdentity(producer.task_activation_identity.value),
            artifact,
            producer.workflow_run_identity,
            producer.attempt_identity,
            (f"{_RUN}:dos:activation-record:1",),
            ("claim.selection-correlation-only",),
        ),
        ArtifactLineageRelation(
            ArtifactLineageRelationIdentity(
                f"{_RUN}:dos:lineage:2:execution-authority"
            ),
            ArtifactLineageKind.EXECUTION_AUTHORITY_SNAPSHOT,
            ArtifactLineageSourceIdentity(
                "QE-SILICON-DOS-RUN-HC01:sha256:"
                "13a70c5d4811da410b3e847599d7d40661d417725a6298ed30ce31b8abbc0604"
            ),
            artifact,
            producer.workflow_run_identity,
            producer.attempt_identity,
            ("QE-SILICON-DOS-RUN-HC01",),
            ("claim.protected-execution-authority-only",),
        ),
        ArtifactLineageRelation(
            ArtifactLineageRelationIdentity(f"{_RUN}:dos:lineage:3:execution-grant"),
            ArtifactLineageKind.EXECUTION_GRANT,
            ArtifactLineageSourceIdentity(f"{_RUN}:dos:grant:1"),
            artifact,
            producer.workflow_run_identity,
            producer.attempt_identity,
            (f"{_RUN}:dos:grant-record:1",),
            ("claim.single-dispatch-grant-only",),
        ),
        ArtifactLineageRelation(
            ArtifactLineageRelationIdentity(
                f"{_RUN}:dos:lineage:4:process-observation"
            ),
            ArtifactLineageKind.PROCESS_OBSERVATION,
            ArtifactLineageSourceIdentity(f"{_RUN}:dos:process:1"),
            artifact,
            producer.workflow_run_identity,
            producer.attempt_identity,
            (f"{_RUN}:dos:process:1",),
            ("claim.process-observation-only",),
        ),
        ArtifactLineageRelation(
            ArtifactLineageRelationIdentity(f"{_RUN}:dos:lineage:5:result-ingress"),
            ArtifactLineageKind.RESULT_INGRESS,
            ArtifactLineageSourceIdentity(
                "qe75-calculated-observation:sha256:"
                "d7890936fb7b3dbf98b048cea09ad4db830e489a3613bf1acca9fb0b191e39a7:"
                "tasks.dos.result-ingress"
            ),
            artifact,
            producer.workflow_run_identity,
            producer.attempt_identity,
            (f"{_RUN}:dos:result-ingress-record:1",),
            ("claim.result-ingress-correlation-only",),
        ),
        ArtifactLineageRelation(
            ArtifactLineageRelationIdentity(f"{_RUN}:dos:lineage:6:result-production"),
            ArtifactLineageKind.RESULT_PRODUCTION,
            ArtifactLineageSourceIdentity(
                producer.result_artifact_relation_identity.value
            ),
            artifact,
            producer.workflow_run_identity,
            producer.attempt_identity,
            (producer.result_object_identity.value,),
            ("claim.result-artifact-correlation-only",),
        ),
    )
    return ArtifactManifestEntry(
        ArtifactManifestEntryIdentity(f"{_RUN}:dos:manifest-entry:si_dos.dat"),
        artifact,
        producer.content_identity,
        "quantum-espresso.dos-text",
        "density-of-states.native-output",
        "external-calculation-artifact.not-redistributed",
        (),
        "qe75-silicon-dos-run/results/artifacts/si_dos.dat",
        relations,
        producer,
    )


def make_legacy_entry(
    name: str,
    digit: str,
    parents: tuple[ArtifactIdentity, ...] = (),
) -> ArtifactManifestEntry:
    """Return one explicitly limited synthetic legacy entry.

    Evidence ID: Helper owns no identifier.

    Requirement: Support parent-graph closure evidence without an independent claim.

    Method: Construct matching unknown-legacy producer and manifest-entry records.

    Oracle: Consuming tests own expected graph behavior.

    Acceptance: Return one locally valid entry with supplied parents.

    Interpretation: Failure blocks consuming evidence owners.

    Limitations: Synthetic legacy state is not calculated physical data.
    """
    artifact = ArtifactIdentity(f"artifact.{name}")
    content = make_content(digit * 64, 1)
    producer = UnknownLegacyProducer(
        ArtifactProducerProvenanceIdentity(f"producer.{name}"),
        1,
        ArtifactProducerKind.UNKNOWN_LEGACY,
        artifact,
        content,
        (f"evidence.{name}",),
        ("claim.synthetic-legacy-only",),
        "synthetic parent-graph partition",
        ("producer lineage intentionally unavailable",),
        "synthetic_test_data",
    )
    return ArtifactManifestEntry(
        ArtifactManifestEntryIdentity(f"entry.{name}"),
        artifact,
        content,
        "synthetic.test-record",
        "parent-closure-test",
        "retained-verification-fixture",
        parents,
        None,
        (),
        producer,
    )


def evidence_closure(*entries: ArtifactManifestEntry) -> tuple[str, ...]:
    """Return the exact evidence closure index for supplied entries.

    Evidence ID: Helper owns no identifier.

    Requirement: Support manifest closure evidence without an independent claim.

    Method: Collect producer and lineage evidence identity tuples.

    Oracle: Consuming tests own expected manifest behavior.

    Acceptance: Return the unique lexically sorted union.

    Interpretation: Failure blocks consuming evidence owners.

    Limitations: Collection does not establish referenced evidence existence.
    """
    values = {
        evidence
        for entry in entries
        for evidence in entry.producer_provenance.evidence_identity_values
    }
    values.update(
        evidence
        for entry in entries
        for relation in entry.lineage_relations
        for evidence in relation.evidence_identity_values
    )
    return tuple(sorted(values))


def test_artifact__retained_dos__binds_actual_attempt_result_and_content() -> None:
    """Evidence ID: SV-WFA-001

    Requirement: A represented Workflow producer binds the retained DOS content-
    identity observation to the exact Workflow, run, Task instance, activation,
    attempt, and result.

    Method: Load the compact calculated observation and construct one manifest entry
    from its represented identities.

    Oracle: The retained observation is the exact authorized tutorial-run record.

    Acceptance: Every producer correlation and content field equals the retained value.

    Interpretation: Failure identifies fabricated, omitted, or drifted run lineage.

    Limitations: The test neither reads the external DOS bytes nor upgrades the
    observation's tutorial-only claim status.
    """
    repository_root = Path(__file__).resolve().parents[6]
    path = repository_root / (
        "examples/tutorials/silicon-dos/qe/expected/qe75-calculated-observation.json"
    )
    observation_bytes = path.read_bytes()
    observation_digest = hashlib.sha256(observation_bytes).hexdigest()
    checkpoint_path = repository_root / (
        ".pi/checkpoints/qe-silicon-dos-workflow-execution.json"
    )
    checkpoint_digest = hashlib.sha256(checkpoint_path.read_bytes()).hexdigest()
    observed: dict[str, Any] = json.loads(observation_bytes)
    task: dict[str, Any] = observed["tasks"]["dos"]
    execution: dict[str, Any] = task["execution"]
    artifact: dict[str, Any] = task["dos_artifact"]

    entry = make_entry()
    producer = entry.producer_provenance
    assert type(producer) is RepresentedWorkflowProducer
    manifest = ArtifactManifest(
        ArtifactManifestIdentity(f"{_RUN}:artifacts:manifest:1"),
        1,
        None,
        None,
        producer.workflow_identity,
        producer.workflow_run_identity,
        evidence_closure(entry),
        (entry,),
    )
    assert producer.workflow_identity.value == observed["workflow_identity"]
    assert producer.workflow_run_identity.value == observed["workflow_run_id"]
    assert manifest.workflow_identity is producer.workflow_identity
    assert manifest.workflow_run_identity is producer.workflow_run_identity
    assert producer.task_instance_identity.value == task["task_instance_identity"]
    assert producer.task_activation_identity.value == execution["activation_identity"]
    assert producer.attempt_identity.value == execution["attempt_identity"]
    assert producer.result_object_identity.value == task["result_object_identity"]
    lineage = {relation.kind: relation for relation in entry.lineage_relations}
    assert (
        lineage[ArtifactLineageKind.EXECUTION_GRANT].source_identity.value
        == (execution["grant_identity"])
    )
    assert (
        lineage[ArtifactLineageKind.PROCESS_OBSERVATION].source_identity.value
        == (task["process_observation_identity"])
    )
    authority_source = lineage[
        ArtifactLineageKind.EXECUTION_AUTHORITY_SNAPSHOT
    ].source_identity.value
    assert authority_source.endswith(checkpoint_digest)
    ingress_source = lineage[ArtifactLineageKind.RESULT_INGRESS].source_identity.value
    assert observation_digest in ingress_source
    assert entry.content_identity.digest == artifact["sha256"]
    assert entry.content_identity.byte_count == artifact["byte_count"]
    assert "not-scientifically-validated" in producer.claim_boundary_identity_values[1]


def test_artifact__content_identity__is_strict_fixed_sha256_and_u64() -> None:
    """Evidence ID: SV-WFA-002

    Requirement: Content identity accepts only fixed lowercase SHA-256 text and an
    exact non-Boolean unsigned-64-bit byte count.

    Method: Construct boundary-valid and representative invalid values.

    Oracle: The public content-identity contract defines exact lexical and numeric
    domains and intentionally defers algorithm agility.

    Acceptance: Valid boundaries construct; wrong types raise ``TypeError`` and wrong
    values raise ``ValueError``.

    Interpretation: Failure identifies coercion, digest normalization, or overflow.

    Limitations: Represented-value validation does not hash bytes.
    """
    assert ArtifactContentIdentity("sha256", "0" * 64, 0).byte_count == 0
    upper = ArtifactContentIdentity("sha256", "f" * 64, 2**64 - 1)
    assert upper.byte_count == 2**64 - 1
    with pytest.raises(TypeError, match="excluding bool"):
        ArtifactContentIdentity("sha256", "0" * 64, True)
    with pytest.raises(ValueError, match="unsigned 64-bit"):
        ArtifactContentIdentity("sha256", "0" * 64, 2**64)
    with pytest.raises(ValueError, match="lowercase hexadecimal"):
        ArtifactContentIdentity("sha256", "A" * 64, 1)
    with pytest.raises(ValueError, match="algorithm must equal"):
        ArtifactContentIdentity("sha512", "0" * 64, 1)


def test_artifact__producer_union__retains_five_non_interchangeable_variants() -> None:
    """Evidence ID: SV-WFA-003

    Requirement: Producer provenance is closed over five separately shaped variants;
    inapplicable Workflow lineage cannot leak into non-Workflow records.

    Method: Construct one value of every public variant and inspect its discriminator
    and source-specific fields.

    Oracle: The accepted Workflow artifact architecture defines the five variants and
    prohibits a sparse bag of mostly absent fields.

    Acceptance: Kinds are exhaustive and distinct; only the represented producer has
    ``workflow_run_identity``.

    Interpretation: Failure identifies variant collapse or provenance overclaiming.

    Limitations: Synthetic non-Workflow identities establish no external truth.
    """
    artifact_ids = tuple(ArtifactIdentity(f"artifact.{index}") for index in range(5))
    content = tuple(make_content(str(index) * 64, index + 1) for index in range(5))
    represented = make_workflow_producer(
        artifact_identity=artifact_ids[0], content_identity=content[0]
    )
    external = ExternalSourceObservation(
        ArtifactProducerProvenanceIdentity("producer.external"),
        1,
        ArtifactProducerKind.EXTERNAL_SOURCE_OBSERVATION,
        artifact_ids[1],
        content[1],
        ("evidence.observation",),
        ("claim.observed-bytes-only",),
        "producer.qe.external",
        "external.attempt.1",
        "external.artifact.1",
        None,
        "observation.1",
        "revision.1",
        "2026-09-03T10:43:55Z",
        "method.retained-record",
        "receipt.1",
        "producer predates the represented Workflow",
        ("external Workflow execution records are unavailable",),
    )
    fixture = ImportedRetainedFixture(
        ArtifactProducerProvenanceIdentity("producer.fixture"),
        1,
        ArtifactProducerKind.IMPORTED_RETAINED_FIXTURE,
        artifact_ids[2],
        content[2],
        ("evidence.fixture",),
        ("claim.synthetic-fixture-only",),
        "fixture.1",
        "fixture.revision.1",
        "source.1",
        "fixtures/source/one",
        "import.1",
        "import.receipt.1",
        "retained.source.1",
        make_content("a" * 64, 7),
        "retained.checksum.1",
        "retained.provenance.1",
        "synthetic_test_data",
    )
    authored = HumanAuthoredCompactInput(
        ArtifactProducerProvenanceIdentity("producer.authored"),
        1,
        ArtifactProducerKind.HUMAN_AUTHORED_COMPACT_INPUT,
        artifact_ids[3],
        content[3],
        ("evidence.authorship",),
        ("claim.input-authorship-only",),
        "input.1",
        "input.revision.1",
        ("author.human.1",),
        "authority.repository-maintainer",
        None,
        "review.1",
        "authorship.record.1",
    )
    legacy = UnknownLegacyProducer(
        ArtifactProducerProvenanceIdentity("producer.legacy"),
        1,
        ArtifactProducerKind.UNKNOWN_LEGACY,
        artifact_ids[4],
        content[4],
        ("evidence.legacy-checksum",),
        ("claim.legacy-bytes-only",),
        "producer record unavailable",
        ("attempt identity unavailable", "Workflow identity unavailable"),
        "incomplete_producer_provenance",
    )
    producers = (represented, external, fixture, authored, legacy)
    assert {producer.kind for producer in producers} == set(ArtifactProducerKind)
    assert external.limitation_values == (
        "external Workflow execution records are unavailable",
    )
    assert fixture.retained_content_identity == make_content("a" * 64, 7)
    assert hasattr(represented, "workflow_run_identity")
    assert all(
        not hasattr(producer, "workflow_run_identity") for producer in producers[1:]
    )


def test_artifact__producer_variants__reject_wrong_tags_and_incomplete_boundaries() -> (
    None
):
    """Evidence ID: SV-WFA-004

    Requirement: Each concrete producer enforces its exact tag and required boundary;
    an external observation must retain an upstream artifact/result identity and valid
    known timestamp.

    Method: Supply a wrong variant tag, absent upstream output identities, and an
    impossible calendar timestamp.

    Oracle: Concrete class identity and the mandatory discriminator must agree exactly.

    Acceptance: Every malformed producer raises ``ValueError``.

    Interpretation: Failure identifies ambiguous dispatch or fabricated external
    provenance tolerance.

    Limitations: Calendar validation does not establish observation authenticity.
    """
    producer = make_workflow_producer()
    with pytest.raises(ValueError, match="kind must equal represented_workflow"):
        RepresentedWorkflowProducer(
            producer.identity,
            1,
            ArtifactProducerKind.UNKNOWN_LEGACY,
            producer.artifact_identity,
            producer.content_identity,
            producer.evidence_identity_values,
            producer.claim_boundary_identity_values,
            producer.workflow_identity,
            producer.workflow_run_identity,
            producer.task_instance_identity,
            producer.task_activation_identity,
            producer.attempt_identity,
            producer.result_object_identity,
            producer.result_artifact_relation_identity,
        )

    common = (
        ArtifactProducerProvenanceIdentity("producer.external.bad"),
        1,
        ArtifactProducerKind.EXTERNAL_SOURCE_OBSERVATION,
        ArtifactIdentity("artifact.external.bad"),
        make_content(),
        ("evidence.external",),
        ("claim.external",),
        "producer.external",
        "attempt.external",
    )
    with pytest.raises(ValueError, match="artifact_identity or external_result"):
        ExternalSourceObservation(
            *common,
            None,
            None,
            "observation.bad",
            None,
            None,
            "method.one",
            "receipt.one",
            "outside Workflow",
            ("producer records unavailable",),
        )
    with pytest.raises(ValueError, match="real UTC calendar"):
        ExternalSourceObservation(
            *common,
            "artifact.upstream",
            None,
            "observation.bad-time",
            None,
            "2026-02-31T10:00:00Z",
            "method.one",
            "receipt.one",
            "outside Workflow",
            ("producer records unavailable",),
        )
    with pytest.raises(ValueError, match="limitation_values must not be empty"):
        ExternalSourceObservation(
            *common,
            "artifact.upstream",
            None,
            "observation.no-limitations",
            None,
            None,
            "method.one",
            "receipt.one",
            "outside Workflow",
            (),
        )


def test_artifact__manifest_entry__rejects_mismatched_or_noncanonical_lineage() -> None:
    """Evidence ID: SV-WFA-005

    Requirement: An entry closes exact artifact/content, typed lineage, execution,
    attempt, and portable-reference relations and uses ordered non-self parents.

    Method: Replace each join side and construct self/unsorted parents, an absolute
    path, incomplete execution lineage, and a wrong-attempt relation.

    Oracle: Manifest closure requires exact producer and content correlation before a
    Workflow may rely on the entry.

    Acceptance: Every mismatch or noncanonical parent relation raises ``ValueError``.

    Interpretation: Failure identifies admissible fabricated lineage or unstable
    manifest ordering.

    Limitations: Manifest-wide parent closure is exercised separately.
    """
    entry = make_entry()
    mismatched_producer = make_workflow_producer(
        artifact_identity=ArtifactIdentity("artifact.other"),
        content_identity=entry.content_identity,
    )
    with pytest.raises(ValueError, match="producer artifact identity"):
        ArtifactManifestEntry(
            entry.identity,
            entry.artifact_identity,
            entry.content_identity,
            entry.native_format,
            entry.semantic_role,
            entry.retention_classification,
            (),
            None,
            entry.lineage_relations,
            mismatched_producer,
        )
    with pytest.raises(ValueError, match="producer content identity"):
        ArtifactManifestEntry(
            entry.identity,
            entry.artifact_identity,
            make_content("e" * 64),
            entry.native_format,
            entry.semantic_role,
            entry.retention_classification,
            (),
            None,
            entry.lineage_relations,
            entry.producer_provenance,
        )
    with pytest.raises(ValueError, match="must not name itself"):
        ArtifactManifestEntry(
            entry.identity,
            entry.artifact_identity,
            entry.content_identity,
            entry.native_format,
            entry.semantic_role,
            entry.retention_classification,
            (entry.artifact_identity,),
            None,
            entry.lineage_relations,
            entry.producer_provenance,
        )
    with pytest.raises(ValueError, match="unique and lexically sorted"):
        ArtifactManifestEntry(
            entry.identity,
            entry.artifact_identity,
            entry.content_identity,
            entry.native_format,
            entry.semantic_role,
            entry.retention_classification,
            (ArtifactIdentity("parent.z"), ArtifactIdentity("parent.a")),
            None,
            entry.lineage_relations,
            entry.producer_provenance,
        )
    with pytest.raises(ValueError, match="portable relative reference"):
        ArtifactManifestEntry(
            entry.identity,
            entry.artifact_identity,
            entry.content_identity,
            entry.native_format,
            entry.semantic_role,
            entry.retention_classification,
            (),
            "/Users/alice/private.dat",
            entry.lineage_relations,
            entry.producer_provenance,
        )
    with pytest.raises(ValueError, match="requires exactly one CPN"):
        ArtifactManifestEntry(
            entry.identity,
            entry.artifact_identity,
            entry.content_identity,
            entry.native_format,
            entry.semantic_role,
            entry.retention_classification,
            (),
            None,
            (),
            entry.producer_provenance,
        )
    incomplete_execution = tuple(
        relation
        for relation in entry.lineage_relations
        if relation.kind is not ArtifactLineageKind.RESULT_INGRESS
    )
    with pytest.raises(ValueError, match="applicable execution lineage"):
        ArtifactManifestEntry(
            entry.identity,
            entry.artifact_identity,
            entry.content_identity,
            entry.native_format,
            entry.semantic_role,
            entry.retention_classification,
            (),
            None,
            incomplete_execution,
            entry.producer_provenance,
        )
    wrong_attempt = (
        replace(
            entry.lineage_relations[0],
            operation_attempt_identity=AttemptIdentity("attempt.other"),
        ),
        *entry.lineage_relations[1:],
    )
    with pytest.raises(ValueError, match="run and attempt must equal"):
        ArtifactManifestEntry(
            entry.identity,
            entry.artifact_identity,
            entry.content_identity,
            entry.native_format,
            entry.semantic_role,
            entry.retention_classification,
            (),
            None,
            wrong_attempt,
            entry.producer_provenance,
        )


def test_artifact__manifest__is_immutable_canonical_revision_chain() -> None:
    """Evidence ID: SV-WFA-006

    Requirement: A manifest is immutable, nonempty, canonically ordered, closes exact
    evidence and acyclic parent lineage, and requires predecessor plus supersession
    identities only after revision one.

    Method: Construct valid first/second revisions and invalid revision, predecessor,
    evidence, duplicate, dangling-parent, and parent-cycle partitions.

    Oracle: The public manifest contract defines append-only correction and local
    canonical closure.

    Acceptance: Valid revisions construct and malformed values raise the documented
    exception taxonomy.

    Interpretation: Failure identifies mutable history or ambiguous manifest closure.

    Limitations: The constructor cannot prove predecessor or external evidence
    existence in persistence.
    """
    entry = make_entry()
    first_identity = ArtifactManifestIdentity("manifest.1")
    workflow = WorkflowIdentity("workflow.one")
    run = WorkflowRunIdentity("run.one")
    evidence = evidence_closure(entry)
    first = ArtifactManifest(
        first_identity, 1, None, None, workflow, run, evidence, (entry,)
    )
    second = ArtifactManifest(
        ArtifactManifestIdentity("manifest.2"),
        2,
        first.identity,
        ArtifactManifestSupersessionIdentity("supersession.2-over-1"),
        workflow,
        run,
        evidence,
        (entry,),
    )
    assert second.predecessor_manifest_identity is first.identity
    with pytest.raises(FrozenInstanceError):
        first.revision = 2  # type: ignore[misc]
    with pytest.raises(TypeError, match="excluding bool"):
        ArtifactManifest(
            first_identity,
            True,
            None,
            None,
            workflow,
            run,
            evidence,
            (entry,),
        )
    with pytest.raises(ValueError, match="absent for revision 1"):
        ArtifactManifest(
            first_identity,
            1,
            ArtifactManifestIdentity("prior"),
            ArtifactManifestSupersessionIdentity("unexpected"),
            workflow,
            run,
            evidence,
            (entry,),
        )
    with pytest.raises(ValueError, match="required after revision 1"):
        ArtifactManifest(
            ArtifactManifestIdentity("manifest.2"),
            2,
            None,
            None,
            workflow,
            run,
            evidence,
            (entry,),
        )
    with pytest.raises(ValueError, match="must not be empty"):
        ArtifactManifest(first_identity, 1, None, None, workflow, run, ("x",), ())
    with pytest.raises(ValueError, match="unique lexically sorted"):
        ArtifactManifest(
            first_identity,
            1,
            None,
            None,
            workflow,
            run,
            evidence,
            (entry, entry),
        )
    with pytest.raises(ValueError, match="exactly close"):
        ArtifactManifest(
            first_identity,
            1,
            None,
            None,
            workflow,
            run,
            ("evidence.unclosed",),
            (entry,),
        )

    dangling = make_legacy_entry("dangling", "1", (ArtifactIdentity("missing"),))
    with pytest.raises(ValueError, match="parent artifact identity"):
        ArtifactManifest(
            first_identity,
            1,
            None,
            None,
            workflow,
            run,
            evidence_closure(dangling),
            (dangling,),
        )
    left_identity = ArtifactIdentity("artifact.left")
    right_identity = ArtifactIdentity("artifact.right")
    left = make_legacy_entry("left", "2", (right_identity,))
    right = make_legacy_entry("right", "3", (left_identity,))
    with pytest.raises(ValueError, match="must be acyclic"):
        ArtifactManifest(
            first_identity,
            1,
            None,
            None,
            workflow,
            run,
            evidence_closure(left, right),
            (left, right),
        )


def test_artifact__public_owner__does_not_alias_legacy_provenance_identity() -> None:
    """Evidence ID: SV-WFA-007

    Requirement: Workflow-owned v2 identities are explicit new owners, not aliases of
    equal-looking transitional ``ksdft2effmass.provenance`` records.

    Method: Compare public class identities and reject a legacy identity in a Workflow
    manifest entry.

    Oracle: The migration crosswalk requires explicit adaptation rather than aliases.

    Acceptance: The classes are distinct and a legacy identity raises ``TypeError``.

    Interpretation: Failure identifies owner collapse or accidental compatibility.

    Limitations: This test does not implement or authorize a migration adapter.
    """
    assert ArtifactIdentity is not legacy_provenance.ArtifactIdentity
    entry = make_entry()
    legacy = legacy_provenance.ArtifactIdentity("legacy", "0" * 64, 1)
    with pytest.raises(TypeError, match="ArtifactIdentity"):
        ArtifactManifestEntry(
            entry.identity,
            legacy,  # type: ignore[arg-type]
            entry.content_identity,
            entry.native_format,
            entry.semantic_role,
            entry.retention_classification,
            (),
            None,
            entry.lineage_relations,
            entry.producer_provenance,
        )
