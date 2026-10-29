"""Direct analysis of rank-two composite-band alignment and locality."""

from __future__ import annotations

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
    ComplexUnitaryProcrustesTolerance,
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
)
from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorAnalyzer1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.hamiltonian import HermitianHamiltonian
from ksdft2effmass.solidstate import (
    BandProjectedOperatorPathConstructor1D,
    BandProjectedOperatorPathRequest1D,
    BlockHoppingInterpolationRequest1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    BlockHoppingTruncationRequest1D,
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    PolarBandFrameTransporter1D,
    PolarBandFrameTransportRequest1D,
    ReciprocalBandFramePath1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformRequest1D,
    ReciprocalOperatorSamples1D,
)

from .configuration import Periodic1DCompositeBandAlignmentConfiguration
from .result import (
    Periodic1DCompositeBandAlignmentCalculationResult,
    Periodic1DCompositeBandAlignmentChannelRangeResult,
    Periodic1DCompositeBandAlignmentDiagnostics,
    Periodic1DCompositeBandAlignmentRangeResult,
    Periodic1DCompositeBandAlignmentTransformResult,
)


class Periodic1DCompositeBandAlignmentAnalyzer:
    """Calculate one complete rank-two alignment and block-locality result."""

    __slots__ = ()

    def execute(
        self,
        configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> Periodic1DCompositeBandAlignmentCalculationResult:
        """Construct the exact parent, align frames, and evaluate finite ranges."""
        if type(configuration) is not Periodic1DCompositeBandAlignmentConfiguration:
            raise TypeError(
                "configuration must be Periodic1DCompositeBandAlignmentConfiguration"
            )
        unit = Unitless()
        parent = self._parent_model(configuration)
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
            configuration,
        )
        evaluation_spectrum, _ = self._spectrum_and_frames(
            evaluation_parent,
            configuration,
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
        attack_rotations = self._attack_rotations(configuration)
        attacked = self._rotate_path(reference, attack_rotations)
        tolerance = ComplexUnitaryProcrustesTolerance(
            rank_absolute=configuration.procrustes_rank_absolute_tolerance,
            rank_relative=configuration.procrustes_rank_relative_tolerance,
            validation_absolute=configuration.dimensionless_absolute_tolerance,
            validation_relative=0.0,
            rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
        )
        source = np.asarray(
            [frame.magnitude for frame in attacked.frames], dtype=np.complex128
        )
        target = np.asarray(
            [frame.magnitude for frame in reference.frames], dtype=np.complex128
        )
        solver = NumpyBatchedComplexUnitaryProcrustesSolver()
        pointwise_selection = solver.solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                source,
                target,
                tolerance,
            )
        )
        pointwise_rotation_values = (
            pointwise_selection.require_unique_right_unitary_transformations()
        )
        pointwise = self._rotate_path(
            attacked,
            tuple(pointwise_rotation_values[index] for index in range(source.shape[0])),
        )
        global_selection = solver.solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                source.reshape(1, -1, configuration.retained_rank),
                target.reshape(1, -1, configuration.retained_rank),
                tolerance,
            )
        )
        global_rotation_value = (
            global_selection.require_unique_right_unitary_transformations()[0]
        )
        globally_aligned = self._rotate_path(
            attacked,
            tuple(
                global_rotation_value for _ in range(configuration.construction_size)
            ),
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
            BlockHoppingHermiticityAnalyzer1D().execute(
                transform.hopping_model,
                ScalarQuantity(configuration.energy_absolute_tolerance, unit),
                configuration.construction_size,
            )
            for transform in transformed
        )
        cyclic_models = tuple(transform.hopping_model for transform in transformed)
        ordinary_models = tuple(self._ordinary_model(model) for model in cyclic_models)
        direct_evaluation_targets = self._direct_evaluation_targets(
            configuration,
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
                ordinary_representatives=ordinary.representatives,
                cyclic_conversion_representative=(
                    transform.hopping_model.representatives[0]
                ),
                cyclic_conversion_power=ScalarQuantity(
                    self._cyclic_conversion_power(
                        transform.hopping_model,
                        configuration.retained_rank,
                    ),
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
            for channel, transform, ordinary, diagnostic, interpolation_error in zip(
                Periodic1DCompositeBandAlignmentTransformResult.CHANNELS,
                transformed,
                ordinary_models,
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
                configuration,
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
        pointwise_rotations = tuple(
            ComplexMatrixQuantity(value, unit) for value in pointwise_rotation_values
        )
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
            pointwise_minimum_cross_singular_value=float(
                np.min(pointwise_selection.cross_singular_values)
            ),
            global_minimum_cross_singular_value=float(
                np.min(global_selection.cross_singular_values)
            ),
            pointwise_maximum_rank_cutoff=float(
                np.max(pointwise_selection.applied_rank_cutoffs)
            ),
            global_rank_cutoff=float(global_selection.applied_rank_cutoffs[0]),
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
            global_rotation=ComplexMatrixQuantity(global_rotation_value, unit),
            reference_operators=reference_operator.matrices,
            attacked_operators=attacked_operator.matrices,
            pointwise_aligned_operators=pointwise_operator.matrices,
            globally_aligned_operators=global_operator.matrices,
            diagnostics=diagnostics,
            transforms=transform_results,
            ranges=range_results,
        )

    @staticmethod
    def _parent_model(
        configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> BlockHoppingModel1D:
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

    @staticmethod
    def _spectrum_and_frames(
        samples: ReciprocalOperatorSamples1D,
        configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> tuple[MatrixQuantity, tuple[ComplexMatrixQuantity, ...]]:
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

    @classmethod
    def _attack_rotations(
        cls,
        configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> tuple[Complex128Array, ...]:
        return cls._attack_rotations_at(
            configuration,
            configuration.construction_reduced_momenta(),
        )

    @staticmethod
    def _attack_rotations_at(
        configuration: Periodic1DCompositeBandAlignmentConfiguration,
        reduced_momenta: tuple[float, ...],
    ) -> tuple[Complex128Array, ...]:
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

    @staticmethod
    def _rotate_path(
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

    @staticmethod
    def _ordinary_model(model: BlockHoppingModel1D) -> BlockHoppingModel1D:
        conversion_representative = -len(model.representatives) // 2
        retained = tuple(
            (representative, block)
            for representative, block in zip(
                model.representatives,
                model.hopping_blocks,
                strict=True,
            )
            if representative != conversion_representative
        )
        if len(retained) != len(model.representatives) - 1:
            raise ValueError("cyclic model does not contain one negative Nyquist class")
        return BlockHoppingModel1D(
            reciprocal_period=model.reciprocal_period,
            representatives=tuple(item[0] for item in retained),
            hopping_blocks=tuple(item[1] for item in retained),
        )

    @staticmethod
    def _cyclic_conversion_power(
        model: BlockHoppingModel1D,
        retained_rank: int,
    ) -> float:
        conversion_representative = -len(model.representatives) // 2
        block = model.hopping_blocks[
            model.representatives.index(conversion_representative)
        ]
        return float(np.linalg.norm(block.magnitude) ** 2 / retained_rank)

    @classmethod
    def _direct_evaluation_targets(
        cls,
        configuration: Periodic1DCompositeBandAlignmentConfiguration,
        ordinary_models: tuple[BlockHoppingModel1D, ...],
        evaluation_coordinates: VectorQuantity,
    ) -> tuple[ReciprocalOperatorSamples1D, ...]:
        reference = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(
                ordinary_models[0], evaluation_coordinates
            )
        ).execute()
        attacks = cls._attack_rotations_at(
            configuration,
            configuration.evaluation_reduced_momenta(),
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

    @staticmethod
    def _maximum_error_channels(
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

    @classmethod
    def _range_result(
        cls,
        configuration: Periodic1DCompositeBandAlignmentConfiguration,
        maximum_range: int,
        construction_target: BandSpectrumSamples1D,
        ordinary_models: tuple[BlockHoppingModel1D, ...],
        complete_evaluation: tuple[ReciprocalOperatorSamples1D, ...],
        direct_evaluation_targets: tuple[ReciprocalOperatorSamples1D, ...],
    ) -> Periodic1DCompositeBandAlignmentRangeResult:
        analyzer = BandApproximationErrorAnalyzer1D()
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
            truncation_errors = cls._maximum_error_channels(evaluation, complete)
            total_errors = cls._maximum_error_channels(evaluation, direct)
            channels.append(
                Periodic1DCompositeBandAlignmentChannelRangeResult(
                    channel=channel,
                    ordinary_omitted_block_l2_norm=ScalarQuantity(
                        truncation.omitted_block_l2_norm,
                        Unitless(),
                    ),
                    construction_total_spectral_maximum_error=analyzer.execute(
                        construction_target,
                        construction,
                        configuration.dimensionless_absolute_tolerance,
                    ).maximum_absolute_error,
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

    @staticmethod
    def _maximum_matrix_defect(
        reference: tuple[ComplexMatrixQuantity, ...],
        candidate: tuple[ComplexMatrixQuantity, ...],
    ) -> float:
        return float(
            max(
                np.linalg.norm(left.magnitude - right.magnitude)
                for left, right in zip(reference, candidate, strict=True)
            )
        )

    @staticmethod
    def _maximum_projector_defect(
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

    @staticmethod
    def _rotation_recovery_defect(
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
