r"""Software verification of ksdft2effmass.harness public API.

Evidence profile: routine

Bounded artifact scope: the ``ksdft2effmass.harness`` public import inventory.

Facet and represented meaning

The artifact verifies exact package-level availability of the accepted public Harness
contracts, including the compiler aliases.

Intrinsic and cross-object scope

This is an artifact-owned import-surface check. Runtime loading and compilation are
owned by their respective ActionObjects.

VVUQ and scientific exclusions

This is software verification only. It establishes no authority, scientific validity,
protected execution, persistence, projection, or human acceptance.
"""

import pytest

import ksdft2effmass.harness as api

pytestmark = pytest.mark.software_verification


class TestHarnessCompilerPublicApi:
    """Own the exact package-level Harness public export inventory."""

    @staticmethod
    def test_artifact__public_api__exports_exact_harness_surface() -> None:
        """Evidence ID: software-verification.harness-configuration.phase1.public-api

        Requirement: The v2 harness package exports exactly the approved configuration,
        identity, Task, selection, prerequisite, decision, authority, and compiler
        public surface.

        Acceptance: ``__all__`` equals the literal approved inventory and every name is
        importable.
        """
        expected = (
            "ContentIdentity",
            "SnapshotIdentity",
            "HumanReviewConfiguration",
            "HarnessPersistenceConfiguration",
            "PythonConformanceConfiguration",
            "HarnessResourceConfiguration",
            "HarnessCatalogConfiguration",
            "HarnessConfigurationSource",
            "HarnessConfiguration",
            "HarnessConfigurationSourceBinding",
            "HarnessConfigurationResolutionFinding",
            "HarnessConfigurationResolutionResult",
            "HarnessConfigurationSourceJsonSerializer",
            "HarnessConfigurationSourceJsonDeserializer",
            "HarnessConfigurationResolver",
            "HarnessConfigurationValidator",
            "HarnessConfigurationJsonSerializer",
            "HarnessConfigurationJsonDeserializer",
            "ArchivedTaskSource",
            "HarnessTask",
            "HarnessTaskSerializer",
            "HarnessTaskDeserializer",
            "HarnessTaskRegistry",
            "DevelopmentTaskSelection",
            "DevelopmentTaskSelectionSerializer",
            "DevelopmentTaskSelectionDeserializer",
            "DevelopmentPrerequisiteKind",
            "DevelopmentPrerequisiteLineage",
            "DevelopmentPrerequisiteLineagePolicy",
            "DevelopmentPrerequisiteObservationStatus",
            "DevelopmentPrerequisiteOutcome",
            "DevelopmentPrerequisiteAggregateStatus",
            "DevelopmentPrerequisiteRequirement",
            "DevelopmentPrerequisiteContract",
            "RetainedPrerequisiteResultReference",
            "RetainedPrerequisiteObservation",
            "DevelopmentPrerequisiteEdgeResult",
            "DevelopmentPrerequisiteResolutionResult",
            "DevelopmentPrerequisiteResolver",
            "DevelopmentDecision",
            "DevelopmentDecisionOption",
            "DevelopmentDecisionSerializer",
            "DevelopmentDecisionSourceProvenance",
            "DevelopmentAuthorityContext",
            "DevelopmentAuthorityContextResolutionResult",
            "DevelopmentAuthorityContextResolver",
            "DevelopmentAuthorityDiagnostic",
            "DevelopmentAuthorityLedgerSnapshot",
            "DevelopmentAuthorityPolicy",
            "DevelopmentAuthorityReconstructionReceipt",
            "DevelopmentAuthorityResolutionSerializer",
            "DevelopmentAuthoritySnapshotSource",
            "DevelopmentAuthorizationRevocation",
            "DevelopmentAuthorizationUse",
            "DevelopmentEligibilityReference",
            "DevelopmentIssuerAnchorBinding",
            "DevelopmentOperationAuthorizationInput",
            "DevelopmentOperationAuthorizationResult",
            "DevelopmentOperationAuthorizationSerializer",
            "DevelopmentOperationAuthorizer",
            "DevelopmentPromotionAuthorization",
            "DevelopmentPromotionOperationBinding",
            "DevelopmentReviewAuthorization",
            "DevelopmentReviewOperationBinding",
            "DevelopmentSignatureEntry",
            "DevelopmentSignedAuthoritySnapshot",
            "DevelopmentSignedAuthoritySnapshotSerializer",
            "DevelopmentTaskAuthorization",
            "DevelopmentTaskOperationBinding",
            "DevelopmentTaskSignatureConfiguration",
            "DevelopmentTaskSignatureConfigurationSerializer",
            "DevelopmentTaskSignatureRequirementResolver",
            "DevelopmentTaskSignatureRequirementResult",
            "DevelopmentTrustAnchor",
            "DevelopmentTrustConfiguration",
            "DevelopmentTrustConfigurationPin",
            "DevelopmentTrustConfigurationSerializer",
            "HarnessSourceFamily",
            "HarnessSourceFamilyContract",
            "HarnessLegacyDecisionBinding",
            "HarnessSourceContract",
            "HarnessSourceIdentity",
            "HarnessParsedValue",
            "HarnessSourceProvenance",
            "HarnessSourceRecord",
            "HarnessSourceSnapshot",
            "HarnessSourceLoadStatus",
            "HarnessSourceLoadSucceeded",
            "HarnessSourceLoadFailed",
            "HarnessSourceLoadResult",
            "HarnessCapabilityCatalog",
            "HarnessResourceCatalog",
            "HarnessEvidenceCatalog",
            "HarnessStateIdentity",
            "HarnessState",
            "HarnessCompilerPhase",
            "HarnessDiagnosticSeverity",
            "HarnessCompilerFailureCode",
            "HarnessCompilerDiagnostic",
            "HarnessCompilationStatus",
            "HarnessCompilationSucceeded",
            "HarnessCompilationFailed",
            "HarnessCompilationResult",
            "HarnessRepositoryLoader",
            "HarnessCompiler",
        )
        assert api.__all__ == expected
        assert all(hasattr(api, name) for name in expected)
