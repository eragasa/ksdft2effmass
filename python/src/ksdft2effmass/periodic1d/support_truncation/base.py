"""Periodic one-dimensional specialization of real-space support truncation."""

from __future__ import annotations

from ksdft2effmass.real_space_support_truncation import RealSpaceSupportTruncation


class Periodic1DSupportTruncation(RealSpaceSupportTruncation):  # noqa: B024 - intentionally nominal marker
    """Identify irreversible removal of periodic 1D translation support.

    Concrete subclasses must state the integer-translation support, conjugate-closure
    rule, basis and gauge, and normalization used to assess removal consequences. The
    specialization owns no cutoff inventory, transform backend, tolerance, selection
    policy, or wire format.
    """

    __slots__ = ()


__all__ = ["Periodic1DSupportTruncation"]
