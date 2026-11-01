"""Direct analysis of rank-two composite-band alignment and locality."""

from __future__ import annotations

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.linalg.eigen import SpectralDecomposition
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityAnalyzer1D,
    BlockHoppingHermiticityRequest1D,
)
from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorAnalyzer1D,
    BandApproximationErrorRequest1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.hamiltonian import HermitianHamiltonian
from ksdft2effmass.periodic1d.rank2.gauge_alignment.analysis import (
    Periodic1DRank2GaugeAlignmentAnalysisRequest,
    Periodic1DRank2GaugeAlignmentAnalyzer,
)
from ksdft2effmass.solidstate import (
    BandProjectedOperatorPathConstructor1D,
    BandProjectedOperatorPathRequest1D,
    BlockHoppingInterpolationRequest1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    BlockHoppingTruncationRequest1D,
    BlockHoppingTruncator1D,
    CenteredEvenMeshCyclicToOrdinaryConverter1D,
    CenteredEvenMeshCyclicToOrdinaryRequest1D,
    CenteredUniformReciprocalMesh1D,
    PolarBandFrameTransporter1D,
    PolarBandFrameTransportRequest1D,
    ReciprocalBandFramePath1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformRequest1D,
    ReciprocalOperatorSamples1D,
)

from ..configuration import Periodic1DCompositeBandAlignmentConfiguration
from .result import (
    Periodic1DCompositeBandAlignmentCalculationResult,
    Periodic1DCompositeBandAlignmentChannelRangeResult,
    Periodic1DCompositeBandAlignmentDiagnostics,
    Periodic1DCompositeBandAlignmentRangeResult,
    Periodic1DCompositeBandAlignmentTransformResult,
)


