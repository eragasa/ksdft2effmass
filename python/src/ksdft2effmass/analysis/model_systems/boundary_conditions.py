"""Immutable boundary-condition contracts for model-system analyses."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.operators.quantities import ScalarQuantity


@dataclass(frozen=True, slots=True)
class DirichletBoundaryCondition:
    """Represent one constant value prescribed on every selected boundary point.

    Parameters
    ----------
    value
        Finite scalar boundary value with the field's explicit unit. A zero magnitude
        represents a homogeneous Dirichlet condition without discarding its unit.
    """

    value: ScalarQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.value, ScalarQuantity):
            raise TypeError("value must be ScalarQuantity")

    @property
    def condition_kind(self) -> str:
        """Return the exact boundary-condition kind identifier."""
        return "dirichlet"

    @property
    def is_homogeneous(self) -> bool:
        """Return whether the prescribed boundary value is exactly zero."""
        return self.value.magnitude == 0.0
