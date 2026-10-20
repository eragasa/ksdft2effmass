"""Bounded root exports required by retained research-monograph adapters.

New code imports canonical capability packages directly. This root preserves only the
symbols consumed by repository-retained calculation adapters; it does not aggregate the
full campaign library or define a namespace pattern for new campaigns.
"""

from ...model_systems.qho1d import (
    QHO1DResultVerifier as HarmonicOscillatorResultVerifier,
)
from ...model_systems.qho1d import (
    QHO1DStudyEvaluator as HarmonicOscillatorStudyEvaluator,
)
from ...model_systems.qho1d import (
    QHO1DStudyInputDeserializer as HarmonicOscillatorStudyInputDeserializer,
)
from ...model_systems.qho1d import (
    QHO1DStudyResultSerializer as HarmonicOscillatorStudyResultSerializer,
)
from ..periodic_1d import (
    Periodic1DCompositeCampaign,
    Periodic1DCompositeCampaignModel,
    Periodic1DIsolatedBandCampaign,
    Periodic1DIsolatedBandCampaignModel,
    Periodic1DStressCampaign,
    Periodic1DStressCampaignModel,
)
from .impurity_defect_2d import StageCParentSvgPlotter

__all__ = [
    "HarmonicOscillatorResultVerifier",
    "HarmonicOscillatorStudyEvaluator",
    "HarmonicOscillatorStudyInputDeserializer",
    "HarmonicOscillatorStudyResultSerializer",
    "Periodic1DCompositeCampaign",
    "Periodic1DCompositeCampaignModel",
    "Periodic1DIsolatedBandCampaign",
    "Periodic1DIsolatedBandCampaignModel",
    "Periodic1DStressCampaign",
    "Periodic1DStressCampaignModel",
    "StageCParentSvgPlotter",
]
