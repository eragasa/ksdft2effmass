"""Localized onsite perturbations for finite periodic one-dimensional cells."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

type ComplexMatrix = npt.NDArray[np.complex128]
type IntegerVector = npt.NDArray[np.int64]
type RealVector = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class Periodic1DGaussianOnsitePerturbationDefinition:
    """Define a dimensionless Gaussian onsite operator perturbation.

    Parameters
    ----------
    width_cells
        Positive Gaussian width in primitive-cell units.
    strength
        Finite dimensionless profile amplitude.
    orbital_block
        Finite nonempty Hermitian orbital block multiplied by the scalar profile.

    Raises
    ------
    TypeError
        If either scalar is not an exact built-in ``float``.
    ValueError
        If a scalar is nonfinite, the width is nonpositive, or the orbital block is
        empty, nonsquare, nonfinite, or non-Hermitian.
    OverflowError
        If conversion to complex128 cannot represent an input value.
    MemoryError
        If immutable block storage cannot be allocated.

    Notes
    -----
    This object defines perturbation data only. It has no pristine-parent model,
    represented state-space, compatibility, energy-reference, or provenance identity
    and therefore is not a ``Periodic1DDefectModel``.
    """

    width_cells: float
    strength: float
    orbital_block: ComplexMatrix

    def __post_init__(self) -> None:
        """Validate and freeze the intrinsic perturbation data."""
        self._check_args_scalars()
        self._check_args_orbital_block()

    def _check_args_scalars(self) -> None:
        if type(self.width_cells) is not float:
            raise TypeError("width_cells must be a float")
        if type(self.strength) is not float:
            raise TypeError("strength must be a float")
        if not np.isfinite(self.width_cells) or self.width_cells <= 0.0:
            raise ValueError("width_cells must be positive and finite")
        if not np.isfinite(self.strength):
            raise ValueError("strength must be finite")

    def _check_args_orbital_block(self) -> None:
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
        """Return the onsite orbital-block dimension.

        Returns
        -------
        int
            Positive exact built-in orbital count.
        """
        return int(self.orbital_block.shape[0])


@dataclass(frozen=True, slots=True)
class Periodic1DGaussianOnsitePerturbationRequest:
    """Request one finite representation of Gaussian perturbation data.

    Parameters
    ----------
    definition
        Exact Gaussian onsite perturbation definition.
    cell_count
        Positive exact built-in number of periodic cells.

    Raises
    ------
    TypeError
        If a field has an incompatible exact type or ``cell_count`` is boolean.
    ValueError
        If ``cell_count`` is not positive.
    """

    definition: Periodic1DGaussianOnsitePerturbationDefinition
    cell_count: int

    def __post_init__(self) -> None:
        """Validate exact definition ownership and positive extent."""
        if type(self.definition) is not Periodic1DGaussianOnsitePerturbationDefinition:
            raise TypeError(
                "definition must be Periodic1DGaussianOnsitePerturbationDefinition"
            )
        if isinstance(self.cell_count, bool) or not isinstance(self.cell_count, int):
            raise TypeError("cell_count must be an integer")
        if self.cell_count < 1:
            raise ValueError("cell_count must be positive")


@dataclass(frozen=True, slots=True)
class Periodic1DGaussianOnsitePerturbationResult:
    """Retain one represented perturbation and its minimum-image profile.

    Parameters
    ----------
    coordinates_cells
        Ordered integer minimum-image cell coordinates.
    profile
        Finite scalar profile values in matching order.
    matrix
        Finite nonempty square complex128 represented perturbation.

    Raises
    ------
    ValueError
        If vectors are empty, shapes disagree, or values are nonfinite.
    OverflowError
        If conversion to the declared NumPy representations cannot represent a value.
    MemoryError
        If immutable result storage cannot be allocated.

    Notes
    -----
    The matrix is perturbation-only. Parent-model and represented-operator identities
    are supplied by a consuming campaign operation rather than inferred here.
    """

    coordinates_cells: IntegerVector
    profile: RealVector
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        """Validate and freeze the represented perturbation arrays."""
        coordinates = np.asarray(self.coordinates_cells, dtype=np.int64)
        profile = np.asarray(self.profile, dtype=np.float64)
        matrix = np.asarray(self.matrix, dtype=np.complex128)
        self._check_args_shapes(coordinates, profile, matrix)
        self._freeze_arrays(coordinates, profile, matrix)

    def _check_args_shapes(
        self, coordinates: IntegerVector, profile: RealVector, matrix: ComplexMatrix
    ) -> None:
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

    def _freeze_arrays(
        self, coordinates: IntegerVector, profile: RealVector, matrix: ComplexMatrix
    ) -> None:
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


class Periodic1DGaussianOnsitePerturbationConstructor:
    """Construct a minimum-image Gaussian onsite perturbation matrix."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DGaussianOnsitePerturbationRequest
    ) -> Periodic1DGaussianOnsitePerturbationResult:
        """Evaluate the profile and block-diagonal represented perturbation.

        Parameters
        ----------
        request
            Exact perturbation definition and finite periodic extent.

        Returns
        -------
        Periodic1DGaussianOnsitePerturbationResult
            Ordered minimum-image coordinates, scalar profile, and dense matrix.

        Raises
        ------
        TypeError
            If ``request`` is not the exact request type.
        OverflowError
            If binary64 evaluation leaves finite representable range.
        MemoryError
            If dense matrix or result storage cannot be allocated. Matrix assembly
            scales quadratically in ``cell_count * orbital_count`` storage.
        """
        if type(request) is not Periodic1DGaussianOnsitePerturbationRequest:
            raise TypeError(
                "request must be Periodic1DGaussianOnsitePerturbationRequest"
            )
        definition = request.definition
        indices = np.arange(request.cell_count, dtype=np.int64)
        coordinates = np.where(
            indices <= request.cell_count // 2,
            indices,
            indices - request.cell_count,
        )
        profile = definition.strength * np.exp(
            -np.square(coordinates) / (2.0 * definition.width_cells**2)
        )
        if not np.all(np.isfinite(profile)):
            raise OverflowError("Gaussian profile is not finite in binary64")
        block_size = definition.orbital_count
        matrix = np.zeros(
            (block_size * request.cell_count, block_size * request.cell_count),
            dtype=np.complex128,
        )
        for site, value in enumerate(profile):
            matrix[
                block_size * site : block_size * (site + 1),
                block_size * site : block_size * (site + 1),
            ] = value * definition.orbital_block
        return Periodic1DGaussianOnsitePerturbationResult(
            coordinates,
            np.asarray(profile, dtype=np.float64),
            matrix,
        )
