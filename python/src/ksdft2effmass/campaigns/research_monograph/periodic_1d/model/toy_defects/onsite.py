"""Localized onsite toy defects on finite periodic-1D cells."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

type ComplexMatrix = npt.NDArray[np.complex128]
type IntegerVector = npt.NDArray[np.int64]
type RealVector = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class Periodic1DGaussianOnsiteDefectModel:
    """Represent a dimensionless Gaussian onsite operator perturbation."""

    width_cells: float
    strength: float
    orbital_block: ComplexMatrix

    def __post_init__(self) -> None:
        if type(self.width_cells) is not float:
            raise TypeError("width_cells must be a float")
        if type(self.strength) is not float:
            raise TypeError("strength must be a float")
        if not np.isfinite(self.width_cells) or self.width_cells <= 0.0:
            raise ValueError("width_cells must be positive and finite")
        if not np.isfinite(self.strength):
            raise ValueError("strength must be finite")
        block = np.asarray(self.orbital_block, dtype=np.complex128)
        if block.ndim != 2 or block.shape[0] == 0 or block.shape[0] != block.shape[1]:
            raise ValueError("orbital_block must be nonempty and square")
        if not np.all(np.isfinite(block)):
            raise ValueError("orbital_block must contain only finite values")
        if not np.array_equal(block, block.conj().T):
            raise ValueError("orbital_block must be Hermitian")
        immutable = np.frombuffer(
            block.tobytes(order="C"), dtype=np.complex128
        ).reshape(block.shape)
        object.__setattr__(self, "orbital_block", immutable)

    @property
    def orbital_count(self) -> int:
        """Return the onsite block dimension."""
        return int(self.orbital_block.shape[0])


@dataclass(frozen=True, slots=True)
class Periodic1DGaussianOnsiteDefectRequest:
    """Request one represented Gaussian onsite perturbation."""

    model: Periodic1DGaussianOnsiteDefectModel
    cell_count: int

    def __post_init__(self) -> None:
        if type(self.model) is not Periodic1DGaussianOnsiteDefectModel:
            raise TypeError("model must be Periodic1DGaussianOnsiteDefectModel")
        if isinstance(self.cell_count, bool) or not isinstance(self.cell_count, int):
            raise TypeError("cell_count must be an integer")
        if self.cell_count < 1:
            raise ValueError("cell_count must be positive")


@dataclass(frozen=True, slots=True)
class Periodic1DGaussianOnsiteDefectResult:
    """Retain the represented perturbation and its minimum-image profile."""

    coordinates_cells: IntegerVector
    profile: RealVector
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        coordinates = np.asarray(self.coordinates_cells, dtype=np.int64)
        profile = np.asarray(self.profile, dtype=np.float64)
        matrix = np.asarray(self.matrix, dtype=np.complex128)
        if coordinates.ndim != 1 or coordinates.size == 0:
            raise ValueError("coordinates_cells must be a nonempty vector")
        if profile.shape != coordinates.shape or not np.all(np.isfinite(profile)):
            raise ValueError("profile must be finite and match coordinates")
        if (
            matrix.ndim != 2
            or matrix.shape[0] == 0
            or matrix.shape[0] != matrix.shape[1]
        ):
            raise ValueError("matrix must be nonempty and square")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("matrix must contain only finite values")
        immutable_coordinates = np.frombuffer(
            coordinates.tobytes(order="C"), dtype=np.int64
        ).reshape(coordinates.shape)
        immutable_profile = np.frombuffer(
            profile.tobytes(order="C"), dtype=np.float64
        ).reshape(profile.shape)
        immutable_matrix = np.frombuffer(
            matrix.tobytes(order="C"), dtype=np.complex128
        ).reshape(matrix.shape)
        object.__setattr__(self, "coordinates_cells", immutable_coordinates)
        object.__setattr__(self, "profile", immutable_profile)
        object.__setattr__(self, "matrix", immutable_matrix)


class Periodic1DGaussianOnsiteDefectConstructor:
    """Construct a minimum-image Gaussian onsite perturbation."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DGaussianOnsiteDefectRequest
    ) -> Periodic1DGaussianOnsiteDefectResult:
        """Evaluate the profile and block-diagonal represented operator."""
        model = request.model
        indices = np.arange(request.cell_count, dtype=np.int64)
        coordinates = np.where(
            indices <= request.cell_count // 2,
            indices,
            indices - request.cell_count,
        )
        profile = model.strength * np.exp(
            -np.square(coordinates) / (2.0 * model.width_cells**2)
        )
        block_size = model.orbital_count
        matrix = np.zeros(
            (block_size * request.cell_count, block_size * request.cell_count),
            dtype=np.complex128,
        )
        for site, value in enumerate(profile):
            matrix[
                block_size * site : block_size * (site + 1),
                block_size * site : block_size * (site + 1),
            ] = value * model.orbital_block
        return Periodic1DGaussianOnsiteDefectResult(
            coordinates,
            np.asarray(profile, dtype=np.float64),
            matrix,
        )
