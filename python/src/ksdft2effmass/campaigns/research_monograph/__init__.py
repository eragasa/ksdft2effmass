"""Bounded root exports required by retained research-monograph adapters.

New code imports canonical capability packages directly. This root preserves only the
symbols consumed by repository-retained calculation adapters; it does not aggregate the
full campaign library or define a namespace pattern for new campaigns.
"""

from ..periodic_1d import (
    Periodic1DCompositeCampaign,
    Periodic1DCompositeCampaignModel,
    Periodic1DIsolatedBandCampaign,
    Periodic1DIsolatedBandCampaignModel,
    Periodic1DStressCampaign,
    Periodic1DStressCampaignModel,
)
from ..piab1d import (
    ParticleInBoxConvergenceVerifier,
    ParticleInBoxConvergenceWorkflow,
    ParticleInBoxEigenpairSweepVerifier,
    ParticleInBoxEigenpairSweepWorkflow,
    ParticleInBoxIdentifiabilityVerifier,
    ParticleInBoxIdentifiabilityWorkflow,
    ParticleInBoxNormSweepVerifier,
    ParticleInBoxNormSweepWorkflow,
    ParticleInBoxResidualStudyEvaluator,
    ParticleInBoxResultVerifier,
    ParticleInBoxStudyInputDeserializer,
    ParticleInBoxStudyResultSerializer,
)
from ..qho1d import (
    HarmonicOscillatorResultVerifier,
    HarmonicOscillatorStudyEvaluator,
    HarmonicOscillatorStudyInputDeserializer,
    HarmonicOscillatorStudyResultSerializer,
)
from .impurity_defect_2d import StageCParentSvgPlotter

__all__ = [
    "HarmonicOscillatorResultVerifier",
    "HarmonicOscillatorStudyEvaluator",
    "HarmonicOscillatorStudyInputDeserializer",
    "HarmonicOscillatorStudyResultSerializer",
    "ParticleInBoxConvergenceVerifier",
    "ParticleInBoxConvergenceWorkflow",
    "ParticleInBoxEigenpairSweepVerifier",
    "ParticleInBoxEigenpairSweepWorkflow",
    "ParticleInBoxIdentifiabilityVerifier",
    "ParticleInBoxIdentifiabilityWorkflow",
    "ParticleInBoxNormSweepVerifier",
    "ParticleInBoxNormSweepWorkflow",
    "ParticleInBoxResidualStudyEvaluator",
    "ParticleInBoxResultVerifier",
    "ParticleInBoxStudyInputDeserializer",
    "ParticleInBoxStudyResultSerializer",
    "Periodic1DCompositeCampaign",
    "Periodic1DCompositeCampaignModel",
    "Periodic1DIsolatedBandCampaign",
    "Periodic1DIsolatedBandCampaignModel",
    "Periodic1DStressCampaign",
    "Periodic1DStressCampaignModel",
    "StageCParentSvgPlotter",
]
