"""Finite-range consequences for the non-flat four-state realization."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
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
    BlockHoppingBandEvaluator,
    BlockHoppingBandTolerance,
)
from projectkoios.physkit.solidstate.tb.diagnostics import (
    BlockHoppingHermiticityAnalyzer,
)
from projectkoios.physkit.solidstate.tb.truncation import (
    ConjugateClosedBlockHoppingTruncator,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
)

from .nonflat_experiment import ComplexArray, SmoothFourStateExperiment
from .truncation_definition import SmoothFourStateTruncationDefinition
from .truncation_results import (
    SmoothFourStateTruncationPointResult,
    SmoothFourStateTruncationRangeResult,
    SmoothFourStateTruncationResult,
)

RealArray = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class _ReferenceRangeResult:
    maximum_range: int
    ordinary_omitted_power: float
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
        reference_full, reference_eigenvalues = self._evaluate_bands(
            reference_model,
            evaluation_coordinates,
            model.frame_absolute_tolerance,
        )
        reference_nyquist_power = self._nyquist_power(
            parent.reference_blocks[~ordinary_mask]
        )
        reference_ranges = tuple(
            self._reference_range(
                maximum_range,
                reference_model,
                reference_full,
                reference_eigenvalues,
                evaluation_coordinates,
                model.frame_absolute_tolerance,
            )
            for maximum_range in definition.maximum_ranges
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
        comparison_full, comparison_full_eigenvalues = cls._evaluate_bands(
            comparison_model,
            evaluation_coordinates,
            model.frame_absolute_tolerance,
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

        ranges = tuple(
            cls._range(
                maximum_range,
                reference_range,
                comparison_model,
                comparison_full,
                comparison_full_eigenvalues,
                direct_eigenvalues,
                reference_nyquist_power,
                comparison_nyquist_power,
                evaluation_coordinates,
                model.frame_absolute_tolerance,
                amplitude,
            )
            for maximum_range, reference_range in zip(
                definition.maximum_ranges, reference_ranges, strict=True
            )
        )
        return SmoothFourStateTruncationPointResult(
            amplitude=amplitude,
            reference_nyquist_power=reference_nyquist_power,
            comparison_nyquist_power=comparison_nyquist_power,
            reference_maximum_ordinary_hermiticity_defect=reference_hermiticity,
            comparison_maximum_ordinary_hermiticity_defect=comparison_hermiticity,
            maximum_direct_band_defect=float(np.max(np.abs(direct_difference))),
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
        reference_model: BlockHoppingModel,
        reference_full: ComplexArray,
        reference_eigenvalues: RealArray,
        evaluation_coordinates: RealArray,
        hermiticity_tolerance: float,
    ) -> _ReferenceRangeResult:
        retained = tuple(
            LatticeDisplacement(LatticeDimension.ONE, (displacement,))
            for displacement in range(-maximum_range, maximum_range + 1)
        )
        truncated = ConjugateClosedBlockHoppingTruncator().execute(
            reference_model,
            retained,
            f"reference-range-{maximum_range}",
        )
        matrices, eigenvalues = cls._evaluate_bands(
            truncated.truncated,
            evaluation_coordinates,
            hermiticity_tolerance,
        )
        if not bool(np.isfinite(matrices - reference_full).all()):
            raise FloatingPointError("reference truncation difference became nonfinite")
        difference = eigenvalues - reference_eigenvalues
        return _ReferenceRangeResult(
            maximum_range=maximum_range,
            ordinary_omitted_power=truncated.omitted_power.magnitude / 2.0,
            maximum_band_error=float(np.max(np.abs(difference))),
            rms_band_error=cls._rms(difference),
        )

    @classmethod
    def _range(
        cls,
        maximum_range: int,
        reference_range: _ReferenceRangeResult,
        comparison_model: BlockHoppingModel,
        comparison_full: ComplexArray,
        comparison_full_eigenvalues: RealArray,
        direct_eigenvalues: RealArray,
        reference_nyquist_power: float,
        comparison_nyquist_power: float,
        evaluation_coordinates: RealArray,
        hermiticity_tolerance: float,
        amplitude: float,
    ) -> SmoothFourStateTruncationRangeResult:
        retained = tuple(
            LatticeDisplacement(LatticeDimension.ONE, (displacement,))
            for displacement in range(-maximum_range, maximum_range + 1)
        )
        truncator = ConjugateClosedBlockHoppingTruncator()
        if reference_range.maximum_range != maximum_range:
            raise AssertionError("reference cutoff must match the comparison cutoff")
        comparison = truncator.execute(
            comparison_model,
            retained,
            f"comparison-{amplitude.hex()}-range-{maximum_range}",
        )
        comparison_truncated, comparison_truncated_eigenvalues = cls._evaluate_bands(
            comparison.truncated,
            evaluation_coordinates,
            hermiticity_tolerance,
        )
        # The matrix differences are intentionally formed before eigenvalue errors so
        # nonfinite arithmetic cannot be hidden by a Hermitian eigensolver.
        if not bool(np.isfinite(comparison_truncated - comparison_full).all()):
            raise FloatingPointError(
                "comparison truncation difference became nonfinite"
            )
        comparison_truncation_difference = (
            comparison_truncated_eigenvalues - comparison_full_eigenvalues
        )
        comparison_total_difference = (
            comparison_truncated_eigenvalues - direct_eigenvalues
        )
        reference_ordinary_power = reference_range.ordinary_omitted_power
        comparison_ordinary_power = comparison.omitted_power.magnitude / 2.0
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
            reference_maximum_band_error=reference_range.maximum_band_error,
            reference_rms_band_error=reference_range.rms_band_error,
            comparison_maximum_truncation_band_error=float(
                np.max(np.abs(comparison_truncation_difference))
            ),
            comparison_rms_truncation_band_error=cls._rms(
                comparison_truncation_difference
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
    def _evaluate_bands(
        model: BlockHoppingModel,
        coordinates: RealArray,
        hermiticity_tolerance: float,
    ) -> tuple[ComplexArray, RealArray]:
        evaluation = BlockHoppingBandEvaluator().evaluate(
            model,
            MatrixQuantity(coordinates[:, None], Unitless()),
            BlockHoppingBandTolerance(
                hermiticity_absolute=ScalarQuantity(
                    hermiticity_tolerance,
                    Unitless(),
                ),
                hermiticity_relative=0.0,
            ),
        )
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
    def _nyquist_power(blocks: ComplexArray) -> float:
        if blocks.shape[0] != 1:
            raise ValueError("exactly one cyclic Nyquist block is required")
        return float(np.sum(np.abs(blocks[0]) ** 2) / 2.0)

    @staticmethod
    def _rms(values: RealArray) -> float:
        return math.sqrt(float(np.mean(np.square(values))))
