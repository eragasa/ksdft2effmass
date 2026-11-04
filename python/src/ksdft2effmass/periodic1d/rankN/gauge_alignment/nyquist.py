"""Nyquist-mode disposition and its stable string mapping."""

from ksdft2effmass.serialization import StrWireEnum


class NyquistModeDispositionEnum(StrWireEnum):
    """State the mathematical disposition of a self-inverse Nyquist mode."""

    ABSENT_ON_ODD_MESH = "absent-on-odd-mesh"


__all__ = ["NyquistModeDispositionEnum"]
