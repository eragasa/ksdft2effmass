"""Evidence class and represented meaning
Software verification of the provenance Python public import artifact.
Owned contract, oracle, and scope
The package import surface is the artifact owner; the accepted P2 export inventory is
the exact oracle.
VVUQ and scientific exclusions
Pass/fail concerns imports only; numerical verification, scientific validation, UQ,
execution, and cross-language conformance are excluded.
"""

from enum import StrEnum

import pytest

import ksdft2effmass.provenance as provenance

pytestmark = pytest.mark.software_verification

EXPECTED_EXPORTS = (
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


def test_public_api__export_inventory__matches_accepted_sorted_surface() -> None:
    """Evidence ID
    SV-PROV-062
    Requirement
    The provenance package exposes exactly the accepted sorted, unique P2 public names.
    Method
    Compare public __all__ with a fixed independent inventory and resolve each
    attribute.
    Oracle
    The human-approved P2 public classes and enums fix EXPECTED_EXPORTS independently of
    runtime discovery.
    Acceptance
    __all__ equals the fixed tuple, is sorted/unique, and every attribute resolves with
    matching __name__.
    Interpretation
    Failure indicates missing, extra, renamed, duplicate, or unresolved public API
    state.
    Limitations
    Import success does not validate object behavior, scientific meaning, or another
    language.
    """
    assert provenance.__all__ == EXPECTED_EXPORTS
    assert provenance.__all__ == tuple(sorted(set(provenance.__all__)))
    for name in EXPECTED_EXPORTS:
        assert getattr(provenance, name).__name__ == name


def test_public_api__module_origins__resolve_from_provenance_package() -> None:
    """Evidence ID
    SV-PROV-063
    Requirement
    Public P2 objects resolve from the provenance implementation modules rather than CPN
    or backend packages.
    Method
    Inspect __module__ for every exported class and enum.
    Oracle
    The accepted package boundary requires the ksdft2effmass.provenance module prefix.
    Acceptance
    Every export module begins exactly with the provenance package prefix.
    Interpretation
    Failure indicates an import alias or architecture leakage.
    Limitations
    Transitive dependency isolation is owned by separate static evidence.
    """
    for name in EXPECTED_EXPORTS:
        assert getattr(provenance, name).__module__.startswith(
            "ksdft2effmass.provenance"
        )


def test_public_api__string_enums__have_exact_strenum_semantics() -> None:
    """Evidence ID
    SV-PROV-076
    Requirement
    Every public string-valued provenance enum is a StrEnum whose members behave as
    their exact wire strings.
    Method
    Inspect the fixed public enum inventory, its base class, and every member's
    string/equality behavior.
    Oracle
    Python StrEnum semantics and each independently asserted class-owned value
    vocabulary define expected behavior.
    Acceptance
    Every type subclasses StrEnum; each member is str, equals its value, and str(member)
    equals value.
    Interpretation
    Failure indicates enum-policy or runtime/wire string-semantics drift.
    Limitations
    Cross-language enum implementations are excluded.
    """
    enum_names = (
        "ArtifactIdentityVerificationStatus",
        "ArtifactLocationKind",
        "CapabilityKind",
        "CorrelationIssue",
        "CorrelationStatus",
        "ExternalExecutionStatus",
        "ExternalFailureCode",
        "ExternalFailureStage",
        "LineageKind",
        "ManifestState",
        "VerificationStatus",
    )
    for name in enum_names:
        enum_type = getattr(provenance, name)
        assert issubclass(enum_type, StrEnum)
        for member in enum_type:
            value = member.value
            assert isinstance(member, str)
            assert member == value
            assert str(member) == value
