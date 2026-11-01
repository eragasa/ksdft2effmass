"""Periodic one-dimensional specialization of gauge alignment."""

from __future__ import annotations

from ksdft2effmass.gauge_alignment import GaugeAlignment


class Periodic1DGaugeAlignment(GaugeAlignment):  # noqa: B024 - nominal marker
    """Identify a periodic-1D retained-space gauge-alignment capability.

    Concrete subclasses must declare the retained rank, gauge group, right- or
    left-action convention, reciprocal-coordinate domain, and applicability. The
    specialization owns no mesh, transport route, alignment algorithm, threshold,
    locality policy, or serialization format.
    """

    __slots__ = ()


__all__ = ["Periodic1DGaugeAlignment"]
