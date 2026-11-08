"""Test-owned structured bases and parents for periodic-1D synthetic cases."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy as np
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.operators import LabeledComponentBasisCoordinate
from ksdft2effmass.periodic.periodic1d.operators import Periodic1DBasisIdentity
from ksdft2effmass.periodic.periodic1d.rankN.models import Periodic1DRankNParentModel

_TEST_LABELS: dict[int, tuple[str, ...]] = {
    3: ("test-orbital-a", "test-orbital-b", "test-orbital-c"),
    4: (
        "test-orbital-a",
        "test-orbital-b",
        "test-orbital-c",
        "test-orbital-d",
    ),
}


def synthetic_basis_identity(retained_rank: int) -> Periodic1DBasisIdentity:
    """Return an explicit synthetic basis from the reviewed test inventory."""
    try:
        labels = _TEST_LABELS[retained_rank]
    except KeyError as error:
        raise ValueError("retained_rank is not in the test basis inventory") from error
    return Periodic1DBasisIdentity(
        display_identifier=f"periodic1d-rankN-test-basis-r{retained_rank:02d}",
        coordinates=tuple(
            LabeledComponentBasisCoordinate(label=label) for label in labels
        ),
    )


@dataclass(frozen=True, slots=True, eq=False)
class SyntheticPeriodic1DRankNParentModel(Periodic1DRankNParentModel):
    """Implement the analytic parent formula only in test verification support."""

    MODEL_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.test.periodic1d-rankN-analytic-parent.v1"
    )

    retained_rank: int
    basis: Periodic1DBasisIdentity
    reference_frame: ComplexArray = field(repr=False)
    sewing_map: ComplexArray = field(repr=False)

    def __post_init__(self) -> None:
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        if type(self.basis) is not Periodic1DBasisIdentity:
            raise TypeError("basis must be the exact Periodic1DBasisIdentity")
        if self.basis.dimension != self.retained_rank:
            raise ValueError("basis dimension must equal retained_rank")
        reference = NumpyImmutableArrayConstructor(
            self.reference_frame,
            "reference_frame",
            np.dtype(np.complex128),
        ).execute()
        sewing = NumpyImmutableArrayConstructor(
            self.sewing_map,
            "sewing_map",
            np.dtype(np.complex128),
        ).execute()
        expected_reference = np.zeros(
            (self.ambient_dimension, self.retained_rank),
            dtype=np.complex128,
        )
        expected_reference[: self.retained_rank] = np.eye(
            self.retained_rank,
            dtype=np.complex128,
        )
        if not np.array_equal(reference, expected_reference):
            raise ValueError(
                "reference_frame must be the retained-coordinate embedding"
            )
        if not np.array_equal(
            sewing,
            np.eye(self.ambient_dimension, dtype=np.complex128),
        ):
            raise ValueError("sewing_map must be the identity")
        object.__setattr__(self, "reference_frame", reference)
        object.__setattr__(self, "sewing_map", sewing)

    @property
    def model_id(self) -> str:
        return f"{self.MODEL_FAMILY_IDENTITY}:r{self.retained_rank:02d}"

    @property
    def model_role(self) -> PeriodicModelRole:
        return PeriodicModelRole.CONTROL_MODEL

    @property
    def basis_identity(self) -> Periodic1DBasisIdentity:
        return self.basis

    @property
    def band_subspace_rank(self) -> int:
        return self.retained_rank

    @property
    def ambient_dimension(self) -> int:
        return 2 * self.retained_rank

    @property
    def endpoint_sewing_map(self) -> ComplexArray:
        return self.sewing_map

    @property
    def exact_isolation_gap(self) -> float:
        return 2.1

    @staticmethod
    def _coordinates(value: RealArray) -> RealArray:
        coordinates = NumpyImmutableArrayConstructor(
            value,
            "reduced_coordinates",
            np.dtype(np.float64),
        ).execute()
        if coordinates.ndim != 1 or coordinates.size == 0:
            raise ValueError("reduced_coordinates must be a nonempty vector")
        return coordinates

    def retained_energies(self, reduced_coordinates: RealArray) -> RealArray:
        coordinates = self._coordinates(reduced_coordinates)
        phase = 2.0 * np.pi * coordinates
        harmonic = 0.75 * np.cos(phase) + 0.25 * np.cos(2.0 * phase)
        orbital = np.arange(self.retained_rank, dtype=np.float64)
        normalized = (2.0 * orbital - self.retained_rank + 1.0) / (
            self.retained_rank - 1.0
        )
        return np.asarray(
            0.4 * normalized[None, :]
            + 0.25 * (1.0 + 0.2 * normalized[None, :]) * harmonic[:, None],
            dtype=np.float64,
        )

    def exterior_energies(self, reduced_coordinates: RealArray) -> RealArray:
        coordinates = self._coordinates(reduced_coordinates)
        phase = 2.0 * np.pi * coordinates
        harmonic = 0.75 * np.cos(phase) + 0.25 * np.cos(2.0 * phase)
        orbital = np.arange(self.retained_rank, dtype=np.float64)
        normalized = (2.0 * orbital - self.retained_rank + 1.0) / (
            self.retained_rank - 1.0
        )
        return np.asarray(
            3.0 + 0.3 * normalized[None, :] + 0.1 * harmonic[:, None],
            dtype=np.float64,
        )

    def parent_hamiltonians(self, reduced_coordinates: RealArray) -> ComplexArray:
        diagonal = np.concatenate(
            (
                self.retained_energies(reduced_coordinates),
                self.exterior_energies(reduced_coordinates),
            ),
            axis=1,
        )
        identity = np.eye(self.ambient_dimension, dtype=np.complex128)
        return np.asarray(
            diagonal[:, :, None] * identity[None, :, :],
            dtype=np.complex128,
        )

    def reference_frames(self, reduced_coordinates: RealArray) -> ComplexArray:
        coordinates = self._coordinates(reduced_coordinates)
        return np.broadcast_to(
            self.reference_frame,
            (coordinates.size,) + self.reference_frame.shape,
        ).copy()

    def exact_reduced_hamiltonians(
        self,
        reduced_coordinates: RealArray,
    ) -> ComplexArray:
        energies = self.retained_energies(reduced_coordinates)
        identity = np.eye(self.retained_rank, dtype=np.complex128)
        return np.asarray(
            energies[:, :, None] * identity[None, :, :],
            dtype=np.complex128,
        )


def synthetic_parent_model(retained_rank: int) -> SyntheticPeriodic1DRankNParentModel:
    """Return an explicit analytic parent from the test-owned basis inventory."""
    ambient_dimension = 2 * retained_rank
    frame = np.zeros((ambient_dimension, retained_rank), dtype=np.complex128)
    frame[:retained_rank] = np.eye(retained_rank, dtype=np.complex128)
    return SyntheticPeriodic1DRankNParentModel(
        retained_rank=retained_rank,
        basis=synthetic_basis_identity(retained_rank),
        reference_frame=frame,
        sewing_map=np.eye(ambient_dimension, dtype=np.complex128),
    )


__all__ = [
    "SyntheticPeriodic1DRankNParentModel",
    "synthetic_basis_identity",
    "synthetic_parent_model",
]
