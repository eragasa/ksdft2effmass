"""Generic, explicit-input PI harness contract.

The package exports immutable concrete records/results and fieldless action
objects only.  It performs no repository, current-directory, Git, or ``.pi``
discovery.
"""

from __future__ import annotations

from typing import TypeAlias

from .chains import ChainView, EvaluateChainState, TaskReference
from .checkpoints import CheckpointRecord, ValidateCheckpointSet
from .checksums import ChecksumEntry, ChecksumManifest, ValidateChecksumManifest
from .evidence import AuditEvidenceIdentifiers, EvidenceIdentifierOccurrence
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
    ResolveResource,
    ResourceManifest,
    ResourceReference,
    SkillDescriptor,
    ValidateResourceManifest,
    ValidateSkillResources,
)
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
    "ProjectProfile",
    "SkillDescriptor",
    "OwnershipScope",
    "AgentDescriptorView",
    "EvidenceIdentifierOccurrence",
    "OwnershipManifestView",
    "CheckpointRecord",
    "TaskReference",
    "ChainView",
    "ChecksumEntry",
    "ChecksumManifest",
    "ValidationIssue",
    "ValidationResult",
    "ProjectProfileLoadResult",
    "ResourceResolutionResult",
    "ChainEvaluationResult",
    "EvidenceAuditResult",
    "JsonSerializationResult",
    "JsonDeserializationResult",
    "WireRecordKind",
    "HarnessWireRecord",
    "HarnessInternalError",
    "SerializeJsonRecord",
    "DeserializeJsonRecord",
    "LoadProjectProfile",
    "ResolveResource",
    "ValidateResourceManifest",
    "ValidateOwnershipManifest",
    "ValidateCheckpointSet",
    "EvaluateChainState",
    "AuditEvidenceIdentifiers",
    "ValidateChecksumManifest",
    "ValidateSkillResources",
    "Identifier",
    "ResourcePath",
    "OwnershipScopePath",
    "DiagnosticPath",
    "Version",
)
