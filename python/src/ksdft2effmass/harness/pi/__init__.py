"""Generic, explicit-input PI harness contract.

The root package exports generic records, results, and fieldless actions plus the
public :mod:`conformance` domain package. It performs no implicit repository,
current-directory, Git, or ``.pi`` discovery; filesystem actions require an explicit
root and exact paths.
"""

from __future__ import annotations

from typing import TypeAlias

from . import conformance as conformance
from .checkpoints import (
    CheckpointDecisionResolutionRequest,
    CheckpointDecisionResolutionResult,
    CheckpointDecisionResolver,
    CheckpointRecord,
    CheckpointSetValidator,
)
from .checksums import ChecksumEntry, ChecksumManifest, ChecksumManifestValidator
from .configuration import (
    PiHarnessAgentDefinition,
    PiHarnessAgentDefinitionResolver,
    PiHarnessConfiguration,
    PiHarnessConfigurationDeserializer,
)
from .human_review import (
    HumanReviewDecision,
    HumanReviewDecisionRecorder,
    HumanReviewFinding,
    HumanReviewObservation,
    HumanReviewPacket,
    HumanReviewPreparer,
    HumanReviewTarget,
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
from .ownership import AgentDescriptorView, OwnershipManifestView, OwnershipScope
from .profiles import ProjectProfile, ProjectProfileLoader
from .resources import (
    ResourceManifest,
    ResourceManifestRefresher,
    ResourceManifestRefreshRequest,
    ResourceManifestRefreshResult,
    ResourceManifestValidator,
    ResourceReference,
    ResourceResolver,
    SkillDescriptor,
    SkillResourceValidator,
)
from .task_state import TaskStateInspectionRequest as TaskStateInspectionRequest
from .task_state import TaskStateInspectionResult as TaskStateInspectionResult
from .task_state import TaskStateInspector as TaskStateInspector
from .validation import (
    JsonDeserializationResult,
    JsonRecordDeserializer,
    JsonRecordSerializer,
    JsonSerializationResult,
    ProjectProfileLoadResult,
    ResourceResolutionResult,
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
    | ChecksumEntry
    | ChecksumManifest
    | ValidationIssue
    | ValidationResult
)

# Resolve annotations that cross module cycles only after every concrete record
# exists. These are aliases, not registries or runtime extension points.
from . import checkpoints as _checkpoints_module  # noqa: E402
from . import validation as _validation_module  # noqa: E402

_validation_module.HarnessWireRecord = HarnessWireRecord
_checkpoints_module.ProjectProfile = ProjectProfile  # type: ignore[misc]

__all__ = (
    "ArtifactIdentity",
    "ResourceReference",
    "ResourceManifest",
    "ResourceManifestRefreshRequest",
    "ProjectProfile",
    "SkillDescriptor",
    "OwnershipScope",
    "AgentDescriptorView",
    "PiHarnessConfiguration",
    "PiHarnessAgentDefinition",
    "conformance",
    "HumanReviewTarget",
    "HumanReviewObservation",
    "HumanReviewFinding",
    "HumanReviewPacket",
    "HumanReviewDecision",
    "OwnershipManifestView",
    "CheckpointRecord",
    "CheckpointDecisionResolutionRequest",
    "ChecksumEntry",
    "ChecksumManifest",
    "TaskStateInspectionRequest",
    "ValidationIssue",
    "ValidationResult",
    "ProjectProfileLoadResult",
    "ResourceResolutionResult",
    "TaskStateInspectionResult",
    "ResourceManifestRefreshResult",
    "CheckpointDecisionResolutionResult",
    "JsonSerializationResult",
    "JsonDeserializationResult",
    "WireRecordKind",
    "HarnessWireRecord",
    "HarnessInternalError",
    "JsonRecordSerializer",
    "JsonRecordDeserializer",
    "PiHarnessConfigurationDeserializer",
    "PiHarnessAgentDefinitionResolver",
    "ProjectProfileLoader",
    "ResourceManifestRefresher",
    "ResourceResolver",
    "ResourceManifestValidator",
    "CheckpointDecisionResolver",
    "CheckpointSetValidator",
    "HumanReviewPreparer",
    "HumanReviewDecisionRecorder",
    "TaskStateInspector",
    "ChecksumManifestValidator",
    "SkillResourceValidator",
    "Identifier",
    "ResourcePath",
    "OwnershipScopePath",
    "DiagnosticPath",
    "Version",
)
