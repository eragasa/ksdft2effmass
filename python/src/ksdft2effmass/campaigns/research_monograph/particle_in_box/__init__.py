"""Deprecated compatibility façade for the PIAB1D campaigns."""

import warnings

from ...piab1d import (
    JsonValue,
    ParticleInBoxCampaignResultDecoder,
    ParticleInBoxConvergenceVerifier,
    ParticleInBoxConvergenceWorkflow,
    ParticleInBoxEigenpairSweepVerifier,
    ParticleInBoxEigenpairSweepWorkflow,
    ParticleInBoxIdentifiabilityVerifier,
    ParticleInBoxIdentifiabilityWorkflow,
    ParticleInBoxNormSweepVerifier,
    ParticleInBoxNormSweepWorkflow,
    ParticleInBoxResidualStudyEvaluator,
    ParticleInBoxResidualStudyResult,
    ParticleInBoxResultVerifier,
    ParticleInBoxStudyDefinition,
    ParticleInBoxStudyInputDeserializer,
    ParticleInBoxStudyResultSerializer,
    RetainedModelClassFitResult,
    RetainedModelClassFitter,
)

warnings.warn(
    "ksdft2effmass.campaigns.research_monograph.particle_in_box is deprecated; "
    "use ksdft2effmass.campaigns.piab1d",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "JsonValue",
    "ParticleInBoxCampaignResultDecoder",
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
    "ParticleInBoxResidualStudyResult",
    "ParticleInBoxStudyDefinition",
    "ParticleInBoxStudyInputDeserializer",
    "ParticleInBoxStudyResultSerializer",
    "RetainedModelClassFitResult",
    "RetainedModelClassFitter",
]
