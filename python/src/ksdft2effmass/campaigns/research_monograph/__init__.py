"""Public compositions for reproducible research-monograph calculations.

This package binds exact monograph study definitions, retained wire formats, and
provenance conventions to reusable analysis contracts. It does not own the underlying
scientific algorithms, grant execution authority, or establish scientific acceptance.
"""

from .harmonic_oscillator import (
    HarmonicOscillatorResultVerifier,
    HarmonicOscillatorStudyDefinition,
    HarmonicOscillatorStudyEvaluator,
    HarmonicOscillatorStudyInputDeserializer,
    HarmonicOscillatorStudyResult,
    HarmonicOscillatorStudyResultSerializer,
)
from .particle_in_box import (
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

__all__ = [
    "HarmonicOscillatorResultVerifier",
    "HarmonicOscillatorStudyDefinition",
    "HarmonicOscillatorStudyEvaluator",
    "HarmonicOscillatorStudyInputDeserializer",
    "HarmonicOscillatorStudyResult",
    "HarmonicOscillatorStudyResultSerializer",
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
    "ParticleInBoxResidualStudyResult",
    "ParticleInBoxResultVerifier",
    "ParticleInBoxStudyDefinition",
    "ParticleInBoxStudyInputDeserializer",
    "ParticleInBoxStudyResultSerializer",
    "RetainedModelClassFitResult",
    "RetainedModelClassFitter",
]
