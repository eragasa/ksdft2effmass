"""Nominal scientific base for hopping-coefficient locality."""

from __future__ import annotations

from abc import ABC


class HoppingLocality(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify locality diagnostics on an unchanged hopping representation.

    Concrete subclasses must declare their coefficient index space, support geometry,
    basis and gauge, normalization, and diagnostic range inventory. Membership never
    implies that coefficients were removed or that a finite-support operator was
    constructed. This base owns no lattice primitive, transform backend, tolerance,
    acceptance policy, or wire format.
    """

    __slots__ = ()


__all__ = ["HoppingLocality"]
