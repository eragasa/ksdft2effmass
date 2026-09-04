"""Workflow-owned immutable artifact manifests and producer provenance.

This module represents portable artifact identity, exact observed byte identity,
closed producer-provenance variants, and manifest revision relationships.  It performs
no filesystem access, hashing, location resolution, persistence, serialization,
external execution, scientific interpretation, or retention action.

The records are calculator-independent.  A represented Workflow producer retains the
exact Workflow, run, Task, activation, attempt, and ResultObject identities.  External,
fixture, human-authored, and unknown-legacy producers retain their actual evidence
boundary without fabricated Workflow lineage.  Exact byte identity does not establish
format validity, semantic compatibility, scientific correctness, validation,
uncertainty quantification, or human acceptance.  Callers must not encode
credentials, private keys, tokens, scheduler secrets, or restricted data in identity,
reference, evidence, limitation, or claim-boundary text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import PurePosixPath

from .model import (
    AttemptIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)

_MAX_U64 = 18_446_744_073_709_551_615
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
_TIMESTAMP_PATTERN = re.compile(
    r"[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])"
    r"T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z\Z",
    re.ASCII,
)


def _require_identity(value: object, owner: str) -> None:
    """Require one nonempty exact built-in string identity."""
    if type(value) is not str:
        raise TypeError(f"{owner} must be a built-in str")
    if not value:
        raise ValueError(f"{owner} must not be empty")


def _require_optional_identity(value: object, owner: str) -> None:
    """Require an absent or nonempty exact built-in string identity."""
    if value is not None:
        _require_identity(value, owner)


def _require_identity_tuple(
    values: object,
    owner: str,
    *,
    allow_empty: bool = False,
) -> None:
    """Require one immutable lexically ordered identity collection."""
    if type(values) is not tuple:
        raise TypeError(f"{owner} must be a built-in tuple")
    if not allow_empty and not values:
        raise ValueError(f"{owner} must not be empty")
    for value in values:
        _require_identity(value, f"{owner} member")
    if values != tuple(sorted(values)) or len(set(values)) != len(values):
        raise ValueError(f"{owner} must be unique and lexically sorted")


def _require_portable_reference(value: object, owner: str) -> None:
    """Reject absolute, home-relative, parent-traversing, or native-path text."""
    _require_identity(value, owner)
    assert isinstance(value, str)
    if "\\" in value or value.startswith(("/", "~")):
        raise ValueError(f"{owner} must be a portable relative reference")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or value != path.as_posix()
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise ValueError(f"{owner} must be a portable relative reference")
    if re.match(r"[A-Za-z]:", value, re.ASCII) is not None:
        raise ValueError(f"{owner} must be a portable relative reference")


@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    """Nominal identity of one artifact independent of its byte representation.

    Parameters
    ----------
    value
        Nonempty owner-local identity.  It is not a path, digest, storage locator, or
        assertion that artifact bytes exist.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact nominal identity."""
        _require_identity(self.value, "artifact identity value")


@dataclass(frozen=True, slots=True)
class ArtifactManifestIdentity:
    """Nominal identity of one immutable artifact-manifest revision.

    Parameters
    ----------
    value
        Nonempty owner-local identity.  Revision ordering is represented separately by
        :class:`ArtifactManifest`.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact nominal identity."""
        _require_identity(self.value, "artifact manifest identity value")


@dataclass(frozen=True, slots=True)
class ArtifactManifestEntryIdentity:
    """Nominal identity of one exact entry in an artifact manifest revision.

    Parameters
    ----------
    value
        Nonempty owner-local identity used by downstream consumers to reference the
        exact manifest entry rather than an artifact label alone.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact nominal identity."""
        _require_identity(self.value, "artifact manifest entry identity value")


@dataclass(frozen=True, slots=True)
class ArtifactManifestSupersessionIdentity:
    """Nominal identity of one immutable manifest-correction relation.

    Parameters
    ----------
    value
        Nonempty owner-local identity distinct from both manifest revisions.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact nominal identity."""
        _require_identity(self.value, "artifact manifest supersession identity value")


@dataclass(frozen=True, slots=True)
class ResultArtifactRelationIdentity:
    """Nominal identity of the exact relation from a result to an artifact.

    Parameters
    ----------
    value
        Nonempty owner-local relation identity.  It establishes no result or artifact
        existence outside a correlated manifest boundary.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact nominal identity."""
        _require_identity(self.value, "result-artifact relation identity value")


@dataclass(frozen=True, slots=True)
class ArtifactLineageRelationIdentity:
    """Nominal identity of one explicit artifact-lineage edge.

    Parameters
    ----------
    value
        Nonempty owner-local relation identity.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact nominal identity."""
        _require_identity(self.value, "artifact lineage relation identity value")


@dataclass(frozen=True, slots=True)
class ArtifactLineageSourceIdentity:
    """Nominal source identity for one typed artifact-lineage edge.

    Parameters
    ----------
    value
        Nonempty identity owned by the applicable Workflow, calculator, integration,
        normalization, or analysis boundary.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact nominal identity."""
        _require_identity(self.value, "artifact lineage source identity value")


@dataclass(frozen=True, slots=True)
class ArtifactProducerProvenanceIdentity:
    """Nominal identity of one closed producer-provenance record.

    Parameters
    ----------
    value
        Nonempty owner-local identity distinct from artifact and manifest identities.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact nominal identity."""
        _require_identity(self.value, "artifact producer provenance identity value")


@dataclass(frozen=True, slots=True)
class ArtifactContentIdentity:
    """Exact SHA-256 identity and byte count observed at another boundary.

    Parameters
    ----------
    algorithm
        Exact string ``"sha256"``.  Algorithm agility is intentionally deferred.
    digest
        Exactly 64 lowercase hexadecimal SHA-256 characters.
    byte_count
        Exact built-in integer byte count in the inclusive unsigned 64-bit range
        :math:`[0, 2^{64}-1]`.  Booleans and numeric strings are rejected.

    Notes
    -----
    Construction does not read bytes or compute a digest.  Agreement of represented
    values establishes byte identity only, subject to the selected algorithm.
    """

    algorithm: str
    digest: str
    byte_count: int

    def __post_init__(self) -> None:
        """Validate the fixed algorithm, digest representation, and byte range."""
        if type(self.algorithm) is not str:
            raise TypeError("algorithm must be a built-in str")
        if self.algorithm != "sha256":
            raise ValueError("algorithm must equal sha256")
        if type(self.digest) is not str:
            raise TypeError("digest must be a built-in str")
        if _SHA256_PATTERN.fullmatch(self.digest) is None:
            raise ValueError(
                "digest must contain 64 lowercase hexadecimal SHA-256 characters"
            )
        if type(self.byte_count) is not int:
            raise TypeError("byte_count must be a built-in int excluding bool")
        if not 0 <= self.byte_count <= _MAX_U64:
            raise ValueError("byte_count must be in the unsigned 64-bit range")


class ArtifactProducerKind(StrEnum):
    """Closed producer-provenance discriminator.

    Attributes
    ----------
    REPRESENTED_WORKFLOW
        Artifact produced by an exactly represented Workflow Task result.
    EXTERNAL_SOURCE_OBSERVATION
        Artifact observed from a producer genuinely outside the represented Workflow.
    IMPORTED_RETAINED_FIXTURE
        Retained fixture imported without upgrading its source evidence.
    HUMAN_AUTHORED_COMPACT_INPUT
        Compact input authored under an identified human authority boundary.
    UNKNOWN_LEGACY
        Legacy artifact whose producer cannot be represented without inference.
    """

    REPRESENTED_WORKFLOW = "represented_workflow"
    EXTERNAL_SOURCE_OBSERVATION = "external_source_observation"
    IMPORTED_RETAINED_FIXTURE = "imported_retained_fixture"
    HUMAN_AUTHORED_COMPACT_INPUT = "human_authored_compact_input"
    UNKNOWN_LEGACY = "unknown_legacy"


class ArtifactLineageKind(StrEnum):
    """Closed kind for an explicit edge into an artifact manifest entry.

    Attributes
    ----------
    CPN_SELECTION
        Workflow-owned colored-Petri-net selection leading to Task activation.
    RESULT_PRODUCTION
        Correlation from the exact immutable ResultObject to the artifact.
    EXECUTION_GRANT
        Exact protected/external execution grant used by the producing attempt.
    EXECUTION_AUTHORITY_SNAPSHOT
        Exact immutable authority snapshot supporting that execution grant.
    PROCESS_OBSERVATION
        Exact process-observation record for the producing attempt.
    RESULT_INGRESS
        Exact Workflow result-ingress record admitting the immutable result.
    NATIVE_RESOLUTION
        Integration-owned resolution of an exact native artifact.
    PARSER
        Mechanically faithful parser record for exact native bytes.
    NORMALIZATION
        Versioned normalization policy or normalized-observation relation.
    ANALYSIS
        Downstream scientific-analysis relation without implied acceptance.
    """

    CPN_SELECTION = "cpn_selection"
    RESULT_PRODUCTION = "result_production"
    EXECUTION_GRANT = "execution_grant"
    EXECUTION_AUTHORITY_SNAPSHOT = "execution_authority_snapshot"
    PROCESS_OBSERVATION = "process_observation"
    RESULT_INGRESS = "result_ingress"
    NATIVE_RESOLUTION = "native_resolution"
    PARSER = "parser"
    NORMALIZATION = "normalization"
    ANALYSIS = "analysis"


@dataclass(frozen=True, slots=True)
class ArtifactLineageRelation:
    """One explicit identity-correlated edge into an artifact manifest entry.

    Parameters
    ----------
    identity
        Exact nominal identity of this lineage relation.
    kind
        Closed semantic kind of the source-to-artifact edge.
    source_identity
        Nominal identity owned by the source boundary named by ``kind``.
    target_artifact_identity
        Exact target artifact identity in the enclosing manifest entry.
    workflow_run_identity, operation_attempt_identity
        Exact Workflow run and operation attempt owning this edge.  For direct
        production edges these must agree with the represented producer; later
        parser, normalization, or analysis edges retain their own exact attempt.
    evidence_identity_values, claim_boundary_identity_values
        Nonempty, unique, lexically sorted supporting-evidence and claim-boundary
        identities.

    Notes
    -----
    The relation does not prove source existence or scientific compatibility.  A
    manifest closes target and evidence references that it contains.
    """

    identity: ArtifactLineageRelationIdentity
    kind: ArtifactLineageKind
    source_identity: ArtifactLineageSourceIdentity
    target_artifact_identity: ArtifactIdentity
    workflow_run_identity: WorkflowRunIdentity
    operation_attempt_identity: AttemptIdentity
    evidence_identity_values: tuple[str, ...]
    claim_boundary_identity_values: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact relation types and canonical evidence identities."""
        if type(self.identity) is not ArtifactLineageRelationIdentity:
            raise TypeError("identity must be an ArtifactLineageRelationIdentity")
        if not isinstance(self.kind, ArtifactLineageKind):
            raise TypeError("kind must be an ArtifactLineageKind")
        if type(self.source_identity) is not ArtifactLineageSourceIdentity:
            raise TypeError("source_identity must be an ArtifactLineageSourceIdentity")
        if type(self.target_artifact_identity) is not ArtifactIdentity:
            raise TypeError("target_artifact_identity must be an ArtifactIdentity")
        if type(self.workflow_run_identity) is not WorkflowRunIdentity:
            raise TypeError("workflow_run_identity must be a WorkflowRunIdentity")
        if type(self.operation_attempt_identity) is not AttemptIdentity:
            raise TypeError("operation_attempt_identity must be an AttemptIdentity")
        _require_identity_tuple(
            self.evidence_identity_values,
            "evidence_identity_values",
        )
        _require_identity_tuple(
            self.claim_boundary_identity_values,
            "claim_boundary_identity_values",
        )


