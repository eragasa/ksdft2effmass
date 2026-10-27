"""Finite-range consequences for the non-flat four-state realization."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from projectkoios.numerics.linalg.frobenius import complex_matrix_frobenius
from projectkoios.numerics.linalg.hermitian_spectrum import (
    BatchedHermitianSpectrumDefinition,
    BatchedHermitianSpectrumTolerance,
)
from projectkoios.numerics.linalg.numpy.hermitian_spectrum import (
    NumpyBatchedHermitianSpectrumSolver,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    BlockHoppingModel,
    BlockHoppingTerm,
)
from projectkoios.physkit.solidstate.tb.bands import (
    BlockHoppingBandEvaluation,
    BlockHoppingBandTolerance,
    BlockHoppingRangeBandEntry,
    BlockHoppingRangeBandEvaluation,
    BlockHoppingRangeBandEvaluator,
    BlockHoppingRangeBandSelection,
)
from projectkoios.physkit.solidstate.tb.diagnostics import (
    BlockHoppingHermiticityAnalyzer,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
)

from ..nonflat.experiment import ComplexArray, SmoothFourStateExperiment
from .definition import SmoothFourStateTruncationDefinition
from .results import (
    SmoothFourStateTruncationPointResult,
    SmoothFourStateTruncationRangeResult,
    SmoothFourStateTruncationResult,
)

RealArray = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class _HamiltonianErrors:
    maximum: float
    rms: float


@dataclass(frozen=True, slots=True)
class _ReferenceRangeResult:
    maximum_range: int
    ordinary_omitted_power: float
    maximum_hamiltonian_error: float
    rms_hamiltonian_error: float
    maximum_band_error: float
    rms_band_error: float


class SmoothFourStateTruncationExperiment:
    """Measure actual band consequences of explicit ordinary-lattice cutoffs.

    The cyclic Nyquist representative from the even construction mesh is not passed to
    PhysKit as an ordinary-lattice term.  Its power is retained as a separate conversion
    channel before PhysKit applies caller-selected conjugate-closed inventories.
    """

    __slots__ = ()

    def execute(
        self, definition: SmoothFourStateTruncationDefinition
    ) -> SmoothFourStateTruncationResult:
        """Evaluate all declared pointwise amplitudes and finite ranges."""
        if type(definition) is not SmoothFourStateTruncationDefinition:
            raise TypeError("definition must be SmoothFourStateTruncationDefinition")
        model = definition.model
        parent = SmoothFourStateExperiment._prepare_parent(model)
        evaluation_coordinates, offset = self._evaluation_coordinates(definition)
        separation = self._minimum_periodic_separation(
            parent.coordinates, evaluation_coordinates
        )
        if separation <= np.finfo(np.float64).eps:
            raise FloatingPointError(
                "construction and evaluation meshes are not disjoint"
            )

        ordinary_mask = np.asarray(
            [
                displacement != -(model.reciprocal_mesh_size // 2)
                for displacement in parent.displacements
            ],
            dtype=np.bool_,
        )
        ordinary_displacements = tuple(
            displacement
            for displacement, include in zip(
                parent.displacements, ordinary_mask, strict=True
            )
            if bool(include)
        )
        reference_blocks = parent.reference_blocks[ordinary_mask]
        reference_model = self._model(
            "reference-ordinary-full",
            ordinary_displacements,
            reference_blocks,
        )
        reference_hermiticity = self._maximum_hermiticity_defect(
            reference_model, model.frame_absolute_tolerance
        )
        reference_family = self._evaluate_range_family(
            reference_model,
            definition.maximum_ranges,
            evaluation_coordinates,
            model.frame_absolute_tolerance,
            "reference",
        )
        reference_full, reference_eigenvalues = self._band_arrays(
            reference_family.source_band_evaluation
        )
        reference_nyquist_power = self._nyquist_power(
            parent.reference_blocks[~ordinary_mask]
        )
        reference_ranges = tuple(
            self._reference_range(
                maximum_range,
                entry,
                reference_full,
                reference_eigenvalues,
            )
            for maximum_range, entry in zip(
                definition.maximum_ranges,
                reference_family.entries,
                strict=True,
            )
        )

        points = tuple(
            self._point(
                definition,
                parent.coordinates,
                parent.retained_matrices,
                parent.displacements,
                ordinary_mask,
                reference_full,
                reference_eigenvalues,
                reference_ranges,
                reference_nyquist_power,
                reference_hermiticity,
                evaluation_coordinates,
                amplitude,
            )
            for amplitude in model.amplitudes
        )
        return SmoothFourStateTruncationResult(
            definition=definition,
            minimum_external_gap=parent.minimum_external_gap,
            minimum_transport_singular_value=parent.minimum_transport_singular_value,
            maximum_transport_procrustes_residual=(
                parent.maximum_transport_procrustes_residual
            ),
            maximum_transport_unitarity_defect=(
                parent.maximum_transport_unitarity_defect
            ),
            maximum_transport_rank_cutoff=parent.maximum_transport_rank_cutoff,
            closure_holonomy_phases=parent.closure_holonomy_phases,
            closure_holonomy_unitarity_defect=(
                parent.closure_holonomy_unitarity_defect
            ),
            maximum_frame_orthonormality_defect=(
                parent.maximum_frame_orthonormality_defect
            ),
            periodic_closure_defect=parent.periodic_closure_defect,
            maximum_reference_hermiticity_defect=(
                parent.maximum_reference_hermiticity_defect
            ),
            evaluation_coordinate_offset=offset,
            minimum_construction_evaluation_separation=separation,
            points=points,
        )

    @classmethod
    def _point(
        cls,
        definition: SmoothFourStateTruncationDefinition,
        construction_coordinates: RealArray,
        construction_reference: ComplexArray,
        cyclic_displacements: tuple[int, ...],
        ordinary_mask: npt.NDArray[np.bool_],
        reference_full: ComplexArray,
        reference_eigenvalues: RealArray,
        reference_ranges: tuple[_ReferenceRangeResult, ...],
        reference_nyquist_power: float,
        reference_hermiticity: float,
        evaluation_coordinates: RealArray,
        amplitude: float,
    ) -> SmoothFourStateTruncationPointResult:
        model = definition.model
        construction_comparison = SmoothFourStateExperiment._comparison_matrices(
            construction_coordinates,
            construction_reference,
            amplitude,
        )
        cyclic_comparison_blocks = SmoothFourStateExperiment._fourier_blocks(
            construction_coordinates,
            construction_comparison,
            cyclic_displacements,
        )
        comparison_nyquist_power = cls._nyquist_power(
            cyclic_comparison_blocks[~ordinary_mask]
        )
        ordinary_displacements = tuple(
            displacement
            for displacement, include in zip(
                cyclic_displacements, ordinary_mask, strict=True
            )
            if bool(include)
        )
        comparison_model = cls._model(
            f"comparison-ordinary-full-{amplitude.hex()}",
            ordinary_displacements,
            cyclic_comparison_blocks[ordinary_mask],
        )
        comparison_hermiticity = cls._maximum_hermiticity_defect(
            comparison_model, model.frame_absolute_tolerance
        )
        comparison_family = cls._evaluate_range_family(
            comparison_model,
            definition.maximum_ranges,
            evaluation_coordinates,
            model.frame_absolute_tolerance,
            f"comparison-{amplitude.hex()}",
        )
        comparison_full, comparison_full_eigenvalues = cls._band_arrays(
            comparison_family.source_band_evaluation
        )
        direct_comparison = SmoothFourStateExperiment._comparison_matrices(
            evaluation_coordinates,
            reference_full,
            amplitude,
        )
        direct_eigenvalues = cls._owner_eigenvalues(
            direct_comparison, model.frame_absolute_tolerance
        )
        direct_difference = direct_eigenvalues - reference_eigenvalues
        interpolation_difference = comparison_full_eigenvalues - direct_eigenvalues
        interpolation_hamiltonian_errors = cls._hamiltonian_errors(
            comparison_full - direct_comparison,
            interpolation_difference,
        )

        ranges = tuple(
            cls._range(
                maximum_range,
                reference_range,
                comparison_entry,
                comparison_full,
                comparison_full_eigenvalues,
                direct_comparison,
                direct_eigenvalues,
                reference_nyquist_power,
                comparison_nyquist_power,
            )
            for maximum_range, reference_range, comparison_entry in zip(
                definition.maximum_ranges,
                reference_ranges,
                comparison_family.entries,
                strict=True,
            )
        )
        return SmoothFourStateTruncationPointResult(
            amplitude=amplitude,
            reference_nyquist_power=reference_nyquist_power,
            comparison_nyquist_power=comparison_nyquist_power,
            reference_maximum_ordinary_hermiticity_defect=reference_hermiticity,
            comparison_maximum_ordinary_hermiticity_defect=comparison_hermiticity,
            maximum_direct_band_defect=float(np.max(np.abs(direct_difference))),
            comparison_maximum_interpolation_hamiltonian_error=(
                interpolation_hamiltonian_errors.maximum
            ),
            comparison_rms_interpolation_hamiltonian_error=(
                interpolation_hamiltonian_errors.rms
            ),
            comparison_maximum_interpolation_band_error=float(
                np.max(np.abs(interpolation_difference))
            ),
            comparison_rms_interpolation_band_error=cls._rms(interpolation_difference),
            ranges=ranges,
        )

    @classmethod
    def _reference_range(
        cls,
        maximum_range: int,
        entry: BlockHoppingRangeBandEntry,
        reference_full: ComplexArray,
        reference_eigenvalues: RealArray,
    ) -> _ReferenceRangeResult:
        matrices, eigenvalues = cls._band_arrays(entry.band_evaluation)
        matrix_difference = matrices - reference_full
        if not bool(np.isfinite(matrix_difference).all()):
            raise FloatingPointError("reference truncation difference became nonfinite")
        difference = eigenvalues - reference_eigenvalues
        hamiltonian_errors = cls._hamiltonian_errors(matrix_difference, difference)
        return _ReferenceRangeResult(
            maximum_range=maximum_range,
            ordinary_omitted_power=entry.truncation.omitted_power.magnitude / 2.0,
            maximum_hamiltonian_error=hamiltonian_errors.maximum,
            rms_hamiltonian_error=hamiltonian_errors.rms,
            maximum_band_error=float(np.max(np.abs(difference))),
            rms_band_error=cls._rms(difference),
        )

    @classmethod
    def _range(
        cls,
        maximum_range: int,
        reference_range: _ReferenceRangeResult,
        comparison_entry: BlockHoppingRangeBandEntry,
        comparison_full: ComplexArray,
        comparison_full_eigenvalues: RealArray,
        direct_comparison: ComplexArray,
        direct_eigenvalues: RealArray,
        reference_nyquist_power: float,
        comparison_nyquist_power: float,
    ) -> SmoothFourStateTruncationRangeResult:
        if reference_range.maximum_range != maximum_range:
            raise AssertionError("reference cutoff must match the comparison cutoff")
        comparison_truncated, comparison_truncated_eigenvalues = cls._band_arrays(
            comparison_entry.band_evaluation
        )
        # Matrix differences are formed before eigenvalue errors so nonfinite
        # arithmetic cannot be hidden by a Hermitian eigensolver.
        comparison_truncation_matrix_difference = comparison_truncated - comparison_full
        comparison_total_matrix_difference = comparison_truncated - direct_comparison
        comparison_truncation_difference = (
            comparison_truncated_eigenvalues - comparison_full_eigenvalues
        )
        comparison_total_difference = (
            comparison_truncated_eigenvalues - direct_eigenvalues
        )
        comparison_truncation_hamiltonian_errors = cls._hamiltonian_errors(
            comparison_truncation_matrix_difference,
            comparison_truncation_difference,
        )
        comparison_total_hamiltonian_errors = cls._hamiltonian_errors(
            comparison_total_matrix_difference,
            comparison_total_difference,
        )
        reference_ordinary_power = reference_range.ordinary_omitted_power
        comparison_ordinary_power = (
            comparison_entry.truncation.omitted_power.magnitude / 2.0
        )
        return SmoothFourStateTruncationRangeResult(
            maximum_range=maximum_range,
            reference_ordinary_omitted_power=reference_ordinary_power,
            comparison_ordinary_omitted_power=comparison_ordinary_power,
            reference_total_omitted_power=(
                reference_ordinary_power + reference_nyquist_power
            ),
            comparison_total_omitted_power=(
                comparison_ordinary_power + comparison_nyquist_power
            ),
            reference_maximum_truncation_hamiltonian_error=(
                reference_range.maximum_hamiltonian_error
            ),
            reference_rms_truncation_hamiltonian_error=(
                reference_range.rms_hamiltonian_error
            ),
            reference_maximum_band_error=reference_range.maximum_band_error,
            reference_rms_band_error=reference_range.rms_band_error,
            comparison_maximum_truncation_hamiltonian_error=(
                comparison_truncation_hamiltonian_errors.maximum
            ),
            comparison_rms_truncation_hamiltonian_error=(
                comparison_truncation_hamiltonian_errors.rms
            ),
            comparison_maximum_truncation_band_error=float(
                np.max(np.abs(comparison_truncation_difference))
            ),
            comparison_rms_truncation_band_error=cls._rms(
                comparison_truncation_difference
            ),
            comparison_maximum_total_hamiltonian_error=(
                comparison_total_hamiltonian_errors.maximum
            ),
            comparison_rms_total_hamiltonian_error=(
                comparison_total_hamiltonian_errors.rms
            ),
            comparison_maximum_total_band_error=float(
                np.max(np.abs(comparison_total_difference))
            ),
            comparison_rms_total_band_error=cls._rms(comparison_total_difference),
        )

    @staticmethod
    def _evaluation_coordinates(
        definition: SmoothFourStateTruncationDefinition,
    ) -> tuple[RealArray, float]:
        construction_size = definition.model.reciprocal_mesh_size
        evaluation_size = definition.evaluation_mesh_size
        offset = 1.0 / float(construction_size + 1)
        coordinates = -0.5 + (
            np.arange(evaluation_size, dtype=np.float64) + offset
        ) / float(evaluation_size)
        coordinates.setflags(write=False)
        return coordinates, offset

    @staticmethod
    def _minimum_periodic_separation(
        construction: RealArray, evaluation: RealArray
    ) -> float:
        differences = np.abs(evaluation[:, None] - construction[None, :])
        wrapped = np.minimum(differences, 1.0 - differences)
        return float(np.min(wrapped))

    @staticmethod
    def _model(
        identifier: str,
        displacements: tuple[int, ...],
        blocks: ComplexArray,
    ) -> BlockHoppingModel:
        return BlockHoppingModel(
            identifier=identifier,
            dimension=LatticeDimension.ONE,
            terms=tuple(
                BlockHoppingTerm(
                    displacement=LatticeDisplacement(
                        LatticeDimension.ONE, (displacement,)
                    ),
                    coefficient=ComplexMatrixQuantity(block, Unitless()),
                )
                for displacement, block in zip(displacements, blocks, strict=True)
            ),
            energy_unit=Unitless(),
            energy_reference="declared-parent-energy-zero",
            basis_identifier="transported-retained-rank-two-frame",
        )

    @staticmethod
    def _maximum_hermiticity_defect(
        model: BlockHoppingModel, tolerance: float
    ) -> float:
        result = BlockHoppingHermiticityAnalyzer().execute(model)
        if result.missing_targets:
            raise ValueError("ordinary hopping inventory is not conjugate closed")
        maximum = result.maximum_frobenius_defect
        if maximum is None:
            raise ValueError(
                "ordinary hopping inventory has no Hermiticity comparisons"
            )
        defect = maximum.magnitude
        if defect > tolerance:
            raise FloatingPointError(
                "ordinary hopping model fails Hermiticity tolerance"
            )
        return defect

    @staticmethod
    def _evaluate_range_family(
        model: BlockHoppingModel,
        maximum_ranges: tuple[int, ...],
        coordinates: RealArray,
        hermiticity_tolerance: float,
        identifier_prefix: str,
    ) -> BlockHoppingRangeBandEvaluation:
        selections = tuple(
            BlockHoppingRangeBandSelection(
                retained_displacements=tuple(
                    LatticeDisplacement(LatticeDimension.ONE, (displacement,))
                    for displacement in range(-maximum_range, maximum_range + 1)
                ),
                truncated_identifier=f"{identifier_prefix}-range-{maximum_range}",
            )
            for maximum_range in maximum_ranges
        )
        return BlockHoppingRangeBandEvaluator().evaluate(
            model,
            selections,
            MatrixQuantity(coordinates[:, None], Unitless()),
            BlockHoppingBandTolerance(
                hermiticity_absolute=ScalarQuantity(
                    hermiticity_tolerance,
                    Unitless(),
                ),
                hermiticity_relative=0.0,
            ),
        )

    @staticmethod
    def _band_arrays(
        evaluation: BlockHoppingBandEvaluation,
    ) -> tuple[ComplexArray, RealArray]:
        matrices = np.stack(
            tuple(
                matrix.magnitude
                for matrix in evaluation.bloch_evaluation.bloch_matrices
            ),
            axis=0,
        ).astype(np.complex128, copy=False)
        eigenvalues = np.asarray(
            evaluation.band_energies.magnitude,
            dtype=np.float64,
        )
        return matrices, eigenvalues

    @staticmethod
    def _owner_eigenvalues(matrices: ComplexArray, tolerance: float) -> RealArray:
        owner_tolerance = BatchedHermitianSpectrumTolerance(
            hermiticity_absolute=tolerance,
            hermiticity_relative=0.0,
        )
        if matrices.shape[0] == 0:
            definition = BatchedHermitianSpectrumDefinition.empty(
                matrices.shape[1],
                owner_tolerance,
            )
        else:
            definition = BatchedHermitianSpectrumDefinition(
                tuple(
                    tuple(tuple(complex(entry) for entry in row) for row in matrix)
                    for matrix in matrices
                ),
                owner_tolerance,
            )
        result = NumpyBatchedHermitianSpectrumSolver().solve(definition)
        return np.asarray(result.eigenvalues, dtype=np.float64).reshape(
            result.batch_size,
            result.dimension,
        )

    @staticmethod
    def _hamiltonian_errors(
        matrix_differences: ComplexArray,
        eigenvalue_differences: RealArray,
    ) -> _HamiltonianErrors:
        """Return rank-normalized Frobenius errors and verify spectral bounds."""
        if matrix_differences.ndim != 3 or matrix_differences.shape[1:] != (2, 2):
            raise ValueError("matrix differences must have shape (point, 2, 2)")
        if eigenvalue_differences.shape != (matrix_differences.shape[0], 2):
            raise ValueError("eigenvalue differences must have shape (point, 2)")
        if matrix_differences.shape[0] == 0:
            raise ValueError("Hamiltonian error evaluation requires at least one point")

        powers: list[float] = []
        norms: list[float] = []
        for matrix, eigenvalues in zip(
            matrix_differences, eigenvalue_differences, strict=True
        ):
            value = complex_matrix_frobenius(
                tuple(tuple(complex(entry) for entry in row) for row in matrix)
            )
            spectral_maximum = float(np.max(np.abs(eigenvalues)))
            bound_tolerance = (
                32.0 * np.finfo(np.float64).eps * max(1.0, value.norm, spectral_maximum)
            )
            if spectral_maximum > value.norm + bound_tolerance:
                raise FloatingPointError(
                    "spectral error exceeds its Frobenius perturbation bound"
                )
            powers.append(value.power)
            norms.append(value.norm)

        rank = 2.0
        return _HamiltonianErrors(
            maximum=max(norms) / math.sqrt(rank),
            rms=math.sqrt(math.fsum(powers) / (rank * len(powers))),
        )

    @staticmethod
    def _nyquist_power(blocks: ComplexArray) -> float:
        if blocks.shape[0] != 1:
            raise ValueError("exactly one cyclic Nyquist block is required")
        return float(np.sum(np.abs(blocks[0]) ** 2) / 2.0)

    @staticmethod
    def _rms(values: RealArray) -> float:
        return math.sqrt(float(np.mean(np.square(values))))
