"""Nominal scientific base for numerical-consistency assessments."""

from __future__ import annotations

from abc import ABC


class NumericalConsistency(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify one assessment of a declared finite numerical route.

    Concrete subclasses must retain the numerical source being varied or compared, such
    as a mesh, interpolation, Fourier reconstruction, or independent route. Numerical
    consistency is not parent-model adequacy, model-reduction error, or scientific
    validation. This base owns no universal tolerance or combined diagnostic score.
    """

    __slots__ = ()


__all__ = ["NumericalConsistency"]