def _require_common_provenance(
    *,
    identity: object,
    schema_version: object,
    kind: object,
    expected_kind: ArtifactProducerKind,
    artifact_identity: object,
    content_identity: object,
    evidence_identity_values: object,
    claim_boundary_identity_values: object,
) -> None:
    """Validate fields common to every concrete producer variant."""
    if type(identity) is not ArtifactProducerProvenanceIdentity:
        raise TypeError("identity must be an ArtifactProducerProvenanceIdentity")
    if type(schema_version) is not int:
        raise TypeError("schema_version must be a built-in int excluding bool")
    if schema_version != 1:
        raise ValueError("schema_version must equal 1")
    if not isinstance(kind, ArtifactProducerKind):
        raise TypeError("kind must be an ArtifactProducerKind")
    if kind is not expected_kind:
        raise ValueError(f"kind must equal {expected_kind.value}")
    if type(artifact_identity) is not ArtifactIdentity:
        raise TypeError("artifact_identity must be an ArtifactIdentity")
    if type(content_identity) is not ArtifactContentIdentity:
        raise TypeError("content_identity must be an ArtifactContentIdentity")
    _require_identity_tuple(evidence_identity_values, "evidence_identity_values")
    _require_identity_tuple(
        claim_boundary_identity_values,
        "claim_boundary_identity_values",
    )


