"""Canonical periodic-1D composite-band campaign family.

The facade exposes campaign records and operations while keeping the untruncated
physical parent, finite parent representation, retained spaces and operators,
gauge-qualified represented forms, approximation studies, and verification evidence
as distinct objects.
"""

from .adoption import (
    Periodic1DCompositeOperatorGroupAdoption,
    Periodic1DCompositeScientificAdoption,
    Periodic1DCompositeScientificAdoptionRequest,
    Periodic1DCompositeScientificAdoptionResult,
)
from .campaign import Periodic1DCompositeCampaign
from .correlation import (
    Periodic1DCompositeCampaignCorrelationRequest,
    Periodic1DCompositeCampaignCorrelationResult,
    Periodic1DCompositeCampaignCorrelator,
)
from .correlation_workflow import (
    Periodic1DCompositeCampaignWorkflow,
    Periodic1DCompositeCampaignWorkflowRequest,
    Periodic1DCompositeCampaignWorkflowResult,
)
from .definition import (
    Periodic1DCompositeCampaignDefinition,
    Periodic1DCompositeCampaignJsonSerializer,
)
from .encoded_documents import Periodic1DCompositeEncodedDocuments
from .numerical_verification import (
    Periodic1DCompositeGroupVerificationResult,
    Periodic1DCompositeResultVerifier,
    Periodic1DCompositeUnavailableVerificationChannel,
    Periodic1DCompositeVerificationRequest,
    Periodic1DCompositeVerificationResult,
)
from .results import (
    Periodic1DCompositeArtifactIdentities,
    Periodic1DCompositeBandGroupResult,
    Periodic1DCompositeBandIsolationResult,
    Periodic1DCompositeCampaignResult,
    Periodic1DCompositeDirectRouteComparisonResult,
    Periodic1DCompositeExternalIsolationStatus,
    Periodic1DCompositeGaugeComparisonResult,
    Periodic1DCompositeHoppingRangeResult,
    Periodic1DCompositeHoppingRepresentationResult,
    Periodic1DCompositeResultJsonSerializer,
    Periodic1DCompositeWilsonGroupResult,
)
from .verification import (
    Periodic1DCompositeCampaignVerificationRequest,
    Periodic1DCompositeCampaignVerificationResult,
    Periodic1DCompositeCampaignVerifier,
)
from .verified_workflow import (
    Periodic1DCompositeVerifiedWorkflow,
    Periodic1DCompositeVerifiedWorkflowRequest,
    Periodic1DCompositeVerifiedWorkflowResult,
)

__all__ = [
    "Periodic1DCompositeArtifactIdentities",
    "Periodic1DCompositeBandGroupResult",
    "Periodic1DCompositeBandIsolationResult",
    "Periodic1DCompositeCampaign",
    "Periodic1DCompositeCampaignCorrelationRequest",
    "Periodic1DCompositeCampaignCorrelationResult",
    "Periodic1DCompositeCampaignCorrelator",
    "Periodic1DCompositeCampaignDefinition",
    "Periodic1DCompositeCampaignJsonSerializer",
    "Periodic1DCompositeCampaignResult",
    "Periodic1DCompositeCampaignVerificationRequest",
    "Periodic1DCompositeCampaignVerificationResult",
    "Periodic1DCompositeCampaignVerifier",
    "Periodic1DCompositeCampaignWorkflow",
    "Periodic1DCompositeCampaignWorkflowRequest",
    "Periodic1DCompositeCampaignWorkflowResult",
    "Periodic1DCompositeDirectRouteComparisonResult",
    "Periodic1DCompositeEncodedDocuments",
    "Periodic1DCompositeExternalIsolationStatus",
    "Periodic1DCompositeGaugeComparisonResult",
    "Periodic1DCompositeGroupVerificationResult",
    "Periodic1DCompositeHoppingRangeResult",
    "Periodic1DCompositeHoppingRepresentationResult",
    "Periodic1DCompositeOperatorGroupAdoption",
    "Periodic1DCompositeResultJsonSerializer",
    "Periodic1DCompositeResultVerifier",
    "Periodic1DCompositeScientificAdoption",
    "Periodic1DCompositeScientificAdoptionRequest",
    "Periodic1DCompositeScientificAdoptionResult",
    "Periodic1DCompositeUnavailableVerificationChannel",
    "Periodic1DCompositeVerificationRequest",
    "Periodic1DCompositeVerificationResult",
    "Periodic1DCompositeVerifiedWorkflow",
    "Periodic1DCompositeVerifiedWorkflowRequest",
    "Periodic1DCompositeVerifiedWorkflowResult",
    "Periodic1DCompositeWilsonGroupResult",
]
