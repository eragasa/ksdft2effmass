"""Dimensionless analytic periodic-2D finite-rank parent models."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import ClassVar

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity

from .base import Periodic2DRankNModel


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNAnalyticParentModel(Periodic2DRankNModel):
    """Define one separated-sector synthetic parent on the reduced reciprocal torus.

    Parameters
    ----------
    retained_rank
        Finite retained-sector dimension, at least two.
    positive_bonds
        Unique nonzero integer harmonic vectors in reduced reciprocal coordinates.
    parent_scale
        Finite dimensionless coupling in the closed interval ``[0, 1]``.
    basis
        Exact ordered retained-sector basis identity.
    role
        Explicit evidentiary role of this scientific model.

    Notes
    -----
    This model owns only the parent and retained embedding. Gauge transformations,
    study case identities, geometry, meshes, and calculation inventories are separate.
    """

    MODEL_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic2d-rankN-analytic-parent.v1"
    )
    NORM_ENERGY_SCALE: ClassVar[float] = 1.0
    EXTERNAL_GAP_LOWER_BOUND: ClassVar[float] = 1.9

    retained_rank: int
    positive_bonds: tuple[tuple[int, int], ...]
    parent_scale: float
    basis: Periodic2DBasisIdentity
    role: PeriodicModelRole = field(kw_only=True)

    def __post_init__(self) -> None:
        """Validate the finite-rank parent and its exact basis correlation."""
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        if type(self.positive_bonds) is not tuple or not self.positive_bonds:
            raise TypeError("positive_bonds must be a nonempty tuple")
        if any(
            type(bond) is not tuple
            or len(bond) != 2
            or any(type(component) is not int for component in bond)
            or bond == (0, 0)
            for bond in self.positive_bonds
        ):
            raise TypeError("positive_bonds must contain nonzero integer pairs")
        if len(set(self.positive_bonds)) != len(self.positive_bonds):
            raise ValueError("positive_bonds must be unique")
        if type(self.parent_scale) is not float:
            raise TypeError("parent_scale must be a built-in float")
        if not math.isfinite(self.parent_scale):
            raise ValueError("parent_scale must be finite")
        if not 0.0 <= self.parent_scale <= 1.0:
            raise ValueError("parent_scale must be in the closed interval [0, 1]")
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
            for bond in self.positive_bonds
        )
        return (
            f"{self.MODEL_FAMILY_IDENTITY}:"
            f"role-{self.model_role.to_wire()}:r{self.retained_rank:02d}:"
            f"bonds-{bonds}:lambda-{self.parent_scale.hex()}"
        )

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
        bonds = np.asarray(self.positive_bonds, dtype=np.float64)
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
            0.25 * self.parent_scale * (1.0 + 0.2 * orbital) * structure[..., None]
        )
        return self._immutable_float(
            np.asarray(values, dtype=np.float64),
            "retained_energies",
        )

    def exterior_energies(self, reduced_coordinates: Float64Array) -> Float64Array:
        """Return the separated exterior-sector energies."""
        structure = self.structure_factor(reduced_coordinates)
        orbital = self._orbital_coordinates()
        values = 3.0 + 0.3 * orbital + 0.1 * self.parent_scale * structure[..., None]
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


__all__ = ["Periodic2DRankNAnalyticParentModel"]
