r"""Software verification of public api.

Facet and represented meaning

-----------------------------
This artifact-owned software verification covers the exact Python package import
surface, its accepted export inventory, and the defining-module ownership of every
exported object.

Intrinsic and cross-object scope

--------------------------------
The ``ksdft2effmass.provenance`` package import surface is the owned artifact.
``provenance.__all__`` and the accepted P2 export inventory define the public
boundary, and exact defining-module ownership is part of that artifact. Individual
class and enum behavior remains owned by dedicated class modules. Dependency
direction is owned separately by ``test__import_dependency_direction.py``.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the declared Python package surface. It does not establish
individual object behavior, dependency direction, numerical verification,
scientific validation, uncertainty quantification, provenance truth, external-tool
correctness, cross-language conformance, or release readiness.
"""

import pytest

import ksdft2effmass.provenance as provenance
import ksdft2effmass.provenance.actions as provenance_actions
import ksdft2effmass.provenance.external_execution as provenance_external_execution
import ksdft2effmass.provenance.external_tools as provenance_external_tools
import ksdft2effmass.provenance.records as provenance_records
import ksdft2effmass.provenance.tool_observations as provenance_tool_observations

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

EXPECTED_MODULE_ORIGINS = {
    "ArtifactIdentity": "ksdft2effmass.provenance.records",
    "ArtifactIdentityVerificationResult": "ksdft2effmass.provenance.actions",
    "ArtifactIdentityVerificationStatus": "ksdft2effmass.provenance.actions",
    "ArtifactIdentityVerifier": "ksdft2effmass.provenance.actions",
    "ArtifactLocation": "ksdft2effmass.provenance.records",
    "ArtifactLocationKind": "ksdft2effmass.provenance.records",
    "ArtifactReference": "ksdft2effmass.provenance.records",
    "ArtifactSpecification": "ksdft2effmass.provenance.records",
    "CapabilityKind": "ksdft2effmass.provenance.external_tools",
    "CorrelationIssue": "ksdft2effmass.provenance.actions",
    "CorrelationStatus": "ksdft2effmass.provenance.actions",
    "DeclaredCapability": "ksdft2effmass.provenance.external_tools",
    "ExecutionCorrelationResult": "ksdft2effmass.provenance.actions",
    "ExecutionOutcomeCorrelator": "ksdft2effmass.provenance.actions",
    "ExternalExecutionFailure": "ksdft2effmass.provenance.external_execution",
    "ExternalExecutionRequest": "ksdft2effmass.provenance.external_execution",
    "ExternalExecutionResult": "ksdft2effmass.provenance.external_execution",
    "ExternalExecutionStatus": "ksdft2effmass.provenance.external_execution",
    "ExternalFailureCode": "ksdft2effmass.provenance.external_execution",
    "ExternalFailureStage": "ksdft2effmass.provenance.external_execution",
    "ExternalToolIdentity": "ksdft2effmass.provenance.external_tools",
    "ExternalToolSpecification": "ksdft2effmass.provenance.external_tools",
    "InstallationObservation": "ksdft2effmass.provenance.tool_observations",
    "LineageKind": "ksdft2effmass.provenance.records",
    "LineageRelation": "ksdft2effmass.provenance.records",
    "ManifestState": "ksdft2effmass.provenance.records",
    "ProvenanceJsonError": "ksdft2effmass.provenance.serialization",
    "ProvenanceJsonSerializer": "ksdft2effmass.provenance.serialization",
    "ProvenanceRecord": "ksdft2effmass.provenance.records",
    "RunManifest": "ksdft2effmass.provenance.records",
    "VerificationObservation": "ksdft2effmass.provenance.tool_observations",
    "VerificationStatus": "ksdft2effmass.provenance.tool_observations",
}

