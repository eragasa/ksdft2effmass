"""Scientific gauge-alignment identities for periodic-3D rank-N studies."""

from ksdft2effmass.serialization import StrWireEnum


class Periodic3DRankNGaugeAlignment(StrWireEnum):
    """Identify one prescribed periodic-3D retained-space gauge alignment."""

    IDENTITY = "identity"
    GLOBAL_UNITARY = "global-unitary"
    POINTWISE_UNITARY = "pointwise-unitary"
    KNOWN_INVERSE_ORACLE = "known-inverse-oracle"


__all__ = ["Periodic3DRankNGaugeAlignment"]
