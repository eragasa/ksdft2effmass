"""Scientific gauge-alignment identities and stable string mappings."""

from ksdft2effmass.serialization import StringWireEnum


class Periodic1DRankNGaugeAlignment(StringWireEnum):
    """Identify one prescribed retained-space gauge alignment."""

    IDENTITY = "identity"
    GLOBAL_UNITARY = "global-unitary"
    POINTWISE_UNITARY = "pointwise-unitary"
    KNOWN_INVERSE_ORACLE = "known-inverse-oracle"


__all__ = ["Periodic1DRankNGaugeAlignment"]