EXPECTED_ENUM_EXPORTS = {
    "ArtifactIdentityVerificationStatus": (
        provenance_actions.ArtifactIdentityVerificationStatus
    ),
    "ArtifactLocationKind": provenance_records.ArtifactLocationKind,
    "CapabilityKind": provenance_external_tools.CapabilityKind,
    "CorrelationIssue": provenance_actions.CorrelationIssue,
    "CorrelationStatus": provenance_actions.CorrelationStatus,
    "ExternalExecutionStatus": provenance_external_execution.ExternalExecutionStatus,
    "ExternalFailureCode": provenance_external_execution.ExternalFailureCode,
    "ExternalFailureStage": provenance_external_execution.ExternalFailureStage,
    "LineageKind": provenance_records.LineageKind,
    "ManifestState": provenance_records.ManifestState,
    "VerificationStatus": provenance_tool_observations.VerificationStatus,
}


def test_public_api__export_inventory__matches_exact_accepted_surface() -> None:
    """Evidence ID: SV-PROV-062

    Requirement: The package exports exactly the accepted sorted, unique P2 public-name
    inventory.

    Method: Compare ``provenance.__all__`` with the fixed independent EXPECTED_EXPORTS
    tuple
    and check the fixed tuple's ordering and uniqueness.

    Oracle: The literal EXPECTED_EXPORTS tuple records the accepted P2 package boundary
    independently of package discovery or runtime derivation.

    Acceptance: ``provenance.__all__`` equals EXPECTED_EXPORTS exactly, and
    EXPECTED_EXPORTS
    equals its sorted unique form.

    Interpretation: Failure identifies a missing, extra, renamed, duplicated, or
    reordered public
    export, or a defect in the maintained independent oracle.

    Limitations: Export inventory does not establish defining-module ownership, object
    behavior,
    dependency direction, or another language's package surface.
    """
    assert provenance.__all__ == EXPECTED_EXPORTS
    assert EXPECTED_EXPORTS == tuple(sorted(set(EXPECTED_EXPORTS)))


def test_public_api__defining_modules__match_exact_ownership_map() -> None:
    """Evidence ID: SV-PROV-063

    Requirement: Every accepted package export originates from its exact defining
    provenance
    submodule rather than a legacy, compatibility, backend, or CPN module.

    Method: Build one complete name-to-``__module__`` observation for EXPECTED_EXPORTS
    and
    compare it with the fixed literal EXPECTED_MODULE_ORIGINS mapping.

    Oracle: EXPECTED_MODULE_ORIGINS independently assigns every accepted export to one
    exact
    defining module; no prefix matching or production-derived expectation is used.

    Acceptance: The complete observed mapping equals EXPECTED_MODULE_ORIGINS exactly.

    Interpretation: Failure identifies export resolution drift, wrong submodule
    ownership, legacy or
    compatibility routing, backend/CPN leakage, or a stale maintained oracle.

    Limitations: Exact defining modules do not establish transitive dependency direction
    or
    individual exported-object behavior.
    """
    observed = {name: getattr(provenance, name).__module__ for name in EXPECTED_EXPORTS}
    assert observed == EXPECTED_MODULE_ORIGINS


def test_public_api__enum_exports__are_exact_defining_class_objects() -> None:
    """Evidence ID: SV-PROV-076

    Requirement: The package re-exports exactly the intended public enum classes as the
    identical
    class objects supplied by their defining modules.

    Method: Resolve the fixed EXPECTED_ENUM_EXPORTS names from the package and compare
    one
    exact observed name-to-class dictionary with the defining-class dictionary.

    Oracle: The literal enum-name inventory and explicit defining-module class
    references
    specify the accepted package re-export identities independently of ``__all__``.

    Acceptance: The observed enum dictionary equals EXPECTED_ENUM_EXPORTS with object
    identity
    semantics for each class value.

    Interpretation: Failure identifies a missing, replaced, aliased, or wrongly defined
    enum re-export,
    or a defect in the maintained enum inventory.

    Limitations: This package-surface evidence does not retest enum members, wire
    values,
    ``StrEnum`` behavior, or any other class-owned enum semantics.
    """
    observed = {name: getattr(provenance, name) for name in EXPECTED_ENUM_EXPORTS}
    assert observed == EXPECTED_ENUM_EXPORTS
