"""Evidence class and represented meaning
Software verification of the generic PI harness package import surface; no physical,
mathematical, or numerical object is represented.

Owned contract, oracle, and scope
The primary owner is the package public API artifact. The accepted H1 exact
public-surface list is the independent oracle.

VVUQ and scientific exclusions
Passing establishes import completeness and closure only, not numerical verification,
scientific validation, UQ, physical correctness, or release readiness.
"""

from __future__ import annotations

import pytest

import ksdft2effmass.harness.pi as api

pytestmark = pytest.mark.software_verification


def test_public_api__exports__match_exact_h1_surface() -> None:
    """Evidence ID
    SV-HARNESS-039
    Requirement
    The package exports every and only accepted H1 public name.
    Method
    Compare ``__all__`` and attribute availability with a literal transcription of
    the accepted surface.
    Oracle
    H1 contract-surface.md lists the exact records, results, support types, actions,
    and semantic primitives.
    Acceptance
    ``__all__`` equals the exact 41-name sequence and every listed attribute
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
    H1 requires eleven concrete actions with no roots, profiles, caches, clients, or
    mutable state.
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
        "ResolveResource",
        "ValidateResourceManifest",
        "ValidateOwnershipManifest",
        "ValidateCheckpointSet",
        "EvaluateChainState",
        "AuditEvidenceIdentifiers",
        "ValidateChecksumManifest",
        "ValidateSkillResources",
    )
    for name in names:
        instance = getattr(api, name)()
        assert not hasattr(instance, "__dict__")
        assert type(instance).__slots__ == ()
