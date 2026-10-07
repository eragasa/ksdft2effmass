"""Directional contraction of one retained Löwdin quadratic tensor."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)

from .diagnostics import antihermitian_maximum_frobenius
from .reduction import WannierKineticLowdinQuadraticReductionResult3D


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticLowdinQuadraticDirectionalContractionRequest3D:
    """Declare normalized Cartesian directions for quadratic-tensor contraction.

    Parameters
    ----------
    reduction
        Identified selected-space quadratic reduction to contract.
    cartesian_directions
        Nonempty matrix of unitless normalized Cartesian row vectors.
    direction_absolute_tolerance
        Absolute tolerance applied to each Euclidean direction norm.
    """

    reduction: WannierKineticLowdinQuadraticReductionResult3D
    cartesian_directions: MatrixQuantity
    direction_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate reduction type, Cartesian directions, and norm tolerance."""
        self._check_args_reduction()
        self._check_args_directions()

    def _check_args_reduction(self) -> None:
        """Require one exact finite quadratic-reduction result."""
        if type(self.reduction) is not (WannierKineticLowdinQuadraticReductionResult3D):
            raise TypeError(
                "reduction must be WannierKineticLowdinQuadraticReductionResult3D"
            )

    def _check_args_directions(self) -> None:
        """Require nonempty normalized dimensionless Cartesian directions."""
        if type(self.cartesian_directions) is not MatrixQuantity:
            raise TypeError("cartesian_directions must be MatrixQuantity")
        if not isinstance(self.cartesian_directions.unit, Unitless):
            raise ValueError("cartesian_directions must be unitless")
        if self.cartesian_directions.magnitude.ndim != 2 or (
            self.cartesian_directions.magnitude.shape[1] != 3
        ):
            raise ValueError("cartesian_directions must have shape (count, 3)")
        if self.cartesian_directions.magnitude.shape[0] == 0:
            raise ValueError("cartesian_directions must contain at least one row")
        if type(self.direction_absolute_tolerance) is not float:
            raise TypeError("direction_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.direction_absolute_tolerance)
            or self.direction_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "direction_absolute_tolerance must be finite and nonnegative"
            )
        norms = np.linalg.norm(self.cartesian_directions.magnitude, axis=1)
        if np.any(np.abs(norms - 1.0) > self.direction_absolute_tolerance):
            raise ValueError("every Cartesian direction must have unit Euclidean norm")


