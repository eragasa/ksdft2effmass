"""Scientific gauge-alignment identities for periodic-2D rank-N studies."""

from ksdft2effmass.serialization import StringWireEnum


class Periodic2DRankNGaugeAlignment(StringWireEnum):
    """Identify one prescribed periodic-2D retained-space gauge alignment."""

    IDENTITY = "identity"
    GLOBAL_UNITARY = "global-unitary"
    POINTWISE_UNITARY = "pointwise-unitary"
    KNOWN_INVERSE_ORACLE = "known-inverse-oracle"


__all__ = ["Periodic2DRankNGaugeAlignment"]