@dataclass(frozen=True, slots=True)
class RepresentedWorkflowProducer:
    """Exact producer provenance for an artifact returned by a Workflow Task.

    Parameters
    ----------
    identity, schema_version, kind
        Provenance identity, exact version ``1``, and mandatory discriminator
        :attr:`ArtifactProducerKind.REPRESENTED_WORKFLOW`.
    artifact_identity, content_identity
        Nominal artifact identity and already-observed SHA-256/byte-count identity.
    evidence_identity_values, claim_boundary_identity_values
        Nonempty, unique, lexically sorted identity tuples describing supporting
        evidence and the limits of claims supported by that evidence.
    workflow_identity, workflow_run_identity
        Exact reusable Workflow and represented run identities.
    task_instance_identity, task_activation_identity, attempt_identity
        Exact producing Task instance, activation, and attempt identities.
    result_object_identity
        Exact immutable ResultObject identity returned by the producing Task.
    result_artifact_relation_identity
        Nominal identity of the exact relation between the ResultObject and artifact.

    Notes
    -----
    This record does not prove that the identities exist in a repository or that the
    represented execution was authorized, successful, converged, or scientifically
    accepted.  Those are cross-object or external-boundary claims.
    """

    identity: ArtifactProducerProvenanceIdentity
    schema_version: int
    kind: ArtifactProducerKind
    artifact_identity: ArtifactIdentity
    content_identity: ArtifactContentIdentity
    evidence_identity_values: tuple[str, ...]
    claim_boundary_identity_values: tuple[str, ...]
    workflow_identity: WorkflowIdentity
    workflow_run_identity: WorkflowRunIdentity
    task_instance_identity: TaskInstanceIdentity
    task_activation_identity: TaskActivationIdentity
    attempt_identity: AttemptIdentity
    result_object_identity: ResultObjectIdentity
    result_artifact_relation_identity: ResultArtifactRelationIdentity

    def __post_init__(self) -> None:
        """Validate the represented Workflow producer's intrinsic fields."""
        _require_common_provenance(
            identity=self.identity,
            schema_version=self.schema_version,
            kind=self.kind,
            expected_kind=ArtifactProducerKind.REPRESENTED_WORKFLOW,
            artifact_identity=self.artifact_identity,
            content_identity=self.content_identity,
            evidence_identity_values=self.evidence_identity_values,
            claim_boundary_identity_values=self.claim_boundary_identity_values,
        )
        for name, value, expected in (
            ("workflow_identity", self.workflow_identity, WorkflowIdentity),
            (
                "workflow_run_identity",
                self.workflow_run_identity,
                WorkflowRunIdentity,
            ),
            (
                "task_instance_identity",
                self.task_instance_identity,
                TaskInstanceIdentity,
            ),
            (
                "task_activation_identity",
                self.task_activation_identity,
                TaskActivationIdentity,
            ),
            ("attempt_identity", self.attempt_identity, AttemptIdentity),
            (
                "result_object_identity",
                self.result_object_identity,
                ResultObjectIdentity,
            ),
        ):
            if type(value) is not expected:
                raise TypeError(f"{name} must be a {expected.__name__}")
        if (
            type(self.result_artifact_relation_identity)
            is not ResultArtifactRelationIdentity
        ):
            raise TypeError(
                "result_artifact_relation_identity must be a "
                "ResultArtifactRelationIdentity"
            )


