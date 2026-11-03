"""PhysKit block-hopping construction for the synthetic periodic-3D parent."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    DenseBlockHoppingModel,
    DenseBlockHoppingTerm,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBlockHoppingParentBuilder:
    """Construct the selected finite-range parent as a PhysKit hopping model.

    The parent has an ordered retained sector followed by an equally sized exterior
    sector. ``hopping_scale`` multiplies the first- and second-harmonic hopping
    blocks but does not alter the onsite block. Gauge attacks and retained-frame
    transformations are deliberately outside this construction.
    """

    MODEL_FAMILY_IDENTITY = "ksdft2effmass.periodic3d-rankN-block-hopping-parent.v1"
    ENERGY_REFERENCE = "dimensionless-zero-v1"

    retained_rank: int
    positive_bonds: tuple[tuple[int, int, int], ...]
    hopping_scale: float

    def __post_init__(self) -> None:
        """Validate the intrinsic block-hopping construction parameters."""
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        if type(self.positive_bonds) is not tuple or not self.positive_bonds:
            raise TypeError("positive_bonds must be a nonempty tuple")
        if any(
            type(bond) is not tuple
            or len(bond) != 3
            or any(type(component) is not int for component in bond)
            or bond == (0, 0, 0)
            for bond in self.positive_bonds
        ):
            raise TypeError("positive_bonds must contain nonzero integer triples")
        if len(set(self.positive_bonds)) != len(self.positive_bonds):
            raise ValueError("positive_bonds must be unique")
        if type(self.hopping_scale) is not float:
            raise TypeError("hopping_scale must be a built-in float")
        if not math.isfinite(self.hopping_scale):
            raise ValueError("hopping_scale must be finite")

    @property
    def ambient_dimension(self) -> int:
        """Return the ordered retained-plus-exterior basis size."""
        return 2 * self.retained_rank

    @property
    def basis_identifier(self) -> str:
        """Return the ordered ambient primitive-cell basis identity."""
        return (
            f"{self.MODEL_FAMILY_IDENTITY}:"
            f"ambient-retained-then-exterior-r{self.retained_rank:02d}"
        )

    @property
    def model_identifier(self) -> str:
        """Return an identity containing every model-defining construction input."""
        canonical_bonds = tuple(
            sorted(
                min(
                    bond,
                    (-bond[0], -bond[1], -bond[2]),
                )
                for bond in self.positive_bonds
            )
        )
        bond_identity = ";".join(
            ",".join(str(component) for component in bond) for bond in canonical_bonds
        )
        canonical_scale = 0.0 if self.hopping_scale == 0.0 else self.hopping_scale
        return (
            f"{self.MODEL_FAMILY_IDENTITY}:r{self.retained_rank:02d}:"
            f"hopping-scale-{canonical_scale.hex()}:bonds-{bond_identity}"
        )

    def execute(self) -> DenseBlockHoppingModel:
        """Construct the exact onsite, first-, and second-harmonic blocks."""
        rank = self.retained_rank
        orbital_index = np.arange(rank, dtype=np.float64)
        orbital_coordinates = (2.0 * orbital_index - rank + 1.0) / (rank - 1.0)
        onsite_diagonal = np.concatenate(
            (
                0.4 * orbital_coordinates,
                3.0 + 0.3 * orbital_coordinates,
            )
        ).astype(np.complex128)
        coefficient_diagonals: dict[tuple[int, int, int], Complex128Array] = {
            (0, 0, 0): onsite_diagonal
        }

        if self.hopping_scale != 0.0:
            bond_count = len(self.positive_bonds)
            for harmonic, retained_weight, exterior_weight in (
                (1, 0.25 * 0.75 / (2.0 * bond_count), 0.1 * 0.75 / (2.0 * bond_count)),
                (2, 0.25 * 0.25 / (2.0 * bond_count), 0.1 * 0.25 / (2.0 * bond_count)),
            ):
                hopping_diagonal = (
                    self.hopping_scale
                    * np.concatenate(
                        (
                            retained_weight * (1.0 + 0.2 * orbital_coordinates),
                            np.full(rank, exterior_weight, dtype=np.float64),
                        )
                    )
                ).astype(np.complex128)
                for bond in self.positive_bonds:
                    displacement = (
                        harmonic * bond[0],
                        harmonic * bond[1],
                        harmonic * bond[2],
                    )
                    for sign in (-1, 1):
                        signed_displacement = (
                            sign * displacement[0],
                            sign * displacement[1],
                            sign * displacement[2],
                        )
                        previous = coefficient_diagonals.get(signed_displacement)
                        if previous is None:
                            coefficient_diagonals[signed_displacement] = (
                                hopping_diagonal.copy()
                            )
                        else:
                            coefficient_diagonals[signed_displacement] = (
                                previous + hopping_diagonal
                            )

        energy_unit = Unitless()
        terms = tuple(
            DenseBlockHoppingTerm(
                displacement=LatticeDisplacement(
                    dimension=LatticeDimension.THREE,
                    components=displacement,
                ),
                coefficient=ComplexMatrixQuantity(
                    magnitude=np.diag(diagonal).astype(np.complex128),
                    unit=energy_unit,
                ),
            )
            for displacement, diagonal in sorted(coefficient_diagonals.items())
        )
        return DenseBlockHoppingModel(
            identifier=self.model_identifier,
            dimension=LatticeDimension.THREE,
            terms=terms,
            energy_unit=energy_unit,
            energy_reference=self.ENERGY_REFERENCE,
            basis_identifier=self.basis_identifier,
        )


__all__ = ["Periodic3DRankNBlockHoppingParentBuilder"]
