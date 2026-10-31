"""Nominal scientific base for real-space support truncation."""

from __future__ import annotations

from abc import ABC


class RealSpaceSupportTruncation(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify one irreversible truncation of represented real-space support.

    Concrete subclasses must declare the support geometry and conjugate-closure rule.
    Operator and band errors retained by subclasses are consequences of spatial support
    removal; they are not spectral-subspace truncation errors. This base owns no lattice
    primitive, Fourier backend, threshold policy, or serialization format.
    """

    __slots__ = ()


__all__ = ["RealSpaceSupportTruncation"]
