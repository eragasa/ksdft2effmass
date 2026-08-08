r"""Software verification of harness pi public api.

Facet and represented meaning
Software verification of the generic PI harness package import surface; no physical,
mathematical, or numerical object is represented.

Intrinsic and cross-object scope
The primary owner is the package public API artifact. The accepted maintained-tool
contracts provide the exact public-surface list used as the independent oracle.

VVUQ and scientific exclusions
Passing establishes import completeness and closure only, not numerical verification,
scientific validation, UQ, physical correctness, or release readiness.
"""

from __future__ import annotations

from typing import Any

import pytest

import ksdft2effmass.harness.pi as api

pytestmark = pytest.mark.software_verification


def test_public_api__exports__match_exact_h1_surface() -> None:
    """Evidence ID
    SV-HARNESS-039
    Requirement
    The package exports every and only the accepted maintained harness public names.
    Method
    Compare ``__all__`` and attribute availability with a literal transcription of
    the accepted surface.
    Oracle
    The accepted validator and task-state tool contracts expand the H1 surface with
    the exact records, results, and actions named below.
    Acceptance
    ``__all__`` equals the exact 60-name sequence and every listed attribute
    resolves from the public package.
    Interpretation
    Failure indicates source/public-contract drift or an incomplete package import.
    Limitations
    Import presence does not prove action semantics, documentation quality,
    scientific validity, UQ, or release status.
    """
    expected = (
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
        "PrepareHumanReviewPacket",
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
    assert api.__all__ == expected
    assert all(hasattr(api, name) for name in expected)


def test_public_api__action_instances__retain_no_mutable_state() -> None:
    """Evidence ID
    SV-HARNESS-040
    Requirement
    Every accepted ActionObject is concrete, fieldless, and stateless.
    Method
    Construct each exact public action and inspect its instance storage surface.
    Oracle
    The accepted maintained harness surface requires sixteen concrete actions with no
    roots, profiles, caches, clients, or mutable state.
    Acceptance
    Every instance lacks ``__dict__`` and its class declares empty slots.
    Interpretation
    Failure exposes an unauthorized retained-state or public-surface change.
    Limitations
    This structural check does not establish each action's relational behavior or
    any scientific claim.
    """
    names = (
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
        "PrepareHumanReviewPacket",
        "ValidatePythonTestEvidence",
        "InspectTaskState",
        "ValidateChecksumManifest",
        "ValidateSkillResources",
    )

    def assert_public_action_is_fieldless_and_stateless(name: Any) -> Any:
        """Evidence ID
        Owns no identifier; supports the enclosing stable evidence ID SV-HARNESS-040.
        Requirement
        Each action in the exact literal inventory satisfies the same fieldless and
        stateless public-action requirement.
        Method
        Construct the named action and mechanically apply the enclosing test's two
        storage assertions.
        Oracle
        The accepted inventory requires identical empty-slot instance structure for
        every listed action.
        Acceptance
        The instance has no ``__dict__`` and its class declares empty slots.
        Interpretation
        Failure identifies one listed action that violates the shared structural
        contract; this helper makes no independent evidence claim.
        Limitations
        The iteration mechanically applies one identical requirement, oracle, and
        acceptance rule across the exact literal inventory; it hides no distinct
        partition or action semantics.
        """
        instance = getattr(api, name)()
        assert not hasattr(instance, "__dict__")
        assert type(instance).__slots__ == ()

    _ = [assert_public_action_is_fieldless_and_stateless(name) for name in names]
