"""Test-owned analytic periodic-2D finite-rank composition support."""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import product
from typing import ClassVar

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.operators import PeriodicBasisInventory
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity
from ksdft2effmass.periodic.periodic2d.rankN.models import Periodic2DRankNParentModel
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.case import (
    Periodic2DRankNParentGaugeCase,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.request import (
    Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.transformation import (
    Periodic2DRankNGivensGaugeTransformation,
)


@dataclass(frozen=True, slots=True, eq=False)
class SyntheticPeriodic2DRankNParentModel(Periodic2DRankNParentModel):
    """Define one separated-sector synthetic parent on the reduced reciprocal torus.

    Parameters
    ----------
    retained_rank
        Finite retained-sector dimension, at least two.
    bond_inventory
        Unique nonzero integer harmonic vectors in reduced reciprocal coordinates.
    coupling_scale
        Finite dimensionless coupling in the closed interval ``[0, 1]``.
    basis
        Exact ordered retained-sector basis identity.
    role
        Explicit evidentiary role of this scientific model.

    Notes
    -----
    This test value supplies only the parent and retained embedding. Reusable source
    owns the contract, while gauge transformations and study composition stay separate.
    """

    MODEL_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic2d-rankN-analytic-parent.v1"
    )
    NORM_ENERGY_SCALE: ClassVar[float] = 1.0
    EXTERNAL_GAP_LOWER_BOUND: ClassVar[float] = 1.9

    retained_rank: int
    bond_inventory: tuple[tuple[int, int], ...]
    coupling_scale: float
    basis: Periodic2DBasisIdentity
    role: PeriodicModelRole

    def __post_init__(self) -> None:
        """Validate the finite-rank parent and its exact basis correlation."""
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        if type(self.bond_inventory) is not tuple or not self.bond_inventory:
            raise TypeError("bond_inventory must be a nonempty tuple")
        if any(
            type(bond) is not tuple
            or len(bond) != 2
            or any(type(component) is not int for component in bond)
            or bond == (0, 0)
            for bond in self.bond_inventory
        ):
            raise TypeError("bond_inventory must contain nonzero integer pairs")
        if len(set(self.bond_inventory)) != len(self.bond_inventory):
            raise ValueError("bond_inventory must be unique")
        if type(self.coupling_scale) is not float:
            raise TypeError("coupling_scale must be a built-in float")
        if not math.isfinite(self.coupling_scale):
            raise ValueError("coupling_scale must be finite")
        if not 0.0 <= self.coupling_scale <= 1.0:
            raise ValueError("coupling_scale must be in the closed interval [0, 1]")
        if type(self.basis) is not Periodic2DBasisIdentity:
            raise TypeError("basis must be the exact Periodic2DBasisIdentity type")
        if self.basis.dimension != self.retained_rank:
            raise ValueError("basis dimension must match retained_rank")
        if type(self.role) is not PeriodicModelRole:
            raise TypeError("role must be PeriodicModelRole")

    @property
    def model_id(self) -> str:
        """Return the stable parent identity independently of any transformation."""
        bonds = ";".join(
            ",".join(str(component) for component in bond)
            for bond in self.bond_inventory
        )
        return (
            f"{self.MODEL_FAMILY_IDENTITY}:"
            f"role-{self.model_role.to_wire()}:r{self.retained_rank:02d}:"
            f"bonds-{bonds}:lambda-{self.coupling_scale.hex()}"
        )

    @property
    def positive_bonds(self) -> tuple[tuple[int, int], ...]:
        """Return the test-owned harmonic support."""
        return self.bond_inventory

    @property
    def parent_scale(self) -> float:
        """Return the test-owned parent coupling scale."""
        return self.coupling_scale

    @property
    def isolation_gap_lower_bound(self) -> float:
        """Return the conservative gap lower bound for this synthetic family."""
        return self.EXTERNAL_GAP_LOWER_BOUND

    @property
    def model_role(self) -> PeriodicModelRole:
        """Return the explicitly supplied evidentiary role."""
        return self.role

    @property
    def basis_identity(self) -> Periodic2DBasisIdentity:
        """Return the exact ordered retained-sector basis identity."""
        return self.basis

    @property
    def band_subspace_rank(self) -> int:
        """Return the finite retained-sector rank."""
        return self.retained_rank

    @property
    def ambient_dimension(self) -> int:
        """Return the retained-plus-exterior parent dimension."""
        return 2 * self.retained_rank

    @staticmethod
    def _immutable_float(value: Float64Array, name: str) -> Float64Array:
        return NumpyImmutableArrayConstructor(
            value,
            name,
            np.dtype(np.float64),
        ).execute()

    @staticmethod
    def _immutable_complex(value: Complex128Array, name: str) -> Complex128Array:
        return NumpyImmutableArrayConstructor(
            value,
            name,
            np.dtype(np.complex128),
        ).execute()

    def _coordinates(self, value: Float64Array) -> Float64Array:
        coordinates = self._immutable_float(value, "reduced_coordinates")
        if coordinates.ndim < 2 or coordinates.shape[-1] != 2:
            raise ValueError("reduced_coordinates must have shape (..., 2)")
        if any(size <= 0 for size in coordinates.shape[:-1]):
            raise ValueError("reduced-coordinate mesh axes must be nonempty")
        return coordinates

    def structure_factor(self, reduced_coordinates: Float64Array) -> Float64Array:
        """Return the normalized first/second-harmonic structure factor."""
        coordinates = self._coordinates(reduced_coordinates)
        bonds = np.asarray(self.bond_inventory, dtype=np.float64)
        arguments = 2.0 * np.pi * np.einsum("...d,bd->...b", coordinates, bonds)
        values = np.mean(
            0.75 * np.cos(arguments) + 0.25 * np.cos(2.0 * arguments),
            axis=-1,
        )
        return self._immutable_float(
            np.asarray(values, dtype=np.float64),
            "structure_factor",
        )

    def _orbital_coordinates(self) -> Float64Array:
        orbital = np.arange(self.retained_rank, dtype=np.float64)
        values = (2.0 * orbital - self.retained_rank + 1.0) / (self.retained_rank - 1.0)
        return np.asarray(values, dtype=np.float64)

    def retained_energies(self, reduced_coordinates: Float64Array) -> Float64Array:
        """Return the strictly ordered retained-sector energies."""
        structure = self.structure_factor(reduced_coordinates)
        orbital = self._orbital_coordinates()
        values = 0.4 * orbital + (
            0.25 * self.coupling_scale * (1.0 + 0.2 * orbital) * structure[..., None]
        )
        return self._immutable_float(
            np.asarray(values, dtype=np.float64),
            "retained_energies",
        )

    def exterior_energies(self, reduced_coordinates: Float64Array) -> Float64Array:
        """Return the separated exterior-sector energies."""
        structure = self.structure_factor(reduced_coordinates)
        orbital = self._orbital_coordinates()
        values = 3.0 + 0.3 * orbital + 0.1 * self.coupling_scale * structure[..., None]
        return self._immutable_float(
            np.asarray(values, dtype=np.float64),
            "exterior_energies",
        )

    def parent_hamiltonians(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return diagonal parent operators in the ordered ambient coordinates."""
        retained = self.retained_energies(reduced_coordinates)
        exterior = self.exterior_energies(reduced_coordinates)
        diagonal = np.concatenate((retained, exterior), axis=-1)
        identity = np.eye(self.ambient_dimension, dtype=np.complex128)
        values = diagonal[..., :, None] * identity
        return self._immutable_complex(
            np.asarray(values, dtype=np.complex128),
            "parent_hamiltonians",
        )

    def reference_frames(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return the constant retained-coordinate embedding on one mesh."""
        coordinates = self._coordinates(reduced_coordinates)
        frame = np.zeros(
            (self.ambient_dimension, self.retained_rank),
            dtype=np.complex128,
        )
        frame[: self.retained_rank] = np.eye(
            self.retained_rank,
            dtype=np.complex128,
        )
        values = np.broadcast_to(frame, (*coordinates.shape[:-1], *frame.shape)).copy()
        return self._immutable_complex(values, "reference_frames")

    def exact_reduced_hamiltonians(
        self,
        reduced_coordinates: Float64Array,
    ) -> Complex128Array:
        """Return retained operators in the analytic reference frame."""
        energies = self.retained_energies(reduced_coordinates)
        identity = np.eye(self.retained_rank, dtype=np.complex128)
        values = energies[..., :, None] * identity
        return self._immutable_complex(
            np.asarray(values, dtype=np.complex128),
            "exact_reduced_hamiltonians",
        )


class SyntheticPeriodic2DRankNCaseExpander:
    """Construct the historical analytic cross product only for tests."""

    def __init__(
        self,
        *,
        request: Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
        basis_inventory: PeriodicBasisInventory[Periodic2DBasisIdentity],
    ) -> None:
        if type(request) is not Periodic2DRankNBandEquivalenceHoppingLocalityRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")
        if type(basis_inventory) is not PeriodicBasisInventory:
            raise TypeError("basis_inventory must be the exact PeriodicBasisInventory")
        if basis_inventory.retained_ranks != request.retained_ranks:
            raise ValueError("basis inventory ranks must match the requested ranks")
        self._request = request
        self._basis_inventory = basis_inventory

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        return self._request.band_subspace_ranks

    def execute(self) -> tuple[Periodic2DRankNParentGaugeCase, ...]:
        inventory = product(
            self._request.cases,
            self._request.retained_ranks,
            self._request.circuit_depths,
            self._request.parent_scales,
            self._request.transformation_coefficients,
        )
        return tuple(
            Periodic2DRankNParentGaugeCase(
                case_identifier=values[0].identifier,
                parent_model=SyntheticPeriodic2DRankNParentModel(
                    retained_rank=values[1],
                    bond_inventory=values[0].positive_bonds,
                    coupling_scale=values[3],
                    basis=self._basis_inventory.basis_identity_for_rank(values[1]),
                    role=PeriodicModelRole.CONTROL_MODEL,
                ),
                gauge_transformation=Periodic2DRankNGivensGaugeTransformation(
                    retained_rank=values[1],
                    circuit_depth=values[2],
                    harmonic_bonds=values[0].positive_bonds,
                    normalization=values[0].gauge_normalization,
                    coefficient=values[4],
                ),
            )
            for values in inventory
        )


__all__ = [
    "SyntheticPeriodic2DRankNCaseExpander",
    "SyntheticPeriodic2DRankNParentModel",
]
