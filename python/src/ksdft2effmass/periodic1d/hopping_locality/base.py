"""Periodic one-dimensional specialization of hopping locality."""

from __future__ import annotations

from ksdft2effmass.hopping_locality import HoppingLocality


class Periodic1DHoppingLocality(HoppingLocality):  # noqa: B024 - intentionally nominal marker
    """Identify unchanged hopping coefficients indexed by 1D translations.

    Concrete subclasses must state the integer-translation inventory, range convention,
    conjugate relation, basis and gauge, and normalization. The specialization does not
    imply support removal and owns no Fourier algorithm, tolerance, or wire format.
    """

    __slots__ = ()


__all__ = ["Periodic1DHoppingLocality"]
