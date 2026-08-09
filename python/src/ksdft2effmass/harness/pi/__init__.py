"""Generic, explicit-input PI harness contract.

The package exports immutable concrete records/results and fieldless action
objects only. It performs no implicit repository, current-directory, Git, or
``.pi`` discovery; filesystem actions require an explicit root and exact paths.
"""

from __future__ import annotations

from typing import TypeAlias

from .chains import ChainView, EvaluateChainState, TaskReference
from .checkpoints import (
    CheckpointDecisionResolutionRequest,
    CheckpointDecisionResolutionResult,
    CheckpointRecord,
    ResolveCheckpointDecision,
    ValidateCheckpointSet,
)
from .checksums import ChecksumEntry, ChecksumManifest, ValidateChecksumManifest
from .evidence import AuditEvidenceIdentifiers, EvidenceIdentifierOccurrence
from .human_review import (
    HumanReviewDecision,
    HumanReviewFinding,
    HumanReviewObservation,
    HumanReviewPacket,
    HumanReviewPreparer,
    HumanReviewTarget,
    RecordHumanReviewDecision,
)
from .identity import (
    ArtifactIdentity,
    DiagnosticPath,
    HarnessInternalError,
    Identifier,
    OwnershipScopePath,
    ResourcePath,
    Version,
)
from .ownership import (
    AgentDescriptorView,
    OwnershipManifestView,
    OwnershipScope,
    ValidateOwnershipManifest,
)
from .profiles import LoadProjectProfile, ProjectProfile
from .resources import (
    RefreshResourceManifest,
    ResolveResource,
    ResourceManifest,
    ResourceManifestRefreshRequest,
    ResourceManifestRefreshResult,
    ResourceReference,
    SkillDescriptor,
    ValidateResourceManifest,
    ValidateSkillResources,
)
from .task_state import InspectTaskState as InspectTaskState
from .task_state import TaskStateInspectionRequest as TaskStateInspectionRequest
from .task_state import TaskStateInspectionResult as TaskStateInspectionResult
from .test_evidence import PythonTestEvidenceFinding as PythonTestEvidenceFinding
from .test_evidence import PythonTestEvidenceRequest as PythonTestEvidenceRequest
from .test_evidence import PythonTestEvidenceSource as PythonTestEvidenceSource
from .test_evidence import (
    PythonTestEvidenceValidationResult as PythonTestEvidenceValidationResult,
)
from .test_evidence import ValidatePythonTestEvidence as ValidatePythonTestEvidence
from .validation import (
    ChainEvaluationResult,
    DeserializeJsonRecord,
    EvidenceAuditResult,
    JsonDeserializationResult,
    JsonSerializationResult,
    ProjectProfileLoadResult,
    ResourceResolutionResult,
    SerializeJsonRecord,
    ValidationIssue,
    ValidationResult,
    WireRecordKind,
)

HarnessWireRecord: TypeAlias = (  # noqa: UP040 - public typing union on 3.11+
    ArtifactIdentity
    | ResourceReference
    | ResourceManifest
    | ProjectProfile
    | SkillDescriptor
    | OwnershipScope
    | AgentDescriptorView
    | OwnershipManifestView
    | CheckpointRecord
    | TaskReference
    | ChainView
    | ChecksumEntry
    | ChecksumManifest
    | EvidenceIdentifierOccurrence
    | ValidationIssue
    | ValidationResult
)

# Resolve annotations that cross module cycles only after every concrete record
# exists. These are aliases, not registries or runtime extension points.
from . import chains as _chains_module  # noqa: E402
from . import checkpoints as _checkpoints_module  # noqa: E402
from . import evidence as _evidence_module  # noqa: E402
from . import ownership as _ownership_module  # noqa: E402
from . import resources as _resources_module  # noqa: E402
from . import validation as _validation_module  # noqa: E402

_validation_module.HarnessWireRecord = HarnessWireRecord
_resources_module.ProjectProfile = ProjectProfile  # type: ignore[misc]
_ownership_module.ChainView = ChainView  # type: ignore[misc]
_ownership_module.ProjectProfile = ProjectProfile  # type: ignore[misc]
_checkpoints_module.ProjectProfile = ProjectProfile  # type: ignore[misc]
_chains_module.ProjectProfile = ProjectProfile  # type: ignore[misc]
_evidence_module.ProjectProfile = ProjectProfile  # type: ignore[misc]

__all__ = (
    "ArtifactIdentity",
    "ResourceReference",
    "ResourceManifest",
    "ResourceManifestRefreshRequest",
    "ProjectProfile",
    "SkillDescriptor",
    "OwnershipScope",
    "AgentDescriptorView",
    "EvidenceIdentifierOccurrence",
    "HumanReviewTarget",
    "HumanReviewObservation",
    "HumanReviewFinding",
    "HumanReviewPacket",
    "HumanReviewDecision",
    "OwnershipManifestView",
    "CheckpointRecord",
    "CheckpointDecisionResolutionRequest",
    "TaskReference",
    "ChainView",
    "ChecksumEntry",
    "ChecksumManifest",
    "PythonTestEvidenceSource",
    "PythonTestEvidenceRequest",
    "PythonTestEvidenceFinding",
    "TaskStateInspectionRequest",
    "ValidationIssue",
    "ValidationResult",
    "ProjectProfileLoadResult",
    "ResourceResolutionResult",
    "ChainEvaluationResult",
    "EvidenceAuditResult",
    "PythonTestEvidenceValidationResult",
    "TaskStateInspectionResult",
    "ResourceManifestRefreshResult",
    "CheckpointDecisionResolutionResult",
    "JsonSerializationResult",
    "JsonDeserializationResult",
    "WireRecordKind",
    "HarnessWireRecord",
    "HarnessInternalError",
    "SerializeJsonRecord",
    "DeserializeJsonRecord",
    "LoadProjectProfile",
    "RefreshResourceManifest",
    "ResolveResource",
    "ValidateResourceManifest",
    "ResolveCheckpointDecision",
    "ValidateOwnershipManifest",
    "ValidateCheckpointSet",
    "EvaluateChainState",
    "AuditEvidenceIdentifiers",
    "HumanReviewPreparer",
    "RecordHumanReviewDecision",
    "ValidatePythonTestEvidence",
    "InspectTaskState",
    "ValidateChecksumManifest",
    "ValidateSkillResources",
    "Identifier",
    "ResourcePath",
    "OwnershipScopePath",
    "DiagnosticPath",
    "Version",
)
