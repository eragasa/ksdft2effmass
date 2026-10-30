"""Request-bound Fourier and locality analysis for one alignment channel."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayValidator
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesResult,
)
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierTensorEvaluator,
    FinitePeriodicMatrixFourierTransformer,
    FinitePeriodicMatrixHermiticityAnalyzer,
    FinitePeriodicMatrixParsevalAnalyzer,
    FinitePeriodicMatrixSamples,
)
from projectkoios.physkit.units import Unitless

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    FourierMatrixBlockNormInventoryAnalyzer1D,
    MatrixErrorDecompositionAnalyzer,
    MatrixFieldComparisonAnalyzer,
    MatrixFieldErrorAnalyzer,
    MatrixFieldIsometryAnalyzer,
    SymmetricRangeTailAnalyzer1D,
    SymmetricRangeTailMonotonicityAnalyzer1D,
)

from .calculation import Periodic1DHigherRankAlignmentCalculationRequest
from .channel_results import (
    _ODD_CENTERED_NO_NYQUIST_DISPOSITION,
    Periodic1DHigherRankChannelMeshResult,
    Periodic1DHigherRankSupportResult,
)
from .definition import (
    Periodic1DHigherRankAlignmentChannel,
    Periodic1DHigherRankAlignmentStatus,
)
from .diagnostics import (
    Periodic1DHigherRankFrameErrorResult,
    Periodic1DHigherRankMatrixComparisonResult,
    Periodic1DHigherRankMatrixErrorResult,
    Periodic1DHigherRankProcrustesDiagnostics,
)
from .model import Periodic1DHigherRankAnalyticCase
from .result import Periodic1DHigherRankAlignmentStatusResult


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankChannelAnalysisRequest:
    """Bind one qualified channel and all of its immutable scientific inputs."""

    calculation_request: Periodic1DHigherRankAlignmentCalculationRequest
    model: Periodic1DHigherRankAnalyticCase
    mesh: CenteredUniformMesh
    coordinates: RealArray
    status: Periodic1DHigherRankAlignmentStatusResult
    aligned_samples: ComplexArray
    aligned_frames: ComplexArray
    global_selection: Periodic1DHigherRankProcrustesDiagnostics
    pointwise_alignment: NumpyBatchedComplexUnitaryProcrustesResult | None = None

    def __post_init__(self) -> None:
        if (
            type(self.calculation_request)
            is not Periodic1DHigherRankAlignmentCalculationRequest
        ):
            raise TypeError("calculation_request must be the exact request record")
        if type(self.model) is not Periodic1DHigherRankAnalyticCase:
            raise TypeError("model must be Periodic1DHigherRankAnalyticCase")
        if type(self.mesh) is not CenteredUniformMesh:
            raise TypeError("mesh must be CenteredUniformMesh")
        if type(self.status) is not Periodic1DHigherRankAlignmentStatusResult:
            raise TypeError("status must be the exact alignment status record")
        if type(self.global_selection) is not Periodic1DHigherRankProcrustesDiagnostics:
            raise TypeError("global_selection must be the exact Procrustes record")
        request = self.calculation_request
        rank = self.model.retained_rank
        if (
            rank != request.retained_rank
            or self.model.circuit_depth != request.circuit_depth
        ):
            raise ValueError("model rank and depth must match the calculation request")
        coordinates = NumpyImmutableArrayValidator(
            self.coordinates,
            "coordinates",
            np.dtype(np.float64),
        ).execute()
        samples = NumpyImmutableArrayValidator(
            self.aligned_samples,
            "aligned_samples",
            np.dtype(np.complex128),
        ).execute()
        frames = NumpyImmutableArrayValidator(
            self.aligned_frames,
            "aligned_frames",
            np.dtype(np.complex128),
        ).execute()
        if coordinates.ndim != 1:
            raise ValueError("coordinates must be a one-dimensional array")
        if samples.ndim != 3:
            raise ValueError("aligned_samples must be a three-dimensional array")
        if frames.ndim != 3:
            raise ValueError("aligned_frames must be a three-dimensional array")
        if self.mesh.dimension != 1 or self.mesh.offsets != (0.0,):
            raise ValueError("channel analysis requires the unshifted periodic-1D mesh")
        expected_coordinates = np.asarray(
            -0.5 + np.arange(self.mesh.size, dtype=np.float64) / self.mesh.size,
            dtype=np.float64,
        )
        if not np.array_equal(coordinates, expected_coordinates):
            raise ValueError("coordinates must equal the declared construction mesh")
        if samples.shape != (self.mesh.size, rank, rank):
            raise ValueError("aligned_samples must have shape (M, r, r)")
        if frames.shape != (
            self.mesh.size,
            self.model.ambient_dimension,
            rank,
        ):
            raise ValueError("aligned_frames must have shape (M, 2r, r)")
        if (
            self.status.case_identity != request.case_identity
            or self.status.retained_rank != request.retained_rank
            or self.status.circuit_depth != request.circuit_depth
            or self.status.construction_mesh_size != self.mesh.size
        ):
            raise ValueError("status must match the calculation case and mesh")
        if self.status.status is not Periodic1DHigherRankAlignmentStatus.QUALIFIED:
            raise ValueError("channel analysis requires a qualified status")
        if self.status.channel not in request.configuration.alignment_channels:
            raise ValueError("status channel must belong to the calculation request")
        channel = self.status.channel
        attacked = self.model.attacked_reduced_hamiltonians(coordinates)
        attacked_frames = self.model.attacked_frames(coordinates)
        if channel is Periodic1DHigherRankAlignmentChannel.IDENTITY:
            right_action = np.broadcast_to(
                np.eye(rank, dtype=np.complex128),
                (self.mesh.size, rank, rank),
            )
        elif channel is Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY:
            selected = self.global_selection.selected_global_right_unitary
            if selected is None:
                raise ValueError("qualified global channel requires a selected unitary")
            right_action = np.broadcast_to(
                selected.magnitude,
                (self.mesh.size, rank, rank),
            )
        elif channel is Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY:
            if (
                type(self.pointwise_alignment)
                is not NumpyBatchedComplexUnitaryProcrustesResult
            ):
                raise TypeError(
                    "qualified pointwise channel requires the exact solver result"
                )
            if (
                self.pointwise_alignment.row_count != self.model.ambient_dimension
                or not bool(self.pointwise_alignment.full_rank.all())
            ):
                raise ValueError(
                    "pointwise solver result must be full rank in the ambient space"
                )
            right_action = self.pointwise_alignment.right_unitary_completions
        else:
            gauge = self.model.gauge_unitaries(coordinates)
            right_action = np.swapaxes(gauge.conjugate(), -1, -2)
        if right_action.shape != (self.mesh.size, rank, rank):
            raise ValueError("channel right action must match the case and mesh")
        if (
            channel is not Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY
            and self.pointwise_alignment is not None
        ):
            raise ValueError(
                "pointwise_alignment is reserved for the pointwise channel"
            )
        right_isometry = MatrixFieldIsometryAnalyzer().execute(right_action)
        if (
            right_isometry.normalized_maximum_frobenius_defect
            > request.controls.model_structure_tolerance
        ):
            raise ValueError("channel right action must remain unitary")
        expected_samples = np.asarray(
            np.swapaxes(right_action.conjugate(), -1, -2) @ attacked @ right_action,
            dtype=np.complex128,
        )
        expected_frames = np.asarray(
            attacked_frames @ right_action, dtype=np.complex128
        )
        if not np.array_equal(samples, expected_samples):
            raise ValueError("aligned_samples do not match the declared channel")
        if not np.array_equal(frames, expected_frames):
            raise ValueError("aligned_frames do not match the declared channel")
        selection_status = self.global_selection.status
        if (
            selection_status.case_identity != request.case_identity
            or selection_status.retained_rank != request.retained_rank
            or selection_status.circuit_depth != request.circuit_depth
            or selection_status.channel
            is not Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY
            or selection_status.construction_mesh_size
            != request.configuration.global_unitary_selection_mesh_size
            or self.global_selection.selection_mesh_size
            != request.configuration.global_unitary_selection_mesh_size
        ):
            raise ValueError("global selection must match the calculation request")


@final
class Periodic1DHigherRankChannelAnalyzer:
    """Calculate transform and locality gate evidence for one channel."""

    __slots__ = ("_request", "_fourier_transformer", "_fourier_evaluator")

    def __init__(
        self,
        *,
        request: Periodic1DHigherRankChannelAnalysisRequest,
        fourier_transformer: FinitePeriodicMatrixFourierTransformer,
        fourier_evaluator: FinitePeriodicMatrixFourierTensorEvaluator,
    ) -> None:
        """Bind one complete channel request and canonical finite-periodic owners."""
        if type(request) is not Periodic1DHigherRankChannelAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankChannelAnalysisRequest"
            )
        if type(fourier_transformer) is not FinitePeriodicMatrixFourierTransformer:
            raise TypeError(
                "fourier_transformer must be the PhysKit finite-periodic owner"
            )
        if type(fourier_evaluator) is not FinitePeriodicMatrixFourierTensorEvaluator:
            raise TypeError(
                "fourier_evaluator must be the PhysKit finite-periodic evaluator"
            )
        self._request = request
        self._fourier_transformer = fourier_transformer
        self._fourier_evaluator = fourier_evaluator

    @property
    def request(self) -> Periodic1DHigherRankChannelAnalysisRequest:
        """Return the exact channel-analysis request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DHigherRankChannelMeshResult:
        """Return the complete typed result for the bound qualified channel."""
        request = self._request
        calculation_request = request.calculation_request
        controls = calculation_request.controls
        model = request.model
        coordinates = request.coordinates
        channel = request.status.channel
        reference_frames = model.reference_frames(coordinates)
        frame_norms = np.linalg.norm(
            request.aligned_frames - reference_frames,
            axis=(-2, -1),
        )
        frame_scale = math.sqrt(model.retained_rank)
        frame_recovery = Periodic1DHigherRankFrameErrorResult(
            rank=model.retained_rank,
            frobenius_maximum=float(np.max(frame_norms)),
            frobenius_rms=float(np.sqrt(np.mean(frame_norms**2))),
            normalized_frobenius_maximum=float(np.max(frame_norms) / frame_scale),
            normalized_frobenius_rms=float(
                np.sqrt(np.mean(frame_norms**2)) / frame_scale
            ),
        )
        direct_construction = self._direct_evaluation_field(coordinates)
        represented_operator_recovery = MatrixFieldErrorAnalyzer().execute(
            request.aligned_samples,
            direct_construction,
            controls.energy_reference,
        )
        known_recovery_applicable = channel in (
            Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY,
            Periodic1DHigherRankAlignmentChannel.KNOWN_INVERSE_ORACLE,
        )
        source = FinitePeriodicMatrixSamples.from_array(
            mesh=request.mesh,
            matrix_samples=request.aligned_samples,
            energy_unit=Unitless(),
            energy_reference=calculation_request.energy_reference_identifier,
            basis_identifier=calculation_request.represented_basis_identifier,
        )
        transform = self._fourier_transformer.transform(source)
        integer_modes = np.asarray(transform.series.integer_modes[:, 0], dtype=np.int64)
        expected_modes = np.arange(
            -(request.mesh.size // 2),
            request.mesh.size // 2 + 1,
            dtype=np.int64,
        )
        mode_inventory = {int(value) for value in integer_modes}
        representative_inventory_ordered_unique = bool(
            np.array_equal(integer_modes, expected_modes)
        )
        inversion_closed = mode_inventory == {-value for value in mode_inventory}
        index_bijection_pass = (
            np.unique(np.mod(integer_modes, request.mesh.size)).size
            == request.mesh.size
        )
        reconstruction_values = self._fourier_evaluator.evaluate(
            transform.series,
            (coordinates,),
            controls.maximum_working_elements,
        ).matrix_values
        reconstruction = MatrixFieldErrorAnalyzer().execute(
            reconstruction_values,
            request.aligned_samples,
            controls.energy_reference,
        )
        parseval = FinitePeriodicMatrixParsevalAnalyzer().analyze(transform)
        parseval_scale = max(
            parseval.sample_mean_squared_frobenius_norm.magnitude,
            controls.saturation_denominator_floor,
        )
        parseval_relative = parseval.absolute_defect.magnitude / parseval_scale
        hermiticity = FinitePeriodicMatrixHermiticityAnalyzer().analyze(transform)
        normalization = math.sqrt(model.retained_rank) * controls.energy_reference
        ordinary_hermiticity = (
            hermiticity.ordinary_maximum_frobenius_defect.magnitude / normalization
        )
        twisted_hermiticity = (
            hermiticity.twisted_cyclic_maximum_frobenius_defect.magnitude
            / normalization
        )
        blocks = FourierMatrixBlockNormInventoryAnalyzer1D().execute(
            transform.series,
            controls.maximum_recorded_block_range,
            controls.energy_reference,
        )
        configuration = calculation_request.configuration
        evaluation_coordinates = np.asarray(
            -0.5
            + (
                np.arange(configuration.evaluation_mesh_size, dtype=np.float64)
                + configuration.evaluation_shift_numerator
                / configuration.evaluation_shift_denominator
            )
            / configuration.evaluation_mesh_size,
            dtype=np.float64,
        )
        full_evaluation = self._fourier_evaluator.evaluate(
            transform.series,
            (evaluation_coordinates,),
            controls.maximum_working_elements,
        ).matrix_values
        direct_evaluation = self._direct_evaluation_field(evaluation_coordinates)
        interpolation = MatrixFieldComparisonAnalyzer().execute(
            full_evaluation,
            direct_evaluation,
            controls.energy_reference,
            controls.saturation_denominator_floor,
        )
        tail_analyzer = SymmetricRangeTailAnalyzer1D()
        tails = tuple(
            tail_analyzer.execute(transform.series, support, controls.energy_reference)
            for support in controls.support_radii
        )
        support_results: list[Periodic1DHigherRankSupportResult] = []
        modes = transform.series.integer_modes[:, 0]
        for tail in tails:
            retained_mask = np.abs(modes) <= tail.maximum_range
            indices = tuple(int(index) for index in np.flatnonzero(retained_mask))
            omitted_indices = tuple(
                int(index) for index in np.flatnonzero(np.logical_not(retained_mask))
            )
            truncated_series = transform.series.take(indices)
            omitted_series = transform.series.take(omitted_indices)
            truncated_evaluation = self._fourier_evaluator.evaluate(
                truncated_series,
                (evaluation_coordinates,),
                controls.maximum_working_elements,
            ).matrix_values
            omitted_construction = self._fourier_evaluator.evaluate(
                omitted_series,
                (coordinates,),
                controls.maximum_working_elements,
            ).matrix_values
            truncation = MatrixFieldComparisonAnalyzer().execute(
                truncated_evaluation,
                full_evaluation,
                controls.energy_reference,
                controls.saturation_denominator_floor,
            )
            total = MatrixFieldComparisonAnalyzer().execute(
                truncated_evaluation,
                direct_evaluation,
                controls.energy_reference,
                controls.saturation_denominator_floor,
            )
            decomposition = MatrixErrorDecompositionAnalyzer().execute(
                full_evaluation - direct_evaluation,
                truncated_evaluation - full_evaluation,
                truncated_evaluation - direct_evaluation,
                controls.energy_reference,
            )
            construction_weight = float(
                np.mean(
                    np.linalg.norm(
                        omitted_construction,
                        axis=(-2, -1),
                    )
                    ** 2
                )
            )
            parseval_denominator = max(
                construction_weight,
                tail.omitted_squared_frobenius_weight,
                model.retained_rank * controls.saturation_denominator_floor,
            )
            support_results.append(
                Periodic1DHigherRankSupportResult(
                    maximum_range=tail.maximum_range,
                    rank=model.retained_rank,
                    energy_reference=controls.energy_reference,
                    retained_translations=tail.retained_translations,
                    omitted_squared_frobenius_weight=(
                        tail.omitted_squared_frobenius_weight
                    ),
                    normalized_omitted_squared_frobenius_weight=(
                        tail.normalized_omitted_squared_frobenius_weight
                    ),
                    omitted_frobenius_l2_norm=tail.omitted_frobenius_l2_norm,
                    normalized_omitted_frobenius_l2_norm=(
                        tail.normalized_omitted_frobenius_l2_norm
                    ),
                    omitted_block_l1_norm=tail.omitted_block_l1_norm,
                    normalized_omitted_block_l1_norm=(
                        tail.normalized_omitted_block_l1_norm
                    ),
                    construction_parseval_relative_defect=(
                        abs(construction_weight - tail.omitted_squared_frobenius_weight)
                        / parseval_denominator
                    ),
                    construction_parseval_pass=(
                        abs(construction_weight - tail.omitted_squared_frobenius_weight)
                        / parseval_denominator
                        <= controls.fourier_consistency_tolerance
                    ),
                    truncation=(
                        Periodic1DHigherRankMatrixComparisonResult.from_diagnostics(
                            truncation,
                            controls.perturbation_bound_tolerance,
                        )
                    ),
                    total=Periodic1DHigherRankMatrixComparisonResult.from_diagnostics(
                        total,
                        controls.perturbation_bound_tolerance,
                    ),
                    error_decomposition_defect=(decomposition.maximum_frobenius_defect),
                    normalized_error_decomposition_defect=(
                        decomposition.normalized_maximum_frobenius_defect
                    ),
                    error_decomposition_pass=(
                        decomposition.normalized_maximum_frobenius_defect
                        <= controls.error_decomposition_tolerance
                    ),
                )
            )
        monotonicity = SymmetricRangeTailMonotonicityAnalyzer1D().execute(
            tails,
            controls.tail_monotonicity_tolerance,
        )
        maximum_tail_increase = max(
            max(
                item.normalized_squared_weight_increase,
                item.normalized_l2_norm_increase,
                item.normalized_l1_norm_increase,
            )
            for item in monotonicity
        )
        return Periodic1DHigherRankChannelMeshResult(
            status=request.status,
            transform_backend_identifier=transform.backend_identifier,
            transform_backend_version=transform.backend_version,
            fourier_representative_count=transform.series.term_count,
            fourier_representative_inventory_ordered_unique=(
                representative_inventory_ordered_unique
            ),
            fourier_inversion_closed=inversion_closed,
            fourier_index_bijection_pass=index_bijection_pass,
            no_nyquist_disposition=_ODD_CENTERED_NO_NYQUIST_DISPOSITION,
            coefficient_translations=np.asarray(
                [block.translation for block in blocks.blocks],
                dtype=np.int64,
            ),
            block_raw_frobenius_norms=np.asarray(
                [block.raw_frobenius_norm for block in blocks.blocks],
                dtype=np.float64,
            ),
            block_normalized_frobenius_norms=np.asarray(
                [block.normalized_frobenius_norm for block in blocks.blocks],
                dtype=np.float64,
            ),
            frame_recovery=frame_recovery,
            known_frame_recovery_pass=(
                frame_recovery.normalized_frobenius_maximum
                <= controls.direct_recovery_tolerance
                if known_recovery_applicable
                else None
            ),
            represented_operator_recovery=(
                Periodic1DHigherRankMatrixErrorResult.from_diagnostics(
                    represented_operator_recovery
                )
            ),
            known_operator_recovery_pass=(
                represented_operator_recovery.normalized_matrix_frobenius_maximum
                <= controls.direct_recovery_tolerance
                if known_recovery_applicable
                else None
            ),
            reconstruction=Periodic1DHigherRankMatrixErrorResult.from_diagnostics(
                reconstruction
            ),
            reconstruction_pass=(
                reconstruction.normalized_matrix_frobenius_maximum
                <= controls.fourier_consistency_tolerance
            ),
            interpolation=Periodic1DHigherRankMatrixComparisonResult.from_diagnostics(
                interpolation,
                controls.perturbation_bound_tolerance,
            ),
            final_interpolation_operator_pass=(
                interpolation.errors.normalized_matrix_frobenius_maximum
                <= controls.final_interpolation_operator_tolerance
            ),
            final_interpolation_spectrum_pass=(
                interpolation.errors.normalized_ordered_spectrum_maximum
                <= controls.final_interpolation_spectrum_tolerance
            ),
            parseval_relative_defect=parseval_relative,
            parseval_pass=(parseval_relative <= controls.fourier_consistency_tolerance),
            ordinary_hermiticity_defect=ordinary_hermiticity,
            ordinary_hermiticity_pass=(
                ordinary_hermiticity <= controls.fourier_consistency_tolerance
            ),
            twisted_cyclic_hermiticity_defect=twisted_hermiticity,
            twisted_cyclic_hermiticity_pass=(
                twisted_hermiticity <= controls.fourier_consistency_tolerance
            ),
            supports=tuple(support_results),
            maximum_tail_increase=maximum_tail_increase,
            all_tail_monotonicity_checks_pass=all(item.passes for item in monotonicity),
        )

    def _direct_evaluation_field(
        self,
        coordinates: RealArray,
    ) -> ComplexArray:
        request = self._request
        model = request.model
        channel = request.status.channel
        if channel is Periodic1DHigherRankAlignmentChannel.IDENTITY:
            return model.attacked_reduced_hamiltonians(coordinates)
        if channel is Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY:
            selected = request.global_selection.selected_global_right_unitary
            if selected is None:
                raise ValueError(
                    "global direct evaluation requires an applicable unitary"
                )
            attacked = model.attacked_reduced_hamiltonians(coordinates)
            right = np.broadcast_to(
                selected.magnitude,
                (coordinates.size, model.retained_rank, model.retained_rank),
            )
            adjoint = np.swapaxes(right.conjugate(), -1, -2)
            return np.asarray(adjoint @ attacked @ right, dtype=np.complex128)
        return model.exact_reduced_hamiltonians(coordinates)


__all__ = [
    "Periodic1DHigherRankChannelAnalysisRequest",
    "Periodic1DHigherRankChannelAnalyzer",
]
