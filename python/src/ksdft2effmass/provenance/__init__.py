"""Portable provenance and external-tool lifecycle public API.

The package exposes immutable DataObjects and ResultObjects, stateless
ActionObjects, and a strict version-1 JSON boundary.  It performs no filesystem,
network, process, tool-discovery, workflow-engine, or scientific computation.
"""

from .actions import (
    ArtifactIdentityVerificationResult,
    ArtifactIdentityVerificationStatus,
    ArtifactIdentityVerifier,
    CorrelationIssue,
    CorrelationStatus,
    ExecutionCorrelationResult,
    ExecutionOutcomeCorrelator,
)
from .records import (
    ArtifactIdentity,
    ArtifactLocation,
    ArtifactLocationKind,
    ArtifactReference,
    ArtifactSpecification,
    LineageKind,
    LineageRelation,
    ManifestState,
    ProvenanceRecord,
    RunManifest,
)
from .serialization import ProvenanceJsonError, ProvenanceJsonSerializer
from .tools import (
    CapabilityKind,
    DeclaredCapability,
    ExternalExecutionFailure,
    ExternalExecutionRequest,
    ExternalExecutionResult,
    ExternalExecutionStatus,
    ExternalFailureCode,
    ExternalFailureStage,
    ExternalToolIdentity,
    ExternalToolSpecification,
    InstallationObservation,
    VerificationObservation,
    VerificationStatus,
)

__all__ = (
    "ArtifactIdentity",
    "ArtifactIdentityVerificationResult",
    "ArtifactIdentityVerificationStatus",
    "ArtifactIdentityVerifier",
    "ArtifactLocation",
    "ArtifactLocationKind",
    "ArtifactReference",
    "ArtifactSpecification",
    "CapabilityKind",
    "CorrelationIssue",
    "CorrelationStatus",
    "DeclaredCapability",
    "ExecutionCorrelationResult",
    "ExecutionOutcomeCorrelator",
    "ExternalExecutionFailure",
    "ExternalExecutionRequest",
    "ExternalExecutionResult",
    "ExternalExecutionStatus",
    "ExternalFailureCode",
    "ExternalFailureStage",
    "ExternalToolIdentity",
    "ExternalToolSpecification",
    "InstallationObservation",
    "LineageKind",
    "LineageRelation",
    "ManifestState",
    "ProvenanceJsonError",
    "ProvenanceJsonSerializer",
    "ProvenanceRecord",
    "RunManifest",
    "VerificationObservation",
    "VerificationStatus",
)
