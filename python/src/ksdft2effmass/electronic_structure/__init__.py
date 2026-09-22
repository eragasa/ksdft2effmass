"""Calculator-independent electronic-structure representation contracts.

The initial public surface owns reciprocal-space k-point sampling independently of
physical crystal-structure records.
"""

from .sampling import KPointSampling, KPointWeightNormalization

__all__ = ["KPointSampling", "KPointWeightNormalization"]
