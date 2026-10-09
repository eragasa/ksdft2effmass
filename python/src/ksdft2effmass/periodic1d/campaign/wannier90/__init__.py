"""Canonical periodic-1D campaign integration for retained Wannier90 evidence.

The package owns exact encoded campaign documents, campaign-specific adaptation,
correlation, and bounded verification. Generic native artifact records, parsers, and
correlators remain owned by :mod:`ksdft2effmass.integration.wannier90`; this package
only composes them with the explicit retained campaign inventory. No object here
executes Wannier90, discovers files, or establishes scientific acceptance.
"""

from .correlation import (
    Periodic1DWannier90CampaignWorkflow,
    Periodic1DWannier90CampaignWorkflowRequest,
    Periodic1DWannier90CampaignWorkflowResult,
)
from .encoded_documents import Periodic1DWannier90EncodedDocuments
from .integration import Periodic1DWannier90Integration
from .integration_correlation import (
    Periodic1DWannier90IntegrationCorrelationRequest,
    Periodic1DWannier90IntegrationCorrelationResult,
    Periodic1DWannier90IntegrationCorrelator,
)
from .integration_verification import (
    Periodic1DWannier90IntegrationVerificationRequest,
    Periodic1DWannier90IntegrationVerificationResult,
    Periodic1DWannier90IntegrationVerifier,
)
from .native_artifacts import (
    Periodic1DWannier90NativeArtifactGroup,
    Periodic1DWannier90NativeArtifactGroupResult,
    Periodic1DWannier90NativeArtifactWorkflow,
    Periodic1DWannier90NativeArtifactWorkflowRequest,
    Periodic1DWannier90NativeArtifactWorkflowResult,
)
from .results import (
    Periodic1DWannier90CampaignResult,
    Periodic1DWannier90ResultJsonSerializer,
    Periodic1DWannier90WilsonGroupResult,
)
from .verification import (
    Periodic1DWannier90WilsonGroupVerificationResult,
    Periodic1DWannier90WilsonVerificationRequest,
    Periodic1DWannier90WilsonVerificationResult,
    Periodic1DWannier90WilsonVerifier,
)
from .verified_workflow import (
    Periodic1DWannier90VerifiedNativeWorkflow,
    Periodic1DWannier90VerifiedNativeWorkflowRequest,
    Periodic1DWannier90VerifiedNativeWorkflowResult,
)

__all__ = [
    "Periodic1DWannier90CampaignResult",
    "Periodic1DWannier90CampaignWorkflow",
    "Periodic1DWannier90CampaignWorkflowRequest",
    "Periodic1DWannier90CampaignWorkflowResult",
    "Periodic1DWannier90EncodedDocuments",
    "Periodic1DWannier90Integration",
    "Periodic1DWannier90IntegrationCorrelationRequest",
    "Periodic1DWannier90IntegrationCorrelationResult",
    "Periodic1DWannier90IntegrationCorrelator",
    "Periodic1DWannier90IntegrationVerificationRequest",
    "Periodic1DWannier90IntegrationVerificationResult",
    "Periodic1DWannier90IntegrationVerifier",
    "Periodic1DWannier90NativeArtifactGroup",
    "Periodic1DWannier90NativeArtifactGroupResult",
    "Periodic1DWannier90NativeArtifactWorkflow",
    "Periodic1DWannier90NativeArtifactWorkflowRequest",
    "Periodic1DWannier90NativeArtifactWorkflowResult",
    "Periodic1DWannier90ResultJsonSerializer",
    "Periodic1DWannier90VerifiedNativeWorkflow",
    "Periodic1DWannier90VerifiedNativeWorkflowRequest",
    "Periodic1DWannier90VerifiedNativeWorkflowResult",
    "Periodic1DWannier90WilsonGroupResult",
    "Periodic1DWannier90WilsonGroupVerificationResult",
    "Periodic1DWannier90WilsonVerificationRequest",
    "Periodic1DWannier90WilsonVerificationResult",
    "Periodic1DWannier90WilsonVerifier",
]
