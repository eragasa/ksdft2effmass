"""Deprecated compatibility façade for the QHO1D campaign."""

import warnings

from ...qho1d import (
    HarmonicOscillatorResultVerifier,
    HarmonicOscillatorStudyDefinition,
    HarmonicOscillatorStudyEvaluator,
    HarmonicOscillatorStudyInputDeserializer,
    HarmonicOscillatorStudyResult,
    HarmonicOscillatorStudyResultSerializer,
)

warnings.warn(
    "ksdft2effmass.campaigns.research_monograph.harmonic_oscillator is deprecated; "
    "use ksdft2effmass.campaigns.qho1d",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "HarmonicOscillatorResultVerifier",
    "HarmonicOscillatorStudyDefinition",
    "HarmonicOscillatorStudyEvaluator",
    "HarmonicOscillatorStudyInputDeserializer",
    "HarmonicOscillatorStudyResult",
    "HarmonicOscillatorStudyResultSerializer",
]
