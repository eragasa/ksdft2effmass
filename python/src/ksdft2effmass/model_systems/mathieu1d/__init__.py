"""Mathieu1d controlled model-system studies.

``Mathieu1d`` is dimension-specific. The current supported study evaluates a scalar
periodic cosine parent and a finite single-band Fourier/hopping reduction. Its sampled
finite diagnostics do not establish continuum isolation or material validation.
"""

from .study import (
    Mathieu1dFiniteDifferenceRefinementObservation,
    Mathieu1dPlaneWaveRefinementObservation,
    Mathieu1dStudyDefinition,
    Mathieu1dStudyEvaluator,
    Mathieu1dStudyInputDeserializer,
    Mathieu1dStudyInputSerializer,
    Mathieu1dStudyResult,
    Mathieu1dStudyResultSerializer,
    Mathieu1dStudyVerificationResult,
    Mathieu1dStudyVerificationSerializer,
    Mathieu1dStudyVerifier,
)

__all__ = [
    "Mathieu1dFiniteDifferenceRefinementObservation",
    "Mathieu1dPlaneWaveRefinementObservation",
    "Mathieu1dStudyDefinition",
    "Mathieu1dStudyEvaluator",
    "Mathieu1dStudyInputDeserializer",
    "Mathieu1dStudyInputSerializer",
    "Mathieu1dStudyResult",
    "Mathieu1dStudyResultSerializer",
    "Mathieu1dStudyVerificationResult",
    "Mathieu1dStudyVerificationSerializer",
    "Mathieu1dStudyVerifier",
]
