"""Nominal scientific base for real-space support truncation."""

from __future__ import annotations

from ksdft2effmass.support_truncation import SupportTruncation


class RealSpaceSupportTruncation(SupportTruncation):  # noqa: B024 - intentionally nominal marker
    """Identify one irreversible truncation of represented real-space support.

    This specialization fixes the generic support domain to represented real space.
    Concrete subclasses must declare the support geometry and conjugate-closure rule.
    Operator and band errors retained by subclasses are consequences of spatial support
    removal; they are not spectral-subspace truncation errors. This base owns no lattice
    primitive, Fourier backend, threshold policy, or serialization format.
    """

    __slots__ = ()


__all__ = ["RealSpaceSupportTruncation"]
