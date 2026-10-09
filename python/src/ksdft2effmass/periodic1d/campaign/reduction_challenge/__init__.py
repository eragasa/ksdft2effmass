"""Canonical periodic-1D reduction-challenge campaign family.

The facade exposes exact wires, typed campaign controls and outcomes, read-only
correlation, independent numerical verification, and composed workflows. Historical
``stress`` filenames, JSON keys, evidence-status text, and result-kind identity remain
wire concerns and are not exported as canonical software names.
"""

from .campaign import Periodic1DReductionChallengeCampaign
from .correlation import (
    Periodic1DReductionChallengeCampaignCorrelationRequest,
    Periodic1DReductionChallengeCampaignCorrelationResult,
    Periodic1DReductionChallengeCampaignCorrelator,
)
from .correlation_workflow import (
    Periodic1DReductionChallengeCampaignWorkflow,
    Periodic1DReductionChallengeCampaignWorkflowRequest,
    Periodic1DReductionChallengeCampaignWorkflowResult,
)
from .definition import (
    Periodic1DReductionChallengeCampaignDefinition,
    Periodic1DReductionChallengeCampaignJsonSerializer,
    Periodic1DReductionChallengePotentialShape,
)
from .encoded_documents import Periodic1DReductionChallengeEncodedDocuments
from .numerical_verification import (
    Periodic1DReductionChallengeResultVerifier,
    Periodic1DReductionChallengeVerificationRequest,
    Periodic1DReductionChallengeVerificationResult,
)
from .results import (
    Periodic1DReductionChallengeCampaignResult,
    Periodic1DReductionChallengeDiscretizationObservation,
    Periodic1DReductionChallengeGaugeCovarianceResult,
    Periodic1DReductionChallengeMeshBandIsolationResult,
    Periodic1DReductionChallengePotentialAmplitudeResult,
    Periodic1DReductionChallengePotentialShapeCase,
    Periodic1DReductionChallengePotentialShapeResult,
    Periodic1DReductionChallengeResultJsonSerializer,
    Periodic1DReductionChallengeRouteAssumptionResult,
)
from .verification import (
    Periodic1DReductionChallengeCampaignVerificationRequest,
    Periodic1DReductionChallengeCampaignVerificationResult,
    Periodic1DReductionChallengeCampaignVerifier,
)
from .verified_workflow import (
    Periodic1DReductionChallengeVerifiedWorkflow,
    Periodic1DReductionChallengeVerifiedWorkflowRequest,
    Periodic1DReductionChallengeVerifiedWorkflowResult,
)

__all__ = [
    "Periodic1DReductionChallengeCampaign",
    "Periodic1DReductionChallengeCampaignCorrelationRequest",
    "Periodic1DReductionChallengeCampaignCorrelationResult",
    "Periodic1DReductionChallengeCampaignCorrelator",
    "Periodic1DReductionChallengeCampaignDefinition",
    "Periodic1DReductionChallengeCampaignJsonSerializer",
    "Periodic1DReductionChallengeCampaignResult",
    "Periodic1DReductionChallengeCampaignVerificationRequest",
    "Periodic1DReductionChallengeCampaignVerificationResult",
    "Periodic1DReductionChallengeCampaignVerifier",
    "Periodic1DReductionChallengeCampaignWorkflow",
    "Periodic1DReductionChallengeCampaignWorkflowRequest",
    "Periodic1DReductionChallengeCampaignWorkflowResult",
    "Periodic1DReductionChallengeDiscretizationObservation",
    "Periodic1DReductionChallengeEncodedDocuments",
    "Periodic1DReductionChallengeGaugeCovarianceResult",
    "Periodic1DReductionChallengeMeshBandIsolationResult",
    "Periodic1DReductionChallengePotentialAmplitudeResult",
    "Periodic1DReductionChallengePotentialShape",
    "Periodic1DReductionChallengePotentialShapeCase",
    "Periodic1DReductionChallengePotentialShapeResult",
    "Periodic1DReductionChallengeResultJsonSerializer",
    "Periodic1DReductionChallengeResultVerifier",
    "Periodic1DReductionChallengeRouteAssumptionResult",
    "Periodic1DReductionChallengeVerificationRequest",
    "Periodic1DReductionChallengeVerificationResult",
    "Periodic1DReductionChallengeVerifiedWorkflow",
    "Periodic1DReductionChallengeVerifiedWorkflowRequest",
    "Periodic1DReductionChallengeVerifiedWorkflowResult",
]