@dataclass(frozen=True, slots=True)
class ExternalSourceObservation:
    """Producer provenance for bytes observed outside a represented Workflow.

    Parameters
    ----------
    identity, schema_version, kind
        Provenance identity, exact version ``1``, and mandatory discriminator
        :attr:`ArtifactProducerKind.EXTERNAL_SOURCE_OBSERVATION`.
    artifact_identity, content_identity
        Enclosing artifact identity and already-observed SHA-256/byte-count identity.
    evidence_identity_values, claim_boundary_identity_values
        Nonempty, unique, lexically sorted evidence and claim-boundary identities.
    external_producer_identity, producer_attempt_identity
        Authoritative external producer and its exact attempt identities.
    external_artifact_identity, external_result_identity
        Upstream artifact and/or result identity.  At least one must be present.
    source_observation_identity
        Exact identity of the observation that acquired the represented values.
    source_revision, observed_at
        Optional known external revision and RFC 3339 UTC second timestamp.
    observation_method_identity, observation_receipt_identity
        Exact identities of the observation method and retained receipt.
    workflow_context_unavailable_reason
        Nonempty reason Workflow/run/Task/activation identities are unavailable rather
        than fabricated.
    limitation_values
        Nonempty tuple of explicit source-observation limitations in caller order.

    Notes
    -----
    This variant is for a producer genuinely outside the represented Workflow.  It
    cannot be used to invent Workflow lineage for historical or third-party bytes.
    """

    identity: ArtifactProducerProvenanceIdentity
    schema_version: int
    kind: ArtifactProducerKind
    artifact_identity: ArtifactIdentity
    content_identity: ArtifactContentIdentity
    evidence_identity_values: tuple[str, ...]
    claim_boundary_identity_values: tuple[str, ...]
    external_producer_identity: str
    producer_attempt_identity: str
    external_artifact_identity: str | None
    external_result_identity: str | None
    source_observation_identity: str
    source_revision: str | None
    observed_at: str | None
    observation_method_identity: str
    observation_receipt_identity: str
    workflow_context_unavailable_reason: str
    limitation_values: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate external observation identity and explicit unavailability."""
        _require_common_provenance(
            identity=self.identity,
            schema_version=self.schema_version,
            kind=self.kind,
            expected_kind=ArtifactProducerKind.EXTERNAL_SOURCE_OBSERVATION,
            artifact_identity=self.artifact_identity,
            content_identity=self.content_identity,
            evidence_identity_values=self.evidence_identity_values,
            claim_boundary_identity_values=self.claim_boundary_identity_values,
        )
        for name, value in (
            ("external_producer_identity", self.external_producer_identity),
            ("producer_attempt_identity", self.producer_attempt_identity),
            ("source_observation_identity", self.source_observation_identity),
            ("observation_method_identity", self.observation_method_identity),
            ("observation_receipt_identity", self.observation_receipt_identity),
            (
                "workflow_context_unavailable_reason",
                self.workflow_context_unavailable_reason,
            ),
        ):
            _require_identity(value, name)
        _require_optional_identity(
            self.external_artifact_identity,
            "external_artifact_identity",
        )
        _require_optional_identity(
            self.external_result_identity,
            "external_result_identity",
        )
        if (
            self.external_artifact_identity is None
            and self.external_result_identity is None
        ):
            raise ValueError(
                "external_artifact_identity or external_result_identity is required"
            )
        _require_optional_identity(self.source_revision, "source_revision")
        if self.observed_at is not None:
            if type(self.observed_at) is not str:
                raise TypeError("observed_at must be a built-in str or None")
            if _TIMESTAMP_PATTERN.fullmatch(self.observed_at) is None:
                raise ValueError("observed_at must be an RFC 3339 UTC second timestamp")
            try:
                datetime.strptime(self.observed_at, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError as error:
                raise ValueError(
                    "observed_at must be a real UTC calendar timestamp"
                ) from error
        if type(self.limitation_values) is not tuple:
            raise TypeError("limitation_values must be a built-in tuple")
        if not self.limitation_values:
            raise ValueError("limitation_values must not be empty")
        for limitation in self.limitation_values:
            _require_identity(limitation, "limitation_values member")


@dataclass(frozen=True, slots=True)
class ImportedRetainedFixture:
    """Producer provenance for a retained fixture imported from an identified source.

    Parameters
    ----------
    identity, schema_version, kind
        Provenance identity, version ``1``, and mandatory
        :attr:`ArtifactProducerKind.IMPORTED_RETAINED_FIXTURE` discriminator.
    artifact_identity, content_identity
        Fixture artifact and already-observed SHA-256/byte-count identities.
    evidence_identity_values, claim_boundary_identity_values
        Nonempty, unique, lexically sorted evidence and claim-boundary identities.
    fixture_identity, fixture_revision
        Exact fixture and revision identities.
    source_identity, source_reference
        Exact retained source identity and nonempty portable reference text.
    import_identity, import_receipt_identity
        Exact import operation and retained receipt identities.
    retained_source_identity
        Exact retained source identity copied from the source boundary.
    retained_content_identity
        Exact retained source content identity, distinct from the imported fixture
        artifact's content identity when the import changes bytes.
    retained_checksum_identity
        Exact retained checksum identity copied from the source boundary.
    retained_provenance_identity
        Exact retained provenance identity copied from the source boundary.
    evidence_classification
        Nonempty evidence-classification identity retained without upgrade.
    """

    identity: ArtifactProducerProvenanceIdentity
    schema_version: int
    kind: ArtifactProducerKind
    artifact_identity: ArtifactIdentity
    content_identity: ArtifactContentIdentity
    evidence_identity_values: tuple[str, ...]
    claim_boundary_identity_values: tuple[str, ...]
    fixture_identity: str
    fixture_revision: str
    source_identity: str
    source_reference: str
    import_identity: str
    import_receipt_identity: str
    retained_source_identity: str
    retained_content_identity: ArtifactContentIdentity
    retained_checksum_identity: str
    retained_provenance_identity: str
    evidence_classification: str

    def __post_init__(self) -> None:
        """Validate retained fixture, source, import, and evidence identities."""
        _require_common_provenance(
            identity=self.identity,
            schema_version=self.schema_version,
            kind=self.kind,
            expected_kind=ArtifactProducerKind.IMPORTED_RETAINED_FIXTURE,
            artifact_identity=self.artifact_identity,
            content_identity=self.content_identity,
            evidence_identity_values=self.evidence_identity_values,
            claim_boundary_identity_values=self.claim_boundary_identity_values,
        )
        for name, value in (
            ("fixture_identity", self.fixture_identity),
            ("fixture_revision", self.fixture_revision),
            ("source_identity", self.source_identity),
            ("source_reference", self.source_reference),
            ("import_identity", self.import_identity),
            ("import_receipt_identity", self.import_receipt_identity),
            ("retained_source_identity", self.retained_source_identity),
            ("retained_checksum_identity", self.retained_checksum_identity),
            ("retained_provenance_identity", self.retained_provenance_identity),
            ("evidence_classification", self.evidence_classification),
        ):
            _require_identity(value, name)
        if type(self.retained_content_identity) is not ArtifactContentIdentity:
            raise TypeError(
                "retained_content_identity must be an ArtifactContentIdentity"
            )


@dataclass(frozen=True, slots=True)
class HumanAuthoredCompactInput:
    """Producer provenance for compact input authored by identified human authority.

    Parameters
    ----------
    identity, schema_version, kind
        Provenance identity, version ``1``, and mandatory
        :attr:`ArtifactProducerKind.HUMAN_AUTHORED_COMPACT_INPUT` discriminator.
    artifact_identity, content_identity
        Compact artifact and already-observed SHA-256/byte-count identities.
    evidence_identity_values, claim_boundary_identity_values
        Nonempty, unique, lexically sorted evidence and claim-boundary identities.
    compact_input_identity, compact_input_revision
        Exact authored-input and revision identities.
    author_identity_values
        Nonempty, unique, lexically sorted identities of represented authors.
    authorship_authority_identity
        Exact authority boundary under which authorship is represented.
    source_identity, review_identity
        Optional exact source and review identities when applicable.
    authorship_record_identity
        Exact retained authorship record identity.

    Notes
    -----
    Authorship is not calculator execution, scientific validation, or Workflow result
    production.  No Workflow/run/Task/result fields exist on this variant.
    """

    identity: ArtifactProducerProvenanceIdentity
    schema_version: int
    kind: ArtifactProducerKind
    artifact_identity: ArtifactIdentity
    content_identity: ArtifactContentIdentity
    evidence_identity_values: tuple[str, ...]
    claim_boundary_identity_values: tuple[str, ...]
    compact_input_identity: str
    compact_input_revision: str
    author_identity_values: tuple[str, ...]
    authorship_authority_identity: str
    source_identity: str | None
    review_identity: str | None
    authorship_record_identity: str

    def __post_init__(self) -> None:
        """Validate compact-input authorship and optional source/review identities."""
        _require_common_provenance(
            identity=self.identity,
            schema_version=self.schema_version,
            kind=self.kind,
            expected_kind=ArtifactProducerKind.HUMAN_AUTHORED_COMPACT_INPUT,
            artifact_identity=self.artifact_identity,
            content_identity=self.content_identity,
            evidence_identity_values=self.evidence_identity_values,
            claim_boundary_identity_values=self.claim_boundary_identity_values,
        )
        _require_identity(self.compact_input_identity, "compact_input_identity")
        _require_identity(self.compact_input_revision, "compact_input_revision")
        _require_identity_tuple(self.author_identity_values, "author_identity_values")
        _require_identity(
            self.authorship_authority_identity,
            "authorship_authority_identity",
        )
        _require_optional_identity(self.source_identity, "source_identity")
        _require_optional_identity(self.review_identity, "review_identity")
        _require_identity(
            self.authorship_record_identity,
            "authorship_record_identity",
        )


@dataclass(frozen=True, slots=True)
class UnknownLegacyProducer:
    """Explicitly limited producer provenance for an incompletely known artifact.

    Parameters
    ----------
    identity, schema_version, kind
        Provenance identity, version ``1``, and mandatory
        :attr:`ArtifactProducerKind.UNKNOWN_LEGACY` discriminator.
    artifact_identity, content_identity
        Legacy artifact and already-observed SHA-256/byte-count identities.
    evidence_identity_values, claim_boundary_identity_values
        Nonempty, unique, lexically sorted identities for all known evidence and claim
        boundaries.  Unknown facts must not be replaced by invented identities.
    reason
        Nonempty reason complete producer provenance is unavailable.
    limitation_values
        Nonempty immutable tuple of explicit limitations, preserving caller order.
    claim_status
        Nonempty bounded claim-status identity.

    Notes
    -----
    This variant cannot upgrade the artifact's evidence status.  It contains no
    Workflow, Task, fixture, external-producer, or human-authorship fields.
    """

    identity: ArtifactProducerProvenanceIdentity
    schema_version: int
    kind: ArtifactProducerKind
    artifact_identity: ArtifactIdentity
    content_identity: ArtifactContentIdentity
    evidence_identity_values: tuple[str, ...]
    claim_boundary_identity_values: tuple[str, ...]
    reason: str
    limitation_values: tuple[str, ...]
    claim_status: str

    def __post_init__(self) -> None:
        """Validate explicit legacy uncertainty, limitations, and claim status."""
        _require_common_provenance(
            identity=self.identity,
            schema_version=self.schema_version,
            kind=self.kind,
            expected_kind=ArtifactProducerKind.UNKNOWN_LEGACY,
            artifact_identity=self.artifact_identity,
            content_identity=self.content_identity,
            evidence_identity_values=self.evidence_identity_values,
            claim_boundary_identity_values=self.claim_boundary_identity_values,
        )
        _require_identity(self.reason, "reason")
        if type(self.limitation_values) is not tuple:
            raise TypeError("limitation_values must be a built-in tuple")
        if not self.limitation_values:
            raise ValueError("limitation_values must not be empty")
        for limitation in self.limitation_values:
            _require_identity(limitation, "limitation_values member")
        _require_identity(self.claim_status, "claim_status")


type ArtifactProducerProvenance = (
    RepresentedWorkflowProducer
    | ExternalSourceObservation
    | ImportedRetainedFixture
    | HumanAuthoredCompactInput
    | UnknownLegacyProducer
)
"""Closed producer-provenance union for Workflow-owned artifact manifests."""


@dataclass(frozen=True, slots=True)
class ArtifactManifestEntry:
    """One immutable portable artifact inventory entry.

    Parameters
    ----------
    identity
        Exact manifest-entry identity referenced by downstream consumers.
    artifact_identity, content_identity
        Nominal artifact identity and already-observed exact SHA-256/byte-count
        identity.
    native_format, semantic_role, retention_classification
        Nonempty format, role, and retention identifiers.  Retention metadata grants
        no deletion, transfer, publication, or access authority.
    parent_artifact_identities
        Unique artifact parents sorted lexically by ``ArtifactIdentity.value``.  The
        entry cannot name itself as a parent.
    portable_store_reference
        Optional normalized relative POSIX reference.  Absolute, home-relative,
        parent-traversing, and platform-native paths are rejected.
    lineage_relations
        Unique explicit lineage relations sorted by relation identity.  Every target
        must equal this entry's artifact identity.  Represented Workflow producers
        require selection and result-production relations; execution grant/snapshot,
        process-observation, and result-ingress relations close as one applicable set.
    producer_provenance
        Exactly one concrete member of :data:`ArtifactProducerProvenance`.  Its
        artifact and content identities must equal this entry exactly.

    Raises
    ------
    TypeError
        If a field or concrete producer variant has the wrong semantic type.
    ValueError
        If identities disagree, parent ordering is invalid, or a local invariant is
        violated.
    """

    identity: ArtifactManifestEntryIdentity
    artifact_identity: ArtifactIdentity
    content_identity: ArtifactContentIdentity
    native_format: str
    semantic_role: str
    retention_classification: str
    parent_artifact_identities: tuple[ArtifactIdentity, ...]
    portable_store_reference: str | None
    lineage_relations: tuple[ArtifactLineageRelation, ...]
    producer_provenance: ArtifactProducerProvenance

    def __post_init__(self) -> None:
        """Validate one closed entry and its exact producer correlation."""
        if type(self.identity) is not ArtifactManifestEntryIdentity:
            raise TypeError("identity must be an ArtifactManifestEntryIdentity")
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be an ArtifactIdentity")
        if type(self.content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be an ArtifactContentIdentity")
        for name, value in (
            ("native_format", self.native_format),
            ("semantic_role", self.semantic_role),
            ("retention_classification", self.retention_classification),
        ):
            _require_identity(value, name)
        if type(self.parent_artifact_identities) is not tuple or any(
            type(value) is not ArtifactIdentity
            for value in self.parent_artifact_identities
        ):
            raise TypeError(
                "parent_artifact_identities must be a tuple of ArtifactIdentity"
            )
        ordered = tuple(
            sorted(self.parent_artifact_identities, key=lambda value: value.value)
        )
        if self.parent_artifact_identities != ordered or len(
            set(self.parent_artifact_identities)
        ) != len(self.parent_artifact_identities):
            raise ValueError(
                "parent_artifact_identities must be unique and lexically sorted"
            )
        if self.artifact_identity in self.parent_artifact_identities:
            raise ValueError("an artifact entry must not name itself as a parent")
        if self.portable_store_reference is not None:
            _require_portable_reference(
                self.portable_store_reference,
                "portable_store_reference",
            )
        if type(self.lineage_relations) is not tuple or any(
            type(value) is not ArtifactLineageRelation
            for value in self.lineage_relations
        ):
            raise TypeError(
                "lineage_relations must be a tuple of ArtifactLineageRelation"
            )
        ordered_relations = tuple(
            sorted(self.lineage_relations, key=lambda value: value.identity.value)
        )
        relation_identities = tuple(value.identity for value in self.lineage_relations)
        if self.lineage_relations != ordered_relations or len(
            set(relation_identities)
        ) != len(relation_identities):
            raise ValueError(
                "lineage_relations must have unique lexically sorted identities"
            )
        if any(
            relation.target_artifact_identity != self.artifact_identity
            for relation in self.lineage_relations
        ):
            raise ValueError("lineage relation target must equal entry artifact")
        variants = (
            RepresentedWorkflowProducer,
            ExternalSourceObservation,
            ImportedRetainedFixture,
            HumanAuthoredCompactInput,
            UnknownLegacyProducer,
        )
        if type(self.producer_provenance) not in variants:
            raise TypeError(
                "producer_provenance must be one exact ArtifactProducerProvenance "
                "variant"
            )
        if self.producer_provenance.artifact_identity != self.artifact_identity:
            raise ValueError("producer artifact identity must equal entry identity")
        if self.producer_provenance.content_identity != self.content_identity:
            raise ValueError("producer content identity must equal entry content")
        if type(self.producer_provenance) is RepresentedWorkflowProducer:
            by_kind = {relation.kind: relation for relation in self.lineage_relations}
            required = {
                ArtifactLineageKind.CPN_SELECTION,
                ArtifactLineageKind.RESULT_PRODUCTION,
            }
            if not required.issubset(by_kind) or any(
                sum(relation.kind is kind for relation in self.lineage_relations) != 1
                for kind in required
            ):
                raise ValueError(
                    "represented Workflow producer requires exactly one CPN selection "
                    "and result-production lineage relation"
                )
            production_kinds = required | {
                ArtifactLineageKind.EXECUTION_GRANT,
                ArtifactLineageKind.EXECUTION_AUTHORITY_SNAPSHOT,
                ArtifactLineageKind.PROCESS_OBSERVATION,
                ArtifactLineageKind.RESULT_INGRESS,
            }
            production_relations = tuple(
                relation
                for relation in self.lineage_relations
                if relation.kind in production_kinds
            )
            if any(
                relation.workflow_run_identity
                != self.producer_provenance.workflow_run_identity
                or relation.operation_attempt_identity
                != self.producer_provenance.attempt_identity
                for relation in production_relations
            ):
                raise ValueError(
                    "production lineage run and attempt must equal producer lineage"
                )
            if (
                by_kind[ArtifactLineageKind.CPN_SELECTION].source_identity.value
                != self.producer_provenance.task_activation_identity.value
            ):
                raise ValueError(
                    "CPN selection source must equal TaskActivation identity"
                )
            if (
                by_kind[ArtifactLineageKind.RESULT_PRODUCTION].source_identity.value
                != self.producer_provenance.result_artifact_relation_identity.value
            ):
                raise ValueError(
                    "result-production source must equal result-artifact relation"
                )
            execution_kinds = {
                ArtifactLineageKind.EXECUTION_GRANT,
                ArtifactLineageKind.EXECUTION_AUTHORITY_SNAPSHOT,
                ArtifactLineageKind.PROCESS_OBSERVATION,
                ArtifactLineageKind.RESULT_INGRESS,
            }
            present_execution_kinds = execution_kinds.intersection(by_kind)
            if present_execution_kinds and (
                present_execution_kinds != execution_kinds
                or any(
                    sum(relation.kind is kind for relation in self.lineage_relations)
                    != 1
                    for kind in execution_kinds
                )
            ):
                raise ValueError(
                    "applicable execution lineage requires grant, authority snapshot, "
                    "process observation, and result ingress"
                )


@dataclass(frozen=True, slots=True)
class ArtifactManifest:
    """One immutable portable artifact-manifest revision.

    Parameters
    ----------
    identity
        Nominal identity of this exact manifest revision.
    revision
        Positive built-in integer revision in :math:`[1,2^{64}-1]`.  Booleans and
        numeric strings are rejected.
    predecessor_manifest_identity, supersession_identity
        Both are absent for revision 1 and required for every later revision.  The
        predecessor must differ from ``identity``.  A correction therefore creates a
        new manifest and exact supersession relation rather than rewriting history.
    workflow_identity, workflow_run_identity
        Exact owner Workflow and represented run identities.  Producer provenance
        remains separately variant-specific for each entry.
    evidence_identity_values
        Nonempty, unique, lexically sorted closure index containing exactly every
        evidence identity referenced by entry producers and lineage relations.
    entries
        Nonempty tuple with unique entry/artifact identities, sorted lexically by
        manifest-entry identity.  Every parent artifact must be present, and the
        included parent graph must be acyclic.

    Notes
    -----
    Construction validates manifest-local closure only.  It does not locate artifacts,
    observe bytes, validate formats, resolve references, verify external evidence
    existence, serialize, persist, or perform retention actions.
    """

    identity: ArtifactManifestIdentity
    revision: int
    predecessor_manifest_identity: ArtifactManifestIdentity | None
    supersession_identity: ArtifactManifestSupersessionIdentity | None
    workflow_identity: WorkflowIdentity
    workflow_run_identity: WorkflowRunIdentity
    evidence_identity_values: tuple[str, ...]
    entries: tuple[ArtifactManifestEntry, ...]

    def __post_init__(self) -> None:
        """Validate owner/run correlation, revision lineage, and entry closure."""
        if type(self.identity) is not ArtifactManifestIdentity:
            raise TypeError("identity must be an ArtifactManifestIdentity")
        if type(self.revision) is not int:
            raise TypeError("revision must be a built-in int excluding bool")
        if not 1 <= self.revision <= _MAX_U64:
            raise ValueError("revision must be in the range [1, 2^64-1]")
        if self.predecessor_manifest_identity is not None and (
            type(self.predecessor_manifest_identity) is not ArtifactManifestIdentity
        ):
            raise TypeError(
                "predecessor_manifest_identity must be an "
                "ArtifactManifestIdentity or None"
            )
        if self.supersession_identity is not None and (
            type(self.supersession_identity) is not ArtifactManifestSupersessionIdentity
        ):
            raise TypeError(
                "supersession_identity must be an "
                "ArtifactManifestSupersessionIdentity or None"
            )
        if self.revision == 1 and (
            self.predecessor_manifest_identity is not None
            or self.supersession_identity is not None
        ):
            raise ValueError(
                "predecessor_manifest_identity and supersession_identity must be "
                "absent for revision 1"
            )
        if self.revision > 1 and (
            self.predecessor_manifest_identity is None
            or self.supersession_identity is None
        ):
            raise ValueError(
                "predecessor_manifest_identity and supersession_identity are "
                "required after revision 1"
            )
        if self.predecessor_manifest_identity == self.identity:
            raise ValueError("a manifest revision must not name itself as predecessor")
        if type(self.workflow_identity) is not WorkflowIdentity:
            raise TypeError("workflow_identity must be a WorkflowIdentity")
        if type(self.workflow_run_identity) is not WorkflowRunIdentity:
            raise TypeError("workflow_run_identity must be a WorkflowRunIdentity")
        _require_identity_tuple(
            self.evidence_identity_values,
            "evidence_identity_values",
        )
        if type(self.entries) is not tuple or any(
            type(value) is not ArtifactManifestEntry for value in self.entries
        ):
            raise TypeError("entries must be a tuple of ArtifactManifestEntry")
        if not self.entries:
            raise ValueError("entries must not be empty")
        ordered = tuple(sorted(self.entries, key=lambda value: value.identity.value))
        entry_identities = tuple(value.identity for value in self.entries)
        artifact_identities = tuple(value.artifact_identity for value in self.entries)
        if (
            self.entries != ordered
            or len(set(entry_identities)) != len(entry_identities)
            or len(set(artifact_identities)) != len(artifact_identities)
        ):
            raise ValueError(
                "entries must have unique lexically sorted entry identities and "
                "unique artifact identities"
            )
        evidence = {
            evidence_identity
            for entry in self.entries
            for evidence_identity in entry.producer_provenance.evidence_identity_values
        }
        evidence.update(
            evidence_identity
            for entry in self.entries
            for relation in entry.lineage_relations
            for evidence_identity in relation.evidence_identity_values
        )
        if self.evidence_identity_values != tuple(sorted(evidence)):
            raise ValueError(
                "evidence_identity_values must exactly close entry evidence references"
            )
        entries_by_artifact = {entry.artifact_identity: entry for entry in self.entries}
        if any(
            parent not in entries_by_artifact
            for entry in self.entries
            for parent in entry.parent_artifact_identities
        ):
            raise ValueError(
                "every parent artifact identity must have a manifest entry"
            )
        unresolved_parents = {
            entry.artifact_identity: set(entry.parent_artifact_identities)
            for entry in self.entries
        }
        while unresolved_parents:
            roots = {
                artifact_identity
                for artifact_identity, parents in unresolved_parents.items()
                if not parents
            }
            if not roots:
                raise ValueError("manifest parent artifact graph must be acyclic")
            unresolved_parents = {
                artifact_identity: parents - roots
                for artifact_identity, parents in unresolved_parents.items()
                if artifact_identity not in roots
            }