class Periodic1DCompositeBandAlignmentAnalyzer:
    """Calculate one complete rank-two alignment and block-locality result."""

    __slots__ = ("_procrustes_solver", "_request")

    def __init__(
        self,
        request: Periodic1DCompositeBandAlignmentConfiguration,
        procrustes_solver: NumpyBatchedComplexUnitaryProcrustesSolver,
    ) -> None:
        if type(request) is not Periodic1DCompositeBandAlignmentConfiguration:
            raise TypeError(
                "request must be Periodic1DCompositeBandAlignmentConfiguration"
            )
        if type(procrustes_solver) is not NumpyBatchedComplexUnitaryProcrustesSolver:
            raise TypeError(
                "procrustes_solver must be NumpyBatchedComplexUnitaryProcrustesSolver"
            )
        self._request = request
        self._procrustes_solver = procrustes_solver

    @property
    def request(self) -> Periodic1DCompositeBandAlignmentConfiguration:
        """Return the complete immutable composite-alignment request."""
        return self._request

    @property
    def procrustes_solver(self) -> NumpyBatchedComplexUnitaryProcrustesSolver:
        """Return the explicitly selected right-action Procrustes collaborator."""
        return self._procrustes_solver

    def execute(self) -> Periodic1DCompositeBandAlignmentCalculationResult:
        """Construct the exact parent, align frames, and evaluate finite ranges."""
        configuration = self.request
        unit = Unitless()
        parent = self._parent_model()
        construction_coordinates = VectorQuantity(
            np.asarray(configuration.construction_reduced_momenta(), dtype=np.float64),
            unit,
        )
        evaluation_coordinates = VectorQuantity(
            np.asarray(configuration.evaluation_reduced_momenta(), dtype=np.float64),
            unit,
        )
        construction_parent = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(parent, construction_coordinates)
        ).execute()
        evaluation_parent = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(parent, evaluation_coordinates)
        ).execute()
        construction_spectrum, raw_frames = self._spectrum_and_frames(
            construction_parent,
        )
        evaluation_spectrum, _ = self._spectrum_and_frames(
            evaluation_parent,
        )
        mesh = CenteredUniformReciprocalMesh1D(
            ScalarQuantity(1.0, unit), configuration.construction_size
        )
        raw_path = ReciprocalBandFramePath1D(
            mesh=mesh,
            frames=raw_frames,
            sewing_map=ComplexMatrixQuantity(np.eye(4, dtype=np.complex128), unit),
            orthonormality_absolute_tolerance=(
                configuration.dimensionless_absolute_tolerance
            ),
        )
        transport = PolarBandFrameTransporter1D(
            PolarBandFrameTransportRequest1D(
                raw_path,
                configuration.overlap_singular_value_threshold,
            )
        ).execute()
        reference = transport.transported
        attack_rotations = self._attack_rotations()
        attacked = self._rotate_path(reference, attack_rotations)
        alignment = Periodic1DRank2GaugeAlignmentAnalyzer(
            Periodic1DRank2GaugeAlignmentAnalysisRequest(
                reference=reference,
                attacked=attacked,
                rank_absolute_tolerance=(
                    configuration.procrustes_rank_absolute_tolerance
                ),
                rank_relative_tolerance=(
                    configuration.procrustes_rank_relative_tolerance
                ),
                validation_absolute_tolerance=(
                    configuration.dimensionless_absolute_tolerance
                ),
            ),
            self.procrustes_solver,
        ).execute()
        pointwise = alignment.pointwise_aligned
        globally_aligned = alignment.globally_aligned
        pointwise_rotation_values = np.asarray(
            [value.magnitude for value in alignment.pointwise_rotations],
            dtype=np.complex128,
        )

        reference_operator = BandProjectedOperatorPathConstructor1D(
            BandProjectedOperatorPathRequest1D(
                construction_parent,
                reference,
                configuration.dimensionless_absolute_tolerance,
            )
        ).execute()
        attacked_operator = BandProjectedOperatorPathConstructor1D(
            BandProjectedOperatorPathRequest1D(
                construction_parent,
                attacked,
                configuration.dimensionless_absolute_tolerance,
            )
        ).execute()
        pointwise_operator = BandProjectedOperatorPathConstructor1D(
            BandProjectedOperatorPathRequest1D(
                construction_parent,
                pointwise,
                configuration.dimensionless_absolute_tolerance,
            )
        ).execute()
        global_operator = BandProjectedOperatorPathConstructor1D(
            BandProjectedOperatorPathRequest1D(
                construction_parent,
                globally_aligned,
                configuration.dimensionless_absolute_tolerance,
            )
        ).execute()
        transformed = tuple(
            ReciprocalOperatorFourierTransformer1D(
                ReciprocalOperatorFourierTransformRequest1D(
                    samples,
                    mesh,
                    configuration.dimensionless_absolute_tolerance,
                    configuration.energy_absolute_tolerance,
                )
            ).execute()
            for samples in (
                reference_operator,
                attacked_operator,
                pointwise_operator,
            )
        )
        hermiticity = tuple(
            BlockHoppingHermiticityAnalyzer1D(
                BlockHoppingHermiticityRequest1D(
                    transform.hopping_model,
                    ScalarQuantity(configuration.energy_absolute_tolerance, unit),
                    configuration.construction_size,
                )
            ).execute()
            for transform in transformed
        )
        cyclic_models = tuple(transform.hopping_model for transform in transformed)
        ordinary_conversions = tuple(
            CenteredEvenMeshCyclicToOrdinaryConverter1D(
                CenteredEvenMeshCyclicToOrdinaryRequest1D(model)
            ).execute()
            for model in cyclic_models
        )
        ordinary_models = tuple(
            conversion.ordinary for conversion in ordinary_conversions
        )
        direct_evaluation_targets = self._direct_evaluation_targets(
            ordinary_models,
            evaluation_coordinates,
        )
        complete_evaluation = tuple(
            BlockHoppingInterpolator1D(
                BlockHoppingInterpolationRequest1D(model, evaluation_coordinates)
            ).execute()
            for model in ordinary_models
        )
        interpolation_errors = tuple(
            self._maximum_error_channels(complete, direct)
            for complete, direct in zip(
                complete_evaluation,
                direct_evaluation_targets,
                strict=True,
            )
        )
        transform_results = tuple(
            Periodic1DCompositeBandAlignmentTransformResult(
                channel=channel,
                representatives=transform.hopping_model.representatives,
                hopping_blocks=transform.hopping_model.hopping_blocks,
                ordinary_representatives=conversion.ordinary.representatives,
                cyclic_conversion_representative=(conversion.conversion_representative),
                cyclic_conversion_power=ScalarQuantity(
                    conversion.conversion_power_per_matrix_dimension,
                    unit,
                ),
                reconstruction_maximum_frobenius_error=ScalarQuantity(
                    transform.reconstruction_maximum_frobenius_error,
                    unit,
                ),
                hermiticity_maximum_frobenius_error=(
                    diagnostic.maximum_frobenius_defect
                ),
                evaluation_interpolation_hamiltonian_maximum_error=ScalarQuantity(
                    interpolation_error[0],
                    unit,
                ),
                evaluation_interpolation_spectral_maximum_error=ScalarQuantity(
                    interpolation_error[1],
                    unit,
                ),
            )
            for channel, transform, conversion, diagnostic, interpolation_error in zip(
                Periodic1DCompositeBandAlignmentTransformResult.CHANNELS,
                transformed,
                ordinary_conversions,
                hermiticity,
                interpolation_errors,
                strict=True,
            )
        )
        construction_target = BandSpectrumSamples1D(
            construction_coordinates,
            ScalarQuantity(1.0, unit),
            MatrixQuantity(
                construction_spectrum.magnitude[:, : configuration.retained_rank],
                unit,
            ),
        )
        range_results = tuple(
            self._range_result(
                maximum_range,
                construction_target,
                ordinary_models,
                complete_evaluation,
                direct_evaluation_targets,
            )
            for maximum_range in configuration.hopping_ranges
        )
        gaps = np.concatenate(
            (
                construction_spectrum.magnitude[:, configuration.retained_rank]
                - construction_spectrum.magnitude[:, configuration.retained_rank - 1],
                evaluation_spectrum.magnitude[:, configuration.retained_rank]
                - evaluation_spectrum.magnitude[:, configuration.retained_rank - 1],
            )
        )
        minimum_gap = float(np.min(gaps))
        if minimum_gap < configuration.sampled_gap_threshold:
            raise ValueError("parent sampled retained/excluded gap does not pass")
        pointwise_rotations = alignment.pointwise_rotations
        diagnostics = Periodic1DCompositeBandAlignmentDiagnostics(
            minimum_sampled_gap=ScalarQuantity(minimum_gap, unit),
            minimum_overlap_singular_value=(transport.minimum_overlap_singular_value),
            closure_eigenphases=transport.closure_eigenphases,
            attack_frame_maximum_frobenius_defect=self._maximum_matrix_defect(
                reference.frames,
                attacked.frames,
            ),
            pointwise_frame_maximum_frobenius_defect=self._maximum_matrix_defect(
                reference.frames,
                pointwise.frames,
            ),
            pointwise_projector_maximum_frobenius_defect=(
                self._maximum_projector_defect(reference.frames, attacked.frames)
            ),
            pointwise_rotation_recovery_maximum_frobenius_defect=(
                self._rotation_recovery_defect(
                    pointwise_rotation_values,
                    attack_rotations,
                )
            ),
            global_frame_maximum_frobenius_defect=self._maximum_matrix_defect(
                reference.frames,
                globally_aligned.frames,
            ),
            attacked_operator_maximum_frobenius_defect=ScalarQuantity(
                self._maximum_matrix_defect(
                    reference_operator.matrices,
                    attacked_operator.matrices,
                ),
                unit,
            ),
            pointwise_operator_maximum_frobenius_defect=ScalarQuantity(
                self._maximum_matrix_defect(
                    reference_operator.matrices,
                    pointwise_operator.matrices,
                ),
                unit,
            ),
            global_operator_maximum_frobenius_defect=ScalarQuantity(
                self._maximum_matrix_defect(
                    reference_operator.matrices,
                    global_operator.matrices,
                ),
                unit,
            ),
            pointwise_minimum_cross_singular_value=(
                alignment.pointwise_minimum_cross_singular_value
            ),
            global_minimum_cross_singular_value=(
                alignment.global_minimum_cross_singular_value
            ),
            pointwise_maximum_rank_cutoff=alignment.pointwise_maximum_rank_cutoff,
            global_rank_cutoff=alignment.global_rank_cutoff,
        )
        return Periodic1DCompositeBandAlignmentCalculationResult(
            calculation_family=(
                Periodic1DCompositeBandAlignmentCalculationResult.CALCULATION_FAMILY
            ),
            configuration=configuration,
            construction_reduced_momenta=(configuration.construction_reduced_momenta()),
            evaluation_reduced_momenta=configuration.evaluation_reduced_momenta(),
            construction_parent_spectrum=construction_spectrum,
            evaluation_parent_spectrum=evaluation_spectrum,
            reference_frames=reference.frames,
            attacked_frames=attacked.frames,
            pointwise_aligned_frames=pointwise.frames,
            globally_aligned_frames=globally_aligned.frames,
            pointwise_rotations=pointwise_rotations,
            global_rotation=alignment.global_rotation,
            reference_operators=reference_operator.matrices,
            attacked_operators=attacked_operator.matrices,
            pointwise_aligned_operators=pointwise_operator.matrices,
            globally_aligned_operators=global_operator.matrices,
            diagnostics=diagnostics,
            transforms=transform_results,
            ranges=range_results,
        )

    def _parent_model(self) -> BlockHoppingModel1D:
        configuration = self.request
        denominator = float(configuration.coefficient_denominator)
        onsite = (
            np.asarray(
                configuration.onsite_numerators,
                dtype=np.complex128,
            )
            / denominator
        )
        positive = (
            np.asarray(
                configuration.positive_hopping_numerators,
                dtype=np.complex128,
            )
            / denominator
        )
        unit = Unitless()
        return BlockHoppingModel1D(
            reciprocal_period=ScalarQuantity(1.0, unit),
            representatives=(-1, 0, 1),
            hopping_blocks=(
                ComplexMatrixQuantity(positive.conj().T, unit),
                ComplexMatrixQuantity(onsite, unit),
                ComplexMatrixQuantity(positive, unit),
            ),
        )

    def _spectrum_and_frames(
        self,
        samples: ReciprocalOperatorSamples1D,
    ) -> tuple[MatrixQuantity, tuple[ComplexMatrixQuantity, ...]]:
        configuration = self.request
        values: list[Float64Array] = []
        frames: list[ComplexMatrixQuantity] = []
        for matrix in samples.matrices:
            symmetric = 0.5 * (matrix.magnitude + matrix.magnitude.conj().T)
            represented = np.triu(symmetric) + np.triu(symmetric, 1).conj().T
            hamiltonian = HermitianHamiltonian(
                matrix=ComplexMatrixQuantity(represented, Unitless())
            )
            eigensystem = SpectralDecomposition(hamiltonian.matrix).eigensystem(4)
            values.append(
                np.asarray(eigensystem.eigenvalues.magnitude, dtype=np.float64)
            )
            frames.append(
                ComplexMatrixQuantity(
                    np.asarray(
                        eigensystem.eigenvectors.magnitude[
                            :, : configuration.retained_rank
                        ],
                        dtype=np.complex128,
                    ),
                    Unitless(),
                )
            )
        return (
            MatrixQuantity(np.asarray(values, dtype=np.float64), Unitless()),
            tuple(frames),
        )

    def _attack_rotations(self) -> tuple[Complex128Array, ...]:
        return self._attack_rotations_at(
            self.request.construction_reduced_momenta(),
        )

    def _attack_rotations_at(
        self,
        reduced_momenta: tuple[float, ...],
    ) -> tuple[Complex128Array, ...]:
        configuration = self.request
        rotations: list[Complex128Array] = []
        for momentum in reduced_momenta:
            angle = configuration.attack_constant_angle + sum(
                coefficient * np.sin(2.0 * np.pi * harmonic * momentum)
                for harmonic, coefficient in enumerate(
                    configuration.attack_sine_coefficients,
                    start=1,
                )
            )
            cosine = float(np.cos(angle))
            sine = float(np.sin(angle))
            rotations.append(
                np.asarray(
                    ((cosine, -sine), (sine, cosine)),
                    dtype=np.complex128,
                )
            )
        return tuple(rotations)

    def _rotate_path(
        self,
        source: ReciprocalBandFramePath1D,
        rotations: tuple[Complex128Array, ...],
    ) -> ReciprocalBandFramePath1D:
        if len(rotations) != source.mesh.point_count:
            raise ValueError("one rotation is required per reciprocal point")
        return ReciprocalBandFramePath1D(
            mesh=source.mesh,
            frames=tuple(
                ComplexMatrixQuantity(frame.magnitude @ rotation, Unitless())
                for frame, rotation in zip(source.frames, rotations, strict=True)
            ),
            sewing_map=source.sewing_map,
            orthonormality_absolute_tolerance=(
                source.orthonormality_absolute_tolerance
            ),
        )

    def _direct_evaluation_targets(
        self,
        ordinary_models: tuple[BlockHoppingModel1D, ...],
        evaluation_coordinates: VectorQuantity,
    ) -> tuple[ReciprocalOperatorSamples1D, ...]:
        reference = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(
                ordinary_models[0], evaluation_coordinates
            )
        ).execute()
        attacks = self._attack_rotations_at(
            self.request.evaluation_reduced_momenta(),
        )
        attacked = ReciprocalOperatorSamples1D(
            coordinates=reference.coordinates,
            reciprocal_period=reference.reciprocal_period,
            matrices=tuple(
                ComplexMatrixQuantity(
                    attack.conj().T @ matrix.magnitude @ attack,
                    matrix.unit,
                )
                for matrix, attack in zip(reference.matrices, attacks, strict=True)
            ),
        )
        return (reference, attacked, reference)

    def _maximum_error_channels(
        self,
        candidate: ReciprocalOperatorSamples1D,
        reference: ReciprocalOperatorSamples1D,
    ) -> tuple[float, float]:
        if len(candidate.matrices) != len(reference.matrices):
            raise ValueError("error-channel operator inventories must have equal size")
        hamiltonian_errors: list[float] = []
        spectral_errors: list[float] = []
        for candidate_matrix, reference_matrix in zip(
            candidate.matrices,
            reference.matrices,
            strict=True,
        ):
            hamiltonian_errors.append(
                float(
                    np.linalg.norm(
                        candidate_matrix.magnitude - reference_matrix.magnitude
                    )
                    / np.sqrt(2.0)
                )
            )
            candidate_hermitian = 0.5 * (
                candidate_matrix.magnitude + candidate_matrix.magnitude.conj().T
            )
            reference_hermitian = 0.5 * (
                reference_matrix.magnitude + reference_matrix.magnitude.conj().T
            )
            spectral_errors.append(
                float(
                    np.max(
                        np.abs(
                            np.linalg.eigvalsh(candidate_hermitian)
                            - np.linalg.eigvalsh(reference_hermitian)
                        )
                    )
                )
            )
        return max(hamiltonian_errors), max(spectral_errors)

    def _range_result(
        self,
        maximum_range: int,
        construction_target: BandSpectrumSamples1D,
        ordinary_models: tuple[BlockHoppingModel1D, ...],
        complete_evaluation: tuple[ReciprocalOperatorSamples1D, ...],
        direct_evaluation_targets: tuple[ReciprocalOperatorSamples1D, ...],
    ) -> Periodic1DCompositeBandAlignmentRangeResult:
        configuration = self.request
        channels: list[Periodic1DCompositeBandAlignmentChannelRangeResult] = []
        for channel, model, complete, direct in zip(
            Periodic1DCompositeBandAlignmentTransformResult.CHANNELS,
            ordinary_models,
            complete_evaluation,
            direct_evaluation_targets,
            strict=True,
        ):
            truncation = BlockHoppingTruncator1D(
                BlockHoppingTruncationRequest1D(model, maximum_range)
            ).execute()
            construction = BlockHoppingInterpolator1D(
                BlockHoppingInterpolationRequest1D(
                    truncation.truncated, construction_target.coordinates
                )
            ).execute()
            evaluation = BlockHoppingInterpolator1D(
                BlockHoppingInterpolationRequest1D(
                    truncation.truncated, direct.coordinates
                )
            ).execute()
            truncation_errors = self._maximum_error_channels(evaluation, complete)
            total_errors = self._maximum_error_channels(evaluation, direct)
            construction_error = BandApproximationErrorAnalyzer1D(
                BandApproximationErrorRequest1D(
                    construction_target,
                    construction,
                    configuration.dimensionless_absolute_tolerance,
                )
            ).execute()
            channels.append(
                Periodic1DCompositeBandAlignmentChannelRangeResult(
                    channel=channel,
                    ordinary_omitted_block_l2_norm=ScalarQuantity(
                        truncation.omitted_block_l2_norm,
                        Unitless(),
                    ),
                    construction_total_spectral_maximum_error=(
                        construction_error.maximum_absolute_error
                    ),
                    evaluation_truncation_hamiltonian_maximum_error=ScalarQuantity(
                        truncation_errors[0],
                        Unitless(),
                    ),
                    evaluation_total_hamiltonian_maximum_error=ScalarQuantity(
                        total_errors[0],
                        Unitless(),
                    ),
                    evaluation_truncation_spectral_maximum_error=ScalarQuantity(
                        truncation_errors[1],
                        Unitless(),
                    ),
                    evaluation_total_spectral_maximum_error=ScalarQuantity(
                        total_errors[1],
                        Unitless(),
                    ),
                )
            )
        return Periodic1DCompositeBandAlignmentRangeResult(
            maximum_range=maximum_range,
            channels=tuple(channels),
        )

    def _maximum_matrix_defect(
        self,
        reference: tuple[ComplexMatrixQuantity, ...],
        candidate: tuple[ComplexMatrixQuantity, ...],
    ) -> float:
        return float(
            max(
                np.linalg.norm(left.magnitude - right.magnitude)
                for left, right in zip(reference, candidate, strict=True)
            )
        )

    def _maximum_projector_defect(
        self,
        reference: tuple[ComplexMatrixQuantity, ...],
        candidate: tuple[ComplexMatrixQuantity, ...],
    ) -> float:
        return float(
            max(
                np.linalg.norm(
                    left.magnitude @ left.magnitude.conj().T
                    - right.magnitude @ right.magnitude.conj().T
                )
                for left, right in zip(reference, candidate, strict=True)
            )
        )

    def _rotation_recovery_defect(
        self,
        recovered: Complex128Array,
        attacks: tuple[Complex128Array, ...],
    ) -> float:
        return float(
            max(
                np.linalg.norm(rotation - attack.conj().T)
                for rotation, attack in zip(recovered, attacks, strict=True)
            )
        )


__all__ = ["Periodic1DCompositeBandAlignmentAnalyzer"]
