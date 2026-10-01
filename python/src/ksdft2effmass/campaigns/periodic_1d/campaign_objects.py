"""Compatibility routes for periodic-1D campaign DataObjects.

New code should import defining modules below ``periodic_1d.model.retained`` and
``periodic_1d.run``. The names remain available here so the initial flat object-model
route continues to identify the same classes.
"""

from .model.retained import (
    Periodic1DCompositeCampaignModel,
    Periodic1DIsolatedBandCampaignModel,
    Periodic1DStressCampaignModel,
)
from .run.composite import (
    Periodic1DCompositeCampaign,
    Periodic1DCompositeCampaignCorrelationRequest,
    Periodic1DCompositeCampaignCorrelationResult,
    Periodic1DCompositeCampaignCorrelator,
    Periodic1DCompositeCampaignVerificationRequest,
    Periodic1DCompositeCampaignVerificationResult,
    Periodic1DCompositeCampaignVerifier,
)
from .run.isolated import (
    Periodic1DIsolatedBandCampaign,
    Periodic1DIsolatedBandCampaignCorrelationRequest,
    Periodic1DIsolatedBandCampaignCorrelationResult,
    Periodic1DIsolatedBandCampaignCorrelator,
    Periodic1DIsolatedBandCampaignVerificationRequest,
    Periodic1DIsolatedBandCampaignVerificationResult,
    Periodic1DIsolatedBandCampaignVerifier,
)
from .run.stress import (
    Periodic1DStressCampaign,
    Periodic1DStressCampaignCorrelationRequest,
    Periodic1DStressCampaignCorrelationResult,
    Periodic1DStressCampaignCorrelator,
    Periodic1DStressCampaignVerificationRequest,
    Periodic1DStressCampaignVerificationResult,
    Periodic1DStressCampaignVerifier,
)

__all__ = [
    "Periodic1DCompositeCampaign",
    "Periodic1DCompositeCampaignCorrelationRequest",
    "Periodic1DCompositeCampaignCorrelationResult",
    "Periodic1DCompositeCampaignCorrelator",
    "Periodic1DCompositeCampaignModel",
    "Periodic1DCompositeCampaignVerificationRequest",
    "Periodic1DCompositeCampaignVerificationResult",
    "Periodic1DCompositeCampaignVerifier",
    "Periodic1DIsolatedBandCampaign",
    "Periodic1DIsolatedBandCampaignCorrelationRequest",
    "Periodic1DIsolatedBandCampaignCorrelationResult",
    "Periodic1DIsolatedBandCampaignCorrelator",
    "Periodic1DIsolatedBandCampaignModel",
    "Periodic1DIsolatedBandCampaignVerificationRequest",
    "Periodic1DIsolatedBandCampaignVerificationResult",
    "Periodic1DIsolatedBandCampaignVerifier",
    "Periodic1DStressCampaign",
    "Periodic1DStressCampaignCorrelationRequest",
    "Periodic1DStressCampaignCorrelationResult",
    "Periodic1DStressCampaignCorrelator",
    "Periodic1DStressCampaignModel",
    "Periodic1DStressCampaignVerificationRequest",
    "Periodic1DStressCampaignVerificationResult",
    "Periodic1DStressCampaignVerifier",
]
