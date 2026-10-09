"""Evaluation of one retained Löwdin quadratic effective Hamiltonian."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
)

from .diagnostics import antihermitian_maximum_frobenius
from .reduction import WannierKineticLowdinQuadraticReductionResult3D


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticLowdinQuadraticModelEvaluationRequest3D:
    """Declare Cartesian offsets for one retained quadratic model evaluation.

    Parameters
    ----------
    reduction
        Identified selected-space quadratic reduction to evaluate.
    cartesian_offsets
        Matrix of Cartesian reciprocal-space row vectors. Its unit must be
        dimensionally compatible with the inverse direct-lattice unit.
    """

    reduction: WannierKineticLowdinQuadraticReductionResult3D
    cartesian_offsets: MatrixQuantity

    def __post_init__(self) -> None:
        """Validate the reduction and Cartesian reciprocal-coordinate contract."""
        self._check_args_reduction()
        self._check_args_offsets()

    def _check_args_reduction(self) -> None:
        """Require one exact finite quadratic-reduction result."""
        if type(self.reduction) is not (WannierKineticLowdinQuadraticReductionResult3D):
            raise TypeError(
                "reduction must be WannierKineticLowdinQuadraticReductionResult3D"
            )

    def _check_args_offsets(self) -> None:
        """Require a nonempty matrix of compatible Cartesian reciprocal vectors."""
        if type(self.cartesian_offsets) is not MatrixQuantity:
            raise TypeError("cartesian_offsets must be MatrixQuantity")
        if self.cartesian_offsets.magnitude.ndim != 2 or (
            self.cartesian_offsets.magnitude.shape[1] != 3
        ):
            raise ValueError("cartesian_offsets must have shape (sample_count, 3)")
        if self.cartesian_offsets.magnitude.shape[0] == 0:
            raise ValueError("cartesian_offsets must contain at least one sample")
        if not isinstance(self.cartesian_offsets.unit, PhysicalUnit):
            raise ValueError("cartesian_offsets must have a physical reciprocal unit")
        target = self.target_offset_unit
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.cartesian_offsets.unit, target
        ):
            raise ValueError(
                "cartesian_offsets unit must be inverse to the direct-lattice unit"
            )

    @property
    def target_offset_unit(self) -> PhysicalUnit:
        """Return the reciprocal unit paired with the derivative lattice unit."""
        inventory = self.reduction.request.hamiltonian_derivatives.request.inventory
        lattice_unit = inventory.direct_lattice.unit
        if not isinstance(lattice_unit, PhysicalUnit):
            raise ValueError("derivative inventory must use a physical lattice unit")
        return PhysicalUnit(f"1 / ({lattice_unit.expression})")


@dataclass(frozen=True, slots=True)
class WannierKineticLowdinQuadraticModelEvaluationDiagnostics3D:
    """Retain the maximum evaluated-matrix anti-Hermitian defect."""

    antihermitian_maximum_frobenius: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate one nonnegative energy-valued defect."""
        if type(self.antihermitian_maximum_frobenius) is not ScalarQuantity:
            raise TypeError("antihermitian_maximum_frobenius must be ScalarQuantity")
        if self.antihermitian_maximum_frobenius.magnitude < 0.0:
            raise ValueError("antihermitian_maximum_frobenius must be nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticLowdinQuadraticModelEvaluationResult3D:
    """Retain selected-space effective matrices at explicit Cartesian offsets."""

    request: WannierKineticLowdinQuadraticModelEvaluationRequest3D
    matrices: tuple[ComplexMatrixQuantity, ...]
    diagnostics: WannierKineticLowdinQuadraticModelEvaluationDiagnostics3D

    def __post_init__(self) -> None:
        """Validate matrix types, units, shapes, values, and diagnostics."""
        self._check_args_types_and_matrices()
        # Result construction checks intrinsic matrix/diagnostic consistency only.
        # Taylor evaluation of the request belongs to the model-evaluation Action.
        self._check_args_diagnostic_correlation()

    def _check_args_types_and_matrices(self) -> None:
        """Require one homogeneous selected-space energy-matrix family."""
        if type(self.request) is not (
            WannierKineticLowdinQuadraticModelEvaluationRequest3D
        ):
            raise TypeError(
                "request must be WannierKineticLowdinQuadraticModelEvaluationRequest3D"
            )
        if type(self.diagnostics) is not (
            WannierKineticLowdinQuadraticModelEvaluationDiagnostics3D
        ):
            raise TypeError(
                "diagnostics must be "
                "WannierKineticLowdinQuadraticModelEvaluationDiagnostics3D"
            )
        sample_count = self.request.cartesian_offsets.magnitude.shape[0]
        rank = self.request.reduction.request.selected_rank
        energy_unit = self.request.reduction.projected_hamiltonian_value.unit
        if type(self.matrices) is not tuple or len(self.matrices) != sample_count:
            raise ValueError("matrices must contain one value per Cartesian offset")
        for matrix in self.matrices:
            if type(matrix) is not ComplexMatrixQuantity:
                raise TypeError("matrices must contain ComplexMatrixQuantity values")
            if matrix.magnitude.shape != (rank, rank):
                raise ValueError("evaluated matrix has the wrong selected rank")
            if matrix.unit != energy_unit:
                raise ValueError("evaluated matrix has the wrong energy unit")

    def _check_args_diagnostic_correlation(self) -> None:
        """Require the anti-Hermiticity diagnostic to match retained matrices."""
        expected = ScalarQuantity(
            antihermitian_maximum_frobenius(
                np.asarray([matrix.magnitude for matrix in self.matrices])
            ),
            self.matrices[0].unit,
        )
        if self.diagnostics.antihermitian_maximum_frobenius != expected:
            raise ValueError("evaluation diagnostics do not match the matrices")


class WannierKineticLowdinQuadraticModelEvaluator3D:
    """Evaluate a retained Löwdin quadratic Hamiltonian at Cartesian offsets."""

    __slots__ = ()

    def execute(
        self, request: WannierKineticLowdinQuadraticModelEvaluationRequest3D
    ) -> WannierKineticLowdinQuadraticModelEvaluationResult3D:
        """Return one selected-space energy matrix for every requested offset."""
        if type(request) is not (WannierKineticLowdinQuadraticModelEvaluationRequest3D):
            raise TypeError(
                "request must be WannierKineticLowdinQuadraticModelEvaluationRequest3D"
            )
        # The Action evaluates the finite Taylor polynomial once. The Result checks
        # only intrinsic matrix diagnostics and does not replay this derivation.
        offsets = MODEL_SYSTEM_UNIT_CONVERTER.convert_matrix(
            request.cartesian_offsets, request.target_offset_unit
        ).magnitude
        reduction = request.reduction
        base = reduction.projected_hamiltonian_value.magnitude
        gradient = np.asarray(
            [matrix.magnitude for matrix in reduction.projected_hamiltonian_gradient]
        )
        quadratic = np.asarray(
            [
                [matrix.magnitude for matrix in row]
                for row in reduction.effective_quadratic
            ]
        )
        matrices = np.asarray(
            [
                base
                + np.einsum("a,aij->ij", offset, gradient, optimize=True)
                + 0.5
                * np.einsum("a,b,abij->ij", offset, offset, quadratic, optimize=True)
                for offset in offsets
            ]
        )
        energy_unit = reduction.projected_hamiltonian_value.unit
        if not isinstance(energy_unit, PhysicalUnit):
            raise ValueError("quadratic model must use a physical energy unit")
        diagnostics = WannierKineticLowdinQuadraticModelEvaluationDiagnostics3D(
            antihermitian_maximum_frobenius=ScalarQuantity(
                antihermitian_maximum_frobenius(matrices),
                energy_unit,
            )
        )
        return WannierKineticLowdinQuadraticModelEvaluationResult3D(
            request=request,
            matrices=tuple(
                ComplexMatrixQuantity(matrix, energy_unit) for matrix in matrices
            ),
            diagnostics=diagnostics,
        )


__all__ = [
    "WannierKineticLowdinQuadraticModelEvaluationDiagnostics3D",
    "WannierKineticLowdinQuadraticModelEvaluationRequest3D",
    "WannierKineticLowdinQuadraticModelEvaluationResult3D",
    "WannierKineticLowdinQuadraticModelEvaluator3D",
]
