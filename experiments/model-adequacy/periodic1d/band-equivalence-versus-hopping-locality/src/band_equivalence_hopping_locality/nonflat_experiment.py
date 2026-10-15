"""Calculation actions for the smooth non-flat four-state realization."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from projectkoios.numerics.finite_periodic.finite_series import (
    FiniteFourierSeriesEvaluationDefinition,
    FiniteFourierSeriesEvaluatorFactory,
    FiniteFourierSeriesMethod,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesDefinition,
    ComplexUnitaryProcrustesMethod,
    ComplexUnitaryProcrustesSolverFactory,
    ComplexUnitaryProcrustesStatus,
    ComplexUnitaryProcrustesTolerance,
)
from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonic,
    PeriodicHarmonicMaximizer,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    BlockHoppingModel,
    BlockHoppingTerm,
)
from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from .nonflat_definition import (
    SmoothFourStateAdaptiveAmplitudeDefinition,
    SmoothFourStateConvergenceDefinition,
    SmoothFourStateDefinition,
    SmoothFourStateParentFamilyDefinition,
)
from .nonflat_results import (
    SmoothFourStateAdaptiveAmplitudeResult,
    SmoothFourStateAmplitudeRefinementResult,
    SmoothFourStateAmplitudeValidationResult,
    SmoothFourStateConvergenceDisposition,
    SmoothFourStateConvergenceResult,
    SmoothFourStateHoppingBlockResult,
    SmoothFourStateParentFamilyResult,
    SmoothFourStatePointResult,
    SmoothFourStateRefinementResult,
    SmoothFourStateResult,
)

ComplexArray = npt.NDArray[np.complex128]
RealArray = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class _PreparedFourStateParent:
    coordinates: RealArray
    retained_matrices: ComplexArray
    traceless_matrices: ComplexArray
    mean_energies: RealArray
    displacements: tuple[int, ...]
    splitting_scale: float
    minimum_external_gap: float
    minimum_transport_singular_value: float
    maximum_frame_orthonormality_defect: float
    periodic_closure_defect: float
    maximum_reference_hermiticity_defect: float
    reference_blocks: ComplexArray
    reference_powers: RealArray
    reference_nonzero_weight: float
    reference_parseval_defect: float


class SmoothFourStateExperiment:
    """Evaluate the smooth gauge family on the specified non-flat parent."""

    __slots__ = ()

    def execute(self, definition: SmoothFourStateDefinition) -> SmoothFourStateResult:
        """Calculate parent diagnostics and all declared amplitudes."""
        if type(definition) is not SmoothFourStateDefinition:
            raise TypeError("definition must be SmoothFourStateDefinition")
        parent = self._prepare_parent(definition)
        maximizer = PeriodicHarmonicMaximizer(
            absolute_degeneracy_tolerance=(
                definition.harmonic_absolute_degeneracy_tolerance
            ),
            relative_degeneracy_tolerance=(
                definition.harmonic_relative_degeneracy_tolerance
            ),
        )
        points = tuple(
            self._point(definition, parent, amplitude, maximizer)
            for amplitude in definition.amplitudes
        )
        return SmoothFourStateResult(
            definition=definition,
            minimum_external_gap=parent.minimum_external_gap,
            minimum_transport_singular_value=(parent.minimum_transport_singular_value),
            maximum_frame_orthonormality_defect=(
                parent.maximum_frame_orthonormality_defect
            ),
            periodic_closure_defect=parent.periodic_closure_defect,
            maximum_reference_hermiticity_defect=(
                parent.maximum_reference_hermiticity_defect
            ),
            points=points,
        )

    @classmethod
    def _prepare_parent(
        cls, definition: SmoothFourStateDefinition
    ) -> _PreparedFourStateParent:
        sample_count = definition.reciprocal_mesh_size
        coordinates = -0.5 + np.arange(sample_count, dtype=np.float64) / float(
            sample_count
        )
        parent_matrices = cls._parent_matrices(
            coordinates, definition.parent_hopping_scale
        )
        eigenvalues, eigenvectors = np.linalg.eigh(parent_matrices)
        external_gap = float(np.min(eigenvalues[:, 2] - eigenvalues[:, 1]))
        if external_gap < definition.minimum_external_gap:
            raise ValueError("external gap fails its declared lower bound")
        raw_frames = eigenvectors[:, :, :2]
        frames, minimum_singular, closure_defect = cls._periodic_frame(
            raw_frames, definition
        )
        identity = np.eye(2, dtype=np.complex128)
        orthonormality_defect = float(
            max(np.linalg.norm(frame.conj().T @ frame - identity) for frame in frames)
        )
        if orthonormality_defect > definition.frame_absolute_tolerance:
            raise FloatingPointError("periodic frame fails orthonormality tolerance")
        retained = np.einsum(
            "nji,njk,nkl->nil",
            frames.conj(),
            parent_matrices,
            frames,
            optimize=True,
        )
        hermiticity_defect = float(
            np.max(np.abs(retained - retained.conj().transpose(0, 2, 1)))
        )
        if hermiticity_defect > definition.frame_absolute_tolerance:
            raise FloatingPointError("retained matrices fail Hermiticity tolerance")
        means = np.trace(retained, axis1=1, axis2=2).real / 2.0
        traceless = retained - means[:, None, None] * identity
        splitting_scale = float(
            np.mean(np.sum(np.abs(traceless) ** 2, axis=(1, 2))) / 2.0
        )
        if not math.isfinite(splitting_scale) or splitting_scale <= 0.0:
            raise FloatingPointError("splitting scale must be finite and positive")
        displacements = tuple(range(-(sample_count // 2), sample_count // 2))
        reference_blocks = cls._fourier_blocks(coordinates, retained, displacements)
        reference_powers = cls._block_powers(
            displacements,
            reference_blocks,
            f"finite-mesh-reference-{sample_count}",
        )
        cls._check_fourier_reconstruction(
            coordinates,
            displacements,
            reference_blocks,
            retained,
            definition.frame_absolute_tolerance,
        )
        cls._check_hopping_symmetry(
            displacements,
            reference_blocks,
            definition.frame_absolute_tolerance,
        )
        reference_nonzero = math.fsum(
            float(power)
            for displacement, power in zip(displacements, reference_powers, strict=True)
            if displacement != 0
        )
        reciprocal_power = float(
            np.mean(np.sum(np.abs(retained) ** 2, axis=(1, 2))) / 2.0
        )
        parseval_defect = abs(reciprocal_power - float(np.sum(reference_powers)))
        for array in (
            coordinates,
            retained,
            traceless,
            means,
            reference_blocks,
            reference_powers,
        ):
            array.setflags(write=False)
        return _PreparedFourStateParent(
            coordinates=coordinates,
            retained_matrices=retained,
            traceless_matrices=traceless,
            mean_energies=means,
            displacements=displacements,
            splitting_scale=splitting_scale,
            minimum_external_gap=external_gap,
            minimum_transport_singular_value=minimum_singular,
            maximum_frame_orthonormality_defect=orthonormality_defect,
            periodic_closure_defect=closure_defect,
            maximum_reference_hermiticity_defect=hermiticity_defect,
            reference_blocks=reference_blocks,
            reference_powers=reference_powers,
            reference_nonzero_weight=reference_nonzero,
            reference_parseval_defect=parseval_defect,
        )

    @staticmethod
    def _parent_matrices(
        coordinates: RealArray, parent_hopping_scale: float
    ) -> ComplexArray:
        lower_onsite = np.asarray([[-1.20, 0.06], [0.06, -0.35]], dtype=np.complex128)
        upper_onsite = np.asarray([[1.00, 0.04], [0.04, 1.75]], dtype=np.complex128)
        lower_hopping = np.diag(np.asarray([0.15, -0.10])).astype(np.complex128)
        upper_hopping = np.diag(np.asarray([0.05, -0.04])).astype(np.complex128)
        coupling = np.diag(np.asarray([0.12, 0.10])).astype(np.complex128)
        matrices = np.empty((coordinates.size, 4, 4), dtype=np.complex128)
        for index, coordinate in enumerate(coordinates):
            phase = np.exp(2.0j * np.pi * coordinate)
            scaled_phase = parent_hopping_scale * phase
            matrices[index] = np.block(
                [
                    [
                        lower_onsite
                        + scaled_phase * lower_hopping
                        + scaled_phase.conjugate() * lower_hopping.conj().T,
                        scaled_phase * coupling,
                    ],
                    [
                        scaled_phase.conjugate() * coupling.conj().T,
                        upper_onsite
                        + scaled_phase * upper_hopping
                        + scaled_phase.conjugate() * upper_hopping.conj().T,
                    ],
                ]
            )
        return matrices

    @classmethod
    def _periodic_frame(
        cls,
        raw_frames: ComplexArray,
        definition: SmoothFourStateDefinition,
    ) -> tuple[ComplexArray, float, float]:
        sample_count = raw_frames.shape[0]
        transported = [raw_frames[0]]
        minimum_singular = 1.0
        for index in range(1, sample_count):
            aligned, singular_values = cls._align_neighbor(
                transported[-1],
                raw_frames[index],
                definition.minimum_transport_singular_value,
                definition.frame_absolute_tolerance,
            )
            minimum_singular = min(minimum_singular, float(singular_values[-1]))
            transported.append(aligned)
        duplicate, singular_values = cls._align_neighbor(
            transported[-1],
            raw_frames[0],
            definition.minimum_transport_singular_value,
            definition.frame_absolute_tolerance,
        )
        minimum_singular = min(minimum_singular, float(singular_values[-1]))
        if minimum_singular <= definition.minimum_transport_singular_value:
            raise ValueError("transport overlap fails its declared lower bound")

        transported_array = np.asarray(transported, dtype=np.complex128)
        mismatch = transported_array[0].conj().T @ duplicate
        left, _, right_h = np.linalg.svd(mismatch)
        mismatch_unitary = left @ right_h
        eigenvalues, eigenvectors = np.linalg.eig(mismatch_unitary)
        eigenvector_inverse = np.linalg.inv(eigenvectors)
        phases = np.angle(eigenvalues)
        corrected = np.empty_like(transported_array)
        for index in range(sample_count):
            fraction = float(index) / float(sample_count)
            correction = (
                eigenvectors
                @ np.diag(np.exp(-1.0j * fraction * phases))
                @ eigenvector_inverse
            )
            correction_left, _, correction_right_h = np.linalg.svd(correction)
            correction = correction_left @ correction_right_h
            corrected[index] = transported_array[index] @ correction
        endpoint_correction = (
            eigenvectors @ np.diag(np.exp(-1.0j * phases)) @ eigenvector_inverse
        )
        correction_left, _, correction_right_h = np.linalg.svd(endpoint_correction)
        endpoint_correction = correction_left @ correction_right_h
        closure_defect = float(
            np.linalg.norm(duplicate @ endpoint_correction - corrected[0])
        )
        if closure_defect > definition.frame_absolute_tolerance:
            raise FloatingPointError("periodic frame fails closure tolerance")
        return corrected, minimum_singular, closure_defect

    @staticmethod
    def _align_neighbor(
        accepted: ComplexArray,
        raw: ComplexArray,
        minimum_singular_value: float,
        numerical_absolute_tolerance: float,
    ) -> tuple[ComplexArray, RealArray]:
        result = ComplexUnitaryProcrustesSolverFactory.create(
            ComplexUnitaryProcrustesMethod.NUMPY_DENSE
        ).solve(
            ComplexUnitaryProcrustesDefinition(
                source_matrix=tuple(
                    tuple(complex(value) for value in row) for row in raw
                ),
                target_matrix=tuple(
                    tuple(complex(value) for value in row) for row in accepted
                ),
                tolerance=ComplexUnitaryProcrustesTolerance(
                    rank_absolute=numerical_absolute_tolerance,
                    rank_relative=1.0e-12,
                    validation_absolute=numerical_absolute_tolerance,
                    validation_relative=1.0e-10,
                ),
            )
        )
        singular_values = np.asarray(result.cross_singular_values, dtype=np.float64)
        if result.status is ComplexUnitaryProcrustesStatus.RANK_DEFICIENT:
            raise ValueError("transport overlap is numerically rank deficient")
        if float(singular_values[-1]) <= minimum_singular_value:
            raise ValueError("transport overlap fails before unitary completion")
        if result.transformation is None:
            raise AssertionError(
                "unique Procrustes result must contain a transformation"
            )
        rotation = np.asarray(result.transformation, dtype=np.complex128)
        return raw @ rotation, singular_values

    @classmethod
    def _point(
        cls,
        definition: SmoothFourStateDefinition,
        parent: _PreparedFourStateParent,
        amplitude: float,
        maximizer: PeriodicHarmonicMaximizer,
    ) -> SmoothFourStatePointResult:
        theta = amplitude * np.sin(2.0 * np.pi * parent.coordinates)
        cosine = np.cos(theta)
        sine = np.sin(theta)
        rotations = np.empty((parent.coordinates.size, 2, 2), dtype=np.complex128)
        rotations[:, 0, 0] = cosine
        rotations[:, 0, 1] = -sine
        rotations[:, 1, 0] = sine
        rotations[:, 1, 1] = cosine
        comparison = np.einsum(
            "nji,njk,nkl->nil",
            rotations.conj(),
            parent.retained_matrices,
            rotations,
            optimize=True,
        )
        comparison_eigenvalues = np.linalg.eigvalsh(comparison)
        reference_eigenvalues = np.linalg.eigvalsh(parent.retained_matrices)
        band_defect = float(
            np.max(np.abs(comparison_eigenvalues - reference_eigenvalues))
        )
        identity = np.eye(2, dtype=np.complex128)
        comparison_traceless = (
            comparison - parent.mean_energies[:, None, None] * identity
        )
        harmonic = cls._correlation_harmonic(
            parent.traceless_matrices, comparison_traceless
        )
        maximum = maximizer.maximize(harmonic)
        raw_correlation = maximum.maximum_value / parent.splitting_scale
        tolerance = definition.verification_absolute_tolerance
        if abs(raw_correlation - 1.0) <= tolerance:
            correlation = 1.0
        elif abs(raw_correlation + 1.0) <= tolerance:
            correlation = -1.0
        elif not -1.0 < raw_correlation < 1.0:
            raise FloatingPointError("maximum correlation lies outside [-1, 1]")
        else:
            correlation = raw_correlation
        optimal_scale = max(0.0, correlation)
        minimum_squared_loss = parent.splitting_scale * (
            1.0 - optimal_scale * optimal_scale
        )
        minimum_threshold = math.sqrt(max(0.0, minimum_squared_loss))
        joint_threshold = math.sqrt(
            max(0.0, 2.0 * parent.splitting_scale * (1.0 - correlation))
        )
        selected_angle = maximum.canonical_maximizing_argument
        reconstruction_angle = 0.0 if selected_angle is None else selected_angle
        global_rotation = np.asarray(
            [
                [math.cos(reconstruction_angle), -math.sin(reconstruction_angle)],
                [math.sin(reconstruction_angle), math.cos(reconstruction_angle)],
            ],
            dtype=np.complex128,
        )
        aligned_traceless = np.einsum(
            "ji,njk,kl->nil",
            global_rotation.conj(),
            parent.traceless_matrices,
            global_rotation,
            optimize=True,
        )
        candidate = (
            parent.mean_energies[:, None, None] * identity
            + optimal_scale * aligned_traceless
        )
        reconstructed_loss = float(
            np.mean(np.sum(np.abs(candidate - comparison) ** 2, axis=(1, 2))) / 2.0
        )
        reconstruction_defect = abs(reconstructed_loss - minimum_squared_loss)

        comparison_blocks = cls._fourier_blocks(
            parent.coordinates, comparison, parent.displacements
        )
        cls._check_fourier_reconstruction(
            parent.coordinates,
            parent.displacements,
            comparison_blocks,
            comparison,
            definition.frame_absolute_tolerance,
        )
        cls._check_hopping_symmetry(
            parent.displacements,
            comparison_blocks,
            definition.frame_absolute_tolerance,
        )
        comparison_powers = cls._block_powers(
            parent.displacements,
            comparison_blocks,
            (f"finite-mesh-comparison-{parent.coordinates.size}-{amplitude.hex()}"),
        )
        comparison_nonzero = math.fsum(
            float(power)
            for displacement, power in zip(
                parent.displacements, comparison_powers, strict=True
            )
            if displacement != 0
        )
        comparison_reciprocal_power = float(
            np.mean(np.sum(np.abs(comparison) ** 2, axis=(1, 2))) / 2.0
        )
        comparison_parseval_defect = abs(
            comparison_reciprocal_power - float(np.sum(comparison_powers))
        )
        blocks = tuple(
            SmoothFourStateHoppingBlockResult(
                displacement=displacement,
                reference_normalized_squared_frobenius_norm=float(reference_power),
                comparison_normalized_squared_frobenius_norm=float(comparison_power),
            )
            for displacement, reference_power, comparison_power in zip(
                parent.displacements,
                parent.reference_powers,
                comparison_powers,
                strict=True,
            )
        )
        return SmoothFourStatePointResult(
            amplitude=amplitude,
            maximum_band_defect=band_defect,
            splitting_scale=parent.splitting_scale,
            harmonic_maximum=maximum,
            discrete_maximum_correlation=correlation,
            minimum_operator_threshold=minimum_threshold,
            exact_spectrum_joint_operator_threshold=joint_threshold,
            minimum_loss_reconstruction_defect=reconstruction_defect,
            reference_nonzero_hopping_weight=parent.reference_nonzero_weight,
            comparison_nonzero_hopping_weight=comparison_nonzero,
            reference_parseval_defect=parent.reference_parseval_defect,
            comparison_parseval_defect=comparison_parseval_defect,
            hopping_blocks=blocks,
        )

    @staticmethod
    def _correlation_harmonic(
        reference: ComplexArray, comparison: ComplexArray
    ) -> PeriodicHarmonic:
        x_value = reference[:, 0, 1].real
        y_value = -reference[:, 0, 1].imag
        z_value = 0.5 * (reference[:, 0, 0].real - reference[:, 1, 1].real)
        target_x = comparison[:, 0, 1].real
        target_y = -comparison[:, 0, 1].imag
        target_z = 0.5 * (comparison[:, 0, 0].real - comparison[:, 1, 1].real)
        return PeriodicHarmonic(
            offset=float(np.mean(y_value * target_y)),
            cosine_coefficient=float(np.mean(x_value * target_x + z_value * target_z)),
            sine_coefficient=float(np.mean(x_value * target_z - z_value * target_x)),
            harmonic_order=2,
            fundamental_interval_start=-math.pi / 2.0,
        )

    @staticmethod
    def _fourier_blocks(
        coordinates: RealArray,
        matrices: ComplexArray,
        displacements: tuple[int, ...],
    ) -> ComplexArray:
        sample_count = coordinates.size
        evaluator = FiniteFourierSeriesEvaluatorFactory.create(
            FiniteFourierSeriesMethod.NUMPY_DENSE
        )
        evaluation_coordinates = tuple(
            (-float(displacement) / float(sample_count),)
            for displacement in displacements
        )
        sample_modes = tuple((index,) for index in range(sample_count))
        origin_shift = np.asarray(
            [(-1.0 if displacement % 2 else 1.0) for displacement in displacements],
            dtype=np.complex128,
        )
        blocks = np.empty(
            (len(displacements), matrices.shape[1], matrices.shape[2]),
            dtype=np.complex128,
        )
        for row in range(matrices.shape[1]):
            for column in range(matrices.shape[2]):
                definition = FiniteFourierSeriesEvaluationDefinition(
                    dimension=1,
                    coordinates=evaluation_coordinates,
                    integer_modes=sample_modes,
                    coefficients=tuple(
                        complex(value) / float(sample_count)
                        for value in matrices[:, row, column]
                    ),
                )
                result = evaluator.evaluate(definition)
                blocks[:, row, column] = origin_shift * np.asarray(
                    result.values, dtype=np.complex128
                )
        return blocks

    @staticmethod
    def _block_powers(
        displacements: tuple[int, ...],
        blocks: ComplexArray,
        identifier: str,
    ) -> RealArray:
        model = BlockHoppingModel(
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
        result = BlockHoppingPowerAnalyzer().execute(model)
        return np.asarray(
            tuple(power.frobenius_power.magnitude / 2.0 for power in result.powers),
            dtype=np.float64,
        )

    @staticmethod
    def _check_fourier_reconstruction(
        coordinates: RealArray,
        displacements: tuple[int, ...],
        blocks: ComplexArray,
        expected: ComplexArray,
        tolerance: float,
    ) -> None:
        evaluator = FiniteFourierSeriesEvaluatorFactory.create(
            FiniteFourierSeriesMethod.NUMPY_DENSE
        )
        owner_coordinates = tuple((float(value),) for value in coordinates)
        modes = tuple((value,) for value in displacements)
        reconstructed = np.empty_like(expected)
        for row in range(expected.shape[1]):
            for column in range(expected.shape[2]):
                definition = FiniteFourierSeriesEvaluationDefinition(
                    dimension=1,
                    coordinates=owner_coordinates,
                    integer_modes=modes,
                    coefficients=tuple(
                        complex(value) for value in blocks[:, row, column]
                    ),
                )
                result = evaluator.evaluate(definition)
                reconstructed[:, row, column] = np.asarray(
                    result.values, dtype=np.complex128
                )
        defect = float(np.max(np.abs(reconstructed - expected)))
        if defect > tolerance:
            raise FloatingPointError("Fourier interpolant fails node reconstruction")

    @staticmethod
    def _check_hopping_symmetry(
        displacements: tuple[int, ...],
        blocks: ComplexArray,
        tolerance: float,
    ) -> None:
        size = len(displacements)
        by_cyclic_class = {
            displacement % size: block
            for displacement, block in zip(displacements, blocks, strict=True)
        }
        defect = max(
            float(
                np.max(np.abs(by_cyclic_class[(-displacement) % size] - block.conj().T))
            )
            for displacement, block in zip(displacements, blocks, strict=True)
        )
        if defect > tolerance:
            raise FloatingPointError("Fourier blocks fail cyclic Hermitian symmetry")


class SmoothFourStateParentFamilyExperiment:
    """Evaluate the representation orbit across a parent-hopping homotopy."""

    __slots__ = ()

    def execute(
        self, definition: SmoothFourStateParentFamilyDefinition
    ) -> SmoothFourStateParentFamilyResult:
        """Evaluate every declared parent scale without changing other controls."""
        if type(definition) is not SmoothFourStateParentFamilyDefinition:
            raise TypeError("definition must be SmoothFourStateParentFamilyDefinition")
        experiment = SmoothFourStateExperiment()
        return SmoothFourStateParentFamilyResult(
            definition=definition,
            members=tuple(
                experiment.execute(definition.definition_at(scale))
                for scale in definition.parent_hopping_scales
            ),
        )


class SmoothFourStateConvergenceExperiment:
    """Apply conservative momentum convergence to the non-flat realization."""

    __slots__ = ()

    def execute(
        self, definition: SmoothFourStateConvergenceDefinition
    ) -> SmoothFourStateConvergenceResult:
        """Evaluate all meshes and derive the bounded stability disposition."""
        if type(definition) is not SmoothFourStateConvergenceDefinition:
            raise TypeError("definition must be SmoothFourStateConvergenceDefinition")
        experiment = SmoothFourStateExperiment()
        mesh_results = tuple(
            experiment.execute(definition.mesh_definition(size))
            for size in definition.reciprocal_mesh_sizes
        )
        refinements = tuple(
            self._refinement(definition, coarse, fine)
            for coarse, fine in zip(mesh_results[:-1], mesh_results[1:], strict=True)
        )
        required = definition.required_stable_refinements
        disposition = (
            SmoothFourStateConvergenceDisposition.CONVERGED
            if all(item.within_tolerances for item in refinements[-required:])
            else SmoothFourStateConvergenceDisposition.UNRESOLVED
        )
        return SmoothFourStateConvergenceResult(
            definition=definition,
            mesh_results=mesh_results,
            refinements=refinements,
            disposition=disposition,
        )

    @staticmethod
    def _refinement(
        definition: SmoothFourStateConvergenceDefinition,
        coarse: SmoothFourStateResult,
        fine: SmoothFourStateResult,
    ) -> SmoothFourStateRefinementResult:
        eigenvalue_defect, projector_defect = (
            SmoothFourStateConvergenceExperiment._shared_parent_invariant_defects(
                coarse.definition.reciprocal_mesh_size,
                fine.definition.reciprocal_mesh_size,
                definition.parent_hopping_scale,
            )
        )
        parent_change = max(
            abs(fine.minimum_external_gap - coarse.minimum_external_gap),
            eigenvalue_defect,
            projector_defect,
            abs(
                fine.maximum_frame_orthonormality_defect
                - coarse.maximum_frame_orthonormality_defect
            ),
            abs(fine.periodic_closure_defect - coarse.periodic_closure_defect),
            abs(
                fine.maximum_reference_hermiticity_defect
                - coarse.maximum_reference_hermiticity_defect
            ),
        )
        correlation_change = max(
            abs(
                fine_point.discrete_maximum_correlation
                - coarse_point.discrete_maximum_correlation
            )
            for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
        )
        threshold_change = max(
            max(
                abs(
                    fine_point.minimum_operator_threshold
                    - coarse_point.minimum_operator_threshold
                ),
                abs(
                    fine_point.exact_spectrum_joint_operator_threshold
                    - coarse_point.exact_spectrum_joint_operator_threshold
                ),
            )
            for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
        )
        hopping_weight_change = max(
            max(
                abs(
                    fine_point.reference_nonzero_hopping_weight
                    - coarse_point.reference_nonzero_hopping_weight
                ),
                abs(
                    fine_point.comparison_nonzero_hopping_weight
                    - coarse_point.comparison_nonzero_hopping_weight
                ),
            )
            for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
        )
        block_change = max(
            SmoothFourStateConvergenceExperiment._shared_block_change(
                coarse_point, fine_point
            )
            for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
        )
        statuses_stable = all(
            coarse_point.harmonic_maximum.status is fine_point.harmonic_maximum.status
            for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
        )
        angle_change = max(
            SmoothFourStateConvergenceExperiment._angle_change(coarse_point, fine_point)
            for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
        )
        band_defect = max(point.maximum_band_defect for point in fine.points)
        reconstruction_defect = max(
            point.minimum_loss_reconstruction_defect for point in fine.points
        )
        parseval_defect = max(
            max(point.reference_parseval_defect, point.comparison_parseval_defect)
            for point in fine.points
        )
        thresholds = definition.thresholds
        margin = definition.verification_absolute_tolerance
        within = (
            statuses_stable
            and parent_change + margin <= thresholds.maximum_parent_diagnostic_change
            and correlation_change + margin <= thresholds.maximum_correlation_change
            and threshold_change + margin <= thresholds.maximum_threshold_change
            and hopping_weight_change + margin
            <= thresholds.maximum_hopping_weight_change
            and block_change + margin <= thresholds.maximum_hopping_block_power_change
            and angle_change + margin <= thresholds.maximum_angle_change
            and band_defect + margin <= thresholds.maximum_band_defect
            and reconstruction_defect + margin
            <= thresholds.maximum_reconstruction_defect
            and parseval_defect + margin <= thresholds.maximum_parseval_defect
        )
        return SmoothFourStateRefinementResult(
            coarse_mesh_size=coarse.definition.reciprocal_mesh_size,
            fine_mesh_size=fine.definition.reciprocal_mesh_size,
            maximum_parent_diagnostic_change=parent_change,
            maximum_shared_parent_eigenvalue_defect=eigenvalue_defect,
            maximum_shared_projector_defect=projector_defect,
            maximum_correlation_change=correlation_change,
            maximum_threshold_change=threshold_change,
            maximum_hopping_weight_change=hopping_weight_change,
            maximum_hopping_block_power_change=block_change,
            maximum_angle_change=angle_change,
            maximizing_angle_dispositions_stable=statuses_stable,
            maximum_band_defect=band_defect,
            maximum_reconstruction_defect=reconstruction_defect,
            maximum_parseval_defect=parseval_defect,
            within_tolerances=within,
        )

    @staticmethod
    def _shared_parent_invariant_defects(
        coarse_size: int,
        fine_size: int,
        parent_hopping_scale: float,
    ) -> tuple[float, float]:
        coarse_coordinates = -0.5 + np.arange(coarse_size, dtype=np.float64) / float(
            coarse_size
        )
        fine_coordinates = -0.5 + np.arange(fine_size, dtype=np.float64) / float(
            fine_size
        )
        coarse_parent = SmoothFourStateExperiment._parent_matrices(
            coarse_coordinates, parent_hopping_scale
        )
        fine_parent = SmoothFourStateExperiment._parent_matrices(
            fine_coordinates, parent_hopping_scale
        )[::2]
        coarse_eigenvalues, coarse_eigenvectors = np.linalg.eigh(coarse_parent)
        fine_eigenvalues, fine_eigenvectors = np.linalg.eigh(fine_parent)
        eigenvalue_defect = float(np.max(np.abs(fine_eigenvalues - coarse_eigenvalues)))
        coarse_retained = coarse_eigenvectors[:, :, :2]
        fine_retained = fine_eigenvectors[:, :, :2]
        coarse_projectors = coarse_retained @ coarse_retained.conj().transpose(0, 2, 1)
        fine_projectors = fine_retained @ fine_retained.conj().transpose(0, 2, 1)
        projector_defect = float(
            np.max(
                np.linalg.norm(
                    fine_projectors - coarse_projectors, axis=(1, 2), ord="fro"
                )
            )
        )
        return eigenvalue_defect, projector_defect

    @staticmethod
    def _shared_block_change(
        coarse: SmoothFourStatePointResult,
        fine: SmoothFourStatePointResult,
    ) -> float:
        coarse_blocks = {item.displacement: item for item in coarse.hopping_blocks}
        fine_blocks = {item.displacement: item for item in fine.hopping_blocks}
        return max(
            max(
                abs(
                    fine_blocks[
                        displacement
                    ].reference_normalized_squared_frobenius_norm
                    - coarse_item.reference_normalized_squared_frobenius_norm
                ),
                abs(
                    fine_blocks[
                        displacement
                    ].comparison_normalized_squared_frobenius_norm
                    - coarse_item.comparison_normalized_squared_frobenius_norm
                ),
            )
            for displacement, coarse_item in coarse_blocks.items()
        )

    @staticmethod
    def _angle_change(
        coarse: SmoothFourStatePointResult,
        fine: SmoothFourStatePointResult,
    ) -> float:
        coarse_angle = coarse.harmonic_maximum.canonical_maximizing_argument
        fine_angle = fine.harmonic_maximum.canonical_maximizing_argument
        if coarse_angle is None and fine_angle is None:
            return 0.0
        if coarse_angle is None or fine_angle is None:
            return math.pi / 2.0
        raw = abs(fine_angle - coarse_angle)
        return min(raw, math.pi - raw)


class SmoothFourStateAdaptiveAmplitudeExperiment:
    """Refine failing intervals and validate them at disjoint quarter points."""

    __slots__ = ()

    def execute(
        self, definition: SmoothFourStateAdaptiveAmplitudeDefinition
    ) -> SmoothFourStateAdaptiveAmplitudeResult:
        """Cache direct samples and fail conservatively at either declared cap."""
        if type(definition) is not SmoothFourStateAdaptiveAmplitudeDefinition:
            raise TypeError(
                "definition must be SmoothFourStateAdaptiveAmplitudeDefinition"
            )
        experiment = SmoothFourStateExperiment()
        initial = definition.initial_definition
        parent = experiment._prepare_parent(initial)
        maximizer = PeriodicHarmonicMaximizer(
            absolute_degeneracy_tolerance=(
                initial.harmonic_absolute_degeneracy_tolerance
            ),
            relative_degeneracy_tolerance=(
                initial.harmonic_relative_degeneracy_tolerance
            ),
        )
        cache: dict[float, SmoothFourStatePointResult] = {}

        def evaluate(amplitudes: tuple[float, ...]) -> SmoothFourStateResult | None:
            new_amplitudes = tuple(
                amplitude for amplitude in amplitudes if amplitude not in cache
            )
            if (
                len(cache) + len(new_amplitudes)
                > definition.maximum_evaluated_amplitudes
            ):
                return None
            for amplitude in new_amplitudes:
                cache[amplitude] = experiment._point(
                    initial, parent, amplitude, maximizer
                )
            return SmoothFourStateResult(
                definition=definition.evaluation_definition(amplitudes),
                minimum_external_gap=parent.minimum_external_gap,
                minimum_transport_singular_value=(
                    parent.minimum_transport_singular_value
                ),
                maximum_frame_orthonormality_defect=(
                    parent.maximum_frame_orthonormality_defect
                ),
                periodic_closure_defect=parent.periodic_closure_defect,
                maximum_reference_hermiticity_defect=(
                    parent.maximum_reference_hermiticity_defect
                ),
                points=tuple(cache[amplitude] for amplitude in amplitudes),
            )

        nodes = initial.amplitudes
        levels: list[SmoothFourStateAmplitudeRefinementResult] = []
        validations: list[SmoothFourStateAmplitudeValidationResult] = []
        final_evaluation: SmoothFourStateResult | None = None
        for level_index in range(definition.maximum_refinement_levels):
            midpoints = tuple(
                0.5 * (left + right)
                for left, right in zip(nodes[:-1], nodes[1:], strict=True)
            )
            midpoint_inventory = tuple(sorted(set(nodes) | set(midpoints)))
            midpoint_evaluation = evaluate(midpoint_inventory)
            if midpoint_evaluation is None:
                break
            final_evaluation = midpoint_evaluation
            midpoint_defects = tuple(
                self._interpolation_defects(
                    cache[left], cache[midpoint], cache[right], 0.5
                )
                for left, midpoint, right in zip(
                    nodes[:-1], midpoints, nodes[1:], strict=True
                )
            )
            midpoint_failing = tuple(
                self._fails(definition, defects) for defects in midpoint_defects
            )
            level = SmoothFourStateAmplitudeRefinementResult(
                level_index=level_index,
                interpolation_nodes=nodes,
                evaluated_amplitudes=midpoint_inventory,
                maximum_correlation_midpoint_defect=max(
                    item[0] for item in midpoint_defects
                ),
                maximum_operator_threshold_midpoint_defect=max(
                    item[1] for item in midpoint_defects
                ),
                maximum_joint_threshold_midpoint_defect=max(
                    item[2] for item in midpoint_defects
                ),
                maximum_hopping_weight_midpoint_defect=max(
                    item[3] for item in midpoint_defects
                ),
                maximum_hopping_block_power_midpoint_defect=max(
                    item[4] for item in midpoint_defects
                ),
                failing_interval_count=sum(midpoint_failing),
                within_tolerances=not any(midpoint_failing),
            )
            levels.append(level)
            candidate_nodes = tuple(
                sorted(
                    set(nodes)
                    | {
                        midpoint
                        for midpoint, interval_fails in zip(
                            midpoints, midpoint_failing, strict=True
                        )
                        if interval_fails
                    }
                )
            )
            if level.within_tolerances:
                quarter_samples = tuple(
                    sample
                    for left, right in zip(nodes[:-1], nodes[1:], strict=True)
                    for sample in (
                        left + 0.25 * (right - left),
                        left + 0.75 * (right - left),
                    )
                )
                validation_inventory = tuple(sorted(set(nodes) | set(quarter_samples)))
                validation_evaluation = evaluate(validation_inventory)
                if validation_evaluation is None:
                    break
                final_evaluation = validation_evaluation
                validation_defects = tuple(
                    self._interpolation_defects(
                        cache[left], cache[sample], cache[right], fraction
                    )
                    for left, right in zip(nodes[:-1], nodes[1:], strict=True)
                    for sample, fraction in (
                        (left + 0.25 * (right - left), 0.25),
                        (left + 0.75 * (right - left), 0.75),
                    )
                )
                validation_failing = tuple(
                    self._fails(definition, defects) for defects in validation_defects
                )
                validation = SmoothFourStateAmplitudeValidationResult(
                    level_index=level_index,
                    interpolation_nodes=nodes,
                    evaluated_amplitudes=quarter_samples,
                    maximum_correlation_defect=max(
                        item[0] for item in validation_defects
                    ),
                    maximum_operator_threshold_defect=max(
                        item[1] for item in validation_defects
                    ),
                    maximum_joint_threshold_defect=max(
                        item[2] for item in validation_defects
                    ),
                    maximum_hopping_weight_defect=max(
                        item[3] for item in validation_defects
                    ),
                    maximum_hopping_block_power_defect=max(
                        item[4] for item in validation_defects
                    ),
                    failing_point_count=sum(validation_failing),
                    within_tolerances=not any(validation_failing),
                )
                validations.append(validation)
                if validation.within_tolerances:
                    return SmoothFourStateAdaptiveAmplitudeResult(
                        definition=definition,
                        levels=tuple(levels),
                        validations=tuple(validations),
                        all_evaluated_amplitudes=tuple(sorted(cache)),
                        final_evaluation=final_evaluation,
                        disposition=SmoothFourStateConvergenceDisposition.CONVERGED,
                    )
                candidate_nodes = tuple(
                    sorted(
                        set(nodes)
                        | {
                            sample
                            for sample, point_fails in zip(
                                quarter_samples, validation_failing, strict=True
                            )
                            if point_fails
                        }
                    )
                )
            if level_index + 1 >= definition.maximum_refinement_levels:
                break
            nodes = candidate_nodes
        if final_evaluation is None or not levels:
            raise RuntimeError("amplitude cap prevented the first required evaluation")
        return SmoothFourStateAdaptiveAmplitudeResult(
            definition=definition,
            levels=tuple(levels),
            validations=tuple(validations),
            all_evaluated_amplitudes=tuple(sorted(cache)),
            final_evaluation=final_evaluation,
            disposition=SmoothFourStateConvergenceDisposition.UNRESOLVED,
        )

    @staticmethod
    def _interpolation_defects(
        left: SmoothFourStatePointResult,
        sample: SmoothFourStatePointResult,
        right: SmoothFourStatePointResult,
        fraction: float,
    ) -> tuple[float, float, float, float, float]:
        def defect(left_value: float, sample_value: float, right_value: float) -> float:
            interpolated = (1.0 - fraction) * left_value + fraction * right_value
            return abs(sample_value - interpolated)

        left_blocks = {item.displacement: item for item in left.hopping_blocks}
        sample_blocks = {item.displacement: item for item in sample.hopping_blocks}
        right_blocks = {item.displacement: item for item in right.hopping_blocks}
        block_defect = max(
            defect(
                left_item.comparison_normalized_squared_frobenius_norm,
                sample_blocks[
                    displacement
                ].comparison_normalized_squared_frobenius_norm,
                right_blocks[displacement].comparison_normalized_squared_frobenius_norm,
            )
            for displacement, left_item in left_blocks.items()
        )
        return (
            defect(
                left.discrete_maximum_correlation,
                sample.discrete_maximum_correlation,
                right.discrete_maximum_correlation,
            ),
            defect(
                left.minimum_operator_threshold,
                sample.minimum_operator_threshold,
                right.minimum_operator_threshold,
            ),
            defect(
                left.exact_spectrum_joint_operator_threshold,
                sample.exact_spectrum_joint_operator_threshold,
                right.exact_spectrum_joint_operator_threshold,
            ),
            defect(
                left.comparison_nonzero_hopping_weight,
                sample.comparison_nonzero_hopping_weight,
                right.comparison_nonzero_hopping_weight,
            ),
            block_defect,
        )

    @staticmethod
    def _fails(
        definition: SmoothFourStateAdaptiveAmplitudeDefinition,
        defects: tuple[float, float, float, float, float],
    ) -> bool:
        thresholds = definition.thresholds
        margin = definition.initial_definition.verification_absolute_tolerance
        return any(
            defect + margin > threshold
            for defect, threshold in zip(
                defects,
                (
                    thresholds.maximum_correlation_midpoint_defect,
                    thresholds.maximum_operator_threshold_midpoint_defect,
                    thresholds.maximum_joint_threshold_midpoint_defect,
                    thresholds.maximum_hopping_weight_midpoint_defect,
                    thresholds.maximum_hopping_block_power_midpoint_defect,
                ),
                strict=True,
            )
        )


__all__ = [
    "SmoothFourStateAdaptiveAmplitudeExperiment",
    "SmoothFourStateConvergenceExperiment",
    "SmoothFourStateExperiment",
    "SmoothFourStateParentFamilyExperiment",
]