@dataclass(frozen=True, slots=True)
class WannierKineticLowdinQuadraticDirectionalContractionDiagnostics3D:
    """Retain the maximum directional-matrix anti-Hermitian defect."""

    antihermitian_maximum_frobenius: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate one nonnegative quadratic-unit defect."""
        if type(self.antihermitian_maximum_frobenius) is not ScalarQuantity:
            raise TypeError("antihermitian_maximum_frobenius must be ScalarQuantity")
        if self.antihermitian_maximum_frobenius.magnitude < 0.0:
            raise ValueError("antihermitian_maximum_frobenius must be nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticLowdinQuadraticDirectionalContractionResult3D:
    """Retain one selected-space quadratic matrix for each Cartesian direction."""

    request: WannierKineticLowdinQuadraticDirectionalContractionRequest3D
    matrices: tuple[ComplexMatrixQuantity, ...]
    diagnostics: WannierKineticLowdinQuadraticDirectionalContractionDiagnostics3D

    def __post_init__(self) -> None:
        """Validate matrix types, units, shapes, values, and diagnostics."""
        self._check_args_types_and_matrices()
        # Result construction checks intrinsic matrix/diagnostic consistency only.
        # Tensor contraction of the request belongs to the contraction Action.
        self._check_args_diagnostic_correlation()

    def _check_args_types_and_matrices(self) -> None:
        """Require one homogeneous selected-space quadratic-matrix family."""
        if type(self.request) is not (
            WannierKineticLowdinQuadraticDirectionalContractionRequest3D
        ):
            raise TypeError(
                "request must be "
                "WannierKineticLowdinQuadraticDirectionalContractionRequest3D"
            )
        if type(self.diagnostics) is not (
            WannierKineticLowdinQuadraticDirectionalContractionDiagnostics3D
        ):
            raise TypeError(
                "diagnostics must be "
                "WannierKineticLowdinQuadraticDirectionalContractionDiagnostics3D"
            )
        direction_count = self.request.cartesian_directions.magnitude.shape[0]
        rank = self.request.reduction.request.selected_rank
        quadratic_unit = self.request.reduction.effective_quadratic[0][0].unit
        if type(self.matrices) is not tuple or len(self.matrices) != direction_count:
            raise ValueError("matrices must contain one value per Cartesian direction")
        for matrix in self.matrices:
            if type(matrix) is not ComplexMatrixQuantity:
                raise TypeError("matrices must contain ComplexMatrixQuantity values")
            if matrix.magnitude.shape != (rank, rank):
                raise ValueError("directional matrix has the wrong selected rank")
            if matrix.unit != quadratic_unit:
                raise ValueError("directional matrix has the wrong quadratic unit")

    def _check_args_diagnostic_correlation(self) -> None:
        """Require the anti-Hermiticity diagnostic to match retained matrices."""
        expected = ScalarQuantity(
            antihermitian_maximum_frobenius(
                np.asarray([matrix.magnitude for matrix in self.matrices])
            ),
            self.matrices[0].unit,
        )
        if self.diagnostics.antihermitian_maximum_frobenius != expected:
            raise ValueError("directional diagnostics do not match the matrices")


class WannierKineticLowdinQuadraticDirectionalContractionConstructor3D:
    """Contract a selected-space quadratic tensor along Cartesian directions."""

    __slots__ = ()

    def execute(
        self,
        request: WannierKineticLowdinQuadraticDirectionalContractionRequest3D,
    ) -> WannierKineticLowdinQuadraticDirectionalContractionResult3D:
        """Return one quadratic-unit matrix for each normalized direction."""
        if type(request) is not (
            WannierKineticLowdinQuadraticDirectionalContractionRequest3D
        ):
            raise TypeError(
                "request must be "
                "WannierKineticLowdinQuadraticDirectionalContractionRequest3D"
            )
        # The Action contracts the tensor once. The Result validates intrinsic
        # diagnostics without replaying this request-to-matrix derivation.
        directions = request.cartesian_directions.magnitude
        quadratic = np.asarray(
            [
                [matrix.magnitude for matrix in row]
                for row in request.reduction.effective_quadratic
            ]
        )
        matrices = np.asarray(
            [
                np.einsum(
                    "a,b,abij->ij",
                    direction,
                    direction,
                    quadratic,
                    optimize=True,
                )
                for direction in directions
            ]
        )
        quadratic_unit = request.reduction.effective_quadratic[0][0].unit
        if not isinstance(quadratic_unit, PhysicalUnit):
            raise ValueError("quadratic tensor must use a physical unit")
        diagnostics_type = (
            WannierKineticLowdinQuadraticDirectionalContractionDiagnostics3D
        )
        diagnostics = diagnostics_type(
            antihermitian_maximum_frobenius=ScalarQuantity(
                antihermitian_maximum_frobenius(matrices),
                quadratic_unit,
            )
        )
        return WannierKineticLowdinQuadraticDirectionalContractionResult3D(
            request=request,
            matrices=tuple(
                ComplexMatrixQuantity(matrix, quadratic_unit) for matrix in matrices
            ),
            diagnostics=diagnostics,
        )


__all__ = [
    "WannierKineticLowdinQuadraticDirectionalContractionConstructor3D",
    "WannierKineticLowdinQuadraticDirectionalContractionDiagnostics3D",
    "WannierKineticLowdinQuadraticDirectionalContractionRequest3D",
    "WannierKineticLowdinQuadraticDirectionalContractionResult3D",
]
