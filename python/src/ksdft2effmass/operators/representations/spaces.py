"""Explicit represented-space identities for operator representations.

This module composes the existing finite operator metadata owner. It does not
create alternative state-space, basis, geometry, or energy-reference classes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from ..records import Basis, EnergyReference, Geometry, StateSpace


def _require_nonempty_exact_string(value: str, name: str, /) -> str:
    """Validate one exact nonempty built-in string without normalization."""
    if type(value) is not str:
        raise TypeError(f"{name} must be an exact built-in string")
    if value == "":
        raise ValueError(f"{name} must not be empty")
    return value


@final
@dataclass(frozen=True, slots=True)
class RepresentationSpaceIdentity:
    """Bind the interpreting metadata for one represented finite space.

    The identity composes existing operator metadata and adds mathematical
    scalar-field and field-coordinate convention identities. The scalar-field
    identity is distinct from a NumPy storage dtype. The object validates only
    nominal state and the state-space/basis dimension relation. It does not infer basis
    orthonormality, completeness, units, or physical equivalence.
    """

    identifier: str
    state_space: StateSpace
    basis: Basis
    geometry: Geometry
    energy_reference: EnergyReference
    scalar_field_id: str
    coordinate_convention_id: str

    def __post_init__(self) -> None:
        """Validate exact metadata types and the represented dimension relation."""
        _require_nonempty_exact_string(self.identifier, "space identity")
        if type(self.state_space) is not StateSpace:
            raise TypeError("state_space must be an exact StateSpace")
        if type(self.basis) is not Basis:
            raise TypeError("basis must be an exact Basis")
        if type(self.geometry) is not Geometry:
            raise TypeError("geometry must be an exact Geometry")
        if type(self.energy_reference) is not EnergyReference:
            raise TypeError("energy_reference must be an exact EnergyReference")
        _require_nonempty_exact_string(self.scalar_field_id, "scalar field identity")
        _require_nonempty_exact_string(
            self.coordinate_convention_id,
            "coordinate convention identity",
        )
        if len(self.basis.ordering) != self.state_space.dimension:
            raise ValueError("basis ordering length must match state-space dimension")

    @property
    def dimension(self) -> int:
        """Return the finite represented dimension."""
        return self.state_space.dimension


__all__ = ["RepresentationSpaceIdentity"]
