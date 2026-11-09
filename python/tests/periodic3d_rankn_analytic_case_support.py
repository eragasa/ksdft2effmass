"""Test-owned analytic periodic-3D finite-rank composition support."""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import product
from typing import ClassVar

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.operators import (
    LabeledComponentBasisCoordinate,
    PeriodicBasisInventory,
    PeriodicBasisInventoryEntry,
)
from ksdft2effmass.periodic.periodic3d.operators import Periodic3DBasisIdentity
from ksdft2effmass.periodic.periodic3d.rankN.models import Periodic3DRankNParentModel
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.case import (
    Periodic3DRankNParentGaugeCase,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.request import (
    Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.transformation import (
    Periodic3DRankNGivensGaugeTransformation,
)

PERIODIC3D_RANK_N_TEST_BASIS_INVENTORY = PeriodicBasisInventory(
    entries=tuple(
        PeriodicBasisInventoryEntry(
            retained_rank=rank,
            basis_identity=Periodic3DBasisIdentity(
                display_identifier=f"periodic3d-rankN-test-basis-r{rank}",
                coordinates=tuple(
                    LabeledComponentBasisCoordinate(
                        label=f"test-retained-orbital-{index:02d}"
                    )
                    for index in range(rank)
                ),
            ),
        )
        for rank in (3, 4, 8)
    )
)


@dataclass(frozen=True, slots=True, eq=False)
class SyntheticPeriodic3DRankNParentModel(Periodic3DRankNParentModel):
    """Define one test-owned separated-sector parent on a reciprocal three-torus."""

    MODEL_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic3d-rankN-analytic-parent.v1"
    )
    EXTERNAL_GAP_LOWER_BOUND: ClassVar[float] = 1.9

    retained_rank: int
    bond_inventory: tuple[tuple[int, int, int], ...]
    coupling_scale: float
    basis: Periodic3DBasisIdentity
    role: PeriodicModelRole

    def __post_init__(self) -> None:
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        if type(self.bond_inventory) is not tuple or not self.bond_inventory:
            raise TypeError("bond_inventory must be a nonempty tuple")
        if any(
            type(bond) is not tuple
            or len(bond) != 3
            or any(type(component) is not int for component in bond)
            or bond == (0, 0, 0)
            for bond in self.bond_inventory
        ):
            raise TypeError("bond_inventory must contain nonzero integer triples")
        if len(set(self.bond_inventory)) != len(self.bond_inventory):
            raise ValueError("bond_inventory must be unique")
        if type(self.coupling_scale) is not float:
            raise TypeError("coupling_scale must be a built-in float")
        if not math.isfinite(self.coupling_scale):
            raise ValueError("coupling_scale must be finite")
        if not 0.0 <= self.coupling_scale <= 1.0:
            raise ValueError("coupling_scale must be in the closed interval [0, 1]")
        if type(self.basis) is not Periodic3DBasisIdentity:
            raise TypeError("basis must be the exact Periodic3DBasisIdentity type")
        if self.basis.dimension != self.retained_rank:
            raise ValueError("basis dimension must match retained_rank")
        if type(self.role) is not PeriodicModelRole:
            raise TypeError("role must be PeriodicModelRole")

    @property
    def model_id(self) -> str:
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
    def model_role(self) -> PeriodicModelRole:
        return self.role

    @property
    def basis_identity(self) -> Periodic3DBasisIdentity:
        return self.basis

    @property
    def band_subspace_rank(self) -> int:
        return self.retained_rank

    @property
    def positive_bonds(self) -> tuple[tuple[int, int, int], ...]:
        return self.bond_inventory

    @property
    def parent_scale(self) -> float:
        return self.coupling_scale

    @property
    def ambient_dimension(self) -> int:
        return 2 * self.retained_rank

    @property
    def isolation_gap_lower_bound(self) -> float:
        return self.EXTERNAL_GAP_LOWER_BOUND

    @staticmethod
    def _immutable_float(value: Float64Array) -> Float64Array:
        return NumpyImmutableArrayConstructor(
            value,
            "analytic_float_result",
            np.dtype(np.float64),
        ).execute()

    @staticmethod
    def _immutable_complex(value: Complex128Array) -> Complex128Array:
        return NumpyImmutableArrayConstructor(
            value,
            "analytic_complex_result",
            np.dtype(np.complex128),
        ).execute()

    def _coordinates(self, value: Float64Array) -> Float64Array:
        coordinates = NumpyImmutableArrayConstructor(
            value,
            "reduced_coordinates",
            np.dtype(np.float64),
        ).execute()
        if coordinates.ndim < 2 or coordinates.shape[-1] != 3:
            raise ValueError("reduced_coordinates must have shape (..., 3)")
        if any(size <= 0 for size in coordinates.shape[:-1]):
            raise ValueError("reduced-coordinate mesh axes must be nonempty")
        return coordinates

    def structure_factor(self, reduced_coordinates: Float64Array) -> Float64Array:
        coordinates = self._coordinates(reduced_coordinates)
        bonds = np.asarray(self.bond_inventory, dtype=np.float64)
        arguments = 2.0 * np.pi * np.einsum("...d,bd->...b", coordinates, bonds)
        values = np.mean(
            0.75 * np.cos(arguments) + 0.25 * np.cos(2.0 * arguments),
            axis=-1,
        )
        return self._immutable_float(np.asarray(values, dtype=np.float64))

    def _orbital_coordinates(self) -> Float64Array:
        orbital = np.arange(self.retained_rank, dtype=np.float64)
        return np.asarray(
            (2.0 * orbital - self.retained_rank + 1.0) / (self.retained_rank - 1.0),
            dtype=np.float64,
        )

    def retained_energies(self, reduced_coordinates: Float64Array) -> Float64Array:
        structure = self.structure_factor(reduced_coordinates)
        orbital = self._orbital_coordinates()
        values = 0.4 * orbital + (
            0.25 * self.coupling_scale * (1.0 + 0.2 * orbital) * structure[..., None]
        )
        return self._immutable_float(np.asarray(values, dtype=np.float64))

    def exterior_energies(self, reduced_coordinates: Float64Array) -> Float64Array:
        structure = self.structure_factor(reduced_coordinates)
        orbital = self._orbital_coordinates()
        values = 3.0 + 0.3 * orbital + 0.1 * self.coupling_scale * structure[..., None]
        return self._immutable_float(np.asarray(values, dtype=np.float64))

    def parent_hamiltonians(self, reduced_coordinates: Float64Array) -> Complex128Array:
        retained = self.retained_energies(reduced_coordinates)
        exterior = self.exterior_energies(reduced_coordinates)
        diagonal = np.concatenate((retained, exterior), axis=-1)
        identity = np.eye(self.ambient_dimension, dtype=np.complex128)
        values = diagonal[..., :, None] * identity
        return self._immutable_complex(np.asarray(values, dtype=np.complex128))

    def reference_frames(self, reduced_coordinates: Float64Array) -> Complex128Array:
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
        return self._immutable_complex(values)

    def exact_reduced_hamiltonians(
        self,
        reduced_coordinates: Float64Array,
    ) -> Complex128Array:
        energies = self.retained_energies(reduced_coordinates)
        identity = np.eye(self.retained_rank, dtype=np.complex128)
        values = energies[..., :, None] * identity
        return self._immutable_complex(np.asarray(values, dtype=np.complex128))


class SyntheticPeriodic3DRankNCaseExpander:
    """Construct the historical analytic cross product only for tests."""

    def __init__(
        self,
        *,
        request: Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
        basis_inventory: PeriodicBasisInventory[Periodic3DBasisIdentity] = (
            PERIODIC3D_RANK_N_TEST_BASIS_INVENTORY
        ),
    ) -> None:
        if type(request) is not Periodic3DRankNBandEquivalenceHoppingLocalityRequest:
            raise TypeError("request must be the exact periodic-3D rank-N request")
        if type(basis_inventory) is not PeriodicBasisInventory:
            raise TypeError("basis_inventory must be the exact PeriodicBasisInventory")
        if basis_inventory.retained_ranks != request.retained_ranks:
            raise ValueError("basis inventory ranks must match the requested ranks")
        self._request = request
        self._basis_inventory = basis_inventory

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        return self._request.band_subspace_ranks

    def execute(self) -> tuple[Periodic3DRankNParentGaugeCase, ...]:
        inventory = product(
            self._request.cases,
            self._request.retained_ranks,
            self._request.circuit_depths,
            self._request.parent_scales,
            self._request.transformation_coefficients,
        )
        return tuple(
            Periodic3DRankNParentGaugeCase(
                case_identifier=values[0].lattice_control.to_wire(),
                parent_model=SyntheticPeriodic3DRankNParentModel(
                    retained_rank=values[1],
                    bond_inventory=values[0].positive_bonds,
                    coupling_scale=values[3],
                    basis=self._basis_inventory.basis_identity_for_rank(values[1]),
                    role=PeriodicModelRole.CONTROL_MODEL,
                ),
                gauge_transformation=Periodic3DRankNGivensGaugeTransformation(
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
    "PERIODIC3D_RANK_N_TEST_BASIS_INVENTORY",
    "SyntheticPeriodic3DRankNCaseExpander",
    "SyntheticPeriodic3DRankNParentModel",
]
